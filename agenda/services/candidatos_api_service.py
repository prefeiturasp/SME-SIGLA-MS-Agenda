"""Serviço para integração com a API de candidatos (buscar habilitados por UUIDs)."""
from __future__ import annotations
import logging
from typing import Any
import requests
from requests import RequestException
from sigla_sdk.context import get_correlation_id
from sigla_sdk.http.api_client import http_client
logger = logging.getLogger(__name__)

class CandidatosApiService:
    """Serviço para chamar o endpoint de candidatos buscar-por-uuids."""

    def __init__(self, base_url: str, timeout_seconds: int=30) -> None:
        """Executa   init  .
        
        Args:
            self: Instância do objeto.
            base_url: Parâmetro base url da operação.
            timeout_seconds: Parâmetro timeout seconds da operação.
        
        Raises:
            Nenhuma exceção específica documentada.
        """
        self.base_url = base_url.rstrip('/')
        self.timeout_seconds = timeout_seconds
        self._headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def buscar_por_uuids_ordenado_por_ranking_escolha(self, uuids: list[str], fields: str='uuid,ranking_escolha') -> list[dict[str, Any]]:
        """POST para /api/v1/habilitados/buscar-por-uuids/ com.
        
        Args:
            self: Instância do objeto.
            uuids: Lista de UUIDs dos candidatos.
            fields: Query string de campos (padrão: uuid,ranking_escolha).
        
        Returns:
            Lista com os registros resultantes.
        
        Raises:
            Nenhuma exceção específica documentada.
        """
        if not uuids:
            return []
        url = f'{self.base_url}/api/v1/habilitados/buscar-por-uuids/'
        params = {'fields': fields, 'order_by': 'ranking_escolha'}
        payload = {'uuids': [str(u) for u in uuids]}
        logger.info('Buscando candidatos por UUIDs', extra={'correlation_id': get_correlation_id(), 'method': 'POST', 'url': url, 'params': params, 'payload': payload, 'fields': fields, 'headers': self._headers})
        try:
            response = http_client.post(url, params=params, json=payload, headers=self._headers, timeout=self.timeout_seconds)
            response.raise_for_status()
        except RequestException:
            logger.error('Erro ao buscar candidatos por UUIDs', extra={'correlation_id': get_correlation_id(), 'method': 'POST', 'url': url})
            raise
        data = response.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        if not isinstance(results, list):
            results = []

        def _key(item: Any) -> Any:
            """Executa  key.
            
            Args:
                item: Parâmetro item da operação.
            
            Returns:
                Resultado da operação.
            
            Raises:
                Nenhuma exceção específica documentada.
            """
            r = item.get('ranking_escolha')
            if r is None:
                return float('inf')
            try:
                return int(r)
            except (TypeError, ValueError):
                return float('inf')
        results = sorted(results, key=_key)
        logger.info('Candidatos buscados por UUIDs (total=%d, ordenado por ranking_escolha asc)', len(results))
        return results  # type: ignore[no-any-return]
