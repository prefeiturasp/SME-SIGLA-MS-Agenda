Estrutura do projeto
====================

Esta seção explica **cada pasta do repositório** e o papel de cada módulo dentro de ``apps/``.

Visão da árvore principal
-------------------------

.. code-block:: text

   ms-agenda/
   ├── apps/              # Módulos de negócio (Django apps)
   ├── config/            # Configurações do projeto Django
   ├── docs/              # Documentação Sphinx (este material)
   ├── requirements/      # Dependências Python por ambiente
   ├── manage.py          # Ponto de entrada do Django
   ├── Dockerfile         # Imagem Docker da API
   ├── docker-compose.yml # Ambiente local (API + banco)
   └── Makefile           # Comandos úteis de desenvolvimento

Pasta ``apps/``
---------------

É onde ficam os **módulos de negócio**. Cada subpasta é um app Django com responsabilidade bem definida.

``apps/core/``
~~~~~~~~~~~~~~

**O que faz:** Fornece a base comum usada pelo restante do projeto.

**Para que serve:** Evita repetir código. Todo modelo do sistema herda de ``BaseModel``, que já traz:

- Identificador único (UUID)
- Data de criação
- Data da última atualização

Também disponibiliza a paginação padrão das listagens da API (formato SIGLA com ``links``, ``count``, ``page``, ``page_size`` e ``results``).

**Analogia:** É a "ficha padrão" que todo cadastro do sistema usa — como um formulário com campos obrigatórios no topo.

``apps/agenda/``
~~~~~~~~~~~~~~~~

**O que faz:** É o **coração** do microserviço. Gerencia as sessões de convocação e as integrações com candidatos e escolhas.

**Para que serve:**

- CRUD e listagem de agendas
- Criação/atualização em lote a partir de um processo
- Distribuição de candidatos por classificação e sessão retardatária
- Exclusão por processo ou por processo e cargo
- Consulta de candidatos restantes em sessões online

**Principais partes internas:**

.. list-table:: Módulos do app agenda
   :header-rows: 1
   :widths: 35 65

   * - Subpasta / arquivo
     - Função
   * - ``models/``
     - Modelo ``Agenda`` e constantes de modalidade
   * - ``api/``
     - Views e rotas REST
   * - ``repository.py``
     - Acesso ao banco (consultas, criação e exclusão)
   * - ``serializers.py``
     - Validação e conversão dos dados da API
   * - ``filters.py``
     - Ordenação com sessões online primeiro
   * - ``services/``
     - Clientes HTTP de Candidatos e Escolhas
   * - ``management/commands/``
     - Criar exemplos e limpar agendas
   * - ``tests/``
     - Testes automatizados do app

**Exemplo:** O frontend envia ``POST /agendas/`` com o processo, as sessões e os UUIDs dos candidatos; o app ordena pelo ranking, fatia a lista e grava as agendas.

Pasta ``config/``
-----------------

**O que faz:** Configurações centrais do projeto Django.

**Para que serve:**

.. list-table:: Arquivos de configuração
   :header-rows: 1
   :widths: 25 75

   * - Arquivo
     - Função
   * - ``settings.py``
     - Banco de dados, apps instalados, CORS, URLs de integração, API keys
   * - ``settings_test.py``
     - Configuração usada pelos testes automatizados
   * - ``urls.py``
     - Rotas da API (``/api/v1/``), admin, healthcheck e Swagger
   * - ``wsgi.py``
     - Ponto de entrada para servidores de produção

**Exemplo:** As variáveis ``API_KEY``, ``CANDIDATOS_API_URL`` e ``ESCOLHAS_API_URL`` em ``settings.py`` dizem ao sistema como autenticar e onde buscar candidatos e escolhas.

Pasta ``requirements/``
-----------------------

**O que faz:** Lista as **dependências Python** do projeto, separadas por ambiente.

**Para que serve:**

.. list-table:: Arquivos de dependências
   :header-rows: 1
   :widths: 25 75

   * - Arquivo
     - Conteúdo
   * - ``base.txt``
     - Dependências essenciais (Django, DRF, PostgreSQL, auditlog, SDK)
   * - ``local.txt``
     - Desenvolvimento (testes, lint, Sphinx, debug toolbar)
   * - ``production.txt``
     - Produção (gunicorn)

Pasta ``docs/``
---------------

**O que faz:** Contém esta documentação em formato reStructuredText (``.rst``) e a configuração do Sphinx.

**Para que serve:** Gerar o site HTML de documentação com ``make docs`` ou ``sphinx-build``.

Arquivos na raiz
----------------

.. list-table:: Arquivos na raiz do projeto
   :header-rows: 1
   :widths: 25 75

   * - Arquivo
     - Função
   * - ``manage.py``
     - Comando Django (migrações, servidor, superusuário, comandos)
   * - ``docker-compose.yml``
     - Sobe API e PostgreSQL juntos
   * - ``Dockerfile``
     - Constrói a imagem Docker da API
   * - ``Makefile``
     - Atalhos: testes, lint, migrações, pre-commit e documentação
   * - ``README.md``
     - Visão técnica rápida e instruções de execução
   * - ``.pre-commit-config.yaml``
     - Hooks de qualidade (black, ruff, mypy)

API — endpoints principais (referência)
---------------------------------------

Para consulta rápida, os principais caminhos da API (prefixo ``/api/v1/``):

**Agendas**

- ``GET /agendas/`` — Listar agendas (filtros por processo e cargo; online primeiro)
- ``POST /agendas/`` — Criar ou atualizar agendas em lote
- ``GET /agendas/{uuid}/`` — Detalhes
- ``PUT /agendas/{uuid}/`` — Atualizar agenda
- ``PATCH /agendas/{uuid}/`` — Atualizar parcialmente
- ``DELETE /agendas/{uuid}/`` — Excluir uma agenda
- ``DELETE /agendas/por-processo/`` — Excluir agendas do processo
- ``DELETE /agendas/por-processo-e-cargo/`` — Excluir agendas do processo e cargo

A documentação interativa da API (Swagger) está disponível em ``/api/docs/`` quando o servidor está rodando.

Comandos úteis de management
----------------------------

.. list-table:: Comandos Django
   :header-rows: 1
   :widths: 40 60

   * - Comando
     - Finalidade
   * - ``criar_agendas``
     - Cria agendas de exemplo para desenvolvimento
   * - ``limpar_agendas``
     - Remove todas as agendas cadastradas
