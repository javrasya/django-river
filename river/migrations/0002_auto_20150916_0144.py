# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import models, migrations
from django.utils.text import slugify


class Migration(migrations.Migration):
    dependencies = [
        ('river', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proceedingmeta',
            name='content_type',
            field=models.ForeignKey(default=1, verbose_name='Content Type', to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proceedingmeta',
            name='field',
            field=models.CharField(default='state', max_length=200, verbose_name='Field'),
            preserve_default=False,
        ),
    ]
