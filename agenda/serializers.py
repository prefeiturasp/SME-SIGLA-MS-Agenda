from rest_framework import serializers
from .models import Agenda


class AgendaListSerializer(serializers.ModelSerializer):
    """Serializer para listagem de agendas (list e retrieve)."""
    
    class Meta:
        model = Agenda
        fields = [
            'uuid',
            'processo_convocacao_uuid', 'processo_convocacao_nome',
            'cargo_uuid', 'cargo_nome', 'cargo_codigo',
            'data_escolha',
            'modalidade',
            'escolha_em',
            'nomeacao_em',
            'classificacao',
            'sessao',
            'retardatario',
            'hora_convocacao_inicio',
            'hora_convocacao_fim',
            'candidatos_uuids',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['uuid', 'criado_em', 'atualizado_em']


class AgendaCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação e atualização de agendas."""
    
    class Meta:
        model = Agenda
        fields = [
            'uuid',
            'processo_convocacao_uuid', 'processo_convocacao_nome',
            'cargo_uuid', 'cargo_nome', 'cargo_codigo',
            'data_escolha',
            'modalidade',
            'escolha_em',
            'nomeacao_em',
            'classificacao',
            'sessao',
            'retardatario',
            'hora_convocacao_inicio',
            'hora_convocacao_fim',
            'candidatos_uuids',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']
