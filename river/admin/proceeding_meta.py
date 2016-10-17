from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from river.models import ProceedingMeta
from river.models.fields.state import StateField
from river.services.object import ObjectService


def get_content_types():
    content_type_pks = []
    for ct in ContentType.objects.all():
        model = ct.model_class()
        for f in model._meta.fields:
            if type(f) is StateField:
                content_type_pks.append(ct.pk)
    return content_type_pks


class ProceedingMetaForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(queryset=ContentType.objects.none())

    class Meta:
        model = ProceedingMeta
        fields = ('content_type', 'transition', 'permissions', 'groups', 'order', 'action_text')

    def __init__(self, *args, **kwargs):
        self.declared_fields['content_type'].queryset = ContentType.objects.filter(pk__in=get_content_types())

        super(ProceedingMetaForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        content_type = self.cleaned_data['content_type']
        field = ObjectService.get_field(content_type.model_class())
        instance = super(ProceedingMetaForm, self).save(commit=False)
        instance.field = field.name
        return super(ProceedingMetaForm, self).save(*args, **kwargs)


class ProceedingMetaAdmin(admin.ModelAdmin):
    form = ProceedingMetaForm


admin.site.register(ProceedingMeta, ProceedingMetaAdmin)
