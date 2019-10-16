import inspect
import re

from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _

from river.models import BaseModel

loaded_functions = {}


class Function(BaseModel):
    name = models.CharField(verbose_name=_("Function Name"), max_length=200, unique=True, null=False, blank=False)
    body = models.TextField(verbose_name=_("Function Body"), max_length=100000, null=False, blank=False)
    version = models.IntegerField(verbose_name=_("Function Version"), default=0)

    def __str__(self):
        return "%s - %s" % (self.name, "v%s" % self.version)

    def get(self):
        func = loaded_functions.get(self.name, None)
        if not func or func["version"] != self.version:
            func = {"function": self._load(), "version": self.version}
            loaded_functions[self.pk] = func
        return func["function"]

    def _load(self):
        func_body = "def _wrapper(context):\n"
        for line in self.body.split("\n"):
            func_body += "\t" + line + "\n"
        func_body += "\thandle(context)\n"
        exec(func_body)
        return eval("_wrapper")


def on_pre_save(sender, instance, *args, **kwargs):
    instance.version += 1


pre_save.connect(on_pre_save, Function)


def _normalize_callback(callback):
    callback_str = inspect.getsource(callback).replace("def %s(" % callback.__name__, "def handle(")
    space_size = callback_str.index('def handle(')
    return re.sub(r'^\s{%s}' % space_size, '', inspect.getsource(callback).replace("def %s(" % callback.__name__, "def handle("))


def create_function(callback):
    return Function.objects.get_or_create(
        name=callback.__module__ + "." + callback.__name__,
        body=_normalize_callback(callback)
    )[0]
