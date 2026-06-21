"""Schemas Pydantic usados para validação de entrada/saída da API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ---------- Livro ----------

class LivroBase(BaseModel):
    titulo: str = Field(..., min_length=1)
    autor: str = Field(..., min_length=1)
    isbn: str = Field(..., min_length=10)
    quantidade_total: int = Field(default=1, ge=1)


class LivroCreate(LivroBase):
    pass


class LivroResponse(LivroBase):
    id: int
    quantidade_disponivel: int

    class Config:
        orm_mode = True


# ---------- Usuario ----------

class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=1)
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
    id: int
    ativo: bool

    class Config:
        orm_mode = True


# ---------- Emprestimo ----------

class EmprestimoCreate(BaseModel):
    livro_id: int
    usuario_id: int


class EmprestimoResponse(BaseModel):
    id: int
    livro_id: int
    usuario_id: int
    data_emprestimo: datetime
    data_devolucao_prevista: datetime
    data_devolucao_real: Optional[datetime]
    devolvido: bool

    class Config:
        orm_mode = True
