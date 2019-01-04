import logging

from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.db.models import Min, Q
from django.db.transaction import atomic
from django.utils import timezone

from river.config import app_config
from river.hooking.completed import PostCompletedHooking, PreCompletedHooking
from river.hooking.transition import PostTransitionHooking, PreTransitionHooking
from river.models import TransitionApproval, TransitionApprovalMeta, PENDING, State, APPROVED
from river.signals import ProceedingSignal, TransitionSignal, FinalSignal
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

LOGGER = logging.getLogger(__name__)


class InstanceWorkflowObject(object):

    def __init__(self, workflow_object, name, field_name):
        self.class_workflow = getattr(workflow_object.__class__.river, name)
        self.workflow_object = workflow_object
        self.name = name
        self.field_name = field_name
        self.initialized = False

    def initialize_approvals(self):
        if not self.initialized and not TransitionApproval.objects.filter(workflow_object=self.workflow_object, field_name=self.name).count():
            content_type = app_config.CONTENT_TYPE_CLASS.objects.get_for_model(self.workflow_object)
            for transition_approval_meta in TransitionApprovalMeta.objects.filter(field_name=self.name, content_type=content_type):
                transition_approval, created = TransitionApproval.objects.update_or_create(
                    workflow_object=self.workflow_object,
                    field_name=transition_approval_meta.field_name,
                    source_state=transition_approval_meta.source_state,
                    destination_state=transition_approval_meta.destination_state,
                    priority=transition_approval_meta.priority,
                    meta=transition_approval_meta,
                    defaults={
                        'status': PENDING,
                    }
                )
                transition_approval.permissions.add(*transition_approval_meta.permissions.all())
                transition_approval.groups.add(*transition_approval_meta.groups.all())
            # self.workflow_object.save()
            self.initialized = True
            LOGGER.debug("Transition approvals are initialized for the workflow object %s" % self.workflow_object)

    @property
    def on_initial_state(self):
        return self.get_state() == self.class_workflow.initial_state

    @property
    def on_final_state(self):
        if self.class_workflow.final_states.count() == 0:
            raise RiverException(ErrorCode.NO_AVAILABLE_FINAL_STATE, 'There is no available final state for the content type %s.' % self._content_type)

        return self.get_state() in self.class_workflow.final_states

    @property
    def next_approvals(self):
        return self._get_next_approvals()

    @property
    def recent_approval(self):
        try:

            return getattr(self.workflow_object, self.name + "_transitions").filter(transaction_date__isnull=False).latest('transaction_date')
        except TransitionApproval.DoesNotExist:
            return None

    @property
    def _content_type(self):
        return ContentType.objects.get_for_model(self.workflow_object)

    # def get_available_transitions(self, as_user, *args, **kwargs):
    # from river.services.proceeding import ProceedingService
    # return ProceedingService.get_available_proceedings(self.workflow_object, [self.get_state()], user=as_user, *args, **kwargs)

    def get_available_states(self, as_user=None):
        transition_approvals = TransitionApproval.objects.filter(
            workflow_object=self.workflow_object,
            source_state=self.get_state(),
        )
        if as_user:
            transition_approvals = transition_approvals.filter(
                permissions__in=as_user.user_permissions.all()
            )
        destination_states = transition_approvals.values_list('destination_state', flat=True)
        return State.objects.filter(pk__in=destination_states)

    def get_available_approvals(self, as_user=None, source_states=None, destination_state=None, god_mod=False):
        def get_transition_approvals(transition_approvals):
            min_priority = transition_approvals.aggregate(Min('priority'))['priority__min']
            transition_approvals = transition_approvals.filter(priority=min_priority)

            if destination_state:
                transition_approvals = transition_approvals.filter(destination_state=destination_state)

            return transition_approvals

        def authorize_transition_approvals(transition_approvals):
            group_q = Q()
            for g in as_user.groups.all():
                group_q = group_q | Q(groups__in=[g])

            permissions = []
            for backend in auth.get_backends():
                permissions.extend(backend.get_all_permissions(as_user))

            permission_q = Q()
            for p in permissions:
                label, codename = p.split('.')
                permission_q = permission_q | Q(permissions__content_type__app_label=label,
                                                permissions__codename=codename)

            return transition_approvals.filter(
                (
                        (Q(transactioner__isnull=True) | Q(transactioner=as_user)) &
                        (Q(permissions__isnull=True) | permission_q) &
                        (Q(groups__isnull=True) | group_q)
                )
            )

        source_states = source_states or [self.get_state()]

        transition_approvals = TransitionApproval.objects.filter(
            workflow_object=self.workflow_object,
            field_name=self.name,
            source_state__in=source_states,
            status=PENDING,
            enabled=True
        )

        suitable_transition_approvals = get_transition_approvals(transition_approvals.filter(skip=False))

        if as_user and not god_mod:
            suitable_transition_approvals = authorize_transition_approvals(suitable_transition_approvals)

        skipped_transition_approvals = get_transition_approvals(transition_approvals.filter(skip=True))
        if skipped_transition_approvals:
            source_state_pks = list(skipped_transition_approvals.values_list('destination_state', flat=True))
            suitable_transition_approvals = suitable_transition_approvals | self.get_available_approvals(
                as_user=as_user,
                source_states=State.objects.filter(pk__in=source_state_pks),
                destination_state=destination_state,
                god_mod=god_mod
            )
        return suitable_transition_approvals

    @atomic
    def approve(self, as_user, next_state=None, god_mod=False):
        def process(action, next_state=None, god_mod=False):
            available_transition_approvals = self.get_available_approvals(as_user=as_user, god_mod=god_mod)
            c = available_transition_approvals.count()
            if c == 0:
                raise RiverException(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, "There is no available state for destination for the user.")
            if c > 1:
                if next_state:
                    available_transition_approvals = available_transition_approvals.filter(destination_state=next_state)
                    if available_transition_approvals.count() == 0:
                        available_states = self.get_available_states(as_user=as_user)
                        raise RiverException(ErrorCode.INVALID_NEXT_STATE_FOR_USER, "Invalid state is given(%s). Valid states is(are) %s" % (
                            next_state.__str__(), ','.join([ast.__str__() for ast in available_states])))
                else:
                    raise RiverException(ErrorCode.NEXT_STATE_IS_REQUIRED,
                                         "State must be given when there are multiple states for destination")

            available_transition_approval = available_transition_approvals[0]
            available_transition_approval.status = action
            available_transition_approval.transactioner = as_user
            available_transition_approval.transaction_date = timezone.now()
            if self.recent_approval:
                available_transition_approval.previous = self.recent_approval
            available_transition_approval.save()

            return available_transition_approval

        transition_approval = process(APPROVED, next_state, god_mod)

        # Any other transitions approval is left?
        rest_of_transition_approvals = self.get_available_approvals(destination_state=next_state, god_mod=True)

        transition_status = False
        previous_state = self.get_state()
        if rest_of_transition_approvals.count() == 0:
            self.set_state(transition_approval.destination_state)
            transition_status = True

            # Next states should be PENDING back again if there is circle.
            self._cycle_proceedings()
            # ProceedingService.get_next_proceedings(workflow_object).update(status=PENDING)

        with ProceedingSignal(self.workflow_object, self.field_name, transition_approval), \
             TransitionSignal(transition_status, self.workflow_object, self.field_name, transition_approval), \
             FinalSignal(self.workflow_object, self.field_name):
            self.workflow_object.save()

        LOGGER.debug("Workflow object %s is proceeded for next transition. Transition: %s -> %s" % (
            self.workflow_object, previous_state, self.get_state()))

    def _get_next_approvals(self, transition_approval_pks=None, current_states=None, index=0, limit=None):
        if not transition_approval_pks:
            transition_approval_pks = []
        index += 1
        current_states = list(current_states.values_list('pk', flat=True)) if current_states else [self.get_state()]
        next_approvals = TransitionApproval.objects.filter(
            workflow_object=self.workflow_object,
            field_name=self.name,
            source_state__in=current_states
        )
        if self.recent_approval:
            next_approvals = next_approvals.exclude(pk=self.recent_approval.pk)
        if next_approvals.exists() and not next_approvals.filter(pk__in=transition_approval_pks).exists() and (
                not limit or index < limit):
            proceedings = self._get_next_approvals(
                transition_approval_pks=transition_approval_pks + list(next_approvals.values_list('pk', flat=True)),
                current_states=State.objects.filter(pk__in=next_approvals.values_list('destination_state', flat=True)),
                index=index,
                limit=limit
            )
        else:
            proceedings = TransitionApproval.objects.filter(pk__in=transition_approval_pks)

        return proceedings

    @atomic
    def _cycle_proceedings(self):
        """
         Finds next proceedings and clone them for cycling if it exists.
        """
        next_approvals = self._get_next_approvals().exclude(
            status=PENDING).exclude(cloned=True)
        for ta in next_approvals:
            clone_transition_approval, c = TransitionApproval.objects.get_or_create(
                source_state=ta.source_state,
                destination_state=ta.destination_state,
                content_type=ta.content_type,
                object_id=ta.object_id,
                field_name=ta.field_name,
                skip=ta.skip,
                priority=ta.priority,
                enabled=ta.enabled,
                status=PENDING,
                meta=ta.meta
            )

            if c:
                clone_transition_approval.permissions.add(*ta.permissions.all())
                clone_transition_approval.groups.add(*ta.groups.all())
            next_approvals.update(cloned=True)

        return True if next_approvals.count() else False

    def get_state(self):
        return getattr(self.workflow_object, self.field_name)

    def set_state(self, state):
        return setattr(self.workflow_object, self.field_name, state)

    def hook_post_transition(self, callback, *args, **kwargs):
        PostTransitionHooking.register(callback, self.workflow_object, self.field_name, *args, **kwargs)

    def hook_pre_transition(self, callback, *args, **kwargs):
        PreTransitionHooking.register(callback, self.workflow_object, self.field_name, *args, **kwargs)

    def hook_post_complete(self, callback):
        PostCompletedHooking.register(callback, self.workflow_object, self.field_name)

    def hook_pre_complete(self, callback):
        PreCompletedHooking.register(callback, self.workflow_object, self.field_name)
