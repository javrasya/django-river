from river.config import app_config

__author__ = 'ahmetdal'


def load_handler_backend():
    handler_module, handler_cls = app_config.HANDLER_BACKEND_CLASS.rsplit('.', 1)
    return getattr(__import__(handler_module, fromlist=[handler_cls]), handler_cls)(**app_config.HANDLER_BACKEND_CONFIG)


handler_backend = load_handler_backend()
