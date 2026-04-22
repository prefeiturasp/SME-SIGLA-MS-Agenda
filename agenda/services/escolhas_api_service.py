"""
Serviço para integração com a API de escolhas.
"""
import logging
from typing import Any, Dict, List

from sigla_sdk.http.api_client import http_client

logger = logging.getLogger(__name__)


class EscolhasApiService:
    """
    Serviço para chamar o endpoint de escolhas.
    """

    def __init__(self, base_url: str, timeout_seconds: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout_seconds = timeout_seconds
        self._headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def buscar_escolhas_por_processo_uuid(self, vaga_escola__lote__processo_uuid: str) -> Dict[str, Any]:
        """
        GET para /api/v1/escolhas/?vaga_escola__lote__processo_uuid=<uuid>
        Retorna a resposta da API de escolhas filtrada por processo.

        Args:
            processo_uuid: UUID do processo de convocação.

        Returns:
            Dicionário com a resposta da API (results, count, etc.).

        Raises:
            Exception: Em caso de erro na requisição.
        """
        url = f"{self.base_url}/api/v1/escolhas/"
        params = {
            'vaga_escola__lote__processo_uuid': str(vaga_escola__lote__processo_uuid),
            'no_page': True,
            'fields': 'candidato_uuid',
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
            'Escolhas buscadas por vaga_escola__lote__processo_uuid=%s',
            vaga_escola__lote__processo_uuid,
        )
        return data
