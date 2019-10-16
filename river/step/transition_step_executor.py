from abc import abstractmethod
from datetime import datetime

from river.models.fields.state import classproperty
from river.models2.transition_step_execution import TransitionStepExecution


class TransitionStepExecutor(object):

    def __init__(self, transition, workflow_object, step):
        self.transition = transition
        self.workflow_object = workflow_object
        assert isinstance(step.step_object, self.expected_step_type)
        self.step = step

    @classproperty
    @abstractmethod
    def expected_step_type(self):
        raise NotImplementedError()

    @abstractmethod
    def _execute(self, transition_step_execution):
        raise NotImplementedError()

    def execute(self):
        transition_step_execution = TransitionStepExecution.objects.create(
            transition_step=self.step,
            workflow_object=self.workflow_object,
            started_at=datetime.now()
        )
        if self._execute(transition_step_execution):
            transition_step_execution.is_done = True
            transition_step_execution.save()
