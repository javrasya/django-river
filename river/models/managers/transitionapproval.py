from django_cte import CTEManager

from river.config import app_config

__author__ = 'ahmetdal'


class TransitionApprovalManager(CTEManager):
    def __init__(self, *args, **kwargs):
        super(TransitionApprovalManager, self).__init__(*args, **kwargs)

    def filter(self, *args, **kwarg):
        workflow_object = kwarg.pop('workflow_object', None)
        if workflow_object:
            kwarg['content_type'] = app_config.CONTENT_TYPE_CLASS.objects.get_for_model(workflow_object)
            kwarg['object_id'] = workflow_object.pk

        return super(TransitionApprovalManager, self).filter(*args, **kwarg)

    def update_or_create(self, *args, **kwarg):
        workflow_object = kwarg.pop('workflow_object', None)
        if workflow_object:
            kwarg['content_type'] = app_config.CONTENT_TYPE_CLASS.objects.get_for_model(workflow_object)
            kwarg['object_id'] = workflow_object.pk

        return super(TransitionApprovalManager, self).update_or_create(*args, **kwarg)
