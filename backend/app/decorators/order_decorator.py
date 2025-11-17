"""
Decorator de Pedido - Implementação do Padrão Decorator

PADRÃO DE PROJETO: Decorator
PROPÓSITO: Adicionar responsabilidades a objetos dinamicamente sem modificar sua estrutura
BENEFÍCIO: Evita explosão de subclasses para cada combinação de extras,
           permite combinar múltiplos decorators facilmente
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class OrderComponent(ABC):
    """
    Interface de componente de pedido.

    Define a interface para objetos que podem ter responsabilidades adicionadas dinamicamente.
    """

    @abstractmethod
    def get_cost(self) -> float:
        """
        Obtém o custo do pedido (incluindo extras).

        Returns:
            float: Custo total
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Obtém a descrição do pedido (incluindo extras).

        Returns:
            str: Descrição completa
        """
        pass

    @abstractmethod
    def get_extras_details(self) -> Dict[str, Any]:
        """
        Obtém detalhes dos extras aplicados.

        Returns:
            Dict[str, Any]: Detalhes dos extras
        """
        pass


class BaseOrder(OrderComponent):
    """
    Componente concreto base representando um pedido sem extras.

    Este é o objeto que será decorado.
    """

    def __init__(self, subtotal: float, description: str = "Pedido padrão"):
        """
        Inicializa pedido base.

        Args:
            subtotal: Valor do subtotal do pedido
            description: Descrição do pedido
        """
        self._subtotal = subtotal
        self._description = description

    def get_cost(self) -> float:
        """Retorna apenas o subtotal sem extras."""
        return self._subtotal

    def get_description(self) -> str:
        """Retorna descrição básica."""
        return self._description

    def get_extras_details(self) -> Dict[str, Any]:
        """Retorna dicionário vazio pois não há extras."""
        return {}


class OrderDecorator(OrderComponent):
    """
    Decorator abstrato de pedido.

    Todos os decorators concretos devem herdar desta classe.
    Mantém uma referência ao componente que está decorando.
    """

    def __init__(self, order: OrderComponent):
        """
        Inicializa decorator com o componente a ser decorado.

        Args:
            order: Componente de pedido a ser decorado
        """
        self._order = order

    def get_cost(self) -> float:
        """
        Delega chamada ao componente decorado.

        Returns:
            float: Custo do componente decorado
        """
        return self._order.get_cost()

    def get_description(self) -> str:
        """
        Delega chamada ao componente decorado.

        Returns:
            str: Descrição do componente decorado
        """
        return self._order.get_description()

    def get_extras_details(self) -> Dict[str, Any]:
        """
        Delega chamada ao componente decorado.

        Returns:
            Dict[str, Any]: Detalhes dos extras do componente decorado
        """
        return self._order.get_extras_details()
