"""Models de Pedido"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Order(Base):
    """
    Model de pedido representando compras de clientes.

    Suporta diferentes tipos de pedido:
    - regular: Entrega padrão
    - express: Entrega rápida
    - international: Envio internacional

    Métodos de pagamento:
    - credit_card: Pagamento com cartão de crédito
    - pix: Pagamento instantâneo PIX
    - boleto: Pagamento com boleto bancário
    """

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    type = Column(String(50), nullable=False)  # regular, express, international
    status = Column(String(50), nullable=False, default="pending")
    # Fluxo de status: pending -> confirmed -> shipped -> delivered (ou cancelled)
    payment_method = Column(String(50), nullable=False)  # credit_card, pix, boleto
    subtotal = Column(Float, nullable=False, default=0.0)
    extras_cost = Column(Float, nullable=False, default=0.0)  # Vindo dos decorators
    total = Column(Float, nullable=False, default=0.0)
    has_gift_wrap = Column(Boolean, default=False)
    has_insurance = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    history = relationship("OrderHistory", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, customer_id={self.customer_id}, type='{self.type}', status='{self.status}', total={self.total})>"


class OrderItem(Base):
    """Model de item de pedido representando produtos em um pedido."""

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    # Relacionamentos
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    def __repr__(self) -> str:
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"


class OrderHistory(Base):
    """Model de histórico de pedido para rastrear mudanças de status."""

    __tablename__ = "order_history"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    status = Column(String(50), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    order = relationship("Order", back_populates="history")

    def __repr__(self) -> str:
        return f"<OrderHistory(id={self.id}, order_id={self.order_id}, status='{self.status}')>"
