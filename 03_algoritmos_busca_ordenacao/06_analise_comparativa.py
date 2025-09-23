"""
Módulo: Análise Comparativa e Otimizações
Tópico: Algoritmos de Busca e Ordenação - Análise Detalhada e Otimizações Práticas
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário a Avançado

Objetivos de Aprendizado:
- Realizar análise comparativa sistemática
- Implementar benchmarks profissionais
- Aplicar otimizações práticas
- Compreender trade-offs de design
- Desenvolver intuição para escolha de algoritmos
- Implementar algoritmos híbridos
- Analisar performance em cenários reais
- Otimizar para diferentes arquiteturas

Conceitos Abordados:
- Metodologia de benchmark
- Análise de complexidade prática vs teórica
- Otimizações de baixo nível
- Algoritmos híbridos e adaptativos
- Cache performance e localidade
- Paralelização de algoritmos
- Profiling e análise de gargalos
- Escolha contextual de algoritmos

Pré-requisitos:
- Módulos 3.1 a 3.5 completos
- Compreensão de todos os algoritmos básicos e avançados
- Conhecimento de análise de complexidade
- Familiaridade com conceitos de arquitetura

Complexidade:
- Análise empírica de todos os algoritmos estudados
- Comparação de constantes multiplicativas
- Impacto de otimizações na complexidade prática
"""

import time
import random
import sys
import gc
import psutil
import os
from typing import List, Tuple, Callable, Dict, Any
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

def metodologia_benchmark():
    """
    Estabelece metodologia rigorosa para benchmarking.
    """
    print("=== METODOLOGIA DE BENCHMARK CIENTÍFICO ===")
    print()
    
    print("1. PRINCÍPIOS FUNDAMENTAIS:")
    print("   → Reprodutibilidade: Resultados consistentes")
    print("   → Isolamento: Minimizar interferências externas")
    print("   → Representatividade: Cenários realistas")
    print("   → Precisão: Medições confiáveis")
    print("   → Comparabilidade: Condições equivalentes")
    print()
    
    print("2. CONFIGURAÇÃO DO AMBIENTE:")
    
    def configurar_ambiente_benchmark():
        """Configura ambiente para benchmarks precisos"""
        # Desabilitar garbage collection durante medições
        gc.disable()
        
        # Configurar recursão para algoritmos recursivos
        sys.setrecursionlimit(10000)
        
        # Informações do sistema
        print(f"   Sistema: {os.name}")
        print(f"   CPU: {psutil.cpu_count()} cores")
        print(f"   Memória: {psutil.virtual_memory().total // (1024**3)} GB")
        print(f"   Python: {sys.version.split()[0]}")
        print()
        
        return True
    
    configurar_ambiente_benchmark()
    
    print("3. TIPOS DE MEDIÇÃO:")
    
    class BenchmarkTimer:
        """Timer preciso para benchmarks"""
        
        def __init__(self, warmup_runs=3, measurement_runs=10):
            self.warmup_runs = warmup_runs
            self.measurement_runs = measurement_runs
            self.times = []
        
        def measure_function(self, func, *args, **kwargs):
            """Mede tempo de execução com warmup"""
            # Warmup - aquece cache e JIT
            for _ in range(self.warmup_runs):
                func(*args, **kwargs)
            
            # Medições reais
            times = []
            for _ in range(self.measurement_runs):
                gc.collect()  # Limpar memória antes da medição
                
                start = time.perf_counter()
                result = func(*args, **kwargs)
                end = time.perf_counter()
                
                times.append(end - start)
            
            self.times = times
            return result, self.get_statistics()
        
        def get_statistics(self):
            """Calcula estatísticas das medições"""
            if not self.times:
                return {}
            
            times_array = np.array(self.times)
            return {
                'mean': np.mean(times_array),
                'median': np.median(times_array),
                'std': np.std(times_array),
                'min': np.min(times_array),
                'max': np.max(times_array),
                'cv': np.std(times_array) / np.mean(times_array) * 100  # Coeficiente de variação
            }
    
    # Demonstração do timer
    timer = BenchmarkTimer()
    
    def exemplo_funcao(n):
        """Função exemplo para demonstrar timer"""
        return sum(range(n))
    
    _, stats = timer.measure_function(exemplo_funcao, 10000)
    
    print("   Exemplo de medição:")
    print(f"   → Tempo médio: {stats['mean']:.6f}s")
    print(f"   → Desvio padrão: {stats['std']:.6f}s")
    print(f"   → Coef. variação: {stats['cv']:.2f}%")
    print()
    
    print("4. GERAÇÃO DE DADOS DE TESTE:")
    
    class DataGenerator:
        """Gerador de dados para testes"""
        
        @staticmethod
        def random_data(size, min_val=1, max_val=1000):
            """Dados aleatórios"""
            return [random.randint(min_val, max_val) for _ in range(size)]
        
        @staticmethod
        def sorted_data(size):
            """Dados ordenados"""
            return list(range(size))
        
        @staticmethod
        def reverse_sorted_data(size):
            """Dados em ordem reversa"""
            return list(range(size, 0, -1))
        
        @staticmethod
        def nearly_sorted_data(size, disorder_percent=5):
            """Dados quase ordenados"""
            data = list(range(size))
            # Embaralhar uma pequena porcentagem
            disorder_count = size * disorder_percent // 100
            for _ in range(disorder_count):
                i, j = random.randint(0, size-1), random.randint(0, size-1)
                data[i], data[j] = data[j], data[i]
            return data
        
        @staticmethod
        def duplicate_heavy_data(size, unique_values=10):
            """Dados com muitas duplicatas"""
            return [random.randint(1, unique_values) for _ in range(size)]
        
        @staticmethod
        def gaussian_data(size, mean=500, std=100):
            """Dados com distribuição gaussiana"""
            return [int(random.gauss(mean, std)) for _ in range(size)]
    
    # Demonstração dos geradores
    gen = DataGenerator()
    
    print("   Tipos de dados de teste:")
    for nome, metodo in [
        ("Aleatório", lambda: gen.random_data(10)),
        ("Ordenado", lambda: gen.sorted_data(10)),
        ("Reverso", lambda: gen.reverse_sorted_data(10)),
        ("Quase ordenado", lambda: gen.nearly_sorted_data(10)),
        ("Duplicatas", lambda: gen.duplicate_heavy_data(10, 3))
    ]:
        dados = metodo()
        print(f"   → {nome:15}: {dados}")
    print()
    
    print("5. CONTROLE DE VARIÁVEIS:")
    print("   ✅ Mesmo hardware para todos os testes")
    print("   ✅ Mesmo conjunto de dados para cada algoritmo")
    print("   ✅ Múltiplas execuções para média estatística")
    print("   ✅ Warmup para estabilizar cache")
    print("   ✅ Garbage collection controlado")
    print("   ✅ Medição de tempo precisa (perf_counter)")
    print("   ✅ Análise estatística dos resultados")
    print()

def benchmark_completo_algoritmos():
    """
    Realiza benchmark completo de todos os algoritmos estudados.
    """
    print("=== BENCHMARK COMPLETO DOS ALGORITMOS ===")
    print()
    
    print("1. IMPLEMENTAÇÕES OTIMIZADAS:")
    
    # Algoritmos de busca
    def busca_linear_otimizada(lista, item):
        """Busca linear com otimizações"""
        # Sentinela para evitar verificação de bounds
        lista_copia = lista + [item]
        i = 0
        while lista_copia[i] != item:
            i += 1
        return i if i < len(lista) else -1
    
    def busca_binaria_otimizada(lista, item):
        """Busca binária iterativa otimizada"""
        esquerda, direita = 0, len(lista) - 1
        
        while esquerda <= direita:
            meio = (esquerda + direita) >> 1  # Divisão por 2 mais rápida
            
            if lista[meio] == item:
                return meio
            elif lista[meio] < item:
                esquerda = meio + 1
            else:
                direita = meio - 1
        
        return -1
    
    # Algoritmos de ordenação básicos
    def bubble_sort_otimizado(lista):
        """Bubble Sort com otimizações"""
        arr = lista.copy()
        n = len(arr)
        
        for i in range(n):
            trocou = False
            # Otimização: últimos i elementos já estão ordenados
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    trocou = True
            
            # Otimização: se não houve trocas, lista está ordenada
            if not trocou:
                break
        
        return arr
    
    def insertion_sort_otimizado(lista):
        """Insertion Sort com busca binária"""
        arr = lista.copy()
        
        for i in range(1, len(arr)):
            chave = arr[i]
            # Busca binária para encontrar posição
            esquerda, direita = 0, i
            
            while esquerda < direita:
                meio = (esquerda + direita) >> 1
                if arr[meio] > chave:
                    direita = meio
                else:
                    esquerda = meio + 1
            
            # Mover elementos e inserir
            for j in range(i, esquerda, -1):
                arr[j] = arr[j - 1]
            arr[esquerda] = chave
        
        return arr
    
    # Algoritmos avançados
    def merge_sort_otimizado(lista):
        """Merge Sort com cutoff para insertion sort"""
        def merge_sort_rec(arr, temp, esquerda, direita):
            if direita - esquerda < 10:  # Cutoff para insertion sort
                insertion_sort_range(arr, esquerda, direita)
                return
            
            if esquerda < direita:
                meio = (esquerda + direita) >> 1
                
                merge_sort_rec(arr, temp, esquerda, meio)
                merge_sort_rec(arr, temp, meio + 1, direita)
                merge_otimizado(arr, temp, esquerda, meio, direita)
        
        def merge_otimizado(arr, temp, esquerda, meio, direita):
            """Merge otimizado usando array temporário"""
            # Copiar para array temporário
            for i in range(esquerda, direita + 1):
                temp[i] = arr[i]
            
            i, j, k = esquerda, meio + 1, esquerda
            
            while i <= meio and j <= direita:
                if temp[i] <= temp[j]:
                    arr[k] = temp[i]
                    i += 1
                else:
                    arr[k] = temp[j]
                    j += 1
                k += 1
            
            # Copiar elementos restantes
            while i <= meio:
                arr[k] = temp[i]
                i += 1
                k += 1
        
        def insertion_sort_range(arr, inicio, fim):
            """Insertion sort para range específico"""
            for i in range(inicio + 1, fim + 1):
                chave = arr[i]
                j = i - 1
                while j >= inicio and arr[j] > chave:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = chave
        
        if len(lista) <= 1:
            return lista.copy()
        
        arr = lista.copy()
        temp = [0] * len(arr)
        merge_sort_rec(arr, temp, 0, len(arr) - 1)
        return arr
    
    def quick_sort_otimizado(lista):
        """Quick Sort com múltiplas otimizações"""
        def quick_sort_rec(arr, inicio, fim):
            while inicio < fim:
                # Cutoff para insertion sort
                if fim - inicio < 16:
                    insertion_sort_range(arr, inicio, fim)
                    break
                
                # Mediana de três para pivô
                pivo_pos = mediana_de_tres(arr, inicio, fim)
                arr[pivo_pos], arr[fim] = arr[fim], arr[pivo_pos]
                
                # Particionamento
                pos_pivo = particionar_hoare(arr, inicio, fim)
                
                # Recursão na menor partição primeiro (otimização de stack)
                if pos_pivo - inicio < fim - pos_pivo:
                    quick_sort_rec(arr, inicio, pos_pivo - 1)
                    inicio = pos_pivo + 1
                else:
                    quick_sort_rec(arr, pos_pivo + 1, fim)
                    fim = pos_pivo - 1
        
        def mediana_de_tres(arr, inicio, fim):
            """Encontra mediana de três elementos"""
            meio = (inicio + fim) >> 1
            
            if arr[meio] < arr[inicio]:
                inicio, meio = meio, inicio
            if arr[fim] < arr[inicio]:
                inicio, fim = fim, inicio
            if arr[fim] < arr[meio]:
                meio, fim = fim, meio
            
            return meio
        
        def particionar_hoare(arr, inicio, fim):
            """Particionamento de Hoare (mais eficiente)"""
            pivo = arr[fim]
            i = inicio - 1
            
            for j in range(inicio, fim):
                if arr[j] <= pivo:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            
            arr[i + 1], arr[fim] = arr[fim], arr[i + 1]
            return i + 1
        
        def insertion_sort_range(arr, inicio, fim):
            for i in range(inicio + 1, fim + 1):
                chave = arr[i]
                j = i - 1
                while j >= inicio and arr[j] > chave:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = chave
        
        if len(lista) <= 1:
            return lista.copy()
        
        arr = lista.copy()
        quick_sort_rec(arr, 0, len(arr) - 1)
        return arr
    
    print("2. CONFIGURAÇÃO DO BENCHMARK:")
    
    # Configurar algoritmos para teste
    algoritmos_busca = [
        ("Busca Linear", busca_linear_otimizada),
        ("Busca Binária", busca_binaria_otimizada)
    ]
    
    algoritmos_ordenacao = [
        ("Bubble Sort", bubble_sort_otimizado),
        ("Insertion Sort", insertion_sort_otimizado),
        ("Merge Sort", merge_sort_otimizado),
        ("Quick Sort", quick_sort_otimizado),
        ("Python sorted()", lambda x: sorted(x))
    ]
    
    # Tamanhos de teste
    tamanhos = [100, 500, 1000, 2000, 5000]
    
    # Tipos de dados
    tipos_dados = [
        ("Aleatório", lambda n: [random.randint(1, n) for _ in range(n)]),
        ("Ordenado", lambda n: list(range(n))),
        ("Reverso", lambda n: list(range(n, 0, -1))),
        ("Quase Ordenado", lambda n: DataGenerator.nearly_sorted_data(n, 5))
    ]
    
    print("3. EXECUTANDO BENCHMARKS DE ORDENAÇÃO:")
    
    class BenchmarkResults:
        """Armazena e analisa resultados de benchmark"""
        
        def __init__(self):
            self.results = defaultdict(lambda: defaultdict(dict))
        
        def add_result(self, algoritmo, tipo_dados, tamanho, tempo):
            self.results[algoritmo][tipo_dados][tamanho] = tempo
        
        def print_summary_table(self):
            """Imprime tabela resumo dos resultados"""
            print("   Tempos médios (ms) por algoritmo e cenário:")
            print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐")
            print("   │   ALGORITMO     │  ALEATÓRIO  │  ORDENADO   │   REVERSO   │ QUASE ORD.  │")
            print("   ├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤")
            
            for algoritmo in self.results:
                linha = f"   │ {algoritmo:15} │"
                for tipo in ["Aleatório", "Ordenado", "Reverso", "Quase Ordenado"]:
                    if tipo in self.results[algoritmo]:
                        # Média dos tempos para todos os tamanhos
                        tempos = list(self.results[algoritmo][tipo].values())
                        tempo_medio = sum(tempos) / len(tempos) * 1000  # Converter para ms
                        linha += f" {tempo_medio:11.3f} │"
                    else:
                        linha += f" {'N/A':11} │"
                print(linha)
            
            print("   └─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘")
    
    # Executar benchmarks
    timer = BenchmarkTimer(warmup_runs=2, measurement_runs=5)
    results = BenchmarkResults()
    
    print("   Executando testes de ordenação...")
    
    for nome_algo, algoritmo in algoritmos_ordenacao:
        print(f"   → Testando {nome_algo}...")
        
        for nome_tipo, gerador in tipos_dados:
            for tamanho in tamanhos:
                # Gerar dados de teste
                dados = gerador(tamanho)
                
                try:
                    # Medir tempo
                    _, stats = timer.measure_function(algoritmo, dados)
                    results.add_result(nome_algo, nome_tipo, tamanho, stats['mean'])
                    
                except Exception as e:
                    print(f"     Erro em {nome_algo} com {nome_tipo} (n={tamanho}): {e}")
                    results.add_result(nome_algo, nome_tipo, tamanho, float('inf'))
    
    results.print_summary_table()
    print()
    
    print("4. ANÁLISE DE ESCALABILIDADE:")
    
    def analisar_escalabilidade(results):
        """Analisa como algoritmos escalam com tamanho"""
        print("   Fator de crescimento (tempo_n2000 / tempo_n1000):")
        print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┐")
        print("   │   ALGORITMO     │  ALEATÓRIO  │  ORDENADO   │   REVERSO   │")
        print("   ├─────────────────┼─────────────┼─────────────┼─────────────┤")
        
        for algoritmo in results.results:
            linha = f"   │ {algoritmo:15} │"
            
            for tipo in ["Aleatório", "Ordenado", "Reverso"]:
                if tipo in results.results[algoritmo]:
                    tempos = results.results[algoritmo][tipo]
                    if 1000 in tempos and 2000 in tempos:
                        fator = tempos[2000] / tempos[1000]
                        linha += f" {fator:11.2f} │"
                    else:
                        linha += f" {'N/A':11} │"
                else:
                    linha += f" {'N/A':11} │"
            
            print(linha)
        
        print("   └─────────────────┴─────────────┴─────────────┴─────────────┘")
        print("   → Fator ~2: O(n log n) | Fator ~4: O(n²)")
    
    analisar_escalabilidade(results)
    print()

def otimizacoes_praticas():
    """
    Demonstra otimizações práticas aplicáveis.
    """
    print("=== OTIMIZAÇÕES PRÁTICAS ===")
    print()
    
    print("1. OTIMIZAÇÕES DE BAIXO NÍVEL:")
    
    def demonstrar_otimizacoes_bit():
        """Demonstra otimizações usando operações bit"""
        print("   Operações bit para divisão/multiplicação:")
        
        # Divisão por 2 usando shift
        def dividir_por_2_normal(n):
            return n // 2
        
        def dividir_por_2_bit(n):
            return n >> 1
        
        # Benchmark das operações
        timer = BenchmarkTimer(measurement_runs=1000000)
        
        n = 12345
        _, stats_normal = timer.measure_function(dividir_por_2_normal, n)
        _, stats_bit = timer.measure_function(dividir_por_2_bit, n)
        
        print(f"   → Divisão normal: {stats_normal['mean']*1e9:.2f} ns")
        print(f"   → Divisão bit:    {stats_bit['mean']*1e9:.2f} ns")
        print(f"   → Speedup:        {stats_normal['mean']/stats_bit['mean']:.2f}x")
        print()
    
    demonstrar_otimizacoes_bit()
    
    print("2. OTIMIZAÇÕES DE MEMÓRIA:")
    
    def comparar_uso_memoria():
        """Compara uso de memória entre implementações"""
        import tracemalloc
        
        def merge_sort_memoria_intensiva(lista):
            """Merge sort que cria muitas listas temporárias"""
            if len(lista) <= 1:
                return lista
            
            meio = len(lista) // 2
            esquerda = merge_sort_memoria_intensiva(lista[:meio])
            direita = merge_sort_memoria_intensiva(lista[meio:])
            
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
        
        def merge_sort_memoria_otimizada(lista):
            """Merge sort que reutiliza array temporário"""
            def merge_sort_rec(arr, temp, inicio, fim):
                if inicio >= fim:
                    return
                
                meio = (inicio + fim) // 2
                merge_sort_rec(arr, temp, inicio, meio)
                merge_sort_rec(arr, temp, meio + 1, fim)
                
                # Merge usando array temporário reutilizado
                for i in range(inicio, fim + 1):
                    temp[i] = arr[i]
                
                i, j, k = inicio, meio + 1, inicio
                
                while i <= meio and j <= fim:
                    if temp[i] <= temp[j]:
                        arr[k] = temp[i]
                        i += 1
                    else:
                        arr[k] = temp[j]
                        j += 1
                    k += 1
                
                while i <= meio:
                    arr[k] = temp[i]
                    i += 1
                    k += 1
            
            arr = lista.copy()
            temp = [0] * len(arr)
            merge_sort_rec(arr, temp, 0, len(arr) - 1)
            return arr
        
        # Testar uso de memória
        dados_teste = [random.randint(1, 1000) for _ in range(1000)]
        
        print("   Comparação de uso de memória:")
        
        # Versão intensiva em memória
        tracemalloc.start()
        resultado1 = merge_sort_memoria_intensiva(dados_teste)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        memoria_intensiva = peak / 1024 / 1024  # MB
        
        # Versão otimizada
        tracemalloc.start()
        resultado2 = merge_sort_memoria_otimizada(dados_teste)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        memoria_otimizada = peak / 1024 / 1024  # MB
        
        print(f"   → Versão intensiva: {memoria_intensiva:.2f} MB")
        print(f"   → Versão otimizada: {memoria_otimizada:.2f} MB")
        print(f"   → Redução:          {(1 - memoria_otimizada/memoria_intensiva)*100:.1f}%")
        print()
    
    comparar_uso_memoria()
    
    print("3. ALGORITMOS HÍBRIDOS:")
    
    def implementar_introsort():
        """Implementa Introsort (Quick + Heap + Insertion)"""
        
        def introsort(lista):
            """Introsort: algoritmo híbrido usado em C++ std::sort"""
            def introsort_rec(arr, inicio, fim, max_depth):
                tamanho = fim - inicio + 1
                
                # Insertion sort para arrays pequenos
                if tamanho < 16:
                    insertion_sort_range(arr, inicio, fim)
                    return
                
                # Heap sort se recursão muito profunda
                if max_depth == 0:
                    heap_sort_range(arr, inicio, fim)
                    return
                
                # Quick sort normal
                pivo = particionar(arr, inicio, fim)
                introsort_rec(arr, inicio, pivo - 1, max_depth - 1)
                introsort_rec(arr, pivo + 1, fim, max_depth - 1)
            
            def insertion_sort_range(arr, inicio, fim):
                for i in range(inicio + 1, fim + 1):
                    chave = arr[i]
                    j = i - 1
                    while j >= inicio and arr[j] > chave:
                        arr[j + 1] = arr[j]
                        j -= 1
                    arr[j + 1] = chave
            
            def heap_sort_range(arr, inicio, fim):
                def heapify(arr, n, i, offset):
                    maior = i
                    esquerdo = 2 * i + 1
                    direito = 2 * i + 2
                    
                    if esquerdo < n and arr[offset + esquerdo] > arr[offset + maior]:
                        maior = esquerdo
                    
                    if direito < n and arr[offset + direito] > arr[offset + maior]:
                        maior = direito
                    
                    if maior != i:
                        arr[offset + i], arr[offset + maior] = arr[offset + maior], arr[offset + i]
                        heapify(arr, n, maior, offset)
                
                tamanho = fim - inicio + 1
                
                # Construir heap
                for i in range(tamanho // 2 - 1, -1, -1):
                    heapify(arr, tamanho, i, inicio)
                
                # Extrair elementos
                for i in range(tamanho - 1, 0, -1):
                    arr[inicio], arr[inicio + i] = arr[inicio + i], arr[inicio]
                    heapify(arr, i, 0, inicio)
            
            def particionar(arr, inicio, fim):
                pivo = arr[fim]
                i = inicio - 1
                
                for j in range(inicio, fim):
                    if arr[j] <= pivo:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                
                arr[i + 1], arr[fim] = arr[fim], arr[i + 1]
                return i + 1
            
            if len(lista) <= 1:
                return lista.copy()
            
            arr = lista.copy()
            max_depth = 2 * int(len(arr).bit_length())  # 2 * log2(n)
            introsort_rec(arr, 0, len(arr) - 1, max_depth)
            return arr
        
        # Testar Introsort
        dados_teste = [random.randint(1, 1000) for _ in range(1000)]
        
        timer = BenchmarkTimer()
        
        # Comparar com outros algoritmos
        algoritmos = [
            ("Quick Sort", quick_sort_otimizado),
            ("Merge Sort", merge_sort_otimizado),
            ("Introsort", introsort),
            ("Python sorted", lambda x: sorted(x))
        ]
        
        print("   Comparação de algoritmos híbridos:")
        print("   ┌─────────────────┬─────────────┬─────────────┐")
        print("   │   ALGORITMO     │    TEMPO    │  SPEEDUP    │")
        print("   ├─────────────────┼─────────────┼─────────────┤")
        
        tempos = {}
        for nome, algoritmo in algoritmos:
            _, stats = timer.measure_function(algoritmo, dados_teste)
            tempos[nome] = stats['mean']
        
        tempo_base = tempos["Python sorted"]
        
        for nome in tempos:
            tempo = tempos[nome]
            speedup = tempo_base / tempo
            print(f"   │ {nome:15} │ {tempo*1000:9.3f} ms │ {speedup:9.2f}x │")
        
        print("   └─────────────────┴─────────────┴─────────────┘")
        print()
    
    implementar_introsort()
    
    print("4. OTIMIZAÇÕES ESPECÍFICAS POR CENÁRIO:")
    
    def otimizacoes_contextuais():
        """Demonstra otimizações específicas por contexto"""
        
        print("   ORDENAÇÃO DE STRINGS:")
        
        def radix_sort_strings(strings):
            """Radix sort para strings (mais eficiente que comparação)"""
            if not strings:
                return strings
            
            # Encontrar comprimento máximo
            max_len = max(len(s) for s in strings)
            
            # Pad strings para mesmo comprimento
            padded = [s.ljust(max_len) for s in strings]
            
            # Radix sort da direita para esquerda
            for pos in range(max_len - 1, -1, -1):
                # Counting sort por caractere na posição
                buckets = [[] for _ in range(256)]  # ASCII
                
                for s in padded:
                    buckets[ord(s[pos])].append(s)
                
                padded = []
                for bucket in buckets:
                    padded.extend(bucket)
            
            # Remover padding
            return [s.rstrip() for s in padded]
        
        # Testar com strings
        strings_teste = [
            "banana", "apple", "cherry", "date", "elderberry",
            "fig", "grape", "honeydew", "kiwi", "lemon"
        ] * 100
        
        timer = BenchmarkTimer()
        
        _, stats_normal = timer.measure_function(lambda x: sorted(x), strings_teste)
        _, stats_radix = timer.measure_function(radix_sort_strings, strings_teste)
        
        print(f"   → Sorted normal: {stats_normal['mean']*1000:.3f} ms")
        print(f"   → Radix sort:    {stats_radix['mean']*1000:.3f} ms")
        print(f"   → Speedup:       {stats_normal['mean']/stats_radix['mean']:.2f}x")
        print()
        
        print("   ORDENAÇÃO DE NÚMEROS PEQUENOS:")
        
        def counting_sort(lista, max_val=1000):
            """Counting sort para números pequenos"""
            if not lista:
                return lista
            
            # Array de contagem
            count = [0] * (max_val + 1)
            
            # Contar ocorrências
            for num in lista:
                count[num] += 1
            
            # Reconstruir array ordenado
            resultado = []
            for i, freq in enumerate(count):
                resultado.extend([i] * freq)
            
            return resultado
        
        # Testar com números pequenos
        numeros_pequenos = [random.randint(1, 100) for _ in range(1000)]
        
        _, stats_normal = timer.measure_function(lambda x: sorted(x), numeros_pequenos)
        _, stats_counting = timer.measure_function(counting_sort, numeros_pequenos)
        
        print(f"   → Sorted normal:  {stats_normal['mean']*1000:.3f} ms")
        print(f"   → Counting sort:  {stats_counting['mean']*1000:.3f} ms")
        print(f"   → Speedup:        {stats_normal['mean']/stats_counting['mean']:.2f}x")
        print()
    
    otimizacoes_contextuais()

def guia_escolha_algoritmos():
    """
    Fornece guia prático para escolha de algoritmos.
    """
    print("=== GUIA PRÁTICO DE ESCOLHA DE ALGORITMOS ===")
    print()
    
    print("1. ÁRVORE DE DECISÃO PARA ORDENAÇÃO:")
    print()
    print("   ┌─ Tamanho < 50? ──── SIM ──── Insertion Sort")
    print("   │")
    print("   ├─ Estabilidade necessária? ──── SIM ──── Merge Sort")
    print("   │")
    print("   ├─ Memória limitada? ──── SIM ──── Heap Sort")
    print("   │")
    print("   ├─ Dados quase ordenados? ──── SIM ──── Insertion Sort")
    print("   │")
    print("   ├─ Performance máxima? ──── SIM ──── Quick Sort (otimizado)")
    print("   │")
    print("   └─ Caso geral ──── Introsort ou Timsort")
    print()
    
    print("2. MATRIZ DE DECISÃO:")
    
    def criar_matriz_decisao():
        """Cria matriz de decisão para algoritmos"""
        
        criterios = [
            "Tamanho pequeno (<50)",
            "Tamanho médio (50-1000)",
            "Tamanho grande (>1000)",
            "Dados aleatórios",
            "Dados ordenados",
            "Dados reversos",
            "Muitas duplicatas",
            "Estabilidade necessária",
            "Memória limitada",
            "Performance crítica",
            "Implementação simples"
        ]
        
        algoritmos = [
            "Insertion", "Quick", "Merge", "Heap", "Bubble", "Selection"
        ]
        
        # Pontuação: 5=Excelente, 4=Bom, 3=OK, 2=Ruim, 1=Péssimo
        scores = {
            "Insertion": [5, 3, 1, 3, 5, 2, 3, 5, 5, 3, 5],
            "Quick":     [3, 5, 5, 5, 2, 2, 4, 1, 4, 5, 3],
            "Merge":     [4, 5, 5, 5, 5, 5, 5, 5, 2, 4, 3],
            "Heap":      [3, 4, 5, 4, 4, 4, 4, 1, 5, 4, 4],
            "Bubble":    [2, 1, 1, 1, 3, 1, 2, 5, 5, 1, 5],
            "Selection": [3, 1, 1, 2, 2, 2, 2, 1, 5, 1, 4]
        }
        
        print("   Matriz de adequação (1=Péssimo, 5=Excelente):")
        print("   ┌─────────────────────────┬─────┬─────┬─────┬─────┬─────┬─────┐")
        print("   │        CRITÉRIO         │ INS │ QCK │ MRG │ HEP │ BBL │ SEL │")
        print("   ├─────────────────────────┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        for i, criterio in enumerate(criterios):
            linha = f"   │ {criterio:23} │"
            for algo in algoritmos:
                score = scores[algo][i]
                linha += f" {score:3} │"
            print(linha)
        
        print("   └─────────────────────────┴─────┴─────┴─────┴─────┴─────┴─────┘")
        print()
        
        # Recomendações por cenário
        print("   RECOMENDAÇÕES POR CENÁRIO:")
        print()
        
        cenarios = [
            ("Sistema embarcado (memória limitada)", "Heap Sort ou Selection Sort"),
            ("Aplicação web (performance crítica)", "Quick Sort otimizado"),
            ("Sistema bancário (estabilidade)", "Merge Sort"),
            ("Dados quase ordenados", "Insertion Sort"),
            ("Lista pequena (<50 elementos)", "Insertion Sort"),
            ("Dados com muitas duplicatas", "3-way Quick Sort"),
            ("Implementação educacional", "Bubble Sort ou Insertion Sort"),
            ("Biblioteca de propósito geral", "Introsort ou Timsort")
        ]
        
        for cenario, recomendacao in cenarios:
            print(f"   → {cenario:35}: {recomendacao}")
        print()
    
    criar_matriz_decisao()
    
    print("3. CHECKLIST DE IMPLEMENTAÇÃO:")
    print()
    
    checklist = [
        "✅ Analisar tamanho típico dos dados",
        "✅ Verificar se estabilidade é necessária",
        "✅ Avaliar restrições de memória",
        "✅ Considerar distribuição dos dados",
        "✅ Definir requisitos de performance",
        "✅ Implementar com otimizações apropriadas",
        "✅ Adicionar fallback para casos extremos",
        "✅ Testar com dados reais",
        "✅ Medir performance em produção",
        "✅ Documentar escolhas e trade-offs"
    ]
    
    for item in checklist:
        print(f"   {item}")
    print()
    
    print("4. ANTI-PADRÕES COMUNS:")
    print()
    
    antipadroes = [
        "❌ Usar Bubble Sort em produção",
        "❌ Quick Sort sem proteção contra O(n²)",
        "❌ Ignorar características dos dados",
        "❌ Otimização prematura sem medição",
        "❌ Implementar do zero sem necessidade",
        "❌ Não considerar algoritmos híbridos",
        "❌ Focar apenas na complexidade teórica",
        "❌ Não testar casos extremos",
        "❌ Ignorar cache e localidade de memória",
        "❌ Não documentar decisões de design"
    ]
    
    for antipadrao in antipadroes:
        print(f"   {antipadrao}")
    print()

if __name__ == "__main__":
    print("MÓDULO 3.6 - ANÁLISE COMPARATIVA E OTIMIZAÇÕES")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    metodologia_benchmark()
    print("\n" + "="*50 + "\n")
    
    benchmark_completo_algoritmos()
    print("\n" + "="*50 + "\n")
    
    otimizacoes_praticas()
    print("\n" + "="*50 + "\n")
    
    guia_escolha_algoritmos()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 3.6 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Metodologia científica de benchmark")
    print("✅ Análise comparativa sistemática")
    print("✅ Otimizações de baixo nível")
    print("✅ Algoritmos híbridos e adaptativos")
    print("✅ Otimizações de memória e cache")
    print("✅ Análise de escalabilidade prática")
    print("✅ Guia de escolha contextual")
    print("✅ Implementação de Introsort")
    print("✅ Anti-padrões e boas práticas")
    print("\n➡️  Próximo: Módulo 3.7 - Algoritmos Especializados")