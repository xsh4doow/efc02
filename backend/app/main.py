"""
Aplicação Principal FastAPI - E-commerce com Padrões de Projeto

Este sistema demonstra a aplicação prática de 6 padrões de projeto:
1. Singleton - ConfigManager e DatabaseManager
2. Repository - Abstração de acesso a dados
3. Factory Method - Criação de produtos e pedidos
4. Strategy - Métodos de pagamento
5. Observer - Notificações de pedidos
6. Decorator - Extras de pedidos
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_config
from app.database import get_db
from app.routers import products, customers, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia ciclo de vida da aplicação.

    Executado na inicialização e encerramento do app.
    """
    # Startup: Cria tabelas do banco de dados
    print("[STARTUP] Iniciando aplicacao...")
    db = get_db()
    db.create_tables()
    print("[OK] Tabelas do banco de dados criadas/verificadas")

    yield

    # Shutdown
    print("[SHUTDOWN] Encerrando aplicacao...")


# Cria instância do FastAPI
config = get_config()
app = FastAPI(
    title=config.settings.app_name,
    version=config.settings.app_version,
    description="""
    Sistema de E-commerce demonstrando padrões de projeto.

    ## Padrões Implementados

    ### 1. Singleton
    - **Localização**: `app/config.py`, `app/database.py`
    - **Uso**: Garante instância única de configuração e banco de dados

    ### 2. Repository
    - **Localização**: `app/repositories/`
    - **Uso**: Abstrai acesso a dados do banco

    ### 3. Factory Method
    - **Localização**: `app/factories/`
    - **Uso**: Cria diferentes tipos de pedidos e produtos

    ### 4. Strategy
    - **Localização**: `app/strategies/`
    - **Uso**: Diferentes métodos de pagamento (cartão/pix/boleto)

    ### 5. Observer
    - **Localização**: `app/observers/`
    - **Uso**: Notificações automáticas de mudança de status

    ### 6. Decorator
    - **Localização**: `app/decorators/`
    - **Uso**: Adiciona extras aos pedidos dinamicamente
    """,
    lifespan=lifespan
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra routers
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)


@app.get("/")
def root():
    """Endpoint raiz com informações do sistema."""
    return {
        "message": "Sistema de E-commerce com Padrões de Projeto",
        "version": config.settings.app_version,
        "patterns": [
            "Singleton",
            "Repository",
            "Factory Method",
            "Strategy",
            "Observer",
            "Decorator"
        ],
        "endpoints": {
            "docs": "/docs",
            "products": "/api/products",
            "customers": "/api/customers",
            "orders": "/api/orders"
        }
    }


@app.get("/health")
def health_check():
    """Verifica saúde da aplicação."""
    return {
        "status": "healthy",
        "database": "connected",
        "version": config.settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.settings.api_host,
        port=config.settings.api_port,
        reload=config.settings.api_reload
    )
