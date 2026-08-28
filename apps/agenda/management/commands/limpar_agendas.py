"""Django management command to clear all agendas."""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand

from agenda.repository import AgendaRepository


class Command(BaseCommand):
    """Representa Command."""

    help = "Remove todos os registros da tabela de agendas"

    def handle(self, *args: Any, **options: Any) -> None:
        """Roda a lógica principal do comando."""
        total_agendas = AgendaRepository.contar_todas()
        self.stdout.write(
            self.style.SUCCESS(f"Removendo {total_agendas} agendas...")
        )
        try:
            if total_agendas > 0:
                AgendaRepository.excluir_todas()
                self.stdout.write(
                    self.style.SUCCESS(f"{total_agendas} agendas removidas!")
                )
            restantes = AgendaRepository.contar_todas()
            if restantes == 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Tabela de agendas completamente limpa!"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Ainda restam {restantes} agendas.")
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Erro ao remover registros: {e}")
            )
