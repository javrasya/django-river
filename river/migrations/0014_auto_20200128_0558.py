from django.db import migrations, models
from django.db.models import F, PositiveIntegerField
from django.db.models.functions import Cast


def backup_values(apps, schema_editor):
    def backup_hook(hook_cls):
        hook_cls.objects.update(object_id2=F("object_id"))
        hook_cls.objects.update(object_id=None)

    backup_hook(apps.get_model("river", "OnApprovedHook"))
    backup_hook(apps.get_model("river", "OnCompleteHook"))
    backup_hook(apps.get_model("river", "OnTransitHook"))


def revert_backup_values(apps, schema_editor):
    def revert_backup_hook(hook_cls):
        hook_cls.objects.update(object_id=Cast(F("object_id2"), output_field=PositiveIntegerField()))
        hook_cls.objects.update(object_id2=None)

    revert_backup_hook(apps.get_model("river", "OnApprovedHook"))
    revert_backup_hook(apps.get_model("river", "OnCompleteHook"))
    revert_backup_hook(apps.get_model("river", "OnTransitHook"))


def restore_values(apps, schema_editor):
    def restore_hook(hook_cls):
        hook_cls.objects.update(object_id=F("object_id2"))

    restore_hook(apps.get_model("river", "OnApprovedHook"))
    restore_hook(apps.get_model("river", "OnCompleteHook"))
    restore_hook(apps.get_model("river", "OnTransitHook"))


def revert_restore_values(apps, schema_editor):
    def revert_restore_hook(hook_cls):
        hook_cls.objects.update(object_id2=F("object_id"))

    revert_restore_hook(apps.get_model("river", "OnApprovedHook"))
    revert_restore_hook(apps.get_model("river", "OnCompleteHook"))
    revert_restore_hook(apps.get_model("river", "OnTransitHook"))


class Migration(migrations.Migration):
    dependencies = [
        ('river', '0013_auto_20191214_0742'),
    ]

    operations = [
        migrations.AddField(
            model_name='onapprovedhook',
            name='object_id2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='oncompletehook',
            name='object_id2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='ontransithook',
            name='object_id2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),

        migrations.RunPython(backup_values, reverse_code=revert_backup_values),
        migrations.AlterField(
            model_name='onapprovedhook',
            name='object_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='oncompletehook',
            name='object_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ontransithook',
            name='object_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.RunPython(restore_values, reverse_code=revert_restore_values),

        migrations.RemoveField(
            model_name='onapprovedhook',
            name='object_id2',
        ),
        migrations.RemoveField(
            model_name='oncompletehook',
            name='object_id2',
        ),
        migrations.RemoveField(
            model_name='ontransithook',
            name='object_id2',
        ),
    ]
