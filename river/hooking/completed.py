from river.hooking.hooking import Hooking
from river.signals import pre_final, post_final

__author__ = 'ahmetdal'


class PreCompletedHooking(Hooking):
    pass


class PostCompletedHooking(Hooking):
    pass


pre_final.connect(PreCompletedHooking.dispatch)
post_final.connect(PostCompletedHooking.dispatch)
