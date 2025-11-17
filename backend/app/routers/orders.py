"""
Router de Pedidos - Demonstra Integração de Todos os Padrões

Este router usa o OrderService que integra:
- Factory Method: Para criar diferentes tipos de pedidos
- Strategy: Para processar pagamentos
- Decorator: Para adicionar extras
- Observer: Para notificar mudanças de status
- Repository: Para persistir dados
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db_session
from app.services.order_service import OrderService
from app.schemas.order_schema import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
    OrderSummary
)

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    session: Session = Depends(get_db_session)
):
    """
    Cria um novo pedido usando TODOS os padrões de projeto integrados.

    Padrões aplicados:
    - Factory Method: Cria tipo correto de pedido (regular/express/international)
    - Strategy: Processa pagamento com método selecionado (cartão/pix/boleto)
    - Decorator: Adiciona extras (embalagem/seguro) dinamicamente
    - Observer: Notifica clientes via email/sms/log sobre criação
    - Repository: Persiste dados no banco

    Args:
        order_data: Dados do pedido
        session: Sessão do banco de dados

    Returns:
        OrderResponse: Pedido criado

    Raises:
        HTTPException: Se erro na criação
    """
    try:
        service = OrderService(session)
        order = service.create_order(order_data)
        return order

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar pedido: {str(e)}"
        )


@router.get("/", response_model=List[OrderResponse])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_db_session)
):
    """
    Lista todos os pedidos com paginação.

    Args:
        skip: Número de pedidos para pular
        limit: Número máximo de pedidos para retornar
        session: Sessão do banco de dados

    Returns:
        List[OrderResponse]: Lista de pedidos
    """
    service = OrderService(session)
    orders = service.get_all_orders(skip, limit)
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    session: Session = Depends(get_db_session)
):
    """
    Obtém um pedido por ID com todos os detalhes.

    Args:
        order_id: ID do pedido
        session: Sessão do banco de dados

    Returns:
        OrderResponse: Dados completos do pedido

    Raises:
        HTTPException: Se pedido não encontrado
    """
    try:
        service = OrderService(session)
        order = service.get_order_by_id(order_id)
        return order

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/customer/{customer_id}", response_model=List[OrderResponse])
def get_customer_orders(
    customer_id: int,
    session: Session = Depends(get_db_session)
):
    """
    Obtém todos os pedidos de um cliente.

    Args:
        customer_id: ID do cliente
        session: Sessão do banco de dados

    Returns:
        List[OrderResponse]: Lista de pedidos do cliente
    """
    service = OrderService(session)
    orders = service.get_orders_by_customer(customer_id)
    return orders


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    session: Session = Depends(get_db_session)
):
    """
    Atualiza o status do pedido e DISPARA NOTIFICAÇÕES (Observer Pattern).

    Quando o status é atualizado, todos os observadores registrados
    (EmailNotifier, SmsNotifier, LogNotifier) são automaticamente notificados.

    Args:
        order_id: ID do pedido
        status_data: Novo status e nota opcional
        session: Sessão do banco de dados

    Returns:
        OrderResponse: Pedido atualizado

    Raises:
        HTTPException: Se pedido não encontrado
    """
    try:
        service = OrderService(session)
        order = service.update_order_status(
            order_id,
            status_data.status,
            status_data.note
        )
        return order

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar status: {str(e)}"
        )
