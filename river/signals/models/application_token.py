import binascii
import os

from django.db.models.signals import pre_save

from apps.riverio.models.application_token import ApplicationToken


__author__ = 'ahmetdal'


def on_pre_save(sender, instance, *args, **kwargs):
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    if not instance.key:
        instance.key = generate_key()


pre_save.connect(on_pre_save, ApplicationToken)

