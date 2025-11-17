"""Repositório de Produtos"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Repositório de produtos com métodos de consulta específicos.

    Estende BaseRepository para adicionar consultas específicas de produtos.
    """

    def __init__(self, session: Session):
        """Inicializa com o model Product."""
        super().__init__(Product, session)

    def get_by_type(self, product_type: str) -> List[Product]:
        """
        Obtém todos os produtos de um tipo específico.

        Args:
            product_type: Tipo de produto (physical, digital, subscription)

        Returns:
            List[Product]: Lista de produtos
        """
        return self.session.query(Product).filter(Product.type == product_type).all()

    def get_in_stock(self) -> List[Product]:
        """
        Obtém todos os produtos que estão em estoque.

        Returns:
            List[Product]: Lista de produtos com estoque > 0
        """
        return self.session.query(Product).filter(Product.stock > 0).all()

    def update_stock(self, product_id: int, quantity_change: int) -> Optional[Product]:
        """
        Atualiza o estoque do produto.

        Args:
            product_id: ID do produto
            quantity_change: Mudança na quantidade (positiva ou negativa)

        Returns:
            Optional[Product]: Produto atualizado ou None se não encontrado
        """
        product = self.get_by_id(product_id)
        if product:
            product.stock += quantity_change
            return self.update(product)
        return None

    def search_by_name(self, name: str) -> List[Product]:
        """
        Busca produtos por nome (busca parcial, case-insensitive).

        Args:
            name: Nome do produto para buscar

        Returns:
            List[Product]: Lista de produtos correspondentes
        """
        return self.session.query(Product).filter(
            Product.name.ilike(f"%{name}%")
        ).all()
