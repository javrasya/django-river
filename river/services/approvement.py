from datetime import datetime
from django.db.models import Min, Q

from river.models import FORWARD
from river.models.approvement import Approvement, PENDING, APPROVED
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
                workflow_object=workflow_object,
                field=field,
                defaults={
                    'order': approvement_meta.order,
                    'status': PENDING,
                }
            )
            approvement.permissions.add(*approvement_meta.permissions.all())
            approvement.groups.add(*approvement_meta.groups.all())

        init_state = StateService.get_initial_state(content_type, field)
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
    def get_approvements_object_waiting_for_approval(workflow_object, field, source_states, user=None, destination_state=None, god_mod=False):

        def get_approvement(approvements):
            min_order = approvements.aggregate(Min('order'))['order__min']
            approvements = approvements.filter(order=min_order)

            if destination_state:
                approvements = approvements.filter(meta__transition__destination_state=destination_state)

            return approvements

        def authorize_approvements(approvements):
            return approvements.filter(
                (
                    (Q(transactioner__isnull=True) | Q(transactioner=user)) &
                    (Q(permissions__isnull=True) | Q(permissions__in=user.user_permissions.all())) &
                    (Q(groups__isnull=True) | Q(groups__in=user.groups.all()))
                )
            )

        approvements = Approvement.objects.filter(
            workflow_object=workflow_object,
            field=field,
            meta__transition__source_state__in=source_states,
            status=PENDING,
            enabled=True
        )

        suitable_approvements = get_approvement(approvements.filter(skip=False))

        if user and not god_mod:
            suitable_approvements = authorize_approvements(suitable_approvements)

        skipped_approvements = get_approvement(approvements.filter(skip=True))
        if skipped_approvements:
            source_state_pks = list(skipped_approvements.values_list('meta__transition__destination_state', flat=True))
            suitable_approvements = suitable_approvements | ApprovementService.get_approvements_object_waiting_for_approval(workflow_object, field, State.objects.filter(pk__in=source_state_pks),
                                                                                                                            user=user, destination_state=destination_state, god_mod=god_mod)
        return suitable_approvements

    @staticmethod
    def get_next_approvements(workflow_object, field, approvements=Approvement.objects.none(), current_states=None, index=0, limit=None):
        index += 1
        current_states = current_states or [getattr(workflow_object, field)]
        next_approvements = Approvement.objects.filter(workflow_object=workflow_object, field=field, meta__transition__source_state__in=current_states)
        if next_approvements and not next_approvements.filter(pk__in=approvements.values_list('pk')) and (not limit or index < limit):
            approvements = ApprovementService.get_next_approvements(workflow_object, field, approvements=approvements | next_approvements, current_states=State.objects.filter(
                pk__in=next_approvements.values_list('meta__transition__destination_state', flat=True)), index=index, limit=limit)

        return approvements

    @staticmethod
    def has_user_any_action(content_type, field, user):
        """
        :param content_type_id:
        :param field_id:
        :param user_id:
        :return: Boolean value indicates whether the user has any role for the content type and field are sent. Any elements existence
          accepted, rejected or pending for the user, means the user in active for the content type and field.
        """
        approvements = Approvement.objects.filter(Q(transactioner=user) | Q(permissions__in=user.user_permissions.all()) | Q(groups__in=user.groups.all())).filter(content_type=content_type,
                                                                                                                                                                   field=field)
        return approvements.count() != 0

    @staticmethod
    def override_permissions(approvement, permissions):
        approvement.permissions.clear()
        approvement.permissions.add(*permissions)

    @staticmethod
    def override_groups(approvement, groups):
        approvement.groups.clear()
        approvement.groups.add(*groups)

    @staticmethod
    def get_initial_approvements(content_type, field):
        initial_state = StateService.get_initial_state(content_type, field)
        return Approvement.objects.filter(meta__transition__source_state=initial_state, meta__transition__direction=FORWARD)

    @staticmethod
    def get_final_approvements(content_type, field):
        final_states = StateService.get_final_states(content_type, field)
        return Approvement.objects.filter(meta__transition__destination_state__in=final_states, meta__transition__direction=FORWARD)
