Visão geral
===========

O que é este módulo?
--------------------

O **Módulo Agenda** é o sistema responsável por registrar as **sessões de convocação** de um processo da SME (Secretaria Municipal de Educação de São Paulo): data, horário, modalidade (presencial ou online), cargo e quais candidatos entram naquela faixa.

Em termos simples: depois que o processo de convocação existe e os candidatos estão habilitados, a equipe precisa **montar a agenda** — quem escolhe em qual sessão, em que horário e se a escolha é presencial ou online. Este módulo guarda essas sessões e a lista de candidatos de cada uma.

Para que serve?
---------------

O sistema permite que a equipe da SME:

- **Crie e atualize agendas em lote** a partir de um processo de convocação
- **Distribua candidatos** nas sessões segundo a classificação (ranking de escolha)
- **Consulte agendas** por processo, cargo, nome do processo ou nome do cargo
- **Priorize sessões online** na listagem e, nesse caso, veja quem ainda não escolheu
- **Exclua agendas** de um processo (ou de um processo e cargo)
- **Integre com outros módulos** (Candidatos, Escolhas e Processos de Convocação)

Onde ele se encaixa no ecossistema SIGLA?
-----------------------------------------

Este módulo **não trabalha sozinho**. Ele se integra com outros sistemas:

.. list-table:: Integrações do ecossistema
   :header-rows: 1
   :widths: 30 70

   * - Sistema
     - Papel no processo de agenda
   * - **Módulo Candidatos**
     - Ordena os UUIDs dos habilitados por ranking de escolha na criação da agenda
   * - **Módulo Escolhas**
     - Informa quem já escolheu vaga; na listagem online o agenda devolve os que ainda faltam
   * - **Módulo Processos de Convocação**
     - Origem do processo; cria, consulta e exclui agendas daquele processo
   * - **Frontend SIGLA**
     - Interface usada pela equipe para montar e acompanhar as sessões

O Módulo Agenda é a **referência central** das sessões de convocação usadas no fluxo de escolha.

Exemplo prático do dia a dia
----------------------------

Imagine o seguinte cenário:

1. A SME abre um **processo de convocação** para um cargo (ex.: Professor I).
2. Os candidatos habilitados já existem no **Módulo Candidatos**, com ranking de escolha.
3. A equipe monta **três sessões**: duas presenciais (manhã e tarde) e uma online.
4. O sistema consulta o ranking, **fatia os candidatos** pela quantidade de cada sessão e grava as agendas.
5. Quem não compareceu na sessão regular entra numa agenda **retardatária**, que reaproveita os primeiros da lista.
6. Na listagem **online**, o sistema pergunta ao Módulo Escolhas quem já escolheu e destaca os **candidatos restantes**.
7. Se o processo for refeito, as agendas daquele processo (ou daquele cargo) podem ser **excluídas** e geradas de novo.

Fluxo resumido
--------------

.. code-block:: text

   Processo de convocação  ----->  Lista de candidatos habilitados
                                            |
                                            v
                                   Ordenar por ranking de escolha
                                   (Módulo Candidatos)
                                            |
                                            v
                                   Criar / atualizar sessões
                                   (data, horário, modalidade, cargo)
                                            |
              +-----------------------------+-----------------------------+
              |                                                           |
              v                                                           v
     Sessão regular                                              Sessão retardatária
     (fatia sequencial da lista)                                 (do início até a quantidade)
              |
              v
     Listagem (ONLINE primeiro)
              |
              +-- Consultar escolhas já feitas (Módulo Escolhas)
              +-- Devolver candidatos ainda sem escolha

Tecnologias utilizadas (referência rápida)
------------------------------------------

Para quem precisa de contexto técnico sem entrar no código:

- **Django** — framework web que estrutura o projeto
- **Django REST Framework** — expõe a API consumida pelo frontend
- **PostgreSQL** — banco de dados onde ficam as agendas
- **django-auditlog** — registra quem alterou o quê e quando
- **drf-spectacular** — documentação interativa da API (Swagger)
- **sigla-sdk** — correlação de logs, cliente HTTP e autenticação entre microserviços
