"""Model de Produto"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    """
    Model de produto representando itens disponíveis para compra.

    Suporta diferentes tipos de produto:
    - physical: Produtos que precisam de envio
    - digital: Produtos para download
    - subscription: Produtos de serviço recorrente
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Float, nullable=False)
    type = Column(String(50), nullable=False)  # physical, digital, subscription
    stock = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', type='{self.type}', price={self.price})>"
