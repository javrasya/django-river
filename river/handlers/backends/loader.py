from river.services.config import RiverConfig

__author__ = 'ahmetdal'


def load_handler_backend():
    handler_module, handler_cls = RiverConfig.HANDLER_BACKEND_CLASS.rsplit('.', 1)
    return getattr(__import__(handler_module, fromlist=[handler_cls]), handler_cls)(**RiverConfig.HANDLER_BACKEND_CONFIG)


handler_backend = load_handler_backend()
