"""Notificador de SMS - Observador"""

from typing import Dict, Any
from datetime import datetime
from app.observers.order_observer import OrderObserver


class SmsNotifier(OrderObserver):
    """
    Observador de notificação por SMS.

    Envia notificações por SMS quando o status do pedido muda.
    Em produção, isso integraria com um serviço de SMS (Twilio, AWS SNS, etc.)
    """

    MAX_SMS_LENGTH = 160

    def update(self, order_data: Dict[str, Any]) -> None:
        """
        Envia notificação por SMS sobre mudança de status do pedido.

        Args:
            order_data: Informações do pedido incluindo telefone e novo status do cliente
        """
        order_id = order_data.get('order_id')
        customer_phone = order_data.get('customer_phone')
        new_status = order_data.get('new_status')

        # Gera mensagem SMS (deve ser curta)
        sms_content = self._generate_sms_content(order_id, new_status)

        print(f"[SmsNotifier] Enviando SMS para {customer_phone}")
        print(f"[SmsNotifier] Mensagem: {sms_content}")

        # Em produção, enviaria SMS real:
        # sms_service.send(
        #     to=customer_phone,
        #     message=sms_content
        # )

    def get_observer_name(self) -> str:
        """Obtém nome do observador."""
        return "sms"

    def _generate_sms_content(self, order_id: int, status: str) -> str:
        """
        Gera conteúdo curto de SMS.

        Args:
            order_id: ID do pedido
            status: Novo status do pedido

        Returns:
            str: Conteúdo do SMS (máximo 160 caracteres)
        """
        status_messages = {
            'pending': f'Pedido #{order_id} recebido. Aguardando confirmação.',
            'confirmed': f'Pedido #{order_id} confirmado! Preparando seus itens.',
            'shipped': f'Pedido #{order_id} enviado! Rastreie sua entrega.',
            'delivered': f'Pedido #{order_id} entregue! Obrigado!',
            'cancelled': f'Pedido #{order_id} cancelado.',
        }

        message = status_messages.get(status, f'Pedido #{order_id}: {status}')

        # Garante que a mensagem cabe no limite de tamanho do SMS
        if len(message) > self.MAX_SMS_LENGTH:
            message = message[:self.MAX_SMS_LENGTH - 3] + '...'

        return message
