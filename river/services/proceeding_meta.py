from river.models.proceeding_meta import ProceedingMeta
from river.models.proceeding import Proceeding

__author__ = 'ahmetdal'


class ProceedingMetaService(object):
    @staticmethod
    def apply_new_proceeding_meta(new_proceeding_meta):
        if new_proceeding_meta.proceedings.count() == 0:
            content_type = new_proceeding_meta.content_type
            WorkflowObjectClass = content_type.model_class()
            field = new_proceeding_meta.field
            Proceeding.objects.bulk_create(
                list(
                    Proceeding(
                        workflow_object=workflow_object,
                        meta=new_proceeding_meta,
                        field=field,
                        content_type=content_type
                    )
                    for workflow_object in WorkflowObjectClass.objects.all()
                )
            )

    @staticmethod
    def build_tree(instance):
        parents = ProceedingMeta.objects.filter(transition__destination_state__pk=instance.transition.source_state.pk).exclude(pk__in=instance.parents.values_list('pk', flat=True))
        children = ProceedingMeta.objects.filter(transition__source_state__pk=instance.transition.destination_state.pk).exclude(parents__in=[instance.pk])
        instance = ProceedingMeta.objects.get(pk=instance.pk)
        if parents:
            instance.parents.add(*parents)

        for child in children:
            child.parents.add(instance)
