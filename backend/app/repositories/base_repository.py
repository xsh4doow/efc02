"""
Repositório Base - Implementação do Padrão Repository

PADRÃO DE PROJETO: Repository
PROPÓSITO: Abstrair lógica de acesso a dados da lógica de negócio
BENEFÍCIO: Centraliza operações de banco de dados, facilita testes e permite
           trocar o banco de dados facilmente sem alterar a lógica de negócio
"""

from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from app.database import Base

# Tipo genérico para classes de model
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Repositório base genérico fornecendo operações CRUD comuns.

    Este padrão separa a lógica de acesso a dados da lógica de negócio,
    tornando o código mais manutenível e testável.

    Parâmetros de Tipo:
        ModelType: A classe model do SQLAlchemy
    """

    def __init__(self, model: Type[ModelType], session: Session):
        """
        Inicializa repositório com model e sessão do banco de dados.

        Args:
            model: Classe model do SQLAlchemy
            session: Sessão do banco de dados
        """
        self.model = model
        self.session = session

    def create(self, obj: ModelType) -> ModelType:
        """
        Cria um novo registro no banco de dados.

        Args:
            obj: Instância do model para criar

        Returns:
            ModelType: Instância do model criada com ID
        """
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Obtém um registro pelo seu ID.

        Args:
            id: ID do registro

        Returns:
            Optional[ModelType]: Instância do model ou None se não encontrado
        """
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Obtém todos os registros com paginação.

        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar

        Returns:
            List[ModelType]: Lista de instâncias do model
        """
        return self.session.query(self.model).offset(skip).limit(limit).all()

    def update(self, obj: ModelType) -> ModelType:
        """
        Atualiza um registro existente.

        Args:
            obj: Instância do model com valores atualizados

        Returns:
            ModelType: Instância do model atualizada
        """
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        """
        Deleta um registro pelo seu ID.

        Args:
            id: ID do registro

        Returns:
            bool: True se deletado, False se não encontrado
        """
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return True
        return False

    def count(self) -> int:
        """
        Conta o número total de registros.

        Returns:
            int: Total de registros
        """
        return self.session.query(self.model).count()
