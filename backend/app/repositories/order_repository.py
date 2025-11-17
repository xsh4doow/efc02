"""Repositório de Pedidos"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.order import Order, OrderItem, OrderHistory
from app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repositório de pedidos com métodos de consulta específicos.

    Estende BaseRepository para adicionar consultas específicas de pedidos.
    """

    def __init__(self, session: Session):
        """Inicializa com o model Order."""
        super().__init__(Order, session)

    def get_all_with_details(self) -> List[Order]:
        """
        Obtém todos os pedidos com relacionamentos carregados.

        Returns:
            List[Order]: Lista de pedidos com relacionamentos
        """
        return self.session.query(Order).options(
            joinedload(Order.customer),
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.history)
        ).order_by(Order.created_at.desc()).all()

    def get_by_id_with_details(self, order_id: int) -> Optional[Order]:
        """
        Obtém pedido com todos os dados relacionados (cliente, itens, histórico).

        Args:
            order_id: ID do pedido

        Returns:
            Optional[Order]: Pedido com relacionamentos carregados
        """
        return self.session.query(Order).options(
            joinedload(Order.customer),
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.history)
        ).filter(Order.id == order_id).first()

    def get_by_customer(self, customer_id: int) -> List[Order]:
        """
        Obtém todos os pedidos de um cliente específico com relacionamentos.

        Args:
            customer_id: ID do cliente

        Returns:
            List[Order]: Lista de pedidos do cliente
        """
        return self.session.query(Order).options(
            joinedload(Order.customer),
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.history)
        ).filter(
            Order.customer_id == customer_id
        ).order_by(Order.created_at.desc()).all()

    def get_by_status(self, status: str) -> List[Order]:
        """
        Obtém todos os pedidos com um status específico.

        Args:
            status: Status do pedido

        Returns:
            List[Order]: Lista de pedidos
        """
        return self.session.query(Order).filter(Order.status == status).all()

    def update_status(self, order_id: int, new_status: str, note: str = None) -> Optional[Order]:
        """
        Atualiza o status do pedido e cria registro no histórico.

        Args:
            order_id: ID do pedido
            new_status: Novo status
            note: Nota opcional sobre a mudança de status

        Returns:
            Optional[Order]: Pedido atualizado ou None se não encontrado
        """
        order = self.get_by_id(order_id)
        if order:
            order.status = new_status

            # Cria registro no histórico
            history = OrderHistory(
                order_id=order_id,
                status=new_status,
                note=note
            )
            self.session.add(history)

            self.session.commit()
            self.session.refresh(order)
            return order
        return None

    def create_with_items(self, order: Order, items: List[dict]) -> Order:
        """
        Cria pedido com itens em uma única transação.

        Args:
            order: Instância do pedido
            items: Lista de dicionários de itens com product_id, quantity, unit_price

        Returns:
            Order: Pedido criado com itens
        """
        # Adiciona pedido
        self.session.add(order)
        self.session.flush()  # Obtém o ID do pedido sem fazer commit

        # Adiciona itens
        for item_data in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                total=item_data['quantity'] * item_data['unit_price']
            )
            self.session.add(order_item)

        # Cria histórico inicial
        history = OrderHistory(
            order_id=order.id,
            status=order.status,
            note="Pedido criado"
        )
        self.session.add(history)

        self.session.commit()
        self.session.refresh(order)
        return order
