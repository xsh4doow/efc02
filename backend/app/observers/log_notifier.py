"""Notificador de Log - Observador"""

from typing import Dict, Any
from datetime import datetime
from app.observers.order_observer import OrderObserver


class LogNotifier(OrderObserver):
    """
    Observador de notificação por log.

    Registra mudanças de status de pedidos nos logs do sistema.
    Útil para auditoria e depuração.
    """

    def update(self, order_data: Dict[str, Any]) -> None:
        """
        Registra mudança de status do pedido.

        Args:
            order_data: Informações do pedido para registrar
        """
        order_id = order_data.get('order_id')
        customer_id = order_data.get('customer_id')
        new_status = order_data.get('new_status')
        old_status = order_data.get('old_status')
        note = order_data.get('note', '')

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        log_entry = self._format_log_entry(
            timestamp, order_id, customer_id, old_status, new_status, note
        )

        print(f"[LogNotifier] {log_entry}")

        # Em produção, escreveria em arquivo de log real:
        # logging.info(log_entry)

    def get_observer_name(self) -> str:
        """Obtém nome do observador."""
        return "log"

    def _format_log_entry(
        self,
        timestamp: str,
        order_id: int,
        customer_id: int,
        old_status: str,
        new_status: str,
        note: str
    ) -> str:
        """
        Formata entrada de log.

        Args:
            timestamp: Timestamp da mudança
            order_id: ID do pedido
            customer_id: ID do cliente
            old_status: Status anterior
            new_status: Novo status
            note: Nota opcional

        Returns:
            str: Entrada de log formatada
        """
        log_entry = (
            f"[{timestamp}] MUDANCA_STATUS_PEDIDO | "
            f"PedidoID={order_id} | "
            f"ClienteID={customer_id} | "
            f"Status={old_status}->{new_status}"
        )

        if note:
            log_entry += f" | Nota={note}"

        return log_entry
