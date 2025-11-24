from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

from auditlog.registry import auditlog

from .base import BaseModel
from .constants import MODALIDADE_CHOICES


class Agenda(BaseModel):
    """
    Modelo para representar agendas de convocação.
    """

    processo_convocacao_uuid = models.UUIDField(verbose_name="UUID do Processo de Convocação")
    processo_convocacao_nome = models.CharField(max_length=200, verbose_name="Nome do Processo de Convocação")
    cargo_uuid = models.UUIDField(verbose_name="UUID do Cargo")
    cargo_nome = models.CharField(max_length=200, verbose_name="Nome do Cargo")
    cargo_codigo = models.CharField(max_length=20, verbose_name="Código do Cargo", default="")
    data_escolha = models.DateTimeField(verbose_name="Data de Publicação", default=timezone.now)

    modalidade = models.CharField(
        max_length=20,
        choices=MODALIDADE_CHOICES,
        verbose_name="Modalidade",
        blank=True,
        null=True
    )
    escolha_em = models.DateField(
        verbose_name="Data de Escolha",
        blank=True,
        null=True
    )
    nomeacao_em = models.DateField(
        verbose_name="Data de Nomeação",
        blank=True,
        null=True
    )
    classificacao = models.IntegerField(
        verbose_name="Classificação",
        blank=True,
        null=True
    )
    sessao = models.CharField(
        max_length=200,
        verbose_name="Sessão",
        blank=True,
        null=True
    )
    retardatario = models.BooleanField(
        verbose_name="Retardatário",
        default=False,
        blank=True,
        null=True
    )
    hora_convocacao_inicio = models.TimeField(
        verbose_name="Hora de Início da Convocação",
        blank=True,
        null=True
    )
    hora_convocacao_fim = models.TimeField(
        verbose_name="Hora de Fim da Convocação",
        blank=True,
        null=True
    )
    candidatos_uuids = ArrayField(
        base_field=models.UUIDField(),
        default=list,
        blank=True,
        null=True,
        verbose_name="UUIDs dos Candidatos"
    )

    class Meta:
        verbose_name = "Agenda de Convocação"
        verbose_name_plural = "Agendas de Convocação"
        ordering = ['escolha_em', 'hora_convocacao_inicio']
        db_table = 'agenda'
    
    def __str__(self):
        return f"{self.processo_convocacao_nome} - {self.cargo_nome}"

auditlog.register(Agenda)
