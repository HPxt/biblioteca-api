# Biblioteca API

API REST para gerenciamento de livros, usuários e empréstimos de uma biblioteca, desenvolvida como projeto da disciplina de Gerência de Configuração e Evolução de Software.

## Tecnologias

- **Linguagem:** Python 3.11
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Banco de dados:** SQLite
- **Testes:** Pytest
- **Containerização:** Docker
- **CI/CD:** GitHub Actions

## Estrutura do projeto

```
biblioteca-api/
├── app/
│   ├── main.py                 # Ponto de entrada da aplicação
│   ├── database.py             # Configuração do banco de dados
│   ├── schemas.py              # Schemas de validação (Pydantic)
│   ├── models/                 # Entidades (Livro, Usuario, Emprestimo)
│   ├── routers/                # Rotas da API
│   └── services/                # Regras de negócio
├── tests/
│   ├── unit/                   # Testes unitários
│   ├── integration/            # Testes de integração
│   └── acceptance/             # Testes de aceitação (end-to-end via API)
├── .github/workflows/ci-cd.yml # Pipeline de CI/CD
├── Dockerfile
└── requirements.txt
```

## Como executar localmente

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`, com documentação interativa em `http://localhost:8000/docs`.

## Como executar com Docker

```bash
docker build -t biblioteca-api .
docker run -p 8000:8000 biblioteca-api
```

## Como executar os testes

```bash
# Todos os testes
python -m pytest tests/ -v

# Apenas testes unitários
python -m pytest tests/unit -v

# Apenas testes de integração
python -m pytest tests/integration -v

# Apenas testes de aceitação
python -m pytest tests/acceptance -v

# Com relatório de cobertura
python -m pytest tests/ --cov=app --cov-report=term-missing
```

## Pipeline de CI/CD

O pipeline é executado automaticamente a cada `push` ou `pull request` para a branch `main`, e contempla três etapas:

1. **Commit Stage:** build da aplicação, testes unitários e testes de integração.
2. **Acceptance Test Stage:** testes de aceitação end-to-end via chamadas HTTP à API.
3. **Release Stage:** build da imagem Docker e publicação no GitHub Container Registry (ghcr.io).

## Endpoints principais

| Método | Rota | Descrição |
|---|---|---|
| POST | `/livros/` | Cadastra um novo livro |
| GET | `/livros/` | Lista todos os livros |
| GET | `/livros/{id}` | Busca um livro por ID |
| DELETE | `/livros/{id}` | Remove um livro |
| POST | `/usuarios/` | Cadastra um novo usuário |
| GET | `/usuarios/` | Lista todos os usuários |
| PATCH | `/usuarios/{id}/desativar` | Desativa um usuário |
| POST | `/emprestimos/` | Realiza um empréstimo |
| PATCH | `/emprestimos/{id}/devolver` | Processa a devolução |
| GET | `/emprestimos/atrasados` | Lista empréstimos atrasados |

## Autores

- Arthur Curi
- Helio Teixeira
- Joao
- Mateus Faissal
- Raphael Senna
- Henrique Peixoto
