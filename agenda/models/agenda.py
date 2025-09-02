from django.db import models
from django.utils import timezone

from auditlog.registry import auditlog

from .base import BaseModel


class Agenda(BaseModel):
    """
    Modelo para representar agendas de convocação.
    """

    processo_convocacao_uuid = models.UUIDField(verbose_name="UUID do Processo de Convocação")
    processo_convocacao_nome = models.CharField(max_length=200, verbose_name="Nome do Processo de Convocação")
    cargo_uuid = models.UUIDField(verbose_name="UUID do Cargo")
    cargo_nome = models.CharField(max_length=200, verbose_name="Nome do Cargo")
    data_escolha = models.DateTimeField(verbose_name="Data de Publicação", default=timezone.now)

    class Meta:
        verbose_name = "Agenda de Convocação"
        verbose_name_plural = "Agendas de Convocação"
        ordering = ['-criado_em']
        db_table = 'agenda'
    
    def __str__(self):
        return f"{self.processo_convocacao_nome} - {self.cargo_nome}"

auditlog.register(Agenda)
