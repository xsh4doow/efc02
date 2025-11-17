"""Schemas Pydantic para Produto"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    """Schema base para produto."""

    name: str = Field(..., min_length=1, max_length=200, description="Nome do produto")
    description: str = Field(..., min_length=1, max_length=1000, description="Descrição do produto")
    price: float = Field(..., gt=0, description="Preço do produto (deve ser maior que 0)")
    type: str = Field(..., description="Tipo do produto (physical, digital, subscription)")
    stock: int = Field(default=0, ge=0, description="Quantidade em estoque")

    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        """Valida tipo do produto."""
        allowed_types = ['physical', 'digital', 'subscription']
        if v.lower() not in allowed_types:
            raise ValueError(f'Tipo deve ser um de: {", ".join(allowed_types)}')
        return v.lower()


class ProductCreate(ProductBase):
    """Schema para criar produto."""
    pass


class ProductUpdate(BaseModel):
    """Schema para atualizar produto."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    """Schema para resposta de produto."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Permite criação a partir de ORM models
