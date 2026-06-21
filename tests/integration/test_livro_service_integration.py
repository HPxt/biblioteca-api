"""Testes de integração entre livro_service e o banco de dados."""

from app.schemas import LivroCreate
from app.services import livro_service


def test_criar_e_buscar_livro(db_session):
    dados = LivroCreate(titulo="Pragmatic Programmer", autor="Hunt e Thomas", isbn="9780201485677", quantidade_total=2)
    livro_criado = livro_service.criar_livro(db_session, dados)

    livro_encontrado = livro_service.buscar_livro_por_id(db_session, livro_criado.id)

    assert livro_encontrado is not None
    assert livro_encontrado.titulo == "Pragmatic Programmer"
    assert livro_encontrado.quantidade_disponivel == 2


def test_listar_livros_retorna_todos_cadastrados(db_session):
    livro_service.criar_livro(db_session, LivroCreate(titulo="Livro A", autor="Autor A", isbn="9780000000001"))
    livro_service.criar_livro(db_session, LivroCreate(titulo="Livro B", autor="Autor B", isbn="9780000000002"))

    livros = livro_service.listar_livros(db_session)

    assert len(livros) == 2


def test_remover_livro_existente(db_session):
    livro = livro_service.criar_livro(db_session, LivroCreate(titulo="Livro C", autor="Autor C", isbn="9780000000003"))

    removido = livro_service.remover_livro(db_session, livro.id)

    assert removido is True
    assert livro_service.buscar_livro_por_id(db_session, livro.id) is None


def test_remover_livro_inexistente_retorna_false(db_session):
    removido = livro_service.remover_livro(db_session, 9999)
    assert removido is False
