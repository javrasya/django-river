from itertools import combinations, chain

__author__ = 'ahmetdal'


def powerset(iterable):
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs, n) for n in range(len(xs) + 1))


class BaseHookingBackend(object):
    def register(self, hooking_cls, callback, workflow_object, field_name, override=False, *args, **kwargs):
        raise NotImplementedError()

    def get_callbacks(self, hooking_cls, workflow_object, field_name, *args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def get_hooking_class(hooking_cls):
        if isinstance(hooking_cls, str):
            module, cls = hooking_cls.rsplit('.', 1)
            hooking_cls = getattr(__import__(module, fromlist=[cls]), cls)
        return hooking_cls

    @staticmethod
    def get_hooking_class_prefix(hooking_cls):
        return '%s.%s_' % (hooking_cls.__module__, hooking_cls.__name__)
