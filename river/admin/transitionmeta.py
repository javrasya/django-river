from django.contrib import admin
from django import forms

from river.models import TransitionMeta
from river.models.transitionapprovalmeta import TransitionApprovalMeta


class TransitionMetaForm(forms.ModelForm):
    class Meta:
        model = TransitionMeta
        fields = ('workflow', 'source_state', 'destination_state')


class TransitionMetaAdmin(admin.ModelAdmin):
    form = TransitionMetaForm
    list_display = ('workflow', 'source_state', 'destination_state')


admin.site.register(TransitionMeta, TransitionMetaAdmin)
