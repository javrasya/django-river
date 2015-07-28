__author__ = 'ahmetdal'


class Handler(object):
    @classmethod
    def register(cls, handler, workflow_object=None, field=None):
        d = {'handler': handler}
        if workflow_object and field:
            d['workflow_object_pk'] = workflow_object.pk
            d['field'] = field
        return d
