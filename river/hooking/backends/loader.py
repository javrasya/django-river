from river.config import app_config

__author__ = 'ahmetdal'

handler_module, hooking_cls = app_config.HOOKING_BACKEND_CLASS.rsplit('.', 1)
callback_backend = getattr(__import__(handler_module, fromlist=[hooking_cls]), hooking_cls)(**app_config.HOOKING_BACKEND_CONFIG)
