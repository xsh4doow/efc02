"""
Factory de Produtos - Implementação do Padrão Factory Method

PADRÃO DE PROJETO: Factory Method
PROPÓSITO: Criar diferentes tipos de produtos sem expor a lógica de criação
BENEFÍCIO: Encapsula a criação de produtos, facilita adicionar novos tipos de produtos
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from app.models.product import Product


class ProductCreator(ABC):
    """
    Criador abstrato de produtos definindo a interface do método factory.

    As subclasses implementam o método factory para criar tipos específicos de produtos.
    """

    @abstractmethod
    def create_product(self, product_data: Dict[str, Any]) -> Product:
        """
        Método factory para criar um produto.

        Args:
            product_data: Dicionário contendo informações do produto

        Returns:
            Product: Instância do produto criada
        """
        pass

    def get_product_type(self) -> str:
        """
        Obtém o tipo de produto que esta factory cria.

        Returns:
            str: Nome do tipo de produto
        """
        return self.__class__.__name__.replace("ProductCreator", "").lower()


class PhysicalProductCreator(ProductCreator):
    """
    Factory para criar produtos físicos.

    Produtos físicos:
    - Requerem envio
    - Têm estoque limitado
    - Exemplos: livros, eletrônicos, roupas
    """

    def create_product(self, product_data: Dict[str, Any]) -> Product:
        """
        Cria um produto físico.

        Args:
            product_data: Informações do produto

        Returns:
            Product: Instância de produto físico
        """
        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            type='physical',
            stock=product_data.get('stock', 0)
        )
        return product


class DigitalProductCreator(ProductCreator):
    """
    Factory para criar produtos digitais.

    Produtos digitais:
    - Sem necessidade de envio (download)
    - Estoque ilimitado (999 representa ilimitado)
    - Exemplos: e-books, software, cursos
    """

    UNLIMITED_STOCK = 999

    def create_product(self, product_data: Dict[str, Any]) -> Product:
        """
        Cria um produto digital.

        Args:
            product_data: Informações do produto

        Returns:
            Product: Instância de produto digital com estoque ilimitado
        """
        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            type='digital',
            stock=self.UNLIMITED_STOCK  # Produtos digitais têm estoque ilimitado
        )
        return product


class SubscriptionProductCreator(ProductCreator):
    """
    Factory para criar produtos de assinatura.

    Produtos de assinatura:
    - Serviço recorrente
    - Disponibilidade ilimitada
    - Exemplos: planos mensais, memberships, SaaS
    """

    UNLIMITED_STOCK = 999

    def create_product(self, product_data: Dict[str, Any]) -> Product:
        """
        Cria um produto de assinatura.

        Args:
            product_data: Informações do produto

        Returns:
            Product: Instância de produto de assinatura
        """
        # Adiciona sufixo /mês à descrição se não estiver presente
        description = product_data['description']
        if not description.lower().endswith(('/month', '/mês')):
            description += " (Assinatura mensal recorrente)"

        product = Product(
            name=product_data['name'],
            description=description,
            price=product_data['price'],
            type='subscription',
            stock=self.UNLIMITED_STOCK  # Assinaturas têm disponibilidade ilimitada
        )
        return product


class ProductFactory:
    """
    Classe factory principal que delega a criação de produtos para criadores específicos.

    Usa o padrão Factory Method para criar diferentes tipos de produtos sem
    lógica condicional complexa.
    """

    _creators = {
        'physical': PhysicalProductCreator(),
        'digital': DigitalProductCreator(),
        'subscription': SubscriptionProductCreator(),
    }

    @classmethod
    def create_product(cls, product_type: str, product_data: Dict[str, Any]) -> Product:
        """
        Cria um produto do tipo especificado.

        Args:
            product_type: Tipo de produto (physical, digital, subscription)
            product_data: Informações do produto

        Returns:
            Product: Instância do produto criada

        Raises:
            ValueError: Se o tipo de produto não for suportado
        """
        creator = cls._creators.get(product_type.lower())
        if not creator:
            raise ValueError(
                f"Tipo de produto desconhecido: {product_type}. "
                f"Tipos suportados: {', '.join(cls._creators.keys())}"
            )

        return creator.create_product(product_data)

    @classmethod
    def get_supported_types(cls) -> list[str]:
        """
        Obtém lista de tipos de produtos suportados.

        Returns:
            list[str]: Lista de nomes dos tipos de produtos
        """
        return list(cls._creators.keys())
