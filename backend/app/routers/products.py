"""Router de Produtos"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db_session
from app.repositories.product_repository import ProductRepository
from app.factories.product_factory import ProductFactory
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    product_type: str = None,
    session: Session = Depends(get_db_session)
):
    """
    Lista todos os produtos com paginação opcional.

    Args:
        skip: Número de produtos para pular
        limit: Número máximo de produtos para retornar
        product_type: Filtro por tipo de produto (opcional)
        session: Sessão do banco de dados

    Returns:
        List[ProductResponse]: Lista de produtos
    """
    repo = ProductRepository(session)

    if product_type:
        products = repo.get_by_type(product_type)
    else:
        products = repo.get_all(skip, limit)

    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    session: Session = Depends(get_db_session)
):
    """
    Obtém um produto por ID.

    Args:
        product_id: ID do produto
        session: Sessão do banco de dados

    Returns:
        ProductResponse: Dados do produto

    Raises:
        HTTPException: Se produto não encontrado
    """
    repo = ProductRepository(session)
    product = repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto {product_id} não encontrado"
        )

    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    session: Session = Depends(get_db_session)
):
    """
    Cria um novo produto usando Factory Method Pattern.

    Args:
        product_data: Dados do produto
        session: Sessão do banco de dados

    Returns:
        ProductResponse: Produto criado

    Raises:
        HTTPException: Se erro na criação
    """
    try:
        # Usa Factory Method para criar produto do tipo correto
        product = ProductFactory.create_product(
            product_type=product_data.type,
            product_data=product_data.model_dump()
        )

        repo = ProductRepository(session)
        created_product = repo.create(product)

        return created_product

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    session: Session = Depends(get_db_session)
):
    """
    Atualiza um produto existente.

    Args:
        product_id: ID do produto
        product_data: Dados para atualizar
        session: Sessão do banco de dados

    Returns:
        ProductResponse: Produto atualizado

    Raises:
        HTTPException: Se produto não encontrado
    """
    repo = ProductRepository(session)
    product = repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto {product_id} não encontrado"
        )

    # Atualiza apenas campos fornecidos
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    updated_product = repo.update(product)
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    session: Session = Depends(get_db_session)
):
    """
    Deleta um produto.

    Args:
        product_id: ID do produto
        session: Sessão do banco de dados

    Raises:
        HTTPException: Se produto não encontrado
    """
    repo = ProductRepository(session)
    deleted = repo.delete(product_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto {product_id} não encontrado"
        )

    return None
