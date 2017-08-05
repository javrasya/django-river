# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 00:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('river', '0009_auto_20170124_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handler',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='handler',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Updated'),
        ),
        migrations.AlterField(
            model_name='proceeding',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='proceeding',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Updated'),
        ),
        migrations.AlterField(
            model_name='proceeding',
            name='transaction_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='proceedingmeta',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='proceedingmeta',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Updated'),
        ),
        migrations.AlterField(
            model_name='state',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='state',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Updated'),
        ),
        migrations.AlterField(
            model_name='transition',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='transition',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Updated'),
        ),
    ]
