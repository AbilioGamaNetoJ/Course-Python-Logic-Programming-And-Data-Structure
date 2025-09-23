"""
MÓDULO 07.3 - COMPLEXIDADE ESPACIAL
===================================

Objetivos de Aprendizado:
- Compreender análise de complexidade espacial
- Dominar conceitos de espaço auxiliar vs espaço total
- Analisar trade-offs entre espaço e tempo
- Implementar técnicas de otimização de memória
- Comparar diferentes abordagens de uso de memória
- Aplicar estratégias de economia de espaço
- Medir e monitorar uso de memória

Conceitos Abordados:
- Complexidade espacial (Space Complexity)
- Espaço auxiliar vs espaço total
- Trade-offs espaço-tempo
- Otimizações de memória
- Estruturas compactas
- Algoritmos in-place
- Garbage collection e gerenciamento de memória
- Análise de vazamentos de memória

Técnicas de Otimização:
- Algoritmos in-place
- Reutilização de estruturas
- Compressão de dados
- Lazy evaluation
- Estruturas bit-wise
- Memory pooling
- Streaming algorithms

Pré-requisitos:
- Notação Big O
- Estruturas de dados básicas
- Análise de algoritmos
- Conceitos de memória
"""

import sys
import gc
import time
import psutil
import os
import tracemalloc
from typing import List, Tuple, Optional, Any, Iterator, Dict
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import numpy as np
import matplotlib.pyplot as plt


class TipoEspaco(Enum):
    """Tipos de análise de espaço."""
    AUXILIAR = "Espaço Auxiliar"
    TOTAL = "Espaço Total"
    IN_PLACE = "In-Place"
    CONSTANTE = "Espaço Constante"


@dataclass
class MedicaoMemoria:
    """Medição de uso de memória."""
    nome: str
    memoria_inicial: int
    memoria_final: int
    memoria_pico: int
    memoria_auxiliar: int
    tempo_execucao: float
    observacoes: str = ""
    
    @property
    def memoria_usada(self) -> int:
        """Memória total usada."""
        return self.memoria_final - self.memoria_inicial
    
    @property
    def eficiencia_espacial(self) -> float:
        """Eficiência espacial (MB/segundo)."""
        if self.tempo_execucao > 0:
            return (self.memoria_usada / 1024 / 1024) / self.tempo_execucao
        return 0.0


@dataclass
class ResultadoAnaliseEspacial:
    """Resultado da análise de complexidade espacial."""
    algoritmo: str
    tipo_espaco: TipoEspaco
    medicoes: List[MedicaoMemoria] = field(default_factory=list)
    complexidade_teorica: str = ""
    complexidade_empirica: str = ""
    trade_offs: str = ""
    otimizacoes: List[str] = field(default_factory=list)


class AnalisadorEspacial:
    """
    Classe para análise de complexidade espacial.
    """
    
    def __init__(self):
        """Inicializa o analisador espacial."""
        self.resultados: List[ResultadoAnaliseEspacial] = []
        self.processo = psutil.Process(os.getpid())
    
    def medir_memoria(self, func, *args, nome: str = "", **kwargs) -> MedicaoMemoria:
        """
        Mede uso de memória de uma função.
        
        Args:
            func: Função a ser medida
            *args: Argumentos da função
            nome: Nome da medição
            **kwargs: Argumentos nomeados da função
        
        Returns:
            Medição de memória
        """
        # Forçar garbage collection antes da medição
        gc.collect()
        
        # Iniciar rastreamento de memória
        tracemalloc.start()
        memoria_inicial = self.processo.memory_info().rss
        
        inicio = time.perf_counter()
        
        try:
            resultado = func(*args, **kwargs)
        except Exception as e:
            resultado = None
            observacoes = f"Erro: {str(e)}"
        else:
            observacoes = ""
        
        fim = time.perf_counter()
        tempo_execucao = fim - inicio
        
        # Obter estatísticas de memória
        memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        memoria_final = self.processo.memory_info().rss
        
        return MedicaoMemoria(
            nome=nome or func.__name__,
            memoria_inicial=memoria_inicial,
            memoria_final=memoria_final,
            memoria_pico=memoria_pico,
            memoria_auxiliar=memoria_pico,
            tempo_execucao=tempo_execucao,
            observacoes=observacoes
        )
    
    def analisar_crescimento_espacial(self, func, tamanhos: List[int], 
                                    nome: str = "") -> ResultadoAnaliseEspacial:
        """
        Analisa crescimento espacial com diferentes tamanhos de entrada.
        
        Args:
            func: Função que recebe tamanho como parâmetro
            tamanhos: Lista de tamanhos para testar
            nome: Nome da análise
        
        Returns:
            Resultado da análise espacial
        """
        medicoes = []
        
        for n in tamanhos:
            medicao = self.medir_memoria(func, n, nome=f"{nome}_n{n}")
            medicoes.append(medicao)
        
        # Determinar complexidade empírica
        complexidade_empirica = self._determinar_complexidade(
            tamanhos, [m.memoria_auxiliar for m in medicoes]
        )
        
        resultado = ResultadoAnaliseEspacial(
            algoritmo=nome or func.__name__,
            tipo_espaco=TipoEspaco.AUXILIAR,
            medicoes=medicoes,
            complexidade_empirica=complexidade_empirica
        )
        
        self.resultados.append(resultado)
        return resultado
    
    def _determinar_complexidade(self, tamanhos: List[int], 
                                memorias: List[int]) -> str:
        """
        Determina complexidade empírica baseada nos dados.
        
        Args:
            tamanhos: Tamanhos de entrada
            memorias: Uso de memória correspondente
        
        Returns:
            String descrevendo a complexidade
        """
        if len(tamanhos) < 2:
            return "Dados insuficientes"
        
        # Calcular razões de crescimento
        razoes = []
        for i in range(1, len(tamanhos)):
            if memorias[i-1] > 0:
                razao_memoria = memorias[i] / memorias[i-1]
                razao_tamanho = tamanhos[i] / tamanhos[i-1]
                razoes.append(razao_memoria / razao_tamanho)
        
        if not razoes:
            return "Não determinado"
        
        razao_media = sum(razoes) / len(razoes)
        
        if razao_media < 1.1:
            return "O(1) - Constante"
        elif razao_media < 1.5:
            return "O(log n) - Logarítmica"
        elif razao_media < 2.5:
            return "O(n) - Linear"
        elif razao_media < 5:
            return "O(n log n) - Linearítmica"
        else:
            return "O(n²) ou superior - Polinomial/Exponencial"
    
    def plotar_analise_espacial(self, resultado: ResultadoAnaliseEspacial):
        """
        Plota gráfico da análise espacial.
        
        Args:
            resultado: Resultado da análise
        """
        if not resultado.medicoes:
            return
        
        # Extrair dados para plotagem
        tamanhos = list(range(len(resultado.medicoes)))
        memorias_auxiliar = [m.memoria_auxiliar / 1024 / 1024 for m in resultado.medicoes]  # MB
        tempos = [m.tempo_execucao * 1000 for m in resultado.medicoes]  # ms
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        # Gráfico 1: Uso de memória
        ax1.plot(tamanhos, memorias_auxiliar, 'b-o', label='Memória Auxiliar')
        ax1.set_xlabel('Tamanho da Entrada')
        ax1.set_ylabel('Memória (MB)')
        ax1.set_title(f'Análise Espacial: {resultado.algoritmo}')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Gráfico 2: Tempo de execução
        ax2.plot(tamanhos, tempos, 'r-s', label='Tempo de Execução')
        ax2.set_xlabel('Tamanho da Entrada')
        ax2.set_ylabel('Tempo (ms)')
        ax2.set_title('Tempo de Execução')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Gráfico 3: Trade-off espaço-tempo
        ax3.scatter(memorias_auxiliar, tempos, c='green', alpha=0.7)
        ax3.set_xlabel('Memória (MB)')
        ax3.set_ylabel('Tempo (ms)')
        ax3.set_title('Trade-off Espaço-Tempo')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()


class AlgoritmosEspaciais:
    """
    Implementações de algoritmos com diferentes complexidades espaciais.
    """
    
    @staticmethod
    def ordenacao_bubble_inplace(arr: List[int]) -> List[int]:
        """
        Bubble sort in-place - O(1) espaço auxiliar.
        
        Args:
            arr: Lista a ser ordenada
        
        Returns:
            Lista ordenada (mesma referência)
        """
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    @staticmethod
    def ordenacao_merge_recursiva(arr: List[int]) -> List[int]:
        """
        Merge sort recursivo - O(n) espaço auxiliar.
        
        Args:
            arr: Lista a ser ordenada
        
        Returns:
            Nova lista ordenada
        """
        if len(arr) <= 1:
            return arr[:]
        
        meio = len(arr) // 2
        esquerda = AlgoritmosEspaciais.ordenacao_merge_recursiva(arr[:meio])
        direita = AlgoritmosEspaciais.ordenacao_merge_recursiva(arr[meio:])
        
        return AlgoritmosEspaciais._merge(esquerda, direita)
    
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
        """
        Fibonacci recursivo - O(n) espaço na pilha.
        
        Args:
            n: Posição na sequência
        
        Returns:
            Valor de Fibonacci
        """
        if n <= 1:
            return n
        return (AlgoritmosEspaciais.fibonacci_recursivo(n-1) + 
                AlgoritmosEspaciais.fibonacci_recursivo(n-2))
    
    @staticmethod
    def fibonacci_iterativo(n: int) -> int:
        """
        Fibonacci iterativo - O(1) espaço auxiliar.
        
        Args:
            n: Posição na sequência
        
        Returns:
            Valor de Fibonacci
        """
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    @staticmethod
    def fibonacci_memoizado(n: int, memo: Optional[Dict[int, int]] = None) -> int:
        """
        Fibonacci com memoização - O(n) espaço auxiliar.
        
        Args:
            n: Posição na sequência
            memo: Dicionário de memoização
        
        Returns:
            Valor de Fibonacci
        """
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return n
        
        memo[n] = (AlgoritmosEspaciais.fibonacci_memoizado(n-1, memo) + 
                   AlgoritmosEspaciais.fibonacci_memoizado(n-2, memo))
        return memo[n]
    
    @staticmethod
    def busca_dfs_recursiva(grafo: Dict[int, List[int]], inicio: int, 
                           visitados: Optional[set] = None) -> List[int]:
        """
        DFS recursiva - O(V) espaço na pilha + visitados.
        
        Args:
            grafo: Grafo representado como dicionário
            inicio: Vértice inicial
            visitados: Conjunto de vértices visitados
        
        Returns:
            Lista de vértices na ordem de visita
        """
        if visitados is None:
            visitados = set()
        
        resultado = []
        if inicio not in visitados:
            visitados.add(inicio)
            resultado.append(inicio)
            
            for vizinho in grafo.get(inicio, []):
                resultado.extend(
                    AlgoritmosEspaciais.busca_dfs_recursiva(grafo, vizinho, visitados)
                )
        
        return resultado
    
    @staticmethod
    def busca_dfs_iterativa(grafo: Dict[int, List[int]], inicio: int) -> List[int]:
        """
        DFS iterativa - O(V) espaço para pilha explícita.
        
        Args:
            grafo: Grafo representado como dicionário
            inicio: Vértice inicial
        
        Returns:
            Lista de vértices na ordem de visita
        """
        visitados = set()
        pilha = [inicio]
        resultado = []
        
        while pilha:
            vertice = pilha.pop()
            if vertice not in visitados:
                visitados.add(vertice)
                resultado.append(vertice)
                
                # Adicionar vizinhos à pilha (em ordem reversa para manter ordem)
                for vizinho in reversed(grafo.get(vertice, [])):
                    if vizinho not in visitados:
                        pilha.append(vizinho)
        
        return resultado
    
    @staticmethod
    def matriz_multiplicacao_naive(A: List[List[int]], 
                                  B: List[List[int]]) -> List[List[int]]:
        """
        Multiplicação de matrizes naive - O(n²) espaço auxiliar.
        
        Args:
            A: Primeira matriz
            B: Segunda matriz
        
        Returns:
            Matriz resultado
        """
        n = len(A)
        m = len(B[0])
        p = len(B)
        
        C = [[0] * m for _ in range(n)]
        
        for i in range(n):
            for j in range(m):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        
        return C
    
    @staticmethod
    def matriz_multiplicacao_otimizada(A: List[List[int]], 
                                     B: List[List[int]]) -> List[List[int]]:
        """
        Multiplicação de matrizes com otimização de cache.
        
        Args:
            A: Primeira matriz
            B: Segunda matriz
        
        Returns:
            Matriz resultado
        """
        n = len(A)
        m = len(B[0])
        p = len(B)
        
        # Transpor B para melhor localidade de cache
        B_T = [[B[j][i] for j in range(p)] for i in range(m)]
        
        C = [[0] * m for _ in range(n)]
        
        for i in range(n):
            for j in range(m):
                soma = 0
                for k in range(p):
                    soma += A[i][k] * B_T[j][k]
                C[i][j] = soma
        
        return C


class EstruturasCompactas:
    """
    Implementações de estruturas de dados compactas.
    """
    
    class BitArray:
        """Array de bits para economia de espaço."""
        
        def __init__(self, tamanho: int):
            """
            Inicializa array de bits.
            
            Args:
                tamanho: Número de bits
            """
            self.tamanho = tamanho
            self.num_bytes = (tamanho + 7) // 8
            self.dados = bytearray(self.num_bytes)
        
        def set_bit(self, posicao: int, valor: bool):
            """
            Define valor de um bit.
            
            Args:
                posicao: Posição do bit
                valor: Valor do bit (True/False)
            """
            if 0 <= posicao < self.tamanho:
                byte_idx = posicao // 8
                bit_idx = posicao % 8
                
                if valor:
                    self.dados[byte_idx] |= (1 << bit_idx)
                else:
                    self.dados[byte_idx] &= ~(1 << bit_idx)
        
        def get_bit(self, posicao: int) -> bool:
            """
            Obtém valor de um bit.
            
            Args:
                posicao: Posição do bit
            
            Returns:
                Valor do bit
            """
            if 0 <= posicao < self.tamanho:
                byte_idx = posicao // 8
                bit_idx = posicao % 8
                return bool(self.dados[byte_idx] & (1 << bit_idx))
            return False
        
        def memoria_usada(self) -> int:
            """Retorna memória usada em bytes."""
            return self.num_bytes
        
        def comparar_com_lista(self, tamanho: int) -> Tuple[int, int]:
            """
            Compara uso de memória com lista de booleans.
            
            Args:
                tamanho: Tamanho para comparação
            
            Returns:
                Tupla (memoria_bitarray, memoria_lista)
            """
            bitarray_memoria = (tamanho + 7) // 8
            lista_memoria = tamanho * sys.getsizeof(True)
            return bitarray_memoria, lista_memoria
    
    class BloomFilter:
        """Filtro de Bloom para testes de pertinência probabilísticos."""
        
        def __init__(self, tamanho: int, num_hash: int):
            """
            Inicializa filtro de Bloom.
            
            Args:
                tamanho: Tamanho do array de bits
                num_hash: Número de funções hash
            """
            self.tamanho = tamanho
            self.num_hash = num_hash
            self.bit_array = EstruturasCompactas.BitArray(tamanho)
            self.num_elementos = 0
        
        def _hash(self, item: Any, seed: int) -> int:
            """Função hash com seed."""
            return hash((item, seed)) % self.tamanho
        
        def adicionar(self, item: Any):
            """
            Adiciona item ao filtro.
            
            Args:
                item: Item a ser adicionado
            """
            for i in range(self.num_hash):
                posicao = self._hash(item, i)
                self.bit_array.set_bit(posicao, True)
            self.num_elementos += 1
        
        def pode_conter(self, item: Any) -> bool:
            """
            Verifica se item pode estar no conjunto.
            
            Args:
                item: Item a verificar
            
            Returns:
                True se pode conter, False se definitivamente não contém
            """
            for i in range(self.num_hash):
                posicao = self._hash(item, i)
                if not self.bit_array.get_bit(posicao):
                    return False
            return True
        
        def taxa_falso_positivo(self) -> float:
            """
            Calcula taxa teórica de falsos positivos.
            
            Returns:
                Taxa de falsos positivos
            """
            if self.num_elementos == 0:
                return 0.0
            
            # Fórmula: (1 - e^(-k*n/m))^k
            # k = num_hash, n = num_elementos, m = tamanho
            import math
            k = self.num_hash
            n = self.num_elementos
            m = self.tamanho
            
            return (1 - math.exp(-k * n / m)) ** k
    
    class SparseMatrix:
        """Matriz esparsa usando dicionário."""
        
        def __init__(self, linhas: int, colunas: int):
            """
            Inicializa matriz esparsa.
            
            Args:
                linhas: Número de linhas
                colunas: Número de colunas
            """
            self.linhas = linhas
            self.colunas = colunas
            self.dados = {}  # (linha, coluna) -> valor
        
        def set(self, linha: int, coluna: int, valor: Any):
            """
            Define valor em posição específica.
            
            Args:
                linha: Linha da matriz
                coluna: Coluna da matriz
                valor: Valor a definir
            """
            if valor != 0:  # Só armazenar valores não-zero
                self.dados[(linha, coluna)] = valor
            elif (linha, coluna) in self.dados:
                del self.dados[(linha, coluna)]
        
        def get(self, linha: int, coluna: int) -> Any:
            """
            Obtém valor de posição específica.
            
            Args:
                linha: Linha da matriz
                coluna: Coluna da matriz
            
            Returns:
                Valor na posição (0 se não definido)
            """
            return self.dados.get((linha, coluna), 0)
        
        def memoria_usada(self) -> int:
            """Retorna estimativa de memória usada."""
            return len(self.dados) * (sys.getsizeof((0, 0)) + sys.getsizeof(0))
        
        def comparar_com_matriz_densa(self) -> Tuple[int, int]:
            """
            Compara uso de memória com matriz densa.
            
            Returns:
                Tupla (memoria_esparsa, memoria_densa)
            """
            memoria_esparsa = self.memoria_usada()
            memoria_densa = self.linhas * self.colunas * sys.getsizeof(0)
            return memoria_esparsa, memoria_densa


class StreamingAlgorithms:
    """
    Algoritmos para processamento de streams com espaço limitado.
    """
    
    class CountMinSketch:
        """Count-Min Sketch para estimativa de frequências."""
        
        def __init__(self, largura: int, profundidade: int):
            """
            Inicializa Count-Min Sketch.
            
            Args:
                largura: Largura da tabela hash
                profundidade: Número de funções hash
            """
            self.largura = largura
            self.profundidade = profundidade
            self.tabela = [[0] * largura for _ in range(profundidade)]
        
        def _hash(self, item: Any, linha: int) -> int:
            """Função hash para linha específica."""
            return hash((item, linha)) % self.largura
        
        def incrementar(self, item: Any, count: int = 1):
            """
            Incrementa contador para item.
            
            Args:
                item: Item a incrementar
                count: Valor do incremento
            """
            for i in range(self.profundidade):
                coluna = self._hash(item, i)
                self.tabela[i][coluna] += count
        
        def estimar(self, item: Any) -> int:
            """
            Estima frequência de um item.
            
            Args:
                item: Item a estimar
            
            Returns:
                Estimativa da frequência
            """
            estimativas = []
            for i in range(self.profundidade):
                coluna = self._hash(item, i)
                estimativas.append(self.tabela[i][coluna])
            return min(estimativas)
    
    class ReservoirSampling:
        """Amostragem de reservatório para streams."""
        
        def __init__(self, tamanho_amostra: int):
            """
            Inicializa amostragem de reservatório.
            
            Args:
                tamanho_amostra: Tamanho da amostra a manter
            """
            self.tamanho_amostra = tamanho_amostra
            self.reservatorio = []
            self.num_elementos = 0
        
        def processar_elemento(self, elemento: Any):
            """
            Processa novo elemento do stream.
            
            Args:
                elemento: Elemento a processar
            """
            self.num_elementos += 1
            
            if len(self.reservatorio) < self.tamanho_amostra:
                self.reservatorio.append(elemento)
            else:
                # Substituir elemento aleatório
                import random
                j = random.randint(0, self.num_elementos - 1)
                if j < self.tamanho_amostra:
                    self.reservatorio[j] = elemento
        
        def obter_amostra(self) -> List[Any]:
            """
            Obtém amostra atual.
            
            Returns:
                Lista com amostra atual
            """
            return self.reservatorio.copy()


# Funções de Demonstração
def demonstrar_complexidade_espacial_basica():
    """Demonstra conceitos básicos de complexidade espacial."""
    print("=== DEMONSTRAÇÃO: COMPLEXIDADE ESPACIAL BÁSICA ===\n")
    
    analisador = AnalisadorEspacial()
    
    print("1. COMPARAÇÃO: FIBONACCI RECURSIVO vs ITERATIVO")
    
    # Fibonacci recursivo (O(n) espaço na pilha)
    def teste_fib_recursivo(n):
        return AlgoritmosEspaciais.fibonacci_recursivo(n)
    
    # Fibonacci iterativo (O(1) espaço auxiliar)
    def teste_fib_iterativo(n):
        return AlgoritmosEspaciais.fibonacci_iterativo(n)
    
    # Testar com diferentes valores
    valores = [10, 15, 20, 25]
    
    print("   Fibonacci Recursivo (O(n) espaço):")
    for n in valores:
        medicao = analisador.medir_memoria(teste_fib_recursivo, n, nome=f"fib_rec_{n}")
        print(f"   n={n:2d}: {medicao.memoria_auxiliar/1024:.1f} KB, "
              f"{medicao.tempo_execucao*1000:.2f} ms")
    
    print("\n   Fibonacci Iterativo (O(1) espaço):")
    for n in valores:
        medicao = analisador.medir_memoria(teste_fib_iterativo, n, nome=f"fib_iter_{n}")
        print(f"   n={n:2d}: {medicao.memoria_auxiliar/1024:.1f} KB, "
              f"{medicao.tempo_execucao*1000:.2f} ms")
    
    print("\n2. COMPARAÇÃO: ORDENAÇÃO IN-PLACE vs COM ESPAÇO AUXILIAR")
    
    # Gerar dados de teste
    import random
    tamanhos = [100, 500, 1000, 2000]
    
    print("   Bubble Sort In-Place (O(1) espaço):")
    for n in tamanhos:
        dados = [random.randint(1, 1000) for _ in range(n)]
        medicao = analisador.medir_memoria(
            AlgoritmosEspaciais.ordenacao_bubble_inplace, 
            dados.copy(), nome=f"bubble_{n}"
        )
        print(f"   n={n:4d}: {medicao.memoria_auxiliar/1024:.1f} KB, "
              f"{medicao.tempo_execucao*1000:.1f} ms")
    
    print("\n   Merge Sort Recursivo (O(n) espaço):")
    for n in tamanhos:
        dados = [random.randint(1, 1000) for _ in range(n)]
        medicao = analisador.medir_memoria(
            AlgoritmosEspaciais.ordenacao_merge_recursiva, 
            dados, nome=f"merge_{n}"
        )
        print(f"   n={n:4d}: {medicao.memoria_auxiliar/1024:.1f} KB, "
              f"{medicao.tempo_execucao*1000:.1f} ms")


def demonstrar_estruturas_compactas():
    """Demonstra estruturas de dados compactas."""
    print("\n=== DEMONSTRAÇÃO: ESTRUTURAS COMPACTAS ===\n")
    
    print("1. BIT ARRAY vs LISTA DE BOOLEANS")
    
    tamanhos = [1000, 10000, 100000, 1000000]
    
    for n in tamanhos:
        bit_array = EstruturasCompactas.BitArray(n)
        memoria_bit, memoria_lista = bit_array.comparar_com_lista(n)
        economia = (1 - memoria_bit / memoria_lista) * 100
        
        print(f"   n={n:7d}: BitArray={memoria_bit:8d} bytes, "
              f"Lista={memoria_lista:8d} bytes, Economia={economia:.1f}%")
    
    print("\n2. BLOOM FILTER")
    
    # Criar Bloom Filter
    bloom = EstruturasCompactas.BloomFilter(tamanho=10000, num_hash=3)
    
    # Adicionar elementos
    elementos = [f"item_{i}" for i in range(1000)]
    for item in elementos:
        bloom.adicionar(item)
    
    # Testar elementos
    verdadeiros_positivos = sum(1 for item in elementos if bloom.pode_conter(item))
    
    # Testar elementos não adicionados
    elementos_teste = [f"teste_{i}" for i in range(1000)]
    falsos_positivos = sum(1 for item in elementos_teste if bloom.pode_conter(item))
    
    taxa_fp_teorica = bloom.taxa_falso_positivo()
    taxa_fp_empirica = falsos_positivos / len(elementos_teste)
    
    print(f"   Elementos adicionados: {len(elementos)}")
    print(f"   Verdadeiros positivos: {verdadeiros_positivos}/{len(elementos)}")
    print(f"   Falsos positivos: {falsos_positivos}/{len(elementos_teste)}")
    print(f"   Taxa FP teórica: {taxa_fp_teorica:.3f}")
    print(f"   Taxa FP empírica: {taxa_fp_empirica:.3f}")
    print(f"   Memória usada: {bloom.bit_array.memoria_usada()} bytes")
    
    print("\n3. MATRIZ ESPARSA")
    
    # Criar matriz esparsa 1000x1000 com poucos elementos
    matriz = EstruturasCompactas.SparseMatrix(1000, 1000)
    
    # Adicionar alguns elementos não-zero
    import random
    for _ in range(100):
        linha = random.randint(0, 999)
        coluna = random.randint(0, 999)
        valor = random.randint(1, 100)
        matriz.set(linha, coluna, valor)
    
    memoria_esparsa, memoria_densa = matriz.comparar_com_matriz_densa()
    economia = (1 - memoria_esparsa / memoria_densa) * 100
    
    print(f"   Matriz 1000x1000 com 100 elementos não-zero:")
    print(f"   Matriz esparsa: {memoria_esparsa:8d} bytes")
    print(f"   Matriz densa:   {memoria_densa:8d} bytes")
    print(f"   Economia: {economia:.1f}%")


def demonstrar_streaming_algorithms():
    """Demonstra algoritmos de streaming."""
    print("\n=== DEMONSTRAÇÃO: ALGORITMOS DE STREAMING ===\n")
    
    print("1. COUNT-MIN SKETCH")
    
    # Criar Count-Min Sketch
    cms = StreamingAlgorithms.CountMinSketch(largura=1000, profundidade=5)
    
    # Simular stream de dados
    import random
    stream = []
    frequencias_reais = {}
    
    # Gerar stream com distribuição zipfiana
    for _ in range(10000):
        # Distribuição onde alguns itens são muito mais frequentes
        if random.random() < 0.1:
            item = f"popular_{random.randint(1, 10)}"
        else:
            item = f"raro_{random.randint(1, 1000)}"
        
        stream.append(item)
        frequencias_reais[item] = frequencias_reais.get(item, 0) + 1
        cms.incrementar(item)
    
    # Testar estimativas
    print("   Comparação de frequências (reais vs estimadas):")
    itens_teste = sorted(frequencias_reais.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for item, freq_real in itens_teste:
        freq_estimada = cms.estimar(item)
        erro = abs(freq_estimada - freq_real) / freq_real * 100
        print(f"   {item:15s}: Real={freq_real:4d}, Estimada={freq_estimada:4d}, "
              f"Erro={erro:.1f}%")
    
    print("\n2. RESERVOIR SAMPLING")
    
    # Criar reservoir sampling
    reservoir = StreamingAlgorithms.ReservoirSampling(tamanho_amostra=100)
    
    # Simular stream grande
    stream_size = 10000
    for i in range(stream_size):
        reservoir.processar_elemento(f"elemento_{i}")
    
    amostra = reservoir.obter_amostra()
    
    print(f"   Stream processado: {stream_size} elementos")
    print(f"   Tamanho da amostra: {len(amostra)}")
    print(f"   Primeiros 10 elementos da amostra: {amostra[:10]}")
    print(f"   Memória usada: ~{len(amostra) * sys.getsizeof('elemento_0')} bytes")
    print(f"   Vs. armazenar tudo: ~{stream_size * sys.getsizeof('elemento_0')} bytes")


def demonstrar_trade_offs_espaco_tempo():
    """Demonstra trade-offs entre espaço e tempo."""
    print("\n=== DEMONSTRAÇÃO: TRADE-OFFS ESPAÇO-TEMPO ===\n")
    
    analisador = AnalisadorEspacial()
    
    print("1. FIBONACCI: RECURSIVO vs MEMOIZADO vs ITERATIVO")
    
    n = 30
    
    # Fibonacci recursivo (exponencial em tempo, linear em espaço)
    medicao_rec = analisador.medir_memoria(
        AlgoritmosEspaciais.fibonacci_recursivo, n, nome="fib_recursivo"
    )
    
    # Fibonacci memoizado (linear em tempo, linear em espaço)
    medicao_memo = analisador.medir_memoria(
        AlgoritmosEspaciais.fibonacci_memoizado, n, nome="fib_memoizado"
    )
    
    # Fibonacci iterativo (linear em tempo, constante em espaço)
    medicao_iter = analisador.medir_memoria(
        AlgoritmosEspaciais.fibonacci_iterativo, n, nome="fib_iterativo"
    )
    
    print(f"   Fibonacci({n}):")
    print(f"   Recursivo:  Tempo={medicao_rec.tempo_execucao*1000:8.2f}ms, "
          f"Memória={medicao_rec.memoria_auxiliar/1024:6.1f}KB")
    print(f"   Memoizado:  Tempo={medicao_memo.tempo_execucao*1000:8.2f}ms, "
          f"Memória={medicao_memo.memoria_auxiliar/1024:6.1f}KB")
    print(f"   Iterativo:  Tempo={medicao_iter.tempo_execucao*1000:8.2f}ms, "
          f"Memória={medicao_iter.memoria_auxiliar/1024:6.1f}KB")
    
    print("\n2. BUSCA EM GRAFO: DFS RECURSIVA vs ITERATIVA")
    
    # Criar grafo de teste
    grafo = {}
    for i in range(100):
        grafo[i] = [j for j in range(max(0, i-2), min(100, i+3)) if j != i]
    
    # DFS recursiva
    medicao_dfs_rec = analisador.medir_memoria(
        AlgoritmosEspaciais.busca_dfs_recursiva, grafo, 0, nome="dfs_recursiva"
    )
    
    # DFS iterativa
    medicao_dfs_iter = analisador.medir_memoria(
        AlgoritmosEspaciais.busca_dfs_iterativa, grafo, 0, nome="dfs_iterativa"
    )
    
    print(f"   DFS em grafo com 100 vértices:")
    print(f"   Recursiva:  Tempo={medicao_dfs_rec.tempo_execucao*1000:6.2f}ms, "
          f"Memória={medicao_dfs_rec.memoria_auxiliar/1024:6.1f}KB")
    print(f"   Iterativa:  Tempo={medicao_dfs_iter.tempo_execucao*1000:6.2f}ms, "
          f"Memória={medicao_dfs_iter.memoria_auxiliar/1024:6.1f}KB")
    
    print("\n3. MULTIPLICAÇÃO DE MATRIZES: NAIVE vs OTIMIZADA")
    
    # Criar matrizes de teste
    n = 100
    A = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    
    # Multiplicação naive
    medicao_naive = analisador.medir_memoria(
        AlgoritmosEspaciais.matriz_multiplicacao_naive, A, B, nome="mult_naive"
    )
    
    # Multiplicação otimizada
    medicao_otim = analisador.medir_memoria(
        AlgoritmosEspaciais.matriz_multiplicacao_otimizada, A, B, nome="mult_otimizada"
    )
    
    print(f"   Multiplicação de matrizes {n}x{n}:")
    print(f"   Naive:      Tempo={medicao_naive.tempo_execucao*1000:6.1f}ms, "
          f"Memória={medicao_naive.memoria_auxiliar/1024:6.1f}KB")
    print(f"   Otimizada:  Tempo={medicao_otim.tempo_execucao*1000:6.1f}ms, "
          f"Memória={medicao_otim.memoria_auxiliar/1024:6.1f}KB")


def demonstrar_tecnicas_otimizacao():
    """Demonstra técnicas de otimização de memória."""
    print("\n=== DEMONSTRAÇÃO: TÉCNICAS DE OTIMIZAÇÃO ===\n")
    
    print("1. LAZY EVALUATION")
    
    class LazyRange:
        """Implementação lazy de range."""
        
        def __init__(self, start, stop, step=1):
            self.start = start
            self.stop = stop
            self.step = step
        
        def __iter__(self):
            current = self.start
            while current < self.stop:
                yield current
                current += self.step
    
    # Comparar memória: lista vs lazy range
    n = 1000000
    
    # Lista completa (eager)
    lista_completa = list(range(n))
    memoria_lista = sys.getsizeof(lista_completa)
    
    # Lazy range
    lazy_range = LazyRange(0, n)
    memoria_lazy = sys.getsizeof(lazy_range)
    
    print(f"   Range de {n} elementos:")
    print(f"   Lista completa: {memoria_lista/1024/1024:.1f} MB")
    print(f"   Lazy range:     {memoria_lazy} bytes")
    print(f"   Economia:       {(1 - memoria_lazy/memoria_lista)*100:.1f}%")
    
    print("\n2. GENERATOR EXPRESSIONS")
    
    # List comprehension vs generator expression
    n = 100000
    
    # List comprehension (eager)
    lista_quadrados = [x**2 for x in range(n)]
    memoria_lista = sys.getsizeof(lista_quadrados)
    
    # Generator expression (lazy)
    gen_quadrados = (x**2 for x in range(n))
    memoria_gen = sys.getsizeof(gen_quadrados)
    
    print(f"   Quadrados de {n} números:")
    print(f"   List comprehension: {memoria_lista/1024:.1f} KB")
    print(f"   Generator:          {memoria_gen} bytes")
    print(f"   Economia:           {(1 - memoria_gen/memoria_lista)*100:.1f}%")
    
    print("\n3. OBJECT POOLING")
    
    class ObjectPool:
        """Pool de objetos para reutilização."""
        
        def __init__(self, factory, max_size=10):
            self.factory = factory
            self.max_size = max_size
            self.pool = []
        
        def get_object(self):
            if self.pool:
                return self.pool.pop()
            return self.factory()
        
        def return_object(self, obj):
            if len(self.pool) < self.max_size:
                # Reset object state if needed
                self.pool.append(obj)
    
    # Exemplo de uso
    class ExpensiveObject:
        def __init__(self):
            self.data = [0] * 1000  # Simular objeto custoso
    
    pool = ObjectPool(ExpensiveObject, max_size=5)
    
    print(f"   Object Pool criado com tamanho máximo: {pool.max_size}")
    print(f"   Objetos no pool: {len(pool.pool)}")
    
    # Usar objetos do pool
    objetos = []
    for i in range(10):
        obj = pool.get_object()
        objetos.append(obj)
    
    print(f"   Após retirar 10 objetos: {len(pool.pool)} no pool")
    
    # Retornar objetos ao pool
    for obj in objetos[:5]:
        pool.return_object(obj)
    
    print(f"   Após retornar 5 objetos: {len(pool.pool)} no pool")


def benchmark_complexidade_espacial():
    """Benchmark de diferentes complexidades espaciais."""
    print("\n=== BENCHMARK: COMPLEXIDADE ESPACIAL ===\n")
    
    analisador = AnalisadorEspacial()
    
    print("Comparação de algoritmos com diferentes complexidades espaciais:")
    print("(Tempo em ms, Memória em KB)")
    print()
    
    tamanhos = [100, 500, 1000, 2000]
    
    for n in tamanhos:
        print(f"n = {n}:")
        
        # Algoritmo O(1) espaço - Fibonacci iterativo
        medicao_o1 = analisador.medir_memoria(
            AlgoritmosEspaciais.fibonacci_iterativo, min(n, 40), nome=f"O1_{n}"
        )
        
        # Algoritmo O(log n) espaço - Busca binária (simulada)
        def busca_binaria_recursiva(arr, target, inicio=0, fim=None):
            if fim is None:
                fim = len(arr) - 1
            if inicio > fim:
                return -1
            meio = (inicio + fim) // 2
            if arr[meio] == target:
                return meio
            elif arr[meio] > target:
                return busca_binaria_recursiva(arr, target, inicio, meio - 1)
            else:
                return busca_binaria_recursiva(arr, target, meio + 1, fim)
        
        arr_teste = list(range(n))
        medicao_olog = analisador.medir_memoria(
            busca_binaria_recursiva, arr_teste, n//2, nome=f"Olog_{n}"
        )
        
        # Algoritmo O(n) espaço - Merge sort
        dados_teste = list(range(n, 0, -1))
        medicao_on = analisador.medir_memoria(
            AlgoritmosEspaciais.ordenacao_merge_recursiva, dados_teste, nome=f"On_{n}"
        )
        
        print(f"   O(1):      Tempo={medicao_o1.tempo_execucao*1000:6.2f}ms, "
              f"Memória={medicao_o1.memoria_auxiliar/1024:6.1f}KB")
        print(f"   O(log n):  Tempo={medicao_olog.tempo_execucao*1000:6.2f}ms, "
              f"Memória={medicao_olog.memoria_auxiliar/1024:6.1f}KB")
        print(f"   O(n):      Tempo={medicao_on.tempo_execucao*1000:6.2f}ms, "
              f"Memória={medicao_on.memoria_auxiliar/1024:6.1f}KB")
        print()


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 07.3 - COMPLEXIDADE ESPACIAL")
    print("=" * 50)
    
    demonstrar_complexidade_espacial_basica()
    demonstrar_estruturas_compactas()
    demonstrar_streaming_algorithms()
    demonstrar_trade_offs_espaco_tempo()
    demonstrar_tecnicas_otimizacao()
    benchmark_complexidade_espacial()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 07.3")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. CONCEITOS FUNDAMENTAIS:
   • Complexidade espacial mede uso de memória
   • Espaço auxiliar vs espaço total
   • Trade-offs entre espaço e tempo
   • Algoritmos in-place vs com espaço auxiliar

2. CLASSES DE COMPLEXIDADE ESPACIAL:
   • O(1): Espaço constante (algoritmos in-place)
   • O(log n): Espaço logarítmico (recursão balanceada)
   • O(n): Espaço linear (cópia de dados)
   • O(n²): Espaço quadrático (matrizes auxiliares)

3. ESTRUTURAS COMPACTAS:
   • Bit Arrays: economia de 8x em arrays de booleans
   • Bloom Filters: testes probabilísticos de pertinência
   • Matrizes Esparsas: economia significativa para dados esparsos
   • Count-Min Sketch: estimativas de frequência em streams

4. TÉCNICAS DE OTIMIZAÇÃO:
   • Lazy Evaluation: computação sob demanda
   • Generator Expressions: iteração sem armazenamento
   • Object Pooling: reutilização de objetos custosos
   • Streaming Algorithms: processamento com espaço limitado

5. TRADE-OFFS ESPAÇO-TEMPO:
   • Fibonacci: recursivo (lento, pouco espaço) vs memoizado (rápido, mais espaço)
   • Ordenação: in-place (lento, O(1)) vs auxiliar (rápido, O(n))
   • Busca: linear (O(1) espaço) vs hash table (O(n) espaço)

6. ALGORITMOS DE STREAMING:
   • Reservoir Sampling: amostra uniforme de stream
   • Count-Min Sketch: estimativa de frequências
   • Processamento com espaço sub-linear
   • Aproximações com garantias probabilísticas

7. MEDIÇÃO E ANÁLISE:
   • Ferramentas: tracemalloc, psutil, sys.getsizeof
   • Métricas: memória auxiliar, pico, crescimento
   • Profiling de memória em tempo real
   • Detecção de vazamentos

8. APLICAÇÕES PRÁTICAS:
   • Sistemas embarcados (memória limitada)
   • Big Data (processamento de streams)
   • Aplicações web (otimização de cache)
   • Jogos (gerenciamento de recursos)

9. LIMITAÇÕES E CONSIDERAÇÕES:
   • Nem sempre é possível otimizar espaço e tempo
   • Complexidade de implementação pode aumentar
   • Trade-offs dependem do contexto de uso
   • Medições podem variar entre plataformas

10. ESTRATÉGIAS DE DESIGN:
    • Identificar gargalos de memória
    • Escolher estruturas apropriadas
    • Implementar lazy loading quando possível
    • Monitorar uso de memória em produção

A análise de complexidade espacial é crucial para:
- Desenvolver software eficiente em recursos
- Otimizar aplicações para dispositivos limitados
- Processar grandes volumes de dados
- Criar sistemas escaláveis e sustentáveis

Próximo: Módulo 07.4 - Profiling e Performance
    """)


if __name__ == "__main__":
    main()