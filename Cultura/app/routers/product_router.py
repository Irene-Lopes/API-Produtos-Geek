from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.models import Produto
from app.services import ProdutoService
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=Produto)
def criar_produto(produto: Produto, session: Session = Depends(get_session)):
    service = ProdutoService(session)
    return service.criar_produto(produto)

@router.get("/", response_model=list[Produto])
def listar_produtos(nome: str = None, categoria: str = None, session: Session = Depends(get_session)):
    service = ProdutoService(session)
    return service.listar_produtos(filtro_nome=nome, filtro_categoria=categoria)

@router.put("/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, produto: Produto, session: Session = Depends(get_session)):
    service = ProdutoService(session)
    produto_atualizado = service.atualizar_produto(produto_id, produto.dict())
    if not produto_atualizado:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto_atualizado

@router.delete("/{produto_id}")
def excluir_produto(produto_id: int, session: Session = Depends(get_session)):
    service = ProdutoService(session)
    if not service.excluir_produto(produto_id):
        raise HTTPException(status_code=400, detail="Produto com estoque disponível ou não encontrado")
    return {"detail": "Produto excluído com sucesso"}



