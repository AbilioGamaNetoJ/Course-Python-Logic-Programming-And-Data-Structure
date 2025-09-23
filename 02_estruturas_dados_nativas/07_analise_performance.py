"""
Módulo: Análise de Performance das Estruturas de Dados Nativas
Tópico: Estruturas de Dados Nativas - Performance e Otimização
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário a Avançado

Objetivos de Aprendizado:
- Compreender complexidade temporal e espacial
- Analisar performance de operações em diferentes estruturas
- Implementar benchmarks para comparação
- Identificar gargalos de performance
- Aplicar técnicas de otimização
- Escolher a estrutura de dados adequada para cada caso
- Usar ferramentas de profiling
- Entender trade-offs entre tempo e espaço

Conceitos Abordados:
- Notação Big O
- Benchmarking de operações
- Profiling de memória
- Comparação entre estruturas
- Otimização de código
- Trade-offs de performance
- Ferramentas de análise

Pré-requisitos:
- Módulos 2.1 a 2.6 completos
- Conhecimento de todas as estruturas nativas
- Compreensão de algoritmos básicos

Complexidade das Estruturas:
- Lista: Acesso O(1), Busca O(n), Inserção O(n)
- Tupla: Acesso O(1), Busca O(n), Imutável
- Dict: Acesso O(1), Busca O(1), Inserção O(1)
- Set: Busca O(1), Inserção O(1), Operações O(n)
- String: Acesso O(1), Busca O(n), Imutável
"""

import time
import sys
import gc
from collections import defaultdict, Counter, deque
import random
import string
import timeit
import tracemalloc
import psutil
import os

def conceito_complexidade():
    """
    Introduz conceitos de complexidade temporal e espacial.
    
    Analogia: Complexidade é como medir a eficiência de diferentes
    métodos para realizar a mesma tarefa.
    """
    print("=== CONCEITOS DE COMPLEXIDADE ===")
    print()
    
    print("1. NOTAÇÃO BIG O:")
    print("   → Descreve como o tempo/espaço cresce com o tamanho da entrada")
    print("   → Foca no pior caso (worst-case scenario)")
    print("   → Ignora constantes e termos de menor ordem")
    print("   → Fundamental para escolher algoritmos eficientes")
    print()
    
    print("2. CLASSES DE COMPLEXIDADE COMUM:")
    print("   ┌─────────────┬─────────────────┬─────────────────────────────┐")
    print("   │ NOTAÇÃO     │   DESCRIÇÃO     │         EXEMPLO             │")
    print("   ├─────────────┼─────────────────┼─────────────────────────────┤")
    print("   │ O(1)        │ Constante       │ Acesso por índice           │")
    print("   │ O(log n)    │ Logarítmica     │ Busca binária               │")
    print("   │ O(n)        │ Linear          │ Busca sequencial            │")
    print("   │ O(n log n)  │ Linearítmica    │ Merge sort, heap sort       │")
    print("   │ O(n²)       │ Quadrática      │ Bubble sort, nested loops   │")
    print("   │ O(2ⁿ)       │ Exponencial     │ Algoritmos recursivos       │")
    print("   │ O(n!)       │ Fatorial        │ Permutações completas       │")
    print("   └─────────────┴─────────────────┴─────────────────────────────┘")
    print()
    
    print("3. VISUALIZAÇÃO DE CRESCIMENTO:")
    tamanhos = [1, 10, 100, 1000]
    
    print("   Comparação para diferentes tamanhos de entrada:")
    print("   ┌─────────┬─────────┬─────────┬─────────┬─────────┐")
    print("   │    n    │  O(1)   │  O(n)   │ O(n²)   │ O(2ⁿ)   │")
    print("   ├─────────┼─────────┼─────────┼─────────┼─────────┤")
    
    for n in tamanhos:
        o1 = 1
        on = n
        on2 = n * n
        o2n = 2 ** min(n, 20)  # Limitando para evitar números muito grandes
        
        print(f"   │ {n:7} │ {o1:7} │ {on:7} │ {on2:7} │ {o2n:7} │")
    
    print("   └─────────┴─────────┴─────────┴─────────┴─────────┘")
    print()
    
    print("4. COMPLEXIDADE DAS ESTRUTURAS NATIVAS:")
    
    estruturas_complexidade = {
        'Lista': {
            'Acesso por índice': 'O(1)',
            'Busca': 'O(n)',
            'Inserção no final': 'O(1) amortizado',
            'Inserção no início': 'O(n)',
            'Remoção no final': 'O(1)',
            'Remoção no início': 'O(n)'
        },
        'Tupla': {
            'Acesso por índice': 'O(1)',
            'Busca': 'O(n)',
            'Criação': 'O(n)',
            'Concatenação': 'O(n+m)'
        },
        'Dicionário': {
            'Acesso por chave': 'O(1) médio',
            'Inserção': 'O(1) médio',
            'Remoção': 'O(1) médio',
            'Busca por valor': 'O(n)'
        },
        'Conjunto (Set)': {
            'Busca': 'O(1) médio',
            'Inserção': 'O(1) médio',
            'Remoção': 'O(1) médio',
            'União': 'O(n+m)',
            'Interseção': 'O(min(n,m))'
        }
    }
    
    for estrutura, operacoes in estruturas_complexidade.items():
        print(f"   {estrutura.upper()}:")
        for operacao, complexidade in operacoes.items():
            print(f"   → {operacao}: {complexidade}")
        print()
    
    print("5. EXEMPLO PRÁTICO - BUSCA:")
    
    def busca_linear(lista, item):
        """Busca linear - O(n)"""
        for i, elemento in enumerate(lista):
            if elemento == item:
                return i
        return -1
    
    def busca_em_set(conjunto, item):
        """Busca em set - O(1) médio"""
        return item in conjunto
    
    # Demonstração
    dados = list(range(1000))
    conjunto_dados = set(dados)
    item_procurado = 999
    
    print("   # Comparando busca linear vs busca em set")
    
    # Busca linear
    start = time.time()
    resultado_linear = busca_linear(dados, item_procurado)
    tempo_linear = time.time() - start
    
    # Busca em set
    start = time.time()
    resultado_set = busca_em_set(conjunto_dados, item_procurado)
    tempo_set = time.time() - start
    
    print(f"   → Busca linear (lista): {tempo_linear:.8f}s")
    print(f"   → Busca em set: {tempo_set:.8f}s")
    print(f"   → Set é {tempo_linear/tempo_set:.1f}x mais rápido")
    print()

def benchmark_operacoes():
    """
    Realiza benchmarks detalhados das operações principais.
    """
    print("=== BENCHMARK DE OPERAÇÕES ===")
    print()
    
    def medir_tempo(func, *args, **kwargs):
        """Mede tempo de execução de uma função"""
        start = time.perf_counter()
        resultado = func(*args, **kwargs)
        end = time.perf_counter()
        return end - start, resultado
    
    print("1. BENCHMARK: CRIAÇÃO DE ESTRUTURAS")
    tamanhos = [1000, 10000, 100000]
    
    for tamanho in tamanhos:
        print(f"\n   Tamanho: {tamanho:,} elementos")
        
        # Lista
        tempo, _ = medir_tempo(list, range(tamanho))
        print(f"   → Lista: {tempo:.6f}s")
        
        # Tupla
        tempo, _ = medir_tempo(tuple, range(tamanho))
        print(f"   → Tupla: {tempo:.6f}s")
        
        # Set
        tempo, _ = medir_tempo(set, range(tamanho))
        print(f"   → Set: {tempo:.6f}s")
        
        # Dict
        tempo, _ = medir_tempo(dict, enumerate(range(tamanho)))
        print(f"   → Dict: {tempo:.6f}s")
    
    print("\n2. BENCHMARK: ACESSO POR ÍNDICE/CHAVE")
    
    # Preparando dados
    tamanho = 100000
    lista = list(range(tamanho))
    tupla = tuple(range(tamanho))
    dicionario = {i: i for i in range(tamanho)}
    
    indices_aleatorios = [random.randint(0, tamanho-1) for _ in range(1000)]
    
    print(f"\n   Acessando 1000 elementos aleatórios em estrutura de {tamanho:,} elementos:")
    
    # Lista
    start = time.perf_counter()
    for i in indices_aleatorios:
        _ = lista[i]
    tempo_lista = time.perf_counter() - start
    print(f"   → Lista[i]: {tempo_lista:.6f}s")
    
    # Tupla
    start = time.perf_counter()
    for i in indices_aleatorios:
        _ = tupla[i]
    tempo_tupla = time.perf_counter() - start
    print(f"   → Tupla[i]: {tempo_tupla:.6f}s")
    
    # Dicionário
    start = time.perf_counter()
    for i in indices_aleatorios:
        _ = dicionario[i]
    tempo_dict = time.perf_counter() - start
    print(f"   → Dict[key]: {tempo_dict:.6f}s")
    
    print("\n3. BENCHMARK: BUSCA DE ELEMENTOS")
    
    # Preparando dados para busca
    elementos_busca = random.sample(range(tamanho), 100)
    conjunto = set(lista)
    
    print(f"\n   Buscando 100 elementos em estrutura de {tamanho:,} elementos:")
    
    # Busca em lista
    start = time.perf_counter()
    for elemento in elementos_busca:
        _ = elemento in lista
    tempo_busca_lista = time.perf_counter() - start
    print(f"   → 'x in lista': {tempo_busca_lista:.6f}s")
    
    # Busca em set
    start = time.perf_counter()
    for elemento in elementos_busca:
        _ = elemento in conjunto
    tempo_busca_set = time.perf_counter() - start
    print(f"   → 'x in set': {tempo_busca_set:.6f}s")
    
    # Busca em dict (chaves)
    start = time.perf_counter()
    for elemento in elementos_busca:
        _ = elemento in dicionario
    tempo_busca_dict = time.perf_counter() - start
    print(f"   → 'x in dict': {tempo_busca_dict:.6f}s")
    
    print(f"\n   → Set é {tempo_busca_lista/tempo_busca_set:.1f}x mais rápido que lista")
    print(f"   → Dict é {tempo_busca_lista/tempo_busca_dict:.1f}x mais rápido que lista")
    
    print("\n4. BENCHMARK: INSERÇÃO DE ELEMENTOS")
    
    print(f"\n   Inserindo 1000 elementos:")
    
    # Lista - append
    lista_teste = []
    start = time.perf_counter()
    for i in range(1000):
        lista_teste.append(i)
    tempo_append = time.perf_counter() - start
    print(f"   → lista.append(): {tempo_append:.6f}s")
    
    # Lista - insert no início
    lista_teste = []
    start = time.perf_counter()
    for i in range(100):  # Menos elementos pois é O(n)
        lista_teste.insert(0, i)
    tempo_insert = time.perf_counter() - start
    print(f"   → lista.insert(0): {tempo_insert:.6f}s (100 elementos)")
    
    # Set - add
    set_teste = set()
    start = time.perf_counter()
    for i in range(1000):
        set_teste.add(i)
    tempo_set_add = time.perf_counter() - start
    print(f"   → set.add(): {tempo_set_add:.6f}s")
    
    # Dict - inserção
    dict_teste = {}
    start = time.perf_counter()
    for i in range(1000):
        dict_teste[i] = i
    tempo_dict_insert = time.perf_counter() - start
    print(f"   → dict[key] = value: {tempo_dict_insert:.6f}s")
    
    print()

def analise_memoria():
    """
    Analisa uso de memória das diferentes estruturas.
    """
    print("=== ANÁLISE DE MEMÓRIA ===")
    print()
    
    print("1. TAMANHO BASE DAS ESTRUTURAS:")
    
    # Estruturas vazias
    lista_vazia = []
    tupla_vazia = ()
    dict_vazio = {}
    set_vazio = set()
    string_vazia = ""
    
    print("   Estruturas vazias:")
    print(f"   → Lista vazia: {sys.getsizeof(lista_vazia)} bytes")
    print(f"   → Tupla vazia: {sys.getsizeof(tupla_vazia)} bytes")
    print(f"   → Dict vazio: {sys.getsizeof(dict_vazio)} bytes")
    print(f"   → Set vazio: {sys.getsizeof(set_vazio)} bytes")
    print(f"   → String vazia: {sys.getsizeof(string_vazia)} bytes")
    print()
    
    print("2. CRESCIMENTO DE MEMÓRIA:")
    
    tamanhos = [10, 100, 1000, 10000]
    
    print("   Memória por tamanho (bytes):")
    print("   ┌─────────┬─────────┬─────────┬─────────┬─────────┐")
    print("   │ Tamanho │  Lista  │  Tupla  │  Dict   │   Set   │")
    print("   ├─────────┼─────────┼─────────┼─────────┼─────────┤")
    
    for tamanho in tamanhos:
        lista = list(range(tamanho))
        tupla = tuple(range(tamanho))
        dicionario = {i: i for i in range(tamanho)}
        conjunto = set(range(tamanho))
        
        mem_lista = sys.getsizeof(lista)
        mem_tupla = sys.getsizeof(tupla)
        mem_dict = sys.getsizeof(dicionario)
        mem_set = sys.getsizeof(conjunto)
        
        print(f"   │ {tamanho:7} │ {mem_lista:7} │ {mem_tupla:7} │ {mem_dict:7} │ {mem_set:7} │")
    
    print("   └─────────┴─────────┴─────────┴─────────┴─────────┘")
    print()
    
    print("3. MEMÓRIA POR ELEMENTO:")
    
    tamanho_ref = 10000
    lista_ref = list(range(tamanho_ref))
    tupla_ref = tuple(range(tamanho_ref))
    dict_ref = {i: i for i in range(tamanho_ref)}
    set_ref = set(range(tamanho_ref))
    
    print(f"   Para {tamanho_ref:,} elementos:")
    print(f"   → Lista: {sys.getsizeof(lista_ref) / tamanho_ref:.2f} bytes/elemento")
    print(f"   → Tupla: {sys.getsizeof(tupla_ref) / tamanho_ref:.2f} bytes/elemento")
    print(f"   → Dict: {sys.getsizeof(dict_ref) / tamanho_ref:.2f} bytes/elemento")
    print(f"   → Set: {sys.getsizeof(set_ref) / tamanho_ref:.2f} bytes/elemento")
    print()
    
    print("4. PROFILING DE MEMÓRIA COM TRACEMALLOC:")
    
    def criar_estruturas_grandes():
        """Cria estruturas grandes para análise"""
        tamanho = 50000
        
        # Lista
        lista = list(range(tamanho))
        
        # Dict com strings
        dicionario = {f"chave_{i}": f"valor_{i}" for i in range(tamanho)}
        
        # Set com strings
        conjunto = {f"item_{i}" for i in range(tamanho)}
        
        return lista, dicionario, conjunto
    
    # Iniciando tracemalloc
    tracemalloc.start()
    
    print("   Criando estruturas grandes...")
    snapshot_inicial = tracemalloc.take_snapshot()
    
    lista_grande, dict_grande, set_grande = criar_estruturas_grandes()
    
    snapshot_final = tracemalloc.take_snapshot()
    
    # Calculando diferença
    top_stats = snapshot_final.compare_to(snapshot_inicial, 'lineno')
    
    print("   Top 3 alocações de memória:")
    for index, stat in enumerate(top_stats[:3]):
        print(f"   → {stat}")
    
    # Memória atual do processo
    processo = psutil.Process(os.getpid())
    memoria_mb = processo.memory_info().rss / 1024 / 1024
    print(f"\n   Memória total do processo: {memoria_mb:.1f} MB")
    
    tracemalloc.stop()
    print()
    
    print("5. COMPARAÇÃO: LISTA vs GERADOR")
    
    def memoria_lista_vs_gerador():
        """Compara memória entre lista e gerador"""
        n = 100000
        
        # Lista
        lista = [x**2 for x in range(n)]
        mem_lista = sys.getsizeof(lista)
        
        # Gerador
        gerador = (x**2 for x in range(n))
        mem_gerador = sys.getsizeof(gerador)
        
        return mem_lista, mem_gerador
    
    mem_lista, mem_gerador = memoria_lista_vs_gerador()
    
    print(f"   Para 100.000 elementos:")
    print(f"   → Lista: {mem_lista:,} bytes")
    print(f"   → Gerador: {mem_gerador:,} bytes")
    print(f"   → Economia: {((mem_lista - mem_gerador) / mem_lista * 100):.1f}%")
    print()

def otimizacao_pratica():
    """
    Demonstra técnicas práticas de otimização.
    """
    print("=== OTIMIZAÇÃO PRÁTICA ===")
    print()
    
    print("1. ESCOLHA DA ESTRUTURA ADEQUADA:")
    
    # Caso 1: Verificação de pertencimento
    print("   Caso 1: Verificar se elementos existem")
    
    def verificar_com_lista(elementos, buscar):
        """Verificação usando lista - O(n) por busca"""
        return [item for item in buscar if item in elementos]
    
    def verificar_com_set(elementos, buscar):
        """Verificação usando set - O(1) por busca"""
        conjunto = set(elementos)
        return [item for item in buscar if item in conjunto]
    
    elementos = list(range(10000))
    buscar = random.sample(elementos, 1000)
    
    # Benchmark
    tempo_lista = timeit.timeit(
        lambda: verificar_com_lista(elementos, buscar),
        number=10
    ) / 10
    
    tempo_set = timeit.timeit(
        lambda: verificar_com_set(elementos, buscar),
        number=10
    ) / 10
    
    print(f"   → Com lista: {tempo_lista:.6f}s")
    print(f"   → Com set: {tempo_set:.6f}s")
    print(f"   → Melhoria: {tempo_lista/tempo_set:.1f}x mais rápido")
    print()
    
    print("2. OTIMIZAÇÃO DE LOOPS:")
    
    # Caso 2: Processamento de dados
    dados = [{'id': i, 'valor': random.randint(1, 100)} for i in range(10000)]
    
    def processar_lento(dados):
        """Versão lenta - múltiplas passadas"""
        # Filtrar valores altos
        valores_altos = []
        for item in dados:
            if item['valor'] > 50:
                valores_altos.append(item)
        
        # Calcular soma
        soma = 0
        for item in valores_altos:
            soma += item['valor']
        
        # Contar itens
        count = 0
        for item in valores_altos:
            count += 1
        
        return soma, count
    
    def processar_rapido(dados):
        """Versão otimizada - uma passada"""
        soma = 0
        count = 0
        for item in dados:
            if item['valor'] > 50:
                soma += item['valor']
                count += 1
        return soma, count
    
    def processar_comprehension(dados):
        """Versão com comprehension"""
        valores_altos = [item['valor'] for item in dados if item['valor'] > 50]
        return sum(valores_altos), len(valores_altos)
    
    # Benchmark das três versões
    tempo_lento = timeit.timeit(lambda: processar_lento(dados), number=100) / 100
    tempo_rapido = timeit.timeit(lambda: processar_rapido(dados), number=100) / 100
    tempo_comp = timeit.timeit(lambda: processar_comprehension(dados), number=100) / 100
    
    print("   Processamento de 10.000 registros:")
    print(f"   → Versão lenta (3 loops): {tempo_lento:.6f}s")
    print(f"   → Versão otimizada (1 loop): {tempo_rapido:.6f}s")
    print(f"   → Comprehension: {tempo_comp:.6f}s")
    print(f"   → Melhoria: {tempo_lento/tempo_rapido:.1f}x mais rápido")
    print()
    
    print("3. CACHE E MEMOIZAÇÃO:")
    
    # Fibonacci sem cache
    def fibonacci_lento(n):
        """Fibonacci recursivo sem cache - O(2^n)"""
        if n <= 1:
            return n
        return fibonacci_lento(n-1) + fibonacci_lento(n-2)
    
    # Fibonacci com cache
    cache_fib = {}
    def fibonacci_cache(n):
        """Fibonacci com memoização - O(n)"""
        if n in cache_fib:
            return cache_fib[n]
        if n <= 1:
            cache_fib[n] = n
            return n
        cache_fib[n] = fibonacci_cache(n-1) + fibonacci_cache(n-2)
        return cache_fib[n]
    
    # Comparação para n=30
    n = 30
    
    start = time.time()
    resultado_lento = fibonacci_lento(n)
    tempo_sem_cache = time.time() - start
    
    start = time.time()
    resultado_cache = fibonacci_cache(n)
    tempo_com_cache = time.time() - start
    
    print(f"   Fibonacci({n}):")
    print(f"   → Sem cache: {tempo_sem_cache:.6f}s")
    print(f"   → Com cache: {tempo_com_cache:.6f}s")
    print(f"   → Melhoria: {tempo_sem_cache/tempo_com_cache:.0f}x mais rápido")
    print()
    
    print("4. OTIMIZAÇÃO DE STRINGS:")
    
    # Concatenação ineficiente
    def concatenar_lento(palavras):
        """Concatenação ineficiente - O(n²)"""
        resultado = ""
        for palavra in palavras:
            resultado += palavra + " "
        return resultado.strip()
    
    # Concatenação eficiente
    def concatenar_rapido(palavras):
        """Concatenação eficiente - O(n)"""
        return " ".join(palavras)
    
    palavras = ["palavra"] * 1000
    
    tempo_lento = timeit.timeit(lambda: concatenar_lento(palavras), number=100) / 100
    tempo_rapido = timeit.timeit(lambda: concatenar_rapido(palavras), number=100) / 100
    
    print(f"   Concatenação de 1000 palavras:")
    print(f"   → Concatenação +=: {tempo_lento:.6f}s")
    print(f"   → join(): {tempo_rapido:.6f}s")
    print(f"   → Melhoria: {tempo_lento/tempo_rapido:.1f}x mais rápido")
    print()
    
    print("5. DICAS DE OTIMIZAÇÃO:")
    print("   ✅ Use set/dict para verificações de pertencimento")
    print("   ✅ Evite loops aninhados desnecessários")
    print("   ✅ Use list/dict comprehensions quando apropriado")
    print("   ✅ Implemente cache para cálculos repetitivos")
    print("   ✅ Use join() para concatenação de strings")
    print("   ✅ Prefira geradores para grandes datasets")
    print("   ✅ Escolha a estrutura de dados adequada ao problema")
    print("   ✅ Profile antes de otimizar")
    print()

def ferramentas_profiling():
    """
    Demonstra ferramentas de profiling e análise.
    """
    print("=== FERRAMENTAS DE PROFILING ===")
    print()
    
    print("1. TIMEIT - MEDIÇÃO PRECISA DE TEMPO:")
    
    # Exemplo com diferentes operações
    operacoes = {
        'Lista append': 'lista.append(1)',
        'Set add': 'conjunto.add(1)',
        'Dict insert': 'dicionario[len(dicionario)] = 1'
    }
    
    setup_code = '''
lista = []
conjunto = set()
dicionario = {}
'''
    
    print("   Tempo para 1000 operações:")
    for nome, codigo in operacoes.items():
        tempo = timeit.timeit(codigo, setup=setup_code, number=1000)
        print(f"   → {nome}: {tempo:.6f}s")
    print()
    
    print("2. CPROFILE - PROFILING DETALHADO:")
    
    import cProfile
    import pstats
    from io import StringIO
    
    def funcao_exemplo():
        """Função para demonstrar profiling"""
        # Operações custosas
        lista = []
        for i in range(10000):
            lista.append(i**2)
        
        # Busca em lista
        for i in range(100):
            _ = 5000 in lista
        
        # Conversão para set e busca
        conjunto = set(lista)
        for i in range(100):
            _ = 5000 in conjunto
        
        return len(lista)
    
    # Executando profiling
    pr = cProfile.Profile()
    pr.enable()
    
    resultado = funcao_exemplo()
    
    pr.disable()
    
    # Capturando estatísticas
    s = StringIO()
    ps = pstats.Stats(pr, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(10)  # Top 10 funções
    
    print("   Profiling da função_exemplo():")
    print("   (Mostrando principais estatísticas)")
    
    # Extraindo informações principais
    stats_output = s.getvalue()
    lines = stats_output.split('\n')
    for line in lines[5:15]:  # Primeiras linhas relevantes
        if line.strip():
            print(f"   {line}")
    print()
    
    print("3. MEMORY_PROFILER - ANÁLISE DE MEMÓRIA:")
    
    def funcao_memoria():
        """Função que consome memória"""
        # Lista grande
        lista_grande = list(range(100000))
        
        # Dict grande
        dict_grande = {i: f"valor_{i}" for i in range(50000)}
        
        # Processamento
        resultado = sum(lista_grande)
        
        return resultado
    
    # Medindo memória antes e depois
    processo = psutil.Process()
    memoria_inicial = processo.memory_info().rss / 1024 / 1024
    
    resultado = funcao_memoria()
    
    memoria_final = processo.memory_info().rss / 1024 / 1024
    diferenca = memoria_final - memoria_inicial
    
    print(f"   Memória antes: {memoria_inicial:.1f} MB")
    print(f"   Memória depois: {memoria_final:.1f} MB")
    print(f"   Diferença: {diferenca:.1f} MB")
    print()
    
    print("4. ANÁLISE DE GARGALOS:")
    
    def identificar_gargalos():
        """Identifica operações custosas"""
        
        # Operação custosa 1: Loop aninhado
        start = time.perf_counter()
        matriz = []
        for i in range(100):
            linha = []
            for j in range(100):
                linha.append(i * j)
            matriz.append(linha)
        tempo_loop_aninhado = time.perf_counter() - start
        
        # Operação custosa 2: List comprehension
        start = time.perf_counter()
        matriz_comp = [[i * j for j in range(100)] for i in range(100)]
        tempo_comprehension = time.perf_counter() - start
        
        # Operação custosa 3: Busca em lista grande
        lista_grande = list(range(10000))
        start = time.perf_counter()
        for i in range(100):
            _ = 9999 in lista_grande
        tempo_busca_lista = time.perf_counter() - start
        
        # Operação otimizada: Busca em set
        set_grande = set(lista_grande)
        start = time.perf_counter()
        for i in range(100):
            _ = 9999 in set_grande
        tempo_busca_set = time.perf_counter() - start
        
        return {
            'loop_aninhado': tempo_loop_aninhado,
            'comprehension': tempo_comprehension,
            'busca_lista': tempo_busca_lista,
            'busca_set': tempo_busca_set
        }
    
    tempos = identificar_gargalos()
    
    print("   Análise de gargalos:")
    print(f"   → Loop aninhado: {tempos['loop_aninhado']:.6f}s")
    print(f"   → List comprehension: {tempos['comprehension']:.6f}s")
    print(f"   → Busca em lista: {tempos['busca_lista']:.6f}s")
    print(f"   → Busca em set: {tempos['busca_set']:.6f}s")
    
    print("\n   Recomendações:")
    if tempos['comprehension'] < tempos['loop_aninhado']:
        print("   ✅ Use list comprehension em vez de loops aninhados")
    if tempos['busca_set'] < tempos['busca_lista']:
        print("   ✅ Use set para buscas frequentes")
    print()
    
    print("5. CHECKLIST DE PERFORMANCE:")
    print("   📊 ANTES DE OTIMIZAR:")
    print("   → Meça o desempenho atual")
    print("   → Identifique os gargalos reais")
    print("   → Defina metas de performance")
    print()
    print("   🔧 DURANTE A OTIMIZAÇÃO:")
    print("   → Otimize um gargalo por vez")
    print("   → Meça após cada mudança")
    print("   → Mantenha a legibilidade do código")
    print()
    print("   ✅ APÓS OTIMIZAR:")
    print("   → Verifique se as metas foram atingidas")
    print("   → Teste a correção do código")
    print("   → Documente as otimizações")
    print()

if __name__ == "__main__":
    print("MÓDULO 2.7 - ANÁLISE DE PERFORMANCE")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceito_complexidade()
    print("\n" + "="*50 + "\n")
    
    benchmark_operacoes()
    print("\n" + "="*50 + "\n")
    
    analise_memoria()
    print("\n" + "="*50 + "\n")
    
    otimizacao_pratica()
    print("\n" + "="*50 + "\n")
    
    ferramentas_profiling()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 2.7 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceitos de complexidade temporal e espacial")
    print("✅ Benchmark de operações em estruturas nativas")
    print("✅ Análise de uso de memória")
    print("✅ Técnicas práticas de otimização")
    print("✅ Ferramentas de profiling e análise")
    print("✅ Identificação e correção de gargalos")
    print("✅ Escolha adequada de estruturas de dados")
    print("\n🎉 MÓDULO 02 - ESTRUTURAS DE DADOS NATIVAS COMPLETO!")
    print("\n📚 Resumo do Módulo 02:")
    print("   2.1 - Listas e Operações")
    print("   2.2 - Tuplas e Imutabilidade") 
    print("   2.3 - Dicionários e Mapeamentos")
    print("   2.4 - Conjuntos (Sets)")
    print("   2.5 - Strings e Manipulação de Texto")
    print("   2.6 - List Comprehensions e Geradores")
    print("   2.7 - Análise de Performance")
    print("\n➡️  Próximo: Módulo 03 - Algoritmos de Busca e Ordenação")