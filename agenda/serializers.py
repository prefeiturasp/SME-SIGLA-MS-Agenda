from rest_framework import serializers
from .models import Agenda


class AgendaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Agenda."""
    
    class Meta:
        model = Agenda
        fields = [
            'uuid',
            'processo_convocacao_uuid', 'processo_convocacao_nome',
            'cargo_uuid', 'cargo_nome',
            'data_escolha',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['uuid', 'criado_em', 'atualizado_em']
