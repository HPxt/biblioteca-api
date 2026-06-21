"""Rotas da API relacionadas a Livros."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import LivroCreate, LivroResponse
from app.services import livro_service

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.post("/", response_model=LivroResponse, status_code=201)
def criar_livro(dados: LivroCreate, db: Session = Depends(get_db)):
    existente = livro_service.buscar_livro_por_isbn(db, dados.isbn)
    if existente:
        raise HTTPException(status_code=400, detail="Já existe um livro com este ISBN.")
    return livro_service.criar_livro(db, dados)


@router.get("/", response_model=list[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    return livro_service.listar_livros(db)


@router.get("/{livro_id}", response_model=LivroResponse)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = livro_service.buscar_livro_por_id(db, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return livro


@router.delete("/{livro_id}", status_code=204)
def remover_livro(livro_id: int, db: Session = Depends(get_db)):
    removido = livro_service.remover_livro(db, livro_id)
    if not removido:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
