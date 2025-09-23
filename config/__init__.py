# -*- coding: utf-8 -*-
"""
MÓDULO DE CONFIGURAÇÃO
=====================

Módulo centralizado para gerenciamento de configurações do sistema.
"""

from .settings import (
    config,
    ConfigManager,
    Environment,
    LogLevel,
    DatabaseConfig,
    LoggingConfig,
    BackupConfig,
    SecurityConfig,
    PerformanceConfig,
    BusinessConfig
)

__all__ = [
    'config',
    'ConfigManager',
    'Environment',
    'LogLevel',
    'DatabaseConfig',
    'LoggingConfig',
    'BackupConfig',
    'SecurityConfig',
    'PerformanceConfig',
    'BusinessConfig'
]