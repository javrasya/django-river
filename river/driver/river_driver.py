from abc import abstractmethod


class RiverDriver(object):

    def __init__(self, workflow, wokflow_object_class, field_name):
        self.workflow = workflow
        self.wokflow_object_class = wokflow_object_class
        self.field_name = field_name
        self._cached_workflow = None

    @abstractmethod
    def get_available_approvals(self, as_user):
        raise NotImplementedError()
