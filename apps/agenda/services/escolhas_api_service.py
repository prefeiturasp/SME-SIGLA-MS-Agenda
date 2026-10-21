"""Serviço para integração com a API de escolhas."""

from __future__ import annotations

import logging
from typing import Any

from django.conf import settings
from requests import RequestException
from sigla_sdk.http.api_client import http_client

from agenda.services.http_log import mascarar_headers

logger = logging.getLogger(__name__)


class EscolhasApiService:
    """Serviço para chamar o endpoint de escolhas."""

    def __init__(self, base_url: str = "", timeout_seconds: int = 0) -> None:
        """Inicializa a instância com os parâmetros informados.

        Args:
            base_url: URL base do serviço remoto.
            timeout_seconds: Tempo máximo de espera, em segundos.
        """
        self.base_url = base_url.rstrip("/") or settings.ESCOLHAS_API_URL
        self.timeout_seconds = timeout_seconds or settings.ESCOLHAS_API_TIMEOUT
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            settings.API_KEY_HEADER: settings.ESCOLHAS_API_KEY,
        }

    def buscar_escolhas_por_processo_uuid(
        self, vaga_escola__lote__processo_uuid: str
    ) -> dict[str, Any]:
        """Busca escolhas por processo uuid.

        Args:
            vaga_escola__lote__processo_uuid: UUID do processo na vaga.

        Returns:
            Dicionário com os dados processados.

        Raises:
            RequestException: Em caso de erro na requisição.
        """
        url = f"{self.base_url}/api/v1/escolhas/"
        params = {
            "vaga_escola__lote__processo_uuid": str(
                vaga_escola__lote__processo_uuid
            ),
            "no_page": True,
            "fields": "candidato_uuid",
        }
        logger.info(
            f"Buscando escolhas por processo uuid | method=GET url={url} "
            f"params={params} "
            f"headers={mascarar_headers(self._headers)} "
            f"timeout_seconds={self.timeout_seconds}"
        )
        try:
            response = http_client.get(
                url,
                params=params,
                headers=self._headers,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except RequestException as exc:
            logger.error(
                f"Erro ao buscar escolhas | method=GET url={url} "
                f"error={exc} "
            )
            raise
        data = response.json()
        logger.info(
            f"Escolhas buscadas | "
            f"vaga_escola__lote__processo_uuid="
            f"{vaga_escola__lote__processo_uuid}"
        )
        return data  # type: ignore[no-any-return]
