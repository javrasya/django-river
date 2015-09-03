# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Handler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
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
        migrations.CreateModel(
            name='Proceeding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('object_id', models.PositiveIntegerField(verbose_name='Related Object')),
                ('field', models.CharField(max_length=200, verbose_name='Field')),
                ('transaction_date', models.DateTimeField(null=True, blank=True)),
                ('status', models.IntegerField(default=0, verbose_name='Status', choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Rejected')])),
                ('skip', models.BooleanField(default=False, verbose_name='Skip')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled?')),
                ('content_type', models.ForeignKey(verbose_name='Content Type', to='contenttypes.ContentType')),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='Groups')),
            ],
            options={
                'verbose_name': 'Proceeding',
                'verbose_name_plural': 'Proceedings',
            },
        ),
        migrations.CreateModel(
            name='ProceedingMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('action_text', models.TextField(max_length=200, null=True, verbose_name='Action Text', blank=True)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='Groups')),
                ('permissions', models.ManyToManyField(to='auth.Permission', verbose_name='Permissions')),
            ],
            options={
                'verbose_name': 'Proceeding Meta',
                'verbose_name_plural': 'Proceeding Metas',
            },
        ),
        migrations.CreateModel(
            name='ProceedingTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('process_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('previous_track', mptt.fields.TreeOneToOneField(related_name='next_track', null=True, blank=True, to='river.ProceedingTrack', verbose_name='Previous track')),
                ('proceeding', models.ForeignKey(related_name='tracks', verbose_name='Proceeding', to='river.Proceeding')),
            ],
            options={
                'verbose_name': 'Proceeding Track',
                'verbose_name_plural': 'Proceeding Tracks',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('label', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200, null=True, verbose_name='Description', blank=True)),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
            },
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('field', models.CharField(max_length=200, verbose_name='Field')),
                ('direction', models.SmallIntegerField(default=1, verbose_name='Transition Direction')),
                ('content_type', models.ForeignKey(verbose_name='Content Type', to='contenttypes.ContentType')),
                ('destination_state', models.ForeignKey(related_name='transitions_as_destination', verbose_name='Next State', to='river.State')),
                ('source_state', models.ForeignKey(related_name='transitions_as_source', verbose_name='Source State', to='river.State')),
            ],
            options={
                'verbose_name': 'Transition',
                'verbose_name_plural': 'Transitions',
            },
        ),
        migrations.AddField(
            model_name='proceedingmeta',
            name='transition',
            field=models.ForeignKey(verbose_name='Transition', to='river.Transition'),
        ),
        migrations.AddField(
            model_name='proceeding',
            name='meta',
            field=models.ForeignKey(related_name='proceedings', verbose_name='Meta', to='river.ProceedingMeta'),
        ),
        migrations.AddField(
            model_name='proceeding',
            name='permissions',
            field=models.ManyToManyField(to='auth.Permission', verbose_name='Permissions'),
        ),
        migrations.AddField(
            model_name='proceeding',
            name='transactioner',
            field=models.ForeignKey(verbose_name='Transactioner', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='proceedingmeta',
            unique_together=set([('transition', 'order')]),
        ),
    ]
