"""
Testes para o Padrão Strategy

Testa diferentes estratégias de pagamento.
"""

import pytest
from app.strategies.credit_card_payment import CreditCardPayment
from app.strategies.pix_payment import PixPayment
from app.strategies.boleto_payment import BoletoPayment


class TestPaymentStrategies:
    """Testes para Payment Strategy Pattern."""

    def test_credit_card_payment_success(self):
        """Testa pagamento bem-sucedido com cartão de crédito."""
        strategy = CreditCardPayment()
        payment_details = {
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25',
            'cardholder_name': 'João Silva'
        }

        result = strategy.process_payment(100.0, payment_details)

        assert result['success'] is True
        assert result['payment_method'] == 'credit_card'
        assert result['amount'] == 100.0
        assert 'transaction_id' in result
        assert result['card_last_4'] == '1111'

    def test_credit_card_payment_invalid_card(self):
        """Testa pagamento com cartão inválido."""
        strategy = CreditCardPayment()
        payment_details = {
            'card_number': '123',  # Muito curto
            'cvv': '123',
            'expiry_date': '12/25',
            'cardholder_name': 'João Silva'
        }

        result = strategy.process_payment(100.0, payment_details)

        assert result['success'] is False
        assert 'inválido' in result['message'].lower()

    def test_credit_card_payment_missing_fields(self):
        """Testa pagamento com campos faltando."""
        strategy = CreditCardPayment()
        payment_details = {
            'card_number': '4111111111111111'
            # Faltando outros campos
        }

        result = strategy.process_payment(100.0, payment_details)

        assert result['success'] is False
        assert 'faltando' in result['message'].lower()

    def test_pix_payment_success(self):
        """Testa geração bem-sucedida de código PIX."""
        strategy = PixPayment()
        payment_details = {}

        result = strategy.process_payment(100.0, payment_details)

        assert result['success'] is True
        assert result['payment_method'] == 'pix'
        assert result['amount'] == 100.0
        assert 'pix_code' in result
        assert 'qr_code_data' in result
        assert 'expires_at' in result
        assert result['status'] == 'pending_payment'

    def test_pix_payment_invalid_amount(self):
        """Testa PIX com valor inválido."""
        strategy = PixPayment()

        result = strategy.process_payment(0.0, {})

        assert result['success'] is False
        assert 'inválido' in result['message'].lower()

    def test_pix_get_payment_method_name(self):
        """Testa nome do método de pagamento PIX."""
        strategy = PixPayment()
        assert strategy.get_payment_method_name() == "PIX"

    def test_boleto_payment_success(self):
        """Testa geração bem-sucedida de boleto."""
        strategy = BoletoPayment()
        payment_details = {
            'payer_name': 'João Silva',
            'payer_cpf': '12345678900'
        }

        result = strategy.process_payment(100.0, payment_details)

        assert result['success'] is True
        assert result['payment_method'] == 'boleto'
        assert result['amount'] == 100.0
        assert 'boleto_code' in result
        assert 'barcode' in result
        assert 'due_date' in result
        assert result['status'] == 'pending_payment'

    def test_boleto_payment_missing_fields(self):
        """Testa boleto com campos faltando."""
        strategy = BoletoPayment()
        payment_details = {
            'payer_name': 'João Silva'
            # Faltando CPF
        }

        result = strategy.process_payment(100.0, payment_details)

        assert result['success'] is False
        assert 'faltando' in result['message'].lower()

    def test_all_strategies_implement_interface(self):
        """Testa que todas estratégias implementam a interface corretamente."""
        strategies = [
            CreditCardPayment(),
            PixPayment(),
            BoletoPayment()
        ]

        for strategy in strategies:
            assert hasattr(strategy, 'process_payment')
            assert hasattr(strategy, 'get_payment_method_name')
            assert callable(strategy.process_payment)
            assert callable(strategy.get_payment_method_name)
