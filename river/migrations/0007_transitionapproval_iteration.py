# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-10-25 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('river', '0006_auto_20191020_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='transitionapproval',
            name='iteration',
            field=models.IntegerField(default=0, verbose_name='Priority'),
        ),
    ]
