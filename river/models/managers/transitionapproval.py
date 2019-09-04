from django_cte import CTEManager

from river.config import app_config

__author__ = 'ahmetdal'


class TransitionApprovalManager(CTEManager):
    def __init__(self, *args, **kwargs):
        super(TransitionApprovalManager, self).__init__(*args, **kwargs)

    def filter(self, *args, **kwarg):
        object = kwarg.pop('workflow_object', None)
        if object:
            kwarg['content_type'] = app_config.CONTENT_TYPE_CLASS.objects.get_for_model(object)
            kwarg['object_id'] = object.pk

        return super(TransitionApprovalManager, self).filter(*args, **kwarg)

    def update_or_create(self, *args, **kwarg):
        object = kwarg.pop('workflow_object', None)
        if object:
            kwarg['content_type'] = app_config.CONTENT_TYPE_CLASS.objects.get_for_model(object)
            kwarg['object_id'] = object.pk

        return super(TransitionApprovalManager, self).update_or_create(*args, **kwarg)

    def skip(self, *args, **kwargs):
        for approval in self.filter(*args, **kwargs):
            approval.skip()
