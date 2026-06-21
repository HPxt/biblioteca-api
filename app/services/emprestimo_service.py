"""Regras de negócio relacionadas a Emprestimo."""

from sqlalchemy.orm import Session

from app.models.emprestimo import Emprestimo
from app.models.livro import Livro
from app.models.usuario import Usuario
from app.schemas import EmprestimoCreate


class EmprestimoIndisponivelError(Exception):
    """Lançada quando não é possível realizar um empréstimo."""


def realizar_emprestimo(db: Session, dados: EmprestimoCreate) -> Emprestimo:
    """Realiza um novo empréstimo, validando livro e usuário."""
    livro = db.query(Livro).filter(Livro.id == dados.livro_id).first()
    usuario = db.query(Usuario).filter(Usuario.id == dados.usuario_id).first()

    if not livro:
        raise EmprestimoIndisponivelError("Livro não encontrado.")
    if not usuario:
        raise EmprestimoIndisponivelError("Usuário não encontrado.")
    if not usuario.pode_emprestar():
        raise EmprestimoIndisponivelError("Usuário inativo não pode realizar empréstimos.")
    if not livro.reservar_copia():
        raise EmprestimoIndisponivelError("Não há cópias disponíveis deste livro.")

    emprestimo = Emprestimo(
        livro_id=livro.id,
        usuario_id=usuario.id,
        data_devolucao_prevista=Emprestimo.calcular_data_prevista(),
    )
    db.add(emprestimo)
    db.commit()
    db.refresh(emprestimo)
    return emprestimo


def devolver_emprestimo(db: Session, emprestimo_id: int) -> Emprestimo | None:
    """Processa a devolução de um empréstimo, liberando a cópia do livro."""
    emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if not emprestimo or emprestimo.devolvido:
        return None

    emprestimo.marcar_devolvido()
    livro = db.query(Livro).filter(Livro.id == emprestimo.livro_id).first()
    if livro:
        livro.devolver_copia()

    db.commit()
    db.refresh(emprestimo)
    return emprestimo


def listar_emprestimos(db: Session):
    """Retorna todos os empréstimos registrados."""
    return db.query(Emprestimo).all()


def listar_emprestimos_atrasados(db: Session):
    """Retorna os empréstimos que estão atrasados."""
    todos = listar_emprestimos(db)
    return [e for e in todos if e.esta_atrasado()]
