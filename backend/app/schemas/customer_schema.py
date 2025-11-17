"""Schemas Pydantic para Cliente"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    """Schema base para cliente."""

    name: str = Field(..., min_length=1, max_length=200, description="Nome do cliente")
    email: EmailStr = Field(..., description="Email do cliente")
    phone: str = Field(..., min_length=10, max_length=20, description="Telefone do cliente")
    address: str = Field(..., min_length=5, max_length=500, description="Endereço do cliente")


class CustomerCreate(CustomerBase):
    """Schema para criar cliente."""
    pass


class CustomerUpdate(BaseModel):
    """Schema para atualizar cliente."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    address: Optional[str] = Field(None, min_length=5, max_length=500)


class CustomerResponse(CustomerBase):
    """Schema para resposta de cliente."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True
