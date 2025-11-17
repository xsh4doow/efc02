"""Decorator de Seguro"""

from typing import Dict, Any
from app.decorators.order_decorator import OrderDecorator, OrderComponent


class InsuranceDecorator(OrderDecorator):
    """
    Decorator que adiciona seguro ao pedido.

    Adiciona custo de seguro baseado em porcentagem do valor do pedido
    e modifica a descrição para incluir informação de cobertura.
    """

    INSURANCE_PERCENTAGE = 0.05  # 5% do valor do pedido

    def __init__(self, order: OrderComponent, coverage_type: str = "standard"):
        """
        Inicializa decorator de seguro.

        Args:
            order: Componente de pedido a ser decorado
            coverage_type: Tipo de cobertura (standard, premium)
        """
        super().__init__(order)
        self._coverage_type = coverage_type

        # Ajusta percentual baseado no tipo de cobertura
        if coverage_type == "premium":
            self._percentage = 0.08  # 8% para cobertura premium
        else:
            self._percentage = self.INSURANCE_PERCENTAGE

    def get_cost(self) -> float:
        """
        Retorna custo do pedido mais o custo do seguro.

        Returns:
            float: Custo total incluindo seguro
        """
        base_cost = self._order.get_cost()
        insurance_cost = base_cost * self._percentage
        return base_cost + insurance_cost

    def get_description(self) -> str:
        """
        Retorna descrição do pedido incluindo seguro.

        Returns:
            str: Descrição completa com seguro
        """
        base_description = self._order.get_description()
        base_cost = self._order.get_cost()
        insurance_cost = base_cost * self._percentage

        coverage_label = "Premium" if self._coverage_type == "premium" else "Padrão"
        insurance_info = f"Seguro {coverage_label} ({int(self._percentage * 100)}% - R$ {insurance_cost:.2f})"

        return f"{base_description} + {insurance_info}"

    def get_extras_details(self) -> Dict[str, Any]:
        """
        Retorna detalhes dos extras incluindo seguro.

        Returns:
            Dict[str, Any]: Detalhes de todos os extras
        """
        extras = self._order.get_extras_details()
        base_cost = self._order.get_cost()
        insurance_cost = base_cost * self._percentage

        extras['insurance'] = {
            'enabled': True,
            'cost': insurance_cost,
            'coverage_type': self._coverage_type,
            'percentage': self._percentage * 100
        }
        return extras

    def get_insurance_cost(self) -> float:
        """
        Obtém apenas o custo do seguro.

        Returns:
            float: Custo do seguro
        """
        return self._order.get_cost() * self._percentage

    def get_coverage_type(self) -> str:
        """
        Obtém o tipo de cobertura.

        Returns:
            str: Tipo de cobertura
        """
        return self._coverage_type
