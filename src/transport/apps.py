from django.apps import AppConfig


class TransportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transport'
    verbose_name = 'Управление перевозками'

    def ready(self):
        import transport.signals  # noqa
