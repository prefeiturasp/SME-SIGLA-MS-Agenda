"""Repositório de acesso a dados de agendas."""

from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from agenda.models import Agenda

logger = logging.getLogger(__name__)


class AgendaRepository:
    """Acesso aos dados de agendas (consultas e persistência)."""

    @classmethod
    def buscar_pelo_uuid(cls, agenda_uuid: str | UUID) -> Agenda:
        """Busca uma agenda pelo UUID.

        Raises:
            Agenda.DoesNotExist: Quando não encontrada.
        """
        logger.info(f"Buscando agenda pelo UUID: {agenda_uuid}")
        return Agenda.objects.get(uuid=agenda_uuid)

    @classmethod
    def criar(cls, **kwargs: Any) -> Agenda:
        """Persiste uma nova agenda."""
        logger.info(
            f"Criando agenda: "
            f"processo={kwargs.get('processo_convocacao_nome')}, "
            f"cargo={kwargs.get('cargo_nome')}"
        )
        return Agenda.objects.create(**kwargs)

    @classmethod
    def contar_todas(cls) -> int:
        """Retorna a quantidade de agendas cadastradas."""
        logger.info("Contando agendas cadastradas")
        return Agenda.objects.count()

    @classmethod
    def excluir_todas(cls) -> int:
        """Remove todas as agendas.

        Returns:
            Quantidade de agendas excluídas.
        """
        logger.info("Excluindo todas as agendas")
        deleted, _ = Agenda.objects.all().delete()
        return deleted

    @classmethod
    def excluir_do_processo(cls, processo_uuid: str | UUID) -> int:
        """Remove agendas vinculadas ao processo de convocação.

        Returns:
            Quantidade de agendas excluídas.
        """
        logger.info(f"Excluindo agendas do processo: {processo_uuid}")
        deleted, _ = Agenda.objects.filter(
            processo_convocacao_uuid=processo_uuid
        ).delete()
        return deleted

    @classmethod
    def excluir_do_processo_e_cargo(
        cls, processo_uuid: str | UUID, cargo_codigo: str
    ) -> int:
        """Remove agendas do processo filtradas pelo código do cargo.

        Returns:
            Quantidade de agendas excluídas.
        """
        logger.info(
            f"Excluindo agendas do processo {processo_uuid} "
            f"e cargo {cargo_codigo}"
        )
        deleted, _ = Agenda.objects.filter(
            processo_convocacao_uuid=processo_uuid, cargo_codigo=cargo_codigo
        ).delete()
        return deleted
