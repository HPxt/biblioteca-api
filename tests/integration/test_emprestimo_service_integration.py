"""Testes de integração do fluxo completo de empréstimo, envolvendo Livro, Usuario e Emprestimo."""

import pytest

from app.schemas import LivroCreate, UsuarioCreate, EmprestimoCreate
from app.services import livro_service, usuario_service, emprestimo_service
from app.services.emprestimo_service import EmprestimoIndisponivelError


def _criar_livro_e_usuario(db_session, quantidade_total=1):
    livro = livro_service.criar_livro(
        db_session, LivroCreate(titulo="1984", autor="Orwell", isbn="9780451524935", quantidade_total=quantidade_total)
    )
    usuario = usuario_service.criar_usuario(
        db_session, UsuarioCreate(nome="Carlos", email="carlos@example.com")
    )
    return livro, usuario


def test_realizar_emprestimo_com_sucesso_reduz_estoque(db_session):
    livro, usuario = _criar_livro_e_usuario(db_session, quantidade_total=1)

    emprestimo = emprestimo_service.realizar_emprestimo(
        db_session, EmprestimoCreate(livro_id=livro.id, usuario_id=usuario.id)
    )

    livro_atualizado = livro_service.buscar_livro_por_id(db_session, livro.id)
    assert emprestimo.id is not None
    assert livro_atualizado.quantidade_disponivel == 0


def test_emprestimo_falha_quando_sem_copias_disponiveis(db_session):
    livro, usuario = _criar_livro_e_usuario(db_session, quantidade_total=1)
    emprestimo_service.realizar_emprestimo(db_session, EmprestimoCreate(livro_id=livro.id, usuario_id=usuario.id))

    with pytest.raises(EmprestimoIndisponivelError):
        emprestimo_service.realizar_emprestimo(db_session, EmprestimoCreate(livro_id=livro.id, usuario_id=usuario.id))


def test_emprestimo_falha_para_usuario_inativo(db_session):
    livro, usuario = _criar_livro_e_usuario(db_session, quantidade_total=1)
    usuario_service.desativar_usuario(db_session, usuario.id)

    with pytest.raises(EmprestimoIndisponivelError):
        emprestimo_service.realizar_emprestimo(db_session, EmprestimoCreate(livro_id=livro.id, usuario_id=usuario.id))


def test_devolver_emprestimo_libera_copia_do_livro(db_session):
    livro, usuario = _criar_livro_e_usuario(db_session, quantidade_total=1)
    emprestimo = emprestimo_service.realizar_emprestimo(
        db_session, EmprestimoCreate(livro_id=livro.id, usuario_id=usuario.id)
    )

    devolvido = emprestimo_service.devolver_emprestimo(db_session, emprestimo.id)
    livro_atualizado = livro_service.buscar_livro_por_id(db_session, livro.id)

    assert devolvido.devolvido is True
    assert livro_atualizado.quantidade_disponivel == 1
