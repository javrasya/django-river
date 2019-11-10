from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from river.core.workflowregistry import workflow_registry
from river.models import OnApprovedHook, OnTransitHook, OnCompleteHook


class BaseHookInline(GenericTabularInline):
    fields = ("callback_function", "hook_type")


class OnApprovedHookInline(BaseHookInline):
    model = OnApprovedHook

    def __init__(self, *args, **kwargs):
        super(OnApprovedHookInline, self).__init__(*args, **kwargs)
        self.fields += ("transition_approval_meta",)


class OnTransitHookInline(BaseHookInline):
    model = OnTransitHook

    def __init__(self, *args, **kwargs):
        super(OnTransitHookInline, self).__init__(*args, **kwargs)
        self.fields += ("transition_meta",)


class OnCompleteHookInline(BaseHookInline):
    model = OnCompleteHook


class DefaultWorkflowModelAdmin(admin.ModelAdmin):
    inlines = [
        OnApprovedHookInline,
        OnTransitHookInline,
        OnCompleteHookInline
    ]

    def __init__(self, *args, **kwargs):
        super(DefaultWorkflowModelAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields += tuple(workflow_registry.get_class_fields(self.model))


class OnApprovedHookAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'callback_function', 'transition_approval_meta')


class OnTransitHookAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'callback_function', 'transition_meta')


class OnCompleteHookAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'callback_function')


admin.site.register(OnApprovedHook, OnApprovedHookAdmin)
admin.site.register(OnTransitHook, OnTransitHookAdmin)
admin.site.register(OnCompleteHook, OnCompleteHookAdmin)
