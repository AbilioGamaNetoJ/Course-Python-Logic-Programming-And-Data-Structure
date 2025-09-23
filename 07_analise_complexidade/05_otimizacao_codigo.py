"""
MÓDULO 07.5 - OTIMIZAÇÃO DE CÓDIGO
==================================

Objetivos de Aprendizado:
- Dominar técnicas de otimização de código Python
- Aplicar princípios de refatoração para performance
- Implementar padrões de otimização eficazes
- Usar ferramentas de análise estática
- Otimizar estruturas de dados e algoritmos
- Aplicar técnicas de cache e memoização
- Implementar lazy evaluation e generators
- Otimizar loops e operações custosas

Conceitos Abordados:
- Otimização algorítmica vs micro-otimização
- Profiling-driven optimization
- Refatoração para performance
- Padrões de otimização em Python
- Cache e memoização
- Lazy evaluation e generators
- Otimização de loops
- Uso eficiente de estruturas de dados
- Paralelização e concorrência
- Otimização de I/O

Técnicas Implementadas:
- Memoização e cache
- List comprehensions otimizadas
- Generator expressions
- Algoritmos in-place
- Pooling de objetos
- Lazy loading
- Batch processing
- Vectorização com NumPy

Pré-requisitos:
- Profiling e análise de performance
- Estruturas de dados avançadas
- Análise de complexidade
- Padrões de design
"""

import functools
import itertools
import operator
import time
import sys
import gc
import weakref
from typing import List, Dict, Any, Callable, Optional, Tuple, Iterator, Generator
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque, Counter
from abc import ABC, abstractmethod
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import numpy as np
import matplotlib.pyplot as plt


class TipoOtimizacao(Enum):
    """Tipos de otimização."""
    ALGORITMICA = "Algorítmica"
    ESTRUTURA_DADOS = "Estrutura de Dados"
    CACHE = "Cache/Memoização"
    LAZY = "Lazy Evaluation"
    PARALELIZACAO = "Paralelização"
    IO = "Input/Output"
    MEMORIA = "Memória"
    MICRO = "Micro-otimização"


@dataclass
class ResultadoOtimizacao:
    """Resultado de uma otimização."""
    nome: str
    tipo: TipoOtimizacao
    tempo_antes: float
    tempo_depois: float
    memoria_antes: int
    memoria_depois: int
    speedup: float = field(init=False)
    economia_memoria: float = field(init=False)
    
    def __post_init__(self):
        """Calcula métricas derivadas."""
        self.speedup = self.tempo_antes / self.tempo_depois if self.tempo_depois > 0 else 0
        self.economia_memoria = ((self.memoria_antes - self.memoria_depois) / 
                               self.memoria_antes * 100 if self.memoria_antes > 0 else 0)


class CacheInteligente:
    """
    Sistema de cache inteligente com diferentes estratégias.
    """
    
    def __init__(self, max_size: int = 128, strategy: str = "LRU"):
        """
        Inicializa cache inteligente.
        
        Args:
            max_size: Tamanho máximo do cache
            strategy: Estratégia de eviction (LRU, LFU, FIFO)
        """
        self.max_size = max_size
        self.strategy = strategy
        self.cache: Dict[Any, Any] = {}
        self.access_order: deque = deque()  # Para LRU
        self.access_count: Counter = Counter()  # Para LFU
        self.insertion_order: deque = deque()  # Para FIFO
        self.hits = 0
        self.misses = 0
    
    def get(self, key: Any) -> Any:
        """
        Obtém valor do cache.
        
        Args:
            key: Chave do cache
        
        Returns:
            Valor ou None se não encontrado
        """
        if key in self.cache:
            self.hits += 1
            self._update_access(key)
            return self.cache[key]
        else:
            self.misses += 1
            return None
    
    def put(self, key: Any, value: Any):
        """
        Adiciona valor ao cache.
        
        Args:
            key: Chave
            value: Valor
        """
        if key in self.cache:
            self.cache[key] = value
            self._update_access(key)
        else:
            if len(self.cache) >= self.max_size:
                self._evict()
            
            self.cache[key] = value
            self.access_order.append(key)
            self.insertion_order.append(key)
            self.access_count[key] = 1
    
    def _update_access(self, key: Any):
        """Atualiza informações de acesso."""
        if self.strategy == "LRU":
            self.access_order.remove(key)
            self.access_order.append(key)
        elif self.strategy == "LFU":
            self.access_count[key] += 1
    
    def _evict(self):
        """Remove item do cache baseado na estratégia."""
        if self.strategy == "LRU":
            key_to_remove = self.access_order.popleft()
        elif self.strategy == "LFU":
            key_to_remove = self.access_count.most_common()[-1][0]
            del self.access_count[key_to_remove]
        elif self.strategy == "FIFO":
            key_to_remove = self.insertion_order.popleft()
        
        del self.cache[key_to_remove]
    
    @property
    def hit_rate(self) -> float:
        """Taxa de acerto do cache."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0
    
    def clear(self):
        """Limpa o cache."""
        self.cache.clear()
        self.access_order.clear()
        self.access_count.clear()
        self.insertion_order.clear()
        self.hits = 0
        self.misses = 0


class MemoizacaoAvancada:
    """
    Sistema avançado de memoização com TTL e limpeza automática.
    """
    
    def __init__(self, ttl: float = None, max_size: int = None):
        """
        Inicializa memoização avançada.
        
        Args:
            ttl: Time-to-live em segundos
            max_size: Tamanho máximo do cache
        """
        self.ttl = ttl
        self.max_size = max_size
        self.cache: Dict[Any, Tuple[Any, float]] = {}
        self.access_times: Dict[Any, float] = {}
    
    def __call__(self, func: Callable) -> Callable:
        """
        Decorador de memoização.
        
        Args:
            func: Função a ser memoizada
        
        Returns:
            Função memoizada
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Criar chave única
            key = self._make_key(args, kwargs)
            
            # Verificar se está no cache e não expirou
            if key in self.cache:
                value, timestamp = self.cache[key]
                if self.ttl is None or time.time() - timestamp < self.ttl:
                    self.access_times[key] = time.time()
                    return value
                else:
                    # Expirou, remover
                    del self.cache[key]
                    del self.access_times[key]
            
            # Calcular valor
            result = func(*args, **kwargs)
            
            # Adicionar ao cache
            current_time = time.time()
            self.cache[key] = (result, current_time)
            self.access_times[key] = current_time
            
            # Limpar cache se necessário
            self._cleanup()
            
            return result
        
        wrapper.cache_info = lambda: {
            'size': len(self.cache),
            'max_size': self.max_size,
            'ttl': self.ttl
        }
        wrapper.cache_clear = lambda: self._clear()
        
        return wrapper
    
    def _make_key(self, args: tuple, kwargs: dict) -> tuple:
        """Cria chave única para argumentos."""
        key = args
        if kwargs:
            key += tuple(sorted(kwargs.items()))
        return key
    
    def _cleanup(self):
        """Limpa cache baseado em tamanho e TTL."""
        current_time = time.time()
        
        # Remover itens expirados
        if self.ttl is not None:
            expired_keys = [
                key for key, (_, timestamp) in self.cache.items()
                if current_time - timestamp >= self.ttl
            ]
            for key in expired_keys:
                del self.cache[key]
                del self.access_times[key]
        
        # Remover itens mais antigos se exceder tamanho
        if self.max_size is not None and len(self.cache) > self.max_size:
            # Ordenar por tempo de acesso
            sorted_keys = sorted(
                self.access_times.keys(),
                key=lambda k: self.access_times[k]
            )
            
            # Remover os mais antigos
            keys_to_remove = sorted_keys[:len(self.cache) - self.max_size]
            for key in keys_to_remove:
                del self.cache[key]
                del self.access_times[key]
    
    def _clear(self):
        """Limpa todo o cache."""
        self.cache.clear()
        self.access_times.clear()


class LazyEvaluator:
    """
    Sistema de avaliação lazy para computações custosas.
    """
    
    def __init__(self):
        """Inicializa avaliador lazy."""
        self.computed_values: Dict[str, Any] = {}
        self.computations: Dict[str, Callable] = {}
    
    def lazy_property(self, name: str, computation: Callable):
        """
        Define propriedade lazy.
        
        Args:
            name: Nome da propriedade
            computation: Função de computação
        """
        self.computations[name] = computation
    
    def get(self, name: str) -> Any:
        """
        Obtém valor lazy.
        
        Args:
            name: Nome da propriedade
        
        Returns:
            Valor computado
        """
        if name not in self.computed_values:
            if name in self.computations:
                self.computed_values[name] = self.computations[name]()
            else:
                raise KeyError(f"Propriedade lazy '{name}' não definida")
        
        return self.computed_values[name]
    
    def invalidate(self, name: str):
        """
        Invalida valor lazy.
        
        Args:
            name: Nome da propriedade
        """
        if name in self.computed_values:
            del self.computed_values[name]
    
    def invalidate_all(self):
        """Invalida todos os valores lazy."""
        self.computed_values.clear()


class ObjectPool:
    """
    Pool de objetos para reutilização e redução de overhead.
    """
    
    def __init__(self, factory: Callable, max_size: int = 100):
        """
        Inicializa pool de objetos.
        
        Args:
            factory: Função para criar novos objetos
            max_size: Tamanho máximo do pool
        """
        self.factory = factory
        self.max_size = max_size
        self.pool: deque = deque()
        self.created_count = 0
        self.reused_count = 0
    
    def acquire(self) -> Any:
        """
        Adquire objeto do pool.
        
        Returns:
            Objeto do pool ou novo objeto
        """
        if self.pool:
            self.reused_count += 1
            return self.pool.popleft()
        else:
            self.created_count += 1
            return self.factory()
    
    def release(self, obj: Any):
        """
        Retorna objeto ao pool.
        
        Args:
            obj: Objeto a ser retornado
        """
        if len(self.pool) < self.max_size:
            # Reset do objeto se necessário
            if hasattr(obj, 'reset'):
                obj.reset()
            self.pool.append(obj)
    
    @property
    def reuse_rate(self) -> float:
        """Taxa de reutilização."""
        total = self.created_count + self.reused_count
        return self.reused_count / total if total > 0 else 0
    
    def stats(self) -> Dict[str, Any]:
        """Estatísticas do pool."""
        return {
            'pool_size': len(self.pool),
            'max_size': self.max_size,
            'created': self.created_count,
            'reused': self.reused_count,
            'reuse_rate': self.reuse_rate
        }


class BatchProcessor:
    """
    Processador em lotes para otimizar operações custosas.
    """
    
    def __init__(self, batch_size: int = 100, flush_interval: float = 1.0):
        """
        Inicializa processador em lotes.
        
        Args:
            batch_size: Tamanho do lote
            flush_interval: Intervalo de flush em segundos
        """
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.batch: List[Any] = []
        self.last_flush = time.time()
        self.processor: Optional[Callable] = None
        self.processed_count = 0
    
    def set_processor(self, processor: Callable):
        """
        Define função de processamento.
        
        Args:
            processor: Função que processa um lote
        """
        self.processor = processor
    
    def add(self, item: Any):
        """
        Adiciona item ao lote.
        
        Args:
            item: Item a ser processado
        """
        self.batch.append(item)
        
        # Verificar se deve processar
        if (len(self.batch) >= self.batch_size or 
            time.time() - self.last_flush >= self.flush_interval):
            self.flush()
    
    def flush(self):
        """Processa lote atual."""
        if self.batch and self.processor:
            self.processor(self.batch.copy())
            self.processed_count += len(self.batch)
            self.batch.clear()
            self.last_flush = time.time()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.flush()


class OptimizadorAlgoritmos:
    """
    Otimizador de algoritmos com diferentes estratégias.
    """
    
    @staticmethod
    def otimizar_busca_sequencial(dados: List[Any], 
                                 frequencias: Dict[Any, int] = None) -> List[Any]:
        """
        Otimiza busca sequencial ordenando por frequência.
        
        Args:
            dados: Lista de dados
            frequencias: Frequências de acesso
        
        Returns:
            Lista otimizada
        """
        if frequencias is None:
            return dados
        
        # Ordenar por frequência decrescente
        return sorted(dados, key=lambda x: frequencias.get(x, 0), reverse=True)
    
    @staticmethod
    def otimizar_loops_aninhados(matriz: List[List[int]]) -> List[List[int]]:
        """
        Otimiza loops aninhados usando cache-friendly access.
        
        Args:
            matriz: Matriz a ser processada
        
        Returns:
            Matriz processada
        """
        if not matriz or not matriz[0]:
            return matriz
        
        linhas, colunas = len(matriz), len(matriz[0])
        resultado = [[0] * colunas for _ in range(linhas)]
        
        # Acesso cache-friendly (por linha)
        for i in range(linhas):
            for j in range(colunas):
                resultado[i][j] = matriz[i][j] * 2
        
        return resultado
    
    @staticmethod
    def otimizar_agregacao(dados: List[Dict[str, Any]], 
                          chave_grupo: str, 
                          chave_valor: str) -> Dict[Any, float]:
        """
        Otimiza agregação usando defaultdict.
        
        Args:
            dados: Lista de dicionários
            chave_grupo: Chave para agrupamento
            chave_valor: Chave para valor
        
        Returns:
            Dicionário agregado
        """
        agregacao = defaultdict(float)
        
        for item in dados:
            grupo = item.get(chave_grupo)
            valor = item.get(chave_valor, 0)
            agregacao[grupo] += valor
        
        return dict(agregacao)
    
    @staticmethod
    def otimizar_filtros_multiplos(dados: List[Any], 
                                  filtros: List[Callable]) -> List[Any]:
        """
        Otimiza múltiplos filtros combinando-os.
        
        Args:
            dados: Lista de dados
            filtros: Lista de funções de filtro
        
        Returns:
            Lista filtrada
        """
        # Combinar filtros em uma única função
        def filtro_combinado(item):
            return all(filtro(item) for filtro in filtros)
        
        return [item for item in dados if filtro_combinado(item)]
    
    @staticmethod
    def otimizar_ordenacao_parcial(dados: List[Any], k: int) -> List[Any]:
        """
        Otimiza ordenação quando só precisamos dos k menores.
        
        Args:
            dados: Lista de dados
            k: Número de elementos desejados
        
        Returns:
            K menores elementos
        """
        import heapq
        return heapq.nsmallest(k, dados)


class OptimizadorEstruturasD dados:
    """
    Otimizador de estruturas de dados.
    """
    
    @staticmethod
    def otimizar_lookup_frequente(dados: List[Any]) -> set:
        """
        Converte lista para set para lookup O(1).
        
        Args:
            dados: Lista de dados
        
        Returns:
            Set otimizado
        """
        return set(dados)
    
    @staticmethod
    def otimizar_contagem(dados: List[Any]) -> Counter:
        """
        Usa Counter para contagem eficiente.
        
        Args:
            dados: Lista de dados
        
        Returns:
            Counter otimizado
        """
        return Counter(dados)
    
    @staticmethod
    def otimizar_agrupamento(dados: List[Tuple[Any, Any]]) -> Dict[Any, List[Any]]:
        """
        Agrupa dados usando defaultdict.
        
        Args:
            dados: Lista de tuplas (chave, valor)
        
        Returns:
            Dicionário agrupado
        """
        grupos = defaultdict(list)
        for chave, valor in dados:
            grupos[chave].append(valor)
        return dict(grupos)
    
    @staticmethod
    def otimizar_fila_prioridade(dados: List[Tuple[int, Any]]) -> List[Any]:
        """
        Usa heapq para fila de prioridade eficiente.
        
        Args:
            dados: Lista de tuplas (prioridade, item)
        
        Returns:
            Lista ordenada por prioridade
        """
        import heapq
        heap = dados.copy()
        heapq.heapify(heap)
        
        resultado = []
        while heap:
            prioridade, item = heapq.heappop(heap)
            resultado.append(item)
        
        return resultado


class ParalelizadorTarefas:
    """
    Paralelizador de tarefas para otimização de performance.
    """
    
    def __init__(self, max_workers: int = None):
        """
        Inicializa paralelizador.
        
        Args:
            max_workers: Número máximo de workers
        """
        self.max_workers = max_workers or multiprocessing.cpu_count()
    
    def processar_paralelo_threads(self, func: Callable, dados: List[Any]) -> List[Any]:
        """
        Processa dados em paralelo usando threads (I/O bound).
        
        Args:
            func: Função a ser aplicada
            dados: Lista de dados
        
        Returns:
            Lista de resultados
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            return list(executor.map(func, dados))
    
    def processar_paralelo_processos(self, func: Callable, dados: List[Any]) -> List[Any]:
        """
        Processa dados em paralelo usando processos (CPU bound).
        
        Args:
            func: Função a ser aplicada
            dados: Lista de dados
        
        Returns:
            Lista de resultados
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            return list(executor.map(func, dados))
    
    def processar_lotes_paralelo(self, func: Callable, dados: List[Any], 
                               tamanho_lote: int = None) -> List[Any]:
        """
        Processa dados em lotes paralelos.
        
        Args:
            func: Função a ser aplicada ao lote
            dados: Lista de dados
            tamanho_lote: Tamanho do lote
        
        Returns:
            Lista de resultados
        """
        if tamanho_lote is None:
            tamanho_lote = len(dados) // self.max_workers
        
        # Dividir em lotes
        lotes = [dados[i:i + tamanho_lote] 
                for i in range(0, len(dados), tamanho_lote)]
        
        # Processar lotes em paralelo
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            resultados_lotes = list(executor.map(func, lotes))
        
        # Combinar resultados
        resultado_final = []
        for resultado_lote in resultados_lotes:
            if isinstance(resultado_lote, list):
                resultado_final.extend(resultado_lote)
            else:
                resultado_final.append(resultado_lote)
        
        return resultado_final


class AnalisadorOtimizacao:
    """
    Analisador de oportunidades de otimização.
    """
    
    def __init__(self):
        """Inicializa analisador."""
        self.otimizacoes: List[ResultadoOtimizacao] = []
    
    def analisar_funcao(self, func_original: Callable, func_otimizada: Callable,
                      args: tuple = (), kwargs: dict = None, 
                      num_execucoes: int = 100) -> ResultadoOtimizacao:
        """
        Analisa otimização de uma função.
        
        Args:
            func_original: Função original
            func_otimizada: Função otimizada
            args: Argumentos para teste
            kwargs: Argumentos nomeados
            num_execucoes: Número de execuções
        
        Returns:
            Resultado da análise
        """
        kwargs = kwargs or {}
        
        # Medir função original
        tempo_antes, memoria_antes = self._medir_funcao(
            func_original, args, kwargs, num_execucoes
        )
        
        # Medir função otimizada
        tempo_depois, memoria_depois = self._medir_funcao(
            func_otimizada, args, kwargs, num_execucoes
        )
        
        resultado = ResultadoOtimizacao(
            nome=f"{func_original.__name__} -> {func_otimizada.__name__}",
            tipo=TipoOtimizacao.ALGORITMICA,
            tempo_antes=tempo_antes,
            tempo_depois=tempo_depois,
            memoria_antes=memoria_antes,
            memoria_depois=memoria_depois
        )
        
        self.otimizacoes.append(resultado)
        return resultado
    
    def _medir_funcao(self, func: Callable, args: tuple, kwargs: dict, 
                     num_execucoes: int) -> Tuple[float, int]:
        """
        Mede tempo e memória de uma função.
        
        Args:
            func: Função a medir
            args: Argumentos
            kwargs: Argumentos nomeados
            num_execucoes: Número de execuções
        
        Returns:
            Tupla (tempo_medio, memoria_usada)
        """
        import psutil
        import tracemalloc
        
        # Medir memória
        tracemalloc.start()
        processo = psutil.Process()
        memoria_inicial = processo.memory_info().rss
        
        # Medir tempo
        tempos = []
        for _ in range(num_execucoes):
            inicio = time.perf_counter()
            func(*args, **kwargs)
            fim = time.perf_counter()
            tempos.append(fim - inicio)
        
        # Calcular médias
        tempo_medio = sum(tempos) / len(tempos)
        
        memoria_final = processo.memory_info().rss
        memoria_usada = memoria_final - memoria_inicial
        
        tracemalloc.stop()
        
        return tempo_medio, memoria_usada
    
    def gerar_relatorio(self) -> str:
        """
        Gera relatório de otimizações.
        
        Returns:
            Relatório formatado
        """
        if not self.otimizacoes:
            return "Nenhuma otimização analisada."
        
        relatorio = ["RELATÓRIO DE OTIMIZAÇÕES", "=" * 50, ""]
        
        for i, opt in enumerate(self.otimizacoes, 1):
            relatorio.extend([
                f"{i}. {opt.nome}",
                f"   Tipo: {opt.tipo.value}",
                f"   Speedup: {opt.speedup:.2f}x",
                f"   Economia de memória: {opt.economia_memoria:.1f}%",
                f"   Tempo antes: {opt.tempo_antes*1000:.2f}ms",
                f"   Tempo depois: {opt.tempo_depois*1000:.2f}ms",
                ""
            ])
        
        # Estatísticas gerais
        speedups = [opt.speedup for opt in self.otimizacoes]
        speedup_medio = sum(speedups) / len(speedups)
        melhor_speedup = max(speedups)
        
        relatorio.extend([
            "ESTATÍSTICAS GERAIS:",
            f"Speedup médio: {speedup_medio:.2f}x",
            f"Melhor speedup: {melhor_speedup:.2f}x",
            f"Total de otimizações: {len(self.otimizacoes)}"
        ])
        
        return "\n".join(relatorio)


# Exemplos de Otimizações
class ExemplosOtimizacao:
    """
    Exemplos práticos de otimização.
    """
    
    @staticmethod
    def exemplo_memoizacao():
        """Exemplo de otimização com memoização."""
        print("=== EXEMPLO: MEMOIZAÇÃO ===\n")
        
        # Função original (ineficiente)
        def fibonacci_lento(n):
            if n <= 1:
                return n
            return fibonacci_lento(n-1) + fibonacci_lento(n-2)
        
        # Função otimizada com memoização
        @MemoizacaoAvancada(ttl=60, max_size=100)
        def fibonacci_rapido(n):
            if n <= 1:
                return n
            return fibonacci_rapido(n-1) + fibonacci_rapido(n-2)
        
        # Testar performance
        n = 30
        
        print(f"Calculando fibonacci({n})...")
        
        # Versão lenta
        inicio = time.perf_counter()
        resultado_lento = fibonacci_lento(n)
        tempo_lento = time.perf_counter() - inicio
        
        # Versão rápida
        inicio = time.perf_counter()
        resultado_rapido = fibonacci_rapido(n)
        tempo_rapido = time.perf_counter() - inicio
        
        print(f"Resultado: {resultado_lento} (ambas versões)")
        print(f"Tempo sem memoização: {tempo_lento:.4f}s")
        print(f"Tempo com memoização: {tempo_rapido:.4f}s")
        print(f"Speedup: {tempo_lento/tempo_rapido:.1f}x")
        
        # Informações do cache
        cache_info = fibonacci_rapido.cache_info()
        print(f"Cache size: {cache_info['size']}")
    
    @staticmethod
    def exemplo_generators():
        """Exemplo de otimização com generators."""
        print("\n=== EXEMPLO: GENERATORS ===\n")
        
        # Função que retorna lista (usa muita memória)
        def processar_lista(n):
            return [i**2 for i in range(n)]
        
        # Função que retorna generator (usa pouca memória)
        def processar_generator(n):
            return (i**2 for i in range(n))
        
        # Testar uso de memória
        import sys
        
        n = 100000
        
        # Lista
        lista = processar_lista(n)
        memoria_lista = sys.getsizeof(lista)
        
        # Generator
        gen = processar_generator(n)
        memoria_gen = sys.getsizeof(gen)
        
        print(f"Processando {n} elementos:")
        print(f"Memória da lista: {memoria_lista/1024:.1f}KB")
        print(f"Memória do generator: {memoria_gen} bytes")
        print(f"Economia: {(memoria_lista - memoria_gen)/memoria_lista*100:.1f}%")
        
        # Testar consumo
        print("\nConsumindo primeiros 5 elementos:")
        gen = processar_generator(n)  # Recriar generator
        primeiros_5 = [next(gen) for _ in range(5)]
        print(f"Primeiros 5: {primeiros_5}")
    
    @staticmethod
    def exemplo_list_comprehensions():
        """Exemplo de otimização com list comprehensions."""
        print("\n=== EXEMPLO: LIST COMPREHENSIONS ===\n")
        
        dados = list(range(100000))
        
        # Versão com loop tradicional
        def filtrar_loop(dados):
            resultado = []
            for x in dados:
                if x % 2 == 0:
                    resultado.append(x**2)
            return resultado
        
        # Versão com list comprehension
        def filtrar_comprehension(dados):
            return [x**2 for x in dados if x % 2 == 0]
        
        # Versão com filter e map
        def filtrar_funcional(dados):
            return list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, dados)))
        
        # Testar performance
        import timeit
        
        tempo_loop = timeit.timeit(
            lambda: filtrar_loop(dados), number=10
        ) / 10
        
        tempo_comp = timeit.timeit(
            lambda: filtrar_comprehension(dados), number=10
        ) / 10
        
        tempo_func = timeit.timeit(
            lambda: filtrar_funcional(dados), number=10
        ) / 10
        
        print(f"Filtrando e transformando {len(dados)} elementos:")
        print(f"Loop tradicional: {tempo_loop*1000:.2f}ms")
        print(f"List comprehension: {tempo_comp*1000:.2f}ms")
        print(f"Filter + map: {tempo_func*1000:.2f}ms")
        
        print(f"\nSpeedup comprehension: {tempo_loop/tempo_comp:.1f}x")
        print(f"Speedup funcional: {tempo_loop/tempo_func:.1f}x")
    
    @staticmethod
    def exemplo_object_pooling():
        """Exemplo de otimização com object pooling."""
        print("\n=== EXEMPLO: OBJECT POOLING ===\n")
        
        class ExpensiveObject:
            """Objeto custoso de criar."""
            def __init__(self):
                # Simular criação custosa
                time.sleep(0.001)
                self.data = [0] * 1000
            
            def reset(self):
                """Reset do objeto para reutilização."""
                self.data = [0] * 1000
            
            def process(self, value):
                """Processa um valor."""
                return sum(self.data) + value
        
        # Sem pooling
        def sem_pooling(valores):
            resultados = []
            for valor in valores:
                obj = ExpensiveObject()
                resultado = obj.process(valor)
                resultados.append(resultado)
            return resultados
        
        # Com pooling
        def com_pooling(valores):
            pool = ObjectPool(ExpensiveObject, max_size=10)
            resultados = []
            
            for valor in valores:
                obj = pool.acquire()
                resultado = obj.process(valor)
                resultados.append(resultado)
                pool.release(obj)
            
            return resultados, pool
        
        # Testar performance
        valores = list(range(50))
        
        # Sem pooling
        inicio = time.perf_counter()
        resultado1 = sem_pooling(valores)
        tempo_sem = time.perf_counter() - inicio
        
        # Com pooling
        inicio = time.perf_counter()
        resultado2, pool = com_pooling(valores)
        tempo_com = time.perf_counter() - inicio
        
        print(f"Processando {len(valores)} valores:")
        print(f"Sem pooling: {tempo_sem:.3f}s")
        print(f"Com pooling: {tempo_com:.3f}s")
        print(f"Speedup: {tempo_sem/tempo_com:.1f}x")
        
        # Estatísticas do pool
        stats = pool.stats()
        print(f"\nEstatísticas do pool:")
        print(f"Objetos criados: {stats['created']}")
        print(f"Objetos reutilizados: {stats['reused']}")
        print(f"Taxa de reutilização: {stats['reuse_rate']*100:.1f}%")
    
    @staticmethod
    def exemplo_paralelizacao():
        """Exemplo de otimização com paralelização."""
        print("\n=== EXEMPLO: PARALELIZAÇÃO ===\n")
        
        def operacao_custosa(n):
            """Operação CPU-intensiva."""
            return sum(i**2 for i in range(n))
        
        # Dados para processar
        dados = [10000] * 8  # 8 operações custosas
        
        # Processamento sequencial
        inicio = time.perf_counter()
        resultado_seq = [operacao_custosa(n) for n in dados]
        tempo_seq = time.perf_counter() - inicio
        
        # Processamento paralelo
        paralelizador = ParalelizadorTarefas()
        
        inicio = time.perf_counter()
        resultado_par = paralelizador.processar_paralelo_processos(
            operacao_custosa, dados
        )
        tempo_par = time.perf_counter() - inicio
        
        print(f"Processando {len(dados)} operações custosas:")
        print(f"Sequencial: {tempo_seq:.3f}s")
        print(f"Paralelo: {tempo_par:.3f}s")
        print(f"Speedup: {tempo_seq/tempo_par:.1f}x")
        print(f"Eficiência: {(tempo_seq/tempo_par)/paralelizador.max_workers*100:.1f}%")
        
        # Verificar resultados
        print(f"Resultados iguais: {resultado_seq == resultado_par}")


def demonstrar_cache_inteligente():
    """Demonstra sistema de cache inteligente."""
    print("=== DEMONSTRAÇÃO: CACHE INTELIGENTE ===\n")
    
    # Testar diferentes estratégias
    estrategias = ["LRU", "LFU", "FIFO"]
    
    for estrategia in estrategias:
        print(f"Testando estratégia {estrategia}:")
        
        cache = CacheInteligente(max_size=5, strategy=estrategia)
        
        # Adicionar itens
        for i in range(10):
            cache.put(f"key_{i}", f"value_{i}")
        
        # Acessar alguns itens múltiplas vezes
        for _ in range(3):
            cache.get("key_1")
            cache.get("key_3")
            cache.get("key_5")
        
        # Verificar o que está no cache
        print(f"  Itens no cache: {list(cache.cache.keys())}")
        print(f"  Hit rate: {cache.hit_rate:.2f}")
        print()


def demonstrar_batch_processing():
    """Demonstra processamento em lotes."""
    print("=== DEMONSTRAÇÃO: BATCH PROCESSING ===\n")
    
    # Simulador de processamento custoso
    def processar_lote(itens):
        print(f"Processando lote de {len(itens)} itens")
        # Simular processamento
        time.sleep(0.1)
    
    # Usar batch processor
    with BatchProcessor(batch_size=5, flush_interval=2.0) as processor:
        processor.set_processor(processar_lote)
        
        print("Adicionando itens ao processador...")
        
        # Adicionar itens um por um
        for i in range(12):
            processor.add(f"item_{i}")
            time.sleep(0.3)  # Simular chegada de itens
        
        print(f"Total processado: {processor.processed_count} itens")


def benchmark_otimizacoes():
    """Benchmark de diferentes otimizações."""
    print("\n=== BENCHMARK: OTIMIZAÇÕES ===\n")
    
    analisador = AnalisadorOtimizacao()
    
    # 1. Busca em lista vs set
    dados_busca = list(range(10000))
    set_busca = set(dados_busca)
    
    def buscar_lista(item):
        return item in dados_busca
    
    def buscar_set(item):
        return item in set_busca
    
    resultado1 = analisador.analisar_funcao(
        buscar_lista, buscar_set, args=(5000,), num_execucoes=1000
    )
    resultado1.tipo = TipoOtimizacao.ESTRUTURA_DADOS
    
    # 2. Loop vs list comprehension
    dados_transform = list(range(1000))
    
    def transform_loop(dados):
        resultado = []
        for x in dados:
            if x % 2 == 0:
                resultado.append(x**2)
        return resultado
    
    def transform_comprehension(dados):
        return [x**2 for x in dados if x % 2 == 0]
    
    resultado2 = analisador.analisar_funcao(
        transform_loop, transform_comprehension, 
        args=(dados_transform,), num_execucoes=1000
    )
    resultado2.tipo = TipoOtimizacao.ALGORITMICA
    
    # 3. Concatenação de strings
    palavras = ["palavra"] * 1000
    
    def concat_tradicional(palavras):
        resultado = ""
        for palavra in palavras:
            resultado += palavra
        return resultado
    
    def concat_join(palavras):
        return "".join(palavras)
    
    resultado3 = analisador.analisar_funcao(
        concat_tradicional, concat_join,
        args=(palavras,), num_execucoes=100
    )
    resultado3.tipo = TipoOtimizacao.ALGORITMICA
    
    # Gerar relatório
    print(analisador.gerar_relatorio())


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 07.5 - OTIMIZAÇÃO DE CÓDIGO")
    print("=" * 50)
    
    # Executar exemplos
    ExemplosOtimizacao.exemplo_memoizacao()
    ExemplosOtimizacao.exemplo_generators()
    ExemplosOtimizacao.exemplo_list_comprehensions()
    ExemplosOtimizacao.exemplo_object_pooling()
    ExemplosOtimizacao.exemplo_paralelizacao()
    
    # Demonstrações adicionais
    demonstrar_cache_inteligente()
    demonstrar_batch_processing()
    benchmark_otimizacoes()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 07.5")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. PRINCÍPIOS DE OTIMIZAÇÃO:
   • Measure first, optimize second
   • Foque nos gargalos reais
   • Considere trade-offs espaço-tempo
   • Mantenha legibilidade do código
   • Valide melhorias com benchmarks

2. TÉCNICAS DE CACHE:
   • Memoização para funções puras
   • Cache inteligente com TTL
   • Diferentes estratégias de eviction (LRU, LFU, FIFO)
   • Cache hit rate como métrica
   • Invalidação seletiva

3. LAZY EVALUATION:
   • Computação sob demanda
   • Generators para economia de memória
   • Lazy properties para objetos
   • Streaming de dados grandes
   • Pipeline de transformações

4. OTIMIZAÇÃO DE ESTRUTURAS:
   • Set para lookup O(1)
   • Counter para contagem eficiente
   • defaultdict para agrupamento
   • heapq para filas de prioridade
   • deque para operações nas extremidades

5. OTIMIZAÇÃO ALGORÍTMICA:
   • Escolha do algoritmo correto
   • Redução de complexidade
   • Algoritmos in-place
   • Ordenação parcial quando possível
   • Filtros combinados

6. PARALELIZAÇÃO:
   • Threads para I/O bound
   • Processos para CPU bound
   • Processamento em lotes
   • Pool de workers
   • Overhead vs benefício

7. OBJECT POOLING:
   • Reutilização de objetos custosos
   • Redução de garbage collection
   • Pool sizing adequado
   • Reset de objetos
   • Métricas de reutilização

8. BATCH PROCESSING:
   • Agrupamento de operações
   • Redução de overhead
   • Flush automático
   • Processamento assíncrono
   • Balanceamento de latência vs throughput

9. MICRO-OTIMIZAÇÕES:
   • List comprehensions vs loops
   • join() vs concatenação
   • Acesso cache-friendly
   • Evitar lookups desnecessários
   • Reutilização de cálculos

10. PROFILING-DRIVEN OPTIMIZATION:
    • Identificar hotspots reais
    • Medir antes e depois
    • Análise de speedup
    • Monitoramento contínuo
    • Regressão de performance

11. FERRAMENTAS E MÉTRICAS:
    • Tempo de execução
    • Uso de memória
    • Throughput
    • Latência
    • Taxa de cache hit

12. BOAS PRÁTICAS:
    • Otimize baseado em dados
    • Mantenha código legível
    • Documente otimizações
    • Teste edge cases
    • Considere manutenibilidade

13. ANTI-PADRÕES:
    • Otimização prematura
    • Micro-otimizações desnecessárias
    • Complexidade excessiva
    • Ignorar profiling
    • Otimizar código não-crítico

14. ESTRATÉGIAS AVANÇADAS:
    • Vectorização com NumPy
    • JIT compilation (Numba)
    • Cython para código crítico
    • Algoritmos aproximados
    • Trade-offs precisão vs velocidade

A otimização eficaz requer:
- Compreensão profunda do problema
- Medição sistemática
- Foco nos gargalos reais
- Balanceamento de trade-offs
- Validação contínua

Conclusão do Módulo 07 - Análise de Complexidade:
Dominamos análise assintótica, complexidade amortizada, 
profiling, e técnicas avançadas de otimização.

Próximo: Módulo 08 - Projetos Práticos
    """)


if __name__ == "__main__":
    main()