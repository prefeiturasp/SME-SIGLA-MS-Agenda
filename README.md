# Agenda SIGLA Backend

Backend Django para gerenciamento de agendas de convocação da SIGLA.

## 🚀 Funcionalidades

### Agendas de Convocação
- **CRUD completo** de agendas
- **Vinculação com processos de convocação** via UUID e nome
- **Vinculação com cargos** via UUID e nome
- **Controle de data de escolha**

## 🏗️ Arquitetura

### Modelo Principal

#### `Agenda`
- Representa o vínculo entre um processo de convocação e um cargo em uma data de escolha
- Campos principais:
  - `processo_convocacao_uuid` (UUID)
  - `processo_convocacao_nome` (string)
  - `cargo_uuid` (UUID)
  - `cargo_nome` (string)
  - `data_escolha` (datetime)

## 📊 API Endpoints

Base path do projeto: `/api/v1/`

### Agendas
- `GET /api/v1/agendas/` - Listar agendas
- `POST /api/v1/agendas/` - Criar agenda
- `GET /api/v1/agendas/{uuid}/` - Detalhes da agenda
- `PUT /api/v1/agendas/{uuid}/` - Atualizar agenda
- `PATCH /api/v1/agendas/{uuid}/` - Atualização parcial
- `DELETE /api/v1/agendas/{uuid}/` - Excluir agenda
- `GET /api/v1/agendas/filtros/` - Listar processos e cargos únicos existentes nas agendas

### Filtros e Consultas
- Filtros diretos:
  - `processo_convocacao_uuid`
  - `cargo_uuid`
- Filtros por data (query params):
  - `data_escolha_inicio=YYYY-MM-DD`
  - `data_escolha_fim=YYYY-MM-DD`
- Busca (`?search=`): por `processo_convocacao_nome` e `cargo_nome`
- Ordenação (`?ordering=`): por `data_escolha` ou `criado_em`

## 🛠️ Tecnologias

- **Django 5.2.5** - Framework web
- **Django REST Framework 3.15.2** - API REST
- **PostgreSQL** ou **SQLite** - Banco de dados
- **django-cors-headers** - CORS para frontend
- **django-filter** - Filtros

## 🚀 Como Executar

### 1. Configuração do Ambiente
```bash
# Clonar o repositório
git clone <repository-url>
cd agenda-sigla-backend

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements/base.txt
```

### 2. Configuração do Banco
```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar variáveis de ambiente
# DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, etc.
```

### 3. Migrações e Setup
```bash
# Aplicar migrações
python manage.py migrate

# (Opcional) Criar superusuário, se necessário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

## 📝 Exemplos de Uso

### Criar Agenda
```http
POST /api/v1/agendas/
Content-Type: application/json

{
  "processo_convocacao_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "processo_convocacao_nome": "Processo de Convocação 2024",
  "cargo_uuid": "456e7890-e89b-12d3-a456-426614174001",
  "cargo_nome": "Analista de Sistemas",
  "data_escolha": "2024-12-01T10:00:00Z"
}
```

### Consultar Filtros
```http
GET /api/v1/agendas/filtros/
```
Resposta:
```json
{
  "processos": [
    { "value": "<uuid-proc>", "label": "Processo de Convocação 2024" }
  ],
  "cargos": [
    { "value": "<uuid-cargo>", "label": "Analista de Sistemas" }
  ]
}
```

## 🔧 Configurações

### Variáveis de Ambiente
- `SECRET_KEY` - Chave secreta do Django
- `DEBUG` - Modo debug (True/False)
- `DB_ENGINE` - Engine do banco (postgresql/sqlite3)
- `DB_NAME` - Nome do banco
- `DB_USER` - Usuário do banco
- `DB_PASSWORD` - Senha do banco
- `DB_HOST` - Host do banco
- `DB_PORT` - Porta do banco

### Configurações Django
- **Idioma**: Português (pt-br)
- **Fuso horário**: America/Sao_Paulo
- **Paginação**: 20 itens por página
- **Permissões**: Aberto (AllowAny) por padrão neste projeto
- **CORS**: Habilitado para desenvolvimento

## 📚 Documentação da API

A API inclui documentação automática via Django REST Framework:
- **Browsable API**: `/api/v1/agendas/`
- **Endpoints exploráveis** com interface web

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 