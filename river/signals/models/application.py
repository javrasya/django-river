from django.db.models.signals import post_save
from esefpy.common.django.middlewares.tls import get_user

from apps.riverio.models.application import Application
from apps.riverio.models.application_token import ApplicationToken


__author__ = 'ahmetdal'


def on_post_save(sender, instance, created=False, *args, **kwargs):
    if created:
        ApplicationToken.objects.create(user=instance.owner, application=instance)

    if not instance.owner:
        user = get_user()
        instance.owner = user


post_save.connect(on_post_save, Application)

