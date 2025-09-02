"""
DRF views for the agenda module.
"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import timedelta

from .models import Agenda
from .serializers import (
    AgendaSerializer,
)
from .utils import CustomPagination


class AgendaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar agendas de convocação.
    """
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['processo_convocacao_uuid', 'cargo_uuid']
    search_fields = ['processo_convocacao_nome', 'cargo_nome']
    ordering_fields = ['data_escolha', 'criado_em']
    ordering = ['-data_escolha']
    pagination_class = CustomPagination
