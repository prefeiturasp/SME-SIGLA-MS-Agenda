"""
Serviço para integração com a API de candidatos (buscar habilitados por UUIDs).
"""

import logging
from typing import Any

import requests  # noqa: F401  (necessário para mock.patch nos testes)
from requests import RequestException
from sigla_sdk.context import get_correlation_id
from sigla_sdk.http.api_client import http_client

logger = logging.getLogger(__name__)


class CandidatosApiService:
    """
    Serviço para chamar o endpoint de candidatos buscar-por-uuids.
    """

    def __init__(self, base_url: str, timeout_seconds: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def buscar_por_uuids_ordenado_por_ranking_escolha(
        self,
        uuids: list[str],
        fields: str = "uuid,ranking_escolha",
    ) -> list[dict[str, Any]]:
        """
        POST para /api/v1/habilitados/buscar-por-uuids/ com
        fields=uuid,ranking_escolha e order_by=ranking_escolha.
        Retorna a lista de candidatos ordenada por ranking_escolha
        de forma ascendente.

        Args:
            uuids: Lista de UUIDs dos candidatos.
            fields: Query string de campos (padrão: uuid,ranking_escolha).

        Returns:
            Lista de dicionários com os campos retornados pela API, ordenada
            por ranking_escolha ascendente.

        Raises:
            RequestException: Em caso de erro na requisição.
        """
        if not uuids:
            return []

        url = f"{self.base_url}/api/v1/habilitados/buscar-por-uuids/"
        params = {
            "fields": fields,
            "order_by": "ranking_escolha",
        }
        payload = {"uuids": [str(u) for u in uuids]}

        logger.info(
            "Buscando candidatos por UUIDs",
            extra={
                "correlation_id": get_correlation_id(),
                "method": "POST",
                "url": url,
                "params": params,
                "payload": payload,
                "fields": fields,
                "headers": self._headers,
            },
        )
        try:
            response = http_client.post(
                url,
                params=params,
                json=payload,
                headers=self._headers,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except RequestException:
            logger.error(
                "Erro ao buscar candidatos por UUIDs",
                extra={
                    "correlation_id": get_correlation_id(),
                    "method": "POST",
                    "url": url,
                },
            )
            raise

        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        if not isinstance(results, list):
            results = []

        # Ordenar por ranking_escolha ascendente
        # (garantir ordem mesmo se a API não ordenar)
        def _key(item):
            r = item.get("ranking_escolha")
            if r is None:
                return float("inf")
            try:
                return int(r)
            except (TypeError, ValueError):
                return float("inf")

        results = sorted(results, key=_key)
        logger.info(
            "Candidatos buscados por UUIDs "
            "(total=%d, ordenado por ranking_escolha asc)",
            len(results),
        )
        return results
