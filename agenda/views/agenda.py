"""DRF views for the agenda module."""

from __future__ import annotations

import logging
from typing import Any

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from requests import RequestException
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from sigla_sdk.context import get_correlation_id

from agenda.filters import AgendaOrderingFilter
from agenda.models import Agenda
from agenda.serializers import (
    AgendaCreateSerializer,
    AgendaListSerializer,
    CreateAgendasPayloadSerializer,
)
from agenda.services.candidatos_api_service import CandidatosApiService
from agenda.services.escolhas_api_service import EscolhasApiService
from agenda.utils import CustomPagination

logger = logging.getLogger(__name__)


class AgendaViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar agendas de convocação."""

    queryset = Agenda.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, AgendaOrderingFilter]
    filterset_fields = ["processo_convocacao_uuid", "cargo_uuid"]
    search_fields = ["processo_convocacao_nome", "cargo_nome"]
    ordering_fields = ["data_escolha", "hora_convocacao_inicio", "criado_em"]
    ordering = ["escolha_em", "hora_convocacao_inicio"]
    pagination_class = CustomPagination

    def get_serializer_class(self) -> Any:
        """Retorna serializer class."""
        if self.action in ["list", "retrieve"]:
            return AgendaListSerializer
        return AgendaCreateSerializer

    def list(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        """Listar as agendas."""
        logger.info(
            "Listando agendas",
            extra={
                "correlation_id": get_correlation_id(),
                "method": request.method,
                "path": request.path,
                "params": request.query_params,
                "user": request.user,
            },
        )
        response = super().list(request, *args, **kwargs)
        results = response.data.get("results", [])
        if (
            results
            and (results[0].get("modalidade") or "").upper() == "ONLINE"
        ):
            primeira_agenda = results[0]
            processo_uuid = primeira_agenda.get("processo_convocacao_uuid")
            candidatos_uuids_agenda = (
                primeira_agenda.get("candidatos_uuids") or []
            )
            escolhas_service = EscolhasApiService(
                base_url=settings.ESCOLHAS_API_URL
            )
            try:
                escolhas_data = (
                    escolhas_service.buscar_escolhas_por_processo_uuid(
                        str(processo_uuid)
                    )
                )
            except RequestException as exc:
                logger.warning(
                    "Erro ao buscar escolhas por processo_uuid=%s: %s",
                    processo_uuid,
                    exc,
                )
            else:
                escolhas_lista = (
                    escolhas_data
                    if isinstance(escolhas_data, list)
                    else escolhas_data.get("results", escolhas_data) or []
                )
                escolhas_candidato_uuids = {
                    str(item.get("candidato_uuid"))
                    for item in escolhas_lista
                    if item.get("candidato_uuid") is not None
                }
                candidatos_uuids_restantes = [
                    str(cand_uuid)
                    for cand_uuid in candidatos_uuids_agenda
                    if str(cand_uuid) not in escolhas_candidato_uuids
                ]
                response.data["candidatos_uuids_restantes"] = (
                    candidatos_uuids_restantes
                )
        return response

    def create(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        """Cria ou atualiza várias agendas a partir do payload."""
        logger.info(
            "Criando agendas",
            extra={
                "correlation_id": get_correlation_id(),
                "method": request.method,
                "path": request.path,
                "processo_uuid": request.data.get("processo_uuid"),
                "processo_nome": request.data.get("processo_nome"),
                "candidatos_uuids": len(
                    request.data.get("candidatos_uuids", [])
                ),
                "agendas": len(request.data.get("agendas", [])),
                "user": request.user,
            },
        )
        payload_serializer = CreateAgendasPayloadSerializer(data=request.data)
        payload_serializer.is_valid(raise_exception=True)
        data = payload_serializer.validated_data
        agendas_data = data["agendas"]
        candidatos_uuids = data["candidatos_uuids"]
        processo_uuid = data["processo_uuid"]
        processo_nome = data.get("processo_nome") or ""
        ordered_candidatos_uuids = []
        if candidatos_uuids:
            try:
                candidatos_service = CandidatosApiService(
                    base_url=settings.CANDIDATOS_API_URL
                )
                results = (
                    candidatos_service.buscar_por_uuids_ordenado_por_ranking_escolha
                )(
                    uuids=candidatos_uuids,
                    fields="uuid,ranking_escolha",
                )
                ordered_candidatos_uuids = [
                    str(c["uuid"])
                    for c in results
                    if c.get("uuid") is not None
                ]
            except RequestException as exc:
                logger.exception(
                    "Erro ao buscar candidatos por UUIDs: %s", exc
                )
                return Response(
                    {"detail": "Erro ao consultar API de candidatos."},
                    status=status.HTTP_502_BAD_GATEWAY,
                )
        cursor = 0
        agendas_criadas = []
        agendas_atualizadas = []
        for item in agendas_data:
            if not item.get("retardatario"):
                qty = item.get("classificacao") or 0
                slice_uuids = ordered_candidatos_uuids[cursor : cursor + qty]
                cursor += qty
            else:
                slice_uuids = ordered_candidatos_uuids[
                    : item.get("classificacao")
                ]
            agenda_item = dict(item)
            agenda_item["processo_convocacao_uuid"] = processo_uuid
            agenda_item["processo_convocacao_nome"] = processo_nome
            agenda_item["candidatos_uuids"] = slice_uuids
            uuid_provido = agenda_item.get("uuid")
            if uuid_provido:
                try:
                    agenda_existente = Agenda.objects.get(uuid=uuid_provido)
                    serializer = AgendaCreateSerializer(
                        agenda_existente, data=agenda_item, partial=False
                    )
                    serializer.is_valid(raise_exception=True)
                    agenda_atualizada = serializer.save()
                    agendas_atualizadas.append(agenda_atualizada)
                except Agenda.DoesNotExist:
                    serializer = AgendaCreateSerializer(data=agenda_item)
                    serializer.is_valid(raise_exception=True)
                    agenda_nova = serializer.save()
                    agendas_criadas.append(agenda_nova)
            else:
                serializer = AgendaCreateSerializer(data=agenda_item)
                serializer.is_valid(raise_exception=True)
                agenda_nova = serializer.save()
                agendas_criadas.append(agenda_nova)
        todas_agendas = agendas_criadas + agendas_atualizadas
        response_serializer = AgendaListSerializer(todas_agendas, many=True)
        status_code = (
            status.HTTP_201_CREATED if agendas_criadas else status.HTTP_200_OK
        )
        logger.info(
            "Agendas criadas",
            extra={
                "correlation_id": get_correlation_id(),
                "method": request.method,
                "path": request.path,
                "processo_uuid": processo_uuid,
                "processo_nome": processo_nome,
                "agendas_criadas": len(agendas_criadas),
                "agendas_atualizadas": len(agendas_atualizadas),
                "todas_agendas": len(todas_agendas),
                "status_code": status_code,
            },
        )
        return Response(response_serializer.data, status=status_code)

    @action(detail=False, methods=["delete"], url_path="por-processo")
    def excluir_por_processo(self, request: Any) -> Any:
        """Remove todas as agendas vinculadas ao processo de convocação."""
        processo_uuid = request.query_params.get("processo_uuid")
        if not processo_uuid:
            return Response(
                {"detail": "processo_uuid é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        deleted, _ = Agenda.objects.filter(
            processo_convocacao_uuid=processo_uuid
        ).delete()
        logger.info(
            "Agendas excluídas por processo",
            extra={
                "correlation_id": get_correlation_id(),
                "processo_uuid": processo_uuid,
                "excluidas": deleted,
            },
        )
        return Response({"excluidas": deleted}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="por-processo-e-cargo")
    def excluir_por_processo_e_cargo(self, request: Any) -> Any:
        """Remove agendas vinculadas ao processo de convocação e ao cargo."""
        processo_uuid = request.query_params.get("processo_uuid")
        if not processo_uuid:
            return Response(
                {"detail": "processo_uuid é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cargo_codigo = request.query_params.get("cargo")
        if not cargo_codigo:
            return Response(
                {"detail": "cargo é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted, _ = Agenda.objects.filter(
            processo_convocacao_uuid=processo_uuid, cargo_codigo=cargo_codigo
        ).delete()
        logger.info(
            "Agendas excluídas por processo e cargo",
            extra={
                "correlation_id": get_correlation_id(),
                "processo_uuid": processo_uuid,
                "cargo_codigo": cargo_codigo,
                "excluidas": deleted,
            },
        )
        return Response({"excluidas": deleted}, status=status.HTTP_200_OK)
