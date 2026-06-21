"""Testes unitários do model Emprestimo."""

from datetime import datetime, timedelta

from app.models.emprestimo import Emprestimo, PRAZO_EMPRESTIMO_DIAS


def test_calcular_data_prevista_soma_prazo_padrao():
    data_inicio = datetime(2026, 1, 1)
    data_prevista = Emprestimo.calcular_data_prevista(data_inicio)
    assert data_prevista == data_inicio + timedelta(days=PRAZO_EMPRESTIMO_DIAS)


def test_marcar_devolvido_atualiza_status_e_data():
    emprestimo = Emprestimo(devolvido=False)
    emprestimo.marcar_devolvido()
    assert emprestimo.devolvido is True
    assert emprestimo.data_devolucao_real is not None


def test_esta_atrasado_quando_prazo_vencido_e_nao_devolvido():
    emprestimo = Emprestimo(
        devolvido=False,
        data_devolucao_prevista=datetime.utcnow() - timedelta(days=1),
    )
    assert emprestimo.esta_atrasado() is True


def test_nao_esta_atrasado_quando_ja_devolvido():
    emprestimo = Emprestimo(
        devolvido=True,
        data_devolucao_prevista=datetime.utcnow() - timedelta(days=1),
    )
    assert emprestimo.esta_atrasado() is False


def test_nao_esta_atrasado_quando_dentro_do_prazo():
    emprestimo = Emprestimo(
        devolvido=False,
        data_devolucao_prevista=datetime.utcnow() + timedelta(days=1),
    )
    assert emprestimo.esta_atrasado() is False
