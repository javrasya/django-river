from django.contrib import admin
from django import forms

from river.models.transitionapprovalmeta import TransitionApprovalMeta


class TransitionApprovalMetaForm(forms.ModelForm):
    class Meta:
        model = TransitionApprovalMeta
        fields = ('workflow', 'source_state', 'destination_state', 'permissions', 'groups', 'priority')


class TransitionApprovalMetaAdmin(admin.ModelAdmin):
    form = TransitionApprovalMetaForm
    list_display = ('workflow', 'source_state', 'destination_state', 'priority')


admin.site.register(TransitionApprovalMeta, TransitionApprovalMetaAdmin)
