import logging

from django.contrib import auth
from django.db.models import Min, Q
from django.db.transaction import atomic

from river.config import app_config
from river.models.proceeding import Proceeding, PENDING
from river.models.proceeding_meta import ProceedingMeta
from river.models.state import State

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class ProceedingService(object):
    @staticmethod
    def init_proceedings(workflow_object, field):

        content_type = app_config.CONTENT_TYPE_CLASS.objects.get_for_model(workflow_object)
        for proceeding_meta in ProceedingMeta.objects.filter(content_type=content_type, field=field):
            proceeding, created = Proceeding.objects.update_or_create(
                meta=proceeding_meta,
                field=proceeding_meta.field,
                workflow_object=workflow_object,
                defaults={
                    'order': proceeding_meta.order,
                    'status': PENDING,
                }
            )
            proceeding.permissions.add(*proceeding_meta.permissions.all())
            proceeding.groups.add(*proceeding_meta.groups.all())

        workflow_object.save()
        LOGGER.debug("Proceedings are initialized for workflow object %s and field %s" % (workflow_object, field))

    @staticmethod
    def get_available_proceedings(workflow_object, field, source_states, user=None, destination_state=None,
                                  god_mod=False):

        def get_proceeding(proceedings):
            min_order = proceedings.aggregate(Min('order'))['order__min']
            proceedings = proceedings.filter(order=min_order)

            if destination_state:
                proceedings = proceedings.filter(meta__transition__destination_state=destination_state)

            return proceedings

        def authorize_proceedings(proceedings):
            group_q = Q()
            for g in user.groups.all():
                group_q = group_q | Q(groups__in=[g])

            permissions = []
            for backend in auth.get_backends():
                permissions.extend(backend.get_all_permissions(user))

            permission_q = Q()
            for p in permissions:
                label, codename = p.split('.')
                permission_q = permission_q | Q(permissions__content_type__app_label=label,
                                                permissions__codename=codename)

            return proceedings.filter(
                (
                    (Q(transactioner__isnull=True) | Q(transactioner=user)) &
                    (Q(permissions__isnull=True) | permission_q) &
                    (Q(groups__isnull=True) | group_q)
                )
            )

        proceedings = Proceeding.objects.filter(
            workflow_object=workflow_object,
            field=field,
            meta__transition__source_state__in=source_states,
            status=PENDING,
            enabled=True
        )

        suitable_proceedings = get_proceeding(proceedings.filter(skip=False))

        if user and not god_mod:
            suitable_proceedings = authorize_proceedings(suitable_proceedings)

        skipped_proceedings = get_proceeding(proceedings.filter(skip=True))
        if skipped_proceedings:
            source_state_pks = list(skipped_proceedings.values_list('meta__transition__destination_state', flat=True))
            suitable_proceedings = suitable_proceedings | ProceedingService.get_available_proceedings(workflow_object,
                                                                                                      field,
                                                                                                      State.objects.filter(
                                                                                                          pk__in=source_state_pks),
                                                                                                      user=user,
                                                                                                      destination_state=destination_state,
                                                                                                      god_mod=god_mod)
        return suitable_proceedings

    @staticmethod
    def get_next_proceedings(workflow_object, field, proceeding_pks=None, current_states=None, index=0, limit=None):
        if not proceeding_pks:
            proceeding_pks = []
        index += 1
        current_states = list(current_states.values_list('pk', flat=True)) if current_states else [
            getattr(workflow_object, field)]
        next_proceedings = Proceeding.objects.filter(workflow_object=workflow_object, field=field,
                                                     meta__transition__source_state__in=current_states)
        if workflow_object.proceeding:
            next_proceedings = next_proceedings.exclude(pk=workflow_object.proceeding.pk)
        if next_proceedings.exists() and not next_proceedings.filter(pk__in=proceeding_pks).exists() and (
                    not limit or index < limit):
            proceedings = ProceedingService.get_next_proceedings(
                workflow_object,
                field,
                proceeding_pks=proceeding_pks + list(next_proceedings.values_list('pk', flat=True)),
                current_states=State.objects.filter(
                    pk__in=next_proceedings.values_list('meta__transition__destination_state', flat=True)),
                index=index,
                limit=limit
            )
        else:
            proceedings = Proceeding.objects.filter(pk__in=proceeding_pks)

        return proceedings

    @staticmethod
    @atomic
    def cycle_proceedings(workflow_object, field):
        """
         Finds next proceedings and clone them for cycling if it exists.
        """
        proceeded_next_proceedings = ProceedingService.get_next_proceedings(workflow_object, field).exclude(
            status=PENDING).exclude(cloned=True)
        for p in proceeded_next_proceedings:
            clone_p, c = Proceeding.objects.get_or_create(
                meta=p.meta,
                content_type=p.content_type,
                object_id=p.object_id,
                field=p.field,
                skip=p.skip,
                order=p.order,
                enabled=p.enabled,
                status=PENDING)

            if c:
                clone_p.permissions.add(*p.permissions.all())
                clone_p.groups.add(*p.groups.all())
        proceeded_next_proceedings.update(cloned=True)

        return True if proceeded_next_proceedings.count() else False

    @staticmethod
    def has_user_any_action(content_type, field, user):
        """
        :param content_type_id:
        :param field_id:
        :param user_id:
        :return: Boolean value indicates whether the user has any role for the content type and field are sent. Any elements existence
          accepted, rejected or pending for the user, means the user in active for the content type and field.
        """
        proceedings = Proceeding.objects.filter(
            Q(transactioner=user) | Q(permissions__in=user.user_permissions.all()) | Q(
                groups__in=user.groups.all())).filter(content_type=content_type,
                                                      field=field)
        return proceedings.count() != 0

    @staticmethod
    def override_permissions(proceeding, permissions):
        proceeding.permissions.clear()
        proceeding.permissions.add(*permissions)

    @staticmethod
    def override_groups(proceeding, groups):
        proceeding.groups.clear()
        proceeding.groups.add(*groups)

    @staticmethod
    def get_initial_proceedings(content_type, field):
        return Proceeding.objects.filter(meta__parents__isnull=True)

    @staticmethod
    def get_final_proceedings(content_type, field):
        return Proceeding.objects.filter(meta__children__isnull=True)
