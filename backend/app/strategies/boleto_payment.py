"""Estratégia de Pagamento via Boleto"""

from typing import Dict, Any
from datetime import datetime, timedelta
import hashlib
import random
from app.strategies.payment_strategy import PaymentStrategy


class BoletoPayment(PaymentStrategy):
    """
    Estratégia de pagamento via boleto bancário.

    Gera um boleto bancário para pagamento.
    Cliente paga no banco ou online.
    Confirmação de pagamento leva 1-3 dias úteis.
    """

    BOLETO_EXPIRATION_DAYS = 3

    def process_payment(self, amount: float, payment_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa pagamento via boleto gerando boleto bancário.

        Args:
            amount: Valor a ser pago
            payment_details: Deve conter 'payer_name', 'payer_cpf'

        Returns:
            Dict[str, Any]: Resultado do pagamento com detalhes do boleto

        Raises:
            ValueError: Se campos obrigatórios estão faltando
        """
        # Valida valor
        if not self.validate_amount(amount):
            return {
                'success': False,
                'message': 'Valor de pagamento inválido',
                'boleto_code': None
            }

        # Valida campos obrigatórios
        required_fields = ['payer_name', 'payer_cpf']
        for field in required_fields:
            if field not in payment_details:
                return {
                    'success': False,
                    'message': f'Campo obrigatório faltando: {field}',
                    'boleto_code': None
                }

        # Gera código de boleto e código de barras
        boleto_code = self._generate_boleto_code()
        barcode = self._generate_barcode(boleto_code, amount)

        # Calcula data de vencimento
        due_date = datetime.now() + timedelta(days=self.BOLETO_EXPIRATION_DAYS)

        return {
            'success': True,
            'message': 'Boleto gerado com sucesso',
            'boleto_code': boleto_code,
            'barcode': barcode,
            'payment_method': 'boleto',
            'amount': amount,
            'generated_at': datetime.now().isoformat(),
            'due_date': due_date.isoformat(),
            'status': 'pending_payment',
            'payer_name': payment_details['payer_name'],
            'payer_cpf': payment_details['payer_cpf'],
            'instructions': 'Pague em qualquer banco ou internet banking antes da data de vencimento'
        }

    def get_payment_method_name(self) -> str:
        """Obtém nome do método de pagamento."""
        return "Boleto Bancário"

    def _generate_boleto_code(self) -> str:
        """
        Gera um código de boleto (linha digitável).

        Returns:
            str: Código de boleto (47 dígitos formatados)
        """
        # Geração simplificada de código de boleto
        # Em produção, isso seguiria os padrões da FEBRABAN
        bank_code = "001"  # Exemplo: Banco do Brasil
        currency_code = "9"

        # Gera dígitos aleatórios
        field1 = f"{bank_code}{currency_code}{random.randint(10000, 99999)}"
        field2 = f"{random.randint(1000000000, 9999999999)}"
        field3 = f"{random.randint(1000000000, 9999999999)}"
        field4 = str(random.randint(1, 9))
        field5 = f"{random.randint(10000000000000, 99999999999999)}"

        # Formata com espaços
        return f"{field1[:5]} {field1[5:]} {field2[:5]} {field2[5:]} {field3[:5]} {field3[5:]} {field4} {field5}"

    def _generate_barcode(self, boleto_code: str, amount: float) -> str:
        """
        Gera código de barras para o boleto.

        Args:
            boleto_code: Código do boleto
            amount: Valor do pagamento

        Returns:
            str: Código de barras (44 dígitos)
        """
        # Remove espaços do código do boleto
        code_digits = boleto_code.replace(" ", "")

        # Pega os primeiros 44 dígitos para o código de barras
        # Em produção, isso seria calculado adequadamente
        return code_digits[:44]

    def confirm_payment(self, boleto_code: str) -> Dict[str, Any]:
        """
        Confirma pagamento do boleto (chamado quando o banco confirma o pagamento).

        Args:
            boleto_code: Código do boleto para confirmar

        Returns:
            Dict[str, Any]: Resultado da confirmação
        """
        # Em produção, isso verificaria com o banco
        transaction_id = hashlib.md5(boleto_code.encode()).hexdigest()[:16].upper()

        return {
            'success': True,
            'message': 'Pagamento de boleto confirmado',
            'transaction_id': transaction_id,
            'confirmed_at': datetime.now().isoformat(),
            'status': 'confirmed'
        }
