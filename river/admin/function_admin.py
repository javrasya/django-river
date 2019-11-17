from codemirror2.widgets import CodeMirrorEditor
from django import forms
from django.contrib import admin

from river.models import Function


class FunctionForm(forms.ModelForm):
    body = forms.CharField(widget=CodeMirrorEditor(options={'mode': 'python'}))

    class Meta:
        model = Function
        fields = ('name', 'body',)


class FunctionAdmin(admin.ModelAdmin):
    form = FunctionForm
    list_display = ('name', 'function_version', 'date_created', 'date_updated')
    readonly_fields = ('version', 'date_created', 'date_updated')

    def function_version(self, obj):  # pylint: disable=no-self-use
        return "v%s" % obj.version


admin.site.register(Function, FunctionAdmin)
