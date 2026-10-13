"""Módulo serializers."""

from rest_framework import serializers

from agenda.models import MODALIDADE_CHOICES, Agenda
from core.serializers import PaginaSerializer

DESCRICOES_AGENDA = {
    "uuid": {"help_text": "Identificador da agenda."},
    "processo_convocacao_uuid": {
        "help_text": "UUID do processo de convocação."
    },
    "processo_convocacao_nome": {
        "help_text": "Nome do processo de convocação."
    },
    "cargo_uuid": {"help_text": "UUID do cargo."},
    "cargo_nome": {"help_text": "Nome do cargo."},
    "cargo_codigo": {
        "help_text": (
            "Código do cargo na SME, como texto. É por ele que a exclusão "
            "por processo e cargo localiza as agendas."
        )
    },
    "data_escolha": {
        "help_text": (
            "Data e hora de publicação da agenda. Assume o momento da "
            "criação quando não é enviada."
        )
    },
    "modalidade": {"help_text": "Modalidade da sessão de escolha."},
    "escolha_em": {"help_text": "Data da sessão de escolha."},
    "nomeacao_em": {"help_text": "Data da nomeação."},
    "classificacao": {
        "help_text": "Quantidade de candidatos previstos para a sessão."
    },
    "sessao": {"help_text": "Identificação da sessão, em texto livre."},
    "retardatario": {
        "help_text": "Indica se a sessão é a dos candidatos retardatários."
    },
    "hora_convocacao_inicio": {"help_text": "Hora de início da sessão."},
    "hora_convocacao_fim": {"help_text": "Hora de término da sessão."},
    "candidatos_uuids": {
        "help_text": (
            "UUIDs dos habilitados do MS-Candidatos convocados para a "
            "sessão, em ordem de ranking de escolha."
        )
    },
    "criado_em": {"help_text": "Data e hora de criação do registro."},
    "atualizado_em": {
        "help_text": "Data e hora da última alteração do registro."
    },
}


class AgendaItemCreateSerializer(serializers.Serializer):
    """Serializer para cada item da lista 'agendas' no payload de criação."""

    uuid = serializers.UUIDField(
        required=False,
        allow_null=True,
        help_text=(
            "UUID de uma agenda existente, para atualizá-la. Sem ele, ou "
            "se não há agenda com esse UUID, uma agenda nova é criada, "
            "com um UUID gerado pelo serviço."
        ),
    )
    cargo_uuid = serializers.UUIDField(
        required=True, help_text="UUID do cargo."
    )
    cargo_nome = serializers.CharField(
        max_length=200, required=True, help_text="Nome do cargo."
    )
    cargo_codigo = serializers.CharField(
        max_length=20,
        required=False,
        default="",
        allow_blank=True,
        help_text="Código do cargo na SME, como texto.",
    )
    data_escolha = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="Data e hora de publicação da agenda.",
    )
    modalidade = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Modalidade da sessão de escolha.",
    )
    escolha_em = serializers.DateField(
        required=False, allow_null=True, help_text="Data da sessão de escolha."
    )
    nomeacao_em = serializers.DateField(
        required=False, allow_null=True, help_text="Data da nomeação."
    )
    classificacao = serializers.IntegerField(
        required=True,
        help_text=(
            "Quantidade de candidatos da sessão: o tamanho da fatia da "
            "lista de candidatos que ela recebe."
        ),
    )
    sessao = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Identificação da sessão, em texto livre.",
    )
    retardatario = serializers.BooleanField(
        required=False,
        default=False,
        allow_null=True,
        help_text=(
            "Indica a sessão dos retardatários, que recebe os primeiros "
            "candidatos da lista em vez da fatia seguinte."
        ),
    )
    hora_convocacao_inicio = serializers.TimeField(
        required=False, allow_null=True, help_text="Hora de início da sessão."
    )
    hora_convocacao_fim = serializers.TimeField(
        required=False, allow_null=True, help_text="Hora de término da sessão."
    )


class CreateAgendasPayloadSerializer(serializers.Serializer):
    """Valida payload de criação em lote de agendas e candidatos."""

    agendas = serializers.ListField(
        child=AgendaItemCreateSerializer(),
        min_length=1,
        error_messages={
            "required": 'O campo "agendas" é obrigatório',
            "min_length": "Envie ao menos uma agenda",
        },
        help_text="Sessões a criar ou atualizar. Ao menos uma.",
    )
    candidatos_uuids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=True,
        default=list,
        error_messages={
            "required": 'O campo "candidatos_uuids" é obrigatório'
        },
        help_text=(
            "UUIDs dos habilitados do MS-Candidatos a distribuir entre as "
            "sessões. Sem o campo, ou com a lista vazia, as sessões ficam "
            "sem candidatos e o MS-Candidatos não é consultado."
        ),
    )
    processo_uuid = serializers.UUIDField(
        error_messages={
            "required": 'O campo "processo_uuid" é obrigatório',
            "invalid": "processo_uuid deve ser um UUID válido",
        },
        help_text=(
            "UUID do processo de convocação, gravado em todas as agendas "
            "do lote."
        ),
    )
    processo_nome = serializers.CharField(
        max_length=200,
        allow_blank=True,
        default="",
        error_messages={"required": 'O campo "processo_nome" é obrigatório'},
        help_text=(
            "Nome do processo de convocação, gravado em todas as agendas "
            "do lote."
        ),
    )


class AgendaListSerializer(serializers.ModelSerializer):
    """Agenda: a sessão de escolha de um cargo em um processo."""

    class Meta:
        """Configuração do serializer."""

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
        extra_kwargs = DESCRICOES_AGENDA


class AgendaCreateSerializer(serializers.ModelSerializer):
    """Dados de uma agenda, como gravados e devolvidos na alteração."""

    class Meta:
        """Configuração do serializer."""

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
        extra_kwargs = DESCRICOES_AGENDA


class AgendaPaginadaSerializer(PaginaSerializer):
    """Página da listagem de agendas."""

    results = AgendaListSerializer(many=True, help_text="Agendas da página.")
    candidatos_uuids_restantes = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        help_text=(
            "Candidatos da primeira agenda da página que ainda não têm "
            "escolha em vaga do processo, segundo o MS-Escolhas. Presente "
            "só quando essa agenda é ONLINE e o MS-Escolhas respondeu."
        ),
    )


class AgendaItemRequisicaoSerializer(AgendaItemCreateSerializer):
    """Sessão de escolha de um cargo, como enviada no lote."""

    cargo_codigo = serializers.CharField(
        max_length=20,
        help_text=(
            "Código do cargo na SME, como texto. Vazio ou ausente resulta "
            "em erro 400."
        ),
    )
    data_escolha = serializers.DateTimeField(
        required=False,
        help_text=(
            "Data e hora de publicação da agenda. Se omitida, vale o "
            "momento da criação ou, na atualização, o valor já gravado. "
            "Nulo resulta em erro 400."
        ),
    )
    modalidade = serializers.ChoiceField(  # type: ignore[assignment]
        choices=MODALIDADE_CHOICES,
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text=(
            "Modalidade da sessão de escolha, em maiúsculas. Outro valor "
            "resulta em erro 400."
        ),
    )


class AgendasLoteRequisicaoSerializer(CreateAgendasPayloadSerializer):
    """Sessões de um processo de convocação e os candidatos a distribuir."""

    agendas = AgendaItemRequisicaoSerializer(  # type: ignore[assignment]
        many=True,
        allow_empty=False,
        help_text="Sessões a criar ou atualizar. Ao menos uma.",
    )
    processo_nome = serializers.CharField(
        max_length=200,
        help_text=(
            "Nome do processo de convocação, gravado em todas as agendas "
            "do lote. Vazio ou ausente resulta em erro 400, com a chave "
            "`processo_convocacao_nome`."
        ),
    )


class AgendasGravadasSerializer(serializers.Serializer):
    """Agendas criadas e atualizadas pelo envio, com as criadas primeiro."""


class AgendasExcluidasSerializer(serializers.Serializer):
    """Resultado de uma exclusão de agendas em lote."""

    excluidas = serializers.IntegerField(
        help_text="Quantidade de agendas excluídas."
    )
