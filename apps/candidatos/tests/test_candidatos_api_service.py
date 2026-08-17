"""Testes unitários para candidatos/services/candidatos_api_service.py.

Cobre __init__ (linhas 19-21) e
buscar_por_uuids_ordenado_por_ranking_escolha (linhas 47-86).
"""

from __future__ import annotations

import uuid
from unittest.mock import MagicMock, patch

import pytest
import requests

from candidatos.services.candidatos_api_service import CandidatosApiService


def test_init_strips_trailing_slash_from_base_url():
    """Verifica init strips trailing slash from base url."""
    svc = CandidatosApiService(base_url="http://localhost:8000/")
    assert svc.base_url == "http://localhost:8000"


def test_init_keeps_url_without_trailing_slash():
    """Verifica init keeps url without trailing slash."""
    svc = CandidatosApiService(base_url="http://api.example.com")
    assert svc.base_url == "http://api.example.com"


def test_init_default_timeout():
    """Verifica init default timeout."""
    svc = CandidatosApiService(base_url="http://x.com")
    assert svc.timeout_seconds == 30


def test_init_custom_timeout():
    """Verifica init custom timeout."""
    svc = CandidatosApiService(base_url="http://x.com", timeout_seconds=10)
    assert svc.timeout_seconds == 10


def test_init_sets_headers():
    """Verifica init sets headers."""
    svc = CandidatosApiService(base_url="http://x.com")
    assert svc._headers == {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def test_buscar_por_uuids_empty_list_returns_empty():
    """Verifica buscar por uuids empty list returns empty."""
    svc = CandidatosApiService(base_url="http://x.com")
    result = svc.buscar_por_uuids_ordenado_por_ranking_escolha(uuids=[])
    assert result == []


def test_buscar_por_uuids_empty_list_does_not_call_requests():
    """Verifica buscar por uuids empty list does not call requests."""
    svc = CandidatosApiService(base_url="http://x.com")
    with patch(
        "candidatos.services.candidatos_api_service.http_client.post"
    ) as mock_post:
        svc.buscar_por_uuids_ordenado_por_ranking_escolha(uuids=[])
        mock_post.assert_not_called()


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_calls_correct_url_and_params(mock_http_client_post):
    """Verifica buscar por uuids calls correct url and params."""
    mock_http_client_post.return_value.json.return_value = {"results": []}
    mock_http_client_post.return_value.raise_for_status = MagicMock()
    svc = CandidatosApiService(base_url="http://candidatos:8000")
    svc.buscar_por_uuids_ordenado_por_ranking_escolha(
        uuids=["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"],
        fields="uuid,ranking_escolha",
    )
    mock_http_client_post.assert_called_once()
    call_args, call_kw = mock_http_client_post.call_args
    assert (
        call_args[0]
        == "http://candidatos:8000/api/v1/habilitados/buscar-por-uuids/"
    )
    assert call_kw["params"] == {
        "fields": "uuid,ranking_escolha",
        "order_by": "ranking_escolha",
    }
    assert call_kw["json"] == {
        "uuids": ["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"]
    }
    assert call_kw["headers"] == svc._headers
    assert call_kw["timeout"] == 30


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_custom_fields_and_timeout(mock_http_client_post):
    """Verifica buscar por uuids custom fields and timeout."""
    mock_http_client_post.return_value.json.return_value = {"results": []}
    mock_http_client_post.return_value.raise_for_status = MagicMock()
    svc = CandidatosApiService(base_url="http://x.com", timeout_seconds=5)
    svc.buscar_por_uuids_ordenado_por_ranking_escolha(
        uuids=["uuid-1"], fields="uuid,nome,ranking_escolha"
    )
    call_kw = mock_http_client_post.call_args[1]
    assert call_kw["params"]["fields"] == "uuid,nome,ranking_escolha"
    assert call_kw["timeout"] == 5


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_converts_uuids_to_strings(mock_http_client_post):
    """Verifica buscar por uuids converts uuids to strings."""
    mock_http_client_post.return_value.json.return_value = {"results": []}
    mock_http_client_post.return_value.raise_for_status = MagicMock()
    u = uuid.uuid4()
    svc = CandidatosApiService(base_url="http://x.com")
    svc.buscar_por_uuids_ordenado_por_ranking_escolha(uuids=[u])
    assert mock_http_client_post.call_args[1]["json"]["uuids"] == [str(u)]


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_uses_results_key_when_present(mock_http_client_post):
    """Verifica buscar por uuids uses results key when present."""
    mock_http_client_post.return_value.raise_for_status = MagicMock()
    mock_http_client_post.return_value.json.return_value = {
        "results": [
            {"uuid": "a", "ranking_escolha": 1},
            {"uuid": "b", "ranking_escolha": 2},
        ],
        "count": 2,
    }
    svc = CandidatosApiService(base_url="http://x.com")
    result = svc.buscar_por_uuids_ordenado_por_ranking_escolha(
        uuids=["a", "b"]
    )
    assert len(result) == 2
    assert result[0]["uuid"] == "a"
    assert result[1]["uuid"] == "b"


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_uses_data_as_list_when_no_results_key(
    mock_http_client_post,
):
    """Verifica buscar por uuids uses data as list when no results key."""
    mock_http_client_post.return_value.raise_for_status = MagicMock()
    mock_http_client_post.return_value.json.return_value = [
        {"uuid": "x", "ranking_escolha": 1}
    ]
    svc = CandidatosApiService(base_url="http://x.com")
    result = svc.buscar_por_uuids_ordenado_por_ranking_escolha(uuids=["x"])
    assert len(result) == 1
    assert result[0]["uuid"] == "x"


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_non_dict_response_returns_empty_list(
    mock_http_client_post,
):
    """Verifica buscar por uuids non dict response returns empty list."""
    mock_http_client_post.return_value.raise_for_status = MagicMock()
    mock_http_client_post.return_value.json.return_value = "not a dict"
    svc = CandidatosApiService(base_url="http://x.com")
    result = svc.buscar_por_uuids_ordenado_por_ranking_escolha(uuids=["a"])
    assert result == []


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_results_not_list_returns_empty_list(
    mock_http_client_post,
):
    """Verifica buscar por uuids results not list returns empty list."""
    mock_http_client_post.return_value.raise_for_status = MagicMock()
    mock_http_client_post.return_value.json.return_value = {
        "results": "not a list"
    }
    svc = CandidatosApiService(base_url="http://x.com")
    result = svc.buscar_por_uuids_ordenado_por_ranking_escolha(uuids=["a"])
    assert result == []


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_sorts_by_ranking_escolha_asc(mock_post):
    """Verifica buscar por uuids sorts by ranking escolha asc."""
    mock_post.return_value.raise_for_status = MagicMock()
    mock_post.return_value.json.return_value = {
        "results": [
            {"uuid": "c", "ranking_escolha": 3},
            {"uuid": "a", "ranking_escolha": 1},
            {"uuid": "b", "ranking_escolha": 2},
        ]
    }
    svc = CandidatosApiService(base_url="http://x.com")
    result = svc.buscar_por_uuids_ordenado_por_ranking_escolha(
        uuids=["a", "b", "c"]
    )
    assert [r["ranking_escolha"] for r in result] == [1, 2, 3]
    assert [r["uuid"] for r in result] == ["a", "b", "c"]


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_none_ranking_goes_last(mock_http_client_post):
    """Verifica buscar por uuids none ranking goes last."""
    mock_http_client_post.return_value.raise_for_status = MagicMock()
    mock_http_client_post.return_value.json.return_value = {
        "results": [
            {"uuid": "a", "ranking_escolha": None},
            {"uuid": "b", "ranking_escolha": 1},
        ]
    }
    svc = CandidatosApiService(base_url="http://x.com")
    result = svc.buscar_por_uuids_ordenado_por_ranking_escolha(
        uuids=["a", "b"]
    )
    assert result[0]["uuid"] == "b"
    assert result[1]["uuid"] == "a"


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_invalid_ranking_goes_last(mock_http_client_post):
    """Verifica buscar por uuids invalid ranking goes last."""
    mock_http_client_post.return_value.raise_for_status = MagicMock()
    mock_http_client_post.return_value.json.return_value = {
        "results": [
            {"uuid": "a", "ranking_escolha": "não é número"},
            {"uuid": "b", "ranking_escolha": 1},
        ]
    }
    svc = CandidatosApiService(base_url="http://x.com")
    result = svc.buscar_por_uuids_ordenado_por_ranking_escolha(
        uuids=["a", "b"]
    )
    assert result[0]["uuid"] == "b"
    assert result[1]["uuid"] == "a"


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_raise_for_status_called(mock_http_client_post):
    """Verifica buscar por uuids raise for status called."""
    mock_http_client_post.return_value.json.return_value = {"results": []}
    mock_http_client_post.return_value.raise_for_status = MagicMock()
    svc = CandidatosApiService(base_url="http://x.com")
    svc.buscar_por_uuids_ordenado_por_ranking_escolha(uuids=["a"])
    mock_http_client_post.return_value.raise_for_status.assert_called_once()


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_raises_on_http_error(mock_http_client_post):
    """Verifica buscar por uuids raises on http error."""
    mock_http_client_post.return_value.raise_for_status.side_effect = (
        requests.HTTPError("404")
    )
    svc = CandidatosApiService(base_url="http://x.com")
    with pytest.raises(requests.RequestException):
        svc.buscar_por_uuids_ordenado_por_ranking_escolha(uuids=["a"])


@patch("candidatos.services.candidatos_api_service.http_client.post")
def test_buscar_por_uuids_raises_on_connection_error(mock_http_client_post):
    """Verifica buscar por uuids raises on connection error."""
    mock_http_client_post.side_effect = requests.RequestException(
        "Connection refused"
    )
    svc = CandidatosApiService(base_url="http://x.com")
    with pytest.raises(requests.RequestException):
        svc.buscar_por_uuids_ordenado_por_ranking_escolha(uuids=["a"])
