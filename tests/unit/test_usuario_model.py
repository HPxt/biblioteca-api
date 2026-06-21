"""Testes unitários do model Usuario."""

from app.models.usuario import Usuario


def test_usuario_ativo_pode_emprestar():
    usuario = Usuario(nome="Ana", email="ana@example.com", ativo=True)
    assert usuario.pode_emprestar() is True


def test_usuario_inativo_nao_pode_emprestar():
    usuario = Usuario(nome="Ana", email="ana@example.com", ativo=False)
    assert usuario.pode_emprestar() is False


def test_desativar_usuario():
    usuario = Usuario(nome="Ana", email="ana@example.com", ativo=True)
    usuario.desativar()
    assert usuario.ativo is False


def test_ativar_usuario():
    usuario = Usuario(nome="Ana", email="ana@example.com", ativo=False)
    usuario.ativar()
    assert usuario.ativo is True
