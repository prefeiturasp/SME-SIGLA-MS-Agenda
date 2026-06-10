"""Django management command to clear all agendas."""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand

from agenda.models import Agenda


class Command(BaseCommand):
    """Representa Command."""

    help = "Remove todos os registros da tabela de agendas"

    def handle(self, *args: Any, **options: Any) -> None:
        """A lógica principal do comando.

        Args:
            self: Instância do objeto.
            *args: Argumentos posicionais variáveis.
            **options: Opções do comando de management.

        Returns:
            Nenhum valor.
        """
        total_agendas = Agenda.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Removendo {total_agendas} agendas...")
        )
        try:
            if total_agendas > 0:
                Agenda.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ {total_agendas} agendas removidas!"
                    )
                )
            restantes = Agenda.objects.count()
            if restantes == 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        "✅ Tabela de agendas completamente limpa!"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Ainda restam {restantes} agendas.")
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erro ao remover registros: {e}")
            )
