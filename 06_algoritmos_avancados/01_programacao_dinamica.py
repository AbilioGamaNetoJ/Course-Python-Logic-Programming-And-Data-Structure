"""
MÓDULO 06.1 - PROGRAMAÇÃO DINÂMICA
==================================

Objetivos de Aprendizado:
- Compreender os princípios da programação dinâmica
- Implementar soluções com memoização e tabulação
- Resolver problemas clássicos de otimização
- Analisar complexidade temporal e espacial
- Aplicar técnicas de otimização de espaço

Conceitos Abordados:
- Subestrutura ótima
- Sobreposição de subproblemas
- Memoização (top-down)
- Tabulação (bottom-up)
- Otimização de espaço
- Reconstrução de soluções

Problemas Clássicos:
- Sequência de Fibonacci
- Problema da Mochila (0/1 e Unbounded)
- Longest Common Subsequence (LCS)
- Longest Increasing Subsequence (LIS)
- Edit Distance (Levenshtein)
- Coin Change Problem
- Maximum Subarray (Kadane)
- Matrix Chain Multiplication

Pré-requisitos:
- Recursão e análise de complexidade
- Estruturas de dados básicas
- Conceitos de otimização

Complexidade Típica:
- Sem DP: Exponencial O(2^n)
- Com DP: Polinomial O(n²) ou O(n³)
"""

from typing import List, Dict, Tuple, Optional, Any
import time
import sys
from functools import lru_cache, wraps
from collections import defaultdict


def memoize(func):
    """
    Decorador para memoização automática.
    
    Args:
        func: Função a ser memoizada
    
    Returns:
        Função com cache automático
    """
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Criar chave única para os argumentos
        key = str(args) + str(sorted(kwargs.items()))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]
    
    wrapper.cache = cache
    wrapper.cache_clear = lambda: cache.clear()
    wrapper.cache_info = lambda: f"Cache size: {len(cache)}"
    
    return wrapper


class FibonacciDP:
    """
    Implementações da sequência de Fibonacci usando diferentes abordagens de DP.
    """
    
    @staticmethod
    def recursivo_simples(n: int) -> int:
        """
        Implementação recursiva simples (ineficiente).
        Complexidade: O(2^n)
        """
        if n <= 1:
            return n
        return FibonacciDP.recursivo_simples(n-1) + FibonacciDP.recursivo_simples(n-2)
    
    @staticmethod
    @memoize
    def memoizado(n: int) -> int:
        """
        Implementação com memoização (top-down).
        Complexidade: O(n) tempo, O(n) espaço
        """
        if n <= 1:
            return n
        return FibonacciDP.memoizado(n-1) + FibonacciDP.memoizado(n-2)
    
    @staticmethod
    def tabulacao(n: int) -> int:
        """
        Implementação com tabulação (bottom-up).
        Complexidade: O(n) tempo, O(n) espaço
        """
        if n <= 1:
            return n
        
        dp = [0] * (n + 1)
        dp[1] = 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
        
        return dp[n]
    
    @staticmethod
    def otimizado_espaco(n: int) -> int:
        """
        Implementação otimizada em espaço.
        Complexidade: O(n) tempo, O(1) espaço
        """
        if n <= 1:
            return n
        
        prev2, prev1 = 0, 1
        
        for i in range(2, n + 1):
            current = prev1 + prev2
            prev2, prev1 = prev1, current
        
        return prev1


class ProblemasMochila:
    """
    Implementações dos problemas clássicos da mochila.
    """
    
    @staticmethod
    def mochila_01_recursiva(pesos: List[int], valores: List[int], 
                           capacidade: int, n: int = None) -> int:
        """
        Mochila 0/1 recursiva simples.
        Complexidade: O(2^n)
        """
        if n is None:
            n = len(pesos)
        
        # Caso base
        if n == 0 or capacidade == 0:
            return 0
        
        # Se o peso do item atual é maior que a capacidade, não pode incluir
        if pesos[n-1] > capacidade:
            return ProblemasMochila.mochila_01_recursiva(pesos, valores, capacidade, n-1)
        
        # Retorna o máximo entre incluir e não incluir o item atual
        incluir = valores[n-1] + ProblemasMochila.mochila_01_recursiva(
            pesos, valores, capacidade - pesos[n-1], n-1)
        nao_incluir = ProblemasMochila.mochila_01_recursiva(pesos, valores, capacidade, n-1)
        
        return max(incluir, nao_incluir)
    
    @staticmethod
    def mochila_01_memoizada(pesos: List[int], valores: List[int], capacidade: int) -> int:
        """
        Mochila 0/1 com memoização.
        Complexidade: O(n * W) tempo e espaço
        """
        n = len(pesos)
        memo = {}
        
        def dp(i: int, w: int) -> int:
            # Caso base
            if i == 0 or w == 0:
                return 0
            
            # Verificar cache
            if (i, w) in memo:
                return memo[(i, w)]
            
            # Se o peso do item atual é maior que a capacidade
            if pesos[i-1] > w:
                resultado = dp(i-1, w)
            else:
                # Máximo entre incluir e não incluir
                incluir = valores[i-1] + dp(i-1, w - pesos[i-1])
                nao_incluir = dp(i-1, w)
                resultado = max(incluir, nao_incluir)
            
            memo[(i, w)] = resultado
            return resultado
        
        return dp(n, capacidade)
    
    @staticmethod
    def mochila_01_tabulacao(pesos: List[int], valores: List[int], capacidade: int) -> Tuple[int, List[int]]:
        """
        Mochila 0/1 com tabulação e reconstrução da solução.
        Complexidade: O(n * W) tempo, O(n * W) espaço
        """
        n = len(pesos)
        
        # Criar tabela DP
        dp = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]
        
        # Preencher tabela
        for i in range(1, n + 1):
            for w in range(1, capacidade + 1):
                if pesos[i-1] <= w:
                    incluir = valores[i-1] + dp[i-1][w - pesos[i-1]]
                    nao_incluir = dp[i-1][w]
                    dp[i][w] = max(incluir, nao_incluir)
                else:
                    dp[i][w] = dp[i-1][w]
        
        # Reconstruir solução
        w = capacidade
        itens_selecionados = []
        
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                itens_selecionados.append(i-1)  # Índice do item
                w -= pesos[i-1]
        
        itens_selecionados.reverse()
        
        return dp[n][capacidade], itens_selecionados
    
    @staticmethod
    def mochila_01_otimizada(pesos: List[int], valores: List[int], capacidade: int) -> int:
        """
        Mochila 0/1 otimizada em espaço.
        Complexidade: O(n * W) tempo, O(W) espaço
        """
        dp = [0] * (capacidade + 1)
        
        for i in range(len(pesos)):
            # Percorrer de trás para frente para evitar usar valores já atualizados
            for w in range(capacidade, pesos[i] - 1, -1):
                dp[w] = max(dp[w], dp[w - pesos[i]] + valores[i])
        
        return dp[capacidade]
    
    @staticmethod
    def mochila_unbounded(pesos: List[int], valores: List[int], capacidade: int) -> int:
        """
        Mochila Unbounded (quantidade ilimitada de cada item).
        Complexidade: O(n * W) tempo, O(W) espaço
        """
        dp = [0] * (capacidade + 1)
        
        for w in range(1, capacidade + 1):
            for i in range(len(pesos)):
                if pesos[i] <= w:
                    dp[w] = max(dp[w], dp[w - pesos[i]] + valores[i])
        
        return dp[capacidade]


class SequenciasDP:
    """
    Problemas de programação dinâmica relacionados a sequências.
    """
    
    @staticmethod
    def lcs_comprimento(texto1: str, texto2: str) -> int:
        """
        Longest Common Subsequence - apenas comprimento.
        Complexidade: O(m * n) tempo, O(m * n) espaço
        """
        m, n = len(texto1), len(texto2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if texto1[i-1] == texto2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    @staticmethod
    def lcs_completa(texto1: str, texto2: str) -> Tuple[int, str]:
        """
        Longest Common Subsequence - comprimento e sequência.
        Complexidade: O(m * n) tempo e espaço
        """
        m, n = len(texto1), len(texto2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Preencher tabela
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if texto1[i-1] == texto2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Reconstruir LCS
        lcs = []
        i, j = m, n
        
        while i > 0 and j > 0:
            if texto1[i-1] == texto2[j-1]:
                lcs.append(texto1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        lcs.reverse()
        return dp[m][n], ''.join(lcs)
    
    @staticmethod
    def lis_comprimento(arr: List[int]) -> int:
        """
        Longest Increasing Subsequence - O(n²).
        Complexidade: O(n²) tempo, O(n) espaço
        """
        if not arr:
            return 0
        
        n = len(arr)
        dp = [1] * n
        
        for i in range(1, n):
            for j in range(i):
                if arr[j] < arr[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        
        return max(dp)
    
    @staticmethod
    def lis_otimizada(arr: List[int]) -> int:
        """
        Longest Increasing Subsequence - O(n log n) usando busca binária.
        Complexidade: O(n log n) tempo, O(n) espaço
        """
        if not arr:
            return 0
        
        from bisect import bisect_left
        
        tails = []
        
        for num in arr:
            pos = bisect_left(tails, num)
            if pos == len(tails):
                tails.append(num)
            else:
                tails[pos] = num
        
        return len(tails)
    
    @staticmethod
    def edit_distance(str1: str, str2: str) -> int:
        """
        Edit Distance (Levenshtein Distance).
        Complexidade: O(m * n) tempo e espaço
        """
        m, n = len(str1), len(str2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Inicializar casos base
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Preencher tabela
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1]  # Sem operação
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j],    # Deletar
                        dp[i][j-1],    # Inserir
                        dp[i-1][j-1]   # Substituir
                    )
        
        return dp[m][n]


class ProblemasClassicos:
    """
    Outros problemas clássicos de programação dinâmica.
    """
    
    @staticmethod
    def coin_change_min_moedas(moedas: List[int], valor: int) -> int:
        """
        Coin Change - número mínimo de moedas.
        Complexidade: O(valor * len(moedas)) tempo, O(valor) espaço
        """
        dp = [float('inf')] * (valor + 1)
        dp[0] = 0
        
        for i in range(1, valor + 1):
            for moeda in moedas:
                if moeda <= i:
                    dp[i] = min(dp[i], dp[i - moeda] + 1)
        
        return dp[valor] if dp[valor] != float('inf') else -1
    
    @staticmethod
    def coin_change_formas(moedas: List[int], valor: int) -> int:
        """
        Coin Change - número de formas diferentes.
        Complexidade: O(valor * len(moedas)) tempo, O(valor) espaço
        """
        dp = [0] * (valor + 1)
        dp[0] = 1
        
        for moeda in moedas:
            for i in range(moeda, valor + 1):
                dp[i] += dp[i - moeda]
        
        return dp[valor]
    
    @staticmethod
    def maximum_subarray_kadane(arr: List[int]) -> Tuple[int, int, int]:
        """
        Maximum Subarray Sum (Algoritmo de Kadane).
        Complexidade: O(n) tempo, O(1) espaço
        
        Returns:
            Tupla (soma_maxima, inicio, fim)
        """
        if not arr:
            return 0, 0, 0
        
        max_ending_here = max_so_far = arr[0]
        inicio = fim = temp_inicio = 0
        
        for i in range(1, len(arr)):
            if max_ending_here < 0:
                max_ending_here = arr[i]
                temp_inicio = i
            else:
                max_ending_here += arr[i]
            
            if max_ending_here > max_so_far:
                max_so_far = max_ending_here
                inicio = temp_inicio
                fim = i
        
        return max_so_far, inicio, fim
    
    @staticmethod
    def matrix_chain_multiplication(dimensoes: List[int]) -> int:
        """
        Matrix Chain Multiplication - número mínimo de multiplicações.
        Complexidade: O(n³) tempo, O(n²) espaço
        
        Args:
            dimensoes: Lista onde dimensoes[i-1] x dimensoes[i] são as dimensões da matriz i
        """
        n = len(dimensoes) - 1  # Número de matrizes
        
        if n < 2:
            return 0
        
        # dp[i][j] = custo mínimo para multiplicar matrizes de i a j
        dp = [[0] * n for _ in range(n)]
        
        # l é o comprimento da cadeia
        for l in range(2, n + 1):
            for i in range(n - l + 1):
                j = i + l - 1
                dp[i][j] = float('inf')
                
                for k in range(i, j):
                    custo = (dp[i][k] + dp[k+1][j] + 
                            dimensoes[i] * dimensoes[k+1] * dimensoes[j+1])
                    dp[i][j] = min(dp[i][j], custo)
        
        return dp[0][n-1]
    
    @staticmethod
    def palindrome_partitioning(s: str) -> int:
        """
        Palindrome Partitioning - número mínimo de cortes.
        Complexidade: O(n³) tempo, O(n²) espaço
        """
        n = len(s)
        
        # Pré-computar quais substrings são palíndromos
        is_palindrome = [[False] * n for _ in range(n)]
        
        # Todo caractere único é palíndromo
        for i in range(n):
            is_palindrome[i][i] = True
        
        # Palíndromos de comprimento 2
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                is_palindrome[i][i + 1] = True
        
        # Palíndromos de comprimento 3 ou mais
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and is_palindrome[i + 1][j - 1]:
                    is_palindrome[i][j] = True
        
        # DP para encontrar número mínimo de cortes
        dp = [0] * n
        
        for i in range(n):
            if is_palindrome[0][i]:
                dp[i] = 0
            else:
                dp[i] = float('inf')
                for j in range(i):
                    if is_palindrome[j + 1][i]:
                        dp[i] = min(dp[i], dp[j] + 1)
        
        return dp[n - 1]


class AnalisadorPerformance:
    """
    Classe para análise de performance dos algoritmos de DP.
    """
    
    @staticmethod
    def comparar_fibonacci(n: int = 35):
        """Compara diferentes implementações de Fibonacci."""
        print(f"=== COMPARAÇÃO FIBONACCI (n={n}) ===\n")
        
        # Fibonacci recursivo simples (apenas para n pequeno)
        if n <= 35:
            start_time = time.time()
            resultado_recursivo = FibonacciDP.recursivo_simples(n)
            tempo_recursivo = time.time() - start_time
            print(f"Recursivo simples: {resultado_recursivo} ({tempo_recursivo:.4f}s)")
        
        # Fibonacci memoizado
        FibonacciDP.memoizado.cache_clear()
        start_time = time.time()
        resultado_memoizado = FibonacciDP.memoizado(n)
        tempo_memoizado = time.time() - start_time
        print(f"Memoizado: {resultado_memoizado} ({tempo_memoizado:.4f}s)")
        print(f"Cache info: {FibonacciDP.memoizado.cache_info()}")
        
        # Fibonacci tabulação
        start_time = time.time()
        resultado_tabulacao = FibonacciDP.tabulacao(n)
        tempo_tabulacao = time.time() - start_time
        print(f"Tabulação: {resultado_tabulacao} ({tempo_tabulacao:.4f}s)")
        
        # Fibonacci otimizado
        start_time = time.time()
        resultado_otimizado = FibonacciDP.otimizado_espaco(n)
        tempo_otimizado = time.time() - start_time
        print(f"Otimizado: {resultado_otimizado} ({tempo_otimizado:.4f}s)")
    
    @staticmethod
    def comparar_mochila():
        """Compara diferentes implementações da mochila."""
        print(f"\n=== COMPARAÇÃO MOCHILA ===\n")
        
        # Dados de teste
        pesos = [10, 20, 30]
        valores = [60, 100, 120]
        capacidade = 50
        
        print(f"Pesos: {pesos}")
        print(f"Valores: {valores}")
        print(f"Capacidade: {capacidade}\n")
        
        # Mochila recursiva
        start_time = time.time()
        resultado_recursivo = ProblemasMochila.mochila_01_recursiva(pesos, valores, capacidade)
        tempo_recursivo = time.time() - start_time
        print(f"Recursiva: {resultado_recursivo} ({tempo_recursivo:.4f}s)")
        
        # Mochila memoizada
        start_time = time.time()
        resultado_memoizado = ProblemasMochila.mochila_01_memoizada(pesos, valores, capacidade)
        tempo_memoizado = time.time() - start_time
        print(f"Memoizada: {resultado_memoizado} ({tempo_memoizado:.4f}s)")
        
        # Mochila tabulação
        start_time = time.time()
        resultado_tabulacao, itens = ProblemasMochila.mochila_01_tabulacao(pesos, valores, capacidade)
        tempo_tabulacao = time.time() - start_time
        print(f"Tabulação: {resultado_tabulacao} ({tempo_tabulacao:.4f}s)")
        print(f"Itens selecionados: {itens}")
        
        # Mochila otimizada
        start_time = time.time()
        resultado_otimizado = ProblemasMochila.mochila_01_otimizada(pesos, valores, capacidade)
        tempo_otimizado = time.time() - start_time
        print(f"Otimizada: {resultado_otimizado} ({tempo_otimizado:.4f}s)")


# Funções de Demonstração
def demonstrar_fibonacci():
    """Demonstra diferentes implementações de Fibonacci."""
    print("=== DEMONSTRAÇÃO: FIBONACCI ===\n")
    
    n = 10
    print(f"Calculando Fibonacci({n}):\n")
    
    # Diferentes implementações
    print(f"Recursivo simples: {FibonacciDP.recursivo_simples(n)}")
    print(f"Memoizado: {FibonacciDP.memoizado(n)}")
    print(f"Tabulação: {FibonacciDP.tabulacao(n)}")
    print(f"Otimizado: {FibonacciDP.otimizado_espaco(n)}")
    
    # Mostrar sequência
    print(f"\nSequência Fibonacci até {n}:")
    for i in range(n + 1):
        print(f"F({i}) = {FibonacciDP.otimizado_espaco(i)}")


def demonstrar_mochila():
    """Demonstra problema da mochila."""
    print("\n=== DEMONSTRAÇÃO: PROBLEMA DA MOCHILA ===\n")
    
    # Dados do problema
    pesos = [1, 3, 4, 5]
    valores = [1, 4, 5, 7]
    capacidade = 7
    
    print(f"Itens disponíveis:")
    for i, (p, v) in enumerate(zip(pesos, valores)):
        print(f"  Item {i}: peso={p}, valor={v}, razão={v/p:.2f}")
    
    print(f"\nCapacidade da mochila: {capacidade}")
    
    # Resolver com tabulação
    valor_maximo, itens_selecionados = ProblemasMochila.mochila_01_tabulacao(pesos, valores, capacidade)
    
    print(f"\nSolução ótima:")
    print(f"  Valor máximo: {valor_maximo}")
    print(f"  Itens selecionados: {itens_selecionados}")
    
    peso_total = sum(pesos[i] for i in itens_selecionados)
    print(f"  Peso total: {peso_total}/{capacidade}")
    
    # Comparar com mochila unbounded
    valor_unbounded = ProblemasMochila.mochila_unbounded(pesos, valores, capacidade)
    print(f"\nMochila Unbounded: {valor_unbounded}")


def demonstrar_sequencias():
    """Demonstra problemas de sequências."""
    print("\n=== DEMONSTRAÇÃO: PROBLEMAS DE SEQUÊNCIAS ===\n")
    
    # LCS
    texto1 = "ABCDGH"
    texto2 = "AEDFHR"
    
    comprimento_lcs, lcs = SequenciasDP.lcs_completa(texto1, texto2)
    print(f"LCS entre '{texto1}' e '{texto2}':")
    print(f"  Comprimento: {comprimento_lcs}")
    print(f"  Sequência: '{lcs}'")
    
    # LIS
    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    lis_len = SequenciasDP.lis_comprimento(arr)
    lis_len_opt = SequenciasDP.lis_otimizada(arr)
    
    print(f"\nLIS do array {arr}:")
    print(f"  Comprimento (O(n²)): {lis_len}")
    print(f"  Comprimento (O(n log n)): {lis_len_opt}")
    
    # Edit Distance
    str1 = "kitten"
    str2 = "sitting"
    distancia = SequenciasDP.edit_distance(str1, str2)
    
    print(f"\nEdit Distance entre '{str1}' e '{str2}': {distancia}")


def demonstrar_problemas_classicos():
    """Demonstra outros problemas clássicos."""
    print("\n=== DEMONSTRAÇÃO: PROBLEMAS CLÁSSICOS ===\n")
    
    # Coin Change
    moedas = [1, 3, 4]
    valor = 6
    
    min_moedas = ProblemasClassicos.coin_change_min_moedas(moedas, valor)
    formas = ProblemasClassicos.coin_change_formas(moedas, valor)
    
    print(f"Coin Change para valor {valor} com moedas {moedas}:")
    print(f"  Número mínimo de moedas: {min_moedas}")
    print(f"  Número de formas diferentes: {formas}")
    
    # Maximum Subarray
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    soma_max, inicio, fim = ProblemasClassicos.maximum_subarray_kadane(arr)
    
    print(f"\nMaximum Subarray do array {arr}:")
    print(f"  Soma máxima: {soma_max}")
    print(f"  Subarray: {arr[inicio:fim+1]} (índices {inicio}-{fim})")
    
    # Matrix Chain Multiplication
    dimensoes = [1, 2, 3, 4, 5]
    min_mult = ProblemasClassicos.matrix_chain_multiplication(dimensoes)
    
    print(f"\nMatrix Chain Multiplication:")
    print(f"  Dimensões das matrizes: {dimensoes}")
    print(f"  Número mínimo de multiplicações: {min_mult}")
    
    # Palindrome Partitioning
    s = "aab"
    min_cortes = ProblemasClassicos.palindrome_partitioning(s)
    
    print(f"\nPalindrome Partitioning da string '{s}':")
    print(f"  Número mínimo de cortes: {min_cortes}")


def benchmark_dp():
    """Executa benchmark dos algoritmos de DP."""
    print("\n=== BENCHMARK: PROGRAMAÇÃO DINÂMICA ===\n")
    
    # Comparar Fibonacci
    AnalisadorPerformance.comparar_fibonacci(35)
    
    # Comparar Mochila
    AnalisadorPerformance.comparar_mochila()
    
    # Teste de escalabilidade
    print(f"\n=== TESTE DE ESCALABILIDADE ===\n")
    
    tamanhos = [100, 500, 1000]
    
    for n in tamanhos:
        print(f"Fibonacci({n}):")
        
        # Memoizado
        FibonacciDP.memoizado.cache_clear()
        start_time = time.time()
        FibonacciDP.memoizado(n)
        tempo_memo = time.time() - start_time
        
        # Tabulação
        start_time = time.time()
        FibonacciDP.tabulacao(n)
        tempo_tab = time.time() - start_time
        
        # Otimizado
        start_time = time.time()
        FibonacciDP.otimizado_espaco(n)
        tempo_opt = time.time() - start_time
        
        print(f"  Memoizado: {tempo_memo:.4f}s")
        print(f"  Tabulação: {tempo_tab:.4f}s")
        print(f"  Otimizado: {tempo_opt:.4f}s")
        print()


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 06.1 - PROGRAMAÇÃO DINÂMICA")
    print("=" * 50)
    
    demonstrar_fibonacci()
    demonstrar_mochila()
    demonstrar_sequencias()
    demonstrar_problemas_classicos()
    benchmark_dp()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 06.1")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. PRINCÍPIOS FUNDAMENTAIS:
   • Subestrutura ótima: solução ótima contém soluções ótimas dos subproblemas
   • Sobreposição de subproblemas: mesmos subproblemas são resolvidos múltiplas vezes
   • Memoização vs Tabulação: top-down vs bottom-up

2. TÉCNICAS DE IMPLEMENTAÇÃO:
   • Memoização: cache automático com decoradores
   • Tabulação: construção iterativa da solução
   • Otimização de espaço: reduzir complexidade espacial

3. PROBLEMAS CLÁSSICOS RESOLVIDOS:
   • Fibonacci: O(2^n) → O(n) com DP
   • Mochila 0/1: otimização com restrições
   • LCS/LIS: problemas de sequências
   • Edit Distance: transformação de strings
   • Coin Change: problemas de contagem e otimização

4. ANÁLISE DE COMPLEXIDADE:
   • Temporal: geralmente O(n²) ou O(n³)
   • Espacial: pode ser otimizada de O(n²) para O(n)
   • Trade-off entre tempo e espaço

5. ESTRATÉGIAS DE OTIMIZAÇÃO:
   • Identificar estados desnecessários
   • Usar estruturas de dados eficientes
   • Aplicar técnicas de compressão de espaço
   • Pré-computar valores quando possível

6. APLICAÇÕES PRÁTICAS:
   • Algoritmos de alinhamento (bioinformática)
   • Otimização de recursos
   • Processamento de linguagem natural
   • Jogos e teoria dos jogos

7. PADRÕES DE DESIGN:
   • Estado e transição
   • Reconstrução de soluções
   • Memoização automática
   • Análise bottom-up vs top-down

A programação dinâmica é uma técnica poderosa que transforma
problemas exponenciais em polinomiais, sendo essencial para
otimização e resolução eficiente de problemas complexos.

Próximo arquivo: Algoritmos Gulosos
    """)


if __name__ == "__main__":
    main()