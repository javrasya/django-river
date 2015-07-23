from django.db.models import Min, Q

from river.models.approvement import Approvement, PENDING
from river.models.approvement_meta import ApprovementMeta
from river.models.object import Object
from river.models.state import State
from river.models.field import Field
from river.services.state import StateService

__author__ = 'ahmetdal'


class ApprovementService:
    def __init__(self):
        pass

    @staticmethod
    def init_approvements(content_type_id, obj_id, field_id):
        content_type = ExternalContentType.objects.get(pk=content_type_id)
        field = Field.objects.get(pk=field_id)
        for approvement_meta in ApprovementMeta.objects.filter(transition__content_type__pk=content_type_id, transition__field__pk=field_id):
            approvement, created = Approvement.objects.update_or_create(
                meta=approvement_meta,
                object_id=obj_id,
                content_type=content_type,
                field=field,
                defaults={
                    'status': PENDING,
                }
            )
            approvement.permissions.add(*approvement_meta.permission.all())
            approvement.groups.add(*approvement_meta.groups.all())

        init_state = StateService.get_init_state(content_type_id, field_id)
        Object.objects.update_or_create(object_id=obj_id, content_type=content_type, field=field, defaults={'state': init_state})

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
    def get_approvements_object_waiting_for_approval(content_type_id, object_id, field_id, user_id, source_states, include_user=True, destination_state_id=None):

        def get_approvement(approvements):
            min_order = approvements.aggregate(Min('meta__order'))['meta__order__min']
            approvements = approvements.filter(meta__order=min_order)
            if include_user:
                user = ExternalUser.objects.get(user_id=user_id)
                approvements = approvements.filter(
                    (
                        (Q(transactioner__isnull=True) | Q(transactioner=user)) &
                        (Q(permissions__isnull=True) | Q(permissions__in=user.permissions.all())) &
                        (Q(groups__isnull=True) | Q(groups__in=user.groups.all()))
                    )
                )
            if destination_state_id:
                approvements = approvements.filter(meta__transition__destination_state__pk=destination_state_id)

            return approvements

        content_type = ExternalContentType.objects.get(pk=content_type_id)
        field = Field.objects.get(pk=field_id)

        approvements = Approvement.objects.filter(
            content_type=content_type,
            object_id=object_id,
            field=field,
            meta__transition__source_state__in=source_states,
            status=PENDING
        )
        all_approvements = get_approvement(approvements)
        unskipped_approvements = get_approvement(approvements.filter(skip=False))

        if all_approvements.count() == 0:
            return all_approvements
        elif unskipped_approvements.count() != 0:
            return unskipped_approvements
        else:
            source_state_pks = list(approvements.values_list('meta__transition__destination_state', flat=True))
            return ApprovementService.get_approvements_object_waiting_for_approval(content_type_id, object_id, field_id, user_id, State.objects.filter(pk__in=source_state_pks), include_user=False)

    @staticmethod
    def has_user_any_action(content_type_id, field_id, user_id):
        """
        :param content_type_id:
        :param field_id:
        :param user_id:
        :return: Boolean value indicates whether the user has any role for the content type and field are sent. Any elements existence
          accepted, rejected or pending for the user, means the user in active for the content type and field.
        """
        user = ExternalUser.objects.get(user_id=user_id)
        content_type = ExternalContentType.objects.get(pk=content_type_id)
        field = Field.objects.get(pk=field_id)
        approvements = Approvement.objects.filter(Q(transactioner=user) | Q(meta__permission__in=user.permissions.all())).filter(content_type=content_type, field=field)
        return approvements.count() != 0
