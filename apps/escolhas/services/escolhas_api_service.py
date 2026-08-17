"""Serviço para integração com a API de escolhas."""

from __future__ import annotations

import logging
from typing import Any

from sigla_sdk.http.api_client import http_client

from integracao.base import BaseApiService

logger = logging.getLogger(__name__)


class EscolhasApiService(BaseApiService):
    """Serviço para chamar o endpoint de escolhas."""

    def buscar_escolhas_por_processo_uuid(
        self, vaga_escola__lote__processo_uuid: str
    ) -> dict[str, Any]:
        """Busca escolhas por processo uuid.

        Args:
            vaga_escola__lote__processo_uuid: UUID do processo na vaga.

        Returns:
            Dicionário com os dados processados.
        """
        url = f"{self.base_url}/api/v1/escolhas/"
        params = {
            "vaga_escola__lote__processo_uuid": str(
                vaga_escola__lote__processo_uuid
            ),
            "no_page": True,
            "fields": "candidato_uuid",
        }
        response = http_client.get(
            url,
            params=params,
            headers=self._headers,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        logger.info(
            "Escolhas buscadas por vaga_escola__lote__processo_uuid=%s",
            vaga_escola__lote__processo_uuid,
        )
        return data  # type: ignore[no-any-return]
