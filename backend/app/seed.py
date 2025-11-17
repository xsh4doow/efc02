"""
Script para popular banco de dados com dados de demonstração

Execute: python -m app.seed
"""

from app.database import get_db
from app.factories.product_factory import ProductFactory
from app.repositories.product_repository import ProductRepository


def seed_products():
    """Popula banco de dados com produtos de demonstração."""

    print("[SEED] Populando banco de dados com produtos...")

    db = get_db()
    session = db.get_session()
    product_repo = ProductRepository(session)

    # Verifica se já existem produtos
    if product_repo.count() > 0:
        print("[AVISO] Banco de dados ja possui produtos. Pulando seed.")
        session.close()
        return

    # Define produtos de demonstração
    products_data = [
        {
            "type": "physical",
            "data": {
                "name": "Notebook Gamer",
                "description": "Notebook de alta performance para jogos e trabalho pesado. Intel i7, 16GB RAM, RTX 3060, SSD 512GB.",
                "price": 5999.00,
                "stock": 10
            }
        },
        {
            "type": "digital",
            "data": {
                "name": "Curso de Python Completo",
                "description": "Curso completo de Python do básico ao avançado. Inclui projetos práticos e certificado.",
                "price": 299.00,
                "stock": 999  # Ilimitado
            }
        },
        {
            "type": "subscription",
            "data": {
                "name": "Plano Premium",
                "description": "Acesso ilimitado a todos os cursos e conteúdos exclusivos",
                "price": 99.00,
                "stock": 999  # Ilimitado
            }
        },
        {
            "type": "physical",
            "data": {
                "name": "Mouse Gamer RGB",
                "description": "Mouse gamer com iluminação RGB, 7 botões programáveis, DPI ajustável até 16000.",
                "price": 249.00,
                "stock": 50
            }
        },
        {
            "type": "digital",
            "data": {
                "name": "E-book Design Patterns",
                "description": "Guia completo sobre padrões de projeto em programação. 500 páginas com exemplos práticos.",
                "price": 49.00,
                "stock": 999  # Ilimitado
            }
        },
        {
            "type": "physical",
            "data": {
                "name": "Teclado Mecânico",
                "description": "Teclado mecânico com switches blue, iluminação RGB, ABNT2.",
                "price": 399.00,
                "stock": 30
            }
        },
        {
            "type": "physical",
            "data": {
                "name": "Headset Gamer",
                "description": "Headset com som surround 7.1, microfone removível, almofadas confortáveis.",
                "price": 299.00,
                "stock": 25
            }
        },
        {
            "type": "digital",
            "data": {
                "name": "Pack de Templates Web",
                "description": "Coleção com 50 templates responsivos para sites e landing pages.",
                "price": 149.00,
                "stock": 999  # Ilimitado
            }
        }
    ]

    # Cria produtos usando Factory Method Pattern
    created_count = 0
    for item in products_data:
        try:
            product = ProductFactory.create_product(
                product_type=item["type"],
                product_data=item["data"]
            )
            product_repo.create(product)
            created_count += 1
            print(f"[OK] Criado: {product.name} ({product.type})")

        except Exception as e:
            print(f"[ERRO] Erro ao criar produto: {str(e)}")

    session.close()
    print(f"\n[SUCESSO] Seed completo! {created_count} produtos criados.")


def main():
    """Função principal."""
    print("=" * 60)
    print("SEED DE DADOS - E-COMMERCE")
    print("=" * 60)

    # Garante que as tabelas existam
    db = get_db()
    db.create_tables()

    # Popula produtos
    seed_products()

    print("=" * 60)
    print("[CONCLUIDO] Processo de seed finalizado!")
    print("=" * 60)


if __name__ == "__main__":
    main()
