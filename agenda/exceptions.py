"""Módulo exceptions."""
from __future__ import annotations
from typing import Any

class AgendaOnlineJaExisteException(Exception):
    """Indica que uma agenda online já existe para o processo e cargo."""

    def __init__(self, processo_nome: Any, cargo_nome: Any) -> None:
        """Executa   init  ."""
        self.processo_nome = processo_nome
        self.cargo_nome = cargo_nome
        super().__init__(f'Agenda online já existe para o processo {processo_nome} e cargo {cargo_nome}')
