"""Model da entidade Emprestimo."""

from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean

from app.database import Base

PRAZO_EMPRESTIMO_DIAS = 14


class Emprestimo(Base):
    """Representa o empréstimo de um livro para um usuário."""

    __tablename__ = "emprestimos"

    id = Column(Integer, primary_key=True, index=True)
    livro_id = Column(Integer, ForeignKey("livros.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    data_emprestimo = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_devolucao_prevista = Column(DateTime, nullable=False)
    data_devolucao_real = Column(DateTime, nullable=True)
    devolvido = Column(Boolean, default=False, nullable=False)

    @staticmethod
    def calcular_data_prevista(data_inicio: datetime = None) -> datetime:
        """Calcula a data prevista de devolução a partir da data de início."""
        if data_inicio is None:
            data_inicio = datetime.utcnow()
        return data_inicio + timedelta(days=PRAZO_EMPRESTIMO_DIAS)

    def marcar_devolvido(self) -> None:
        """Marca o empréstimo como devolvido, registrando a data real."""
        self.devolvido = True
        self.data_devolucao_real = datetime.utcnow()

    def esta_atrasado(self) -> bool:
        """Verifica se o empréstimo está atrasado (não devolvido após o prazo)."""
        if self.devolvido:
            return False
        return datetime.utcnow() > self.data_devolucao_prevista
