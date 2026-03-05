"""
Testes unitários para as views do app agenda usando pytest.
"""
import uuid
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Agenda


pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def agenda():
    return Agenda.objects.create(
        processo_convocacao_uuid=uuid.uuid4(),
        processo_convocacao_nome="Processo Lista",
        cargo_uuid=uuid.uuid4(),
        cargo_nome="Analista",
        data_escolha=timezone.now() + timezone.timedelta(days=15),
        candidatos_uuids=[uuid.uuid4(), uuid.uuid4()],
    )


@pytest.fixture
def agendas():
    itens = []
    for i in range(2):
        itens.append(
            Agenda.objects.create(
                processo_convocacao_uuid=uuid.uuid4(),
                processo_convocacao_nome=f"Processo {i+1}",
                cargo_uuid=uuid.uuid4(),
                cargo_nome=f"Cargo {i+1}",
                data_escolha=timezone.now() + timezone.timedelta(days=10 + i),
                candidatos_uuids=[uuid.uuid4(), uuid.uuid4()],
            )
        )
    return itens


# Testes para AgendaViewSet
def test_agenda_list(client, agenda):
    url = reverse('agendas-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['processo_convocacao_nome'] == agenda.processo_convocacao_nome


@patch('agenda.views.agenda.CandidatosApiService')
def test_agenda_create(mock_service_class, client):
    """Create aceita payload com agendas, candidatos_uuids, processo_uuid, processo_nome."""
    cand_uuid_1 = uuid.uuid4()
    cand_uuid_2 = uuid.uuid4()
    processo_uuid = uuid.uuid4()
    cargo_uuid = uuid.uuid4()

    mock_service_class.return_value.buscar_por_uuids_ordenado_por_ranking_escolha.return_value = [
        {'uuid': cand_uuid_1, 'ranking_escolha': 1},
        {'uuid': cand_uuid_2, 'ranking_escolha': 2},
    ]

    url = reverse('agendas-list')
    data = {
        'agendas': [
            {
                'cargo_uuid': str(cargo_uuid),
                'cargo_nome': 'Cargo Novo',
                'cargo_codigo': '123456',
                'classificacao': 2,
                'data_escolha': (timezone.now() + timedelta(days=30)).isoformat(),
            }
        ],
        'candidatos_uuids': [str(cand_uuid_1), str(cand_uuid_2)],
        'processo_uuid': str(processo_uuid),
        'processo_nome': 'Processo Novo',
    }

    response = client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Agenda.objects.count() == 1
    # breakpoint()

    item = Agenda.objects.first()
    assert item.processo_convocacao_nome == 'Processo Novo'
    assert item.cargo_nome == 'Cargo Novo'
    assert str(item.processo_convocacao_uuid) == str(processo_uuid)


def test_agenda_retrieve(client, agenda):
    url = reverse('agendas-detail', args=[agenda.uuid])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['processo_convocacao_nome'] == agenda.processo_convocacao_nome
    assert response.data['uuid'] == str(agenda.uuid)


def test_agenda_update(client, agenda):
    url = reverse('agendas-detail', args=[agenda.uuid])
    data = {
        'processo_convocacao_nome': 'Processo Atualizado',
        'cargo_nome': 'Cargo Atualizado',
    }

    response = client.patch(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    agenda.refresh_from_db()
    assert agenda.processo_convocacao_nome == 'Processo Atualizado'
    assert agenda.cargo_nome == 'Cargo Atualizado'


def test_agenda_delete(client, agenda):
    url = reverse('agendas-detail', args=[agenda.uuid])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Agenda.objects.count() == 0
