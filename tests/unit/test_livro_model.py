"""Testes unitários do model Livro (sem banco de dados, lógica pura)."""

from app.models.livro import Livro


def test_livro_disponivel_quando_quantidade_maior_que_zero():
    livro = Livro(titulo="Clean Code", autor="Robert Martin", isbn="123", quantidade_disponivel=2)
    assert livro.esta_disponivel() is True


def test_livro_indisponivel_quando_quantidade_zero():
    livro = Livro(titulo="Clean Code", autor="Robert Martin", isbn="123", quantidade_disponivel=0)
    assert livro.esta_disponivel() is False


def test_reservar_copia_reduz_quantidade_disponivel():
    livro = Livro(titulo="Refactoring", autor="Fowler", isbn="456", quantidade_disponivel=3)
    sucesso = livro.reservar_copia()
    assert sucesso is True
    assert livro.quantidade_disponivel == 2


def test_reservar_copia_falha_quando_sem_estoque():
    livro = Livro(titulo="Refactoring", autor="Fowler", isbn="456", quantidade_disponivel=0)
    sucesso = livro.reservar_copia()
    assert sucesso is False
    assert livro.quantidade_disponivel == 0


def test_devolver_copia_incrementa_disponivel():
    livro = Livro(titulo="DDD", autor="Evans", isbn="789", quantidade_total=3, quantidade_disponivel=1)
    livro.devolver_copia()
    assert livro.quantidade_disponivel == 2


def test_devolver_copia_nao_excede_quantidade_total():
    livro = Livro(titulo="DDD", autor="Evans", isbn="789", quantidade_total=3, quantidade_disponivel=3)
    livro.devolver_copia()
    assert livro.quantidade_disponivel == 3
