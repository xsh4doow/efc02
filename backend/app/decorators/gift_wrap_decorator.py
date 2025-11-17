"""Decorator de Embalagem Presente"""

from typing import Dict, Any
from app.decorators.order_decorator import OrderDecorator, OrderComponent


class GiftWrapDecorator(OrderDecorator):
    """
    Decorator que adiciona embalagem presente ao pedido.

    Adiciona custo extra e modifica a descrição do pedido para incluir
    a informação de embalagem presente.
    """

    GIFT_WRAP_COST = 10.0  # Custo fixo da embalagem presente

    def __init__(self, order: OrderComponent, message: str = ""):
        """
        Inicializa decorator de embalagem presente.

        Args:
            order: Componente de pedido a ser decorado
            message: Mensagem opcional para o cartão de presente
        """
        super().__init__(order)
        self._message = message

    def get_cost(self) -> float:
        """
        Retorna custo do pedido mais o custo da embalagem presente.

        Returns:
            float: Custo total incluindo embalagem presente
        """
        return self._order.get_cost() + self.GIFT_WRAP_COST

    def get_description(self) -> str:
        """
        Retorna descrição do pedido incluindo embalagem presente.

        Returns:
            str: Descrição completa com embalagem presente
        """
        base_description = self._order.get_description()
        gift_info = f"Embalagem Presente (R$ {self.GIFT_WRAP_COST:.2f})"

        if self._message:
            gift_info += f' com mensagem: "{self._message}"'

        return f"{base_description} + {gift_info}"

    def get_extras_details(self) -> Dict[str, Any]:
        """
        Retorna detalhes dos extras incluindo embalagem presente.

        Returns:
            Dict[str, Any]: Detalhes de todos os extras
        """
        extras = self._order.get_extras_details()
        extras['gift_wrap'] = {
            'enabled': True,
            'cost': self.GIFT_WRAP_COST,
            'message': self._message if self._message else None
        }
        return extras

    def get_gift_message(self) -> str:
        """
        Obtém a mensagem do cartão de presente.

        Returns:
            str: Mensagem do cartão
        """
        return self._message
