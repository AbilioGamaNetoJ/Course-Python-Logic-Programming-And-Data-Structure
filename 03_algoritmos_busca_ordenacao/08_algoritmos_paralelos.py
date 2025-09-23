"""
Módulo: Algoritmos Paralelos e Distribuídos
Tópico: Paralelização de Algoritmos de Busca e Ordenação
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Avançado

Objetivos de Aprendizado:
- Compreender conceitos de paralelização
- Implementar algoritmos paralelos
- Analisar speedup e eficiência
- Aplicar técnicas de divide-and-conquer paralelo
- Gerenciar sincronização e comunicação
- Otimizar para arquiteturas multi-core
- Implementar algoritmos distribuídos
- Analisar trade-offs de paralelização

Conceitos Abordados:
- Threading vs Multiprocessing em Python
- Algoritmos paralelos de ordenação
- Busca paralela em estruturas
- Sincronização e locks
- Map-Reduce para big data
- Algoritmos distribuídos
- Load balancing e particionamento
- Análise de complexidade paralela

Pré-requisitos:
- Módulos 3.1 a 3.7 completos
- Conhecimento básico de concorrência
- Compreensão de arquiteturas multi-core
- Familiaridade com threading/multiprocessing

Complexidade:
- Análise de speedup teórico vs prático
- Lei de Amdahl e escalabilidade
- Overhead de comunicação
- Eficiência paralela
"""

import threading
import multiprocessing as mp
import concurrent.futures
import time
import random
import math
import queue
from typing import List, Tuple, Callable, Any
import os
import psutil

def conceitos_paralelizacao():
    """
    Introduz conceitos fundamentais de paralelização.
    """
    print("=== CONCEITOS FUNDAMENTAIS DE PARALELIZAÇÃO ===")
    print()
    
    print("1. TIPOS DE PARALELISMO:")
    print("   → Paralelismo de Dados: Mesmo algoritmo, dados diferentes")
    print("   → Paralelismo de Tarefas: Algoritmos diferentes, dados relacionados")
    print("   → Pipeline: Processamento em estágios sequenciais")
    print("   → Divide-and-Conquer: Divisão recursiva do problema")
    print()
    
    print("2. THREADING vs MULTIPROCESSING:")
    
    def demonstrar_gil():
        """Demonstra limitações do GIL em Python"""
        
        def tarefa_cpu_intensiva(n):
            """Tarefa que usa muito CPU"""
            total = 0
            for i in range(n):
                total += i * i
            return total
        
        def tarefa_io_intensiva():
            """Tarefa que simula I/O"""
            time.sleep(0.1)
            return "IO completo"
        
        # Teste sequencial
        print("   TESTE DE PERFORMANCE:")
        
        n = 1000000
        num_threads = 4
        
        # CPU-bound sequencial
        start = time.perf_counter()
        for _ in range(num_threads):
            tarefa_cpu_intensiva(n)
        tempo_seq_cpu = time.perf_counter() - start
        
        # CPU-bound com threading
        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(tarefa_cpu_intensiva, n) for _ in range(num_threads)]
            concurrent.futures.wait(futures)
        tempo_thread_cpu = time.perf_counter() - start
        
        # CPU-bound com multiprocessing
        start = time.perf_counter()
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(tarefa_cpu_intensiva, n) for _ in range(num_threads)]
            concurrent.futures.wait(futures)
        tempo_proc_cpu = time.perf_counter() - start
        
        print(f"   CPU-bound (4 tarefas):")
        print(f"   → Sequencial:     {tempo_seq_cpu:.3f}s")
        print(f"   → Threading:      {tempo_thread_cpu:.3f}s (speedup: {tempo_seq_cpu/tempo_thread_cpu:.2f}x)")
        print(f"   → Multiprocessing: {tempo_proc_cpu:.3f}s (speedup: {tempo_seq_cpu/tempo_proc_cpu:.2f}x)")
        print()
        
        # I/O-bound sequencial
        start = time.perf_counter()
        for _ in range(num_threads):
            tarefa_io_intensiva()
        tempo_seq_io = time.perf_counter() - start
        
        # I/O-bound com threading
        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(tarefa_io_intensiva) for _ in range(num_threads)]
            concurrent.futures.wait(futures)
        tempo_thread_io = time.perf_counter() - start
        
        print(f"   I/O-bound (4 tarefas):")
        print(f"   → Sequencial: {tempo_seq_io:.3f}s")
        print(f"   → Threading:  {tempo_thread_io:.3f}s (speedup: {tempo_seq_io/tempo_thread_io:.2f}x)")
        print()
    
    demonstrar_gil()
    
    print("3. LEI DE AMDAHL:")
    print("   → Speedup máximo = 1 / (s + (1-s)/p)")
    print("   → s = fração sequencial, p = número de processadores")
    print("   → Mostra limitações da paralelização")
    print()
    
    def calcular_speedup_amdahl():
        """Calcula speedup teórico pela Lei de Amdahl"""
        
        fracoes_sequenciais = [0.05, 0.10, 0.25, 0.50]
        processadores = [2, 4, 8, 16, 32]
        
        print("   Speedup teórico pela Lei de Amdahl:")
        print("   ┌─────────────┬─────┬─────┬─────┬─────┬─────┐")
        print("   │ Fração Seq. │  2P │  4P │  8P │ 16P │ 32P │")
        print("   ├─────────────┼─────┼─────┼─────┼─────┼─────┤")
        
        for s in fracoes_sequenciais:
            linha = f"   │    {s:5.2f}    │"
            for p in processadores:
                speedup = 1 / (s + (1 - s) / p)
                linha += f" {speedup:3.1f} │"
            print(linha)
        
        print("   └─────────────┴─────┴─────┴─────┴─────┴─────┘")
        print("   → Observe como fração sequencial limita speedup")
        print()
    
    calcular_speedup_amdahl()
    
    print("4. OVERHEAD DE PARALELIZAÇÃO:")
    
    def medir_overhead():
        """Mede overhead de criação de threads/processos"""
        
        def tarefa_simples(x):
            return x * x
        
        dados = list(range(1000))
        
        # Sequencial
        start = time.perf_counter()
        resultado_seq = [tarefa_simples(x) for x in dados]
        tempo_seq = time.perf_counter() - start
        
        # Threading
        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            resultado_thread = list(executor.map(tarefa_simples, dados))
        tempo_thread = time.perf_counter() - start
        
        # Multiprocessing
        start = time.perf_counter()
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            resultado_proc = list(executor.map(tarefa_simples, dados))
        tempo_proc = time.perf_counter() - start
        
        print("   Overhead para tarefa simples (1000 elementos):")
        print(f"   → Sequencial:      {tempo_seq*1000:.3f}ms")
        print(f"   → Threading:       {tempo_thread*1000:.3f}ms (overhead: {(tempo_thread/tempo_seq-1)*100:+.1f}%)")
        print(f"   → Multiprocessing: {tempo_proc*1000:.3f}ms (overhead: {(tempo_proc/tempo_seq-1)*100:+.1f}%)")
        print()
    
    medir_overhead()

def merge_sort_paralelo():
    """
    Implementa Merge Sort paralelo usando diferentes abordagens.
    """
    print("=== MERGE SORT PARALELO ===")
    print()
    
    print("1. VERSÃO COM THREADING:")
    
    def merge_sort_threading(lista, max_threads=4):
        """
        Merge Sort paralelo usando threading.
        """
        def merge(esquerda, direita):
            """Merge duas listas ordenadas"""
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
        
        def merge_sort_rec(arr, depth=0):
            """Merge sort recursivo com paralelização"""
            if len(arr) <= 1:
                return arr
            
            meio = len(arr) // 2
            esquerda = arr[:meio]
            direita = arr[meio:]
            
            # Paralelizar apenas nos primeiros níveis
            if depth < math.log2(max_threads):
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    future_esq = executor.submit(merge_sort_rec, esquerda, depth + 1)
                    future_dir = executor.submit(merge_sort_rec, direita, depth + 1)
                    
                    esquerda_ord = future_esq.result()
                    direita_ord = future_dir.result()
            else:
                # Sequencial para evitar overhead
                esquerda_ord = merge_sort_rec(esquerda, depth + 1)
                direita_ord = merge_sort_rec(direita, depth + 1)
            
            return merge(esquerda_ord, direita_ord)
        
        return merge_sort_rec(lista.copy())
    
    print("2. VERSÃO COM MULTIPROCESSING:")
    
    def merge_sort_multiprocessing(lista, max_processes=None):
        """
        Merge Sort paralelo usando multiprocessing.
        """
        if max_processes is None:
            max_processes = mp.cpu_count()
        
        def merge(esquerda, direita):
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
        
        def merge_sort_seq(arr):
            """Merge sort sequencial para subprocessos"""
            if len(arr) <= 1:
                return arr
            
            meio = len(arr) // 2
            esquerda = merge_sort_seq(arr[:meio])
            direita = merge_sort_seq(arr[meio:])
            return merge(esquerda, direita)
        
        if len(lista) < 1000:  # Threshold para evitar overhead
            return merge_sort_seq(lista)
        
        # Dividir em chunks para processos
        chunk_size = len(lista) // max_processes
        chunks = []
        
        for i in range(0, len(lista), chunk_size):
            chunks.append(lista[i:i + chunk_size])
        
        # Ordenar chunks em paralelo
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_processes) as executor:
            chunks_ordenados = list(executor.map(merge_sort_seq, chunks))
        
        # Merge sequencial dos chunks ordenados
        while len(chunks_ordenados) > 1:
            novos_chunks = []
            for i in range(0, len(chunks_ordenados), 2):
                if i + 1 < len(chunks_ordenados):
                    merged = merge(chunks_ordenados[i], chunks_ordenados[i + 1])
                    novos_chunks.append(merged)
                else:
                    novos_chunks.append(chunks_ordenados[i])
            chunks_ordenados = novos_chunks
        
        return chunks_ordenados[0] if chunks_ordenados else []
    
    print("3. BENCHMARK DE PERFORMANCE:")
    
    def benchmark_merge_sort():
        """Compara performance das versões paralelas"""
        
        # Gerar dados de teste
        tamanhos = [1000, 5000, 10000, 50000]
        
        print("   Comparação de performance (tempo em ms):")
        print("   ┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐")
        print("   │   TAMANHO   │ SEQUENCIAL  │  THREADING  │ MULTIPROC.  │ PYTHON SORT │")
        print("   ├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤")
        
        for tamanho in tamanhos:
            dados = [random.randint(1, 10000) for _ in range(tamanho)]
            
            # Merge sort sequencial
            def merge_sort_seq(arr):
                if len(arr) <= 1:
                    return arr
                meio = len(arr) // 2
                esquerda = merge_sort_seq(arr[:meio])
                direita = merge_sort_seq(arr[meio:])
                
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
            
            # Medir tempos
            tempos = {}
            
            # Sequencial
            start = time.perf_counter()
            merge_sort_seq(dados.copy())
            tempos['seq'] = (time.perf_counter() - start) * 1000
            
            # Threading
            start = time.perf_counter()
            merge_sort_threading(dados.copy())
            tempos['thread'] = (time.perf_counter() - start) * 1000
            
            # Multiprocessing
            start = time.perf_counter()
            merge_sort_multiprocessing(dados.copy())
            tempos['proc'] = (time.perf_counter() - start) * 1000
            
            # Python built-in
            start = time.perf_counter()
            sorted(dados.copy())
            tempos['python'] = (time.perf_counter() - start) * 1000
            
            print(f"   │ {tamanho:11,} │ {tempos['seq']:11.2f} │ {tempos['thread']:11.2f} │ "
                  f"{tempos['proc']:11.2f} │ {tempos['python']:11.2f} │")
        
        print("   └─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘")
        print()
    
    benchmark_merge_sort()

def quick_sort_paralelo():
    """
    Implementa Quick Sort paralelo com diferentes estratégias.
    """
    print("=== QUICK SORT PARALELO ===")
    print()
    
    print("1. PARALELIZAÇÃO SIMPLES:")
    
    def quick_sort_paralelo_simples(lista, max_depth=3):
        """
        Quick Sort paralelo com profundidade limitada.
        """
        def particionar(arr, inicio, fim):
            """Particionamento padrão"""
            pivo = arr[fim]
            i = inicio - 1
            
            for j in range(inicio, fim):
                if arr[j] <= pivo:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            
            arr[i + 1], arr[fim] = arr[fim], arr[i + 1]
            return i + 1
        
        def quick_sort_rec(arr, inicio, fim, depth=0):
            """Quick sort recursivo com paralelização"""
            if inicio < fim:
                pos_pivo = particionar(arr, inicio, fim)
                
                # Paralelizar apenas nos primeiros níveis
                if depth < max_depth:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                        future_esq = executor.submit(quick_sort_rec, arr, inicio, pos_pivo - 1, depth + 1)
                        future_dir = executor.submit(quick_sort_rec, arr, pos_pivo + 1, fim, depth + 1)
                        
                        future_esq.result()
                        future_dir.result()
                else:
                    # Sequencial para evitar overhead
                    quick_sort_rec(arr, inicio, pos_pivo - 1, depth + 1)
                    quick_sort_rec(arr, pos_pivo + 1, fim, depth + 1)
        
        arr = lista.copy()
        quick_sort_rec(arr, 0, len(arr) - 1)
        return arr
    
    print("2. QUICK SORT COM WORK-STEALING:")
    
    def quick_sort_work_stealing(lista, num_workers=4):
        """
        Quick Sort usando padrão work-stealing.
        """
        if len(lista) <= 1:
            return lista
        
        # Fila de trabalho compartilhada
        work_queue = queue.Queue()
        result_lock = threading.Lock()
        
        # Resultado compartilhado
        arr = lista.copy()
        
        def particionar(inicio, fim):
            """Particionamento thread-safe"""
            pivo = arr[fim]
            i = inicio - 1
            
            for j in range(inicio, fim):
                if arr[j] <= pivo:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            
            arr[i + 1], arr[fim] = arr[fim], arr[i + 1]
            return i + 1
        
        def worker():
            """Worker que processa tarefas da fila"""
            while True:
                try:
                    inicio, fim = work_queue.get(timeout=0.1)
                    
                    if inicio < fim:
                        with result_lock:
                            pos_pivo = particionar(inicio, fim)
                        
                        # Adicionar subtarefas à fila
                        if pos_pivo - 1 > inicio:
                            work_queue.put((inicio, pos_pivo - 1))
                        if fim > pos_pivo + 1:
                            work_queue.put((pos_pivo + 1, fim))
                    
                    work_queue.task_done()
                    
                except queue.Empty:
                    break
        
        # Adicionar tarefa inicial
        work_queue.put((0, len(arr) - 1))
        
        # Criar e iniciar workers
        threads = []
        for _ in range(num_workers):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)
        
        # Aguardar conclusão
        work_queue.join()
        
        # Finalizar threads
        for t in threads:
            t.join()
        
        return arr
    
    print("3. COMPARAÇÃO DE ESTRATÉGIAS:")
    
    def comparar_quick_sort_paralelo():
        """Compara diferentes estratégias de paralelização"""
        
        dados_teste = [random.randint(1, 10000) for _ in range(10000)]
        
        # Quick sort sequencial
        def quick_sort_seq(arr):
            if len(arr) <= 1:
                return arr
            
            pivo = arr[len(arr) // 2]
            esquerda = [x for x in arr if x < pivo]
            meio = [x for x in arr if x == pivo]
            direita = [x for x in arr if x > pivo]
            
            return quick_sort_seq(esquerda) + meio + quick_sort_seq(direita)
        
        algoritmos = [
            ("Sequencial", lambda x: quick_sort_seq(x)),
            ("Paralelo Simples", lambda x: quick_sort_paralelo_simples(x)),
            ("Work-Stealing", lambda x: quick_sort_work_stealing(x)),
            ("Python sorted", lambda x: sorted(x))
        ]
        
        print("   Performance com 10.000 elementos:")
        print("   ┌─────────────────┬─────────────┬─────────────┐")
        print("   │   ALGORITMO     │    TEMPO    │   SPEEDUP   │")
        print("   ├─────────────────┼─────────────┼─────────────┤")
        
        tempo_base = None
        
        for nome, algoritmo in algoritmos:
            start = time.perf_counter()
            resultado = algoritmo(dados_teste.copy())
            tempo = time.perf_counter() - start
            
            if tempo_base is None:
                tempo_base = tempo
                speedup_str = "1.00x"
            else:
                speedup = tempo_base / tempo
                speedup_str = f"{speedup:.2f}x"
            
            print(f"   │ {nome:15} │ {tempo*1000:9.2f} ms │ {speedup_str:11} │")
        
        print("   └─────────────────┴─────────────┴─────────────┘")
        print()
    
    comparar_quick_sort_paralelo()

def busca_paralela():
    """
    Implementa algoritmos de busca paralela.
    """
    print("=== BUSCA PARALELA ===")
    print()
    
    print("1. BUSCA LINEAR PARALELA:")
    
    def busca_linear_paralela(lista, item, num_workers=4):
        """
        Busca linear paralela dividindo lista em chunks.
        """
        if not lista:
            return -1
        
        chunk_size = len(lista) // num_workers
        if chunk_size == 0:
            chunk_size = 1
        
        def buscar_chunk(args):
            """Busca em um chunk específico"""
            chunk, item_busca, offset = args
            for i, valor in enumerate(chunk):
                if valor == item_busca:
                    return offset + i
            return -1
        
        # Criar chunks com offsets
        chunks_com_offset = []
        for i in range(0, len(lista), chunk_size):
            chunk = lista[i:i + chunk_size]
            chunks_com_offset.append((chunk, item, i))
        
        # Buscar em paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            resultados = list(executor.map(buscar_chunk, chunks_com_offset))
        
        # Encontrar primeiro resultado válido
        for resultado in resultados:
            if resultado != -1:
                return resultado
        
        return -1
    
    def busca_linear_todas_ocorrencias(lista, item, num_workers=4):
        """
        Encontra todas as ocorrências em paralelo.
        """
        if not lista:
            return []
        
        chunk_size = len(lista) // num_workers
        if chunk_size == 0:
            chunk_size = 1
        
        def buscar_todas_chunk(args):
            """Encontra todas ocorrências em um chunk"""
            chunk, item_busca, offset = args
            ocorrencias = []
            for i, valor in enumerate(chunk):
                if valor == item_busca:
                    ocorrencias.append(offset + i)
            return ocorrencias
        
        # Criar chunks
        chunks_com_offset = []
        for i in range(0, len(lista), chunk_size):
            chunk = lista[i:i + chunk_size]
            chunks_com_offset.append((chunk, item, i))
        
        # Buscar em paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            resultados = list(executor.map(buscar_todas_chunk, chunks_com_offset))
        
        # Combinar resultados
        todas_ocorrencias = []
        for ocorrencias in resultados:
            todas_ocorrencias.extend(ocorrencias)
        
        return sorted(todas_ocorrencias)
    
    # Demonstração
    dados_busca = list(range(1000)) + [500] * 10 + list(range(1000, 2000))
    item_busca = 500
    
    pos_seq = dados_busca.index(item_busca)
    pos_par = busca_linear_paralela(dados_busca, item_busca)
    todas_par = busca_linear_todas_ocorrencias(dados_busca, item_busca)
    
    print(f"   Buscando {item_busca} em lista de {len(dados_busca)} elementos:")
    print(f"   → Primeira ocorrência sequencial: {pos_seq}")
    print(f"   → Primeira ocorrência paralela:   {pos_par}")
    print(f"   → Todas ocorrências paralelas:    {len(todas_par)} encontradas")
    print(f"   → Posições: {todas_par[:5]}{'...' if len(todas_par) > 5 else ''}")
    print()
    
    print("2. BUSCA BINÁRIA PARALELA:")
    
    def busca_binaria_paralela_aproximada(lista, item, num_workers=4):
        """
        Busca binária paralela usando múltiplos pontos de partida.
        """
        if not lista:
            return -1
        
        def busca_binaria_range(args):
            """Busca binária em um range específico"""
            arr, item_busca, inicio, fim = args
            
            while inicio <= fim:
                meio = (inicio + fim) // 2
                
                if arr[meio] == item_busca:
                    return meio
                elif arr[meio] < item_busca:
                    inicio = meio + 1
                else:
                    fim = meio - 1
            
            return -1
        
        # Dividir espaço de busca
        chunk_size = len(lista) // num_workers
        ranges = []
        
        for i in range(num_workers):
            inicio = i * chunk_size
            fim = min((i + 1) * chunk_size - 1, len(lista) - 1)
            
            # Ajustar ranges para manter ordenação
            if i > 0 and lista[inicio] == lista[inicio - 1]:
                # Encontrar início real do valor
                while inicio > 0 and lista[inicio] == lista[inicio - 1]:
                    inicio -= 1
            
            ranges.append((lista, item, inicio, fim))
        
        # Buscar em paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            resultados = list(executor.map(busca_binaria_range, ranges))
        
        # Retornar primeiro resultado válido
        for resultado in resultados:
            if resultado != -1:
                return resultado
        
        return -1
    
    print("3. BENCHMARK DE BUSCA PARALELA:")
    
    def benchmark_busca_paralela():
        """Compara performance de busca sequencial vs paralela"""
        
        # Dados de teste
        tamanhos = [10000, 50000, 100000, 500000]
        
        print("   Performance de busca (tempo em ms):")
        print("   ┌─────────────┬─────────────┬─────────────┬─────────────┐")
        print("   │   TAMANHO   │ SEQ. LINEAR │ PAR. LINEAR │   SPEEDUP   │")
        print("   ├─────────────┼─────────────┼─────────────┼─────────────┤")
        
        for tamanho in tamanhos:
            dados = list(range(tamanho))
            item = tamanho // 2  # Item no meio
            
            # Busca sequencial
            start = time.perf_counter()
            pos_seq = dados.index(item)
            tempo_seq = (time.perf_counter() - start) * 1000
            
            # Busca paralela
            start = time.perf_counter()
            pos_par = busca_linear_paralela(dados, item)
            tempo_par = (time.perf_counter() - start) * 1000
            
            speedup = tempo_seq / tempo_par if tempo_par > 0 else 0
            
            print(f"   │ {tamanho:11,} │ {tempo_seq:11.3f} │ {tempo_par:11.3f} │ {speedup:11.2f}x │")
        
        print("   └─────────────┴─────────────┴─────────────┴─────────────┘")
        print()
    
    benchmark_busca_paralela()

def map_reduce_algoritmos():
    """
    Implementa padrão Map-Reduce para algoritmos de ordenação e busca.
    """
    print("=== PADRÃO MAP-REDUCE ===")
    print()
    
    print("1. MAP-REDUCE PARA ORDENAÇÃO:")
    
    def map_reduce_sort(lista, num_mappers=4, num_reducers=2):
        """
        Ordenação usando padrão Map-Reduce.
        """
        if not lista:
            return lista
        
        # FASE MAP: Dividir e ordenar chunks
        def map_phase(chunk):
            """Ordena um chunk de dados"""
            return sorted(chunk)
        
        # Dividir dados em chunks
        chunk_size = len(lista) // num_mappers
        chunks = []
        for i in range(0, len(lista), chunk_size):
            chunks.append(lista[i:i + chunk_size])
        
        # Executar fase MAP em paralelo
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_mappers) as executor:
            chunks_ordenados = list(executor.map(map_phase, chunks))
        
        # FASE SHUFFLE: Redistribuir dados por ranges
        if not chunks_ordenados:
            return []
        
        # Encontrar ranges para redistribuição
        todos_valores = []
        for chunk in chunks_ordenados:
            todos_valores.extend(chunk)
        todos_valores.sort()
        
        # Definir ranges para reducers
        range_size = len(todos_valores) // num_reducers
        ranges = []
        for i in range(num_reducers):
            inicio = i * range_size
            fim = (i + 1) * range_size if i < num_reducers - 1 else len(todos_valores)
            if inicio < len(todos_valores):
                min_val = todos_valores[inicio]
                max_val = todos_valores[fim - 1] if fim <= len(todos_valores) else float('inf')
                ranges.append((min_val, max_val))
        
        # Redistribuir chunks ordenados por ranges
        buckets = [[] for _ in range(num_reducers)]
        for chunk in chunks_ordenados:
            for valor in chunk:
                # Encontrar bucket apropriado
                for i, (min_val, max_val) in enumerate(ranges):
                    if min_val <= valor <= max_val:
                        buckets[i].append(valor)
                        break
        
        # FASE REDUCE: Merge final
        def reduce_phase(bucket):
            """Ordena bucket final"""
            return sorted(bucket)
        
        # Executar fase REDUCE em paralelo
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_reducers) as executor:
            buckets_finais = list(executor.map(reduce_phase, buckets))
        
        # Combinar resultado final
        resultado = []
        for bucket in buckets_finais:
            resultado.extend(bucket)
        
        return resultado
    
    print("2. MAP-REDUCE PARA CONTAGEM:")
    
    def map_reduce_count(lista, num_workers=4):
        """
        Conta ocorrências usando Map-Reduce.
        """
        if not lista:
            return {}
        
        # FASE MAP: Contar em chunks
        def map_count(chunk):
            """Conta ocorrências em um chunk"""
            contagem = {}
            for item in chunk:
                contagem[item] = contagem.get(item, 0) + 1
            return contagem
        
        # Dividir em chunks
        chunk_size = len(lista) // num_workers
        chunks = []
        for i in range(0, len(lista), chunk_size):
            chunks.append(lista[i:i + chunk_size])
        
        # Executar MAP em paralelo
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            contagens_parciais = list(executor.map(map_count, chunks))
        
        # FASE REDUCE: Combinar contagens
        contagem_final = {}
        for contagem in contagens_parciais:
            for item, freq in contagem.items():
                contagem_final[item] = contagem_final.get(item, 0) + freq
        
        return contagem_final
    
    print("3. DEMONSTRAÇÃO E BENCHMARK:")
    
    def demonstrar_map_reduce():
        """Demonstra e compara Map-Reduce"""
        
        # Dados de teste
        dados_ordenacao = [random.randint(1, 1000) for _ in range(10000)]
        dados_contagem = [random.randint(1, 100) for _ in range(50000)]
        
        print("   TESTE DE ORDENAÇÃO:")
        
        # Ordenação sequencial
        start = time.perf_counter()
        resultado_seq = sorted(dados_ordenacao.copy())
        tempo_seq = time.perf_counter() - start
        
        # Ordenação Map-Reduce
        start = time.perf_counter()
        resultado_mr = map_reduce_sort(dados_ordenacao.copy())
        tempo_mr = time.perf_counter() - start
        
        print(f"   → Sequencial:  {tempo_seq*1000:.2f}ms")
        print(f"   → Map-Reduce:  {tempo_mr*1000:.2f}ms")
        print(f"   → Speedup:     {tempo_seq/tempo_mr:.2f}x")
        print(f"   → Correto:     {resultado_seq == resultado_mr}")
        print()
        
        print("   TESTE DE CONTAGEM:")
        
        # Contagem sequencial
        start = time.perf_counter()
        from collections import Counter
        contagem_seq = dict(Counter(dados_contagem))
        tempo_seq = time.perf_counter() - start
        
        # Contagem Map-Reduce
        start = time.perf_counter()
        contagem_mr = map_reduce_count(dados_contagem)
        tempo_mr = time.perf_counter() - start
        
        print(f"   → Sequencial:  {tempo_seq*1000:.2f}ms")
        print(f"   → Map-Reduce:  {tempo_mr*1000:.2f}ms")
        print(f"   → Speedup:     {tempo_seq/tempo_mr:.2f}x")
        print(f"   → Correto:     {contagem_seq == contagem_mr}")
        print()
    
    demonstrar_map_reduce()

if __name__ == "__main__":
    print("MÓDULO 3.8 - ALGORITMOS PARALELOS E DISTRIBUÍDOS")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceitos_paralelizacao()
    print("\n" + "="*50 + "\n")
    
    merge_sort_paralelo()
    print("\n" + "="*50 + "\n")
    
    quick_sort_paralelo()
    print("\n" + "="*50 + "\n")
    
    busca_paralela()
    print("\n" + "="*50 + "\n")
    
    map_reduce_algoritmos()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 3.8 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceitos de paralelização e Lei de Amdahl")
    print("✅ Threading vs Multiprocessing em Python")
    print("✅ Merge Sort e Quick Sort paralelos")
    print("✅ Algoritmos de busca paralela")
    print("✅ Padrão Map-Reduce para big data")
    print("✅ Work-stealing e sincronização")
    print("✅ Análise de speedup e overhead")
    print("✅ Otimizações para arquiteturas multi-core")
    print("✅ Benchmarks de performance paralela")
    print("\n➡️  Próximo: Módulo 3.9 - Casos de Uso Avançados")