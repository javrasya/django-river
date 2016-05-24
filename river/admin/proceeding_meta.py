from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from river.models import ProceedingMeta
from river.models.fields.state import StateField


def get_field_choices():
    choices = ((None, "-------------"),)
    for ct in ContentType.objects.all():
        model = ct.model_class()
        choices += tuple(
            ("%s__%s" % (f.name, ct.pk), "%s - %s" % (f.name, ct)) for f in model._meta.fields if type(f) is StateField)
    return choices


class ProceedingMetaForm(forms.ModelForm):
    content_type = forms.HiddenInput()
    field = forms.HiddenInput()
    field_ct = forms.ChoiceField(label=_('Field'), choices=get_field_choices())

    class Meta:
        model = ProceedingMeta
        fields = ('field_ct', 'transition', 'permissions', 'groups', 'order', 'action_text', 'parents')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance and instance.pk:
            self.declared_fields['field_ct'].initial = "%s__%s" % (instance.field, instance.content_type.pk)

        super(ProceedingMetaForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        field, content_type_id = self.cleaned_data['field_ct'].split('__')
        ct = ContentType.objects.get(pk=content_type_id)
        instance = super(ProceedingMetaForm, self).save(commit=False)
        instance.field = field
        instance.content_type = ct
        return super(ProceedingMetaForm, self).save(*args, **kwargs)


class ProceedingMetaAdmin(admin.ModelAdmin):
    form = ProceedingMetaForm


admin.site.register(ProceedingMeta, ProceedingMetaAdmin)
