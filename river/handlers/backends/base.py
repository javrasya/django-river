from itertools import combinations, chain

__author__ = 'ahmetdal'


def powerset(iterable):
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs, n) for n in range(len(xs) + 1))


class BaseHandlerBackend(object):
    def register(self, handler_cls, handler, workflow_object, field, override=False, *args, **kwargs):
        raise NotImplementedError()

    def get_handlers(self, handler_cls, handler, workflow_object, field, *args, **kwargs):
        raise NotImplementedError()

    def get_handler_class(self, handler_cls):
        if isinstance(handler_cls, str):
            module, cls = handler_cls.rsplit('.', 1)
            handler_cls = getattr(__import__(module, fromlist=[cls]), cls)
        return handler_cls

    def get_handler_class_prefix(self, handler_cls):
        return '%s.%s_' % (handler_cls.__module__, handler_cls.__name__)
