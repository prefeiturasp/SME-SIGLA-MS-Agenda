"""
DRF views for the agenda module.
"""
import logging

from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from requests import RequestException

from agenda.models import Agenda
from agenda.serializers import (
    AgendaListSerializer,
    AgendaCreateSerializer,
    CreateAgendasPayloadSerializer,
)
from agenda.utils import CustomPagination
from agenda.services.candidatos_api_service import CandidatosApiService

logger = logging.getLogger(__name__)


class AgendaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar agendas de convocação.
    """
    queryset = Agenda.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['processo_convocacao_uuid', 'cargo_uuid']
    search_fields = ['processo_convocacao_nome', 'cargo_nome']
    ordering_fields = ['data_escolha', 'hora_convocacao_inicio', 'criado_em']
    ordering = ['escolha_em', 'hora_convocacao_inicio']
    pagination_class = CustomPagination
    
    def get_serializer_class(self):
        """
        Retorna o serializer apropriado baseado na ação.
        - AgendaListSerializer para listagem (list) e detalhes (retrieve)
        - AgendaCreateSerializer para criação (create), atualização (update) e atualização parcial (partial_update)
        """
        if self.action in ['list', 'retrieve']:
            return AgendaListSerializer
        return AgendaCreateSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Cria ou atualiza várias agendas a partir do payload com estrutura:
        - agendas: lista de objetos agenda (cada um com classificacao = quantidade de candidatos)
        - candidatos_uuids: lista de UUIDs de candidatos
        - processo_uuid: UUID do processo
        - processo_nome: nome do processo

        Os candidatos são buscados na API de candidatos (buscar-por-uuids), ordenados
        por ranking_escolha ascendente; cada agenda recebe um fatia da lista conforme
        o campo classificacao.
        """
        payload_serializer = CreateAgendasPayloadSerializer(data=request.data)
        payload_serializer.is_valid(raise_exception=True)
        data = payload_serializer.validated_data

        agendas_data = data['agendas']
        candidatos_uuids = data['candidatos_uuids']
        processo_uuid = data['processo_uuid']
        processo_nome = data.get('processo_nome') or ''

        # Buscar candidatos ordenados por ranking_escolha (asc) na API de candidatos
        ordered_candidatos_uuids = []
        if candidatos_uuids:
            try:
                candidatos_service = CandidatosApiService(
                    base_url=settings.CANDIDATOS_API_URL,
                )
                results = candidatos_service.buscar_por_uuids_ordenado_por_ranking_escolha(
                    uuids=candidatos_uuids,
                    fields='uuid,ranking_escolha',
                )
                ordered_candidatos_uuids = [
                    str(c['uuid']) for c in results
                    if c.get('uuid') is not None
                ]
            except RequestException as exc:
                logger.exception('Erro ao buscar candidatos por UUIDs: %s', exc)
                return Response(
                    {'detail': 'Erro ao consultar API de candidatos.'},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

        # Fatiar a lista ordenada de UUIDs conforme classificacao de cada agenda
        cursor = 0
        agendas_criadas = []
        agendas_atualizadas = []

        for item in agendas_data:
            qty = item.get('classificacao') or 0
            slice_uuids = ordered_candidatos_uuids[cursor:cursor + qty]
            cursor += qty

            # Montar dados da agenda com processo e candidatos fatiados
            agenda_item = dict(item)
            agenda_item['processo_convocacao_uuid'] = processo_uuid
            agenda_item['processo_convocacao_nome'] = processo_nome
            agenda_item['candidatos_uuids'] = slice_uuids

            uuid_provido = agenda_item.get('uuid')

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
        status_code = status.HTTP_201_CREATED if agendas_criadas else status.HTTP_200_OK
        return Response(response_serializer.data, status=status_code)
