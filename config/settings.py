# -*- coding: utf-8 -*-
"""
MÓDULO DE CONFIGURAÇÃO CENTRALIZADA
===================================

Este módulo gerencia todas as configurações do sistema através de variáveis
de ambiente, proporcionando flexibilidade e segurança na configuração.

Funcionalidades:
- Carregamento automático de variáveis .env
- Validação de configurações obrigatórias
- Valores padrão seguros
- Configurações específicas por ambiente
- Validação de tipos e ranges
"""

import os
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class Environment(Enum):
    """Ambientes de execução suportados."""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class LogLevel(Enum):
    """Níveis de log suportados."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class DatabaseConfig:
    """Configurações de banco de dados."""
    type: str = "memory"  # memory, sqlite, postgresql, mysql
    host: str = "localhost"
    port: int = 5432
    name: str = "sistema_gestao"
    user: str = ""
    password: str = ""
    path: str = "./data/sistema_gestao.db"


@dataclass
class LoggingConfig:
    """Configurações de logging."""
    level: str = "INFO"
    file: str = "sistema_gestao.log"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    console: bool = True
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


@dataclass
class BackupConfig:
    """Configurações de backup."""
    directory: str = "./backups"
    format: str = "json"
    auto_enabled: bool = False
    interval_hours: int = 24
    max_backups: int = 30


@dataclass
class SecurityConfig:
    """Configurações de segurança."""
    secret_key: str = "default-secret-key-CHANGE-IN-PRODUCTION"
    password_salt: str = "default-salt-CHANGE-IN-PRODUCTION"
    max_login_attempts: int = 3
    session_timeout: int = 3600  # 1 hora


@dataclass
class PerformanceConfig:
    """Configurações de performance."""
    max_cache_size: int = 1000
    operation_timeout: int = 30
    max_threads: int = 4
    batch_size: int = 100


@dataclass
class BusinessConfig:
    """Configurações de regras de negócio."""
    min_stock_level: int = 5
    default_credit_limit: float = 1000.0
    max_discount_percent: float = 50.0
    items_per_page: int = 10


class ConfigManager:
    """Gerenciador centralizado de configurações."""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Inicializa o gerenciador de configurações.
        
        Args:
            env_file: Caminho para arquivo .env personalizado
        """
        self.env_file = env_file or self._find_env_file()
        self._load_env_file()
        self._validate_environment()
        
        # Carregar configurações
        self.system = self._load_app_config()
        self.database = self._load_database_config()
        self.logging = self._load_logging_config()
        self.backup = self._load_backup_config()
        self.security = self._load_security_config()
        self.performance = self._load_performance_config()
        self.business = self._load_business_config()
    
    def _find_env_file(self) -> Optional[str]:
        """Encontra arquivo .env no projeto."""
        current_dir = Path(__file__).parent.parent
        env_paths = [
            current_dir / ".env",
            current_dir.parent / ".env",
            Path.cwd() / ".env"
        ]
        
        for path in env_paths:
            if path.exists():
                return str(path)
        return None
    
    def _load_env_file(self):
        """Carrega variáveis do arquivo .env."""
        if not self.env_file or not Path(self.env_file).exists():
            print("⚠️  Arquivo .env não encontrado. Usando configurações padrão.")
            return
        
        try:
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            print(f"✓ Configurações carregadas de: {self.env_file}")
        except Exception as e:
            print(f"⚠️  Erro ao carregar .env: {e}")
    
    def _validate_environment(self):
        """Valida configurações críticas."""
        env = self.get_env("ENVIRONMENT", "development")
        if env == "production":
            # Validações específicas para produção
            secret = self.get_env("SECRET_KEY", "")
            if not secret or secret == "default-secret-key-CHANGE-IN-PRODUCTION":
                raise ValueError("SECRET_KEY deve ser configurada em produção!")
            
            salt = self.get_env("PASSWORD_SALT", "")
            if not salt or salt == "default-salt-CHANGE-IN-PRODUCTION":
                raise ValueError("PASSWORD_SALT deve ser configurado em produção!")
    
    def get_env(self, key: str, default: Any = None, type_cast: type = str) -> Any:
        """
        Obtém variável de ambiente com conversão de tipo.
        
        Args:
            key: Nome da variável
            default: Valor padrão
            type_cast: Tipo para conversão
            
        Returns:
            Valor convertido ou padrão
        """
        value = os.environ.get(key, default)
        
        if value is None:
            return None
        
        if type_cast == bool:
            return str(value).lower() in ('true', '1', 'yes', 'on')
        elif type_cast == int:
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        elif type_cast == float:
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        else:
            return type_cast(value)
    
    def _load_app_config(self) -> Dict[str, Any]:
        """Carrega configurações da aplicação."""
        return {
            'name': self.get_env('APP_NAME', 'Sistema de Gestão Empresarial'),
            'version': self.get_env('APP_VERSION', '1.0.0'),
            'environment': self.get_env('ENVIRONMENT', 'development'),
            'debug': self.get_env('DEBUG', False, bool),
            'init_sample_data': self.get_env('INIT_SAMPLE_DATA', True, bool)
        }
    
    def _load_database_config(self) -> DatabaseConfig:
        """Carrega configurações de banco de dados."""
        return DatabaseConfig(
            type=self.get_env('DB_TYPE', 'memory'),
            host=self.get_env('DB_HOST', 'localhost'),
            port=self.get_env('DB_PORT', 5432, int),
            name=self.get_env('DB_NAME', 'sistema_gestao'),
            user=self.get_env('DB_USER', ''),
            password=self.get_env('DB_PASSWORD', ''),
            path=self.get_env('DB_PATH', './data/sistema_gestao.db')
        )
    
    def _load_logging_config(self) -> LoggingConfig:
        """Carrega configurações de logging."""
        return LoggingConfig(
            level=self.get_env('LOG_LEVEL', 'INFO'),
            file=self.get_env('LOG_FILE', 'sistema_gestao.log'),
            format=self.get_env('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            console=self.get_env('LOG_CONSOLE', True, bool),
            max_file_size=self.get_env('LOG_MAX_SIZE', 10 * 1024 * 1024, int),
            backup_count=self.get_env('LOG_BACKUP_COUNT', 5, int)
        )
    
    def _load_backup_config(self) -> BackupConfig:
        """Carrega configurações de backup."""
        return BackupConfig(
            directory=self.get_env('BACKUP_DIR', './backups'),
            format=self.get_env('BACKUP_FORMAT', 'json'),
            auto_enabled=self.get_env('AUTO_BACKUP', False, bool),
            interval_hours=self.get_env('BACKUP_INTERVAL', 24, int),
            max_backups=self.get_env('MAX_BACKUPS', 30, int)
        )
    
    def _load_security_config(self) -> SecurityConfig:
        """Carrega configurações de segurança."""
        return SecurityConfig(
            secret_key=self.get_env('SECRET_KEY', 'default-secret-key-CHANGE-IN-PRODUCTION'),
            password_salt=self.get_env('PASSWORD_SALT', 'default-salt-CHANGE-IN-PRODUCTION'),
            max_login_attempts=self.get_env('MAX_LOGIN_ATTEMPTS', 3, int),
            session_timeout=self.get_env('SESSION_TIMEOUT', 3600, int)
        )
    
    def _load_performance_config(self) -> PerformanceConfig:
        """Carrega configurações de performance."""
        return PerformanceConfig(
            max_cache_size=self.get_env('MAX_CACHE_SIZE', 1000, int),
            operation_timeout=self.get_env('OPERATION_TIMEOUT', 30, int),
            max_threads=self.get_env('MAX_THREADS', 4, int),
            batch_size=self.get_env('BATCH_SIZE', 100, int)
        )
    
    def _load_business_config(self) -> BusinessConfig:
        """Carrega configurações de regras de negócio."""
        return BusinessConfig(
            min_stock_level=self.get_env('DEFAULT_MIN_STOCK', 5, int),
            default_credit_limit=self.get_env('DEFAULT_CREDIT_LIMIT', 1000.0, float),
            max_discount_percent=self.get_env('MAX_DISCOUNT_PERCENT', 50.0, float),
            items_per_page=self.get_env('ITEMS_PER_PAGE', 10, int)
        )
    
    def is_development(self) -> bool:
        """Verifica se está em ambiente de desenvolvimento."""
        return self.app['environment'] == Environment.DEVELOPMENT.value
    
    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção."""
        return self.app['environment'] == Environment.PRODUCTION.value
    
    def is_test(self) -> bool:
        """Verifica se está em ambiente de teste."""
        return self.app['environment'] == Environment.TEST.value
    
    def get_log_level(self) -> int:
        """Retorna nível de log como constante do logging."""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return level_map.get(self.logging.level.upper(), logging.INFO)
    
    def create_directories(self):
        """Cria diretórios necessários."""
        directories = [
            Path(self.backup.directory),
            Path(self.logging.file).parent,
            Path(self.database.path).parent if self.database.type == 'sqlite' else None
        ]
        
        for directory in directories:
            if directory and not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
                print(f"✓ Diretório criado: {directory}")
    
    def validate_config(self) -> List[str]:
        """
        Valida todas as configurações.
        
        Returns:
            Lista de erros encontrados
        """
        errors = []
        
        # Validar configurações de negócio
        if self.business.min_stock_level < 0:
            errors.append("DEFAULT_MIN_STOCK deve ser >= 0")
        
        if self.business.default_credit_limit < 0:
            errors.append("DEFAULT_CREDIT_LIMIT deve ser >= 0")
        
        if not (0 <= self.business.max_discount_percent <= 100):
            errors.append("MAX_DISCOUNT_PERCENT deve estar entre 0 e 100")
        
        # Validar configurações de performance
        if self.performance.max_cache_size <= 0:
            errors.append("MAX_CACHE_SIZE deve ser > 0")
        
        if self.performance.operation_timeout <= 0:
            errors.append("OPERATION_TIMEOUT deve ser > 0")
        
        # Validar configurações de backup
        if self.backup.interval_hours <= 0:
            errors.append("BACKUP_INTERVAL deve ser > 0")
        
        return errors
    
    def __str__(self) -> str:
        """Representação string das configurações."""
        return f"""
Configurações do Sistema:
========================
App: {self.app['name']} v{self.app['version']}
Ambiente: {self.app['environment']}
Log Level: {self.logging.level}
Backup: {'Habilitado' if self.backup.auto_enabled else 'Desabilitado'}
Cache: {self.performance.max_cache_size} itens
"""


# Instância global de configuração
config = ConfigManager()

# Criar diretórios necessários
config.create_directories()

# Validar configurações
validation_errors = config.validate_config()
if validation_errors:
    print("⚠️  Erros de configuração encontrados:")
    for error in validation_errors:
        print(f"   - {error}")