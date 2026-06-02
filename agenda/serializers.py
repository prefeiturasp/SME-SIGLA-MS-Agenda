from rest_framework import serializers

from agenda.models import Agenda


class AgendaItemCreateSerializer(serializers.Serializer):
    """
    Serializer para cada item da lista 'agendas' no payload de criação.
    processo_convocacao_uuid e processo_convocacao_nome vêm do root
    (processo_uuid, processo_nome).
    """

    uuid = serializers.UUIDField(required=False, allow_null=True)
    cargo_uuid = serializers.UUIDField(required=True)
    cargo_nome = serializers.CharField(max_length=200, required=True)
    cargo_codigo = serializers.CharField(
        max_length=20, required=False, default="", allow_blank=True
    )
    data_escolha = serializers.DateTimeField(required=False, allow_null=True)
    modalidade = serializers.CharField(
        max_length=20, required=False, allow_blank=True, allow_null=True
    )
    escolha_em = serializers.DateField(required=False, allow_null=True)
    nomeacao_em = serializers.DateField(required=False, allow_null=True)
    classificacao = serializers.IntegerField(
        required=True
    )  # quantidade de candidatos desta agenda
    sessao = serializers.CharField(
        max_length=200, required=False, allow_blank=True, allow_null=True
    )
    retardatario = serializers.BooleanField(
        required=False, default=False, allow_null=True
    )
    hora_convocacao_inicio = serializers.TimeField(
        required=False, allow_null=True
    )
    hora_convocacao_fim = serializers.TimeField(
        required=False, allow_null=True
    )


class CreateAgendasPayloadSerializer(serializers.Serializer):
    """
    Valida o payload do create: agendas, candidatos_uuids,
    processo_uuid, processo_nome.
    """

    agendas = serializers.ListField(
        child=AgendaItemCreateSerializer(),
        min_length=1,
        error_messages={
            "required": 'O campo "agendas" é obrigatório',
            "min_length": "Envie ao menos uma agenda",
        },
    )
    candidatos_uuids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=True,
        default=list,
        error_messages={
            "required": 'O campo "candidatos_uuids" é obrigatório'
        },
    )
    processo_uuid = serializers.UUIDField(
        error_messages={
            "required": 'O campo "processo_uuid" é obrigatório',
            "invalid": "processo_uuid deve ser um UUID válido",
        }
    )
    processo_nome = serializers.CharField(
        max_length=200,
        allow_blank=True,
        default="",
        error_messages={"required": 'O campo "processo_nome" é obrigatório'},
    )


class AgendaListSerializer(serializers.ModelSerializer):
    """Serializer para listagem de agendas (list e retrieve)."""

    class Meta:
        model = Agenda
        fields = [
            "uuid",
            "processo_convocacao_uuid",
            "processo_convocacao_nome",
            "cargo_uuid",
            "cargo_nome",
            "cargo_codigo",
            "data_escolha",
            "modalidade",
            "escolha_em",
            "nomeacao_em",
            "classificacao",
            "sessao",
            "retardatario",
            "hora_convocacao_inicio",
            "hora_convocacao_fim",
            "candidatos_uuids",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["uuid", "criado_em", "atualizado_em"]


class AgendaCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação e atualização de agendas."""

    class Meta:
        model = Agenda
        fields = [
            "uuid",
            "processo_convocacao_uuid",
            "processo_convocacao_nome",
            "cargo_uuid",
            "cargo_nome",
            "cargo_codigo",
            "data_escolha",
            "modalidade",
            "escolha_em",
            "nomeacao_em",
            "classificacao",
            "sessao",
            "retardatario",
            "hora_convocacao_inicio",
            "hora_convocacao_fim",
            "candidatos_uuids",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["criado_em", "atualizado_em"]
