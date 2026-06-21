"""Model da entidade Usuario."""

from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class Usuario(Base):
    """Representa um usuário cadastrado na biblioteca."""

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    ativo = Column(Boolean, default=True, nullable=False)

    def desativar(self) -> None:
        """Desativa o usuário, impedindo novos empréstimos."""
        self.ativo = False

    def ativar(self) -> None:
        """Reativa o usuário."""
        self.ativo = True

    def pode_emprestar(self) -> bool:
        """Verifica se o usuário está apto a realizar um novo empréstimo."""
        return self.ativo
