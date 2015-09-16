# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import models, migrations
from django.utils.text import slugify


def move_from_transition_to_meta(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    ProceedingMeta = apps.get_model("river", "ProceedingMeta")
    for pm in ProceedingMeta.objects.all():
        pm.content_type = pm.transition.content_type
        pm.field = pm.transition.field
        pm.save()


def set_slug(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    State = apps.get_model("river", "State")

    for s in State.objects.all():
        s.slug = slugify(s.label)
        s.save()


class Migration(migrations.Migration):
    dependencies = [
        ('river', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proceedingmeta',
            name='content_type',
            field=models.ForeignKey(default=-1, verbose_name='Content Type', to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proceedingmeta',
            name='field',
            field=models.CharField(default='state', max_length=200, verbose_name='Field'),
            preserve_default=False,
        ),
        migrations.RunPython(move_from_transition_to_meta),

        migrations.RemoveField(
            model_name='transition',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='transition',
            name='field',
        ),
        migrations.AlterUniqueTogether(
            name='proceedingmeta',
            unique_together=set([('content_type', 'field', 'transition', 'order')]),
        ),
        migrations.AlterUniqueTogether(
            name='transition',
            unique_together=set([('source_state', 'destination_state')]),
        ),
        migrations.AddField(
            model_name='state',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, unique=True),
        ),
        migrations.RunPython(set_slug),
        migrations.AlterField(
            model_name='handler',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Created', null=True),
        ),
        migrations.AlterField(
            model_name='handler',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Updated', null=True),
        ),
        migrations.AlterField(
            model_name='proceeding',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Created', null=True),
        ),
        migrations.AlterField(
            model_name='proceeding',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Updated', null=True),
        ),
        migrations.AlterField(
            model_name='proceedingmeta',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Created', null=True),
        ),
        migrations.AlterField(
            model_name='proceedingmeta',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Updated', null=True),
        ),
        migrations.AlterField(
            model_name='proceedingtrack',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Created', null=True),
        ),
        migrations.AlterField(
            model_name='proceedingtrack',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Updated', null=True),
        ),
        migrations.AlterField(
            model_name='state',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Created', null=True),
        ),
        migrations.AlterField(
            model_name='state',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Updated', null=True),
        ),
        migrations.AlterField(
            model_name='transition',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Created', null=True),
        ),
        migrations.AlterField(
            model_name='transition',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Updated', null=True),
        ),
    ]
