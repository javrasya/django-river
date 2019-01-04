from river.config import app_config

__author__ = 'ahmetdal'


def load_callback_backend():
    handler_module, hooking_cls = app_config.HOOKING_BACKEND_CLASS.rsplit('.', 1)
    return getattr(__import__(handler_module, fromlist=[hooking_cls]), hooking_cls)(**app_config.HOOKING_BACKEND_CONFIG)


callback_backend = load_callback_backend()
