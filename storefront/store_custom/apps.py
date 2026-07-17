from django.apps import AppConfig


class StoreCustomConfig(AppConfig):
    name = 'store_custom'

    def ready(self):
        import store_custom.signals.handler