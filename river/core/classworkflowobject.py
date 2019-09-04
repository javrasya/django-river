from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.db.models import Window, F, Q, IntegerField
from django.db.models.functions import Rank, Cast
from django_cte import With

from river.models import State, TransitionApprovalMeta, TransitionApproval, PENDING, Workflow


class ClassWorkflowObject(object):

    def __init__(self, wokflow_object_class, name, field_name):
        self.wokflow_object_class = wokflow_object_class
        self.name = name
        self.field_name = field_name
        self._cached_workflow = None

    @property
    def workflow(self):
        if not self._cached_workflow:
            self._cached_workflow = Workflow.objects.filter(field_name=self.field_name, content_type=self._content_type).first()
        return self._cached_workflow

    def get_on_approval_objects(self, as_user):
        approvals = self.get_available_approvals(as_user)
        object_ids = list(approvals.values_list('object_id', flat=True))
        return self.wokflow_object_class.objects.filter(pk__in=object_ids)

    def get_available_approvals(self, as_user):
        approvals_with_priority_rank = With(
            TransitionApproval.objects.filter(workflow=self.workflow, status=PENDING, skipped=False, enabled=True).annotate(
                priority_rank=Window(
                    expression=Rank(),
                    order_by=F('priority').asc(),
                    partition_by=[F('workflow'), F('object_id'), F('source_state'), F('destination_state')])
            )
        )

        workflow_objects = With(
            self.wokflow_object_class.objects.all(),
            name="workflow_object"
        )

        approvals_after_ranking = approvals_with_priority_rank \
            .join(self._authorized_approvals(as_user), id=approvals_with_priority_rank.col.id) \
            .with_cte(approvals_with_priority_rank) \
            .annotate(object_id_as_int=Cast('object_id', IntegerField()), priority_rank=approvals_with_priority_rank.col.priority_rank) \
            .filter(priority_rank=1)

        return workflow_objects.join(approvals_after_ranking, object_id_as_int=workflow_objects.col.pk) \
            .with_cte(workflow_objects) \
            .filter(source_state=getattr(workflow_objects.col, self.field_name + "_id"))

    @property
    def initial_state(self):
        workflow = Workflow.objects.filter(content_type=self._content_type, field_name=self.name).first()
        return workflow.initial_state if workflow else None

    @property
    def final_states(self):
        final_approvals = TransitionApprovalMeta.objects.filter(workflow=self.workflow, children__isnull=True)
        return State.objects.filter(pk__in=final_approvals.values_list("destination_state", flat=True))

    def _authorized_approvals(self, as_user):
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

        return TransitionApproval.objects.filter(
            Q(workflow=self.workflow, status=PENDING) &
            (
                    (Q(transactioner__isnull=True) | Q(transactioner=as_user)) &
                    (Q(permissions__isnull=True) | permission_q) &
                    (Q(groups__isnull=True) | group_q)
            )
        )

    @property
    def _content_type(self):
        return ContentType.objects.get_for_model(self.wokflow_object_class)
