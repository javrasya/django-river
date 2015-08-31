# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('river', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Handler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash', models.CharField(unique=True, max_length=200, verbose_name='Hash')),
                ('method', models.CharField(max_length=200, verbose_name='Callback Method')),
                ('handler_cls', models.CharField(max_length=200, verbose_name='HandlerClass')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
            ],
            options={
                'verbose_name': 'Handler',
                'verbose_name_plural': 'Handlers',
            },
        ),
    ]
