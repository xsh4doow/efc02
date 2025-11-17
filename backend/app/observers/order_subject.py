"""Sujeito de Pedido - Implementação do Padrão Observer

O Subject mantém uma lista de observadores e os notifica sobre mudanças de estado.
"""

from typing import List, Dict, Any
from app.observers.order_observer import OrderObserver


class OrderSubject:
    """
    Sujeito que mantém e notifica observadores.

    Quando o status do pedido muda, todos os observadores anexados são notificados automaticamente.
    Isso implementa a parte Subject do padrão Observer.
    """

    def __init__(self):
        """Inicializa com lista vazia de observadores."""
        self._observers: List[OrderObserver] = []

    def attach(self, observer: OrderObserver) -> None:
        """
        Anexa um observador para receber notificações.

        Args:
            observer: Observador para anexar
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[OrderSubject] Observador anexado: {observer.get_observer_name()}")

    def detach(self, observer: OrderObserver) -> None:
        """
        Desanexa um observador de receber notificações.

        Args:
            observer: Observador para desanexar
        """
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"[OrderSubject] Observador desanexado: {observer.get_observer_name()}")

    def notify(self, order_data: Dict[str, Any]) -> List[str]:
        """
        Notifica todos os observadores sobre mudança de status do pedido.

        Args:
            order_data: Informações do pedido para enviar aos observadores

        Returns:
            List[str]: Lista de nomes dos observadores notificados
        """
        notified = []
        print(f"[OrderSubject] Notificando {len(self._observers)} observadores sobre pedido #{order_data.get('order_id')} mudança de status para '{order_data.get('new_status')}'")

        for observer in self._observers:
            try:
                observer.update(order_data)
                notified.append(observer.get_observer_name())
            except Exception as e:
                print(f"[OrderSubject] Erro ao notificar {observer.get_observer_name()}: {str(e)}")

        return notified

    def get_observers_count(self) -> int:
        """
        Obtém número de observadores anexados.

        Returns:
            int: Número de observadores
        """
        return len(self._observers)

    def get_observers_names(self) -> List[str]:
        """
        Obtém nomes de todos os observadores anexados.

        Returns:
            List[str]: Lista de nomes dos observadores
        """
        return [observer.get_observer_name() for observer in self._observers]
