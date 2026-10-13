"""Documentação OpenAPI das operações de agendas."""

from __future__ import annotations

from typing import Any

from drf_spectacular.extensions import OpenApiSerializerExtension
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import Direction, OpenApiParameter, extend_schema

from agenda.models import Agenda
from agenda.serializers import (
    AgendaCreateSerializer,
    AgendaListSerializer,
    AgendaPaginadaSerializer,
    AgendasExcluidasSerializer,
    AgendasGravadasSerializer,
    AgendasLoteRequisicaoSerializer,
)
from core.openapi import (
    AVISO_ROTA_HERDADA,
    PARAMETRO_PAGINA,
    PARAMETRO_TAMANHO_PAGINA,
    RESPOSTA_PAGINA_INEXISTENTE,
    erro_interno,
    exemplo_pagina,
    exemplos_requisicao,
    parametro_busca,
    parametro_uuid,
    resposta,
    resposta_nao_encontrado,
    respostas,
)
from core.serializers import ErroDetalheSerializer, ErrosValidacaoSerializer

TAG_AGENDAS = "Agendas"

UUID_AGENDA_EXEMPLO = "3f6a1c2e-9b4d-4e7a-8c15-2d0b7a6e9f31"
UUID_AGENDA_2_EXEMPLO = "b2d4f6a8-1c3e-4a5b-9d7f-0e8c6a4b2d10"
UUID_AGENDA_ONLINE_EXEMPLO = "7c9e1a3b-5d2f-4b6a-8e0c-4a2f6b8d0c53"
UUID_PROCESSO_EXEMPLO = "c1a7e0d2-4b3f-4a6e-8d9c-0f1e2d3c4b5a"
NOME_PROCESSO_EXEMPLO = "1ª convocação — Professor de Educação Infantil"
UUID_CARGO_EXEMPLO = "9b2f6c1e-3a4d-4e8f-b7a1-6c5d4e3f2a10"
NOME_CARGO_EXEMPLO = "Professor de Educação Infantil"
CODIGO_CARGO_EXEMPLO = "3859"
UUID_CANDIDATO_1_EXEMPLO = "4f0c2b9e-6a1d-4c7b-9e35-2d8a1b7c6f04"
UUID_CANDIDATO_2_EXEMPLO = "a3d5e7f9-1b2c-4d6e-8f0a-9b8c7d6e5f41"
UUID_CANDIDATO_3_EXEMPLO = "0d9e8f7a-6b5c-4d3e-a2f1-b0c9d8e7f6a5"

AVISO_PROCESSO_MALFORMADO = (
    "Um valor que não seja UUID não é validado e resulta em erro 500."
)

AVISO_SEM_REDISTRIBUICAO = (
    "`candidatos_uuids` é gravado como enviado: esta rota não consulta o "
    "MS-Candidatos nem refaz a distribuição dos candidatos."
)

EXEMPLO_AGENDA = {
    "uuid": UUID_AGENDA_EXEMPLO,
    "processo_convocacao_uuid": UUID_PROCESSO_EXEMPLO,
    "processo_convocacao_nome": NOME_PROCESSO_EXEMPLO,
    "cargo_uuid": UUID_CARGO_EXEMPLO,
    "cargo_nome": NOME_CARGO_EXEMPLO,
    "cargo_codigo": CODIGO_CARGO_EXEMPLO,
    "data_escolha": "2026-03-02T10:00:00-03:00",
    "modalidade": "PRESENCIAL",
    "escolha_em": "2026-03-10",
    "nomeacao_em": "2026-03-20",
    "classificacao": 2,
    "sessao": "1ª sessão",
    "retardatario": False,
    "hora_convocacao_inicio": "09:00:00",
    "hora_convocacao_fim": "10:00:00",
    "candidatos_uuids": [UUID_CANDIDATO_1_EXEMPLO, UUID_CANDIDATO_2_EXEMPLO],
    "criado_em": "2026-03-02T10:00:00-03:00",
    "atualizado_em": "2026-03-02T10:00:00-03:00",
}

EXEMPLO_AGENDA_2 = {
    **EXEMPLO_AGENDA,
    "uuid": UUID_AGENDA_2_EXEMPLO,
    "classificacao": 1,
    "sessao": "2ª sessão",
    "hora_convocacao_inicio": "10:00:00",
    "hora_convocacao_fim": "11:00:00",
    "candidatos_uuids": [UUID_CANDIDATO_3_EXEMPLO],
}

EXEMPLO_AGENDA_ONLINE = {
    **EXEMPLO_AGENDA,
    "uuid": UUID_AGENDA_ONLINE_EXEMPLO,
    "modalidade": "ONLINE",
    "sessao": "Retardatários",
    "retardatario": True,
    "hora_convocacao_inicio": "14:00:00",
    "hora_convocacao_fim": "15:00:00",
}

EXEMPLO_AGENDA_ALTERADA = {
    **EXEMPLO_AGENDA,
    "sessao": "1ª sessão (remarcada)",
    "atualizado_em": "2026-03-05T14:30:00-03:00",
}

EXEMPLO_ITEM = {
    "cargo_uuid": UUID_CARGO_EXEMPLO,
    "cargo_nome": NOME_CARGO_EXEMPLO,
    "cargo_codigo": CODIGO_CARGO_EXEMPLO,
    "modalidade": "PRESENCIAL",
    "escolha_em": "2026-03-10",
    "nomeacao_em": "2026-03-20",
    "classificacao": 2,
    "sessao": "1ª sessão",
    "hora_convocacao_inicio": "09:00",
    "hora_convocacao_fim": "10:00",
}

EXEMPLO_LOTE = {
    "processo_uuid": UUID_PROCESSO_EXEMPLO,
    "processo_nome": NOME_PROCESSO_EXEMPLO,
    "candidatos_uuids": [
        UUID_CANDIDATO_1_EXEMPLO,
        UUID_CANDIDATO_2_EXEMPLO,
        UUID_CANDIDATO_3_EXEMPLO,
    ],
    "agendas": [
        EXEMPLO_ITEM,
        {
            **EXEMPLO_ITEM,
            "classificacao": 1,
            "sessao": "2ª sessão",
            "hora_convocacao_inicio": "10:00",
            "hora_convocacao_fim": "11:00",
        },
        {
            **EXEMPLO_ITEM,
            "modalidade": "ONLINE",
            "sessao": "Retardatários",
            "retardatario": True,
            "hora_convocacao_inicio": "14:00",
            "hora_convocacao_fim": "15:00",
        },
    ],
}

EXEMPLO_LOTE_DE_ATUALIZACAO = {
    "processo_uuid": UUID_PROCESSO_EXEMPLO,
    "processo_nome": NOME_PROCESSO_EXEMPLO,
    "candidatos_uuids": [UUID_CANDIDATO_1_EXEMPLO, UUID_CANDIDATO_2_EXEMPLO],
    "agendas": [
        {
            **EXEMPLO_ITEM,
            "uuid": UUID_AGENDA_EXEMPLO,
            "sessao": "1ª sessão (remarcada)",
        }
    ],
}

EXEMPLO_DADOS_AGENDA = {
    "processo_convocacao_uuid": UUID_PROCESSO_EXEMPLO,
    "processo_convocacao_nome": NOME_PROCESSO_EXEMPLO,
    "cargo_uuid": UUID_CARGO_EXEMPLO,
    "cargo_nome": NOME_CARGO_EXEMPLO,
    "cargo_codigo": CODIGO_CARGO_EXEMPLO,
    "modalidade": "PRESENCIAL",
    "escolha_em": "2026-03-10",
    "classificacao": 2,
    "sessao": "1ª sessão (remarcada)",
    "hora_convocacao_inicio": "09:00",
    "hora_convocacao_fim": "10:00",
    "candidatos_uuids": [UUID_CANDIDATO_1_EXEMPLO, UUID_CANDIDATO_2_EXEMPLO],
}

ERRO_MODALIDADE = {"modalidade": ['"Online" não é um escolha válido.']}

ERRO_PROCESSO_OBRIGATORIO = {"detail": "processo_uuid é obrigatório."}


class AgendasGravadasExtension(OpenApiSerializerExtension):
    """Descreve ``AgendasGravadasSerializer`` como lista de agendas."""

    target_class = AgendasGravadasSerializer

    def map_serializer(
        self, auto_schema: AutoSchema, direction: Direction
    ) -> dict[str, Any]:
        """Retorna o schema da lista, sem o envelope de página."""
        return {
            "type": "array",
            "description": (
                "Agendas gravadas pelo envio: primeiro as criadas, depois "
                "as atualizadas, cada grupo na ordem dos itens enviados."
            ),
            "items": auto_schema.resolve_serializer(
                AgendaListSerializer, direction
            ).ref,
        }


PARAMETRO_UUID = parametro_uuid("UUID da agenda.")

PARAMETRO_PROCESSO = OpenApiParameter(
    name="processo_uuid",
    type=OpenApiTypes.UUID,
    required=True,
    description=(
        f"UUID do processo de convocação. {AVISO_PROCESSO_MALFORMADO}"
    ),
)

PARAMETROS_LISTAGEM = [
    OpenApiParameter(
        name="processo_convocacao_uuid",
        type=OpenApiTypes.UUID,
        description=(
            "Retorna apenas as agendas do processo de convocação informado."
        ),
    ),
    OpenApiParameter(
        name="cargo_uuid",
        type=OpenApiTypes.UUID,
        description="Retorna apenas as agendas do cargo informado.",
    ),
    parametro_busca(
        "Busca por trecho do nome do processo ou do nome do cargo."
    ),
    OpenApiParameter(
        name="ordering",
        type=OpenApiTypes.STR,
        description=(
            "Campo de ordenação dentro de cada modalidade: `data_escolha`, "
            "`hora_convocacao_inicio` ou `criado_em`. Prefixe com `-` para "
            "ordem decrescente e separe vários campos por vírgula. Sem o "
            "parâmetro, vale a data da sessão (`escolha_em`) e depois a "
            "hora de início. Outros campos são ignorados."
        ),
    ),
    PARAMETRO_PAGINA,
    PARAMETRO_TAMANHO_PAGINA,
]

RESPOSTA_AGENDA = resposta(
    AgendaListSerializer, "Agenda.", {"Agenda": EXEMPLO_AGENDA}
)

RESPOSTA_AGENDA_ALTERADA = resposta(
    AgendaCreateSerializer,
    "Agenda com os dados alterados.",
    {"Agenda alterada": EXEMPLO_AGENDA_ALTERADA},
)

RESPOSTA_NAO_ENCONTRADO = resposta_nao_encontrado(Agenda)

RESPOSTA_EXCLUIDAS = resposta(
    AgendasExcluidasSerializer,
    "Quantidade de agendas excluídas.",
    {
        "Três agendas excluídas": {"excluidas": 3},
        "Nenhuma agenda encontrada": {"excluidas": 0},
    },
)

OPERACOES_AGENDAS = {
    "list": extend_schema(
        operation_id="listar_agendas",
        summary="Listar agendas",
        description=(
            "Retorna as agendas em páginas. As de modalidade ONLINE vêm "
            "sempre primeiro; dentro de cada grupo vale a ordenação "
            "pedida.\n\n"
            "Quando a primeira agenda da página é ONLINE, o serviço "
            "consulta o MS-Escolhas e acrescenta "
            "`candidatos_uuids_restantes`: os candidatos dessa agenda que "
            "ainda não têm escolha em vaga do processo. Se o MS-Escolhas "
            "não responde, a listagem vem sem o campo."
        ),
        parameters=PARAMETROS_LISTAGEM,
        responses=respostas(
            {
                200: resposta(
                    AgendaPaginadaSerializer,
                    "Página de agendas.",
                    {
                        "Agendas presenciais": exemplo_pagina(
                            [EXEMPLO_AGENDA, EXEMPLO_AGENDA_2]
                        ),
                        "Primeira agenda ONLINE": {
                            **exemplo_pagina(
                                [EXEMPLO_AGENDA_ONLINE, EXEMPLO_AGENDA]
                            ),
                            "candidatos_uuids_restantes": [
                                UUID_CANDIDATO_2_EXEMPLO
                            ],
                        },
                    },
                ),
                400: resposta(
                    ErrosValidacaoSerializer,
                    "Filtro com valor que não é UUID.",
                    {
                        "UUID malformado": {
                            "processo_convocacao_uuid": [
                                "Insira um UUID válido."
                            ]
                        }
                    },
                ),
                404: RESPOSTA_PAGINA_INEXISTENTE,
                500: erro_interno("quando `page_size` não é numérico"),
            }
        ),
    ),
    "create": extend_schema(
        operation_id="criar_agendas_em_lote",
        summary="Criar ou atualizar agendas em lote",
        description=(
            "Grava as sessões de um processo de convocação e distribui os "
            "candidatos entre elas. Cada item de `agendas` vira uma "
            "agenda: com o `uuid` de uma agenda existente, ela é "
            "atualizada; nos demais casos, uma agenda nova é criada.\n\n"
            "**Distribuição dos candidatos.** O serviço pede ao "
            "MS-Candidatos os habilitados de `candidatos_uuids`, em ordem "
            "de ranking de escolha. Percorrendo os itens na ordem "
            "enviada, cada sessão regular recebe a fatia seguinte da "
            "lista, do tamanho de `classificacao`. A sessão de "
            "retardatários recebe os primeiros `classificacao` candidatos "
            "da lista, sem consumir a fila das sessões regulares. UUIDs "
            "que o MS-Candidatos não devolve ficam fora da "
            "distribuição.\n\n"
            "Toda chamada refaz a distribuição das agendas enviadas: sem "
            "`candidatos_uuids`, elas ficam sem candidatos, inclusive as "
            "atualizadas.\n\n"
            "- **201**: ao menos uma agenda foi criada.\n"
            "- **200**: todas as agendas enviadas já existiam e foram "
            "atualizadas.\n"
            "- **502**: o MS-Candidatos não respondeu; nada é gravado.\n\n"
            "As agendas são gravadas uma a uma. Se um item é recusado, a "
            "resposta é 400 com o erro dele, e as agendas dos itens "
            "anteriores continuam gravadas."
        ),
        request=AgendasLoteRequisicaoSerializer,
        examples=exemplos_requisicao(
            {
                "Duas sessões e a de retardatários": EXEMPLO_LOTE,
                "Atualizar uma agenda": EXEMPLO_LOTE_DE_ATUALIZACAO,
            }
        ),
        responses=respostas(
            {
                200: resposta(
                    AgendasGravadasSerializer,
                    "Agendas atualizadas; nenhuma foi criada.",
                    {"Uma agenda atualizada": [EXEMPLO_AGENDA_ALTERADA]},
                ),
                201: resposta(
                    AgendasGravadasSerializer,
                    "Agendas gravadas, com ao menos uma criada.",
                    {
                        "Três agendas criadas": [
                            EXEMPLO_AGENDA,
                            EXEMPLO_AGENDA_2,
                            EXEMPLO_AGENDA_ONLINE,
                        ]
                    },
                ),
                400: resposta(
                    ErrosValidacaoSerializer,
                    (
                        "Dados inválidos. Os erros do lote vêm com as "
                        "chaves do corpo enviado, e os de `agendas`, pela "
                        "posição do item. Os erros encontrados ao gravar "
                        "uma agenda vêm com as chaves da própria agenda, "
                        "sem a posição do item."
                    ),
                    {
                        "Campos do lote ausentes": {
                            "agendas": ['O campo "agendas" é obrigatório'],
                            "processo_uuid": [
                                'O campo "processo_uuid" é obrigatório'
                            ],
                        },
                        "Item sem campos obrigatórios": {
                            "agendas": {
                                "0": {
                                    "cargo_uuid": [
                                        "Este campo é obrigatório."
                                    ],
                                    "classificacao": [
                                        "Este campo é obrigatório."
                                    ],
                                }
                            }
                        },
                        "Processo sem nome e cargo sem código": {
                            "processo_convocacao_nome": [
                                "Este campo não pode ser em branco."
                            ],
                            "cargo_codigo": [
                                "Este campo não pode ser em branco."
                            ],
                        },
                        "Modalidade fora das opções": ERRO_MODALIDADE,
                    },
                ),
                500: erro_interno(
                    "quando o corpo é uma lista em vez de um objeto"
                ),
                502: resposta(
                    ErroDetalheSerializer,
                    "O MS-Candidatos não respondeu. Nada é gravado.",
                    {
                        "MS-Candidatos indisponível": {
                            "detail": "Erro ao consultar API de candidatos."
                        }
                    },
                ),
            }
        ),
    ),
    "retrieve": extend_schema(
        operation_id="detalhar_agenda",
        summary="Detalhar agenda",
        description=f"Retorna uma agenda pelo UUID.\n\n{AVISO_ROTA_HERDADA}",
        parameters=[PARAMETRO_UUID],
        responses=respostas(
            {200: RESPOSTA_AGENDA, 404: RESPOSTA_NAO_ENCONTRADO}
        ),
    ),
    "update": extend_schema(
        operation_id="atualizar_agenda",
        summary="Atualizar agenda",
        description=(
            "Substitui os dados de uma agenda. "
            "`processo_convocacao_uuid`, `processo_convocacao_nome`, "
            "`cargo_uuid` e `cargo_nome` são obrigatórios; os demais "
            "campos mantêm o valor atual quando omitidos. "
            f"{AVISO_SEM_REDISTRIBUICAO}\n\n{AVISO_ROTA_HERDADA}"
        ),
        parameters=[PARAMETRO_UUID],
        request=AgendaCreateSerializer,
        examples=exemplos_requisicao(
            {"Dados da agenda": EXEMPLO_DADOS_AGENDA}
        ),
        responses=respostas(
            {
                200: RESPOSTA_AGENDA_ALTERADA,
                400: resposta(
                    ErrosValidacaoSerializer,
                    "Dados inválidos.",
                    {
                        "Campos ausentes": {
                            "processo_convocacao_uuid": [
                                "Este campo é obrigatório."
                            ],
                            "processo_convocacao_nome": [
                                "Este campo é obrigatório."
                            ],
                            "cargo_uuid": ["Este campo é obrigatório."],
                            "cargo_nome": ["Este campo é obrigatório."],
                        },
                        "Modalidade fora das opções": ERRO_MODALIDADE,
                    },
                ),
                404: RESPOSTA_NAO_ENCONTRADO,
            }
        ),
    ),
    "partial_update": extend_schema(
        operation_id="atualizar_parcial_agenda",
        summary="Atualizar agenda parcialmente",
        description=(
            "Altera apenas os campos enviados de uma agenda. "
            f"{AVISO_SEM_REDISTRIBUICAO}"
        ),
        parameters=[PARAMETRO_UUID],
        request=AgendaCreateSerializer,
        examples=exemplos_requisicao(
            {
                "Remarcar o horário": {
                    "hora_convocacao_inicio": "10:00",
                    "hora_convocacao_fim": "11:00",
                }
            }
        ),
        responses=respostas(
            {
                200: RESPOSTA_AGENDA_ALTERADA,
                400: resposta(
                    ErrosValidacaoSerializer,
                    "Dados inválidos.",
                    {
                        "Modalidade e data inválidas": {
                            **ERRO_MODALIDADE,
                            "escolha_em": [
                                "Formato inválido para data. Use um dos "
                                "formatos a seguir: YYYY-MM-DD."
                            ],
                        }
                    },
                ),
                404: RESPOSTA_NAO_ENCONTRADO,
            }
        ),
    ),
    "destroy": extend_schema(
        operation_id="excluir_agenda",
        summary="Excluir agenda",
        description="Exclui a agenda definitivamente.",
        parameters=[PARAMETRO_UUID],
        responses=respostas(
            {
                204: resposta(None, "Agenda excluída."),
                404: RESPOSTA_NAO_ENCONTRADO,
            }
        ),
    ),
    "excluir_por_processo": extend_schema(
        operation_id="excluir_agendas_por_processo",
        summary="Excluir as agendas de um processo",
        description=(
            "Exclui definitivamente todas as agendas do processo de "
            "convocação. Responde 200 também quando o processo não tem "
            "agendas."
        ),
        parameters=[PARAMETRO_PROCESSO],
        responses=respostas(
            {
                200: RESPOSTA_EXCLUIDAS,
                400: resposta(
                    ErroDetalheSerializer,
                    "Parâmetro `processo_uuid` ausente.",
                    {"Processo não informado": ERRO_PROCESSO_OBRIGATORIO},
                ),
                500: erro_interno("quando `processo_uuid` não é um UUID"),
            }
        ),
    ),
    "excluir_por_processo_e_cargo": extend_schema(
        operation_id="excluir_agendas_por_processo_e_cargo",
        summary="Excluir as agendas de um processo e cargo",
        description=(
            "Exclui definitivamente as agendas do processo de convocação "
            "que têm o código de cargo informado. Responde 200 também "
            "quando nenhuma agenda corresponde aos dois parâmetros."
        ),
        parameters=[
            PARAMETRO_PROCESSO,
            OpenApiParameter(
                name="cargo",
                type=OpenApiTypes.STR,
                required=True,
                description=(
                    "Código do cargo (`cargo_codigo`), e não o UUID. Com "
                    "o UUID do cargo, nenhuma agenda é encontrada."
                ),
            ),
        ],
        responses=respostas(
            {
                200: RESPOSTA_EXCLUIDAS,
                400: resposta(
                    ErroDetalheSerializer,
                    "Parâmetro `processo_uuid` ou `cargo` ausente.",
                    {
                        "Processo não informado": ERRO_PROCESSO_OBRIGATORIO,
                        "Cargo não informado": {
                            "detail": "cargo é obrigatório."
                        },
                    },
                ),
                500: erro_interno("quando `processo_uuid` não é um UUID"),
            }
        ),
    ),
}
