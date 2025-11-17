"""Router de Clientes"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db_session
from app.repositories.customer_repository import CustomerRepository
from app.models.customer import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerResponse, CustomerUpdate

router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.get("/", response_model=List[CustomerResponse])
def list_customers(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_db_session)
):
    """
    Lista todos os clientes com paginação.

    Args:
        skip: Número de clientes para pular
        limit: Número máximo de clientes para retornar
        session: Sessão do banco de dados

    Returns:
        List[CustomerResponse]: Lista de clientes
    """
    repo = CustomerRepository(session)
    customers = repo.get_all(skip, limit)
    return customers


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    session: Session = Depends(get_db_session)
):
    """
    Obtém um cliente por ID.

    Args:
        customer_id: ID do cliente
        session: Sessão do banco de dados

    Returns:
        CustomerResponse: Dados do cliente

    Raises:
        HTTPException: Se cliente não encontrado
    """
    repo = CustomerRepository(session)
    customer = repo.get_by_id(customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente {customer_id} não encontrado"
        )

    return customer


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_data: CustomerCreate,
    session: Session = Depends(get_db_session)
):
    """
    Cria um novo cliente.

    Args:
        customer_data: Dados do cliente
        session: Sessão do banco de dados

    Returns:
        CustomerResponse: Cliente criado

    Raises:
        HTTPException: Se email já existe
    """
    repo = CustomerRepository(session)

    # Verifica se email já existe
    if repo.email_exists(customer_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {customer_data.email} já cadastrado"
        )

    customer = Customer(**customer_data.model_dump())
    created_customer = repo.create(customer)

    return created_customer


@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    session: Session = Depends(get_db_session)
):
    """
    Atualiza um cliente existente.

    Args:
        customer_id: ID do cliente
        customer_data: Dados para atualizar
        session: Sessão do banco de dados

    Returns:
        CustomerResponse: Cliente atualizado

    Raises:
        HTTPException: Se cliente não encontrado
    """
    repo = CustomerRepository(session)
    customer = repo.get_by_id(customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente {customer_id} não encontrado"
        )

    # Atualiza apenas campos fornecidos
    update_data = customer_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    updated_customer = repo.update(customer)
    return updated_customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    session: Session = Depends(get_db_session)
):
    """
    Deleta um cliente.

    Args:
        customer_id: ID do cliente
        session: Sessão do banco de dados

    Raises:
        HTTPException: Se cliente não encontrado
    """
    repo = CustomerRepository(session)
    deleted = repo.delete(customer_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente {customer_id} não encontrado"
        )

    return None
