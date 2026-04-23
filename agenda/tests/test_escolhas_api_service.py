"""
Testes unitários para agenda/services/escolhas_api_service.py.
"""
import uuid
from unittest.mock import MagicMock, patch

import pytest
import requests

from agenda.services.escolhas_api_service import EscolhasApiService


def test_escolhas_api_service_init_strips_trailing_slash():
    svc = EscolhasApiService(base_url='http://escolhas:8000/')
    assert svc.base_url == 'http://escolhas:8000'


def test_escolhas_api_service_init_custom_timeout():
    svc = EscolhasApiService(base_url='http://x.com', timeout_seconds=15)
    assert svc.timeout_seconds == 15


def test_escolhas_api_service_init_headers():
    svc = EscolhasApiService(base_url='http://x.com')
    assert svc._headers == {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }


@patch('agenda.services.escolhas_api_service.http_client.get')
def test_buscar_escolhas_por_processo_uuid_chama_url_params_headers_timeout(mock_http_client_get):
    mock_http_client_get.return_value.raise_for_status = MagicMock()
    mock_http_client_get.return_value.json.return_value = {'results': [], 'count': 0}

    processo_uuid = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    svc = EscolhasApiService(base_url='http://escolhas:8000', timeout_seconds=12)
    result = svc.buscar_escolhas_por_processo_uuid(processo_uuid)

    assert result == {'results': [], 'count': 0}
    mock_http_client_get.assert_called_once()
    call_args, call_kw = mock_http_client_get.call_args
    assert call_args[0] == 'http://escolhas:8000/api/v1/escolhas/'
    assert call_kw['params'] == {
        'vaga_escola__lote__processo_uuid': processo_uuid,
        'no_page': True,
        'fields': 'candidato_uuid',
    }
    assert call_kw['headers'] == svc._headers
    assert call_kw['timeout'] == 12
    mock_http_client_get.return_value.raise_for_status.assert_called_once()


@patch('agenda.services.escolhas_api_service.http_client.get')
def test_buscar_escolhas_por_processo_uuid_converte_uuid_para_str(mock_http_client_get):
    mock_http_client_get.return_value.raise_for_status = MagicMock()
    mock_http_client_get.return_value.json.return_value = {}

    u = uuid.uuid4()
    svc = EscolhasApiService(base_url='http://x.com')
    svc.buscar_escolhas_por_processo_uuid(u)

    assert mock_http_client_get.call_args[1]['params']['vaga_escola__lote__processo_uuid'] == str(u)


@patch('agenda.services.escolhas_api_service.http_client.get')
def test_buscar_escolhas_por_processo_uuid_raise_for_status_propaga(mock_http_client_get):
    mock_http_client_get.return_value.raise_for_status.side_effect = requests.HTTPError('404')

    svc = EscolhasApiService(base_url='http://x.com')
    with pytest.raises(requests.HTTPError):
        svc.buscar_escolhas_por_processo_uuid('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb')


@patch('agenda.services.escolhas_api_service.http_client.get')
def test_buscar_escolhas_por_processo_uuid_request_exception_propaga(mock_http_client_get):
    mock_http_client_get.side_effect = requests.RequestException('Connection refused')

    svc = EscolhasApiService(base_url='http://x.com')
    with pytest.raises(requests.RequestException):
        svc.buscar_escolhas_por_processo_uuid('cccccccc-cccc-cccc-cccc-cccccccccccc')
