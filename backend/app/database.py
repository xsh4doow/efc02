"""
Gerenciador de Banco de Dados - Implementação do Padrão Singleton

PADRÃO DE PROJETO: Singleton
PROPÓSITO: Garantir uma única conexão de banco de dados em toda a aplicação
BENEFÍCIO: Previne múltiplas conexões e garante estado consistente do banco de dados
"""

from typing import Optional, Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import get_config

# Classe base para todos os models
Base = declarative_base()


class DatabaseManager:
    """
    Gerenciador de Banco de Dados Singleton

    Gerencia a conexão com o banco SQLite e criação de sessões.
    Garante que apenas um engine de banco de dados existe em toda a aplicação.
    """

    _instance: Optional['DatabaseManager'] = None
    _engine: Optional[Engine] = None
    _session_factory: Optional[sessionmaker] = None

    def __new__(cls) -> 'DatabaseManager':
        """
        Sobrescreve __new__ para controlar criação de instância (padrão Singleton).

        Returns:
            DatabaseManager: A única instância do DatabaseManager
        """
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Inicializa o engine do banco de dados e a factory de sessões."""
        config = get_config()

        # Cria o engine
        self._engine = create_engine(
            config.settings.database_url,
            connect_args={"check_same_thread": False},  # Necessário para SQLite
            echo=config.settings.debug  # Loga queries SQL em modo debug
        )

        # Cria a factory de sessões
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

    @property
    def engine(self) -> Engine:
        """
        Obtém o engine do banco de dados.

        Returns:
            Engine: Instância do engine SQLAlchemy
        """
        return self._engine

    def get_session(self) -> Session:
        """
        Cria uma nova sessão de banco de dados.

        Returns:
            Session: Instância de sessão SQLAlchemy
        """
        return self._session_factory()

    def create_tables(self) -> None:
        """Cria todas as tabelas do banco de dados."""
        Base.metadata.create_all(bind=self._engine)

    def drop_tables(self) -> None:
        """Remove todas as tabelas do banco de dados (use com cuidado!)."""
        Base.metadata.drop_all(bind=self._engine)

    def __repr__(self) -> str:
        return f"<DatabaseManager(engine='{self._engine.url}')>"


# Função global para obter instância do banco de dados
def get_db() -> DatabaseManager:
    """
    Obtém a instância singleton do DatabaseManager.

    Returns:
        DatabaseManager: O gerenciador de banco de dados singleton
    """
    return DatabaseManager()


# Dependência para rotas FastAPI
def get_db_session() -> Generator[Session, None, None]:
    """
    Dependência FastAPI para obter sessão do banco de dados.

    Yields:
        Session: Sessão do banco de dados que será automaticamente fechada
    """
    db_manager = get_db()
    session = db_manager.get_session()
    try:
        yield session
    finally:
        session.close()
