"""Repositório de Clientes"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """
    Repositório de clientes com métodos de consulta específicos.

    Estende BaseRepository para adicionar consultas específicas de clientes.
    """

    def __init__(self, session: Session):
        """Inicializa com o model Customer."""
        super().__init__(Customer, session)

    def get_by_email(self, email: str) -> Optional[Customer]:
        """
        Obtém cliente por endereço de email.

        Args:
            email: Email do cliente

        Returns:
            Optional[Customer]: Instância do cliente ou None se não encontrado
        """
        return self.session.query(Customer).filter(Customer.email == email).first()

    def email_exists(self, email: str) -> bool:
        """
        Verifica se o email já existe.

        Args:
            email: Email para verificar

        Returns:
            bool: True se o email existe, False caso contrário
        """
        return self.session.query(Customer).filter(Customer.email == email).count() > 0
