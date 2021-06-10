import logging

import six
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q, Max
from django.db.transaction import atomic
from django.utils import timezone

from river.config import app_config
from river.models import TransitionApproval, PENDING, State, APPROVED, Workflow, CANCELLED, Transition, DONE, JUMPED
from river.signals import ApproveSignal, TransitionSignal, OnCompleteSignal
from river.utils.error_code import ErrorCode
from river.utils.exceptions import RiverException
from functools import lru_cache

LOGGER = logging.getLogger(__name__)


@lru_cache(None)
def get_cached_workflow(field_name, content_type):
    return Workflow.objects.filter(field_name=field_name, content_type=content_type).first()


class InstanceWorkflowObject(object):
    def __init__(self, workflow_object, field_name):
        self.class_workflow = getattr(workflow_object.__class__.river, field_name)
        self.workflow_object = workflow_object
        self.content_type = app_config.CONTENT_TYPE_CLASS.objects.get_for_model(self.workflow_object)
        self.field_name = field_name
        self.workflow = get_cached_workflow(content_type=self.content_type, field_name=self.field_name)

    @transaction.atomic
    def initialize_approvals(self, iteration=0):
        transition_meta_list = self.workflow.transition_metas.filter(source_state=self.get_state() or self.workflow.initial_state)
        if transition_meta_list:
            for transition_meta in transition_meta_list:
                transition = Transition.objects.create(
                    workflow=self.workflow,
                    workflow_object=self.workflow_object,
                    source_state=transition_meta.source_state,
                    destination_state=transition_meta.destination_state,
                    meta=transition_meta,
                    iteration=iteration
                )
                for transition_approval_meta in transition_meta.transition_approval_meta.all():
                    transition_approval = TransitionApproval.objects.create(
                        workflow=self.workflow,
                        workflow_object=self.workflow_object,
                        transition=transition,
                        priority=transition_approval_meta.priority,
                        meta=transition_approval_meta
                    )
                    transition_approval.permissions.add(*transition_approval_meta.permissions.all())
                    transition_approval.groups.add(*transition_approval_meta.groups.all())
        LOGGER.debug("Next iteration transition approvals are initialized for the workflow object %s" % self.workflow_object)

    @property
    def on_initial_state(self):
        return self.get_state() == self.class_workflow.initial_state

    @property
    def on_final_state(self):
        return self.class_workflow.final_states.filter(pk=self.get_state().pk).count() > 0

    @property
    def next_approvals(self):
        transitions = Transition.objects.filter(workflow=self.workflow, object_id=self.workflow_object.pk, source_state=self.get_state())
        return TransitionApproval.objects.filter(transition__in=transitions)

    @property
    def recent_approval(self):
        try:
            return getattr(self.workflow_object, self.field_name + "_transition_approvals").filter(transaction_date__isnull=False).latest('transaction_date')
        except TransitionApproval.DoesNotExist:
            return None

    @transaction.atomic
    def jump_to(self, state):
        def _transitions_before(iteration):
            return Transition.objects.filter(workflow=self.workflow, workflow_object=self.workflow_object, iteration__lte=iteration)

        try:
            recent_iteration = self.recent_approval.transition.iteration if self.recent_approval else 0
            jumped_transition = getattr(self.workflow_object, self.field_name + "_transitions").filter(
                iteration__gte=recent_iteration, destination_state=state, status=PENDING
            ).earliest("iteration")

            jumped_transitions = _transitions_before(jumped_transition.iteration).filter(status=PENDING)
            for approval in TransitionApproval.objects.filter(pk__in=jumped_transitions.values_list("transition_approvals__pk", flat=True)):
                approval.status = JUMPED
                approval.save()
            jumped_transitions.update(status=JUMPED)
            self.set_state(state)
            self.workflow_object.save()

        except Transition.DoesNotExist:
            raise RiverException(ErrorCode.STATE_IS_NOT_AVAILABLE_TO_BE_JUMPED, "This state is not available to be jumped in the future of this object")

    def get_available_states(self, as_user=None):
        all_destination_state_ids = self.get_available_approvals(as_user=as_user).values_list('transition__destination_state', flat=True)
        return State.objects.filter(pk__in=all_destination_state_ids)

    def get_available_approvals(self, as_user=None, destination_state=None):
        qs = self.class_workflow.get_available_approvals(as_user, ).filter(object_id=self.workflow_object.pk)
        if destination_state:
            qs = qs.filter(transition__destination_state=destination_state)

        return qs

    @atomic
    def approve(self, as_user, next_state=None):
        available_approvals = self.get_available_approvals(as_user=as_user)
        number_of_available_approvals = available_approvals.count()
        if number_of_available_approvals == 0:
            raise RiverException(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER, "There is no available approval for the user.")
        elif next_state:
            available_approvals = available_approvals.filter(transition__destination_state=next_state)
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

        if next_state:
            self.cancel_impossible_future(approval)

        has_transit = False
        if approval.peers.filter(status=PENDING).count() == 0:
            approval.transition.status = DONE
            approval.transition.save()
            previous_state = self.get_state()
            self.set_state(approval.transition.destination_state)
            has_transit = True

        LOGGER.debug("Workflow object %s is proceeded for next transition. Transition: %s -> %s" % (   
                self.workflow_object, previous_state, self.get_state()))

        if next_state:
            self.initialize_approvals(approval.transition.iteration + 1)
        
        with self._approve_signal(approval), self._transition_signal(has_transit, approval), self._on_complete_signal():
            self.workflow_object.save()


    @atomic
    def cancel_impossible_future(self, approved_approval):
        transition = approved_approval.transition

        cancelled_transitions = Transition.objects.filter(
            workflow=self.workflow,
            object_id=self.workflow_object.pk,
            status=PENDING,
            iteration__gte=transition.iteration
        ).exclude(pk=transition.pk)

        TransitionApproval.objects.filter(transition__in=cancelled_transitions).update(status=CANCELLED)
        cancelled_transitions.update(status=CANCELLED)

    def _approve_signal(self, approval):
        return ApproveSignal(self.workflow_object, self.field_name, approval)

    def _transition_signal(self, has_transit, approval):
        return TransitionSignal(has_transit, self.workflow_object, self.field_name, approval)

    def _on_complete_signal(self):
        return OnCompleteSignal(self.workflow_object, self.field_name)

    @property
    def _content_type(self):
        return ContentType.objects.get_for_model(self.workflow_object)

    def _to_key(self, source_state):
        return str(self.content_type.pk) + self.field_name + source_state.label

    def _get_transition_images(self, source_states):
        meta_max_iteration = Transition.objects.filter(
            workflow=self.workflow,
            workflow_object=self.workflow_object,
            source_state__pk__in=source_states,
        ).values_list("meta").annotate(max_iteration=Max("iteration"))

        return Transition.objects.filter(
            Q(workflow=self.workflow, object_id=self.workflow_object.pk) &
            six.moves.reduce(lambda agg, q: q | agg, [Q(meta__id=meta_id, iteration=max_iteration) for meta_id, max_iteration in meta_max_iteration], Q(pk=-1))
        )

    def get_state(self):
        return getattr(self.workflow_object, self.field_name)

    def set_state(self, state):
        return setattr(self.workflow_object, self.field_name, state)
