"""
Testes para o Padrão Factory Method

Testa a criação de diferentes tipos de pedidos e produtos.
"""

import pytest
from app.factories.order_factory import OrderFactory, RegularOrderCreator, ExpressOrderCreator, InternationalOrderCreator
from app.factories.product_factory import ProductFactory, PhysicalProductCreator, DigitalProductCreator, SubscriptionProductCreator


class TestOrderFactory:
    """Testes para OrderFactory (Factory Method Pattern)."""

    def test_create_regular_order(self):
        """Testa criação de pedido regular."""
        order_data = {
            'customer_id': 1,
            'payment_method': 'credit_card',
            'subtotal': 100.0
        }

        order = OrderFactory.create_order('regular', order_data)

        assert order.type == 'regular'
        assert order.total == 100.0  # Sem taxas extras
        assert order.extras_cost == 0.0

    def test_create_express_order(self):
        """Testa criação de pedido expresso com taxa de 15%."""
        order_data = {
            'customer_id': 1,
            'payment_method': 'pix',
            'subtotal': 100.0
        }

        order = OrderFactory.create_order('express', order_data)

        assert order.type == 'express'
        assert order.extras_cost == 15.0  # 15% de 100
        assert order.total == 115.0

    def test_create_international_order(self):
        """Testa criação de pedido internacional com taxa de 30%."""
        order_data = {
            'customer_id': 1,
            'payment_method': 'boleto',
            'subtotal': 100.0
        }

        order = OrderFactory.create_order('international', order_data)

        assert order.type == 'international'
        assert order.extras_cost == 30.0  # 30% de 100
        assert order.total == 130.0

    def test_invalid_order_type(self):
        """Testa erro ao criar pedido com tipo inválido."""
        with pytest.raises(ValueError, match="Tipo de pedido desconhecido"):
            OrderFactory.create_order('invalid_type', {})

    def test_get_supported_types(self):
        """Testa obtenção de tipos suportados."""
        types = OrderFactory.get_supported_types()
        assert 'regular' in types
        assert 'express' in types
        assert 'international' in types


class TestProductFactory:
    """Testes para ProductFactory (Factory Method Pattern)."""

    def test_create_physical_product(self):
        """Testa criação de produto físico."""
        product_data = {
            'name': 'Notebook',
            'description': 'Notebook gamer',
            'price': 3000.0,
            'stock': 10
        }

        product = ProductFactory.create_product('physical', product_data)

        assert product.type == 'physical'
        assert product.stock == 10
        assert product.name == 'Notebook'

    def test_create_digital_product(self):
        """Testa criação de produto digital com estoque ilimitado."""
        product_data = {
            'name': 'Curso Python',
            'description': 'Curso completo',
            'price': 299.0
        }

        product = ProductFactory.create_product('digital', product_data)

        assert product.type == 'digital'
        assert product.stock == 999  # Estoque ilimitado
        assert product.price == 299.0

    def test_create_subscription_product(self):
        """Testa criação de produto de assinatura."""
        product_data = {
            'name': 'Plano Premium',
            'description': 'Acesso completo',
            'price': 99.0
        }

        product = ProductFactory.create_product('subscription', product_data)

        assert product.type == 'subscription'
        assert product.stock == 999  # Ilimitado
        assert 'recorrente' in product.description.lower() or 'Acesso completo' in product.description

    def test_invalid_product_type(self):
        """Testa erro ao criar produto com tipo inválido."""
        with pytest.raises(ValueError, match="Tipo de produto desconhecido"):
            ProductFactory.create_product('invalid_type', {})
