"""
Estratégia de Pagamento - Implementação do Padrão Strategy

PADRÃO DE PROJETO: Strategy
PROPÓSITO: Definir uma família de algoritmos de pagamento, encapsular cada um e torná-los intercambiáveis
BENEFÍCIO: Elimina lógica condicional complexa, facilita adicionar novos métodos de pagamento,
           cada estratégia é independente e testável
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime, timedelta


class PaymentStrategy(ABC):
    """
    Interface abstrata de estratégia de pagamento.

    Todas as estratégias de pagamento devem implementar o método process_payment.
    Este é o núcleo do padrão Strategy.
    """

    @abstractmethod
    def process_payment(self, amount: float, payment_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa pagamento usando esta estratégia.

        Args:
            amount: Valor a ser pago
            payment_details: Detalhes específicos do pagamento

        Returns:
            Dict[str, Any]: Resultado do pagamento com status e informações da transação
        """
        pass

    @abstractmethod
    def get_payment_method_name(self) -> str:
        """
        Obtém o nome deste método de pagamento.

        Returns:
            str: Nome do método de pagamento
        """
        pass

    def validate_amount(self, amount: float) -> bool:
        """
        Valida o valor do pagamento.

        Args:
            amount: Valor para validar

        Returns:
            bool: True se o valor é válido
        """
        return amount > 0
