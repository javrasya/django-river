from river.handlers.handler import Handler
from river.signals import workflow_is_completed

__author__ = 'ahmetdal'


class CompletedHandler(Handler):
    handlers = {}


workflow_is_completed.connect(CompletedHandler.dispatch)
