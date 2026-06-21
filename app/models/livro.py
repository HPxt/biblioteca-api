"""Model da entidade Livro."""

from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class Livro(Base):
    """Representa um livro disponível na biblioteca."""

    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False, index=True)
    autor = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    quantidade_total = Column(Integer, default=1, nullable=False)
    quantidade_disponivel = Column(Integer, default=1, nullable=False)

    def esta_disponivel(self) -> bool:
        """Verifica se há ao menos uma cópia disponível para empréstimo."""
        return self.quantidade_disponivel > 0

    def reservar_copia(self) -> bool:
        """Reduz a quantidade disponível em 1, se houver cópias livres."""
        if not self.esta_disponivel():
            return False
        self.quantidade_disponivel -= 1
        return True

    def devolver_copia(self) -> None:
        """Incrementa a quantidade disponível, respeitando o limite total."""
        if self.quantidade_disponivel < self.quantidade_total:
            self.quantidade_disponivel += 1
