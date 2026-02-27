"""
DRF views for the agenda module.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import timedelta

from agenda.models import Agenda
from agenda.serializers import (
    AgendaListSerializer,
    AgendaCreateSerializer,
)
from agenda.utils import CustomPagination


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
        Cria ou atualiza uma ou várias agendas.
        Aceita uma lista de dicionários com os campos da agenda.
        Se o UUID for fornecido e existir, atualiza a agenda existente.
        Caso contrário, cria uma nova agenda.
        """
        data = request.data
        
        if not isinstance(data, list):
            data = [data]
        
        agendas_criadas = []
        agendas_atualizadas = []
        
        for item in data:
            uuid_provido = item.get('uuid')
            
            if uuid_provido:
                try:
                    agenda_existente = Agenda.objects.get(uuid=uuid_provido)
                    serializer = AgendaCreateSerializer(agenda_existente, data=item, partial=False)
                    serializer.is_valid(raise_exception=True)
                    agenda_atualizada = serializer.save()
                    agendas_atualizadas.append(agenda_atualizada)
                except Agenda.DoesNotExist:
                    serializer = AgendaCreateSerializer(data=item)
                    serializer.is_valid(raise_exception=True)
                    agenda_nova = serializer.save()
                    agendas_criadas.append(agenda_nova)
            else:
                serializer = AgendaCreateSerializer(data=item)
                serializer.is_valid(raise_exception=True)
                agenda_nova = serializer.save()
                agendas_criadas.append(agenda_nova)
        
        todas_agendas = agendas_criadas + agendas_atualizadas
        
        response_serializer = AgendaListSerializer(todas_agendas, many=True)
        status_code = status.HTTP_201_CREATED if agendas_criadas else status.HTTP_200_OK
        return Response(response_serializer.data, status=status_code)
