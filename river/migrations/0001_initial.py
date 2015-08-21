# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name', blank=True)),
                ('description', models.CharField(max_length=200, null=True, verbose_name='Description', blank=True)),
                ('owner', models.ForeignKey(related_name='applications', verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
            },
        ),
        migrations.CreateModel(
            name='Approvement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                'verbose_name': 'Approvement',
                'verbose_name_plural': 'Approvements',
            },
        ),
        migrations.CreateModel(
            name='ApprovementMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('action_text', models.TextField(max_length=200, null=True, verbose_name='Approve Text', blank=True)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='Groups')),
                ('permissions', models.ManyToManyField(to='auth.Permission', verbose_name='Permissions')),
            ],
            options={
                'verbose_name': 'Approvement Meta',
                'verbose_name_plural': 'Approvement Metas',
            },
        ),
        migrations.CreateModel(
            name='ApprovementTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('process_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('approvement', models.ForeignKey(related_name='tracks', verbose_name='Approvement', to='river.Approvement')),
                ('previous_track', mptt.fields.TreeOneToOneField(related_name='next_track', null=True, blank=True, to='river.ApprovementTrack', verbose_name='Previous track')),
            ],
            options={
                'verbose_name': 'Approvement Track',
                'verbose_name_plural': 'Approvement Tracks',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            model_name='approvementmeta',
            name='transition',
            field=models.ForeignKey(verbose_name='Transition', to='river.Transition'),
        ),
        migrations.AddField(
            model_name='approvement',
            name='meta',
            field=models.ForeignKey(related_name='approvements', verbose_name='Approve Definition', to='river.ApprovementMeta'),
        ),
        migrations.AddField(
            model_name='approvement',
            name='permissions',
            field=models.ManyToManyField(to='auth.Permission', verbose_name='Permissions'),
        ),
        migrations.AddField(
            model_name='approvement',
            name='transactioner',
            field=models.ForeignKey(verbose_name='Approver', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='approvementmeta',
            unique_together=set([('transition', 'order')]),
        ),
    ]
