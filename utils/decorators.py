"""
Decorators - Decoradores Úteis para o Curso

Este módulo contém decoradores que facilitam a análise de performance,
logging, cache e outras funcionalidades transversais utilizadas em
todo o curso de Lógica de Programação e Estruturas de Dados.

Tipos de decoradores:
1. Performance (timing, contagem de operações, profiling)
2. Cache (memoização, LRU cache)
3. Logging (execução, erros, debug)
4. Validação (tipos, parâmetros)
5. Retry (tentativas automáticas)
6. Benchmark (comparação de algoritmos)

Autor: Professor de Lógica de Programação
Data: 2024
"""

import time
import functools
import logging
import traceback
import gc
import sys
from typing import Any, Callable, Dict, List, Optional, Union, Tuple
from collections import OrderedDict, defaultdict
from threading import Lock
import warnings


# ============================================================================
# DECORADORES DE PERFORMANCE
# ============================================================================

def medir_tempo(unidade: str = 'auto', precisao: int = 4, exibir: bool = True):
    """
    Decorator que mede o tempo de execução de uma função.
    
    Args:
        unidade: Unidade de tempo ('s', 'ms', 'μs', 'ns', 'auto')
        precisao: Número de casas decimais
        exibir: Se deve exibir o resultado automaticamente
        
    Returns:
        Decorator que adiciona medição de tempo
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            inicio = time.perf_counter()
            
            try:
                resultado = func(*args, **kwargs)
                sucesso = True
            except Exception as e:
                resultado = e
                sucesso = False
            
            fim = time.perf_counter()
            tempo_execucao = fim - inicio
            
            # Formatar tempo baseado na unidade
            if unidade == 'auto':
                if tempo_execucao >= 1:
                    tempo_formatado = f"{tempo_execucao:.{precisao}f}s"
                elif tempo_execucao >= 0.001:
                    tempo_formatado = f"{tempo_execucao * 1000:.{precisao}f}ms"
                elif tempo_execucao >= 0.000001:
                    tempo_formatado = f"{tempo_execucao * 1000000:.{precisao}f}μs"
                else:
                    tempo_formatado = f"{tempo_execucao * 1000000000:.{precisao}f}ns"
            else:
                conversoes = {'s': 1, 'ms': 1000, 'μs': 1000000, 'ns': 1000000000}
                fator = conversoes.get(unidade, 1)
                tempo_formatado = f"{tempo_execucao * fator:.{precisao}f}{unidade}"
            
            if exibir:
                status = "✓" if sucesso else "✗"
                print(f"{status} {func.__name__}: {tempo_formatado}")
            
            # Adicionar tempo como atributo do resultado
            if sucesso:
                if hasattr(resultado, '__dict__'):
                    resultado._tempo_execucao = tempo_execucao
                else:
                    # Para tipos imutáveis, retornar tupla
                    return resultado, tempo_execucao
            
            if not sucesso:
                raise resultado
                
            return resultado
        
        # Adicionar método para obter estatísticas
        wrapper._tempos_execucao = []
        
        def obter_estatisticas():
            if not wrapper._tempos_execucao:
                return None
            
            tempos = wrapper._tempos_execucao
            return {
                'total_execucoes': len(tempos),
                'tempo_total': sum(tempos),
                'tempo_medio': sum(tempos) / len(tempos),
                'tempo_min': min(tempos),
                'tempo_max': max(tempos)
            }
        
        wrapper.obter_estatisticas = obter_estatisticas
        return wrapper
    
    return decorator


class ContadorOperacoes:
    """Classe para contar operações específicas."""
    
    def __init__(self):
        self.contadores = defaultdict(int)
        self.lock = Lock()
    
    def incrementar(self, operacao: str, quantidade: int = 1):
        """Incrementa contador de uma operação."""
        with self.lock:
            self.contadores[operacao] += quantidade
    
    def obter_contagem(self, operacao: str = None) -> Union[int, Dict[str, int]]:
        """Obtém contagem de operações."""
        with self.lock:
            if operacao:
                return self.contadores[operacao]
            return dict(self.contadores)
    
    def resetar(self, operacao: str = None):
        """Reseta contadores."""
        with self.lock:
            if operacao:
                self.contadores[operacao] = 0
            else:
                self.contadores.clear()


def contar_operacoes(*operacoes: str):
    """
    Decorator que conta operações específicas durante a execução.
    
    Args:
        *operacoes: Nomes das operações a serem contadas
        
    Returns:
        Decorator que adiciona contagem de operações
    """
    def decorator(func: Callable) -> Callable:
        contador = ContadorOperacoes()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Resetar contadores
            contador.resetar()
            
            # Injetar contador nos kwargs se solicitado
            if 'contador' in func.__code__.co_varnames:
                kwargs['contador'] = contador
            
            resultado = func(*args, **kwargs)
            
            # Exibir contagens
            contagens = contador.obter_contagem()
            if contagens:
                print(f"Operações em {func.__name__}:")
                for op, count in contagens.items():
                    print(f"  {op}: {count:,}")
            
            return resultado
        
        wrapper.contador = contador
        return wrapper
    
    return decorator


def profile_memoria(exibir: bool = True):
    """
    Decorator que monitora uso de memória.
    
    Args:
        exibir: Se deve exibir o resultado automaticamente
        
    Returns:
        Decorator que adiciona profiling de memória
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Forçar garbage collection antes da medição
            gc.collect()
            
            # Medir memória inicial (aproximação)
            memoria_inicial = sys.getsizeof(args) + sys.getsizeof(kwargs)
            
            resultado = func(*args, **kwargs)
            
            # Medir memória final
            memoria_final = sys.getsizeof(resultado) if resultado is not None else 0
            
            # Calcular diferença
            diferenca_memoria = memoria_final - memoria_inicial
            
            if exibir:
                print(f"Memória {func.__name__}: {diferenca_memoria:+,} bytes")
            
            return resultado
        
        return wrapper
    
    return decorator


# ============================================================================
# DECORADORES DE CACHE
# ============================================================================

def cache_resultado(max_size: int = 128):
    """
    Decorator que implementa cache LRU para resultados de função.
    
    Args:
        max_size: Tamanho máximo do cache
        
    Returns:
        Decorator que adiciona cache
    """
    def decorator(func: Callable) -> Callable:
        cache = OrderedDict()
        hits = 0
        misses = 0
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal hits, misses
            
            # Criar chave do cache
            key = str(args) + str(sorted(kwargs.items()))
            
            # Verificar se está no cache
            if key in cache:
                hits += 1
                # Mover para o final (mais recente)
                cache.move_to_end(key)
                return cache[key]
            
            # Calcular resultado
            misses += 1
            resultado = func(*args, **kwargs)
            
            # Adicionar ao cache
            cache[key] = resultado
            cache.move_to_end(key)
            
            # Remover item mais antigo se necessário
            if len(cache) > max_size:
                cache.popitem(last=False)
            
            return resultado
        
        def cache_info():
            """Retorna informações do cache."""
            return {
                'hits': hits,
                'misses': misses,
                'hit_rate': hits / (hits + misses) if (hits + misses) > 0 else 0,
                'cache_size': len(cache),
                'max_size': max_size
            }
        
        def cache_clear():
            """Limpa o cache."""
            nonlocal hits, misses
            cache.clear()
            hits = misses = 0
        
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper
    
    return decorator


def memoize(func: Callable) -> Callable:
    """
    Decorator simples de memoização.
    
    Args:
        func: Função a ser memoizada
        
    Returns:
        Função com memoização
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]
    
    wrapper.cache = cache
    return wrapper


# ============================================================================
# DECORADORES DE LOGGING
# ============================================================================

def log_execucao(nivel: str = 'INFO', incluir_args: bool = False, 
                incluir_resultado: bool = False):
    """
    Decorator que registra execução de função em log.
    
    Args:
        nivel: Nível de log ('DEBUG', 'INFO', 'WARNING', 'ERROR')
        incluir_args: Se deve incluir argumentos no log
        incluir_resultado: Se deve incluir resultado no log
        
    Returns:
        Decorator que adiciona logging
    """
    def decorator(func: Callable) -> Callable:
        logger = logging.getLogger(func.__module__)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Log de início
            msg_inicio = f"Iniciando {func.__name__}"
            if incluir_args and (args or kwargs):
                msg_inicio += f" com args={args}, kwargs={kwargs}"
            
            getattr(logger, nivel.lower())(msg_inicio)
            
            try:
                resultado = func(*args, **kwargs)
                
                # Log de sucesso
                msg_sucesso = f"Concluído {func.__name__}"
                if incluir_resultado:
                    msg_sucesso += f" -> {resultado}"
                
                getattr(logger, nivel.lower())(msg_sucesso)
                
                return resultado
                
            except Exception as e:
                # Log de erro
                logger.error(f"Erro em {func.__name__}: {str(e)}")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                raise
        
        return wrapper
    
    return decorator


def debug_chamadas(exibir_stack: bool = False):
    """
    Decorator para debug de chamadas de função.
    
    Args:
        exibir_stack: Se deve exibir stack trace
        
    Returns:
        Decorator que adiciona debug
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"🔍 Chamando {func.__name__}")
            
            if args:
                print(f"   Args: {args}")
            if kwargs:
                print(f"   Kwargs: {kwargs}")
            
            if exibir_stack:
                print(f"   Stack: {traceback.format_stack()[-2].strip()}")
            
            resultado = func(*args, **kwargs)
            
            print(f"✅ {func.__name__} retornou: {type(resultado).__name__}")
            
            return resultado
        
        return wrapper
    
    return decorator


# ============================================================================
# DECORADORES DE VALIDAÇÃO
# ============================================================================

def validar_tipos(**tipos):
    """
    Decorator que valida tipos de argumentos.
    
    Args:
        **tipos: Mapeamento nome_arg -> tipo_esperado
        
    Returns:
        Decorator que adiciona validação de tipos
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Obter nomes dos parâmetros
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validar tipos
            for nome, valor in bound_args.arguments.items():
                if nome in tipos:
                    tipo_esperado = tipos[nome]
                    if not isinstance(valor, tipo_esperado):
                        raise TypeError(
                            f"Argumento '{nome}' deve ser do tipo {tipo_esperado.__name__}, "
                            f"recebido {type(valor).__name__}"
                        )
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def validar_range(**ranges):
    """
    Decorator que valida ranges de argumentos numéricos.
    
    Args:
        **ranges: Mapeamento nome_arg -> (min, max)
        
    Returns:
        Decorator que adiciona validação de range
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Obter nomes dos parâmetros
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validar ranges
            for nome, valor in bound_args.arguments.items():
                if nome in ranges:
                    min_val, max_val = ranges[nome]
                    if not (min_val <= valor <= max_val):
                        raise ValueError(
                            f"Argumento '{nome}' deve estar entre {min_val} e {max_val}, "
                            f"recebido {valor}"
                        )
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# ============================================================================
# DECORADORES DE RETRY
# ============================================================================

def retry(max_tentativas: int = 3, delay: float = 1.0, 
          backoff: float = 2.0, excecoes: Tuple = (Exception,)):
    """
    Decorator que implementa retry automático.
    
    Args:
        max_tentativas: Número máximo de tentativas
        delay: Delay inicial entre tentativas (segundos)
        backoff: Fator de multiplicação do delay
        excecoes: Tupla de exceções que devem gerar retry
        
    Returns:
        Decorator que adiciona retry
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tentativa = 0
            delay_atual = delay
            
            while tentativa < max_tentativas:
                try:
                    return func(*args, **kwargs)
                
                except excecoes as e:
                    tentativa += 1
                    
                    if tentativa >= max_tentativas:
                        print(f"❌ {func.__name__} falhou após {max_tentativas} tentativas")
                        raise
                    
                    print(f"⚠️  {func.__name__} falhou (tentativa {tentativa}/{max_tentativas}), "
                          f"tentando novamente em {delay_atual:.1f}s...")
                    
                    time.sleep(delay_atual)
                    delay_atual *= backoff
            
            return None  # Nunca deve chegar aqui
        
        return wrapper
    
    return decorator


# ============================================================================
# DECORADORES DE BENCHMARK
# ============================================================================

def benchmark(repeticoes: int = 5, aquecimento: int = 1):
    """
    Decorator que executa benchmark de função.
    
    Args:
        repeticoes: Número de repetições para o benchmark
        aquecimento: Número de execuções de aquecimento
        
    Returns:
        Decorator que adiciona benchmark
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Aquecimento
            for _ in range(aquecimento):
                func(*args, **kwargs)
            
            # Benchmark
            tempos = []
            for i in range(repeticoes):
                gc.collect()  # Limpar garbage collector
                
                inicio = time.perf_counter()
                resultado = func(*args, **kwargs)
                fim = time.perf_counter()
                
                tempos.append(fim - inicio)
            
            # Calcular estatísticas
            tempo_medio = sum(tempos) / len(tempos)
            tempo_min = min(tempos)
            tempo_max = max(tempos)
            desvio = (sum((t - tempo_medio) ** 2 for t in tempos) / len(tempos)) ** 0.5
            
            print(f"📊 Benchmark {func.__name__} ({repeticoes} execuções):")
            print(f"   Tempo médio: {tempo_medio:.6f}s")
            print(f"   Tempo mín:   {tempo_min:.6f}s")
            print(f"   Tempo máx:   {tempo_max:.6f}s")
            print(f"   Desvio:      {desvio:.6f}s")
            
            return resultado
        
        return wrapper
    
    return decorator


def comparar_algoritmos(*funcs):
    """
    Decorator que compara performance de múltiplos algoritmos.
    
    Args:
        *funcs: Funções a serem comparadas
        
    Returns:
        Decorator que adiciona comparação
    """
    def decorator(func_principal: Callable) -> Callable:
        @functools.wraps(func_principal)
        def wrapper(*args, **kwargs):
            resultados = {}
            
            # Testar função principal
            inicio = time.perf_counter()
            resultado_principal = func_principal(*args, **kwargs)
            fim = time.perf_counter()
            resultados[func_principal.__name__] = fim - inicio
            
            # Testar outras funções
            for func in funcs:
                inicio = time.perf_counter()
                func(*args, **kwargs)
                fim = time.perf_counter()
                resultados[func.__name__] = fim - inicio
            
            # Exibir comparação
            print(f"🏁 Comparação de algoritmos:")
            ordenados = sorted(resultados.items(), key=lambda x: x[1])
            
            for i, (nome, tempo) in enumerate(ordenados):
                if i == 0:
                    print(f"   🥇 {nome}: {tempo:.6f}s (mais rápido)")
                else:
                    fator = tempo / ordenados[0][1]
                    print(f"   {i+1}º {nome}: {tempo:.6f}s ({fator:.1f}x mais lento)")
            
            return resultado_principal
        
        return wrapper
    
    return decorator


# ============================================================================
# DECORADORES ESPECIALIZADOS
# ============================================================================

def deprecated(mensagem: str = "Esta função está obsoleta"):
    """
    Decorator que marca função como obsoleta.
    
    Args:
        mensagem: Mensagem de aviso
        
    Returns:
        Decorator que adiciona aviso de obsolescência
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} está obsoleta. {mensagem}",
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def singleton(cls):
    """
    Decorator que implementa padrão Singleton para classes.
    
    Args:
        cls: Classe a ser transformada em singleton
        
    Returns:
        Classe singleton
    """
    instances = {}
    lock = Lock()
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


# ============================================================================
# FUNÇÕES DE TESTE E DEMONSTRAÇÃO
# ============================================================================

def testar_decorators():
    """
    Testa todos os decorators do módulo.
    """
    print("=== TESTE DOS DECORATORS ===")
    print()
    
    # Teste de medição de tempo
    @medir_tempo(exibir=True)
    def operacao_lenta():
        time.sleep(0.1)
        return "concluído"
    
    print("1. MEDIÇÃO DE TEMPO:")
    resultado = operacao_lenta()
    print()
    
    # Teste de cache
    @cache_resultado(max_size=3)
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print("2. CACHE:")
    print(f"   fib(10) = {fibonacci(10)}")
    print(f"   Cache info: {fibonacci.cache_info()}")
    print()
    
    # Teste de validação
    @validar_tipos(x=int, y=int)
    @validar_range(x=(0, 100), y=(0, 100))
    def somar(x, y):
        return x + y
    
    print("3. VALIDAÇÃO:")
    try:
        print(f"   somar(10, 20) = {somar(10, 20)}")
        print(f"   somar(150, 20) = {somar(150, 20)}")  # Deve falhar
    except ValueError as e:
        print(f"   ❌ Erro esperado: {e}")
    print()
    
    # Teste de benchmark
    @benchmark(repeticoes=3)
    def ordenar_lista():
        import random
        lista = [random.randint(1, 1000) for _ in range(1000)]
        return sorted(lista)
    
    print("4. BENCHMARK:")
    ordenar_lista()
    
    print("\n=== TESTE CONCLUÍDO ===")


if __name__ == "__main__":
    testar_decorators()