"""Rotas da API relacionadas a Usuários."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UsuarioCreate, UsuarioResponse
from app.services import usuario_service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse, status_code=201)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    existente = usuario_service.buscar_usuario_por_email(db, dados.email)
    if existente:
        raise HTTPException(status_code=400, detail="Já existe um usuário com este email.")
    return usuario_service.criar_usuario(db, dados)


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_service.listar_usuarios(db)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuario_service.buscar_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario


@router.patch("/{usuario_id}/desativar", status_code=200)
def desativar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    sucesso = usuario_service.desativar_usuario(db, usuario_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return {"detail": "Usuário desativado com sucesso."}
