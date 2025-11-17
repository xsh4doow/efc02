"""Schemas Pydantic para Pedido"""

from pydantic import BaseModel, Field, field_validator, computed_field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime


class OrderItemCreate(BaseModel):
    """Schema para criar item de pedido."""

    product_id: int = Field(..., gt=0, description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade")


class CustomerSimple(BaseModel):
    """Schema simples para cliente em resposta de pedido."""
    id: int
    name: str
    email: str
    phone: str
    address: str

    class Config:
        from_attributes = True


class ProductSimple(BaseModel):
    """Schema simples para produto em resposta de pedido."""
    id: int
    name: str
    price: float
    type: str

    class Config:
        from_attributes = True


class OrderItemResponse(BaseModel):
    """Schema para resposta de item de pedido."""

    id: int
    product_id: int
    quantity: int
    unit_price: float
    total: float
    product: Optional[ProductSimple] = None  # Produto relacionado

    @computed_field
    @property
    def price(self) -> float:
        """Alias para unit_price para compatibilidade frontend."""
        return self.unit_price

    class Config:
        from_attributes = True


class OrderExtras(BaseModel):
    """Schema para extras do pedido."""

    gift_wrap: bool = Field(default=False, description="Embalagem presente")
    gift_message: Optional[str] = Field(default=None, max_length=500, description="Mensagem do cartão")
    insurance: bool = Field(default=False, description="Seguro")
    insurance_type: Optional[str] = Field(default="standard", description="Tipo de seguro (standard, premium)")

    @field_validator('insurance_type')
    @classmethod
    def validate_insurance_type(cls, v, info):
        """Valida tipo de seguro."""
        if info.data.get('insurance') and v not in ['standard', 'premium']:
            raise ValueError('Tipo de seguro deve ser "standard" ou "premium"')
        return v


class CustomerData(BaseModel):
    """Schema para dados do cliente no pedido."""

    name: str = Field(..., min_length=1, max_length=200)
    email: str = Field(..., description="Email do cliente")
    phone: str = Field(..., min_length=10, max_length=20)
    address: str = Field(..., min_length=5, max_length=500)


class OrderCreate(BaseModel):
    """Schema para criar pedido."""

    customer: CustomerData = Field(..., description="Dados do cliente")
    order_type: str = Field(..., description="Tipo do pedido (regular, express, international)")
    payment_method: str = Field(..., description="Método de pagamento (credit_card, pix, boleto)")
    items: List[OrderItemCreate] = Field(..., min_length=1, description="Itens do pedido")
    extras: OrderExtras = Field(default_factory=OrderExtras, description="Extras do pedido")

    @field_validator('order_type')
    @classmethod
    def validate_order_type(cls, v):
        """Valida tipo do pedido."""
        allowed_types = ['regular', 'express', 'international']
        if v.lower() not in allowed_types:
            raise ValueError(f'Tipo de pedido deve ser um de: {", ".join(allowed_types)}')
        return v.lower()

    @field_validator('payment_method')
    @classmethod
    def validate_payment_method(cls, v):
        """Valida método de pagamento."""
        allowed_methods = ['credit_card', 'pix', 'boleto']
        if v.lower() not in allowed_methods:
            raise ValueError(f'Método de pagamento deve ser um de: {", ".join(allowed_methods)}')
        return v.lower()


class OrderHistoryResponse(BaseModel):
    """Schema para resposta de histórico de pedido."""

    id: int
    status: str
    note: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Schema para resposta de pedido."""

    id: int
    customer_id: int
    customer: Optional[CustomerSimple] = None  # Cliente relacionado
    type: str
    status: str
    payment_method: str
    subtotal: float
    extras_cost: float = 0.0
    total: float
    has_gift_wrap: bool = False
    has_insurance: bool = False
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []
    history: List[OrderHistoryResponse] = []

    # Adiciona order_type como alias para type
    @computed_field
    @property
    def order_type(self) -> str:
        """Alias para type para compatibilidade frontend."""
        return self.type

    # Adiciona total_amount como computed field
    @computed_field
    @property
    def total_amount(self) -> float:
        """Alias para total para compatibilidade frontend."""
        return self.total

    # Adiciona shipping_cost como computed field (calculado do extras_cost ou 0)
    @computed_field
    @property
    def shipping_cost(self) -> float:
        """Custo de envio para compatibilidade frontend."""
        return 0.0  # Pode ser calculado baseado no tipo de pedido se necessário

    # Campos JSON opcionais
    @computed_field
    @property
    def extras_details(self) -> Optional[Dict[str, Any]]:
        """Detalhes dos extras do pedido."""
        details = {}
        if self.has_gift_wrap:
            details['gift_wrap'] = True
        if self.has_insurance:
            details['insurance'] = True
        return details if details else None

    @computed_field
    @property
    def payment_details(self) -> Optional[Dict[str, Any]]:
        """Detalhes do pagamento."""
        return {
            'method': self.payment_method
        }

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Schema para atualizar status do pedido."""

    status: str = Field(..., description="Novo status")
    note: Optional[str] = Field(default=None, max_length=1000, description="Nota sobre a mudança")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        """Valida status do pedido."""
        allowed_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        if v.lower() not in allowed_statuses:
            raise ValueError(f'Status deve ser um de: {", ".join(allowed_statuses)}')
        return v.lower()


class OrderSummary(BaseModel):
    """Schema para resumo do pedido."""

    order_id: int
    total: float
    status: str
    created_at: datetime
    items_count: int
