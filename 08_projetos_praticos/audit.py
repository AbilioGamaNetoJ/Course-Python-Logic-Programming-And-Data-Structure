"""
MÓDULO DE AUDITORIA
==================

Este módulo contém as classes responsáveis pelo sistema de auditoria
e logging de operações do sistema de gestão empresarial.
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import logging

# Adicionar o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import TipoOperacao, LogAuditoria
from repositories import RepositorioMemoria
from config import get_config


class SistemaAuditoria:
    """
    Sistema de auditoria para rastreamento de operações.
    """
    
    def __init__(self):
        """Inicializa o sistema de auditoria."""
        self.repositorio_logs = RepositorioMemoria(LogAuditoria)
        self.config = get_config()
        self.logger = logging.getLogger(__name__)
        
        # Configurar logging específico para auditoria
        self._configurar_logging_auditoria()
    
    def _configurar_logging_auditoria(self):
        """Configura logging específico para auditoria."""
        # Handler específico para logs de auditoria
        audit_handler = logging.FileHandler('auditoria.log', encoding='utf-8')
        audit_formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(levelname)s - %(message)s'
        )
        audit_handler.setFormatter(audit_formatter)
        
        # Logger específico para auditoria
        self.audit_logger = logging.getLogger('auditoria')
        self.audit_logger.addHandler(audit_handler)
        self.audit_logger.setLevel(logging.INFO)
    
    def registrar_operacao(self, tipo: TipoOperacao, entidade: str, entidade_id: str, 
                          usuario: str, detalhes: Optional[Dict[str, Any]] = None):
        """
        Registra uma operação no sistema de auditoria.
        
        Args:
            tipo: Tipo da operação
            entidade: Nome da entidade afetada
            entidade_id: ID da entidade
            usuario: Usuário que executou a operação
            detalhes: Detalhes adicionais da operação
        """
        try:
            # Criar log de auditoria
            log = LogAuditoria(
                id=self._gerar_id_log(),
                timestamp=datetime.now(),
                tipo_operacao=tipo,
                entidade=entidade,
                entidade_id=entidade_id,
                usuario=usuario,
                detalhes=detalhes or {},
                ip_origem="127.0.0.1",  # Em um sistema real, seria obtido da requisição
                user_agent="Sistema Interno"  # Em um sistema real, seria obtido da requisição
            )
            
            # Salvar no repositório
            self.repositorio_logs.criar(log)
            
            # Log no arquivo de auditoria
            self.audit_logger.info(
                f"Operação: {tipo.value} | Entidade: {entidade} | ID: {entidade_id} | "
                f"Usuário: {usuario} | Detalhes: {detalhes}"
            )
            
            self.logger.debug(f"Operação de auditoria registrada: {log.id}")
            
        except Exception as e:
            self.logger.error(f"Erro ao registrar operação de auditoria: {e}")
    
    def _gerar_id_log(self) -> str:
        """Gera ID único para o log."""
        import uuid
        return str(uuid.uuid4())
    
    def buscar_logs_por_entidade(self, entidade: str, entidade_id: str) -> List[LogAuditoria]:
        """
        Busca logs por entidade específica.
        
        Args:
            entidade: Nome da entidade
            entidade_id: ID da entidade
            
        Returns:
            Lista de logs da entidade
        """
        try:
            logs = self.repositorio_logs.listar()
            logs_entidade = [
                log for log in logs 
                if log.entidade == entidade and log.entidade_id == entidade_id
            ]
            
            # Ordenar por timestamp (mais recente primeiro)
            logs_entidade.sort(key=lambda x: x.timestamp, reverse=True)
            
            return logs_entidade
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar logs por entidade: {e}")
            return []
    
    def buscar_logs_por_usuario(self, usuario: str, limite: Optional[int] = None) -> List[LogAuditoria]:
        """
        Busca logs por usuário.
        
        Args:
            usuario: Nome do usuário
            limite: Limite de logs a retornar
            
        Returns:
            Lista de logs do usuário
        """
        try:
            logs = self.repositorio_logs.listar()
            logs_usuario = [log for log in logs if log.usuario == usuario]
            
            # Ordenar por timestamp (mais recente primeiro)
            logs_usuario.sort(key=lambda x: x.timestamp, reverse=True)
            
            if limite:
                logs_usuario = logs_usuario[:limite]
            
            return logs_usuario
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar logs por usuário: {e}")
            return []
    
    def buscar_logs_por_periodo(self, data_inicio: datetime, data_fim: datetime) -> List[LogAuditoria]:
        """
        Busca logs por período.
        
        Args:
            data_inicio: Data de início
            data_fim: Data de fim
            
        Returns:
            Lista de logs do período
        """
        try:
            logs = self.repositorio_logs.listar()
            logs_periodo = [
                log for log in logs 
                if data_inicio <= log.timestamp <= data_fim
            ]
            
            # Ordenar por timestamp (mais recente primeiro)
            logs_periodo.sort(key=lambda x: x.timestamp, reverse=True)
            
            return logs_periodo
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar logs por período: {e}")
            return []
    
    def buscar_logs_por_tipo(self, tipo_operacao: TipoOperacao) -> List[LogAuditoria]:
        """
        Busca logs por tipo de operação.
        
        Args:
            tipo_operacao: Tipo da operação
            
        Returns:
            Lista de logs do tipo
        """
        try:
            logs = self.repositorio_logs.listar()
            logs_tipo = [log for log in logs if log.tipo_operacao == tipo_operacao]
            
            # Ordenar por timestamp (mais recente primeiro)
            logs_tipo.sort(key=lambda x: x.timestamp, reverse=True)
            
            return logs_tipo
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar logs por tipo: {e}")
            return []
    
    def relatorio_atividade(self, dias: int = 30) -> Dict[str, Any]:
        """
        Gera relatório de atividade dos últimos N dias.
        
        Args:
            dias: Número de dias para análise
            
        Returns:
            Dicionário com estatísticas de atividade
        """
        try:
            data_limite = datetime.now() - timedelta(days=dias)
            logs = self.buscar_logs_por_periodo(data_limite, datetime.now())
            
            # Estatísticas gerais
            total_operacoes = len(logs)
            
            # Operações por tipo
            operacoes_por_tipo = Counter(log.tipo_operacao.value for log in logs)
            
            # Atividade por usuário
            atividade_por_usuario = Counter(log.usuario for log in logs)
            
            # Atividade por entidade
            atividade_por_entidade = Counter(log.entidade for log in logs)
            
            # Atividade por dia
            atividade_por_dia = defaultdict(int)
            for log in logs:
                data_str = log.timestamp.strftime('%Y-%m-%d')
                atividade_por_dia[data_str] += 1
            
            # Horários de maior atividade
            atividade_por_hora = defaultdict(int)
            for log in logs:
                hora = log.timestamp.hour
                atividade_por_hora[hora] += 1
            
            return {
                'periodo_dias': dias,
                'total_operacoes': total_operacoes,
                'operacoes_por_tipo': dict(operacoes_por_tipo),
                'atividade_por_usuario': dict(atividade_por_usuario),
                'atividade_por_entidade': dict(atividade_por_entidade),
                'atividade_por_dia': dict(atividade_por_dia),
                'atividade_por_hora': dict(atividade_por_hora),
                'data_relatorio': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório de atividade: {e}")
            return {}
    
    def detectar_atividade_suspeita(self, limite_operacoes_por_minuto: int = 100) -> List[Dict[str, Any]]:
        """
        Detecta atividade suspeita baseada em padrões anômalos.
        
        Args:
            limite_operacoes_por_minuto: Limite de operações por minuto por usuário
            
        Returns:
            Lista de atividades suspeitas detectadas
        """
        try:
            # Analisar últimas 24 horas
            data_limite = datetime.now() - timedelta(hours=24)
            logs = self.buscar_logs_por_periodo(data_limite, datetime.now())
            
            atividades_suspeitas = []
            
            # Agrupar por usuário e minuto
            atividade_por_usuario_minuto = defaultdict(lambda: defaultdict(int))
            
            for log in logs:
                usuario = log.usuario
                minuto_key = log.timestamp.strftime('%Y-%m-%d %H:%M')
                atividade_por_usuario_minuto[usuario][minuto_key] += 1
            
            # Detectar usuários com muitas operações por minuto
            for usuario, atividade_minutos in atividade_por_usuario_minuto.items():
                for minuto, operacoes in atividade_minutos.items():
                    if operacoes > limite_operacoes_por_minuto:
                        atividades_suspeitas.append({
                            'tipo': 'Excesso de operações por minuto',
                            'usuario': usuario,
                            'timestamp': minuto,
                            'operacoes': operacoes,
                            'limite': limite_operacoes_por_minuto,
                            'severidade': 'Alta' if operacoes > limite_operacoes_por_minuto * 2 else 'Média'
                        })
            
            # Detectar operações fora do horário comercial
            for log in logs:
                hora = log.timestamp.hour
                if hora < 6 or hora > 22:  # Fora do horário 6h-22h
                    atividades_suspeitas.append({
                        'tipo': 'Operação fora do horário comercial',
                        'usuario': log.usuario,
                        'timestamp': log.timestamp.strftime('%d/%m/%Y %H:%M'),
                        'operacao': log.tipo_operacao.value,
                        'entidade': log.entidade,
                        'severidade': 'Baixa'
                    })
            
            # Detectar múltiplas tentativas de operações em sequência
            logs_por_usuario = defaultdict(list)
            for log in logs:
                logs_por_usuario[log.usuario].append(log)
            
            for usuario, logs_usuario in logs_por_usuario.items():
                logs_usuario.sort(key=lambda x: x.timestamp)
                
                # Detectar sequências de operações similares
                sequencia_atual = []
                for log in logs_usuario:
                    if (sequencia_atual and 
                        log.tipo_operacao == sequencia_atual[-1].tipo_operacao and
                        log.entidade == sequencia_atual[-1].entidade and
                        (log.timestamp - sequencia_atual[-1].timestamp).seconds < 60):
                        sequencia_atual.append(log)
                    else:
                        if len(sequencia_atual) > 10:  # Mais de 10 operações similares em sequência
                            atividades_suspeitas.append({
                                'tipo': 'Sequência de operações similares',
                                'usuario': usuario,
                                'operacao': sequencia_atual[0].tipo_operacao.value,
                                'entidade': sequencia_atual[0].entidade,
                                'quantidade': len(sequencia_atual),
                                'periodo': f"{sequencia_atual[0].timestamp.strftime('%H:%M')} - {sequencia_atual[-1].timestamp.strftime('%H:%M')}",
                                'severidade': 'Média'
                            })
                        sequencia_atual = [log]
            
            return atividades_suspeitas
            
        except Exception as e:
            self.logger.error(f"Erro ao detectar atividade suspeita: {e}")
            return []
    
    def exportar_logs_csv(self, data_inicio: datetime, data_fim: datetime, 
                         nome_arquivo: Optional[str] = None) -> str:
        """
        Exporta logs para arquivo CSV.
        
        Args:
            data_inicio: Data de início
            data_fim: Data de fim
            nome_arquivo: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo gerado
        """
        import csv
        from pathlib import Path
        
        try:
            logs = self.buscar_logs_por_periodo(data_inicio, data_fim)
            
            if not nome_arquivo:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                nome_arquivo = f"logs_auditoria_{timestamp}.csv"
            
            # Criar diretório de exports se não existir
            export_dir = Path(self.config.system.export_directory)
            export_dir.mkdir(exist_ok=True)
            
            caminho_arquivo = export_dir / nome_arquivo
            
            with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Cabeçalho
                writer.writerow([
                    'Timestamp', 'Tipo Operação', 'Entidade', 'ID Entidade', 
                    'Usuário', 'IP Origem', 'User Agent', 'Detalhes'
                ])
                
                # Dados
                for log in logs:
                    writer.writerow([
                        log.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
                        log.tipo_operacao.value,
                        log.entidade,
                        log.entidade_id,
                        log.usuario,
                        log.ip_origem,
                        log.user_agent,
                        str(log.detalhes)
                    ])
            
            self.logger.info(f"Logs exportados para: {caminho_arquivo}")
            return str(caminho_arquivo)
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar logs: {e}")
            return ""
    
    def limpar_logs_antigos(self, dias_retencao: int = 365):
        """
        Remove logs mais antigos que o período de retenção.
        
        Args:
            dias_retencao: Número de dias para manter os logs
        """
        try:
            data_limite = datetime.now() - timedelta(days=dias_retencao)
            logs = self.repositorio_logs.listar()
            
            logs_removidos = 0
            for log in logs:
                if log.timestamp < data_limite:
                    self.repositorio_logs.deletar(log.id)
                    logs_removidos += 1
            
            self.logger.info(f"Limpeza de logs concluída. {logs_removidos} logs removidos.")
            
        except Exception as e:
            self.logger.error(f"Erro ao limpar logs antigos: {e}")
    
    def obter_estatisticas_sistema(self) -> Dict[str, Any]:
        """
        Obtém estatísticas gerais do sistema de auditoria.
        
        Returns:
            Dicionário com estatísticas
        """
        try:
            logs = self.repositorio_logs.listar()
            
            if not logs:
                return {
                    'total_logs': 0,
                    'primeiro_log': None,
                    'ultimo_log': None,
                    'usuarios_unicos': 0,
                    'entidades_monitoradas': 0
                }
            
            # Ordenar logs por timestamp
            logs.sort(key=lambda x: x.timestamp)
            
            usuarios_unicos = set(log.usuario for log in logs)
            entidades_unicos = set(log.entidade for log in logs)
            
            return {
                'total_logs': len(logs),
                'primeiro_log': logs[0].timestamp.strftime('%d/%m/%Y %H:%M:%S'),
                'ultimo_log': logs[-1].timestamp.strftime('%d/%m/%Y %H:%M:%S'),
                'usuarios_unicos': len(usuarios_unicos),
                'entidades_monitoradas': len(entidades_unicos),
                'tipos_operacao': len(set(log.tipo_operacao for log in logs))
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas do sistema: {e}")
            return {}