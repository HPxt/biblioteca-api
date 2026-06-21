"""Ponto de entrada da API de Gerenciamento de Biblioteca."""

from fastapi import FastAPI

from app.database import init_db
from app.routers import livros, usuarios, emprestimos

app = FastAPI(
    title="API de Gerenciamento de Biblioteca",
    description="Sistema para gerenciamento de livros, usuários e empréstimos.",
    version="1.0.0",
)

app.include_router(livros.router)
app.include_router(usuarios.router)
app.include_router(emprestimos.router)


@app.on_event("startup")
def startup_event():
    """Inicializa o banco de dados na inicialização da aplicação."""
    init_db()


@app.get("/", tags=["Health"])
def health_check():
    """Endpoint simples de verificação de saúde da aplicação."""
    return {"status": "ok", "service": "biblioteca-api"}
