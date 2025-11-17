"""Schemas Pydantic para validação"""

from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from app.schemas.customer_schema import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)
from app.schemas.order_schema import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
    OrderSummary,
    OrderItemResponse,
    OrderHistoryResponse,
)

__all__ = [
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    "OrderCreate",
    "OrderResponse",
    "OrderStatusUpdate",
    "OrderSummary",
    "OrderItemResponse",
    "OrderHistoryResponse",
]
