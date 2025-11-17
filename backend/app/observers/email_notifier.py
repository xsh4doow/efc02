"""Notificador de Email - Observador"""

from typing import Dict, Any
from datetime import datetime
from app.observers.order_observer import OrderObserver


class EmailNotifier(OrderObserver):
    """
    Observador de notificação por email.

    Envia notificações por email quando o status do pedido muda.
    Em produção, isso integraria com um serviço de email (SendGrid, SES, etc.)
    """

    def update(self, order_data: Dict[str, Any]) -> None:
        """
        Envia notificação por email sobre mudança de status do pedido.

        Args:
            order_data: Informações do pedido incluindo email e novo status do cliente
        """
        order_id = order_data.get('order_id')
        customer_email = order_data.get('customer_email')
        customer_name = order_data.get('customer_name')
        new_status = order_data.get('new_status')
        note = order_data.get('note', '')

        # Simula envio de email
        email_content = self._generate_email_content(
            customer_name, order_id, new_status, note
        )

        print(f"[EmailNotifier] Enviando email para {customer_email}")
        print(f"[EmailNotifier] Assunto: Pedido #{order_id} - Atualização de Status")
        print(f"[EmailNotifier] Conteúdo:\n{email_content}")

        # Em produção, enviaria email real:
        # email_service.send(
        #     to=customer_email,
        #     subject=f"Pedido #{order_id} - Atualização de Status",
        #     content=email_content
        # )

    def get_observer_name(self) -> str:
        """Obtém nome do observador."""
        return "email"

    def _generate_email_content(
        self, customer_name: str, order_id: int, status: str, note: str
    ) -> str:
        """
        Gera conteúdo do email baseado no status do pedido.

        Args:
            customer_name: Nome do cliente
            order_id: ID do pedido
            status: Novo status do pedido
            note: Nota opcional sobre a mudança de status

        Returns:
            str: Conteúdo do email
        """
        status_messages = {
            'pending': f'Seu pedido #{order_id} foi recebido e está aguardando confirmação.',
            'confirmed': f'Ótimas notícias! Seu pedido #{order_id} foi confirmado e está sendo preparado.',
            'shipped': f'Seu pedido #{order_id} foi enviado e está a caminho!',
            'delivered': f'Seu pedido #{order_id} foi entregue. Aproveite sua compra!',
            'cancelled': f'Seu pedido #{order_id} foi cancelado.',
        }

        message = status_messages.get(status, f'Seu pedido #{order_id} status: {status}')

        content = f"""
Olá {customer_name},

{message}

{f'Observação: {note}' if note else ''}

ID do Pedido: {order_id}
Status: {status.upper()}
Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Obrigado por comprar conosco!

Atenciosamente,
Equipe E-commerce
        """.strip()

        return content
