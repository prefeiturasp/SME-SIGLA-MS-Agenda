"""Configuração para testes do app agenda."""

from __future__ import annotations

import uuid

import pytest
from django.utils import timezone

from agenda.models import Agenda


@pytest.fixture
def agenda():
    """Cria uma Agenda de teste."""
    from django.utils import timezone

    return Agenda.objects.create(
        processo_convocacao_uuid=uuid.uuid4(),
        processo_convocacao_nome="Processo Teste",
        cargo_uuid=uuid.uuid4(),
        cargo_nome="Analista de Sistemas",
        data_escolha=timezone.now(),
    )


@pytest.fixture
def agendas_multiplas():
    """Cria múltiplas Agendas de teste."""
    itens = []
    for i in range(3):
        itens.append(
            Agenda.objects.create(
                processo_convocacao_uuid=uuid.uuid4(),
                processo_convocacao_nome=f"Processo {i + 1}",
                cargo_uuid=uuid.uuid4(),
                cargo_nome=f"Cargo {i + 1}",
                data_escolha=timezone.now() + timezone.timedelta(days=i),
            )
        )
    return itens
