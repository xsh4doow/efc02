"""Estratégia de Pagamento com Cartão de Crédito"""

from typing import Dict, Any
from datetime import datetime
import hashlib
from app.strategies.payment_strategy import PaymentStrategy


class CreditCardPayment(PaymentStrategy):
    """
    Estratégia de pagamento com cartão de crédito.

    Processa pagamentos via cartão de crédito com aprovação instantânea.
    Requer: número do cartão, CVV, data de expiração, nome do titular
    """

    def process_payment(self, amount: float, payment_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa pagamento com cartão de crédito.

        Args:
            amount: Valor a cobrar
            payment_details: Deve conter 'card_number', 'cvv', 'expiry_date', 'cardholder_name'

        Returns:
            Dict[str, Any]: Resultado do pagamento com detalhes da transação

        Raises:
            ValueError: Se os detalhes do pagamento são inválidos
        """
        # Valida valor
        if not self.validate_amount(amount):
            return {
                'success': False,
                'message': 'Valor de pagamento inválido',
                'transaction_id': None
            }

        # Valida campos obrigatórios
        required_fields = ['card_number', 'cvv', 'expiry_date', 'cardholder_name']
        for field in required_fields:
            if field not in payment_details:
                return {
                    'success': False,
                    'message': f'Campo obrigatório faltando: {field}',
                    'transaction_id': None
                }

        # Valida número do cartão (verificação básica - deve ter 13-19 dígitos)
        card_number = str(payment_details['card_number']).replace(' ', '')
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            return {
                'success': False,
                'message': 'Número de cartão inválido',
                'transaction_id': None
            }

        # Valida CVV (3-4 dígitos)
        cvv = str(payment_details['cvv'])
        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            return {
                'success': False,
                'message': 'CVV inválido',
                'transaction_id': None
            }

        # Simula processamento de pagamento
        # Em produção, isso integraria com um gateway de pagamento
        transaction_id = self._generate_transaction_id(card_number, amount)

        return {
            'success': True,
            'message': 'Pagamento processado com sucesso',
            'transaction_id': transaction_id,
            'payment_method': 'credit_card',
            'amount': amount,
            'processed_at': datetime.now().isoformat(),
            'card_last_4': card_number[-4:]
        }

    def get_payment_method_name(self) -> str:
        """Obtém nome do método de pagamento."""
        return "Cartão de Crédito"

    def _generate_transaction_id(self, card_number: str, amount: float) -> str:
        """
        Gera um ID de transação único.

        Args:
            card_number: Número do cartão
            amount: Valor do pagamento

        Returns:
            str: ID da transação
        """
        data = f"{card_number}{amount}{datetime.now().isoformat()}"
        return hashlib.md5(data.encode()).hexdigest()[:16].upper()
