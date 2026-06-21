"""Regras de negócio relacionadas a Usuario."""

from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas import UsuarioCreate


def criar_usuario(db: Session, dados: UsuarioCreate) -> Usuario:
    """Cria um novo usuário no banco de dados."""
    usuario = Usuario(nome=dados.nome, email=dados.email)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def listar_usuarios(db: Session):
    """Retorna todos os usuários cadastrados."""
    return db.query(Usuario).all()


def buscar_usuario_por_id(db: Session, usuario_id: int) -> Usuario | None:
    """Busca um usuário pelo seu identificador."""
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def buscar_usuario_por_email(db: Session, email: str) -> Usuario | None:
    """Busca um usuário pelo email."""
    return db.query(Usuario).filter(Usuario.email == email).first()


def desativar_usuario(db: Session, usuario_id: int) -> bool:
    """Desativa um usuário, impedindo novos empréstimos."""
    usuario = buscar_usuario_por_id(db, usuario_id)
    if not usuario:
        return False
    usuario.desativar()
    db.commit()
    return True
