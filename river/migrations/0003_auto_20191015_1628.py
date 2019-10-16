# Generated by Django 2.1.4 on 2019-10-15 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('river', '0002_auto_20190920_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Updated')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Function Name')),
                ('body', models.TextField(max_length=100000, verbose_name='Function Body')),
                ('version', models.IntegerField(default=0, verbose_name='Function Version')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OnApprovedHook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Updated')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('hook_type', models.CharField(choices=[('BEFORE', 'Before'), ('AFTER', 'After')], max_length=50, verbose_name='Status')),
                ('callback_function', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='river_onapprovedhook_hooks', to='river.Function', verbose_name='Function')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
                ('transition_approval_meta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='on_approved_hooks', to='river.TransitionApprovalMeta', verbose_name='Transition Approval')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='river_onapprovedhook_hooks', to='river.Workflow', verbose_name='Workflow')),
            ],
        ),
        migrations.CreateModel(
            name='OnCompleteHook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Updated')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('hook_type', models.CharField(choices=[('BEFORE', 'Before'), ('AFTER', 'After')], max_length=50, verbose_name='Status')),
                ('callback_function', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='river_oncompletehook_hooks', to='river.Function', verbose_name='Function')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='river_oncompletehook_hooks', to='river.Workflow', verbose_name='Workflow')),
            ],
        ),
        migrations.CreateModel(
            name='OnTransitHook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Updated')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('hook_type', models.CharField(choices=[('BEFORE', 'Before'), ('AFTER', 'After')], max_length=50, verbose_name='Status')),
                ('callback_function', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='river_ontransithook_hooks', to='river.Function', verbose_name='Function')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
                ('destination_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='on_transition_hook_as_destination', to='river.State', verbose_name='Next State')),
                ('source_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='on_transition_hook_as_source', to='river.State', verbose_name='Source State')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='river_ontransithook_hooks', to='river.Workflow', verbose_name='Workflow')),
            ],
        ),
        migrations.DeleteModel(
            name='Callback',
        ),
        migrations.AlterUniqueTogether(
            name='ontransithook',
            unique_together={('callback_function', 'workflow', 'source_state', 'destination_state', 'content_type', 'object_id')},
        ),
        migrations.AlterUniqueTogether(
            name='oncompletehook',
            unique_together={('callback_function', 'workflow', 'content_type', 'object_id')},
        ),
        migrations.AlterUniqueTogether(
            name='onapprovedhook',
            unique_together={('callback_function', 'workflow', 'transition_approval_meta', 'content_type', 'object_id')},
        ),
    ]
