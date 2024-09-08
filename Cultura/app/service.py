from sqlmodel import Session, select
from app.models import Produto

class ProdutoService:
    def __init__(self, session: Session):
        self.session = session

    def criar_produto(self, produto: Produto):
        self.session.add(produto)
        self.session.commit()
        self.session.refresh(produto)
        return produto

    def listar_produtos(self, filtro_nome: str = None, filtro_categoria: str = None):
        query = select(Produto)
        if filtro_nome:
            query = query.where(Produto.nome == filtro_nome)
        if filtro_categoria:
            query = query.where(Produto.categoria == filtro_categoria)
        return self.session.exec(query).all()

    def atualizar_produto(self, produto_id: int, dados_atualizados: dict):
        produto = self.session.get(Produto, produto_id)
        if produto:
            for key, value in dados_atualizados.items():
                setattr(produto, key, value)
            self.session.commit()
            self.session.refresh(produto)
        return produto

    def excluir_produto(self, produto_id: int):
        produto = self.session.get(Produto, produto_id)
        if produto and produto.quantidade_estoque == 0:
            self.session.delete(produto)
            self.session.commit()
            return True
        return False
