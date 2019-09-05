class WorkflowRegistry(object):
    def __init__(self):
        self.workflows = {}
        self.class_index = {}

    def add(self, name, cls):
        self.workflows[id(cls)] = self.workflows.get(id(cls), set())
        self.workflows[id(cls)].add(name)
        self.class_index[id(cls)] = cls


workflow_registry = WorkflowRegistry()
