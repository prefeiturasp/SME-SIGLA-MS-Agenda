"""
Django admin configuration for the processes module.
"""
from django.contrib import admin
from .models import Agenda


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    """Admin for Agenda model."""

    list_display = (
        'processo_convocacao_nome', 'cargo_nome', 'data_escolha',
    )
    list_filter = ('data_escolha',)
    search_fields = ('processo_convocacao_nome', 'cargo_nome')
    readonly_fields = ('uuid', 'criado_em', 'atualizado_em')
    ordering = ('-data_escolha',)

    fieldsets = (
        ('Processo de Convocação', {
            'fields': ('processo_convocacao_uuid', 'processo_convocacao_nome')
        }),
        ('Cargo', {
            'fields': ('cargo_uuid', 'cargo_nome')
        }),
        ('Datas', {
            'fields': ('data_escolha',)
        }),
        ('Metadados', {
            'fields': ('uuid', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
