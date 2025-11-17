"""
Testes para o Padrão Decorator

Testa decorators de pedidos (embalagem presente e seguro).
"""

import pytest
from app.decorators.order_decorator import BaseOrder
from app.decorators.gift_wrap_decorator import GiftWrapDecorator
from app.decorators.insurance_decorator import InsuranceDecorator


class TestDecoratorPattern:
    """Testes para Decorator Pattern."""

    def test_base_order_cost(self):
        """Testa custo do pedido base sem extras."""
        order = BaseOrder(subtotal=100.0)

        assert order.get_cost() == 100.0
        assert order.get_extras_details() == {}

    def test_gift_wrap_decorator(self):
        """Testa decorator de embalagem presente."""
        order = BaseOrder(subtotal=100.0)
        order_with_gift = GiftWrapDecorator(order, message="Feliz Aniversário!")

        assert order_with_gift.get_cost() == 110.0  # 100 + 10
        assert 'gift_wrap' in order_with_gift.get_extras_details()
        assert order_with_gift.get_extras_details()['gift_wrap']['enabled'] is True
        assert order_with_gift.get_extras_details()['gift_wrap']['cost'] == 10.0
        assert order_with_gift.get_gift_message() == "Feliz Aniversário!"

    def test_insurance_decorator_standard(self):
        """Testa decorator de seguro padrão (5%)."""
        order = BaseOrder(subtotal=100.0)
        order_with_insurance = InsuranceDecorator(order, coverage_type="standard")

        assert order_with_insurance.get_cost() == 105.0  # 100 + 5
        assert 'insurance' in order_with_insurance.get_extras_details()
        assert order_with_insurance.get_insurance_cost() == 5.0
        assert order_with_insurance.get_coverage_type() == "standard"

    def test_insurance_decorator_premium(self):
        """Testa decorator de seguro premium (8%)."""
        order = BaseOrder(subtotal=100.0)
        order_with_insurance = InsuranceDecorator(order, coverage_type="premium")

        assert order_with_insurance.get_cost() == 108.0  # 100 + 8
        assert order_with_insurance.get_insurance_cost() == 8.0
        assert order_with_insurance.get_coverage_type() == "premium"

    def test_combined_decorators(self):
        """Testa combinação de múltiplos decorators."""
        order = BaseOrder(subtotal=100.0)

        # Aplica embalagem presente
        order = GiftWrapDecorator(order, message="Presente!")

        # Aplica seguro
        order = InsuranceDecorator(order, coverage_type="standard")

        # Custo final: 100 (base) + 10 (embalagem) = 110, + 5% de seguro = 115.5
        assert order.get_cost() == 115.5

        extras = order.get_extras_details()
        assert 'gift_wrap' in extras
        assert 'insurance' in extras
        assert extras['gift_wrap']['enabled'] is True
        assert extras['insurance']['enabled'] is True

    def test_decorator_description(self):
        """Testa que decorators modificam a descrição."""
        order = BaseOrder(subtotal=100.0, description="Pedido")

        order = GiftWrapDecorator(order)
        description = order.get_description()

        assert "Embalagem Presente" in description
        assert "Pedido" in description

    def test_multiple_decorators_order(self):
        """Testa que a ordem dos decorators afeta o resultado quando há cálculos percentuais."""
        # Ordem 1: Gift Wrap -> Insurance (seguro calculado sobre subtotal + gift wrap)
        order1 = BaseOrder(subtotal=100.0)
        order1 = GiftWrapDecorator(order1)
        order1 = InsuranceDecorator(order1, "standard")
        cost1 = order1.get_cost()

        # Ordem 2: Insurance -> Gift Wrap (seguro calculado apenas sobre subtotal)
        order2 = BaseOrder(subtotal=100.0)
        order2 = InsuranceDecorator(order2, "standard")
        order2 = GiftWrapDecorator(order2)
        cost2 = order2.get_cost()

        # Ordem 1: 100 + 10 (gift) = 110, + 5% seguro = 115.5
        assert cost1 == 115.5
        # Ordem 2: 100 + 5% seguro = 105, + 10 (gift) = 115.0
        assert cost2 == 115.0
        # A ordem afeta o resultado quando há porcentagens (comportamento esperado)
        assert cost1 != cost2
