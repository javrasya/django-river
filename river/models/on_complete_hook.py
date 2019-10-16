from river.models.hook import Hook


class OnCompleteHook(Hook):
    class Meta:
        unique_together = [('callback_function', 'workflow', 'content_type', 'object_id')]
