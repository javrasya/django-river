import logging

import six
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.transaction import atomic
from django.utils import timezone

from river.config import app_config
from river.hooking.completed import PostCompletedHooking, PreCompletedHooking
from river.hooking.transition import PostTransitionHooking, PreTransitionHooking
from river.models import TransitionApproval, PENDING, State, APPROVED, Workflow
from river.signals import ApproveSignal, TransitionSignal, OnCompleteSignal
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException

LOGGER = logging.getLogger(__name__)


class InstanceWorkflowObject(object):

    def __init__(self, workflow_object, name, field_name):
        self.class_workflow = getattr(workflow_object.__class__.river, name)
        self.workflow_object = workflow_object
        self.content_type = app_config.CONTENT_TYPE_CLASS.objects.get_for_model(self.workflow_object)
        self.name = name
        self.field_name = field_name
        self.initialized = False

    @transaction.atomic
    def initialize_approvals(self):
        if not self.initialized:
            workflow = Workflow.objects.filter(content_type=self.content_type, field_name=self.field_name).first()
            if workflow and workflow.transition_approvals.filter(workflow_object=self.workflow_object).count() == 0:
                transition_approval_metas = workflow.transition_approval_metas.all()
                meta_dict = six.moves.reduce(
                    lambda agg, meta: dict(agg, **{self._to_key(meta.source_state): agg.get(self._to_key(meta.source_state), []) + [meta]}),
                    transition_approval_metas,
                    {})

                next_metas = meta_dict.get(self._to_key(self.class_workflow.initial_state), [])
                while next_metas:
                    source_states = []
                    for next_meta in next_metas:

                        transition_approval, created = TransitionApproval.objects.update_or_create(
                            workflow_object=self.workflow_object,
                            source_state=next_meta.source_state,
                            destination_state=next_meta.destination_state,
                            priority=next_meta.priority,
                            meta=next_meta,
                            workflow=workflow,
                            defaults={
                                'status': PENDING,
                            }
                        )
                        if created:
                            source_states.append(next_meta.destination_state)
                            transition_approval.permissions.add(*next_meta.permissions.all())
                            transition_approval.groups.add(*next_meta.groups.all())
                    next_metas = [m for source_state in source_states for m in meta_dict.get(self._to_key(source_state), [])]
                self.initialized = True
                LOGGER.debug("Transition approvals are initialized for the workflow object %s" % self.workflow_object)

    @property
    def on_initial_state(self):
        return self.get_state() == self.class_workflow.initial_state

    @property
    def on_final_state(self):
        return self.class_workflow.final_states.filter(pk=self.get_state().pk).count() > 0

    @property
    def next_approvals(self):
        return TransitionApproval.objects.filter(
            content_type=self.content_type,
            field_name=self.field_name,
            object_id=self.workflow_object.pk,
            source_state=self.get_state()
        )

    @property
    def recent_approval(self):
        try:
            return getattr(self.workflow_object, self.name + "_transitions").filter(transaction_date__isnull=False).latest('transaction_date')
        except TransitionApproval.DoesNotExist:
            return None

    def get_available_states(self, as_user=None):
        all_destination_state_ids = self.get_available_approvals(as_user=as_user).values_list('destination_state', flat=True)
        return State.objects.filter(pk__in=all_destination_state_ids)

    def get_available_approvals(self, as_user=None, destination_state=None):
        qs = self.class_workflow.get_available_approvals(as_user).filter(object_id=self.workflow_object.pk)
        if destination_state:
            qs = qs.filter(destination_state=destination_state)

        return qs

    @atomic
    def approve(self, as_user, next_state=None):
        available_approvals = self.get_available_approvals(as_user=as_user)
        number_of_available_approvals = available_approvals.count()
        if number_of_available_approvals == 0:
            raise RiverException(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, "There is no available approval for the user.")
        elif next_state:
            available_approvals = available_approvals.filter(destination_state=next_state)
            if available_approvals.count() == 0:
                available_states = self.get_available_states(as_user)
                raise RiverException(ErrorCode.INVALID_NEXT_STATE_FOR_USER, "Invalid state is given(%s). Valid states is(are) %s" % (
                    next_state.__str__(), ','.join([ast.__str__() for ast in available_states])))
        elif number_of_available_approvals > 1 and not next_state:
            raise RiverException(ErrorCode.NEXT_STATE_IS_REQUIRED, "State must be given when there are multiple states for destination")

        approval = available_approvals.first()
        approval.status = APPROVED
        approval.transactioner = as_user
        approval.transaction_date = timezone.now()
        approval.previous = self.recent_approval
        approval.save()

        has_transit = False
        if approval.peers.filter(status=PENDING).count() == 0:
            previous_state = self.get_state()
            self.set_state(approval.destination_state)
            has_transit = True
            if self._check_if_it_cycled(approval.destination_state):
                self._re_create_cycled_path(approval.destination_state)
            LOGGER.debug("Workflow object %s is proceeded for next transition. Transition: %s -> %s" % (
                self.workflow_object, previous_state, self.get_state()))

        with self._approve_signal(approval), self._transition_signal(has_transit, approval), self._on_complete_signal():
            self.workflow_object.save()

    def _approve_signal(self, approval):
        return ApproveSignal(self.workflow_object, self.field_name, approval)

    def _transition_signal(self, has_transit, approval):
        return TransitionSignal(has_transit, self.workflow_object, self.field_name, approval)

    def _on_complete_signal(self):
        return OnCompleteSignal(self.workflow_object, self.field_name)

    def hook_post_transition(self, callback, *args, **kwargs):
        PostTransitionHooking.register(callback, self.workflow_object, self.field_name, *args, **kwargs)

    def hook_pre_transition(self, callback, *args, **kwargs):
        PreTransitionHooking.register(callback, self.workflow_object, self.field_name, *args, **kwargs)

    def hook_post_complete(self, callback):
        PostCompletedHooking.register(callback, self.workflow_object, self.field_name)

    def hook_pre_complete(self, callback):
        PreCompletedHooking.register(callback, self.workflow_object, self.field_name)

    @property
    def _content_type(self):
        return ContentType.objects.get_for_model(self.workflow_object)

    def _to_key(self, source_state):
        return str(self.content_type.pk) + self.field_name + source_state.label

    def _check_if_it_cycled(self, new_state):
        return TransitionApproval.objects.filter(
            workflow_object=self.workflow_object,
            workflow=self.class_workflow.workflow,
            source_state=new_state,
            status=APPROVED
        ).count() > 0

    def _re_create_cycled_path(self, from_state):
        approvals = TransitionApproval.objects.filter(workflow_object=self.workflow_object, workflow=self.class_workflow.workflow, source_state=from_state)
        cycle_ended = False
        while not cycle_ended:
            for old_approval in approvals:
                if old_approval.enabled:
                    cycled_approval, _ = TransitionApproval.objects.get_or_create(
                        source_state=old_approval.source_state,
                        destination_state=old_approval.destination_state,
                        workflow=old_approval.workflow,
                        object_id=old_approval.workflow_object.pk,
                        content_type=old_approval.content_type,
                        skipped=False,
                        priority=old_approval.priority,
                        enabled=True,
                        status=PENDING,
                        meta=old_approval.meta
                    )
                    cycled_approval.permissions.set(old_approval.permissions.all())
                    cycled_approval.groups.set(old_approval.groups.all())
            approvals = TransitionApproval.objects.filter(
                workflow_object=self.workflow_object,
                workflow=self.class_workflow.workflow,
                source_state__in=approvals.values_list("destination_state", flat=TransitionApproval)
            )
            cycle_ended = approvals.filter(source_state=from_state).count() > 0

    def get_state(self):
        return getattr(self.workflow_object, self.field_name)

    def set_state(self, state):
        return setattr(self.workflow_object, self.field_name, state)
