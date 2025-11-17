"""Serviço de Pedidos - Integra Todos os Padrões de Projeto"""

from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.customer import Customer
from app.repositories.order_repository import OrderRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.product_repository import ProductRepository
from app.factories.order_factory import OrderFactory
from app.strategies.payment_strategy import PaymentStrategy
from app.strategies.credit_card_payment import CreditCardPayment
from app.strategies.pix_payment import PixPayment
from app.strategies.boleto_payment import BoletoPayment
from app.decorators.order_decorator import BaseOrder
from app.decorators.gift_wrap_decorator import GiftWrapDecorator
from app.decorators.insurance_decorator import InsuranceDecorator
from app.services.notification_service import NotificationService
from app.schemas.order_schema import OrderCreate


class OrderService:
    """
    Serviço de pedidos que orquestra todos os padrões de projeto.

    Este serviço demonstra a integração natural de múltiplos padrões:
    - Factory Method: Cria diferentes tipos de pedidos
    - Strategy: Processa pagamentos com diferentes métodos
    - Decorator: Adiciona extras ao pedido
    - Observer: Notifica sobre mudanças de status
    - Repository: Persiste e recupera dados
    """

    def __init__(self, session: Session):
        """
        Inicializa serviço com sessão do banco de dados.

        Args:
            session: Sessão do SQLAlchemy
        """
        self.session = session
        self.order_repo = OrderRepository(session)
        self.customer_repo = CustomerRepository(session)
        self.product_repo = ProductRepository(session)
        self.notification_service = NotificationService()

        # Mapeamento de estratégias de pagamento
        self._payment_strategies: Dict[str, PaymentStrategy] = {
            'credit_card': CreditCardPayment(),
            'pix': PixPayment(),
            'boleto': BoletoPayment(),
        }

    def create_order(self, order_data: OrderCreate) -> Order:
        """
        Cria um novo pedido usando todos os padrões de projeto.

        Fluxo:
        1. Cria ou obtém cliente (Repository)
        2. Calcula subtotal dos itens
        3. Aplica decorators (Decorator Pattern)
        4. Cria pedido usando factory (Factory Method)
        5. Processa pagamento (Strategy Pattern)
        6. Persiste pedido (Repository)
        7. Notifica sobre criação (Observer)

        Args:
            order_data: Dados do pedido

        Returns:
            Order: Pedido criado

        Raises:
            ValueError: Se dados inválidos
        """
        # 1. Obtém ou cria cliente
        customer = self._get_or_create_customer(order_data.customer.model_dump())

        # 2. Calcula subtotal e prepara itens
        items_data, subtotal = self._calculate_order_items(order_data.items)

        # 3. Aplica decorators para calcular custo dos extras
        extras_cost = self._calculate_extras_cost(
            subtotal,
            order_data.extras.gift_wrap,
            order_data.extras.insurance,
            order_data.extras.insurance_type
        )

        # 4. Usa Factory Method para criar pedido do tipo correto
        order = OrderFactory.create_order(
            order_type=order_data.order_type,
            order_data={
                'customer_id': customer.id,
                'payment_method': order_data.payment_method,
                'subtotal': subtotal,
                'extras_cost': extras_cost,
                'has_gift_wrap': order_data.extras.gift_wrap,
                'has_insurance': order_data.extras.insurance,
            }
        )

        # 5. Processa pagamento usando Strategy Pattern
        payment_result = self._process_payment(
            order_data.payment_method,
            order.total,
            self._prepare_payment_details(order_data, customer)
        )

        if not payment_result.get('success'):
            raise ValueError(f"Falha no pagamento: {payment_result.get('message')}")

        # 6. Persiste pedido com itens
        created_order = self.order_repo.create_with_items(order, items_data)

        # 7. Atualiza estoque dos produtos
        self._update_products_stock(items_data)

        # 8. Notifica sobre criação do pedido (Observer Pattern)
        self.notification_service.notify_order_status_change(
            order_id=created_order.id,
            customer_id=customer.id,
            customer_name=customer.name,
            customer_email=customer.email,
            customer_phone=customer.phone,
            old_status=None,
            new_status=created_order.status,
            note="Pedido criado com sucesso"
        )

        return created_order

    def update_order_status(self, order_id: int, new_status: str, note: str = None) -> Order:
        """
        Atualiza status do pedido e notifica observadores.

        Args:
            order_id: ID do pedido
            new_status: Novo status
            note: Nota opcional

        Returns:
            Order: Pedido atualizado

        Raises:
            ValueError: Se pedido não encontrado
        """
        # Obtém pedido com detalhes
        order = self.order_repo.get_by_id_with_details(order_id)
        if not order:
            raise ValueError(f"Pedido {order_id} não encontrado")

        old_status = order.status

        # Atualiza status
        updated_order = self.order_repo.update_status(order_id, new_status, note)

        # Notifica observadores sobre mudança (Observer Pattern)
        self.notification_service.notify_order_status_change(
            order_id=order_id,
            customer_id=order.customer.id,
            customer_name=order.customer.name,
            customer_email=order.customer.email,
            customer_phone=order.customer.phone,
            old_status=old_status,
            new_status=new_status,
            note=note
        )

        return updated_order

    def get_order_by_id(self, order_id: int) -> Order:
        """Obtém pedido por ID."""
        order = self.order_repo.get_by_id_with_details(order_id)
        if not order:
            raise ValueError(f"Pedido {order_id} não encontrado")
        return order

    def get_orders_by_customer(self, customer_id: int) -> List[Order]:
        """Obtém todos os pedidos de um cliente."""
        return self.order_repo.get_by_customer(customer_id)

    def get_all_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtém todos os pedidos com paginação e relacionamentos."""
        all_orders = self.order_repo.get_all_with_details()
        return all_orders[skip:skip + limit]

    # Métodos auxiliares privados

    def _get_or_create_customer(self, customer_data: Dict[str, Any]) -> Customer:
        """Obtém cliente existente ou cria novo."""
        customer = self.customer_repo.get_by_email(customer_data['email'])
        if not customer:
            customer = Customer(**customer_data)
            customer = self.customer_repo.create(customer)
        return customer

    def _calculate_order_items(self, items: List[Any]) -> tuple[List[Dict], float]:
        """Calcula itens do pedido e subtotal."""
        items_data = []
        subtotal = 0.0

        for item in items:
            product = self.product_repo.get_by_id(item.product_id)
            if not product:
                raise ValueError(f"Produto {item.product_id} não encontrado")

            if product.stock < item.quantity:
                raise ValueError(f"Estoque insuficiente para produto {product.name}")

            unit_price = product.price
            item_total = unit_price * item.quantity

            items_data.append({
                'product_id': item.product_id,
                'quantity': item.quantity,
                'unit_price': unit_price
            })

            subtotal += item_total

        return items_data, subtotal

    def _calculate_extras_cost(
        self,
        subtotal: float,
        has_gift_wrap: bool,
        has_insurance: bool,
        insurance_type: str = "standard"
    ) -> float:
        """
        Calcula custo dos extras usando Decorator Pattern.

        Args:
            subtotal: Subtotal do pedido
            has_gift_wrap: Se tem embalagem presente
            has_insurance: Se tem seguro
            insurance_type: Tipo de seguro

        Returns:
            float: Custo total dos extras
        """
        # Cria pedido base
        order_component = BaseOrder(subtotal)

        # Aplica decorator de embalagem presente se necessário
        if has_gift_wrap:
            order_component = GiftWrapDecorator(order_component)

        # Aplica decorator de seguro se necessário
        if has_insurance:
            order_component = InsuranceDecorator(order_component, insurance_type)

        # Retorna apenas o custo dos extras
        return order_component.get_cost() - subtotal

    def _process_payment(
        self,
        payment_method: str,
        amount: float,
        payment_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processa pagamento usando Strategy Pattern.

        Args:
            payment_method: Método de pagamento
            amount: Valor
            payment_details: Detalhes do pagamento

        Returns:
            Dict[str, Any]: Resultado do pagamento
        """
        strategy = self._payment_strategies.get(payment_method)
        if not strategy:
            raise ValueError(f"Método de pagamento inválido: {payment_method}")

        return strategy.process_payment(amount, payment_details)

    def _prepare_payment_details(self, order_data: OrderCreate, customer: Customer) -> Dict[str, Any]:
        """Prepara detalhes do pagamento baseado no método."""
        # Simulação de detalhes de pagamento
        # Em produção, isso viria do frontend
        if order_data.payment_method == 'credit_card':
            return {
                'card_number': '4111111111111111',  # Simulado
                'cvv': '123',
                'expiry_date': '12/25',
                'cardholder_name': customer.name
            }
        elif order_data.payment_method in ['pix', 'boleto']:
            return {
                'payer_name': customer.name,
                'payer_cpf': '12345678900'  # Simulado
            }
        return {}

    def _update_products_stock(self, items_data: List[Dict]) -> None:
        """Atualiza estoque dos produtos após venda."""
        for item in items_data:
            self.product_repo.update_stock(
                item['product_id'],
                -item['quantity']  # Diminui estoque
            )
