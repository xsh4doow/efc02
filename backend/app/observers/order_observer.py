"""
Observador de Pedidos - Implementação do Padrão Observer

PADRÃO DE PROJETO: Observer
PROPÓSITO: Definir uma dependência um-para-muitos entre objetos para que quando um objeto
           muda de estado, todos seus dependentes sejam notificados e atualizados automaticamente
BENEFÍCIO: Baixo acoplamento entre Pedido e sistemas de notificação, fácil adicionar/remover
           notificadores sem modificar o código de pedidos
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class OrderObserver(ABC):
    """
    Interface abstrata de observador.

    Todos os observadores devem implementar o método update para receber notificações.
    Este é o núcleo do padrão Observer.
    """

    @abstractmethod
    def update(self, order_data: Dict[str, Any]) -> None:
        """
        Chamado quando o status do pedido muda.

        Args:
            order_data: Dicionário contendo informações do pedido e detalhes da mudança de status
        """
        pass

    @abstractmethod
    def get_observer_name(self) -> str:
        """
        Obtém o nome deste observador.

        Returns:
            str: Nome do observador
        """
        pass
