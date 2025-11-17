"""
Gerenciador de Configuração - Implementação do Padrão Singleton

PADRÃO DE PROJETO: Singleton
PROPÓSITO: Garantir uma única instância de configuração em toda a aplicação
BENEFÍCIO: Previne múltiplas instâncias e garante estado de configuração consistente
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Configurações da aplicação"""

    # Banco de dados
    database_url: str = "sqlite:///./ecommerce.db"

    # Configuração da API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # CORS
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000,localhost:3000,localhost:8000"

    # Aplicação
    app_name: str = "E-commerce System"
    app_version: str = "1.0.0"
    debug: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


class ConfigManager:
    """
    Gerenciador de Configuração Singleton

    Garante que apenas uma instância de configuração existe em toda a aplicação.
    Isso previne inconsistências e uso desnecessário de recursos.
    """

    _instance: Optional['ConfigManager'] = None
    _settings: Optional[Settings] = None

    def __new__(cls) -> 'ConfigManager':
        """
        Sobrescreve __new__ para controlar criação de instância (padrão Singleton).

        Returns:
            ConfigManager: A única instância do ConfigManager
        """
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._settings = Settings()
        return cls._instance

    @property
    def settings(self) -> Settings:
        """
        Obtém configurações da aplicação.

        Returns:
            Settings: Configurações da aplicação
        """
        return self._settings

    def get_cors_origins(self) -> list[str]:
        """
        Obtém origens CORS como uma lista.

        Returns:
            list[str]: Lista de origens CORS permitidas
        """
        return [origin.strip() for origin in self._settings.cors_origins.split(',')]

    def __repr__(self) -> str:
        return f"<ConfigManager(app_name='{self._settings.app_name}', version='{self._settings.app_version}')>"


# Função global para obter instância de config
def get_config() -> ConfigManager:
    """
    Obtém a instância singleton do ConfigManager.

    Returns:
        ConfigManager: O gerenciador de configuração singleton
    """
    return ConfigManager()
