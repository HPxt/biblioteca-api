"""Regras de negócio relacionadas a Livro."""

from sqlalchemy.orm import Session

from app.models.livro import Livro
from app.schemas import LivroCreate


def criar_livro(db: Session, dados: LivroCreate) -> Livro:
    """Cria um novo livro no banco de dados."""
    livro = Livro(
        titulo=dados.titulo,
        autor=dados.autor,
        isbn=dados.isbn,
        quantidade_total=dados.quantidade_total,
        quantidade_disponivel=dados.quantidade_total,
    )
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro


def listar_livros(db: Session):
    """Retorna todos os livros cadastrados."""
    return db.query(Livro).all()


def buscar_livro_por_id(db: Session, livro_id: int) -> Livro | None:
    """Busca um livro pelo seu identificador."""
    return db.query(Livro).filter(Livro.id == livro_id).first()


def buscar_livro_por_isbn(db: Session, isbn: str) -> Livro | None:
    """Busca um livro pelo ISBN."""
    return db.query(Livro).filter(Livro.isbn == isbn).first()


def remover_livro(db: Session, livro_id: int) -> bool:
    """Remove um livro do banco de dados, se existir."""
    livro = buscar_livro_por_id(db, livro_id)
    if not livro:
        return False
    db.delete(livro)
    db.commit()
    return True
