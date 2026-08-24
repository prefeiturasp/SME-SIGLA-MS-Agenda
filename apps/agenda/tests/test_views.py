"""Testes unitários para as views do app agenda usando pytest."""

from __future__ import annotations

import uuid
from datetime import timedelta
from unittest.mock import patch
from urllib.parse import urlencode

import pytest
from django.urls import reverse
from django.utils import timezone
from requests import RequestException
from rest_framework import status
from rest_framework.test import APIClient

from agenda.models import Agenda

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    """Client."""
    return APIClient()


@pytest.fixture
def agenda():
    """Agenda."""
    return Agenda.objects.create(
        processo_convocacao_uuid=uuid.uuid4(),
        processo_convocacao_nome="Processo Lista",
        cargo_uuid=uuid.uuid4(),
        cargo_nome="Analista",
        data_escolha=timezone.now() + timedelta(days=15),
        candidatos_uuids=[],
    )


@pytest.fixture
def agendas():
    """Agendas."""
    itens = []
    for i in range(2):
        itens.append(
            Agenda.objects.create(
                processo_convocacao_uuid=uuid.uuid4(),
                processo_convocacao_nome=f"Processo {i + 1}",
                cargo_uuid=uuid.uuid4(),
                cargo_nome=f"Cargo {i + 1}",
                data_escolha=timezone.now() + timedelta(days=10 + i),
                candidatos_uuids=[uuid.uuid4(), uuid.uuid4()],
            )
        )
    return itens


def test_agenda_list(client, agenda):
    """Verifica agenda list."""
    url = reverse("agendas-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert len(response.data["results"]) == 1
    assert (
        response.data["results"][0]["processo_convocacao_nome"]
        == agenda.processo_convocacao_nome
    )


@patch("agenda.api.views.EscolhasApiService")
def test_list_agenda_online_retorna_candidatos_uuids_restantes(
    mock_escolhas_class, client
):
    """Verifica list agenda online retorna candidatos uuids restantes."""
    cand_1 = str(uuid.uuid4())
    cand_2 = str(uuid.uuid4())
    cand_3 = str(uuid.uuid4())
    Agenda.objects.create(
        processo_convocacao_uuid=uuid.uuid4(),
        processo_convocacao_nome="Processo Online",
        cargo_uuid=uuid.uuid4(),
        cargo_nome="Cargo",
        modalidade="ONLINE",
        candidatos_uuids=[cand_1, cand_2, cand_3],
    )
    mock_service = mock_escolhas_class.return_value
    mock_service.buscar_escolhas_por_processo_uuid.return_value = [
        {"candidato_uuid": cand_1}
    ]
    response = client.get(reverse("agendas-list"))
    assert response.status_code == status.HTTP_200_OK
    assert "candidatos_uuids_restantes" in response.data
    assert set(response.data["candidatos_uuids_restantes"]) == {cand_2, cand_3}


@patch("agenda.api.views.EscolhasApiService")
def test_list_agenda_online_restantes_vazio_quando_todos_escolhidos(
    mock_escolhas_class, client
):
    """Verifica list agenda online restantes vazio quando todos escolhidos."""
    cand_1 = str(uuid.uuid4())
    cand_2 = str(uuid.uuid4())
    Agenda.objects.create(
        processo_convocacao_uuid=uuid.uuid4(),
        processo_convocacao_nome="Processo Online",
        cargo_uuid=uuid.uuid4(),
        cargo_nome="Cargo",
        modalidade="ONLINE",
        candidatos_uuids=[cand_1, cand_2],
    )
    mock_service = mock_escolhas_class.return_value
    mock_service.buscar_escolhas_por_processo_uuid.return_value = [
        {"candidato_uuid": cand_1},
        {"candidato_uuid": cand_2},
    ]
    response = client.get(reverse("agendas-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["candidatos_uuids_restantes"] == []


@patch("agenda.api.views.EscolhasApiService")
def test_list_agenda_online_aceita_escolhas_com_results(
    mock_escolhas_class, client
):
    """Verifica list agenda online aceita escolhas com results."""
    cand_1 = str(uuid.uuid4())
    Agenda.objects.create(
        processo_convocacao_uuid=uuid.uuid4(),
        processo_convocacao_nome="Processo Online",
        cargo_uuid=uuid.uuid4(),
        cargo_nome="Cargo",
        modalidade="ONLINE",
        candidatos_uuids=[cand_1],
    )
    mock_service = mock_escolhas_class.return_value
    mock_service.buscar_escolhas_por_processo_uuid.return_value = {
        "results": [{"candidato_uuid": cand_1}],
        "count": 1,
    }
    response = client.get(reverse("agendas-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["candidatos_uuids_restantes"] == []


def test_list_agenda_presencial_nao_adiciona_candidatos_uuids_restantes(
    client,
):
    """Verifica list agenda presencial nao adiciona candidatos uuids restantes."""
    Agenda.objects.create(
        processo_convocacao_uuid=uuid.uuid4(),
        processo_convocacao_nome="Processo Presencial",
        cargo_uuid=uuid.uuid4(),
        cargo_nome="Cargo",
        modalidade="PRESENCIAL",
        candidatos_uuids=[str(uuid.uuid4())],
    )
    response = client.get(reverse("agendas-list"))
    assert response.status_code == status.HTTP_200_OK
    assert "candidatos_uuids_restantes" not in response.data


def test_list_lista_vazia_nao_quebra(client):
    """Verifica list lista vazia nao quebra."""
    response = client.get(reverse("agendas-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("results") == []
    assert "candidatos_uuids_restantes" not in response.data


@patch("agenda.api.views.EscolhasApiService")
def test_list_agenda_online_request_exception_retorna_200_sem_restantes(
    mock_escolhas_class, client
):
    """Verifica list agenda online request exception retorna 200 sem restantes."""
    Agenda.objects.create(
        processo_convocacao_uuid=uuid.uuid4(),
        processo_convocacao_nome="Processo Online",
        cargo_uuid=uuid.uuid4(),
        cargo_nome="Cargo",
        modalidade="ONLINE",
        candidatos_uuids=[str(uuid.uuid4())],
    )
    mock_service = mock_escolhas_class.return_value
    mock_service.buscar_escolhas_por_processo_uuid.side_effect = (
        RequestException("timeout")
    )
    response = client.get(reverse("agendas-list"))
    assert response.status_code == status.HTTP_200_OK
    assert "candidatos_uuids_restantes" not in response.data


@patch("agenda.api.views.CandidatosApiService")
def test_agenda_create(mock_service_class, client):
    """Verifica agenda create."""
    cand_uuid_1 = uuid.uuid4()
    cand_uuid_2 = uuid.uuid4()
    processo_uuid = uuid.uuid4()
    cargo_uuid = uuid.uuid4()
    mock_service = mock_service_class.return_value
    mock_service.buscar_por_uuids_ordenado_por_ranking_escolha.return_value = [
        {"uuid": cand_uuid_1, "ranking_escolha": 1},
        {"uuid": cand_uuid_2, "ranking_escolha": 2},
    ]
    url = reverse("agendas-list")
    data = {
        "agendas": [
            {
                "cargo_uuid": str(cargo_uuid),
                "cargo_nome": "Cargo Novo",
                "cargo_codigo": "123456",
                "classificacao": 2,
                "data_escolha": (
                    timezone.now() + timedelta(days=30)
                ).isoformat(),
            }
        ],
        "candidatos_uuids": [str(cand_uuid_1), str(cand_uuid_2)],
        "processo_uuid": str(processo_uuid),
        "processo_nome": "Processo Novo",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Agenda.objects.count() == 1
    item = Agenda.objects.first()
    assert item.processo_convocacao_nome == "Processo Novo"
    assert item.cargo_nome == "Cargo Novo"
    assert str(item.processo_convocacao_uuid) == str(processo_uuid)


@patch("agenda.api.views.CandidatosApiService")
def test_agenda_create_request_exception_api_candidatos_retorna_502(
    mock_service_class, client
):
    """Verifica agenda create request exception api candidatos retorna 502."""
    cand_uuid = uuid.uuid4()
    processo_uuid = uuid.uuid4()
    cargo_uuid = uuid.uuid4()
    mock_service = mock_service_class.return_value
    mock_service.buscar_por_uuids_ordenado_por_ranking_escolha.side_effect = (
        RequestException("Erro de conexão")
    )
    url = reverse("agendas-list")
    data = {
        "agendas": [
            {
                "cargo_uuid": str(cargo_uuid),
                "cargo_nome": "Cargo Novo",
                "cargo_codigo": "123456",
                "classificacao": 1,
                "data_escolha": (
                    timezone.now() + timedelta(days=30)
                ).isoformat(),
            }
        ],
        "candidatos_uuids": [str(cand_uuid)],
        "processo_uuid": str(processo_uuid),
        "processo_nome": "Processo Novo",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    assert response.data["detail"] == "Erro ao consultar API de candidatos."
    assert Agenda.objects.count() == 0


@patch("agenda.api.views.CandidatosApiService")
def test_agenda_create_com_uuid_existente_atualiza(mock_service_class, client):
    """Verifica agenda create com uuid existente atualiza."""
    mock_service = mock_service_class.return_value
    mock_method = mock_service.buscar_por_uuids_ordenado_por_ranking_escolha
    mock_method.return_value = []
    processo_uuid = uuid.uuid4()
    cargo_uuid = uuid.uuid4()
    agenda_existente = Agenda.objects.create(
        processo_convocacao_uuid=processo_uuid,
        processo_convocacao_nome="Processo Original",
        cargo_uuid=cargo_uuid,
        cargo_nome="Cargo Original",
        candidatos_uuids=[],
    )
    url = reverse("agendas-list")
    data = {
        "agendas": [
            {
                "uuid": str(agenda_existente.uuid),
                "cargo_uuid": str(cargo_uuid),
                "cargo_nome": "Cargo Atualizado",
                "cargo_codigo": "123",
                "classificacao": 0,
            }
        ],
        "candidatos_uuids": [],
        "processo_uuid": str(processo_uuid),
        "processo_nome": "Processo Atualizado",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Agenda.objects.count() == 1
    agenda_existente.refresh_from_db()
    assert agenda_existente.cargo_nome == "Cargo Atualizado"
    assert agenda_existente.processo_convocacao_nome == "Processo Atualizado"


@patch("agenda.api.views.CandidatosApiService")
def test_agenda_create_com_uuid_inexistente_cria_nova(
    mock_service_class, client
):
    """Verifica agenda create com uuid inexistente cria nova."""
    mock_service = mock_service_class.return_value
    mock_method = mock_service.buscar_por_uuids_ordenado_por_ranking_escolha
    mock_method.return_value = []
    processo_uuid = uuid.uuid4()
    cargo_uuid = uuid.uuid4()
    uuid_fake = uuid.uuid4()
    url = reverse("agendas-list")
    data = {
        "agendas": [
            {
                "uuid": str(uuid_fake),
                "cargo_uuid": str(cargo_uuid),
                "cargo_nome": "Cargo Novo",
                "cargo_codigo": "123",
                "classificacao": 0,
            }
        ],
        "candidatos_uuids": [],
        "processo_uuid": str(processo_uuid),
        "processo_nome": "Processo Novo",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Agenda.objects.count() == 1
    item = Agenda.objects.first()
    assert item.cargo_nome == "Cargo Novo"
    assert item.processo_convocacao_nome == "Processo Novo"
    assert item.uuid != uuid_fake


def test_agenda_retrieve(client, agenda):
    """Verifica agenda retrieve."""
    url = reverse("agendas-detail", args=[agenda.uuid])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.data["processo_convocacao_nome"]
        == agenda.processo_convocacao_nome
    )
    assert response.data["uuid"] == str(agenda.uuid)


def test_agenda_update(client, agenda):
    """Verifica agenda update."""
    url = reverse("agendas-detail", args=[agenda.uuid])
    data = {
        "processo_convocacao_nome": "Processo Atualizado",
        "cargo_nome": "Cargo Atualizado",
    }
    response = client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    agenda.refresh_from_db()
    assert agenda.processo_convocacao_nome == "Processo Atualizado"
    assert agenda.cargo_nome == "Cargo Atualizado"


def test_agenda_delete(client, agenda):
    """Verifica agenda delete."""
    url = reverse("agendas-detail", args=[agenda.uuid])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Agenda.objects.count() == 0


def test_excluir_por_processo_sem_processo_uuid_retorna_400(client):
    """Verifica excluir por processo sem processo uuid retorna 400."""
    url = reverse("agendas-excluir-por-processo")
    response = client.delete(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "processo_uuid é obrigatório."


def test_excluir_por_processo_remove_apenas_agendas_do_processo(client):
    """Verifica excluir por processo remove apenas agendas do processo."""
    processo_a = uuid.uuid4()
    processo_b = uuid.uuid4()
    cargo_a = uuid.uuid4()
    cargo_b = uuid.uuid4()
    Agenda.objects.create(
        processo_convocacao_uuid=processo_a,
        processo_convocacao_nome="Processo A",
        cargo_uuid=cargo_a,
        cargo_nome="Cargo A",
        data_escolha=timezone.now(),
        candidatos_uuids=[],
    )
    Agenda.objects.create(
        processo_convocacao_uuid=processo_a,
        processo_convocacao_nome="Processo A",
        cargo_uuid=cargo_a,
        cargo_nome="Cargo A2",
        data_escolha=timezone.now(),
        candidatos_uuids=[],
    )
    outra = Agenda.objects.create(
        processo_convocacao_uuid=processo_b,
        processo_convocacao_nome="Processo B",
        cargo_uuid=cargo_b,
        cargo_nome="Cargo B",
        data_escolha=timezone.now(),
        candidatos_uuids=[],
    )
    base = reverse("agendas-excluir-por-processo")
    url = f"{base}?{urlencode({'processo_uuid': str(processo_a)})}"
    response = client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["excluidas"] == 2
    assert Agenda.objects.count() == 1
    assert Agenda.objects.filter(uuid=outra.uuid).exists()


def test_excluir_por_processo_sem_agendas_retorna_zero(client):
    """Verifica excluir por processo sem agendas retorna zero."""
    processo_uuid = uuid.uuid4()
    base = reverse("agendas-excluir-por-processo")
    url = f"{base}?{urlencode({'processo_uuid': str(processo_uuid)})}"
    response = client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["excluidas"] == 0


def test_excluir_por_processo_e_cargo_sem_processo_uuid_retorna_400(client):
    """Verifica excluir por processo e cargo sem processo uuid retorna 400."""
    base = reverse("agendas-excluir-por-processo-e-cargo")
    url = f"{base}?{urlencode({'cargo': str(uuid.uuid4())})}"
    response = client.delete(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "processo_uuid é obrigatório."


def test_excluir_por_processo_e_cargo_sem_cargo_retorna_400(client):
    """Verifica excluir por processo e cargo sem cargo retorna 400."""
    base = reverse("agendas-excluir-por-processo-e-cargo")
    url = f"{base}?{urlencode({'processo_uuid': str(uuid.uuid4())})}"
    response = client.delete(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "cargo é obrigatório."


def test_excluir_por_processo_e_cargo_remove_apenas_agendas_do_filtro(client):
    """Verifica exclusão apenas das agendas do processo e cargo informados."""
    processo_a = uuid.uuid4()
    processo_b = uuid.uuid4()
    cargo_a = uuid.uuid4()
    cargo_b = uuid.uuid4()
    Agenda.objects.create(
        processo_convocacao_uuid=processo_a,
        processo_convocacao_nome="Processo A",
        cargo_uuid=cargo_a,
        cargo_nome="Cargo A",
        cargo_codigo="123456",
        data_escolha=timezone.now(),
        candidatos_uuids=[],
    )
    mesmo_processo_outro_cargo = Agenda.objects.create(
        processo_convocacao_uuid=processo_a,
        processo_convocacao_nome="Processo A",
        cargo_uuid=cargo_b,
        cargo_nome="Cargo B",
        cargo_codigo="123456",
        data_escolha=timezone.now(),
        candidatos_uuids=[],
    )
    outro_processo_mesmo_cargo = Agenda.objects.create(
        processo_convocacao_uuid=processo_b,
        processo_convocacao_nome="Processo B",
        cargo_uuid=cargo_a,
        cargo_nome="Cargo A",
        cargo_codigo="1234567",
        data_escolha=timezone.now(),
        candidatos_uuids=[],
    )
    base = reverse("agendas-excluir-por-processo-e-cargo")
    url = f'{base}?{urlencode({
            "processo_uuid": str(processo_a),
            "cargo": "123456",
        })}'
    response = client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["excluidas"] == 2
    assert Agenda.objects.count() == 1
    assert not Agenda.objects.filter(
        uuid=mesmo_processo_outro_cargo.uuid
    ).exists()
    assert Agenda.objects.filter(uuid=outro_processo_mesmo_cargo.uuid).exists()


def test_excluir_por_processo_e_cargo_sem_agendas_retorna_zero(client):
    """Verifica excluir por processo e cargo sem agendas retorna zero."""
    base = reverse("agendas-excluir-por-processo-e-cargo")
    url = f'{base}?{urlencode({
            "processo_uuid": str(uuid.uuid4()),
            "cargo": str(uuid.uuid4()),
        })}'
    response = client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["excluidas"] == 0
