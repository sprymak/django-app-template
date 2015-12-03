from django.apps import AppConfig


class Config(AppConfig):
    name = __name__.split('.')[0]
    verbose_name = _('{{ app_name }}')

    def ready(self):
        from . import signals
