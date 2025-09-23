"""
MÓDULO 07.1 - NOTAÇÃO BIG O E ANÁLISE ASSINTÓTICA
=================================================

Objetivos de Aprendizado:
- Compreender análise assintótica de algoritmos
- Dominar notações O, Ω, Θ (Big O, Big Omega, Big Theta)
- Identificar classes de complexidade
- Analisar crescimento de funções
- Comparar eficiência de algoritmos
- Aplicar análise em casos práticos

Conceitos Abordados:
- Análise assintótica
- Notação Big O (limite superior)
- Notação Big Omega (limite inferior)
- Notação Big Theta (limite exato)
- Classes de complexidade comum
- Análise de melhor, pior e caso médio
- Hierarquia de crescimento
- Regras de simplificação

Classes de Complexidade:
- O(1) - Constante
- O(log n) - Logarítmica
- O(n) - Linear
- O(n log n) - Linearítmica
- O(n²) - Quadrática
- O(n³) - Cúbica
- O(2ⁿ) - Exponencial
- O(n!) - Fatorial

Pré-requisitos:
- Matemática básica (logaritmos, exponenciais)
- Conceitos de algoritmos
- Estruturas de controle
- Recursão
"""

import time
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Callable, Dict, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import functools
from collections import defaultdict


class ClasseComplexidade(Enum):
    """Enumera as principais classes de complexidade."""
    CONSTANTE = "O(1)"
    LOGARITMICA = "O(log n)"
    LINEAR = "O(n)"
    LINEARITMICA = "O(n log n)"
    QUADRATICA = "O(n²)"
    CUBICA = "O(n³)"
    EXPONENCIAL = "O(2ⁿ)"
    FATORIAL = "O(n!)"


@dataclass
class ResultadoAnalise:
    """Resultado da análise de complexidade."""
    algoritmo: str
    tamanho_entrada: int
    tempo_execucao: float
    operacoes_basicas: int
    memoria_utilizada: int
    classe_complexidade: ClasseComplexidade
    observacoes: str = ""


class AnalisadorComplexidade:
    """
    Classe para análise de complexidade de algoritmos.
    """
    
    def __init__(self):
        """Inicializa o analisador."""
        self.resultados: List[ResultadoAnalise] = []
        self.contador_operacoes = 0
        self.memoria_pico = 0
    
    def reset_contadores(self):
        """Reseta contadores de análise."""
        self.contador_operacoes = 0
        self.memoria_pico = 0
    
    def incrementar_operacao(self, quantidade: int = 1):
        """Incrementa contador de operações básicas."""
        self.contador_operacoes += quantidade
    
    def medir_tempo_execucao(self, funcao: Callable, *args, **kwargs) -> Tuple[Any, float]:
        """
        Mede tempo de execução de uma função.
        
        Args:
            funcao: Função a ser medida
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
        
        Returns:
            Tupla (resultado, tempo_execucao)
        """
        inicio = time.perf_counter()
        resultado = funcao(*args, **kwargs)
        fim = time.perf_counter()
        
        return resultado, fim - inicio
    
    def analisar_algoritmo(self, nome: str, funcao: Callable, 
                          entrada: Any, classe_esperada: ClasseComplexidade) -> ResultadoAnalise:
        """
        Analisa complexidade de um algoritmo.
        
        Args:
            nome: Nome do algoritmo
            funcao: Função do algoritmo
            entrada: Dados de entrada
            classe_esperada: Classe de complexidade esperada
        
        Returns:
            Resultado da análise
        """
        self.reset_contadores()
        
        # Medir execução
        resultado, tempo = self.medir_tempo_execucao(funcao, entrada)
        
        # Determinar tamanho da entrada
        if hasattr(entrada, '__len__'):
            tamanho = len(entrada)
        elif isinstance(entrada, int):
            tamanho = entrada
        else:
            tamanho = 1
        
        # Criar resultado
        analise = ResultadoAnalise(
            algoritmo=nome,
            tamanho_entrada=tamanho,
            tempo_execucao=tempo,
            operacoes_basicas=self.contador_operacoes,
            memoria_utilizada=self.memoria_pico,
            classe_complexidade=classe_esperada
        )
        
        self.resultados.append(analise)
        return analise
    
    def comparar_crescimento(self, tamanhos: List[int], 
                           funcoes: Dict[str, Callable]) -> Dict[str, List[float]]:
        """
        Compara crescimento de diferentes algoritmos.
        
        Args:
            tamanhos: Lista de tamanhos de entrada
            funcoes: Dicionário {nome: função}
        
        Returns:
            Dicionário com tempos de execução
        """
        resultados = defaultdict(list)
        
        for tamanho in tamanhos:
            # Gerar entrada de teste
            entrada = list(range(tamanho))
            random.shuffle(entrada)
            
            for nome, funcao in funcoes.items():
                try:
                    _, tempo = self.medir_tempo_execucao(funcao, entrada.copy())
                    resultados[nome].append(tempo)
                except Exception as e:
                    print(f"Erro em {nome} com tamanho {tamanho}: {e}")
                    resultados[nome].append(float('inf'))
        
        return dict(resultados)
    
    def plotar_crescimento(self, tamanhos: List[int], 
                          tempos: Dict[str, List[float]], 
                          titulo: str = "Análise de Crescimento"):
        """
        Plota gráfico de crescimento dos algoritmos.
        
        Args:
            tamanhos: Tamanhos de entrada
            tempos: Tempos de execução por algoritmo
            titulo: Título do gráfico
        """
        plt.figure(figsize=(12, 8))
        
        for nome, tempo_lista in tempos.items():
            # Filtrar valores infinitos
            tamanhos_validos = []
            tempos_validos = []
            
            for t, tempo in zip(tamanhos, tempo_lista):
                if tempo != float('inf') and tempo > 0:
                    tamanhos_validos.append(t)
                    tempos_validos.append(tempo)
            
            if tempos_validos:
                plt.plot(tamanhos_validos, tempos_validos, 
                        marker='o', label=nome, linewidth=2)
        
        plt.xlabel('Tamanho da Entrada (n)')
        plt.ylabel('Tempo de Execução (segundos)')
        plt.title(titulo)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.xscale('log')
        plt.show()
    
    def classificar_complexidade(self, tamanhos: List[int], 
                               tempos: List[float]) -> ClasseComplexidade:
        """
        Classifica complexidade baseada em dados empíricos.
        
        Args:
            tamanhos: Tamanhos de entrada
            tempos: Tempos correspondentes
        
        Returns:
            Classe de complexidade estimada
        """
        if len(tamanhos) < 3 or len(tempos) < 3:
            return ClasseComplexidade.CONSTANTE
        
        # Calcular razões de crescimento
        razoes = []
        for i in range(1, len(tamanhos)):
            if tempos[i-1] > 0 and tamanhos[i-1] > 0:
                razao_tempo = tempos[i] / tempos[i-1]
                razao_tamanho = tamanhos[i] / tamanhos[i-1]
                
                if razao_tamanho > 1:
                    razoes.append(razao_tempo / razao_tamanho)
        
        if not razoes:
            return ClasseComplexidade.CONSTANTE
        
        razao_media = sum(razoes) / len(razoes)
        
        # Classificar baseado na razão média
        if razao_media < 1.1:
            return ClasseComplexidade.CONSTANTE
        elif razao_media < 1.5:
            return ClasseComplexidade.LOGARITMICA
        elif razao_media < 2.5:
            return ClasseComplexidade.LINEAR
        elif razao_media < 4.0:
            return ClasseComplexidade.LINEARITMICA
        elif razao_media < 8.0:
            return ClasseComplexidade.QUADRATICA
        elif razao_media < 16.0:
            return ClasseComplexidade.CUBICA
        else:
            return ClasseComplexidade.EXPONENCIAL


class ExemplosComplexidade:
    """
    Exemplos de algoritmos com diferentes complexidades.
    """
    
    def __init__(self, analisador: AnalisadorComplexidade):
        """
        Inicializa com referência ao analisador.
        
        Args:
            analisador: Instância do analisador de complexidade
        """
        self.analisador = analisador
    
    # O(1) - Complexidade Constante
    def acesso_array(self, arr: List[int], indice: int = 0) -> int:
        """
        Acesso direto a elemento do array.
        Complexidade: O(1)
        """
        self.analisador.incrementar_operacao()
        return arr[indice] if 0 <= indice < len(arr) else -1
    
    def operacao_aritmetica(self, a: int, b: int) -> int:
        """
        Operação aritmética simples.
        Complexidade: O(1)
        """
        self.analisador.incrementar_operacao()
        return a + b * 2 - (a // 3)
    
    # O(log n) - Complexidade Logarítmica
    def busca_binaria(self, arr: List[int], target: int) -> int:
        """
        Busca binária em array ordenado.
        Complexidade: O(log n)
        """
        esquerda, direita = 0, len(arr) - 1
        
        while esquerda <= direita:
            self.analisador.incrementar_operacao()
            meio = (esquerda + direita) // 2
            
            if arr[meio] == target:
                return meio
            elif arr[meio] < target:
                esquerda = meio + 1
            else:
                direita = meio - 1
        
        return -1
    
    def potencia_rapida(self, base: int, expoente: int) -> int:
        """
        Exponenciação rápida.
        Complexidade: O(log n)
        """
        if expoente == 0:
            self.analisador.incrementar_operacao()
            return 1
        
        self.analisador.incrementar_operacao()
        
        if expoente % 2 == 0:
            metade = self.potencia_rapida(base, expoente // 2)
            return metade * metade
        else:
            return base * self.potencia_rapida(base, expoente - 1)
    
    # O(n) - Complexidade Linear
    def busca_linear(self, arr: List[int], target: int) -> int:
        """
        Busca linear em array.
        Complexidade: O(n)
        """
        for i, valor in enumerate(arr):
            self.analisador.incrementar_operacao()
            if valor == target:
                return i
        return -1
    
    def soma_array(self, arr: List[int]) -> int:
        """
        Soma todos os elementos do array.
        Complexidade: O(n)
        """
        soma = 0
        for valor in arr:
            self.analisador.incrementar_operacao()
            soma += valor
        return soma
    
    def encontrar_maximo(self, arr: List[int]) -> int:
        """
        Encontra o maior elemento do array.
        Complexidade: O(n)
        """
        if not arr:
            return None
        
        maximo = arr[0]
        for valor in arr[1:]:
            self.analisador.incrementar_operacao()
            if valor > maximo:
                maximo = valor
        return maximo
    
    # O(n log n) - Complexidade Linearítmica
    def merge_sort(self, arr: List[int]) -> List[int]:
        """
        Algoritmo Merge Sort.
        Complexidade: O(n log n)
        """
        if len(arr) <= 1:
            self.analisador.incrementar_operacao()
            return arr
        
        meio = len(arr) // 2
        esquerda = self.merge_sort(arr[:meio])
        direita = self.merge_sort(arr[meio:])
        
        return self._merge(esquerda, direita)
    
    def _merge(self, esquerda: List[int], direita: List[int]) -> List[int]:
        """Função auxiliar para merge sort."""
        resultado = []
        i = j = 0
        
        while i < len(esquerda) and j < len(direita):
            self.analisador.incrementar_operacao()
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1
        
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        return resultado
    
    def heap_sort(self, arr: List[int]) -> List[int]:
        """
        Algoritmo Heap Sort.
        Complexidade: O(n log n)
        """
        arr = arr.copy()
        n = len(arr)
        
        # Construir heap
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        
        # Extrair elementos
        for i in range(n - 1, 0, -1):
            self.analisador.incrementar_operacao()
            arr[0], arr[i] = arr[i], arr[0]
            self._heapify(arr, i, 0)
        
        return arr
    
    def _heapify(self, arr: List[int], n: int, i: int):
        """Função auxiliar para heap sort."""
        maior = i
        esquerda = 2 * i + 1
        direita = 2 * i + 2
        
        self.analisador.incrementar_operacao()
        
        if esquerda < n and arr[esquerda] > arr[maior]:
            maior = esquerda
        
        if direita < n and arr[direita] > arr[maior]:
            maior = direita
        
        if maior != i:
            arr[i], arr[maior] = arr[maior], arr[i]
            self._heapify(arr, n, maior)
    
    # O(n²) - Complexidade Quadrática
    def bubble_sort(self, arr: List[int]) -> List[int]:
        """
        Algoritmo Bubble Sort.
        Complexidade: O(n²)
        """
        arr = arr.copy()
        n = len(arr)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                self.analisador.incrementar_operacao()
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        
        return arr
    
    def selection_sort(self, arr: List[int]) -> List[int]:
        """
        Algoritmo Selection Sort.
        Complexidade: O(n²)
        """
        arr = arr.copy()
        n = len(arr)
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                self.analisador.incrementar_operacao()
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        
        return arr
    
    def multiplicacao_matrizes_naive(self, A: List[List[int]], 
                                   B: List[List[int]]) -> List[List[int]]:
        """
        Multiplicação de matrizes ingênua.
        Complexidade: O(n³)
        """
        n = len(A)
        C = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    self.analisador.incrementar_operacao()
                    C[i][j] += A[i][k] * B[k][j]
        
        return C
    
    # O(2ⁿ) - Complexidade Exponencial
    def fibonacci_recursivo(self, n: int) -> int:
        """
        Fibonacci recursivo ingênuo.
        Complexidade: O(2ⁿ)
        """
        self.analisador.incrementar_operacao()
        
        if n <= 1:
            return n
        
        return (self.fibonacci_recursivo(n - 1) + 
                self.fibonacci_recursivo(n - 2))
    
    def subconjuntos_recursivo(self, arr: List[int]) -> List[List[int]]:
        """
        Gera todos os subconjuntos recursivamente.
        Complexidade: O(2ⁿ)
        """
        self.analisador.incrementar_operacao()
        
        if not arr:
            return [[]]
        
        primeiro = arr[0]
        resto = arr[1:]
        
        subconjuntos_resto = self.subconjuntos_recursivo(resto)
        
        resultado = []
        for subconjunto in subconjuntos_resto:
            resultado.append(subconjunto)
            resultado.append([primeiro] + subconjunto)
        
        return resultado
    
    # O(n!) - Complexidade Fatorial
    def permutacoes_recursivo(self, arr: List[int]) -> List[List[int]]:
        """
        Gera todas as permutações recursivamente.
        Complexidade: O(n!)
        """
        self.analisador.incrementar_operacao()
        
        if len(arr) <= 1:
            return [arr]
        
        resultado = []
        for i in range(len(arr)):
            elemento = arr[i]
            resto = arr[:i] + arr[i+1:]
            
            for permutacao in self.permutacoes_recursivo(resto):
                resultado.append([elemento] + permutacao)
        
        return resultado
    
    def problema_caixeiro_viajante_brute_force(self, distancias: List[List[int]]) -> Tuple[List[int], int]:
        """
        Resolve TSP por força bruta.
        Complexidade: O(n!)
        """
        n = len(distancias)
        cidades = list(range(1, n))  # Excluir cidade inicial
        
        melhor_rota = None
        menor_distancia = float('inf')
        
        for permutacao in self.permutacoes_recursivo(cidades):
            self.analisador.incrementar_operacao()
            
            rota = [0] + permutacao + [0]  # Começar e terminar na cidade 0
            distancia_total = 0
            
            for i in range(len(rota) - 1):
                distancia_total += distancias[rota[i]][rota[i + 1]]
            
            if distancia_total < menor_distancia:
                menor_distancia = distancia_total
                melhor_rota = rota
        
        return melhor_rota, menor_distancia


class FuncoesComplexidade:
    """
    Funções matemáticas para análise de complexidade.
    """
    
    @staticmethod
    def constante(n: int) -> float:
        """Função constante: f(n) = 1"""
        return 1.0
    
    @staticmethod
    def logaritmica(n: int) -> float:
        """Função logarítmica: f(n) = log₂(n)"""
        return math.log2(max(1, n))
    
    @staticmethod
    def linear(n: int) -> float:
        """Função linear: f(n) = n"""
        return float(n)
    
    @staticmethod
    def linearitmica(n: int) -> float:
        """Função linearítmica: f(n) = n * log₂(n)"""
        return n * math.log2(max(1, n))
    
    @staticmethod
    def quadratica(n: int) -> float:
        """Função quadrática: f(n) = n²"""
        return float(n * n)
    
    @staticmethod
    def cubica(n: int) -> float:
        """Função cúbica: f(n) = n³"""
        return float(n * n * n)
    
    @staticmethod
    def exponencial(n: int) -> float:
        """Função exponencial: f(n) = 2ⁿ"""
        return float(2 ** min(n, 50))  # Limitar para evitar overflow
    
    @staticmethod
    def fatorial(n: int) -> float:
        """Função fatorial: f(n) = n!"""
        return float(math.factorial(min(n, 20)))  # Limitar para evitar overflow
    
    @staticmethod
    def plotar_funcoes_complexidade(max_n: int = 20):
        """
        Plota gráfico das funções de complexidade.
        
        Args:
            max_n: Valor máximo de n
        """
        n_values = list(range(1, max_n + 1))
        
        funcoes = {
            'O(1)': FuncoesComplexidade.constante,
            'O(log n)': FuncoesComplexidade.logaritmica,
            'O(n)': FuncoesComplexidade.linear,
            'O(n log n)': FuncoesComplexidade.linearitmica,
            'O(n²)': FuncoesComplexidade.quadratica,
            'O(n³)': FuncoesComplexidade.cubica,
            'O(2ⁿ)': FuncoesComplexidade.exponencial,
            'O(n!)': FuncoesComplexidade.fatorial
        }
        
        plt.figure(figsize=(14, 10))
        
        for nome, funcao in funcoes.items():
            valores = []
            for n in n_values:
                try:
                    valor = funcao(n)
                    if valor < 1e10:  # Evitar valores muito grandes
                        valores.append(valor)
                    else:
                        valores.append(None)
                except:
                    valores.append(None)
            
            # Filtrar valores None
            n_filtrados = []
            valores_filtrados = []
            for n, v in zip(n_values, valores):
                if v is not None:
                    n_filtrados.append(n)
                    valores_filtrados.append(v)
            
            if valores_filtrados:
                plt.plot(n_filtrados, valores_filtrados, 
                        marker='o', label=nome, linewidth=2)
        
        plt.xlabel('Tamanho da Entrada (n)')
        plt.ylabel('Número de Operações')
        plt.title('Comparação de Funções de Complexidade')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.show()


# Funções de Demonstração
def demonstrar_classes_complexidade():
    """Demonstra diferentes classes de complexidade."""
    print("=== DEMONSTRAÇÃO: CLASSES DE COMPLEXIDADE ===\n")
    
    analisador = AnalisadorComplexidade()
    exemplos = ExemplosComplexidade(analisador)
    
    # Dados de teste
    arr_pequeno = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    arr_ordenado = sorted(arr_pequeno)
    
    print("1. COMPLEXIDADE CONSTANTE - O(1)")
    print("   Operações que executam em tempo constante")
    
    resultado = analisador.analisar_algoritmo(
        "Acesso Array", 
        exemplos.acesso_array, 
        (arr_pequeno, 5), 
        ClasseComplexidade.CONSTANTE
    )
    print(f"   • Acesso ao índice 5: {arr_pequeno[5]}")
    print(f"   • Operações: {resultado.operacoes_basicas}")
    print(f"   • Tempo: {resultado.tempo_execucao:.8f}s\n")
    
    print("2. COMPLEXIDADE LOGARÍTMICA - O(log n)")
    print("   Algoritmos que dividem o problema pela metade")
    
    resultado = analisador.analisar_algoritmo(
        "Busca Binária", 
        exemplos.busca_binaria, 
        (arr_ordenado, 5), 
        ClasseComplexidade.LOGARITMICA
    )
    print(f"   • Buscar 5 em {arr_ordenado}")
    print(f"   • Posição encontrada: {exemplos.busca_binaria(arr_ordenado, 5)}")
    print(f"   • Operações: {resultado.operacoes_basicas}")
    print(f"   • Tempo: {resultado.tempo_execucao:.8f}s\n")
    
    print("3. COMPLEXIDADE LINEAR - O(n)")
    print("   Algoritmos que visitam cada elemento uma vez")
    
    resultado = analisador.analisar_algoritmo(
        "Busca Linear", 
        exemplos.busca_linear, 
        (arr_pequeno, 5), 
        ClasseComplexidade.LINEAR
    )
    print(f"   • Buscar 5 em {arr_pequeno}")
    print(f"   • Posição encontrada: {exemplos.busca_linear(arr_pequeno, 5)}")
    print(f"   • Operações: {resultado.operacoes_basicas}")
    print(f"   • Tempo: {resultado.tempo_execucao:.8f}s\n")
    
    print("4. COMPLEXIDADE LINEARÍTMICA - O(n log n)")
    print("   Algoritmos de ordenação eficientes")
    
    resultado = analisador.analisar_algoritmo(
        "Merge Sort", 
        exemplos.merge_sort, 
        arr_pequeno, 
        ClasseComplexidade.LINEARITMICA
    )
    print(f"   • Ordenar {arr_pequeno}")
    print(f"   • Resultado: {exemplos.merge_sort(arr_pequeno)}")
    print(f"   • Operações: {resultado.operacoes_basicas}")
    print(f"   • Tempo: {resultado.tempo_execucao:.8f}s\n")
    
    print("5. COMPLEXIDADE QUADRÁTICA - O(n²)")
    print("   Algoritmos com loops aninhados")
    
    resultado = analisador.analisar_algoritmo(
        "Bubble Sort", 
        exemplos.bubble_sort, 
        arr_pequeno, 
        ClasseComplexidade.QUADRATICA
    )
    print(f"   • Ordenar {arr_pequeno}")
    print(f"   • Resultado: {exemplos.bubble_sort(arr_pequeno)}")
    print(f"   • Operações: {resultado.operacoes_basicas}")
    print(f"   • Tempo: {resultado.tempo_execucao:.8f}s\n")
    
    print("6. COMPLEXIDADE EXPONENCIAL - O(2ⁿ)")
    print("   Algoritmos que exploram todas as possibilidades")
    
    n_fib = 10
    resultado = analisador.analisar_algoritmo(
        "Fibonacci Recursivo", 
        exemplos.fibonacci_recursivo, 
        n_fib, 
        ClasseComplexidade.EXPONENCIAL
    )
    print(f"   • Fibonacci({n_fib}) = {exemplos.fibonacci_recursivo(n_fib)}")
    print(f"   • Operações: {resultado.operacoes_basicas}")
    print(f"   • Tempo: {resultado.tempo_execucao:.8f}s\n")


def demonstrar_analise_empirica():
    """Demonstra análise empírica de algoritmos."""
    print("=== DEMONSTRAÇÃO: ANÁLISE EMPÍRICA ===\n")
    
    analisador = AnalisadorComplexidade()
    exemplos = ExemplosComplexidade(analisador)
    
    # Tamanhos de teste
    tamanhos = [10, 20, 50, 100, 200, 500]
    
    # Algoritmos para comparar
    algoritmos = {
        'Busca Linear': lambda arr: exemplos.busca_linear(arr, arr[-1]),
        'Busca Binária': lambda arr: exemplos.busca_binaria(sorted(arr), arr[-1]),
        'Bubble Sort': exemplos.bubble_sort,
        'Merge Sort': exemplos.merge_sort
    }
    
    print("Comparando crescimento de algoritmos:")
    print("Tamanhos de teste:", tamanhos)
    
    # Executar comparação
    resultados = analisador.comparar_crescimento(tamanhos, algoritmos)
    
    # Mostrar resultados
    for algoritmo, tempos in resultados.items():
        print(f"\n{algoritmo}:")
        for tamanho, tempo in zip(tamanhos, tempos):
            if tempo != float('inf'):
                print(f"  n={tamanho:3d}: {tempo:.6f}s")
            else:
                print(f"  n={tamanho:3d}: ERRO")
    
    # Classificar complexidades
    print("\nClassificação automática de complexidade:")
    for algoritmo, tempos in resultados.items():
        tempos_validos = [t for t in tempos if t != float('inf')]
        tamanhos_validos = tamanhos[:len(tempos_validos)]
        
        if len(tempos_validos) >= 3:
            classe = analisador.classificar_complexidade(tamanhos_validos, tempos_validos)
            print(f"  {algoritmo}: {classe.value}")


def demonstrar_notacoes_assintoticas():
    """Demonstra as diferentes notações assintóticas."""
    print("\n=== DEMONSTRAÇÃO: NOTAÇÕES ASSINTÓTICAS ===\n")
    
    print("NOTAÇÃO BIG O (O) - Limite Superior:")
    print("  • Define o pior caso ou limite superior do crescimento")
    print("  • f(n) = O(g(n)) se existem c > 0 e n₀ tal que f(n) ≤ c·g(n) para n ≥ n₀")
    print("  • Exemplo: 3n² + 2n + 1 = O(n²)")
    print("  • Usado para: análise de pior caso, garantias de performance\n")
    
    print("NOTAÇÃO BIG OMEGA (Ω) - Limite Inferior:")
    print("  • Define o melhor caso ou limite inferior do crescimento")
    print("  • f(n) = Ω(g(n)) se existem c > 0 e n₀ tal que f(n) ≥ c·g(n) para n ≥ n₀")
    print("  • Exemplo: 3n² + 2n + 1 = Ω(n²)")
    print("  • Usado para: análise de melhor caso, limites inferiores\n")
    
    print("NOTAÇÃO BIG THETA (Θ) - Limite Exato:")
    print("  • Define o crescimento exato (limite superior e inferior)")
    print("  • f(n) = Θ(g(n)) se f(n) = O(g(n)) e f(n) = Ω(g(n))")
    print("  • Exemplo: 3n² + 2n + 1 = Θ(n²)")
    print("  • Usado para: análise de caso médio, crescimento exato\n")
    
    print("EXEMPLOS PRÁTICOS:")
    
    # Exemplo 1: Busca Linear
    print("\n1. Busca Linear:")
    print("   • Melhor caso: O(1) - elemento na primeira posição")
    print("   • Pior caso: O(n) - elemento na última posição ou não existe")
    print("   • Caso médio: Θ(n) - em média, percorre metade do array")
    
    # Exemplo 2: Busca Binária
    print("\n2. Busca Binária:")
    print("   • Melhor caso: O(1) - elemento no meio")
    print("   • Pior caso: O(log n) - elemento nas folhas")
    print("   • Caso médio: Θ(log n) - sempre divide pela metade")
    
    # Exemplo 3: Merge Sort
    print("\n3. Merge Sort:")
    print("   • Melhor caso: Ω(n log n) - sempre divide e conquista")
    print("   • Pior caso: O(n log n) - sempre divide e conquista")
    print("   • Caso médio: Θ(n log n) - comportamento consistente")
    
    # Exemplo 4: Quick Sort
    print("\n4. Quick Sort:")
    print("   • Melhor caso: Ω(n log n) - pivot sempre no meio")
    print("   • Pior caso: O(n²) - pivot sempre no extremo")
    print("   • Caso médio: Θ(n log n) - pivot em posição aleatória")


def demonstrar_regras_simplificacao():
    """Demonstra regras de simplificação da notação Big O."""
    print("\n=== DEMONSTRAÇÃO: REGRAS DE SIMPLIFICAÇÃO ===\n")
    
    print("REGRAS PARA SIMPLIFICAR NOTAÇÃO BIG O:")
    
    print("\n1. REGRA DA SOMA:")
    print("   • O(f(n)) + O(g(n)) = O(max(f(n), g(n)))")
    print("   • Exemplo: O(n) + O(n²) = O(n²)")
    print("   • Exemplo: O(log n) + O(n) = O(n)")
    
    print("\n2. REGRA DO PRODUTO:")
    print("   • O(f(n)) × O(g(n)) = O(f(n) × g(n))")
    print("   • Exemplo: O(n) × O(log n) = O(n log n)")
    print("   • Exemplo: O(n) × O(n) = O(n²)")
    
    print("\n3. REGRA DA CONSTANTE:")
    print("   • O(c × f(n)) = O(f(n)) para qualquer constante c > 0")
    print("   • Exemplo: O(5n) = O(n)")
    print("   • Exemplo: O(100n²) = O(n²)")
    
    print("\n4. REGRA DOS TERMOS DOMINANTES:")
    print("   • Manter apenas o termo de maior crescimento")
    print("   • Exemplo: O(n³ + n² + n + 1) = O(n³)")
    print("   • Exemplo: O(2ⁿ + n¹⁰⁰) = O(2ⁿ)")
    
    print("\n5. REGRA DOS LOGARITMOS:")
    print("   • O(log_a n) = O(log_b n) para quaisquer bases a, b > 1")
    print("   • Exemplo: O(log₂ n) = O(log₁₀ n) = O(ln n)")
    
    print("\nEXEMPLOS DE SIMPLIFICAÇÃO:")
    
    exemplos = [
        ("3n² + 2n + 1", "O(n²)"),
        ("5n log n + 2n + 10", "O(n log n)"),
        ("n³ + 100n² + 50n + 1000", "O(n³)"),
        ("2ⁿ + n⁵ + n² log n", "O(2ⁿ)"),
        ("log n + √n + 1", "O(√n)"),
        ("n! + 2ⁿ + n¹⁰", "O(n!)"),
        ("(log n)² + log n + 1", "O((log n)²)")
    ]
    
    for expressao, simplificada in exemplos:
        print(f"   • {expressao} = {simplificada}")


def benchmark_complexidades():
    """Benchmark comparativo de diferentes complexidades."""
    print("\n=== BENCHMARK: COMPARAÇÃO DE COMPLEXIDADES ===\n")
    
    analisador = AnalisadorComplexidade()
    exemplos = ExemplosComplexidade(analisador)
    
    # Tamanhos progressivos
    tamanhos = [10, 50, 100, 200, 500]
    
    print("Comparação empírica de algoritmos:")
    print("Tamanhos de teste:", tamanhos)
    print()
    
    # Algoritmos de busca
    print("ALGORITMOS DE BUSCA:")
    algoritmos_busca = {
        'Linear O(n)': lambda arr: exemplos.busca_linear(arr, arr[-1]),
        'Binária O(log n)': lambda arr: exemplos.busca_binaria(sorted(arr), arr[-1])
    }
    
    resultados_busca = analisador.comparar_crescimento(tamanhos, algoritmos_busca)
    
    for algoritmo, tempos in resultados_busca.items():
        print(f"\n{algoritmo}:")
        for tamanho, tempo in zip(tamanhos, tempos):
            if tempo != float('inf'):
                print(f"  n={tamanho:3d}: {tempo:.6f}s")
    
    # Algoritmos de ordenação
    print("\nALGORITMOS DE ORDENAÇÃO:")
    algoritmos_ordenacao = {
        'Bubble O(n²)': exemplos.bubble_sort,
        'Selection O(n²)': exemplos.selection_sort,
        'Merge O(n log n)': exemplos.merge_sort,
        'Heap O(n log n)': exemplos.heap_sort
    }
    
    # Usar tamanhos menores para algoritmos quadráticos
    tamanhos_ordenacao = [10, 25, 50, 100, 200]
    resultados_ordenacao = analisador.comparar_crescimento(tamanhos_ordenacao, algoritmos_ordenacao)
    
    for algoritmo, tempos in resultados_ordenacao.items():
        print(f"\n{algoritmo}:")
        for tamanho, tempo in zip(tamanhos_ordenacao, tempos):
            if tempo != float('inf'):
                print(f"  n={tamanho:3d}: {tempo:.6f}s")
    
    # Análise de crescimento
    print("\nANÁLISE DE CRESCIMENTO:")
    print("Razão de crescimento entre tamanhos consecutivos:")
    
    for algoritmo, tempos in resultados_ordenacao.items():
        print(f"\n{algoritmo}:")
        tempos_validos = [t for t in tempos if t != float('inf') and t > 0]
        
        if len(tempos_validos) >= 2:
            for i in range(1, len(tempos_validos)):
                razao = tempos_validos[i] / tempos_validos[i-1]
                tamanho_atual = tamanhos_ordenacao[i]
                tamanho_anterior = tamanhos_ordenacao[i-1]
                fator_tamanho = tamanho_atual / tamanho_anterior
                
                print(f"  n={tamanho_anterior}→{tamanho_atual}: "
                      f"tempo ×{razao:.2f}, tamanho ×{fator_tamanho:.2f}")


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 07.1 - NOTAÇÃO BIG O E ANÁLISE ASSINTÓTICA")
    print("=" * 60)
    
    demonstrar_classes_complexidade()
    demonstrar_notacoes_assintoticas()
    demonstrar_regras_simplificacao()
    demonstrar_analise_empirica()
    benchmark_complexidades()
    
    # Plotar funções de complexidade
    print("\nGerando gráfico de funções de complexidade...")
    try:
        FuncoesComplexidade.plotar_funcoes_complexidade(15)
    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")
    
    print("\n" + "=" * 60)
    print("CONCLUSÃO DO MÓDULO 07.1")
    print("=" * 60)
    print("""
Principais Aprendizados:

1. ANÁLISE ASSINTÓTICA:
   • Foco no comportamento para entradas grandes
   • Ignora constantes e termos de menor ordem
   • Permite comparação objetiva de algoritmos
   • Independente de hardware e implementação

2. NOTAÇÕES MATEMÁTICAS:
   • Big O (O): limite superior, pior caso
   • Big Omega (Ω): limite inferior, melhor caso
   • Big Theta (Θ): limite exato, caso médio
   • Cada uma serve para diferentes análises

3. CLASSES DE COMPLEXIDADE:
   • O(1): Constante - acesso direto, operações básicas
   • O(log n): Logarítmica - busca binária, árvores balanceadas
   • O(n): Linear - busca sequencial, percorrer array
   • O(n log n): Linearítmica - ordenação eficiente
   • O(n²): Quadrática - algoritmos com loops aninhados
   • O(2ⁿ): Exponencial - problemas de força bruta
   • O(n!): Fatorial - permutações, TSP brute force

4. HIERARQUIA DE CRESCIMENTO:
   • O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)
   • Diferenças dramáticas para entradas grandes
   • Importância da escolha do algoritmo correto

5. REGRAS DE SIMPLIFICAÇÃO:
   • Soma: manter termo dominante
   • Produto: multiplicar complexidades
   • Constantes: podem ser ignoradas
   • Logaritmos: base não importa

6. ANÁLISE PRÁTICA:
   • Medição empírica complementa análise teórica
   • Constantes ocultas podem ser importantes
   • Tamanho da entrada determina algoritmo ideal
   • Trade-offs entre diferentes recursos

7. APLICAÇÕES:
   • Escolha de algoritmos e estruturas de dados
   • Previsão de performance e escalabilidade
   • Otimização de sistemas críticos
   • Análise de viabilidade computacional

8. LIMITAÇÕES:
   • Análise assintótica ignora constantes
   • Comportamento para entradas pequenas pode diferir
   • Fatores como cache e memória não são considerados
   • Implementação específica pode alterar performance

A análise de complexidade é fundamental para:
- Escolher algoritmos apropriados
- Prever comportamento em escala
- Identificar gargalos de performance
- Projetar sistemas eficientes

Próximo: Módulo 07.2 - Análise Amortizada
    """)


if __name__ == "__main__":
    main()