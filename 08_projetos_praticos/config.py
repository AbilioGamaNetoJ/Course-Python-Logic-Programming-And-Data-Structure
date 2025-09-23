"""
CONFIGURAÇÕES CENTRALIZADAS DO SISTEMA
=====================================

Este módulo centraliza todas as configurações do sistema de gestão empresarial,
permitindo fácil manutenção e personalização sem alterar o código principal.
"""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any
from pathlib import Path


class LogLevel(Enum):
    """Níveis de logging disponíveis."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LoggingConfig:
    """Configurações de logging."""
    level: LogLevel = LogLevel.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: str = "sistema_gestao.log"
    console_output: bool = True
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


@dataclass
class DatabaseConfig:
    """Configurações de banco de dados."""
    type: str = "memory"  # memory, sqlite, postgresql, etc.
    host: str = "localhost"
    port: int = 5432
    database: str = "gestao_empresarial"
    username: str = ""
    password: str = ""
    connection_pool_size: int = 10
    timeout: int = 30


@dataclass
class BusinessConfig:
    """Configurações de regras de negócio."""
    default_credit_limit: float = 5000.0
    min_stock_level: int = 5
    max_items_per_order: int = 100
    currency: str = "BRL"
    tax_rate: float = 0.18  # 18% de impostos
    discount_threshold: float = 1000.0  # Desconto acima de R$ 1000
    discount_rate: float = 0.05  # 5% de desconto
    
    # Validações
    min_product_price: float = 0.01
    max_product_price: float = 999999.99
    min_customer_age: int = 18
    max_customer_name_length: int = 100


@dataclass
class SecurityConfig:
    """Configurações de segurança."""
    password_min_length: int = 8
    session_timeout: int = 3600  # 1 hora em segundos
    max_login_attempts: int = 3
    lockout_duration: int = 900  # 15 minutos em segundos
    encryption_key: str = ""  # Deve ser definida no .env
    jwt_secret: str = ""  # Deve ser definida no .env
    jwt_expiration: int = 86400  # 24 horas em segundos


@dataclass
class SystemConfig:
    """Configurações gerais do sistema."""
    app_name: str = "Sistema de Gestão Empresarial"
    version: str = "1.0.0"
    debug_mode: bool = False
    init_sample_data: bool = True
    backup_directory: str = "backups"
    export_directory: str = "exports"
    temp_directory: str = "temp"
    max_file_upload_size: int = 50 * 1024 * 1024  # 50MB
    
    # Performance
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hora
    pagination_size: int = 50
    max_search_results: int = 1000


@dataclass
class Config:
    """Configuração principal do sistema."""
    logging: LoggingConfig
    database: DatabaseConfig
    business: BusinessConfig
    security: SecurityConfig
    system: SystemConfig
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Cria configuração a partir de variáveis de ambiente."""
        # Carregar variáveis do arquivo .env se existir
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        
        # Logging
        logging_config = LoggingConfig(
            level=LogLevel(os.getenv('LOG_LEVEL', 'INFO')),
            format=os.getenv('LOG_FORMAT', "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            log_file=os.getenv('LOG_FILE', 'sistema_gestao.log'),
            console_output=os.getenv('LOG_CONSOLE', 'true').lower() == 'true',
            max_file_size=int(os.getenv('LOG_MAX_SIZE', '10485760')),  # 10MB
            backup_count=int(os.getenv('LOG_BACKUP_COUNT', '5'))
        )
        
        # Database
        database_config = DatabaseConfig(
            type=os.getenv('DB_TYPE', 'memory'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME', 'gestao_empresarial'),
            username=os.getenv('DB_USER', ''),
            password=os.getenv('DB_PASSWORD', ''),
            connection_pool_size=int(os.getenv('DB_POOL_SIZE', '10')),
            timeout=int(os.getenv('DB_TIMEOUT', '30'))
        )
        
        # Business
        business_config = BusinessConfig(
            default_credit_limit=float(os.getenv('DEFAULT_CREDIT_LIMIT', '5000.0')),
            min_stock_level=int(os.getenv('MIN_STOCK_LEVEL', '5')),
            max_items_per_order=int(os.getenv('MAX_ITEMS_PER_ORDER', '100')),
            currency=os.getenv('CURRENCY', 'BRL'),
            tax_rate=float(os.getenv('TAX_RATE', '0.18')),
            discount_threshold=float(os.getenv('DISCOUNT_THRESHOLD', '1000.0')),
            discount_rate=float(os.getenv('DISCOUNT_RATE', '0.05')),
            min_product_price=float(os.getenv('MIN_PRODUCT_PRICE', '0.01')),
            max_product_price=float(os.getenv('MAX_PRODUCT_PRICE', '999999.99')),
            min_customer_age=int(os.getenv('MIN_CUSTOMER_AGE', '18')),
            max_customer_name_length=int(os.getenv('MAX_CUSTOMER_NAME_LENGTH', '100'))
        )
        
        # Security
        security_config = SecurityConfig(
            password_min_length=int(os.getenv('PASSWORD_MIN_LENGTH', '8')),
            session_timeout=int(os.getenv('SESSION_TIMEOUT', '3600')),
            max_login_attempts=int(os.getenv('MAX_LOGIN_ATTEMPTS', '3')),
            lockout_duration=int(os.getenv('LOCKOUT_DURATION', '900')),
            encryption_key=os.getenv('ENCRYPTION_KEY', ''),
            jwt_secret=os.getenv('JWT_SECRET', ''),
            jwt_expiration=int(os.getenv('JWT_EXPIRATION', '86400'))
        )
        
        # System
        system_config = SystemConfig(
            app_name=os.getenv('APP_NAME', 'Sistema de Gestão Empresarial'),
            version=os.getenv('APP_VERSION', '1.0.0'),
            debug_mode=os.getenv('DEBUG_MODE', 'false').lower() == 'true',
            init_sample_data=os.getenv('INIT_SAMPLE_DATA', 'true').lower() == 'true',
            backup_directory=os.getenv('BACKUP_DIR', 'backups'),
            export_directory=os.getenv('EXPORT_DIR', 'exports'),
            temp_directory=os.getenv('TEMP_DIR', 'temp'),
            max_file_upload_size=int(os.getenv('MAX_FILE_UPLOAD_SIZE', '52428800')),  # 50MB
            cache_enabled=os.getenv('CACHE_ENABLED', 'true').lower() == 'true',
            cache_ttl=int(os.getenv('CACHE_TTL', '3600')),
            pagination_size=int(os.getenv('PAGINATION_SIZE', '50')),
            max_search_results=int(os.getenv('MAX_SEARCH_RESULTS', '1000'))
        )
        
        return cls(
            logging=logging_config,
            database=database_config,
            business=business_config,
            security=security_config,
            system=system_config
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário."""
        return {
            'logging': {
                'level': self.logging.level.value,
                'format': self.logging.format,
                'log_file': self.logging.log_file,
                'console_output': self.logging.console_output,
                'max_file_size': self.logging.max_file_size,
                'backup_count': self.logging.backup_count
            },
            'database': {
                'type': self.database.type,
                'host': self.database.host,
                'port': self.database.port,
                'database': self.database.database,
                'username': self.database.username,
                'connection_pool_size': self.database.connection_pool_size,
                'timeout': self.database.timeout
            },
            'business': {
                'default_credit_limit': self.business.default_credit_limit,
                'min_stock_level': self.business.min_stock_level,
                'max_items_per_order': self.business.max_items_per_order,
                'currency': self.business.currency,
                'tax_rate': self.business.tax_rate,
                'discount_threshold': self.business.discount_threshold,
                'discount_rate': self.business.discount_rate,
                'min_product_price': self.business.min_product_price,
                'max_product_price': self.business.max_product_price,
                'min_customer_age': self.business.min_customer_age,
                'max_customer_name_length': self.business.max_customer_name_length
            },
            'security': {
                'password_min_length': self.security.password_min_length,
                'session_timeout': self.security.session_timeout,
                'max_login_attempts': self.security.max_login_attempts,
                'lockout_duration': self.security.lockout_duration,
                'jwt_expiration': self.security.jwt_expiration
            },
            'system': {
                'app_name': self.system.app_name,
                'version': self.system.version,
                'debug_mode': self.system.debug_mode,
                'init_sample_data': self.system.init_sample_data,
                'backup_directory': self.system.backup_directory,
                'export_directory': self.system.export_directory,
                'temp_directory': self.system.temp_directory,
                'max_file_upload_size': self.system.max_file_upload_size,
                'cache_enabled': self.system.cache_enabled,
                'cache_ttl': self.system.cache_ttl,
                'pagination_size': self.system.pagination_size,
                'max_search_results': self.system.max_search_results
            }
        }
    
    def validate(self) -> bool:
        """Valida as configurações."""
        errors = []
        
        # Validar configurações de negócio
        if self.business.default_credit_limit < 0:
            errors.append("Limite de crédito padrão deve ser positivo")
        
        if self.business.min_stock_level < 0:
            errors.append("Estoque mínimo deve ser positivo")
        
        if self.business.tax_rate < 0 or self.business.tax_rate > 1:
            errors.append("Taxa de imposto deve estar entre 0 e 1")
        
        # Validar configurações de segurança
        if self.security.password_min_length < 4:
            errors.append("Comprimento mínimo da senha deve ser pelo menos 4")
        
        if self.security.session_timeout < 60:
            errors.append("Timeout da sessão deve ser pelo menos 60 segundos")
        
        # Validar configurações do sistema
        if self.system.pagination_size < 1:
            errors.append("Tamanho da paginação deve ser pelo menos 1")
        
        if self.system.max_search_results < 1:
            errors.append("Máximo de resultados de busca deve ser pelo menos 1")
        
        if errors:
            print("Erros de configuração encontrados:")
            for error in errors:
                print(f"- {error}")
            return False
        
        return True
    
    def create_directories(self):
        """Cria diretórios necessários."""
        directories = [
            self.system.backup_directory,
            self.system.export_directory,
            self.system.temp_directory
        ]
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)


# Instância global de configuração
config = Config.from_env()

# Validar configurações na inicialização
if not config.validate():
    raise ValueError("Configurações inválidas encontradas")

# Criar diretórios necessários
config.create_directories()


def get_config() -> Config:
    """Retorna a instância global de configuração."""
    return config


def reload_config():
    """Recarrega as configurações."""
    global config
    config = Config.from_env()
    if not config.validate():
        raise ValueError("Configurações inválidas encontradas após reload")
    config.create_directories()


# Configurações específicas para desenvolvimento
if config.system.debug_mode:
    print("MODO DEBUG ATIVADO")
    print(f"Configurações carregadas: {config.system.app_name} v{config.system.version}")
    
    # Em modo debug, mostrar configurações (sem dados sensíveis)
    config_dict = config.to_dict()
    # Remover dados sensíveis do debug
    if 'database' in config_dict:
        config_dict['database'].pop('password', None)
    
    import json
    print("Configurações atuais:")
    print(json.dumps(config_dict, indent=2, ensure_ascii=False))