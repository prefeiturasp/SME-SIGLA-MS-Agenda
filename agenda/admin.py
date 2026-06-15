"""Django admin configuration for the processes module."""

from django.contrib import admin

from .models import Agenda


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    """Admin for Agenda model."""

    list_display = (
        "processo_convocacao_nome",
        "cargo_nome",
        "data_escolha",
        "modalidade",
        "escolha_em",
        "nomeacao_em",
        "classificacao",
        "sessao",
        "retardatario",
    )
    list_filter = (
        "data_escolha",
        "modalidade",
        "retardatario",
        "escolha_em",
        "nomeacao_em",
    )
    search_fields = ("processo_convocacao_nome", "cargo_nome", "sessao")
    readonly_fields = ("uuid", "criado_em", "atualizado_em")
    ordering = ("-data_escolha",)

    fieldsets = (
        (
            "Processo de Convocação",
            {
                "fields": (
                    "processo_convocacao_uuid",
                    "processo_convocacao_nome",
                )
            },
        ),
        ("Cargo", {"fields": ("cargo_uuid", "cargo_nome", "cargo_codigo")}),
        ("Datas", {"fields": ("data_escolha", "escolha_em", "nomeacao_em")}),
        (
            "Informações da Agenda",
            {
                "fields": (
                    "modalidade",
                    "classificacao",
                    "sessao",
                    "retardatario",
                    "candidatos_uuids",
                )
            },
        ),
        (
            "Horários de Convocação",
            {
                "fields": ("hora_convocacao_inicio", "hora_convocacao_fim"),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadados",
            {
                "fields": ("uuid", "criado_em", "atualizado_em"),
                "classes": ("collapse",),
            },
        ),
    )
