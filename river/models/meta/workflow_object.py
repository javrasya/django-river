from django.db.models.base import ModelBase
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from river.models import Approvement
from river.services.approvement import ApprovementService
from river.services.config import RiverConfig


class WorkflowObjectMetaclass(ModelBase):
    def __new__(cls, name, bases, attrs):
        result = super(WorkflowObjectMetaclass, cls).__new__(cls, name, bases, attrs)

        pre_save.connect(_pre_save, result, False)
        post_save.connect(_post_save, result, False)

        return result


def _pre_save(*args, **kwargs):  # signal, sender, instance):
    """
    Desc: Set initial state of the object.
    :param kwargs:
    :return:
    """
    from river.models.fields.state import StateField
    from river.services.state import StateService

    instance = kwargs['instance']
    model = instance.__class__
    fields = []
    for f in model._meta.fields:
        if isinstance(f, StateField):
            fields.append(f)
    if model.objects.filter(pk=instance.pk).count() == 0:
        for f in fields:
            initial_state = StateService.get_init_state(RiverConfig.CONTENT_TYPE_CLASS.objects.get_for_model(instance), f.name)
            f.set_state(instance, initial_state)


def _post_save(*args, **kwargs):  # signal, sender, instance):
    """
    Desc:  Generate TransitionApprovements according to TransitionApproverDefinition of the content type at the beginning.
    :param kwargs:
    :return:
    """
    from river.models.fields.state import StateField

    instance = kwargs['instance']
    for f in instance._meta.fields:
        if isinstance(f, StateField):
            approvements = Approvement.objects.filter(workflow_object=instance, field=f.name)
            if approvements.count() == 0:
                ApprovementService.init_approvements(instance, f.name)
