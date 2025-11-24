"""
Testes unitários para as views do app agenda usando pytest.
"""
import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
import uuid

from ..models import Agenda
from ..serializers import AgendaSerializer


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
            )
        )
    return itens


# Testes para AgendaViewSet

def test_agenda_list(client, agenda):
    url = reverse('agenda-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['processo_convocacao_nome'] == agenda.processo_convocacao_nome


def test_agenda_create(client):
    url = reverse('agenda-list')
    data = {
        'processo_convocacao_uuid': str(uuid.uuid4()),
        'processo_convocacao_nome': 'Processo Novo',
        'cargo_uuid': str(uuid.uuid4()),
        'cargo_nome': 'Cargo Novo',
        'data_escolha': (timezone.now() + timedelta(days=30)).isoformat(),
    }

    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Agenda.objects.count() == 1

    item = Agenda.objects.first()
    assert item.processo_convocacao_nome == 'Processo Novo'
    assert item.cargo_nome == 'Cargo Novo'


def test_agenda_retrieve(client, agenda):
    url = reverse('agenda-detail', args=[agenda.uuid])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['processo_convocacao_nome'] == agenda.processo_convocacao_nome
    assert response.data['uuid'] == str(agenda.uuid)


def test_agenda_update(client, agenda):
    url = reverse('agenda-detail', args=[agenda.uuid])
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
    url = reverse('agenda-detail', args=[agenda.uuid])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Agenda.objects.count() == 0
