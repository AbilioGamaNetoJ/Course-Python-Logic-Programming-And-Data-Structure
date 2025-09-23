"""
Módulo: Casos de Uso Avançados de Algoritmos
Tópico: Aplicações Práticas e Otimizações Específicas
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Avançado

Objetivos de Aprendizado:
- Aplicar algoritmos em problemas reais
- Implementar otimizações específicas por domínio
- Combinar múltiplos algoritmos
- Analisar trade-offs em cenários práticos
- Desenvolver soluções híbridas
- Otimizar para casos específicos
- Implementar algoritmos adaptativos
- Resolver problemas de performance complexos

Conceitos Abordados:
- Algoritmos híbridos e adaptativos
- Otimizações específicas por domínio
- Cache-aware algorithms
- Algoritmos online vs offline
- Processamento de streams
- Algoritmos aproximados
- Heurísticas e meta-heurísticas
- Análise de casos extremos

Pré-requisitos:
- Módulos 3.1 a 3.8 completos
- Compreensão de complexidade
- Conhecimento de estruturas de dados
- Experiência com benchmarking

Complexidade:
- Análise multi-dimensional
- Trade-offs tempo vs espaço vs precisão
- Adaptação dinâmica de estratégias
- Otimização para hardware específico
"""

import time
import random
import math
import heapq
import bisect
import sys
from typing import List, Tuple, Dict, Any, Optional, Callable
from collections import defaultdict, deque
import statistics
import psutil
import gc

def algoritmos_hibridos():
    """
    Implementa algoritmos híbridos que combinam múltiplas estratégias.
    """
    print("=== ALGORITMOS HÍBRIDOS ===")
    print()
    
    print("1. INTROSORT (INTROSPECTIVE SORT):")
    
    def introsort(lista):
        """
        Implementa Introsort: Quick Sort + Heap Sort + Insertion Sort.
        """
        def insertion_sort(arr, inicio, fim):
            """Insertion sort para arrays pequenos"""
            for i in range(inicio + 1, fim + 1):
                chave = arr[i]
                j = i - 1
                while j >= inicio and arr[j] > chave:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = chave
        
        def heapify(arr, n, i):
            """Heapify para heap sort"""
            maior = i
            esquerda = 2 * i + 1
            direita = 2 * i + 2
            
            if esquerda < n and arr[esquerda] > arr[maior]:
                maior = esquerda
            
            if direita < n and arr[direita] > arr[maior]:
                maior = direita
            
            if maior != i:
                arr[i], arr[maior] = arr[maior], arr[i]
                heapify(arr, n, maior)
        
        def heap_sort(arr, inicio, fim):
            """Heap sort para casos degenerados"""
            n = fim - inicio + 1
            temp = arr[inicio:fim + 1]
            
            # Construir heap
            for i in range(n // 2 - 1, -1, -1):
                heapify(temp, n, i)
            
            # Extrair elementos
            for i in range(n - 1, 0, -1):
                temp[0], temp[i] = temp[i], temp[0]
                heapify(temp, i, 0)
            
            # Copiar de volta
            arr[inicio:fim + 1] = temp
        
        def particionar(arr, inicio, fim):
            """Particionamento com mediana de três"""
            meio = (inicio + fim) // 2
            
            # Mediana de três
            if arr[meio] < arr[inicio]:
                arr[inicio], arr[meio] = arr[meio], arr[inicio]
            if arr[fim] < arr[inicio]:
                arr[inicio], arr[fim] = arr[fim], arr[inicio]
            if arr[fim] < arr[meio]:
                arr[meio], arr[fim] = arr[fim], arr[meio]
            
            arr[meio], arr[fim] = arr[fim], arr[meio]
            pivo = arr[fim]
            
            i = inicio - 1
            for j in range(inicio, fim):
                if arr[j] <= pivo:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            
            arr[i + 1], arr[fim] = arr[fim], arr[i + 1]
            return i + 1
        
        def introsort_rec(arr, inicio, fim, max_depth):
            """Recursão principal do Introsort"""
            tamanho = fim - inicio + 1
            
            # Usar insertion sort para arrays pequenos
            if tamanho <= 16:
                insertion_sort(arr, inicio, fim)
                return
            
            # Usar heap sort se profundidade máxima atingida
            if max_depth == 0:
                heap_sort(arr, inicio, fim)
                return
            
            # Usar quick sort normalmente
            pos_pivo = particionar(arr, inicio, fim)
            introsort_rec(arr, inicio, pos_pivo - 1, max_depth - 1)
            introsort_rec(arr, pos_pivo + 1, fim, max_depth - 1)
        
        if not lista:
            return lista
        
        arr = lista.copy()
        max_depth = 2 * math.floor(math.log2(len(arr)))
        introsort_rec(arr, 0, len(arr) - 1, max_depth)
        return arr
    
    print("2. TIMSORT (ALGORITMO DO PYTHON):")
    
    def timsort_simplificado(lista):
        """
        Versão simplificada do Timsort usado pelo Python.
        """
        MIN_MERGE = 32
        
        def insertion_sort(arr, esquerda, direita):
            """Insertion sort otimizado"""
            for i in range(esquerda + 1, direita + 1):
                chave = arr[i]
                j = i - 1
                while j >= esquerda and arr[j] > chave:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = chave
        
        def merge(arr, esquerda, meio, direita):
            """Merge otimizado"""
            # Criar arrays temporários
            L = arr[esquerda:meio + 1]
            R = arr[meio + 1:direita + 1]
            
            i = j = 0
            k = esquerda
            
            # Merge principal
            while i < len(L) and j < len(R):
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
            
            # Copiar elementos restantes
            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
            
            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
        
        def get_min_run_size(n):
            """Calcula tamanho mínimo de run"""
            r = 0
            while n >= MIN_MERGE:
                r |= n & 1
                n >>= 1
            return n + r
        
        def encontrar_runs(arr):
            """Encontra runs naturais na array"""
            runs = []
            n = len(arr)
            i = 0
            
            while i < n:
                inicio = i
                
                # Encontrar run crescente ou decrescente
                if i + 1 < n:
                    if arr[i] <= arr[i + 1]:
                        # Run crescente
                        while i + 1 < n and arr[i] <= arr[i + 1]:
                            i += 1
                    else:
                        # Run decrescente - reverter
                        while i + 1 < n and arr[i] > arr[i + 1]:
                            i += 1
                        # Reverter o run
                        arr[inicio:i + 1] = reversed(arr[inicio:i + 1])
                
                # Estender run se muito pequeno
                min_run = get_min_run_size(n)
                if i - inicio + 1 < min_run:
                    fim = min(inicio + min_run - 1, n - 1)
                    insertion_sort(arr, inicio, fim)
                    i = fim
                
                runs.append((inicio, i))
                i += 1
            
            return runs
        
        if len(lista) <= 1:
            return lista
        
        arr = lista.copy()
        runs = encontrar_runs(arr)
        
        # Merge runs usando stack
        stack = []
        
        for run in runs:
            stack.append(run)
            
            # Manter invariantes do stack
            while len(stack) > 1:
                if len(stack) >= 3:
                    # Verificar invariantes A > B + C e B > C
                    c_size = stack[-1][1] - stack[-1][0] + 1
                    b_size = stack[-2][1] - stack[-2][0] + 1
                    a_size = stack[-3][1] - stack[-3][0] + 1
                    
                    if a_size <= b_size + c_size or b_size <= c_size:
                        # Merge menor dos dois
                        if a_size < c_size:
                            # Merge A e B
                            merge(arr, stack[-3][0], stack[-3][1], stack[-2][1])
                            stack[-3] = (stack[-3][0], stack[-2][1])
                            stack.pop(-2)
                        else:
                            # Merge B e C
                            merge(arr, stack[-2][0], stack[-2][1], stack[-1][1])
                            stack[-2] = (stack[-2][0], stack[-1][1])
                            stack.pop()
                    else:
                        break
                else:
                    # Apenas dois elementos
                    b_size = stack[-1][1] - stack[-1][0] + 1
                    a_size = stack[-2][1] - stack[-2][0] + 1
                    
                    if a_size <= b_size:
                        merge(arr, stack[-2][0], stack[-2][1], stack[-1][1])
                        stack[-2] = (stack[-2][0], stack[-1][1])
                        stack.pop()
                    else:
                        break
        
        # Merge runs restantes
        while len(stack) > 1:
            merge(arr, stack[-2][0], stack[-2][1], stack[-1][1])
            stack[-2] = (stack[-2][0], stack[-1][1])
            stack.pop()
        
        return arr
    
    print("3. BENCHMARK DE ALGORITMOS HÍBRIDOS:")
    
    def benchmark_hibridos():
        """Compara algoritmos híbridos com implementações padrão"""
        
        # Diferentes tipos de dados
        cenarios = [
            ("Aleatório", lambda n: [random.randint(1, 1000) for _ in range(n)]),
            ("Quase Ordenado", lambda n: list(range(n)) + [random.randint(1, n) for _ in range(n//10)]),
            ("Reverso", lambda n: list(range(n, 0, -1))),
            ("Muitas Duplicatas", lambda n: [random.randint(1, 10) for _ in range(n)]),
            ("Poucos Únicos", lambda n: [i % 5 for i in range(n)])
        ]
        
        tamanho = 10000
        
        print("   Comparação de algoritmos híbridos (10.000 elementos):")
        print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐")
        print("   │    CENÁRIO      │   PYTHON    │  INTROSORT  │   TIMSORT   │   SPEEDUP   │")
        print("   ├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤")
        
        for nome, gerador in cenarios:
            dados = gerador(tamanho)
            
            # Python sorted
            start = time.perf_counter()
            sorted(dados.copy())
            tempo_python = time.perf_counter() - start
            
            # Introsort
            start = time.perf_counter()
            introsort(dados.copy())
            tempo_intro = time.perf_counter() - start
            
            # Timsort simplificado
            start = time.perf_counter()
            timsort_simplificado(dados.copy())
            tempo_tim = time.perf_counter() - start
            
            # Melhor speedup
            melhor_tempo = min(tempo_intro, tempo_tim)
            speedup = tempo_python / melhor_tempo
            
            print(f"   │ {nome:15} │ {tempo_python*1000:9.2f} ms │ {tempo_intro*1000:9.2f} ms │ "
                  f"{tempo_tim*1000:9.2f} ms │ {speedup:9.2f}x │")
        
        print("   └─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘")
        print()
    
    benchmark_hibridos()

def algoritmos_adaptativos():
    """
    Implementa algoritmos que se adaptam aos dados de entrada.
    """
    print("=== ALGORITMOS ADAPTATIVOS ===")
    print()
    
    print("1. BUSCA ADAPTATIVA:")
    
    class BuscaAdaptativa:
        """
        Sistema de busca que se adapta aos padrões de acesso.
        """
        
        def __init__(self, dados):
            self.dados = dados.copy()
            self.frequencia_acesso = defaultdict(int)
            self.cache = {}
            self.cache_size = 100
            self.estrategia = "linear"  # linear, binaria, interpolada
            
        def _detectar_padrao(self):
            """Detecta padrão nos dados para escolher estratégia"""
            if len(self.dados) < 100:
                return "linear"
            
            # Verificar se está ordenado
            ordenado = all(self.dados[i] <= self.dados[i+1] for i in range(len(self.dados)-1))
            
            if ordenado:
                # Verificar distribuição para interpolação
                if len(set(self.dados)) > len(self.dados) * 0.8:  # Poucos duplicados
                    return "interpolada"
                else:
                    return "binaria"
            else:
                return "linear"
        
        def _busca_linear_adaptativa(self, item):
            """Busca linear que move elementos acessados para frente"""
            for i, valor in enumerate(self.dados):
                if valor == item:
                    # Move to Front heuristic
                    if i > 0:
                        self.dados[0], self.dados[i] = self.dados[i], self.dados[0]
                        return 0
                    return i
            return -1
        
        def _busca_binaria(self, item):
            """Busca binária padrão"""
            esquerda, direita = 0, len(self.dados) - 1
            
            while esquerda <= direita:
                meio = (esquerda + direita) // 2
                
                if self.dados[meio] == item:
                    return meio
                elif self.dados[meio] < item:
                    esquerda = meio + 1
                else:
                    direita = meio - 1
            
            return -1
        
        def _busca_interpolada(self, item):
            """Busca por interpolação"""
            esquerda, direita = 0, len(self.dados) - 1
            
            while (esquerda <= direita and 
                   item >= self.dados[esquerda] and 
                   item <= self.dados[direita]):
                
                if esquerda == direita:
                    return esquerda if self.dados[esquerda] == item else -1
                
                # Interpolação
                pos = esquerda + int(((item - self.dados[esquerda]) * (direita - esquerda)) / 
                                   (self.dados[direita] - self.dados[esquerda]))
                
                if self.dados[pos] == item:
                    return pos
                elif self.dados[pos] < item:
                    esquerda = pos + 1
                else:
                    direita = pos - 1
            
            return -1
        
        def buscar(self, item):
            """Busca adaptativa principal"""
            # Verificar cache primeiro
            if item in self.cache:
                return self.cache[item]
            
            # Atualizar frequência
            self.frequencia_acesso[item] += 1
            
            # Adaptar estratégia periodicamente
            if len(self.frequencia_acesso) % 50 == 0:
                self.estrategia = self._detectar_padrao()
            
            # Executar busca baseada na estratégia
            if self.estrategia == "linear":
                resultado = self._busca_linear_adaptativa(item)
            elif self.estrategia == "binaria":
                resultado = self._busca_binaria(item)
            else:  # interpolada
                resultado = self._busca_interpolada(item)
            
            # Atualizar cache
            if len(self.cache) >= self.cache_size:
                # Remove item menos frequente
                item_menos_freq = min(self.cache.keys(), 
                                    key=lambda x: self.frequencia_acesso[x])
                del self.cache[item_menos_freq]
            
            self.cache[item] = resultado
            return resultado
    
    print("2. ORDENAÇÃO ADAPTATIVA:")
    
    def ordenacao_adaptativa(lista):
        """
        Escolhe algoritmo de ordenação baseado nas características dos dados.
        """
        def analisar_dados(arr):
            """Analisa características dos dados"""
            n = len(arr)
            if n <= 1:
                return {"algoritmo": "nenhum"}
            
            # Verificar se já está ordenado
            inversoes = 0
            for i in range(n - 1):
                if arr[i] > arr[i + 1]:
                    inversoes += 1
            
            ordenacao_parcial = 1 - (inversoes / (n * (n - 1) / 2))
            
            # Verificar duplicatas
            unicos = len(set(arr))
            taxa_duplicatas = 1 - (unicos / n)
            
            # Verificar distribuição
            if unicos > 1:
                min_val, max_val = min(arr), max(arr)
                range_dados = max_val - min_val
                densidade = unicos / (range_dados + 1) if range_dados > 0 else 1
            else:
                densidade = 1
            
            return {
                "tamanho": n,
                "ordenacao_parcial": ordenacao_parcial,
                "taxa_duplicatas": taxa_duplicatas,
                "densidade": densidade,
                "range": max(arr) - min(arr) if unicos > 1 else 0
            }
        
        def insertion_sort(arr):
            """Insertion sort para arrays pequenos"""
            for i in range(1, len(arr)):
                chave = arr[i]
                j = i - 1
                while j >= 0 and arr[j] > chave:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = chave
            return arr
        
        def counting_sort(arr):
            """Counting sort para ranges pequenos"""
            if not arr:
                return arr
            
            min_val, max_val = min(arr), max(arr)
            range_val = max_val - min_val + 1
            
            count = [0] * range_val
            for num in arr:
                count[num - min_val] += 1
            
            resultado = []
            for i, freq in enumerate(count):
                resultado.extend([i + min_val] * freq)
            
            return resultado
        
        def quick_sort(arr):
            """Quick sort padrão"""
            if len(arr) <= 1:
                return arr
            
            pivo = arr[len(arr) // 2]
            esquerda = [x for x in arr if x < pivo]
            meio = [x for x in arr if x == pivo]
            direita = [x for x in arr if x > pivo]
            
            return quick_sort(esquerda) + meio + quick_sort(direita)
        
        # Analisar dados
        analise = analisar_dados(lista)
        
        # Escolher algoritmo
        if analise["tamanho"] <= 10:
            algoritmo = "insertion"
        elif analise["ordenacao_parcial"] > 0.8:
            algoritmo = "insertion"  # Bom para dados quase ordenados
        elif analise["taxa_duplicatas"] > 0.5:
            algoritmo = "counting"  # Muitas duplicatas
        elif analise["range"] <= 1000 and analise["densidade"] > 0.1:
            algoritmo = "counting"  # Range pequeno
        else:
            algoritmo = "quick"
        
        # Executar algoritmo escolhido
        if algoritmo == "insertion":
            return insertion_sort(lista.copy())
        elif algoritmo == "counting":
            return counting_sort(lista.copy())
        else:
            return quick_sort(lista.copy())
    
    print("3. DEMONSTRAÇÃO DE ADAPTAÇÃO:")
    
    def demonstrar_adaptacao():
        """Demonstra como algoritmos se adaptam aos dados"""
        
        # Diferentes cenários
        cenarios = [
            ("Pequeno (5 elementos)", [5, 2, 8, 1, 9]),
            ("Quase Ordenado", list(range(100)) + [50, 75]),
            ("Muitas Duplicatas", [1, 2, 1, 3, 2, 1, 3, 2] * 50),
            ("Range Pequeno", [random.randint(1, 10) for _ in range(200)]),
            ("Aleatório Grande", [random.randint(1, 10000) for _ in range(1000)])
        ]
        
        print("   Algoritmos escolhidos por cenário:")
        print("   ┌─────────────────────┬─────────────────┬─────────────┐")
        print("   │      CENÁRIO        │    ALGORITMO    │    TEMPO    │")
        print("   ├─────────────────────┼─────────────────┼─────────────┤")
        
        for nome, dados in cenarios:
            start = time.perf_counter()
            resultado = ordenacao_adaptativa(dados)
            tempo = (time.perf_counter() - start) * 1000
            
            # Determinar algoritmo usado (simplificado)
            if len(dados) <= 10:
                alg = "Insertion Sort"
            elif len(set(dados)) / len(dados) < 0.5:
                alg = "Counting Sort"
            else:
                alg = "Quick Sort"
            
            print(f"   │ {nome:19} │ {alg:15} │ {tempo:9.3f} ms │")
        
        print("   └─────────────────────┴─────────────────┴─────────────┘")
        print()
        
        # Demonstrar busca adaptativa
        print("   Busca adaptativa em ação:")
        
        # Dados ordenados
        dados_ord = list(range(1000))
        busca_ord = BuscaAdaptativa(dados_ord)
        
        # Dados aleatórios
        dados_rand = [random.randint(1, 1000) for _ in range(1000)]
        busca_rand = BuscaAdaptativa(dados_rand)
        
        # Simular padrão de acesso
        itens_busca = [100, 200, 300, 100, 200, 100]  # Alguns repetidos
        
        print(f"   → Dados ordenados - Estratégia: {busca_ord._detectar_padrao()}")
        print(f"   → Dados aleatórios - Estratégia: {busca_rand._detectar_padrao()}")
        
        for item in itens_busca:
            pos_ord = busca_ord.buscar(item)
            pos_rand = busca_rand.buscar(item)
            print(f"   → Busca {item}: Ordenado={pos_ord}, Aleatório={pos_rand}")
        
        print()
    
    demonstrar_adaptacao()

def otimizacoes_especificas():
    """
    Implementa otimizações específicas para diferentes cenários.
    """
    print("=== OTIMIZAÇÕES ESPECÍFICAS ===")
    print()
    
    print("1. CACHE-AWARE ALGORITHMS:")
    
    def merge_sort_cache_aware(lista, cache_size=64):
        """
        Merge Sort otimizado para cache de CPU.
        """
        def merge_in_place(arr, inicio, meio, fim, temp):
            """Merge usando buffer temporário"""
            # Copiar primeira metade para buffer
            for i in range(inicio, meio + 1):
                temp[i - inicio] = arr[i]
            
            i, j, k = 0, meio + 1, inicio
            temp_size = meio - inicio + 1
            
            # Merge
            while i < temp_size and j <= fim:
                if temp[i] <= arr[j]:
                    arr[k] = temp[i]
                    i += 1
                else:
                    arr[k] = arr[j]
                    j += 1
                k += 1
            
            # Copiar elementos restantes do buffer
            while i < temp_size:
                arr[k] = temp[i]
                i += 1
                k += 1
        
        def merge_sort_rec(arr, inicio, fim, temp):
            """Recursão cache-aware"""
            if fim - inicio <= cache_size:
                # Usar insertion sort para blocos pequenos
                for i in range(inicio + 1, fim + 1):
                    chave = arr[i]
                    j = i - 1
                    while j >= inicio and arr[j] > chave:
                        arr[j + 1] = arr[j]
                        j -= 1
                    arr[j + 1] = chave
                return
            
            meio = (inicio + fim) // 2
            merge_sort_rec(arr, inicio, meio, temp)
            merge_sort_rec(arr, meio + 1, fim, temp)
            merge_in_place(arr, inicio, meio, fim, temp)
        
        if not lista:
            return lista
        
        arr = lista.copy()
        temp = [0] * (len(arr) // 2 + 1)
        merge_sort_rec(arr, 0, len(arr) - 1, temp)
        return arr
    
    print("2. ALGORITMOS PARA STREAMING:")
    
    class StreamProcessor:
        """
        Processador de dados em streaming.
        """
        
        def __init__(self, window_size=1000):
            self.window_size = window_size
            self.buffer = deque(maxlen=window_size)
            self.sorted_buffer = []
            self.stats = {
                'count': 0,
                'sum': 0,
                'min': float('inf'),
                'max': float('-inf')
            }
        
        def add_element(self, elemento):
            """Adiciona elemento ao stream"""
            # Atualizar estatísticas
            self.stats['count'] += 1
            self.stats['sum'] += elemento
            self.stats['min'] = min(self.stats['min'], elemento)
            self.stats['max'] = max(self.stats['max'], elemento)
            
            # Adicionar ao buffer
            if len(self.buffer) == self.window_size:
                # Remover elemento mais antigo das estatísticas da janela
                elemento_removido = self.buffer[0]
                if elemento_removido in self.sorted_buffer:
                    self.sorted_buffer.remove(elemento_removido)
            
            self.buffer.append(elemento)
            
            # Manter buffer ordenado usando inserção binária
            bisect.insort(self.sorted_buffer, elemento)
            if len(self.sorted_buffer) > self.window_size:
                self.sorted_buffer.pop(0)
        
        def get_median(self):
            """Retorna mediana da janela atual"""
            if not self.sorted_buffer:
                return None
            
            n = len(self.sorted_buffer)
            if n % 2 == 0:
                return (self.sorted_buffer[n//2 - 1] + self.sorted_buffer[n//2]) / 2
            else:
                return self.sorted_buffer[n//2]
        
        def get_percentile(self, p):
            """Retorna percentil p da janela atual"""
            if not self.sorted_buffer:
                return None
            
            n = len(self.sorted_buffer)
            index = int(p * (n - 1) / 100)
            return self.sorted_buffer[index]
        
        def get_top_k(self, k):
            """Retorna top k elementos da janela"""
            return self.sorted_buffer[-k:] if len(self.sorted_buffer) >= k else self.sorted_buffer[:]
    
    print("3. ALGORITMOS APROXIMADOS:")
    
    def quick_select_aproximado(lista, k, epsilon=0.1):
        """
        Quick Select aproximado que retorna elemento próximo ao k-ésimo.
        """
        def particionar_aproximado(arr, inicio, fim):
            """Particionamento com amostragem"""
            # Usar amostra para escolher pivô
            sample_size = min(10, fim - inicio + 1)
            sample_indices = random.sample(range(inicio, fim + 1), sample_size)
            sample = [arr[i] for i in sample_indices]
            pivo = statistics.median(sample)
            
            # Encontrar elemento mais próximo do pivô
            pivo_idx = inicio
            min_diff = abs(arr[inicio] - pivo)
            for i in range(inicio, fim + 1):
                diff = abs(arr[i] - pivo)
                if diff < min_diff:
                    min_diff = diff
                    pivo_idx = i
            
            # Mover pivô para o final
            arr[pivo_idx], arr[fim] = arr[fim], arr[pivo_idx]
            pivo_val = arr[fim]
            
            # Particionamento padrão
            i = inicio - 1
            for j in range(inicio, fim):
                if arr[j] <= pivo_val:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            
            arr[i + 1], arr[fim] = arr[fim], arr[i + 1]
            return i + 1
        
        def quick_select_rec(arr, inicio, fim, k_target):
            """Quick select recursivo aproximado"""
            if inicio == fim:
                return arr[inicio]
            
            pos_pivo = particionar_aproximado(arr, inicio, fim)
            
            # Tolerância para aproximação
            tolerancia = int(epsilon * len(arr))
            
            if abs(pos_pivo - k_target) <= tolerancia:
                return arr[pos_pivo]
            elif pos_pivo > k_target:
                return quick_select_rec(arr, inicio, pos_pivo - 1, k_target)
            else:
                return quick_select_rec(arr, pos_pivo + 1, fim, k_target)
        
        if not lista or k < 0 or k >= len(lista):
            return None
        
        arr = lista.copy()
        return quick_select_rec(arr, 0, len(arr) - 1, k)
    
    print("4. DEMONSTRAÇÃO DE OTIMIZAÇÕES:")
    
    def demonstrar_otimizacoes():
        """Demonstra diferentes otimizações"""
        
        # Teste cache-aware
        dados_grandes = [random.randint(1, 100000) for _ in range(50000)]
        
        print("   Cache-aware vs Merge Sort padrão:")
        
        # Merge sort padrão
        def merge_sort_padrao(arr):
            if len(arr) <= 1:
                return arr
            meio = len(arr) // 2
            esquerda = merge_sort_padrao(arr[:meio])
            direita = merge_sort_padrao(arr[meio:])
            
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
        
        start = time.perf_counter()
        merge_sort_padrao(dados_grandes.copy())
        tempo_padrao = time.perf_counter() - start
        
        start = time.perf_counter()
        merge_sort_cache_aware(dados_grandes.copy())
        tempo_cache = time.perf_counter() - start
        
        print(f"   → Merge Sort padrão:     {tempo_padrao*1000:.2f}ms")
        print(f"   → Merge Sort cache-aware: {tempo_cache*1000:.2f}ms")
        print(f"   → Speedup:               {tempo_padrao/tempo_cache:.2f}x")
        print()
        
        # Teste streaming
        print("   Processamento de stream:")
        processor = StreamProcessor(window_size=100)
        
        # Simular stream de dados
        stream_data = [random.randint(1, 1000) for _ in range(500)]
        
        for i, valor in enumerate(stream_data):
            processor.add_element(valor)
            
            if i % 100 == 99:  # A cada 100 elementos
                mediana = processor.get_median()
                p95 = processor.get_percentile(95)
                top5 = processor.get_top_k(5)
                
                print(f"   → Posição {i+1}: Mediana={mediana:.1f}, P95={p95}, Top5={top5[-1]}")
        
        print()
        
        # Teste algoritmo aproximado
        print("   Quick Select aproximado:")
        dados_teste = [random.randint(1, 1000) for _ in range(1000)]
        k = 500  # Mediana
        
        # Exato
        dados_ordenados = sorted(dados_teste)
        valor_exato = dados_ordenados[k]
        
        # Aproximado
        valor_aprox = quick_select_aproximado(dados_teste, k, epsilon=0.05)
        
        erro = abs(valor_exato - valor_aprox) / valor_exato * 100
        
        print(f"   → Valor exato (k={k}):     {valor_exato}")
        print(f"   → Valor aproximado:       {valor_aprox}")
        print(f"   → Erro relativo:          {erro:.2f}%")
        print()
    
    demonstrar_otimizacoes()

if __name__ == "__main__":
    print("MÓDULO 3.9 - CASOS DE USO AVANÇADOS")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    algoritmos_hibridos()
    print("\n" + "="*50 + "\n")
    
    algoritmos_adaptativos()
    print("\n" + "="*50 + "\n")
    
    otimizacoes_especificas()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 3.9 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Algoritmos híbridos (Introsort, Timsort)")
    print("✅ Sistemas adaptativos que se ajustam aos dados")
    print("✅ Otimizações cache-aware")
    print("✅ Processamento de streams em tempo real")
    print("✅ Algoritmos aproximados e heurísticas")
    print("✅ Trade-offs entre precisão e performance")
    print("✅ Análise multi-dimensional de complexidade")
    print("✅ Implementações específicas por domínio")
    print("✅ Benchmarking avançado e profiling")
    print("\n🎉 MÓDULO 03 - ALGORITMOS DE BUSCA E ORDENAÇÃO COMPLETO!")
    print("\n➡️  Próximo: Módulo 04 - Estruturas de Dados Lineares")