import inspect
import logging
from datetime import datetime

from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.db.models import CASCADE, Min, Q
from django.db.models.signals import post_save
from django.db.transaction import atomic

from river.config import app_config
from river.models.transitionapprovalmeta import TransitionApprovalMeta
from river.signals import ProceedingSignal, TransitionSignal, FinalSignal
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation

from river.models.state import State
from river.models.transitionapproval import TransitionApproval, PENDING, APPROVED

__author__ = 'ahmetdal'

from django.db import models

LOGGER = logging.getLogger(__name__)


class WorkflowRegistry(object):
    def __init__(self):
        self.workflows = {}

    def add(self, name, cls):
        self.workflows[id(cls)] = self.workflows.get(id(cls), set())
        self.workflows[id(cls)].add(name)


workflow_registry = WorkflowRegistry()


class ClassWorkflowObject(object):

    def __init__(self, workflow_class, name, field_name):
        self.workflow_class = workflow_class
        self.name = name
        self.field_name = field_name

    @property
    def _content_type(self):
        return ContentType.objects.get_for_model(self.workflow_class)

    def get_objects_waiting_for_approval(self, as_user):
        object_pks = []
        for workflow_object in self.workflow_class.objects.all():
            instance_workflow = getattr(workflow_object.river, self.name)
            transition_approvals = instance_workflow.get_available_transition_approvals(as_user=as_user)
            if transition_approvals.count():
                object_pks.append(workflow_object.pk)
        return self.workflow_class.objects.filter(pk__in=object_pks)

    @property
    def initial_state(self):
        initial_states = State.objects.filter(
            pk__in=TransitionApprovalMeta.objects.filter(
                content_type=self._content_type,
                workflow__name=self.name,
                parents__isnull=True
            ).values_list("source_state", flat=True)
        )
        if initial_states.count() == 0:
            raise RiverException(ErrorCode.NO_AVAILABLE_INITIAL_STATE, 'There is no available initial state for the content type %s. ' % self._content_type)
        elif initial_states.count() > 1:
            raise RiverException(ErrorCode.MULTIPLE_INITIAL_STATE,
                                 'There are multiple initial state for the content type %s. Have only one initial state' % self._content_type)

        return initial_states[0]

    @property
    def final_states(self):
        return State.objects.filter(
            pk__in=TransitionApprovalMeta.objects.filter(
                workflow__name=self.name,
                children__isnull=True,
                content_type=self._content_type
            ).values_list("destination_state", flat=True)
        )


class InstanceWorkflowObject(object):

    def __init__(self, workflow_object, name, field_name):
        self.class_workflow = getattr(workflow_object.__class__.river, name)
        self.workflow_object = workflow_object
        self.name = name
        self.field_name = field_name
        self.initialized = False

    def initialize_transitions(self):
        if not self.initialized and not TransitionApproval.objects.filter(workflow_object=self.workflow_object, workflow__name=self.name).count():
            content_type = app_config.CONTENT_TYPE_CLASS.objects.get_for_model(self.workflow_object)
            for transition_approval_meta in TransitionApprovalMeta.objects.filter(workflow__name=self.name, content_type=content_type):
                transition_approval, created = TransitionApproval.objects.update_or_create(
                    workflow_object=self.workflow_object,
                    workflow=transition_approval_meta.workflow,
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
    def is_complete(self):
        return TransitionApproval.objects.filter(
            workflow_object=self.workflow_object,
            workflow__name=self.name,
            source_state=self.get_state()
        ).count() == 0

    @property
    def on_initial_state(self):
        return self.get_state() == self.class_workflow.initial_state

    @property
    def on_final_state(self):
        if self.class_workflow.final_states.count() == 0:
            raise RiverException(ErrorCode.NO_AVAILABLE_FINAL_STATE, 'There is no available final state for the content type %s.' % self._content_type)

        return self.get_state() in self.class_workflow.final_states

    @property
    def next_transition_approvals(self):
        return self._get_next_transition_approvals()

    @property
    def current_transition_approval(self):
        try:

            return getattr(self.workflow_object, "transitions_in_" + self.name).filter(transaction_date__isnull=False).latest('transaction_date')
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

    def get_available_transition_approvals(self, as_user=None, source_states=None, destination_state=None, god_mod=False):
        def get_transition_approvals(transition_approvals):
            min_priority = transition_approvals.aggregate(Min('priority'))['priority__min']
            min_priority = min_priority if min_priority is not None else -1
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
            workflow__name=self.name,
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
            suitable_transition_approvals = skipped_transition_approvals | self.get_available_transition_approvals(
                as_user=as_user,
                source_states=State.objects.filter(pk__in=source_state_pks),
                destination_state=destination_state,
                god_mod=god_mod
            )
        return suitable_transition_approvals

    @atomic
    def proceed(self, as_user, next_state=None, god_mod=False):
        def process(action, next_state=None, god_mod=False):
            available_transition_approvals = self.get_available_transition_approvals(as_user=as_user, god_mod=god_mod)
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
            available_transition_approval.transaction_date = datetime.now()
            if self.current_transition_approval:
                available_transition_approval.previous = self.current_transition_approval
            available_transition_approval.save()

            return available_transition_approval

        transition_approval = process(APPROVED, next_state, god_mod)

        # Any other transitions approval is left?
        rest_of_transition_approvals = self.get_available_transition_approvals(destination_state=next_state, god_mod=True)

        transition_status = False
        if rest_of_transition_approvals.count() == 0:
            self.set_state(transition_approval.destination_state)
            transition_status = True

            # Next states should be PENDING back again if there is circle.
            self._cycle_proceedings()
            # ProceedingService.get_next_proceedings(workflow_object).update(status=PENDING)

        with ProceedingSignal(self.workflow_object, transition_approval), TransitionSignal(transition_status, self.workflow_object, transition_approval), FinalSignal(self.workflow_object, self.name):
            self.workflow_object.save()

        LOGGER.debug("Workflow object %s is proceeded for next transition. Transition: %s -> %s" % (
            self.workflow_object, self.get_state().label, self.get_state()))

    def _get_next_transition_approvals(self, transition_approval_pks=None, current_states=None, index=0, limit=None):
        if not transition_approval_pks:
            transition_approval_pks = []
        index += 1
        current_states = list(current_states.values_list('pk', flat=True)) if current_states else [self.get_state()]
        next_transition_approvals = TransitionApproval.objects.filter(
            workflow_object=self.workflow_object,
            workflow__name=self.name,
            source_state__in=current_states
        )
        if self.current_transition_approval:
            next_transition_approvals = next_transition_approvals.exclude(pk=self.current_transition_approval.pk)
        if next_transition_approvals.exists() and not next_transition_approvals.filter(pk__in=transition_approval_pks).exists() and (
                not limit or index < limit):
            proceedings = self._get_next_transition_approvals(
                transition_approval_pks=transition_approval_pks + list(next_transition_approvals.values_list('pk', flat=True)),
                current_states=State.objects.filter(pk__in=next_transition_approvals.values_list('destination_state', flat=True)),
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
        next_transition_approvals = self._get_next_transition_approvals().exclude(
            status=PENDING).exclude(cloned=True)
        for ta in next_transition_approvals:
            clone_transition_approval, c = TransitionApproval.objects.get_or_create(
                source_state=ta.source_state,
                destination_state=ta.destination_state,
                content_type=ta.content_type,
                object_id=ta.object_id,
                workflow=ta.workflow,
                skip=ta.skip,
                priority=ta.priority,
                enabled=ta.enabled,
                status=PENDING)

            if c:
                clone_transition_approval.permissions.add(*ta.permissions.all())
                clone_transition_approval.groups.add(*ta.groups.all())
            next_transition_approvals.update(cloned=True)

        return True if next_transition_approvals.count() else False

    def get_state(self):
        return getattr(self.workflow_object, self.field_name)

    def set_state(self, state):
        return setattr(self.workflow_object, self.field_name, state)


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(instance) if instance else self.getter(owner)


class RiverObject(object):

    def __init__(self, owner, field_name):
        self.owner = owner
        self.field_name = field_name
        self.is_class = inspect.isclass(owner)

    def __getattr__(self, workflow_name):
        cls = self.owner if self.is_class else self.owner.__class__
        if workflow_name not in workflow_registry.workflows[id(cls)]:
            raise Exception("Workflow with name:%s doesn't exist for class:%s" % (workflow_name, cls.__name__))
        if self.is_class:
            return ClassWorkflowObject(self.owner, workflow_name, self.field_name)
        else:
            return InstanceWorkflowObject(self.owner, workflow_name, self.field_name)

    def all(self, cls):
        return list([getattr(self, workflow_name) for workflow_name in workflow_registry.workflows[id(cls)]])


registered_classes = set()


class StateField(models.ForeignKey):
    def __init__(self, workflow_name, *args, **kwargs):
        self.workflow_name = workflow_name
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['to'] = '%s.%s' % (State._meta.app_label, State._meta.object_name)
        kwargs['on_delete'] = kwargs.get('on_delete', CASCADE)
        super(StateField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        args = [self.workflow_name] + args
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name):
        @classproperty
        def river(_self):
            return RiverObject(_self, name)

        workflow_registry.add(self.workflow_name, cls)

        self._add_to_class(cls, "transitions_in_" + self.workflow_name, GenericRelation('%s.%s' % (TransitionApproval._meta.app_label, TransitionApproval._meta.object_name)))

        if cls not in registered_classes:
            self._add_to_class(cls, "river", river)

        super(StateField, self).contribute_to_class(cls, name)

        if cls not in registered_classes:
            post_save.connect(_post_save, self.model, False, dispatch_uid='%s_%s_riverstatefield_post' % (self.model, name))

        registered_classes.add(cls)

    @staticmethod
    def _add_to_class(cls, key, value, ignore_exists=False):
        if ignore_exists or not hasattr(cls, key):
            cls.add_to_class(key, value)


def _post_save(sender, instance, created, *args, **kwargs):  # signal, sender, instance):
    for workflow in instance.river.all(instance.__class__):
        if created:
            workflow.initialize_transitions()
        if not workflow.get_state():
            init_state = getattr(instance.__class__.river, workflow.name).initial_state
            workflow.set_state(init_state)
            instance.save()
