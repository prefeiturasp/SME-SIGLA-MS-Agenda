Regras de negócio
=================

Esta seção descreve as **regras que o sistema aplica** — ou seja, o que pode e o que não pode acontecer no cadastro e na consulta de agendas.

Agenda
------

O que é
~~~~~~~

Uma **agenda** representa uma **sessão de convocação** de um processo, para um cargo. Cada registro guarda, entre outros dados:

- Processo de convocação (UUID e nome)
- Cargo (UUID, nome e código)
- Data de publicação
- Modalidade (presencial ou online)
- Data de escolha e data de nomeação
- Classificação (quantidade de candidatos daquela sessão)
- Sessão (identificação textual)
- Se é **retardatária**
- Horário de início e fim da convocação
- Lista de UUIDs dos candidatos daquela sessão

Modalidade
~~~~~~~~~~

.. list-table:: Modalidades da agenda
   :header-rows: 1
   :widths: 25 75

   * - Modalidade
     - Significado
   * - **Presencial**
     - A escolha acontece em sessão presencial
   * - **Online**
     - A escolha acontece de forma online

Criação e atualização em lote
-----------------------------

O ``POST /agendas/`` **não cria uma agenda isolada**. Ele recebe um lote com:

- Lista de **agendas** (ao menos uma)
- Lista de **candidatos_uuids** (pode ser vazia)
- **processo_uuid** (obrigatório)
- **processo_nome** (opcional)

Como os candidatos são distribuídos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Se houver UUIDs de candidatos, o sistema consulta o **Módulo Candidatos** e **ordena** a lista por ranking de escolha.
2. Se essa consulta falhar, a criação **não segue** (erro de integração).
3. Para cada item do lote:

   - **Sessão regular** (não retardatária): pega a **próxima fatia** da lista ordenada, do tamanho da ``classificacao``, e avança o cursor.
   - **Sessão retardatária**: pega os candidatos **do início** da lista ordenada até a ``classificacao`` (não usa o cursor das sessões regulares).

4. O processo (UUID e nome) é copiado para cada agenda gerada.
5. Se o item vier com ``uuid`` e a agenda existir, o registro é **atualizado**; se o UUID não existir, a agenda é **criada**. Sem UUID, sempre cria.

**Exemplo:** 10 candidatos ordenados por ranking e duas sessões regulares com classificação 4 e 6. A primeira sessão fica com os 4 primeiros; a segunda, com os 6 seguintes. Uma sessão retardatária com classificação 3 ficaria com os 3 primeiros da lista original.

Listagem
--------

Regras importantes
~~~~~~~~~~~~~~~~~~

- É possível filtrar por ``processo_convocacao_uuid`` e ``cargo_uuid``.
- A busca textual considera nome do processo e nome do cargo.
- A ordenação padrão usa data de escolha e horário de início.
- Agendas **ONLINE** aparecem **antes** das demais na listagem.
- Se a primeira agenda da página for **ONLINE**, o sistema consulta o **Módulo Escolhas** pelo processo e devolve ``candidatos_uuids_restantes``: candidatos daquela agenda que **ainda não escolheram**.
- Se a consulta de escolhas falhar, a listagem **continua** (sem a lista de restantes).

Exclusão
--------

Há duas formas de excluir em lote:

.. list-table:: Exclusão de agendas
   :header-rows: 1
   :widths: 40 60

   * - Ação
     - Regra
   * - Por processo
     - ``processo_uuid`` é obrigatório; remove todas as agendas daquele processo
   * - Por processo e cargo
     - ``processo_uuid`` e ``cargo`` (código do cargo) são obrigatórios; remove só as agendas daquele par

A resposta informa quantos registros foram excluídos.

Auditoria
---------

Alterações em agendas são **registradas automaticamente** (quem alterou, quando e o que mudou), via auditoria do modelo.
