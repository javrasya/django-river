# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.template.defaultfilters import slugify
from river.models.factories import ProceedingMetaObjectFactory
from river.services.proceeding_meta import ProceedingMetaService


def move_from_transition_to_meta(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    ProceedingMeta = apps.get_model("river", "ProceedingMeta")
    for pm in ProceedingMeta.objects.all():
        pm.content_type = pm.transition.content_type
        pm.field = pm.transition.field
        pm.save()


class Migration(migrations.Migration):
    dependencies = [
        ('river', '0002_auto_20150916_0144'),
    ]

    operations = [
        migrations.RunPython(move_from_transition_to_meta),
    ]
