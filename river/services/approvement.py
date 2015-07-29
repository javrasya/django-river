from django.db.models import Min, Q

from river.models.approvement import Approvement, PENDING
from river.models.approvement_meta import ApprovementMeta
from river.models.state import State
from river.services.config import RiverConfig
from river.services.state import StateService

__author__ = 'ahmetdal'


class ApprovementService:
    def __init__(self):
        pass

    @staticmethod
    def init_approvements(workflow_object, field):
        content_type = RiverConfig.CONTENT_TYPE_CLASS.objects.get_for_model(workflow_object)
        for approvement_meta in ApprovementMeta.objects.filter(transition__content_type=content_type, transition__field=field):
            approvement, created = Approvement.objects.update_or_create(
                meta=approvement_meta,
                object=workflow_object,
                field=field,
                defaults={
                    'order': approvement_meta.order,
                    'status': PENDING,
                }
            )
            approvement.permissions.add(*approvement_meta.permissions.all())
            approvement.groups.add(*approvement_meta.groups.all())

        init_state = StateService.get_init_state(content_type, field)
        setattr(workflow_object, field, init_state)
        workflow_object.save()

    # @staticmethod
    # def apply_approvements(content_type_id, obj_id, field_id):
    #     content_type = ExternalContentType.objects.get(pk=content_type_id)
    #     field = Field.objects.get(pk=field_id)
    #     for approvement_meta in ApprovementMeta.objects.filter(transition__content_type=content_type):
    #         Approvement.objects.get_or_create(
    #             meta=approvement_meta,
    #             object_id=obj_id,
    #             content_type=content_type,
    #             field=field,
    #             defaults={
    #                 'status': PENDING
    #             }
    #         )

    @staticmethod
    def get_approvements_object_waiting_for_approval(workflow_object, field, user, source_states, include_user=True, destination_state=None):

        def get_approvement(approvements):
            min_order = approvements.aggregate(Min('order'))['order__min']
            approvements = approvements.filter(order=min_order)
            if include_user:
                approvements = approvements.filter(
                    (
                        (Q(transactioner__isnull=True) | Q(transactioner=user)) &
                        (Q(permissions__isnull=True) | Q(permissions__in=user.user_permissions.all())) &
                        (Q(groups__isnull=True) | Q(groups__in=user.groups.all()))
                    )
                )
            if destination_state:
                approvements = approvements.filter(meta__transition__destination_state=destination_state)

            return approvements

        approvements = Approvement.objects.filter(
            object=workflow_object,
            field=field,
            meta__transition__source_state__in=source_states,
            status=PENDING,
            enabled=True
        )
        all_approvements = get_approvement(approvements)
        unskipped_approvements = get_approvement(approvements.filter(skip=False))

        if all_approvements.count() == 0:
            return all_approvements
        elif unskipped_approvements.count() != 0:
            return unskipped_approvements
        else:
            source_state_pks = list(approvements.values_list('meta__transition__destination_state', flat=True))
            return ApprovementService.get_approvements_object_waiting_for_approval(workflow_object, field, user, State.objects.filter(pk__in=source_state_pks), include_user=False)

    @staticmethod
    def has_user_any_action(content_type, field, user):
        """
        :param content_type_id:
        :param field_id:
        :param user_id:
        :return: Boolean value indicates whether the user has any role for the content type and field are sent. Any elements existence
          accepted, rejected or pending for the user, means the user in active for the content type and field.
        """
        approvements = Approvement.objects.filter(Q(transactioner=user) | Q(meta__permission__in=user.permissions.all())).filter(content_type=content_type, field=field)
        return approvements.count() != 0

    @staticmethod
    def override_permissions(approvement, permissions):
        approvement.permissions.clear()
        approvement.permissions.add(*permissions)

    @staticmethod
    def override_groups(approvement, groups):
        approvement.groups.clear()
        approvement.groups.add(*groups)
