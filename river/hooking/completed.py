from river.hooking.hooking import Hooking
from river.signals import pre_on_complete, post_on_complete

__author__ = 'ahmetdal'


class PreCompletedHooking(Hooking):
    pass


class PostCompletedHooking(Hooking):
    pass


pre_on_complete.connect(PreCompletedHooking.dispatch)
post_on_complete.connect(PostCompletedHooking.dispatch)
