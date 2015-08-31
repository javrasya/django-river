from river.handlers.handler import Handler
from river.signals import pre_final, post_final

__author__ = 'ahmetdal'


class PreCompletedHandler(Handler):
    pass


class PostCompletedHandler(Handler):
    pass


pre_final.connect(PreCompletedHandler.dispatch)
post_final.connect(PostCompletedHandler.dispatch)
