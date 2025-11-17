"""Serviço de Notificação - Gerencia Observadores"""

from typing import List
from app.observers.order_subject import OrderSubject
from app.observers.email_notifier import EmailNotifier
from app.observers.sms_notifier import SmsNotifier
from app.observers.log_notifier import LogNotifier


class NotificationService:
    """
    Serviço de notificação que gerencia observadores.

    Utiliza o padrão Observer para notificar múltiplos sistemas
    quando o status do pedido muda.
    """

    def __init__(self):
        """Inicializa serviço com subject e observadores padrão."""
        self.subject = OrderSubject()

        # Anexa observadores padrão
        self.subject.attach(EmailNotifier())
        self.subject.attach(SmsNotifier())
        self.subject.attach(LogNotifier())

    def notify_order_status_change(
        self,
        order_id: int,
        customer_id: int,
        customer_name: str,
        customer_email: str,
        customer_phone: str,
        old_status: str,
        new_status: str,
        note: str = None
    ) -> List[str]:
        """
        Notifica todos os observadores sobre mudança de status do pedido.

        Args:
            order_id: ID do pedido
            customer_id: ID do cliente
            customer_name: Nome do cliente
            customer_email: Email do cliente
            customer_phone: Telefone do cliente
            old_status: Status anterior
            new_status: Novo status
            note: Nota opcional sobre a mudança

        Returns:
            List[str]: Lista de observadores notificados
        """
        order_data = {
            'order_id': order_id,
            'customer_id': customer_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'old_status': old_status,
            'new_status': new_status,
            'note': note
        }

        return self.subject.notify(order_data)

    def get_active_notifiers(self) -> List[str]:
        """
        Obtém lista de notificadores ativos.

        Returns:
            List[str]: Nomes dos notificadores
        """
        return self.subject.get_observers_names()
