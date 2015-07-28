# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('river', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvement',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order'),
        ),
    ]
