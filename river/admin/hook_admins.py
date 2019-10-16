from django.contrib import admin

from river.models import OnApprovedHook, OnTransitHook, OnCompleteHook


class OnApprovedHookAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'callback_function', 'transition_approval_meta')


class OnTransitHookAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'callback_function', 'source_state', 'destination_state')


class OnCompleteHookAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'callback_function')


admin.site.register(OnApprovedHook, OnApprovedHookAdmin)
admin.site.register(OnTransitHook, OnTransitHookAdmin)
admin.site.register(OnCompleteHook, OnCompleteHookAdmin)
