"""
Factory de Pedidos - Implementação do Padrão Factory Method

PADRÃO DE PROJETO: Factory Method
PROPÓSITO: Criar diferentes tipos de pedidos sem expor a lógica de criação
BENEFÍCIO: Evita código condicional complexo, facilita adicionar novos tipos de pedidos,
          segue o Princípio Aberto/Fechado
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from app.models.order import Order


class OrderCreator(ABC):
    """
    Criador abstrato de pedidos definindo a interface do método factory.

    Este é o núcleo do padrão Factory Method. As subclasses implementam
    o método factory para criar tipos específicos de pedidos.
    """

    @abstractmethod
    def create_order(self, order_data: Dict[str, Any]) -> Order:
        """
        Método factory para criar um pedido.

        Args:
            order_data: Dicionário contendo informações do pedido

        Returns:
            Order: Instância do pedido criada
        """
        pass

    def get_order_type(self) -> str:
        """
        Obtém o tipo de pedido que esta factory cria.

        Returns:
            str: Nome do tipo de pedido
        """
        return self.__class__.__name__.replace("OrderCreator", "").lower()


class RegularOrderCreator(OrderCreator):
    """
    Factory para criar pedidos regulares.

    Pedidos regulares:
    - Tempo de entrega padrão (7-10 dias)
    - Sem taxas extras
    - Opção mais econômica
    """

    def create_order(self, order_data: Dict[str, Any]) -> Order:
        """
        Cria um pedido regular.

        Args:
            order_data: Informações do pedido

        Returns:
            Order: Instância de pedido regular
        """
        order = Order(
            customer_id=order_data['customer_id'],
            type='regular',
            payment_method=order_data['payment_method'],
            subtotal=order_data['subtotal'],
            extras_cost=order_data.get('extras_cost', 0.0),
            total=order_data['subtotal'] + order_data.get('extras_cost', 0.0),
            has_gift_wrap=order_data.get('has_gift_wrap', False),
            has_insurance=order_data.get('has_insurance', False),
            status='pending'
        )
        return order


class ExpressOrderCreator(OrderCreator):
    """
    Factory para criar pedidos expressos.

    Pedidos expressos:
    - Entrega rápida (2-3 dias)
    - Taxa adicional de 15% sobre o subtotal
    - Processamento prioritário
    """

    EXTRA_FEE_PERCENTAGE = 0.15

    def create_order(self, order_data: Dict[str, Any]) -> Order:
        """
        Cria um pedido expresso com entrega acelerada.

        Args:
            order_data: Informações do pedido

        Returns:
            Order: Instância de pedido expresso com taxa extra
        """
        # Calcula taxa de entrega expressa
        express_fee = order_data['subtotal'] * self.EXTRA_FEE_PERCENTAGE
        extras_cost = order_data.get('extras_cost', 0.0) + express_fee

        order = Order(
            customer_id=order_data['customer_id'],
            type='express',
            payment_method=order_data['payment_method'],
            subtotal=order_data['subtotal'],
            extras_cost=extras_cost,
            total=order_data['subtotal'] + extras_cost,
            has_gift_wrap=order_data.get('has_gift_wrap', False),
            has_insurance=order_data.get('has_insurance', False),
            status='pending'
        )
        return order


class InternationalOrderCreator(OrderCreator):
    """
    Factory para criar pedidos internacionais.

    Pedidos internacionais:
    - Envio internacional (15-30 dias)
    - Taxa adicional de 30% sobre o subtotal (alfândega + frete)
    - Requer documentação adicional
    """

    EXTRA_FEE_PERCENTAGE = 0.30

    def create_order(self, order_data: Dict[str, Any]) -> Order:
        """
        Cria um pedido internacional com taxas de alfândega e frete.

        Args:
            order_data: Informações do pedido

        Returns:
            Order: Instância de pedido internacional com taxas internacionais
        """
        # Calcula taxa de frete e alfândega internacional
        international_fee = order_data['subtotal'] * self.EXTRA_FEE_PERCENTAGE
        extras_cost = order_data.get('extras_cost', 0.0) + international_fee

        order = Order(
            customer_id=order_data['customer_id'],
            type='international',
            payment_method=order_data['payment_method'],
            subtotal=order_data['subtotal'],
            extras_cost=extras_cost,
            total=order_data['subtotal'] + extras_cost,
            has_gift_wrap=order_data.get('has_gift_wrap', False),
            has_insurance=order_data.get('has_insurance', False),
            status='pending'
        )
        return order


class OrderFactory:
    """
    Classe factory principal que delega a criação de pedidos para criadores específicos.

    Isso demonstra o padrão Factory Method usando diferentes criadores
    baseados no tipo de pedido, evitando lógica condicional complexa.
    """

    _creators = {
        'regular': RegularOrderCreator(),
        'express': ExpressOrderCreator(),
        'international': InternationalOrderCreator(),
    }

    @classmethod
    def create_order(cls, order_type: str, order_data: Dict[str, Any]) -> Order:
        """
        Cria um pedido do tipo especificado.

        Args:
            order_type: Tipo de pedido (regular, express, international)
            order_data: Informações do pedido

        Returns:
            Order: Instância do pedido criada

        Raises:
            ValueError: Se o tipo de pedido não for suportado
        """
        creator = cls._creators.get(order_type.lower())
        if not creator:
            raise ValueError(
                f"Tipo de pedido desconhecido: {order_type}. "
                f"Tipos suportados: {', '.join(cls._creators.keys())}"
            )

        return creator.create_order(order_data)

    @classmethod
    def get_supported_types(cls) -> list[str]:
        """
        Obtém lista de tipos de pedidos suportados.

        Returns:
            list[str]: Lista de nomes dos tipos de pedidos
        """
        return list(cls._creators.keys())
