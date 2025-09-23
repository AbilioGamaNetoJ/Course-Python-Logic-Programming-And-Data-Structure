"""
MÓDULO 07.4 - PROFILING E PERFORMANCE
====================================

Objetivos de Aprendizado:
- Dominar ferramentas de profiling em Python
- Identificar gargalos de performance
- Medir tempo de execução e uso de memória
- Implementar benchmarking sistemático
- Otimizar código baseado em dados
- Usar profilers para análise detalhada
- Aplicar técnicas de monitoramento

Conceitos Abordados:
- Profiling de CPU e memória
- Benchmarking e medição de performance
- Identificação de hotspots
- Análise de call stack
- Monitoramento de recursos
- Otimização baseada em dados
- Ferramentas de debugging de performance

Ferramentas Utilizadas:
- cProfile: profiling de CPU
- memory_profiler: profiling de memória
- timeit: medição precisa de tempo
- psutil: monitoramento de sistema
- tracemalloc: rastreamento de memória
- line_profiler: profiling linha por linha
- py-spy: profiling em produção

Pré-requisitos:
- Análise de complexidade
- Estruturas de dados
- Conceitos de sistema operacional
- Estatística básica
"""

import cProfile
import pstats
import io
import time
import timeit
import sys
import gc
import psutil
import os
import tracemalloc
import threading
import multiprocessing
from typing import List, Dict, Any, Callable, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import functools
import contextlib
import matplotlib.pyplot as plt
import numpy as np
from memory_profiler import profile as memory_profile


class TipoProfiler(Enum):
    """Tipos de profiler disponíveis."""
    CPU = "CPU Profiler"
    MEMORIA = "Memory Profiler"
    LINHA = "Line Profiler"
    SISTEMA = "System Monitor"


@dataclass
class MedicaoTempo:
    """Medição de tempo de execução."""
    nome: str
    tempo_medio: float
    tempo_min: float
    tempo_max: float
    desvio_padrao: float
    num_execucoes: int
    tempo_total: float
    
    @property
    def throughput(self) -> float:
        """Throughput (execuções por segundo)."""
        return self.num_execucoes / self.tempo_total if self.tempo_total > 0 else 0


@dataclass
class MedicaoMemoria:
    """Medição de uso de memória."""
    nome: str
    memoria_inicial: int
    memoria_final: int
    memoria_pico: int
    memoria_media: int
    num_alocacoes: int
    tamanho_medio_alocacao: float
    
    @property
    def memoria_usada(self) -> int:
        """Memória total usada."""
        return self.memoria_final - self.memoria_inicial


@dataclass
class PerfilCPU:
    """Perfil de CPU de uma função."""
    nome: str
    tempo_total: float
    tempo_proprio: float
    num_chamadas: int
    tempo_por_chamada: float
    funcoes_chamadas: Dict[str, int] = field(default_factory=dict)
    hotspots: List[str] = field(default_factory=list)


@dataclass
class RelatorioPerformance:
    """Relatório completo de performance."""
    nome: str
    medicao_tempo: Optional[MedicaoTempo] = None
    medicao_memoria: Optional[MedicaoMemoria] = None
    perfil_cpu: Optional[PerfilCPU] = None
    recomendacoes: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


class ProfilerTempo:
    """
    Profiler para medição precisa de tempo.
    """
    
    def __init__(self):
        """Inicializa o profiler de tempo."""
        self.medicoes: Dict[str, List[float]] = defaultdict(list)
    
    @contextlib.contextmanager
    def medir(self, nome: str):
        """
        Context manager para medir tempo de execução.
        
        Args:
            nome: Nome da medição
        """
        inicio = time.perf_counter()
        try:
            yield
        finally:
            fim = time.perf_counter()
            tempo = fim - inicio
            self.medicoes[nome].append(tempo)
    
    def medir_funcao(self, func: Callable, *args, nome: str = "", 
                    num_execucoes: int = 100, **kwargs) -> MedicaoTempo:
        """
        Mede tempo de execução de uma função.
        
        Args:
            func: Função a ser medida
            *args: Argumentos da função
            nome: Nome da medição
            num_execucoes: Número de execuções
            **kwargs: Argumentos nomeados
        
        Returns:
            Medição de tempo
        """
        nome = nome or func.__name__
        tempos = []
        
        # Aquecimento
        for _ in range(min(10, num_execucoes // 10)):
            func(*args, **kwargs)
        
        # Medições
        tempo_total_inicio = time.perf_counter()
        for _ in range(num_execucoes):
            inicio = time.perf_counter()
            func(*args, **kwargs)
            fim = time.perf_counter()
            tempos.append(fim - inicio)
        tempo_total_fim = time.perf_counter()
        
        # Calcular estatísticas
        tempo_medio = sum(tempos) / len(tempos)
        tempo_min = min(tempos)
        tempo_max = max(tempos)
        
        # Desvio padrão
        variancia = sum((t - tempo_medio) ** 2 for t in tempos) / len(tempos)
        desvio_padrao = variancia ** 0.5
        
        return MedicaoTempo(
            nome=nome,
            tempo_medio=tempo_medio,
            tempo_min=tempo_min,
            tempo_max=tempo_max,
            desvio_padrao=desvio_padrao,
            num_execucoes=num_execucoes,
            tempo_total=tempo_total_fim - tempo_total_inicio
        )
    
    def benchmark_comparativo(self, funcoes: Dict[str, Callable], 
                            args: tuple = (), kwargs: dict = None,
                            num_execucoes: int = 100) -> Dict[str, MedicaoTempo]:
        """
        Compara performance de múltiplas funções.
        
        Args:
            funcoes: Dicionário {nome: função}
            args: Argumentos para as funções
            kwargs: Argumentos nomeados
            num_execucoes: Número de execuções por função
        
        Returns:
            Dicionário com medições
        """
        kwargs = kwargs or {}
        resultados = {}
        
        for nome, func in funcoes.items():
            medicao = self.medir_funcao(func, *args, nome=nome, 
                                      num_execucoes=num_execucoes, **kwargs)
            resultados[nome] = medicao
        
        return resultados
    
    def obter_estatisticas(self, nome: str) -> Optional[MedicaoTempo]:
        """
        Obtém estatísticas de uma medição.
        
        Args:
            nome: Nome da medição
        
        Returns:
            Estatísticas da medição
        """
        if nome not in self.medicoes:
            return None
        
        tempos = self.medicoes[nome]
        tempo_medio = sum(tempos) / len(tempos)
        tempo_min = min(tempos)
        tempo_max = max(tempos)
        
        variancia = sum((t - tempo_medio) ** 2 for t in tempos) / len(tempos)
        desvio_padrao = variancia ** 0.5
        
        return MedicaoTempo(
            nome=nome,
            tempo_medio=tempo_medio,
            tempo_min=tempo_min,
            tempo_max=tempo_max,
            desvio_padrao=desvio_padrao,
            num_execucoes=len(tempos),
            tempo_total=sum(tempos)
        )


class ProfilerMemoria:
    """
    Profiler para análise de uso de memória.
    """
    
    def __init__(self):
        """Inicializa o profiler de memória."""
        self.processo = psutil.Process(os.getpid())
        self.medicoes: List[MedicaoMemoria] = []
    
    @contextlib.contextmanager
    def monitorar(self, nome: str, intervalo: float = 0.1):
        """
        Context manager para monitorar uso de memória.
        
        Args:
            nome: Nome da medição
            intervalo: Intervalo de amostragem em segundos
        """
        # Forçar garbage collection
        gc.collect()
        
        # Iniciar rastreamento
        tracemalloc.start()
        memoria_inicial = self.processo.memory_info().rss
        
        # Monitoramento em thread separada
        memorias = []
        parar_monitoramento = threading.Event()
        
        def monitor():
            while not parar_monitoramento.is_set():
                memorias.append(self.processo.memory_info().rss)
                time.sleep(intervalo)
        
        thread_monitor = threading.Thread(target=monitor)
        thread_monitor.start()
        
        try:
            yield
        finally:
            parar_monitoramento.set()
            thread_monitor.join()
            
            # Obter estatísticas finais
            memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            memoria_final = self.processo.memory_info().rss
            memoria_media = sum(memorias) / len(memorias) if memorias else memoria_inicial
            
            medicao = MedicaoMemoria(
                nome=nome,
                memoria_inicial=memoria_inicial,
                memoria_final=memoria_final,
                memoria_pico=memoria_pico,
                memoria_media=int(memoria_media),
                num_alocacoes=0,  # Seria necessário instrumentação adicional
                tamanho_medio_alocacao=0.0
            )
            
            self.medicoes.append(medicao)
    
    def medir_funcao(self, func: Callable, *args, nome: str = "", **kwargs) -> MedicaoMemoria:
        """
        Mede uso de memória de uma função.
        
        Args:
            func: Função a ser medida
            *args: Argumentos da função
            nome: Nome da medição
            **kwargs: Argumentos nomeados
        
        Returns:
            Medição de memória
        """
        nome = nome or func.__name__
        
        with self.monitorar(nome):
            resultado = func(*args, **kwargs)
        
        return self.medicoes[-1]
    
    def analisar_vazamentos(self, func: Callable, *args, 
                          num_iteracoes: int = 10, **kwargs) -> List[int]:
        """
        Analisa possíveis vazamentos de memória.
        
        Args:
            func: Função a ser analisada
            *args: Argumentos da função
            num_iteracoes: Número de iterações
            **kwargs: Argumentos nomeados
        
        Returns:
            Lista com uso de memória por iteração
        """
        memorias = []
        
        for i in range(num_iteracoes):
            gc.collect()  # Forçar limpeza
            memoria_antes = self.processo.memory_info().rss
            
            func(*args, **kwargs)
            
            gc.collect()  # Forçar limpeza novamente
            memoria_depois = self.processo.memory_info().rss
            
            memorias.append(memoria_depois - memoria_antes)
        
        return memorias


class ProfilerCPU:
    """
    Profiler para análise de CPU.
    """
    
    def __init__(self):
        """Inicializa o profiler de CPU."""
        self.perfis: Dict[str, PerfilCPU] = {}
    
    def perfilar_funcao(self, func: Callable, *args, nome: str = "", **kwargs) -> PerfilCPU:
        """
        Perfila execução de uma função.
        
        Args:
            func: Função a ser perfilada
            *args: Argumentos da função
            nome: Nome do perfil
            **kwargs: Argumentos nomeados
        
        Returns:
            Perfil de CPU
        """
        nome = nome or func.__name__
        
        # Criar profiler
        profiler = cProfile.Profile()
        
        # Executar com profiling
        profiler.enable()
        resultado = func(*args, **kwargs)
        profiler.disable()
        
        # Analisar resultados
        stats_stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.sort_stats('cumulative')
        
        # Extrair informações principais
        total_calls = stats.total_calls
        total_time = stats.total_tt
        
        # Obter função principal
        func_stats = None
        for func_info, (cc, nc, tt, ct, callers) in stats.stats.items():
            if func_info[2] == func.__name__:
                func_stats = (cc, nc, tt, ct)
                break
        
        if func_stats:
            cc, nc, tt, ct = func_stats
            tempo_proprio = tt
            tempo_total = ct
            num_chamadas = cc
            tempo_por_chamada = ct / cc if cc > 0 else 0
        else:
            tempo_proprio = total_time
            tempo_total = total_time
            num_chamadas = 1
            tempo_por_chamada = total_time
        
        # Identificar hotspots (top 5 funções por tempo)
        hotspots = []
        stats.sort_stats('tottime')
        stats_stream.seek(0)
        stats_stream.truncate(0)
        stats.print_stats(5)
        
        perfil = PerfilCPU(
            nome=nome,
            tempo_total=tempo_total,
            tempo_proprio=tempo_proprio,
            num_chamadas=num_chamadas,
            tempo_por_chamada=tempo_por_chamada,
            hotspots=hotspots
        )
        
        self.perfis[nome] = perfil
        return perfil
    
    def comparar_perfis(self, perfis: List[str]) -> Dict[str, Any]:
        """
        Compara múltiplos perfis de CPU.
        
        Args:
            perfis: Lista de nomes de perfis
        
        Returns:
            Comparação dos perfis
        """
        comparacao = {
            'tempos_totais': {},
            'tempos_proprios': {},
            'num_chamadas': {},
            'eficiencia': {}
        }
        
        for nome in perfis:
            if nome in self.perfis:
                perfil = self.perfis[nome]
                comparacao['tempos_totais'][nome] = perfil.tempo_total
                comparacao['tempos_proprios'][nome] = perfil.tempo_proprio
                comparacao['num_chamadas'][nome] = perfil.num_chamadas
                comparacao['eficiencia'][nome] = perfil.tempo_por_chamada
        
        return comparacao


class MonitorSistema:
    """
    Monitor de recursos do sistema.
    """
    
    def __init__(self, intervalo: float = 1.0):
        """
        Inicializa monitor do sistema.
        
        Args:
            intervalo: Intervalo de amostragem em segundos
        """
        self.intervalo = intervalo
        self.processo = psutil.Process(os.getpid())
        self.historico: Dict[str, List[float]] = defaultdict(list)
        self.monitorando = False
        self.thread_monitor = None
    
    def iniciar_monitoramento(self):
        """Inicia monitoramento contínuo."""
        if self.monitorando:
            return
        
        self.monitorando = True
        self.thread_monitor = threading.Thread(target=self._monitorar)
        self.thread_monitor.start()
    
    def parar_monitoramento(self):
        """Para monitoramento contínuo."""
        self.monitorando = False
        if self.thread_monitor:
            self.thread_monitor.join()
    
    def _monitorar(self):
        """Loop de monitoramento."""
        while self.monitorando:
            try:
                # CPU
                cpu_percent = self.processo.cpu_percent()
                self.historico['cpu'].append(cpu_percent)
                
                # Memória
                memoria = self.processo.memory_info()
                self.historico['memoria_rss'].append(memoria.rss)
                self.historico['memoria_vms'].append(memoria.vms)
                
                # Sistema
                cpu_sistema = psutil.cpu_percent()
                memoria_sistema = psutil.virtual_memory()
                
                self.historico['cpu_sistema'].append(cpu_sistema)
                self.historico['memoria_sistema'].append(memoria_sistema.percent)
                
                # Threads
                num_threads = self.processo.num_threads()
                self.historico['threads'].append(num_threads)
                
                time.sleep(self.intervalo)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break
    
    def obter_estatisticas(self) -> Dict[str, Dict[str, float]]:
        """
        Obtém estatísticas do monitoramento.
        
        Returns:
            Estatísticas por métrica
        """
        stats = {}
        
        for metrica, valores in self.historico.items():
            if valores:
                stats[metrica] = {
                    'media': sum(valores) / len(valores),
                    'min': min(valores),
                    'max': max(valores),
                    'atual': valores[-1] if valores else 0
                }
        
        return stats
    
    def plotar_historico(self, metricas: List[str] = None):
        """
        Plota histórico de métricas.
        
        Args:
            metricas: Lista de métricas a plotar
        """
        if not metricas:
            metricas = ['cpu', 'memoria_rss', 'cpu_sistema', 'memoria_sistema']
        
        fig, axes = plt.subplots(len(metricas), 1, figsize=(12, 3 * len(metricas)))
        if len(metricas) == 1:
            axes = [axes]
        
        for i, metrica in enumerate(metricas):
            if metrica in self.historico and self.historico[metrica]:
                valores = self.historico[metrica]
                tempo = list(range(len(valores)))
                
                axes[i].plot(tempo, valores, label=metrica)
                axes[i].set_title(f'{metrica.replace("_", " ").title()}')
                axes[i].set_xlabel('Tempo (amostras)')
                
                if 'cpu' in metrica:
                    axes[i].set_ylabel('CPU (%)')
                elif 'memoria' in metrica:
                    if 'sistema' in metrica:
                        axes[i].set_ylabel('Memória (%)')
                    else:
                        axes[i].set_ylabel('Memória (bytes)')
                elif 'threads' in metrica:
                    axes[i].set_ylabel('Número de Threads')
                
                axes[i].grid(True, alpha=0.3)
                axes[i].legend()
        
        plt.tight_layout()
        plt.show()


class BenchmarkSuite:
    """
    Suite completa de benchmarking.
    """
    
    def __init__(self):
        """Inicializa suite de benchmark."""
        self.profiler_tempo = ProfilerTempo()
        self.profiler_memoria = ProfilerMemoria()
        self.profiler_cpu = ProfilerCPU()
        self.monitor_sistema = MonitorSistema()
        self.relatorios: List[RelatorioPerformance] = []
    
    def benchmark_completo(self, func: Callable, *args, nome: str = "",
                          num_execucoes: int = 100, **kwargs) -> RelatorioPerformance:
        """
        Executa benchmark completo de uma função.
        
        Args:
            func: Função a ser testada
            *args: Argumentos da função
            nome: Nome do benchmark
            num_execucoes: Número de execuções
            **kwargs: Argumentos nomeados
        
        Returns:
            Relatório completo de performance
        """
        nome = nome or func.__name__
        
        print(f"Executando benchmark completo: {nome}")
        
        # Medição de tempo
        print("  - Medindo tempo...")
        medicao_tempo = self.profiler_tempo.medir_funcao(
            func, *args, nome=nome, num_execucoes=num_execucoes, **kwargs
        )
        
        # Medição de memória
        print("  - Medindo memória...")
        medicao_memoria = self.profiler_memoria.medir_funcao(
            func, *args, nome=nome, **kwargs
        )
        
        # Profiling de CPU
        print("  - Perfilando CPU...")
        perfil_cpu = self.profiler_cpu.perfilar_funcao(
            func, *args, nome=nome, **kwargs
        )
        
        # Gerar recomendações
        recomendacoes = self._gerar_recomendacoes(
            medicao_tempo, medicao_memoria, perfil_cpu
        )
        
        relatorio = RelatorioPerformance(
            nome=nome,
            medicao_tempo=medicao_tempo,
            medicao_memoria=medicao_memoria,
            perfil_cpu=perfil_cpu,
            recomendacoes=recomendacoes
        )
        
        self.relatorios.append(relatorio)
        return relatorio
    
    def _gerar_recomendacoes(self, tempo: MedicaoTempo, 
                           memoria: MedicaoMemoria, 
                           cpu: PerfilCPU) -> List[str]:
        """
        Gera recomendações baseadas nas medições.
        
        Args:
            tempo: Medição de tempo
            memoria: Medição de memória
            cpu: Perfil de CPU
        
        Returns:
            Lista de recomendações
        """
        recomendacoes = []
        
        # Análise de tempo
        if tempo.desvio_padrao / tempo.tempo_medio > 0.1:
            recomendacoes.append(
                "Alta variabilidade no tempo de execução - "
                "considere otimizar algoritmo ou reduzir dependências externas"
            )
        
        if tempo.tempo_medio > 1.0:
            recomendacoes.append(
                "Tempo de execução alto - "
                "considere paralelização ou otimização algorítmica"
            )
        
        # Análise de memória
        if memoria.memoria_usada > 100 * 1024 * 1024:  # 100MB
            recomendacoes.append(
                "Alto uso de memória - "
                "considere algoritmos in-place ou processamento em lotes"
            )
        
        # Análise de CPU
        if cpu.num_chamadas > 1000:
            recomendacoes.append(
                "Muitas chamadas de função - "
                "considere inlining ou redução de overhead"
            )
        
        if cpu.tempo_proprio / cpu.tempo_total < 0.5:
            recomendacoes.append(
                "Muito tempo gasto em chamadas de função - "
                "analise dependências e considere otimizações"
            )
        
        return recomendacoes
    
    def comparar_implementacoes(self, implementacoes: Dict[str, Callable],
                              args: tuple = (), kwargs: dict = None,
                              num_execucoes: int = 100) -> Dict[str, RelatorioPerformance]:
        """
        Compara múltiplas implementações.
        
        Args:
            implementacoes: Dicionário {nome: função}
            args: Argumentos para as funções
            kwargs: Argumentos nomeados
            num_execucoes: Número de execuções
        
        Returns:
            Dicionário com relatórios
        """
        kwargs = kwargs or {}
        relatorios = {}
        
        print(f"Comparando {len(implementacoes)} implementações...")
        
        for nome, func in implementacoes.items():
            print(f"\nTestando: {nome}")
            relatorio = self.benchmark_completo(
                func, *args, nome=nome, num_execucoes=num_execucoes, **kwargs
            )
            relatorios[nome] = relatorio
        
        # Análise comparativa
        self._analisar_comparacao(relatorios)
        
        return relatorios
    
    def _analisar_comparacao(self, relatorios: Dict[str, RelatorioPerformance]):
        """
        Analisa comparação entre implementações.
        
        Args:
            relatorios: Relatórios a comparar
        """
        print("\n" + "=" * 50)
        print("ANÁLISE COMPARATIVA")
        print("=" * 50)
        
        # Comparação de tempo
        tempos = {nome: rel.medicao_tempo.tempo_medio 
                 for nome, rel in relatorios.items()}
        melhor_tempo = min(tempos.values())
        pior_tempo = max(tempos.values())
        
        print("\nTEMPO DE EXECUÇÃO:")
        for nome, tempo in sorted(tempos.items(), key=lambda x: x[1]):
            speedup = pior_tempo / tempo
            print(f"  {nome:20s}: {tempo*1000:8.2f}ms (speedup: {speedup:.2f}x)")
        
        # Comparação de memória
        memorias = {nome: rel.medicao_memoria.memoria_usada 
                   for nome, rel in relatorios.items()}
        
        print("\nUSO DE MEMÓRIA:")
        for nome, memoria in sorted(memorias.items(), key=lambda x: x[1]):
            print(f"  {nome:20s}: {memoria/1024/1024:8.2f}MB")
        
        # Recomendação geral
        melhor_geral = min(relatorios.keys(), 
                          key=lambda x: tempos[x] * memorias[x])
        print(f"\nMELHOR IMPLEMENTAÇÃO GERAL: {melhor_geral}")
    
    def gerar_relatorio_html(self, arquivo: str = "benchmark_report.html"):
        """
        Gera relatório HTML dos benchmarks.
        
        Args:
            arquivo: Nome do arquivo HTML
        """
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Relatório de Performance</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .relatorio { border: 1px solid #ccc; margin: 20px 0; padding: 15px; }
                .metrica { margin: 10px 0; }
                .recomendacao { background: #f0f8ff; padding: 10px; margin: 5px 0; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Relatório de Performance</h1>
        """
        
        for relatorio in self.relatorios:
            html += f"""
            <div class="relatorio">
                <h2>{relatorio.nome}</h2>
                
                <h3>Tempo de Execução</h3>
                <div class="metrica">
                    <strong>Tempo Médio:</strong> {relatorio.medicao_tempo.tempo_medio*1000:.2f}ms<br>
                    <strong>Desvio Padrão:</strong> {relatorio.medicao_tempo.desvio_padrao*1000:.2f}ms<br>
                    <strong>Throughput:</strong> {relatorio.medicao_tempo.throughput:.2f} exec/s
                </div>
                
                <h3>Uso de Memória</h3>
                <div class="metrica">
                    <strong>Memória Usada:</strong> {relatorio.medicao_memoria.memoria_usada/1024/1024:.2f}MB<br>
                    <strong>Pico de Memória:</strong> {relatorio.medicao_memoria.memoria_pico/1024/1024:.2f}MB
                </div>
                
                <h3>Perfil de CPU</h3>
                <div class="metrica">
                    <strong>Tempo Total:</strong> {relatorio.perfil_cpu.tempo_total:.4f}s<br>
                    <strong>Número de Chamadas:</strong> {relatorio.perfil_cpu.num_chamadas}
                </div>
                
                <h3>Recomendações</h3>
            """
            
            for rec in relatorio.recomendacoes:
                html += f'<div class="recomendacao">{rec}</div>'
            
            html += "</div>"
        
        html += """
        </body>
        </html>
        """
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Relatório HTML gerado: {arquivo}")


# Exemplos de Algoritmos para Benchmark
class AlgoritmosBenchmark:
    """
    Algoritmos de exemplo para benchmarking.
    """
    
    @staticmethod
    def ordenacao_bubble(arr: List[int]) -> List[int]:
        """Bubble sort - O(n²) tempo, O(1) espaço."""
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    @staticmethod
    def ordenacao_quick(arr: List[int]) -> List[int]:
        """Quick sort - O(n log n) tempo médio, O(log n) espaço."""
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        esquerda = [x for x in arr if x < pivot]
        meio = [x for x in arr if x == pivot]
        direita = [x for x in arr if x > pivot]
        
        return (AlgoritmosBenchmark.ordenacao_quick(esquerda) + 
                meio + 
                AlgoritmosBenchmark.ordenacao_quick(direita))
    
    @staticmethod
    def ordenacao_merge(arr: List[int]) -> List[int]:
        """Merge sort - O(n log n) tempo, O(n) espaço."""
        if len(arr) <= 1:
            return arr
        
        meio = len(arr) // 2
        esquerda = AlgoritmosBenchmark.ordenacao_merge(arr[:meio])
        direita = AlgoritmosBenchmark.ordenacao_merge(arr[meio:])
        
        return AlgoritmosBenchmark._merge(esquerda, direita)
    
    @staticmethod
    def _merge(esquerda: List[int], direita: List[int]) -> List[int]:
        """Combina duas listas ordenadas."""
        resultado = []
        i = j = 0
        
        while i < len(esquerda) and j < len(direita):
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1
        
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        return resultado
    
    @staticmethod
    def fibonacci_recursivo(n: int) -> int:
        """Fibonacci recursivo - O(2^n) tempo."""
        if n <= 1:
            return n
        return (AlgoritmosBenchmark.fibonacci_recursivo(n-1) + 
                AlgoritmosBenchmark.fibonacci_recursivo(n-2))
    
    @staticmethod
    def fibonacci_iterativo(n: int) -> int:
        """Fibonacci iterativo - O(n) tempo, O(1) espaço."""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    @staticmethod
    def fibonacci_memoizado(n: int, memo: dict = None) -> int:
        """Fibonacci com memoização - O(n) tempo, O(n) espaço."""
        if memo is None:
            memo = {}
        if n in memo:
            return memo[n]
        if n <= 1:
            return n
        memo[n] = (AlgoritmosBenchmark.fibonacci_memoizado(n-1, memo) + 
                   AlgoritmosBenchmark.fibonacci_memoizado(n-2, memo))
        return memo[n]
    
    @staticmethod
    def busca_linear(arr: List[int], target: int) -> int:
        """Busca linear - O(n) tempo."""
        for i, valor in enumerate(arr):
            if valor == target:
                return i
        return -1
    
    @staticmethod
    def busca_binaria(arr: List[int], target: int) -> int:
        """Busca binária - O(log n) tempo."""
        esquerda, direita = 0, len(arr) - 1
        
        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            if arr[meio] == target:
                return meio
            elif arr[meio] < target:
                esquerda = meio + 1
            else:
                direita = meio - 1
        
        return -1


# Funções de Demonstração
def demonstrar_profiling_basico():
    """Demonstra profiling básico de tempo e memória."""
    print("=== DEMONSTRAÇÃO: PROFILING BÁSICO ===\n")
    
    profiler_tempo = ProfilerTempo()
    profiler_memoria = ProfilerMemoria()
    
    print("1. PROFILING DE TEMPO")
    
    # Testar diferentes algoritmos de ordenação
    import random
    dados = [random.randint(1, 1000) for _ in range(1000)]
    
    # Bubble sort
    medicao_bubble = profiler_tempo.medir_funcao(
        AlgoritmosBenchmark.ordenacao_bubble, dados, 
        nome="Bubble Sort", num_execucoes=10
    )
    
    # Quick sort
    medicao_quick = profiler_tempo.medir_funcao(
        AlgoritmosBenchmark.ordenacao_quick, dados,
        nome="Quick Sort", num_execucoes=10
    )
    
    # Merge sort
    medicao_merge = profiler_tempo.medir_funcao(
        AlgoritmosBenchmark.ordenacao_merge, dados,
        nome="Merge Sort", num_execucoes=10
    )
    
    print("   Resultados (1000 elementos, 10 execuções):")
    for medicao in [medicao_bubble, medicao_quick, medicao_merge]:
        print(f"   {medicao.nome:12s}: "
              f"{medicao.tempo_medio*1000:6.2f}ms ± {medicao.desvio_padrao*1000:5.2f}ms "
              f"(throughput: {medicao.throughput:.1f} exec/s)")
    
    print("\n2. PROFILING DE MEMÓRIA")
    
    # Testar uso de memória
    def criar_lista_grande(n):
        return [i**2 for i in range(n)]
    
    def criar_generator(n):
        return (i**2 for i in range(n))
    
    # Lista vs generator
    medicao_lista = profiler_memoria.medir_funcao(
        criar_lista_grande, 100000, nome="Lista"
    )
    
    medicao_gen = profiler_memoria.medir_funcao(
        criar_generator, 100000, nome="Generator"
    )
    
    print("   Uso de memória (100.000 elementos):")
    print(f"   Lista:     {medicao_lista.memoria_usada/1024/1024:6.2f}MB")
    print(f"   Generator: {medicao_gen.memoria_usada/1024:6.2f}KB")
    
    print("\n3. ANÁLISE DE VAZAMENTOS")
    
    def funcao_com_vazamento():
        # Simular vazamento criando referências circulares
        lista = []
        for i in range(1000):
            obj = {'id': i, 'ref': lista}
            lista.append(obj)
        return len(lista)
    
    def funcao_sem_vazamento():
        # Função limpa
        return sum(i**2 for i in range(1000))
    
    vazamentos1 = profiler_memoria.analisar_vazamentos(
        funcao_com_vazamento, num_iteracoes=5
    )
    
    vazamentos2 = profiler_memoria.analisar_vazamentos(
        funcao_sem_vazamento, num_iteracoes=5
    )
    
    print("   Análise de vazamentos (5 iterações):")
    print(f"   Com vazamento:    {vazamentos1}")
    print(f"   Sem vazamento:    {vazamentos2}")
    
    # Detectar tendência
    if len(vazamentos1) > 1:
        tendencia1 = sum(vazamentos1[1:]) / len(vazamentos1[1:]) - vazamentos1[0]
        tendencia2 = sum(vazamentos2[1:]) / len(vazamentos2[1:]) - vazamentos2[0]
        
        print(f"   Tendência 1: {tendencia1/1024:.1f}KB por iteração")
        print(f"   Tendência 2: {tendencia2/1024:.1f}KB por iteração")


def demonstrar_profiling_cpu():
    """Demonstra profiling de CPU."""
    print("\n=== DEMONSTRAÇÃO: PROFILING DE CPU ===\n")
    
    profiler_cpu = ProfilerCPU()
    
    print("1. PERFIL DE FIBONACCI RECURSIVO")
    
    # Perfilar fibonacci recursivo
    perfil_fib_rec = profiler_cpu.perfilar_funcao(
        AlgoritmosBenchmark.fibonacci_recursivo, 25, nome="Fibonacci Recursivo"
    )
    
    print(f"   Tempo total: {perfil_fib_rec.tempo_total:.4f}s")
    print(f"   Tempo próprio: {perfil_fib_rec.tempo_proprio:.4f}s")
    print(f"   Número de chamadas: {perfil_fib_rec.num_chamadas}")
    print(f"   Tempo por chamada: {perfil_fib_rec.tempo_por_chamada*1000:.4f}ms")
    
    print("\n2. PERFIL DE FIBONACCI ITERATIVO")
    
    # Perfilar fibonacci iterativo
    perfil_fib_iter = profiler_cpu.perfilar_funcao(
        AlgoritmosBenchmark.fibonacci_iterativo, 25, nome="Fibonacci Iterativo"
    )
    
    print(f"   Tempo total: {perfil_fib_iter.tempo_total:.4f}s")
    print(f"   Tempo próprio: {perfil_fib_iter.tempo_proprio:.4f}s")
    print(f"   Número de chamadas: {perfil_fib_iter.num_chamadas}")
    print(f"   Tempo por chamada: {perfil_fib_iter.tempo_por_chamada*1000:.4f}ms")
    
    print("\n3. COMPARAÇÃO DE PERFIS")
    
    comparacao = profiler_cpu.comparar_perfis([
        "Fibonacci Recursivo", "Fibonacci Iterativo"
    ])
    
    print("   Tempos totais:")
    for nome, tempo in comparacao['tempos_totais'].items():
        print(f"     {nome:20s}: {tempo:.4f}s")
    
    print("   Eficiência (tempo por chamada):")
    for nome, tempo in comparacao['eficiencia'].items():
        print(f"     {nome:20s}: {tempo*1000:.4f}ms")


def demonstrar_monitor_sistema():
    """Demonstra monitoramento de sistema."""
    print("\n=== DEMONSTRAÇÃO: MONITOR DE SISTEMA ===\n")
    
    monitor = MonitorSistema(intervalo=0.5)
    
    print("1. MONITORAMENTO DURANTE EXECUÇÃO")
    
    # Iniciar monitoramento
    monitor.iniciar_monitoramento()
    
    # Executar algumas operações custosas
    print("   Executando operações custosas...")
    
    # Operação CPU-intensiva
    def operacao_cpu():
        return sum(i**2 for i in range(100000))
    
    # Operação memória-intensiva
    def operacao_memoria():
        dados = []
        for i in range(10000):
            dados.append([j for j in range(100)])
        return len(dados)
    
    for i in range(5):
        print(f"   Iteração {i+1}/5")
        operacao_cpu()
        operacao_memoria()
        time.sleep(1)
    
    # Parar monitoramento
    monitor.parar_monitoramento()
    
    print("\n2. ESTATÍSTICAS DO MONITORAMENTO")
    
    stats = monitor.obter_estatisticas()
    
    for metrica, valores in stats.items():
        print(f"   {metrica.replace('_', ' ').title()}:")
        print(f"     Média: {valores['media']:.2f}")
        print(f"     Mín:   {valores['min']:.2f}")
        print(f"     Máx:   {valores['max']:.2f}")
        print(f"     Atual: {valores['atual']:.2f}")
        print()


def demonstrar_benchmark_suite():
    """Demonstra suite completa de benchmark."""
    print("\n=== DEMONSTRAÇÃO: BENCHMARK SUITE ===\n")
    
    suite = BenchmarkSuite()
    
    print("1. BENCHMARK COMPLETO DE ALGORITMO")
    
    # Dados de teste
    import random
    dados = [random.randint(1, 1000) for _ in range(1000)]
    
    # Benchmark do merge sort
    relatorio = suite.benchmark_completo(
        AlgoritmosBenchmark.ordenacao_merge, dados,
        nome="Merge Sort", num_execucoes=50
    )
    
    print(f"\nRelatório: {relatorio.nome}")
    print(f"Tempo médio: {relatorio.medicao_tempo.tempo_medio*1000:.2f}ms")
    print(f"Memória usada: {relatorio.medicao_memoria.memoria_usada/1024/1024:.2f}MB")
    print(f"Chamadas de função: {relatorio.perfil_cpu.num_chamadas}")
    
    print("\nRecomendações:")
    for rec in relatorio.recomendacoes:
        print(f"  - {rec}")
    
    print("\n2. COMPARAÇÃO DE IMPLEMENTAÇÕES")
    
    # Comparar algoritmos de ordenação
    implementacoes = {
        "Bubble Sort": AlgoritmosBenchmark.ordenacao_bubble,
        "Quick Sort": AlgoritmosBenchmark.ordenacao_quick,
        "Merge Sort": AlgoritmosBenchmark.ordenacao_merge,
        "Python Sort": lambda arr: sorted(arr)
    }
    
    # Usar dados menores para bubble sort não demorar muito
    dados_pequenos = [random.randint(1, 100) for _ in range(100)]
    
    relatorios = suite.comparar_implementacoes(
        implementacoes, args=(dados_pequenos,), num_execucoes=20
    )
    
    print("\n3. COMPARAÇÃO DE FIBONACCI")
    
    implementacoes_fib = {
        "Recursivo": AlgoritmosBenchmark.fibonacci_recursivo,
        "Iterativo": AlgoritmosBenchmark.fibonacci_iterativo,
        "Memoizado": AlgoritmosBenchmark.fibonacci_memoizado
    }
    
    relatorios_fib = suite.comparar_implementacoes(
        implementacoes_fib, args=(20,), num_execucoes=100
    )


def benchmark_estruturas_dados():
    """Benchmark de estruturas de dados."""
    print("\n=== BENCHMARK: ESTRUTURAS DE DADOS ===\n")
    
    profiler = ProfilerTempo()
    
    print("1. COMPARAÇÃO: LISTA vs DEQUE")
    
    # Operações em lista
    def operacoes_lista(n):
        lista = []
        # Inserções no início (custoso para lista)
        for i in range(n):
            lista.insert(0, i)
        # Remoções do início
        while lista:
            lista.pop(0)
    
    # Operações em deque
    def operacoes_deque(n):
        fila = deque()
        # Inserções no início (eficiente para deque)
        for i in range(n):
            fila.appendleft(i)
        # Remoções do início
        while fila:
            fila.popleft()
    
    tamanhos = [100, 500, 1000, 2000]
    
    print("   Inserções e remoções no início:")
    print("   Tamanho | Lista (ms) | Deque (ms) | Speedup")
    print("   --------|------------|------------|--------")
    
    for n in tamanhos:
        medicao_lista = profiler.medir_funcao(
            operacoes_lista, n, nome=f"lista_{n}", num_execucoes=10
        )
        
        medicao_deque = profiler.medir_funcao(
            operacoes_deque, n, nome=f"deque_{n}", num_execucoes=10
        )
        
        speedup = medicao_lista.tempo_medio / medicao_deque.tempo_medio
        
        print(f"   {n:7d} | {medicao_lista.tempo_medio*1000:10.2f} | "
              f"{medicao_deque.tempo_medio*1000:10.2f} | {speedup:7.1f}x")
    
    print("\n2. COMPARAÇÃO: DICT vs SET para LOOKUP")
    
    # Preparar dados
    dados = list(range(10000))
    dict_dados = {i: f"valor_{i}" for i in dados}
    set_dados = set(dados)
    
    def lookup_dict(dados_dict, chaves):
        return sum(1 for chave in chaves if chave in dados_dict)
    
    def lookup_set(dados_set, chaves):
        return sum(1 for chave in chaves if chave in dados_set)
    
    # Chaves para buscar
    chaves_busca = [i for i in range(0, 10000, 100)]  # 100 chaves
    
    medicao_dict = profiler.medir_funcao(
        lookup_dict, dict_dados, chaves_busca, 
        nome="dict_lookup", num_execucoes=1000
    )
    
    medicao_set = profiler.medir_funcao(
        lookup_set, set_dados, chaves_busca,
        nome="set_lookup", num_execucoes=1000
    )
    
    print(f"   Dict lookup: {medicao_dict.tempo_medio*1000000:.2f}μs")
    print(f"   Set lookup:  {medicao_set.tempo_medio*1000000:.2f}μs")
    print(f"   Diferença:   {abs(medicao_dict.tempo_medio - medicao_set.tempo_medio)*1000000:.2f}μs")


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 07.4 - PROFILING E PERFORMANCE")
    print("=" * 50)
    
    demonstrar_profiling_basico()
    demonstrar_profiling_cpu()
    demonstrar_monitor_sistema()
    demonstrar_benchmark_suite()
    benchmark_estruturas_dados()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 07.4")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. FERRAMENTAS DE PROFILING:
   • cProfile: profiling detalhado de CPU
   • memory_profiler: análise de uso de memória
   • timeit: medição precisa de tempo
   • psutil: monitoramento de recursos do sistema
   • tracemalloc: rastreamento de alocações

2. TIPOS DE ANÁLISE:
   • Profiling de CPU: identificar funções custosas
   • Profiling de memória: detectar vazamentos e uso excessivo
   • Profiling de linha: análise linha por linha
   • Monitoramento de sistema: recursos globais

3. MÉTRICAS IMPORTANTES:
   • Tempo de execução (médio, mín, máx, desvio)
   • Throughput (operações por segundo)
   • Uso de memória (atual, pico, vazamentos)
   • Número de chamadas de função
   • Eficiência por chamada

4. BENCHMARKING SISTEMÁTICO:
   • Aquecimento antes das medições
   • Múltiplas execuções para estatísticas
   • Controle de variáveis externas
   • Comparação relativa entre implementações
   • Análise de trade-offs

5. IDENTIFICAÇÃO DE GARGALOS:
   • Hotspots: funções que consomem mais tempo
   • Vazamentos de memória: crescimento contínuo
   • Overhead de chamadas: muitas chamadas pequenas
   • Ineficiências algorítmicas: complexidade desnecessária

6. OTIMIZAÇÃO BASEADA EM DADOS:
   • Medir antes de otimizar
   • Focar nos gargalos reais
   • Validar melhorias com benchmarks
   • Considerar trade-offs espaço-tempo
   • Monitorar regressões

7. FERRAMENTAS AVANÇADAS:
   • py-spy: profiling em produção sem overhead
   • line_profiler: análise linha por linha
   • memory_profiler: decoradores para funções
   • Jupyter %timeit: profiling interativo

8. BOAS PRÁTICAS:
   • Profile em ambiente similar à produção
   • Use dados realistas nos testes
   • Considere variabilidade nas medições
   • Documente configurações de teste
   • Automatize benchmarks críticos

9. MONITORAMENTO CONTÍNUO:
   • Integrar profiling no CI/CD
   • Alertas para regressões de performance
   • Dashboards de métricas
   • Profiling em produção quando necessário

10. INTERPRETAÇÃO DE RESULTADOS:
    • Estatísticas descritivas (média, desvio)
    • Comparações relativas (speedup, eficiência)
    • Análise de tendências
    • Correlação entre métricas
    • Impacto no usuário final

11. LIMITAÇÕES E CUIDADOS:
    • Overhead do profiling pode afetar medições
    • Variabilidade entre execuções
    • Diferenças entre ambientes
    • Micro-benchmarks vs performance real
    • Otimização prematura

12. APLICAÇÕES PRÁTICAS:
    • Otimização de algoritmos críticos
    • Identificação de vazamentos
    • Planejamento de capacidade
    • Análise de escalabilidade
    • Debugging de performance

O profiling é essencial para:
- Desenvolvimento de software eficiente
- Identificação proativa de problemas
- Otimização baseada em evidências
- Garantia de qualidade de performance
- Manutenção de sistemas em produção

Próximo: Módulo 07.5 - Otimização de Código
    """)


if __name__ == "__main__":
    main()