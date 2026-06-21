"""Rotas da API relacionadas a Empréstimos."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EmprestimoCreate, EmprestimoResponse
from app.services import emprestimo_service
from app.services.emprestimo_service import EmprestimoIndisponivelError

router = APIRouter(prefix="/emprestimos", tags=["Emprestimos"])


@router.post("/", response_model=EmprestimoResponse, status_code=201)
def realizar_emprestimo(dados: EmprestimoCreate, db: Session = Depends(get_db)):
    try:
        return emprestimo_service.realizar_emprestimo(db, dados)
    except EmprestimoIndisponivelError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/", response_model=list[EmprestimoResponse])
def listar_emprestimos(db: Session = Depends(get_db)):
    return emprestimo_service.listar_emprestimos(db)


@router.get("/atrasados", response_model=list[EmprestimoResponse])
def listar_atrasados(db: Session = Depends(get_db)):
    return emprestimo_service.listar_emprestimos_atrasados(db)


@router.patch("/{emprestimo_id}/devolver", response_model=EmprestimoResponse)
def devolver_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    emprestimo = emprestimo_service.devolver_emprestimo(db, emprestimo_id)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado ou já devolvido.")
    return emprestimo
