"""Configuração do app Django ``agenda``."""

from django.apps import AppConfig


class AgendaConfig(AppConfig):
    """App de agendas de convocação."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "agenda"
