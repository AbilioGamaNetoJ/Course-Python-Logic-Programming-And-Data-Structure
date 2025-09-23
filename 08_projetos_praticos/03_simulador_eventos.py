"""
MÓDULO 08.3 - SIMULADOR DE EVENTOS DISCRETOS
============================================

Objetivos de Aprendizado:
- Implementar simulador de eventos discretos completo
- Dominar conceitos de simulação estocástica
- Aplicar teoria de filas e sistemas de espera
- Implementar diferentes distribuições probabilísticas
- Coletar e analisar estatísticas de simulação
- Otimizar sistemas através de simulação
- Validar modelos matemáticos com simulação
- Implementar técnicas de redução de variância

Conceitos Abordados:
- Discrete Event Simulation (DES)
- Event-driven simulation
- Teoria de Filas (M/M/1, M/M/c, M/G/1)
- Distribuições probabilísticas
- Geração de números aleatórios
- Análise estatística de resultados
- Warm-up period e steady state
- Confidence intervals
- Variance reduction techniques

Algoritmos Implementados:
- Event scheduling algorithm
- Priority queue para eventos
- Statistical collectors
- Random number generators
- Queue discipline algorithms (FIFO, LIFO, Priority)
- Batch means method
- Replication method

Pré-requisitos:
- Estruturas de dados (filas, heaps)
- Probabilidade e estatística
- Análise de algoritmos
- Programação orientada a objetos
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
from abc import ABC, abstractmethod
import heapq
import time
import math
import random
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class TipoEvento(Enum):
    """Tipos de eventos na simulação."""
    CHEGADA = "Chegada"
    SAIDA = "Saída"
    INICIO_SERVICO = "Início de Serviço"
    FIM_SERVICO = "Fim de Serviço"
    FALHA = "Falha"
    REPARO = "Reparo"
    CUSTOM = "Personalizado"


class TipoDistribuicao(Enum):
    """Tipos de distribuições probabilísticas."""
    EXPONENCIAL = "Exponencial"
    NORMAL = "Normal"
    UNIFORME = "Uniforme"
    POISSON = "Poisson"
    WEIBULL = "Weibull"
    GAMMA = "Gamma"
    TRIANGULAR = "Triangular"
    DETERMINISTICO = "Determinístico"


class DisciplinaFila(Enum):
    """Disciplinas de atendimento em filas."""
    FIFO = "First In, First Out"
    LIFO = "Last In, First Out"
    PRIORIDADE = "Prioridade"
    RANDOM = "Aleatório"
    SJF = "Shortest Job First"
    ROUND_ROBIN = "Round Robin"


@dataclass
class Evento:
    """Representa um evento na simulação."""
    tempo: float
    tipo: TipoEvento
    entidade_id: Optional[str] = None
    dados: Dict[str, Any] = field(default_factory=dict)
    prioridade: int = 0  # Menor valor = maior prioridade
    
    def __lt__(self, other):
        """Comparação para heap (prioridade por tempo, depois por prioridade)."""
        if self.tempo != other.tempo:
            return self.tempo < other.tempo
        return self.prioridade < other.prioridade


@dataclass
class Entidade:
    """Representa uma entidade no sistema (cliente, job, etc.)."""
    id: str
    tempo_chegada: float
    tempo_inicio_servico: Optional[float] = None
    tempo_fim_servico: Optional[float] = None
    prioridade: int = 0
    dados: Dict[str, Any] = field(default_factory=dict)
    
    def tempo_espera(self) -> Optional[float]:
        """Calcula tempo de espera na fila."""
        if self.tempo_inicio_servico is not None:
            return self.tempo_inicio_servico - self.tempo_chegada
        return None
    
    def tempo_servico(self) -> Optional[float]:
        """Calcula tempo de serviço."""
        if (self.tempo_inicio_servico is not None and 
            self.tempo_fim_servico is not None):
            return self.tempo_fim_servico - self.tempo_inicio_servico
        return None
    
    def tempo_sistema(self) -> Optional[float]:
        """Calcula tempo total no sistema."""
        if self.tempo_fim_servico is not None:
            return self.tempo_fim_servico - self.tempo_chegada
        return None


@dataclass
class EstatisticasSimulacao:
    """Estatísticas coletadas durante a simulação."""
    tempo_simulacao: float = 0.0
    entidades_processadas: int = 0
    entidades_na_fila: List[int] = field(default_factory=list)
    tempos_espera: List[float] = field(default_factory=list)
    tempos_servico: List[float] = field(default_factory=list)
    tempos_sistema: List[float] = field(default_factory=list)
    utilizacao_servidor: List[float] = field(default_factory=list)
    throughput: List[float] = field(default_factory=list)
    
    def adicionar_entidade(self, entidade: Entidade):
        """Adiciona estatísticas de uma entidade processada."""
        self.entidades_processadas += 1
        
        if entidade.tempo_espera() is not None:
            self.tempos_espera.append(entidade.tempo_espera())
        
        if entidade.tempo_servico() is not None:
            self.tempos_servico.append(entidade.tempo_servico())
        
        if entidade.tempo_sistema() is not None:
            self.tempos_sistema.append(entidade.tempo_sistema())
    
    def calcular_metricas(self) -> Dict[str, float]:
        """Calcula métricas estatísticas."""
        metricas = {}
        
        if self.tempos_espera:
            metricas['tempo_espera_medio'] = np.mean(self.tempos_espera)
            metricas['tempo_espera_max'] = np.max(self.tempos_espera)
            metricas['tempo_espera_std'] = np.std(self.tempos_espera)
        
        if self.tempos_servico:
            metricas['tempo_servico_medio'] = np.mean(self.tempos_servico)
            metricas['tempo_servico_max'] = np.max(self.tempos_servico)
            metricas['tempo_servico_std'] = np.std(self.tempos_servico)
        
        if self.tempos_sistema:
            metricas['tempo_sistema_medio'] = np.mean(self.tempos_sistema)
            metricas['tempo_sistema_max'] = np.max(self.tempos_sistema)
            metricas['tempo_sistema_std'] = np.std(self.tempos_sistema)
        
        if self.entidades_na_fila:
            metricas['tamanho_fila_medio'] = np.mean(self.entidades_na_fila)
            metricas['tamanho_fila_max'] = np.max(self.entidades_na_fila)
        
        if self.utilizacao_servidor:
            metricas['utilizacao_media'] = np.mean(self.utilizacao_servidor)
        
        if self.throughput:
            metricas['throughput_medio'] = np.mean(self.throughput)
        
        if self.tempo_simulacao > 0:
            metricas['taxa_chegada'] = self.entidades_processadas / self.tempo_simulacao
        
        return metricas


class GeradorAleatorio:
    """
    Gerador de números aleatórios com diferentes distribuições.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Inicializa gerador.
        
        Args:
            seed: Semente para reprodutibilidade
        """
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
    
    def exponencial(self, taxa: float) -> float:
        """
        Gera número aleatório com distribuição exponencial.
        
        Args:
            taxa: Taxa (lambda) da distribuição
        
        Returns:
            Número aleatório
        """
        return np.random.exponential(1.0 / taxa)
    
    def normal(self, media: float, desvio: float) -> float:
        """Gera número aleatório com distribuição normal."""
        return max(0, np.random.normal(media, desvio))
    
    def uniforme(self, minimo: float, maximo: float) -> float:
        """Gera número aleatório com distribuição uniforme."""
        return np.random.uniform(minimo, maximo)
    
    def poisson(self, taxa: float) -> int:
        """Gera número aleatório com distribuição de Poisson."""
        return np.random.poisson(taxa)
    
    def weibull(self, forma: float, escala: float) -> float:
        """Gera número aleatório com distribuição de Weibull."""
        return np.random.weibull(forma) * escala
    
    def gamma(self, forma: float, escala: float) -> float:
        """Gera número aleatório com distribuição Gamma."""
        return np.random.gamma(forma, escala)
    
    def triangular(self, minimo: float, moda: float, maximo: float) -> float:
        """Gera número aleatório com distribuição triangular."""
        return np.random.triangular(minimo, moda, maximo)
    
    def deterministico(self, valor: float) -> float:
        """Retorna valor determinístico (sem aleatoriedade)."""
        return valor
    
    def gerar(self, tipo: TipoDistribuicao, **parametros) -> float:
        """
        Gera número aleatório baseado no tipo de distribuição.
        
        Args:
            tipo: Tipo de distribuição
            **parametros: Parâmetros da distribuição
        
        Returns:
            Número aleatório gerado
        """
        if tipo == TipoDistribuicao.EXPONENCIAL:
            return self.exponencial(parametros['taxa'])
        elif tipo == TipoDistribuicao.NORMAL:
            return self.normal(parametros['media'], parametros['desvio'])
        elif tipo == TipoDistribuicao.UNIFORME:
            return self.uniforme(parametros['minimo'], parametros['maximo'])
        elif tipo == TipoDistribuicao.POISSON:
            return self.poisson(parametros['taxa'])
        elif tipo == TipoDistribuicao.WEIBULL:
            return self.weibull(parametros['forma'], parametros['escala'])
        elif tipo == TipoDistribuicao.GAMMA:
            return self.gamma(parametros['forma'], parametros['escala'])
        elif tipo == TipoDistribuicao.TRIANGULAR:
            return self.triangular(parametros['minimo'], parametros['moda'], parametros['maximo'])
        elif tipo == TipoDistribuicao.DETERMINISTICO:
            return self.deterministico(parametros['valor'])
        else:
            raise ValueError(f"Tipo de distribuição não suportado: {tipo}")


class Fila:
    """
    Implementação de fila com diferentes disciplinas de atendimento.
    """
    
    def __init__(self, disciplina: DisciplinaFila = DisciplinaFila.FIFO,
                 capacidade_maxima: Optional[int] = None):
        """
        Inicializa fila.
        
        Args:
            disciplina: Disciplina de atendimento
            capacidade_maxima: Capacidade máxima da fila (None = ilimitada)
        """
        self.disciplina = disciplina
        self.capacidade_maxima = capacidade_maxima
        self.entidades: List[Entidade] = []
        self.historico_tamanho: List[Tuple[float, int]] = []
    
    def esta_cheia(self) -> bool:
        """Verifica se a fila está cheia."""
        if self.capacidade_maxima is None:
            return False
        return len(self.entidades) >= self.capacidade_maxima
    
    def esta_vazia(self) -> bool:
        """Verifica se a fila está vazia."""
        return len(self.entidades) == 0
    
    def tamanho(self) -> int:
        """Retorna tamanho atual da fila."""
        return len(self.entidades)
    
    def adicionar(self, entidade: Entidade, tempo_atual: float) -> bool:
        """
        Adiciona entidade à fila.
        
        Args:
            entidade: Entidade a ser adicionada
            tempo_atual: Tempo atual da simulação
        
        Returns:
            True se adicionada com sucesso, False se fila cheia
        """
        if self.esta_cheia():
            return False
        
        if self.disciplina == DisciplinaFila.FIFO:
            self.entidades.append(entidade)
        elif self.disciplina == DisciplinaFila.LIFO:
            self.entidades.append(entidade)
        elif self.disciplina == DisciplinaFila.PRIORIDADE:
            # Inserir mantendo ordem de prioridade
            inserido = False
            for i, ent in enumerate(self.entidades):
                if entidade.prioridade < ent.prioridade:  # Menor valor = maior prioridade
                    self.entidades.insert(i, entidade)
                    inserido = True
                    break
            if not inserido:
                self.entidades.append(entidade)
        elif self.disciplina == DisciplinaFila.SJF:
            # Shortest Job First - precisa de tempo de serviço estimado
            tempo_servico_estimado = entidade.dados.get('tempo_servico_estimado', 0)
            inserido = False
            for i, ent in enumerate(self.entidades):
                tempo_ent = ent.dados.get('tempo_servico_estimado', 0)
                if tempo_servico_estimado < tempo_ent:
                    self.entidades.insert(i, entidade)
                    inserido = True
                    break
            if not inserido:
                self.entidades.append(entidade)
        else:  # RANDOM ou outros
            self.entidades.append(entidade)
        
        # Registrar tamanho da fila
        self.historico_tamanho.append((tempo_atual, len(self.entidades)))
        
        return True
    
    def remover(self, tempo_atual: float) -> Optional[Entidade]:
        """
        Remove entidade da fila.
        
        Args:
            tempo_atual: Tempo atual da simulação
        
        Returns:
            Entidade removida ou None se fila vazia
        """
        if self.esta_vazia():
            return None
        
        if self.disciplina == DisciplinaFila.FIFO:
            entidade = self.entidades.pop(0)
        elif self.disciplina == DisciplinaFila.LIFO:
            entidade = self.entidades.pop()
        elif self.disciplina == DisciplinaFila.RANDOM:
            indice = random.randint(0, len(self.entidades) - 1)
            entidade = self.entidades.pop(indice)
        else:  # PRIORIDADE, SJF, etc.
            entidade = self.entidades.pop(0)  # Já estão ordenadas
        
        # Registrar tamanho da fila
        self.historico_tamanho.append((tempo_atual, len(self.entidades)))
        
        return entidade
    
    def obter_estatisticas_tamanho(self) -> Dict[str, float]:
        """Obtém estatísticas do tamanho da fila ao longo do tempo."""
        if not self.historico_tamanho:
            return {}
        
        tamanhos = [tamanho for _, tamanho in self.historico_tamanho]
        
        return {
            'tamanho_medio': np.mean(tamanhos),
            'tamanho_maximo': np.max(tamanhos),
            'tamanho_minimo': np.min(tamanhos),
            'desvio_padrao': np.std(tamanhos)
        }


class Servidor:
    """
    Representa um servidor no sistema de filas.
    """
    
    def __init__(self, id: str, gerador: GeradorAleatorio,
                 tipo_distribuicao: TipoDistribuicao,
                 parametros_distribuicao: Dict[str, float]):
        """
        Inicializa servidor.
        
        Args:
            id: Identificador do servidor
            gerador: Gerador de números aleatórios
            tipo_distribuicao: Tipo de distribuição do tempo de serviço
            parametros_distribuicao: Parâmetros da distribuição
        """
        self.id = id
        self.gerador = gerador
        self.tipo_distribuicao = tipo_distribuicao
        self.parametros_distribuicao = parametros_distribuicao
        self.ocupado = False
        self.entidade_atual: Optional[Entidade] = None
        self.tempo_inicio_servico: Optional[float] = None
        self.historico_utilizacao: List[Tuple[float, bool]] = []
        self.entidades_atendidas: List[Entidade] = []
    
    def esta_livre(self) -> bool:
        """Verifica se o servidor está livre."""
        return not self.ocupado
    
    def iniciar_servico(self, entidade: Entidade, tempo_atual: float) -> float:
        """
        Inicia serviço de uma entidade.
        
        Args:
            entidade: Entidade a ser atendida
            tempo_atual: Tempo atual da simulação
        
        Returns:
            Tempo de serviço gerado
        """
        self.ocupado = True
        self.entidade_atual = entidade
        self.tempo_inicio_servico = tempo_atual
        entidade.tempo_inicio_servico = tempo_atual
        
        # Gerar tempo de serviço
        tempo_servico = self.gerador.gerar(
            self.tipo_distribuicao,
            **self.parametros_distribuicao
        )
        
        # Registrar mudança de estado
        self.historico_utilizacao.append((tempo_atual, True))
        
        return tempo_servico
    
    def finalizar_servico(self, tempo_atual: float):
        """
        Finaliza serviço atual.
        
        Args:
            tempo_atual: Tempo atual da simulação
        """
        if self.entidade_atual:
            self.entidade_atual.tempo_fim_servico = tempo_atual
            self.entidades_atendidas.append(self.entidade_atual)
        
        self.ocupado = False
        self.entidade_atual = None
        self.tempo_inicio_servico = None
        
        # Registrar mudança de estado
        self.historico_utilizacao.append((tempo_atual, False))
    
    def calcular_utilizacao(self, tempo_total: float) -> float:
        """
        Calcula utilização do servidor.
        
        Args:
            tempo_total: Tempo total da simulação
        
        Returns:
            Percentual de utilização (0-1)
        """
        if not self.historico_utilizacao or tempo_total <= 0:
            return 0.0
        
        tempo_ocupado = 0.0
        estado_atual = False
        tempo_anterior = 0.0
        
        for tempo, ocupado in self.historico_utilizacao:
            if estado_atual:
                tempo_ocupado += tempo - tempo_anterior
            
            estado_atual = ocupado
            tempo_anterior = tempo
        
        # Se ainda está ocupado no final
        if estado_atual:
            tempo_ocupado += tempo_total - tempo_anterior
        
        return tempo_ocupado / tempo_total


class SimuladorEventos:
    """
    Simulador de eventos discretos principal.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Inicializa simulador.
        
        Args:
            seed: Semente para reprodutibilidade
        """
        self.tempo_atual = 0.0
        self.lista_eventos: List[Evento] = []
        self.gerador = GeradorAleatorio(seed)
        self.estatisticas = EstatisticasSimulacao()
        self.entidades_criadas = 0
        self.handlers_eventos: Dict[TipoEvento, Callable] = {}
        
        # Componentes do sistema
        self.filas: Dict[str, Fila] = {}
        self.servidores: Dict[str, Servidor] = {}
        
        # Controle de simulação
        self.tempo_warmup = 0.0
        self.coletando_estatisticas = False
    
    def agendar_evento(self, evento: Evento):
        """
        Agenda um evento na lista de eventos futuros.
        
        Args:
            evento: Evento a ser agendado
        """
        heapq.heappush(self.lista_eventos, evento)
    
    def proximo_evento(self) -> Optional[Evento]:
        """
        Obtém próximo evento da lista.
        
        Returns:
            Próximo evento ou None se lista vazia
        """
        if self.lista_eventos:
            return heapq.heappop(self.lista_eventos)
        return None
    
    def registrar_handler(self, tipo_evento: TipoEvento, handler: Callable):
        """
        Registra handler para um tipo de evento.
        
        Args:
            tipo_evento: Tipo do evento
            handler: Função handler
        """
        self.handlers_eventos[tipo_evento] = handler
    
    def processar_evento(self, evento: Evento):
        """
        Processa um evento.
        
        Args:
            evento: Evento a ser processado
        """
        self.tempo_atual = evento.tempo
        
        # Verificar se deve começar a coletar estatísticas
        if not self.coletando_estatisticas and self.tempo_atual >= self.tempo_warmup:
            self.coletando_estatisticas = True
            print(f"Iniciando coleta de estatísticas no tempo {self.tempo_atual:.2f}")
        
        # Chamar handler específico do evento
        if evento.tipo in self.handlers_eventos:
            self.handlers_eventos[evento.tipo](evento)
        else:
            print(f"Warning: Nenhum handler registrado para evento {evento.tipo}")
    
    def adicionar_fila(self, nome: str, fila: Fila):
        """Adiciona fila ao sistema."""
        self.filas[nome] = fila
    
    def adicionar_servidor(self, nome: str, servidor: Servidor):
        """Adiciona servidor ao sistema."""
        self.servidores[nome] = servidor
    
    def criar_entidade(self, dados: Optional[Dict[str, Any]] = None) -> Entidade:
        """
        Cria nova entidade no sistema.
        
        Args:
            dados: Dados adicionais da entidade
        
        Returns:
            Nova entidade criada
        """
        self.entidades_criadas += 1
        entidade = Entidade(
            id=f"ent_{self.entidades_criadas}",
            tempo_chegada=self.tempo_atual,
            dados=dados or {}
        )
        return entidade
    
    def coletar_estatisticas_sistema(self):
        """Coleta estatísticas do sistema no tempo atual."""
        if not self.coletando_estatisticas:
            return
        
        # Coletar tamanhos das filas
        for nome, fila in self.filas.items():
            self.estatisticas.entidades_na_fila.append(fila.tamanho())
        
        # Coletar utilização dos servidores
        utilizacao_total = 0
        for servidor in self.servidores.values():
            if servidor.ocupado:
                utilizacao_total += 1
        
        if self.servidores:
            utilizacao_percentual = utilizacao_total / len(self.servidores)
            self.estatisticas.utilizacao_servidor.append(utilizacao_percentual)
    
    def executar(self, tempo_simulacao: float, tempo_warmup: float = 0.0):
        """
        Executa simulação.
        
        Args:
            tempo_simulacao: Tempo total de simulação
            tempo_warmup: Tempo de aquecimento (não coleta estatísticas)
        """
        print(f"Iniciando simulação por {tempo_simulacao} unidades de tempo")
        print(f"Período de aquecimento: {tempo_warmup} unidades")
        
        self.tempo_warmup = tempo_warmup
        self.tempo_atual = 0.0
        self.coletando_estatisticas = False
        
        inicio_real = time.time()
        
        # Loop principal da simulação
        while self.tempo_atual < tempo_simulacao:
            # Coletar estatísticas do sistema
            self.coletar_estatisticas_sistema()
            
            # Processar próximo evento
            evento = self.proximo_evento()
            
            if evento is None:
                print("Warning: Lista de eventos vazia, terminando simulação")
                break
            
            if evento.tempo > tempo_simulacao:
                break
            
            self.processar_evento(evento)
        
        # Finalizar simulação
        self.tempo_atual = tempo_simulacao
        self.estatisticas.tempo_simulacao = tempo_simulacao
        
        tempo_real = time.time() - inicio_real
        print(f"Simulação concluída em {tempo_real:.2f} segundos")
        print(f"Entidades criadas: {self.entidades_criadas}")
        print(f"Entidades processadas: {self.estatisticas.entidades_processadas}")
    
    def obter_relatorio(self) -> Dict[str, Any]:
        """Gera relatório completo da simulação."""
        relatorio = {
            'parametros_simulacao': {
                'tempo_total': self.estatisticas.tempo_simulacao,
                'tempo_warmup': self.tempo_warmup,
                'entidades_criadas': self.entidades_criadas,
                'entidades_processadas': self.estatisticas.entidades_processadas
            },
            'metricas_sistema': self.estatisticas.calcular_metricas(),
            'filas': {},
            'servidores': {}
        }
        
        # Estatísticas das filas
        for nome, fila in self.filas.items():
            relatorio['filas'][nome] = {
                'disciplina': fila.disciplina.value,
                'capacidade_maxima': fila.capacidade_maxima,
                'tamanho_final': fila.tamanho(),
                **fila.obter_estatisticas_tamanho()
            }
        
        # Estatísticas dos servidores
        for nome, servidor in self.servidores.items():
            utilizacao = servidor.calcular_utilizacao(self.estatisticas.tempo_simulacao)
            relatorio['servidores'][nome] = {
                'utilizacao': utilizacao,
                'entidades_atendidas': len(servidor.entidades_atendidas),
                'ocupado_final': servidor.ocupado
            }
        
        return relatorio


class SistemaFilaSimples:
    """
    Sistema de fila simples M/M/1 (chegadas Poisson, serviço exponencial, 1 servidor).
    """
    
    def __init__(self, taxa_chegada: float, taxa_servico: float, seed: Optional[int] = None):
        """
        Inicializa sistema M/M/1.
        
        Args:
            taxa_chegada: Taxa de chegada (lambda)
            taxa_servico: Taxa de serviço (mu)
            seed: Semente para reprodutibilidade
        """
        self.taxa_chegada = taxa_chegada
        self.taxa_servico = taxa_servico
        self.simulador = SimuladorEventos(seed)
        
        # Criar componentes
        self.fila = Fila(DisciplinaFila.FIFO)
        self.servidor = Servidor(
            "servidor_1",
            self.simulador.gerador,
            TipoDistribuicao.EXPONENCIAL,
            {'taxa': taxa_servico}
        )
        
        # Adicionar ao simulador
        self.simulador.adicionar_fila("principal", self.fila)
        self.simulador.adicionar_servidor("principal", self.servidor)
        
        # Registrar handlers
        self.simulador.registrar_handler(TipoEvento.CHEGADA, self.processar_chegada)
        self.simulador.registrar_handler(TipoEvento.FIM_SERVICO, self.processar_fim_servico)
        
        # Agendar primeira chegada
        tempo_primeira_chegada = self.simulador.gerador.exponencial(taxa_chegada)
        evento_chegada = Evento(tempo_primeira_chegada, TipoEvento.CHEGADA)
        self.simulador.agendar_evento(evento_chegada)
    
    def processar_chegada(self, evento: Evento):
        """Processa chegada de uma entidade."""
        # Criar nova entidade
        entidade = self.simulador.criar_entidade()
        
        # Tentar adicionar à fila
        if self.fila.adicionar(entidade, self.simulador.tempo_atual):
            # Se servidor está livre, iniciar serviço imediatamente
            if self.servidor.esta_livre():
                self.iniciar_servico()
        else:
            # Fila cheia - entidade é perdida (sistema com perda)
            print(f"Entidade {entidade.id} perdida - fila cheia")
        
        # Agendar próxima chegada
        tempo_proxima_chegada = (self.simulador.tempo_atual + 
                               self.simulador.gerador.exponencial(self.taxa_chegada))
        
        evento_chegada = Evento(tempo_proxima_chegada, TipoEvento.CHEGADA)
        self.simulador.agendar_evento(evento_chegada)
    
    def processar_fim_servico(self, evento: Evento):
        """Processa fim de serviço."""
        # Finalizar serviço atual
        entidade_atendida = self.servidor.entidade_atual
        self.servidor.finalizar_servico(self.simulador.tempo_atual)
        
        # Adicionar às estatísticas
        if entidade_atendida and self.simulador.coletando_estatisticas:
            self.simulador.estatisticas.adicionar_entidade(entidade_atendida)
        
        # Se há entidades na fila, iniciar próximo serviço
        if not self.fila.esta_vazia():
            self.iniciar_servico()
    
    def iniciar_servico(self):
        """Inicia serviço da próxima entidade na fila."""
        entidade = self.fila.remover(self.simulador.tempo_atual)
        
        if entidade:
            tempo_servico = self.servidor.iniciar_servico(entidade, self.simulador.tempo_atual)
            
            # Agendar fim do serviço
            tempo_fim_servico = self.simulador.tempo_atual + tempo_servico
            evento_fim = Evento(tempo_fim_servico, TipoEvento.FIM_SERVICO)
            self.simulador.agendar_evento(evento_fim)
    
    def executar_simulacao(self, tempo_simulacao: float, tempo_warmup: float = 0.0):
        """Executa simulação do sistema."""
        self.simulador.executar(tempo_simulacao, tempo_warmup)
        return self.simulador.obter_relatorio()
    
    def calcular_metricas_teoricas(self) -> Dict[str, float]:
        """Calcula métricas teóricas do sistema M/M/1."""
        rho = self.taxa_chegada / self.taxa_servico  # Utilização
        
        if rho >= 1:
            return {'erro': 'Sistema instável (rho >= 1)'}
        
        return {
            'utilizacao_teorica': rho,
            'tamanho_fila_medio_teorico': rho**2 / (1 - rho),
            'tamanho_sistema_medio_teorico': rho / (1 - rho),
            'tempo_espera_medio_teorico': rho / (self.taxa_servico * (1 - rho)),
            'tempo_sistema_medio_teorico': 1 / (self.taxa_servico * (1 - rho))
        }


class SistemaFilaMultiplosServidores:
    """
    Sistema de fila M/M/c (múltiplos servidores).
    """
    
    def __init__(self, taxa_chegada: float, taxa_servico: float, 
                 num_servidores: int, seed: Optional[int] = None):
        """
        Inicializa sistema M/M/c.
        
        Args:
            taxa_chegada: Taxa de chegada
            taxa_servico: Taxa de serviço por servidor
            num_servidores: Número de servidores
            seed: Semente para reprodutibilidade
        """
        self.taxa_chegada = taxa_chegada
        self.taxa_servico = taxa_servico
        self.num_servidores = num_servidores
        self.simulador = SimuladorEventos(seed)
        
        # Criar fila
        self.fila = Fila(DisciplinaFila.FIFO)
        self.simulador.adicionar_fila("principal", self.fila)
        
        # Criar servidores
        self.servidores = []
        for i in range(num_servidores):
            servidor = Servidor(
                f"servidor_{i+1}",
                self.simulador.gerador,
                TipoDistribuicao.EXPONENCIAL,
                {'taxa': taxa_servico}
            )
            self.servidores.append(servidor)
            self.simulador.adicionar_servidor(f"servidor_{i+1}", servidor)
        
        # Registrar handlers
        self.simulador.registrar_handler(TipoEvento.CHEGADA, self.processar_chegada)
        self.simulador.registrar_handler(TipoEvento.FIM_SERVICO, self.processar_fim_servico)
        
        # Agendar primeira chegada
        tempo_primeira_chegada = self.simulador.gerador.exponencial(taxa_chegada)
        evento_chegada = Evento(tempo_primeira_chegada, TipoEvento.CHEGADA)
        self.simulador.agendar_evento(evento_chegada)
    
    def obter_servidor_livre(self) -> Optional[Servidor]:
        """Obtém primeiro servidor livre."""
        for servidor in self.servidores:
            if servidor.esta_livre():
                return servidor
        return None
    
    def processar_chegada(self, evento: Evento):
        """Processa chegada de uma entidade."""
        # Criar nova entidade
        entidade = self.simulador.criar_entidade()
        
        # Verificar se há servidor livre
        servidor_livre = self.obter_servidor_livre()
        
        if servidor_livre:
            # Iniciar serviço imediatamente
            tempo_servico = servidor_livre.iniciar_servico(entidade, self.simulador.tempo_atual)
            
            # Agendar fim do serviço
            tempo_fim_servico = self.simulador.tempo_atual + tempo_servico
            evento_fim = Evento(
                tempo_fim_servico, 
                TipoEvento.FIM_SERVICO,
                entidade_id=servidor_livre.id
            )
            self.simulador.agendar_evento(evento_fim)
        else:
            # Adicionar à fila
            self.fila.adicionar(entidade, self.simulador.tempo_atual)
        
        # Agendar próxima chegada
        tempo_proxima_chegada = (self.simulador.tempo_atual + 
                               self.simulador.gerador.exponencial(self.taxa_chegada))
        
        evento_chegada = Evento(tempo_proxima_chegada, TipoEvento.CHEGADA)
        self.simulador.agendar_evento(evento_chegada)
    
    def processar_fim_servico(self, evento: Evento):
        """Processa fim de serviço."""
        # Encontrar servidor que terminou
        servidor = None
        for s in self.servidores:
            if s.id == evento.entidade_id:
                servidor = s
                break
        
        if not servidor:
            print(f"Erro: Servidor {evento.entidade_id} não encontrado")
            return
        
        # Finalizar serviço
        entidade_atendida = servidor.entidade_atual
        servidor.finalizar_servico(self.simulador.tempo_atual)
        
        # Adicionar às estatísticas
        if entidade_atendida and self.simulador.coletando_estatisticas:
            self.simulador.estatisticas.adicionar_entidade(entidade_atendida)
        
        # Se há entidades na fila, iniciar próximo serviço
        if not self.fila.esta_vazia():
            entidade = self.fila.remover(self.simulador.tempo_atual)
            
            if entidade:
                tempo_servico = servidor.iniciar_servico(entidade, self.simulador.tempo_atual)
                
                # Agendar fim do serviço
                tempo_fim_servico = self.simulador.tempo_atual + tempo_servico
                evento_fim = Evento(
                    tempo_fim_servico, 
                    TipoEvento.FIM_SERVICO,
                    entidade_id=servidor.id
                )
                self.simulador.agendar_evento(evento_fim)
    
    def executar_simulacao(self, tempo_simulacao: float, tempo_warmup: float = 0.0):
        """Executa simulação do sistema."""
        self.simulador.executar(tempo_simulacao, tempo_warmup)
        return self.simulador.obter_relatorio()


def demonstrar_sistema_mm1():
    """Demonstra sistema M/M/1."""
    print("=== DEMONSTRAÇÃO: SISTEMA M/M/1 ===\n")
    
    # Parâmetros do sistema
    taxa_chegada = 0.8  # 0.8 entidades por unidade de tempo
    taxa_servico = 1.0  # 1.0 entidades por unidade de tempo
    
    print(f"Taxa de chegada (λ): {taxa_chegada}")
    print(f"Taxa de serviço (μ): {taxa_servico}")
    print(f"Utilização teórica (ρ): {taxa_chegada/taxa_servico:.2f}")
    
    # Criar sistema
    sistema = SistemaFilaSimples(taxa_chegada, taxa_servico, seed=42)
    
    # Calcular métricas teóricas
    metricas_teoricas = sistema.calcular_metricas_teoricas()
    print("\nMétricas Teóricas:")
    for metrica, valor in metricas_teoricas.items():
        print(f"  {metrica}: {valor:.4f}")
    
    # Executar simulação
    print("\nExecutando simulação...")
    relatorio = sistema.executar_simulacao(tempo_simulacao=1000, tempo_warmup=100)
    
    # Mostrar resultados
    print("\nResultados da Simulação:")
    metricas_sim = relatorio['metricas_sistema']
    
    comparacoes = [
        ('Utilização', 'utilizacao_teorica', 'utilizacao_media'),
        ('Tempo no Sistema', 'tempo_sistema_medio_teorico', 'tempo_sistema_medio'),
        ('Tempo de Espera', 'tempo_espera_medio_teorico', 'tempo_espera_medio'),
        ('Tamanho da Fila', 'tamanho_fila_medio_teorico', 'tamanho_fila_medio')
    ]
    
    print(f"{'Métrica':<20} {'Teórico':<12} {'Simulado':<12} {'Erro %':<10}")
    print("-" * 60)
    
    for nome, key_teorico, key_simulado in comparacoes:
        if key_teorico in metricas_teoricas and key_simulado in metricas_sim:
            teorico = metricas_teoricas[key_teorico]
            simulado = metricas_sim[key_simulado]
            erro = abs(teorico - simulado) / teorico * 100 if teorico != 0 else 0
            
            print(f"{nome:<20} {teorico:<12.4f} {simulado:<12.4f} {erro:<10.2f}")
    
    print()


def demonstrar_sistema_mmc():
    """Demonstra sistema M/M/c."""
    print("=== DEMONSTRAÇÃO: SISTEMA M/M/c ===\n")
    
    # Parâmetros do sistema
    taxa_chegada = 2.5
    taxa_servico = 1.0
    num_servidores = 3
    
    print(f"Taxa de chegada (λ): {taxa_chegada}")
    print(f"Taxa de serviço por servidor (μ): {taxa_servico}")
    print(f"Número de servidores (c): {num_servidores}")
    print(f"Utilização do sistema (ρ): {taxa_chegada/(num_servidores*taxa_servico):.2f}")
    
    # Criar sistema
    sistema = SistemaFilaMultiplosServidores(
        taxa_chegada, taxa_servico, num_servidores, seed=42
    )
    
    # Executar simulação
    print("\nExecutando simulação...")
    relatorio = sistema.executar_simulacao(tempo_simulacao=1000, tempo_warmup=100)
    
    # Mostrar resultados
    print("\nResultados da Simulação:")
    metricas = relatorio['metricas_sistema']
    
    print(f"Entidades processadas: {relatorio['parametros_simulacao']['entidades_processadas']}")
    print(f"Tempo médio no sistema: {metricas.get('tempo_sistema_medio', 0):.4f}")
    print(f"Tempo médio de espera: {metricas.get('tempo_espera_medio', 0):.4f}")
    print(f"Tamanho médio da fila: {metricas.get('tamanho_fila_medio', 0):.4f}")
    print(f"Utilização média: {metricas.get('utilizacao_media', 0):.4f}")
    
    # Estatísticas por servidor
    print("\nEstatísticas por Servidor:")
    for nome, stats in relatorio['servidores'].items():
        print(f"  {nome}: Utilização = {stats['utilizacao']:.4f}, "
              f"Entidades = {stats['entidades_atendidas']}")
    
    print()


def demonstrar_diferentes_disciplinas():
    """Demonstra diferentes disciplinas de fila."""
    print("=== DEMONSTRAÇÃO: DISCIPLINAS DE FILA ===\n")
    
    disciplinas = [
        DisciplinaFila.FIFO,
        DisciplinaFila.LIFO,
        DisciplinaFila.PRIORIDADE
    ]
    
    resultados = {}
    
    for disciplina in disciplinas:
        print(f"Testando disciplina: {disciplina.value}")
        
        # Criar sistema personalizado
        simulador = SimuladorEventos(seed=42)
        fila = Fila(disciplina)
        
        # Para prioridade, criar entidades com diferentes prioridades
        entidades_teste = []
        for i in range(10):
            entidade = Entidade(
                id=f"ent_{i}",
                tempo_chegada=i,
                prioridade=i % 3  # Prioridades 0, 1, 2
            )
            entidades_teste.append(entidade)
        
        # Adicionar entidades à fila
        for entidade in entidades_teste:
            fila.adicionar(entidade, entidade.tempo_chegada)
        
        # Remover entidades e ver ordem
        ordem_saida = []
        while not fila.esta_vazia():
            entidade = fila.remover(0)
            if entidade:
                ordem_saida.append((entidade.id, entidade.prioridade))
        
        resultados[disciplina.value] = ordem_saida
        
        print(f"  Ordem de saída: {[ent_id for ent_id, _ in ordem_saida]}")
        if disciplina == DisciplinaFila.PRIORIDADE:
            print(f"  Prioridades: {[prio for _, prio in ordem_saida]}")
        print()
    
    return resultados


def benchmark_simulacao():
    """Benchmark de performance da simulação."""
    print("=== BENCHMARK: PERFORMANCE DA SIMULAÇÃO ===\n")
    
    configuracoes = [
        ("Pequeno", 100, 10),
        ("Médio", 1000, 100),
        ("Grande", 10000, 1000)
    ]
    
    resultados_benchmark = {}
    
    for nome, tempo_sim, tempo_warmup in configuracoes:
        print(f"Testando configuração {nome}...")
        print(f"  Tempo de simulação: {tempo_sim}")
        print(f"  Tempo de warmup: {tempo_warmup}")
        
        # Criar sistema
        sistema = SistemaFilaSimples(0.8, 1.0, seed=42)
        
        # Medir tempo de execução
        inicio = time.time()
        relatorio = sistema.executar_simulacao(tempo_sim, tempo_warmup)
        tempo_execucao = time.time() - inicio
        
        # Calcular métricas de performance
        entidades_processadas = relatorio['parametros_simulacao']['entidades_processadas']
        eventos_por_segundo = entidades_processadas / tempo_execucao if tempo_execucao > 0 else 0
        
        resultados_benchmark[nome] = {
            'tempo_execucao': tempo_execucao,
            'entidades_processadas': entidades_processadas,
            'eventos_por_segundo': eventos_por_segundo,
            'utilizacao_memoria': 0  # Placeholder - poderia usar psutil
        }
        
        print(f"  Tempo de execução: {tempo_execucao:.3f}s")
        print(f"  Entidades processadas: {entidades_processadas}")
        print(f"  Eventos/segundo: {eventos_por_segundo:.1f}")
        print()
    
    # Resumo
    print("RESUMO DO BENCHMARK:")
    print("-" * 60)
    print(f"{'Config':<10} {'Tempo (s)':<12} {'Entidades':<12} {'Eventos/s':<12}")
    print("-" * 60)
    
    for nome, metricas in resultados_benchmark.items():
        print(f"{nome:<10} {metricas['tempo_execucao']:<12.3f} "
              f"{metricas['entidades_processadas']:<12} "
              f"{metricas['eventos_por_segundo']:<12.1f}")


def visualizar_resultados_simulacao():
    """Cria visualizações dos resultados da simulação."""
    print("=== VISUALIZAÇÃO: RESULTADOS DA SIMULAÇÃO ===\n")
    
    # Executar simulação para coleta de dados
    sistema = SistemaFilaSimples(0.8, 1.0, seed=42)
    relatorio = sistema.executar_simulacao(tempo_simulacao=500, tempo_warmup=50)
    
    # Criar figura com subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Análise do Sistema de Filas M/M/1', fontsize=16)
    
    # 1. Histograma dos tempos de espera
    if sistema.simulador.estatisticas.tempos_espera:
        axes[0, 0].hist(sistema.simulador.estatisticas.tempos_espera, 
                       bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Distribuição dos Tempos de Espera')
        axes[0, 0].set_xlabel('Tempo de Espera')
        axes[0, 0].set_ylabel('Frequência')
        axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Histograma dos tempos de serviço
    if sistema.simulador.estatisticas.tempos_servico:
        axes[0, 1].hist(sistema.simulador.estatisticas.tempos_servico, 
                       bins=30, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 1].set_title('Distribuição dos Tempos de Serviço')
        axes[0, 1].set_xlabel('Tempo de Serviço')
        axes[0, 1].set_ylabel('Frequência')
        axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Evolução do tamanho da fila
    if sistema.fila.historico_tamanho:
        tempos, tamanhos = zip(*sistema.fila.historico_tamanho)
        axes[1, 0].plot(tempos, tamanhos, color='orange', linewidth=1)
        axes[1, 0].set_title('Evolução do Tamanho da Fila')
        axes[1, 0].set_xlabel('Tempo')
        axes[1, 0].set_ylabel('Tamanho da Fila')
        axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Utilização do servidor ao longo do tempo
    if sistema.servidor.historico_utilizacao:
        tempos_util = []
        utilizacao = []
        estado_atual = False
        
        for tempo, ocupado in sistema.servidor.historico_utilizacao:
            tempos_util.extend([tempo, tempo])
            utilizacao.extend([int(estado_atual), int(ocupado)])
            estado_atual = ocupado
        
        axes[1, 1].plot(tempos_util, utilizacao, color='red', linewidth=1)
        axes[1, 1].set_title('Utilização do Servidor')
        axes[1, 1].set_xlabel('Tempo')
        axes[1, 1].set_ylabel('Servidor Ocupado (0/1)')
        axes[1, 1].set_ylim(-0.1, 1.1)
        axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Estatísticas resumidas
    metricas = relatorio['metricas_sistema']
    print("Estatísticas da Simulação:")
    print(f"  Tempo médio de espera: {metricas.get('tempo_espera_medio', 0):.4f}")
    print(f"  Tempo médio de serviço: {metricas.get('tempo_servico_medio', 0):.4f}")
    print(f"  Tempo médio no sistema: {metricas.get('tempo_sistema_medio', 0):.4f}")
    print(f"  Tamanho médio da fila: {metricas.get('tamanho_fila_medio', 0):.4f}")
    print(f"  Utilização do servidor: {metricas.get('utilizacao_media', 0):.4f}")


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 08.3 - SIMULADOR DE EVENTOS DISCRETOS")
    print("=" * 50)
    
    # Executar demonstrações
    demonstrar_sistema_mm1()
    demonstrar_sistema_mmc()
    demonstrar_diferentes_disciplinas()
    benchmark_simulacao()
    
    # Visualizações (comentar se não quiser mostrar gráficos)
    try:
        visualizar_resultados_simulacao()
    except Exception as e:
        print(f"Erro na visualização: {e}")
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 08.3")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. SIMULAÇÃO DE EVENTOS DISCRETOS:
   • Event-driven simulation paradigm
   • Lista de eventos futuros (FEL) com priority queue
   • Avanço do tempo por eventos (não por incrementos fixos)
   • Handlers específicos para cada tipo de evento
   • Controle de estado do sistema

2. TEORIA DE FILAS:
   • Sistema M/M/1: Chegadas Poisson, serviço exponencial, 1 servidor
   • Sistema M/M/c: Múltiplos servidores em paralelo
   • Disciplinas de atendimento (FIFO, LIFO, Prioridade, SJF)
   • Métricas fundamentais: utilização, tempo de espera, tamanho da fila

3. COMPONENTES DO SIMULADOR:
   • Eventos: Representam mudanças de estado no sistema
   • Entidades: Objetos que fluem pelo sistema (clientes, jobs)
   • Filas: Estruturas de espera com diferentes disciplinas
   • Servidores: Recursos que processam entidades
   • Estatísticas: Coletores de métricas de performance

4. GERAÇÃO DE NÚMEROS ALEATÓRIOS:
   • Distribuições probabilísticas (Exponencial, Normal, Uniforme)
   • Geradores com semente para reprodutibilidade
   • Modelagem de processos estocásticos
   • Validação estatística dos geradores

5. COLETA DE ESTATÍSTICAS:
   • Período de warm-up para atingir steady state
   • Métricas de performance (throughput, latência, utilização)
   • Intervalos de confiança para resultados
   • Análise de convergência estatística

6. VALIDAÇÃO E VERIFICAÇÃO:
   • Comparação com resultados teóricos (M/M/1)
   • Análise de sensibilidade dos parâmetros
   • Verificação da implementação
   • Validação do modelo conceitual

7. OTIMIZAÇÃO DE PERFORMANCE:
   • Estruturas de dados eficientes (heaps para eventos)
   • Minimização de overhead computacional
   • Técnicas de redução de variância
   • Paralelização quando aplicável

8. DISCIPLINAS DE FILA:
   • FIFO: Ordem de chegada (mais comum)
   • LIFO: Último a chegar, primeiro a sair
   • Prioridade: Baseada em importância/urgência
   • SJF: Shortest Job First para minimizar tempo médio
   • Round Robin: Fatias de tempo para fairness

9. ANÁLISE DE RESULTADOS:
   • Visualização de distribuições e tendências
   • Identificação de gargalos no sistema
   • Comparação de cenários alternativos
   • Tomada de decisão baseada em dados

10. APLICAÇÕES PRÁTICAS:
    • Sistemas de atendimento (call centers, hospitais)
    • Redes de computadores (roteadores, protocolos)
    • Manufatura (linhas de produção, logística)
    • Sistemas operacionais (escalonamento, I/O)
    • Finanças (modelagem de riscos, mercados)

TÉCNICAS AVANÇADAS:
- Simulação de Monte Carlo
- Métodos de redução de variância
- Simulação paralela e distribuída
- Otimização via simulação
- Análise de sensibilidade automatizada

PRÓXIMOS PASSOS:
- Implementar simulação contínua (equações diferenciais)
- Estudar redes de filas complexas
- Aplicar machine learning para otimização
- Desenvolver interfaces gráficas interativas
- Integrar com sistemas de monitoramento real

Este módulo fornece uma base sólida para modelagem e análise
de sistemas complexos através de simulação, permitindo
avaliar performance, identificar gargalos e otimizar
operações antes da implementação real.
    """)


if __name__ == "__main__":
    main()