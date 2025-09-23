"""
MÓDULO 06.4 - DIVIDIR E CONQUISTAR
==================================

Objetivos de Aprendizado:
- Compreender o paradigma dividir e conquistar
- Implementar algoritmos clássicos de ordenação
- Analisar complexidade de algoritmos recursivos
- Otimizar com técnicas de divisão eficiente
- Aplicar em problemas de busca e multiplicação

Conceitos Abordados:
- Divisão do problema em subproblemas
- Resolução recursiva de subproblemas
- Combinação de soluções parciais
- Análise de complexidade com Master Theorem
- Otimizações e casos base
- Paralelização natural

Algoritmos Implementados:
- Merge Sort (ordenação por intercalação)
- Quick Sort (ordenação por particionamento)
- Binary Search (busca binária)
- Matrix Multiplication (Strassen)
- Maximum Subarray (Kadane recursivo)
- Closest Pair of Points
- Fast Fourier Transform (conceitual)
- Integer Multiplication (Karatsuba)

Pré-requisitos:
- Recursão avançada
- Análise de complexidade
- Estruturas de dados básicas

Complexidade Típica:
- Divisão: O(1) ou O(n)
- Conquista: T(n/2) ou T(n/k)
- Combinação: O(1) a O(n)
- Total: O(n log n) para casos balanceados
"""

from typing import List, Tuple, Optional, Any, Callable
import time
import random
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class TipoProblema(Enum):
    """Tipos de problemas dividir e conquistar."""
    ORDENACAO = "ordenacao"
    BUSCA = "busca"
    MULTIPLICACAO = "multiplicacao"
    GEOMETRICO = "geometrico"
    NUMERICO = "numerico"


@dataclass
class EstatisticasDC:
    """Estatísticas de algoritmos dividir e conquistar."""
    divisoes: int = 0
    comparacoes: int = 0
    trocas: int = 0
    combinacoes: int = 0
    profundidade_maxima: int = 0
    tempo_execucao: float = 0.0
    memoria_usada: int = 0
    
    def reset(self):
        """Reseta todas as estatísticas."""
        self.divisoes = 0
        self.comparacoes = 0
        self.trocas = 0
        self.combinacoes = 0
        self.profundidade_maxima = 0
        self.tempo_execucao = 0.0
        self.memoria_usada = 0


class DivideConquerBase(ABC):
    """
    Classe base para algoritmos dividir e conquistar.
    """
    
    def __init__(self):
        """Inicializa algoritmo dividir e conquistar."""
        self.stats = EstatisticasDC()
        self.debug = False
        self.limite_recursao = 1000
    
    @abstractmethod
    def caso_base(self, dados: Any) -> bool:
        """
        Verifica se é caso base (não precisa dividir).
        
        Args:
            dados: Dados do problema
        
        Returns:
            True se é caso base
        """
        pass
    
    @abstractmethod
    def resolver_caso_base(self, dados: Any) -> Any:
        """
        Resolve caso base diretamente.
        
        Args:
            dados: Dados do caso base
        
        Returns:
            Solução do caso base
        """
        pass
    
    @abstractmethod
    def dividir(self, dados: Any) -> List[Any]:
        """
        Divide problema em subproblemas.
        
        Args:
            dados: Dados do problema
        
        Returns:
            Lista de subproblemas
        """
        pass
    
    @abstractmethod
    def conquistar(self, subproblema: Any, profundidade: int) -> Any:
        """
        Resolve subproblema recursivamente.
        
        Args:
            subproblema: Dados do subproblema
            profundidade: Profundidade atual da recursão
        
        Returns:
            Solução do subproblema
        """
        pass
    
    @abstractmethod
    def combinar(self, solucoes: List[Any]) -> Any:
        """
        Combina soluções dos subproblemas.
        
        Args:
            solucoes: Lista de soluções parciais
        
        Returns:
            Solução combinada
        """
        pass
    
    def resolver(self, dados: Any) -> Any:
        """
        Resolve problema usando dividir e conquistar.
        
        Args:
            dados: Dados do problema
        
        Returns:
            Solução do problema
        """
        self.stats.reset()
        start_time = time.time()
        
        resultado = self._dc_recursivo(dados, 0)
        
        self.stats.tempo_execucao = time.time() - start_time
        return resultado
    
    def _dc_recursivo(self, dados: Any, profundidade: int) -> Any:
        """
        Função recursiva principal.
        
        Args:
            dados: Dados atuais
            profundidade: Profundidade da recursão
        
        Returns:
            Solução
        """
        self.stats.profundidade_maxima = max(self.stats.profundidade_maxima, profundidade)
        
        if self.debug:
            print(f"{'  ' * profundidade}Profundidade {profundidade}: {dados}")
        
        # Verificar limite de recursão
        if profundidade > self.limite_recursao:
            raise RecursionError(f"Limite de recursão excedido: {self.limite_recursao}")
        
        # Caso base
        if self.caso_base(dados):
            return self.resolver_caso_base(dados)
        
        # Dividir
        self.stats.divisoes += 1
        subproblemas = self.dividir(dados)
        
        # Conquistar
        solucoes = []
        for subproblema in subproblemas:
            solucao = self.conquistar(subproblema, profundidade + 1)
            solucoes.append(solucao)
        
        # Combinar
        self.stats.combinacoes += 1
        return self.combinar(solucoes)


class MergeSort(DivideConquerBase):
    """
    Implementação do Merge Sort usando dividir e conquistar.
    """
    
    def __init__(self):
        super().__init__()
        self.tipo = TipoProblema.ORDENACAO
    
    def caso_base(self, dados: List[Any]) -> bool:
        """Caso base: lista com 1 ou 0 elementos."""
        return len(dados) <= 1
    
    def resolver_caso_base(self, dados: List[Any]) -> List[Any]:
        """Retorna lista já ordenada (caso base)."""
        return dados.copy()
    
    def dividir(self, dados: List[Any]) -> List[List[Any]]:
        """Divide lista no meio."""
        meio = len(dados) // 2
        esquerda = dados[:meio]
        direita = dados[meio:]
        return [esquerda, direita]
    
    def conquistar(self, subproblema: List[Any], profundidade: int) -> List[Any]:
        """Resolve subproblema recursivamente."""
        return self._dc_recursivo(subproblema, profundidade)
    
    def combinar(self, solucoes: List[List[Any]]) -> List[Any]:
        """Intercala duas listas ordenadas."""
        esquerda, direita = solucoes[0], solucoes[1]
        resultado = []
        i = j = 0
        
        # Intercalar elementos
        while i < len(esquerda) and j < len(direita):
            self.stats.comparacoes += 1
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1
        
        # Adicionar elementos restantes
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        
        return resultado
    
    def ordenar(self, lista: List[Any]) -> List[Any]:
        """
        Ordena lista usando Merge Sort.
        
        Args:
            lista: Lista a ser ordenada
        
        Returns:
            Lista ordenada
        """
        return self.resolver(lista)


class QuickSort(DivideConquerBase):
    """
    Implementação do Quick Sort usando dividir e conquistar.
    """
    
    def __init__(self, estrategia_pivot: str = "ultimo"):
        super().__init__()
        self.tipo = TipoProblema.ORDENACAO
        self.estrategia_pivot = estrategia_pivot  # "primeiro", "ultimo", "meio", "aleatorio"
    
    def caso_base(self, dados: Tuple[List[Any], int, int]) -> bool:
        """Caso base: subarray com 1 ou 0 elementos."""
        lista, inicio, fim = dados
        return inicio >= fim
    
    def resolver_caso_base(self, dados: Tuple[List[Any], int, int]) -> List[Any]:
        """Retorna lista (caso base não modifica)."""
        lista, _, _ = dados
        return lista
    
    def dividir(self, dados: Tuple[List[Any], int, int]) -> List[Tuple[List[Any], int, int]]:
        """Particiona array em torno do pivot."""
        lista, inicio, fim = dados
        
        # Escolher pivot
        pivot_idx = self._escolher_pivot(lista, inicio, fim)
        
        # Mover pivot para o final
        lista[pivot_idx], lista[fim] = lista[fim], lista[pivot_idx]
        pivot = lista[fim]
        
        # Particionamento
        i = inicio - 1
        
        for j in range(inicio, fim):
            self.stats.comparacoes += 1
            if lista[j] <= pivot:
                i += 1
                if i != j:
                    lista[i], lista[j] = lista[j], lista[i]
                    self.stats.trocas += 1
        
        # Colocar pivot na posição correta
        lista[i + 1], lista[fim] = lista[fim], lista[i + 1]
        self.stats.trocas += 1
        
        pivot_final = i + 1
        
        # Retornar subproblemas
        return [
            (lista, inicio, pivot_final - 1),  # Esquerda
            (lista, pivot_final + 1, fim)      # Direita
        ]
    
    def _escolher_pivot(self, lista: List[Any], inicio: int, fim: int) -> int:
        """Escolhe índice do pivot baseado na estratégia."""
        if self.estrategia_pivot == "primeiro":
            return inicio
        elif self.estrategia_pivot == "ultimo":
            return fim
        elif self.estrategia_pivot == "meio":
            return (inicio + fim) // 2
        elif self.estrategia_pivot == "aleatorio":
            return random.randint(inicio, fim)
        else:
            return fim  # Default: último
    
    def conquistar(self, subproblema: Tuple[List[Any], int, int], profundidade: int) -> List[Any]:
        """Resolve subproblema recursivamente."""
        return self._dc_recursivo(subproblema, profundidade)
    
    def combinar(self, solucoes: List[List[Any]]) -> List[Any]:
        """Quick Sort ordena in-place, retorna primeira solução."""
        return solucoes[0] if solucoes else []
    
    def ordenar(self, lista: List[Any]) -> List[Any]:
        """
        Ordena lista usando Quick Sort.
        
        Args:
            lista: Lista a ser ordenada
        
        Returns:
            Lista ordenada (modificada in-place)
        """
        lista_copia = lista.copy()
        self.resolver((lista_copia, 0, len(lista_copia) - 1))
        return lista_copia


class BinarySearch(DivideConquerBase):
    """
    Implementação da busca binária usando dividir e conquistar.
    """
    
    def __init__(self):
        super().__init__()
        self.tipo = TipoProblema.BUSCA
        self.valor_procurado = None
    
    def caso_base(self, dados: Tuple[List[Any], int, int]) -> bool:
        """Caso base: subarray vazio ou elemento único."""
        lista, inicio, fim = dados
        return inicio > fim
    
    def resolver_caso_base(self, dados: Tuple[List[Any], int, int]) -> int:
        """Retorna -1 (não encontrado) ou índice se encontrou."""
        lista, inicio, fim = dados
        
        if inicio <= fim and inicio < len(lista):
            self.stats.comparacoes += 1
            if lista[inicio] == self.valor_procurado:
                return inicio
        
        return -1
    
    def dividir(self, dados: Tuple[List[Any], int, int]) -> List[Tuple[List[Any], int, int]]:
        """Divide array no meio baseado na comparação."""
        lista, inicio, fim = dados
        meio = (inicio + fim) // 2
        
        self.stats.comparacoes += 1
        if lista[meio] == self.valor_procurado:
            return [(lista, meio, meio)]  # Encontrou
        elif lista[meio] < self.valor_procurado:
            return [(lista, meio + 1, fim)]  # Buscar à direita
        else:
            return [(lista, inicio, meio - 1)]  # Buscar à esquerda
    
    def conquistar(self, subproblema: Tuple[List[Any], int, int], profundidade: int) -> int:
        """Resolve subproblema recursivamente."""
        return self._dc_recursivo(subproblema, profundidade)
    
    def combinar(self, solucoes: List[int]) -> int:
        """Retorna primeira solução (índice encontrado ou -1)."""
        return solucoes[0] if solucoes else -1
    
    def buscar(self, lista: List[Any], valor: Any) -> int:
        """
        Busca valor na lista ordenada.
        
        Args:
            lista: Lista ordenada
            valor: Valor a ser procurado
        
        Returns:
            Índice do valor ou -1 se não encontrado
        """
        self.valor_procurado = valor
        return self.resolver((lista, 0, len(lista) - 1))


class MatrixMultiplication(DivideConquerBase):
    """
    Multiplicação de matrizes usando algoritmo de Strassen.
    """
    
    def __init__(self, usar_strassen: bool = True):
        super().__init__()
        self.tipo = TipoProblema.MULTIPLICACAO
        self.usar_strassen = usar_strassen
        self.limite_strassen = 64  # Usar método tradicional para matrizes pequenas
    
    def caso_base(self, dados: Tuple[List[List[int]], List[List[int]]]) -> bool:
        """Caso base: matrizes pequenas."""
        A, B = dados
        n = len(A)
        return n <= self.limite_strassen or not self.usar_strassen
    
    def resolver_caso_base(self, dados: Tuple[List[List[int]], List[List[int]]]) -> List[List[int]]:
        """Multiplicação tradicional para caso base."""
        A, B = dados
        n = len(A)
        C = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
                    self.stats.comparacoes += 1
        
        return C
    
    def dividir(self, dados: Tuple[List[List[int]], List[List[int]]]) -> List[Tuple[List[List[int]], List[List[int]]]]:
        """Divide matrizes em quadrantes."""
        A, B = dados
        n = len(A)
        meio = n // 2
        
        # Dividir A em quadrantes
        A11 = [[A[i][j] for j in range(meio)] for i in range(meio)]
        A12 = [[A[i][j] for j in range(meio, n)] for i in range(meio)]
        A21 = [[A[i][j] for j in range(meio)] for i in range(meio, n)]
        A22 = [[A[i][j] for j in range(meio, n)] for i in range(meio, n)]
        
        # Dividir B em quadrantes
        B11 = [[B[i][j] for j in range(meio)] for i in range(meio)]
        B12 = [[B[i][j] for j in range(meio, n)] for i in range(meio)]
        B21 = [[B[i][j] for j in range(meio)] for i in range(meio, n)]
        B22 = [[B[i][j] for j in range(meio, n)] for i in range(meio, n)]
        
        if self.usar_strassen:
            # Algoritmo de Strassen - 7 multiplicações
            return [
                (self._somar_matrizes(A11, A22), self._somar_matrizes(B11, B22)),  # M1
                (self._somar_matrizes(A21, A22), B11),                              # M2
                (A11, self._subtrair_matrizes(B12, B22)),                          # M3
                (A22, self._subtrair_matrizes(B21, B11)),                          # M4
                (self._somar_matrizes(A11, A12), B22),                             # M5
                (self._subtrair_matrizes(A21, A11), self._somar_matrizes(B11, B12)), # M6
                (self._subtrair_matrizes(A12, A22), self._somar_matrizes(B21, B22))  # M7
            ]
        else:
            # Método tradicional - 8 multiplicações
            return [
                (A11, B11), (A12, B21),  # C11
                (A11, B12), (A12, B22),  # C12
                (A21, B11), (A22, B21),  # C21
                (A21, B12), (A22, B22)   # C22
            ]
    
    def conquistar(self, subproblema: Tuple[List[List[int]], List[List[int]]], profundidade: int) -> List[List[int]]:
        """Resolve multiplicação recursivamente."""
        return self._dc_recursivo(subproblema, profundidade)
    
    def combinar(self, solucoes: List[List[List[int]]]) -> List[List[int]]:
        """Combina resultados das multiplicações."""
        if self.usar_strassen and len(solucoes) == 7:
            # Algoritmo de Strassen
            M1, M2, M3, M4, M5, M6, M7 = solucoes
            
            # Calcular quadrantes do resultado
            C11 = self._somar_matrizes(
                self._subtrair_matrizes(self._somar_matrizes(M1, M4), M5), M7
            )
            C12 = self._somar_matrizes(M3, M5)
            C21 = self._somar_matrizes(M2, M4)
            C22 = self._somar_matrizes(
                self._subtrair_matrizes(self._somar_matrizes(M1, M3), M2), M6
            )
            
            return self._combinar_quadrantes(C11, C12, C21, C22)
        
        else:
            # Método tradicional
            n = len(solucoes[0])
            C = [[0] * (n * 2) for _ in range(n * 2)]
            
            # C11 = A11*B11 + A12*B21
            C11 = self._somar_matrizes(solucoes[0], solucoes[1])
            # C12 = A11*B12 + A12*B22
            C12 = self._somar_matrizes(solucoes[2], solucoes[3])
            # C21 = A21*B11 + A22*B21
            C21 = self._somar_matrizes(solucoes[4], solucoes[5])
            # C22 = A21*B12 + A22*B22
            C22 = self._somar_matrizes(solucoes[6], solucoes[7])
            
            return self._combinar_quadrantes(C11, C12, C21, C22)
    
    def _somar_matrizes(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        """Soma duas matrizes."""
        n = len(A)
        return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
    
    def _subtrair_matrizes(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        """Subtrai duas matrizes."""
        n = len(A)
        return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]
    
    def _combinar_quadrantes(self, C11: List[List[int]], C12: List[List[int]], 
                           C21: List[List[int]], C22: List[List[int]]) -> List[List[int]]:
        """Combina quadrantes em matriz completa."""
        n = len(C11)
        C = [[0] * (n * 2) for _ in range(n * 2)]
        
        for i in range(n):
            for j in range(n):
                C[i][j] = C11[i][j]
                C[i][j + n] = C12[i][j]
                C[i + n][j] = C21[i][j]
                C[i + n][j + n] = C22[i][j]
        
        return C
    
    def multiplicar(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        """
        Multiplica duas matrizes quadradas.
        
        Args:
            A: Primeira matriz
            B: Segunda matriz
        
        Returns:
            Produto A * B
        """
        # Verificar se matrizes são quadradas e de mesmo tamanho
        if len(A) != len(A[0]) or len(B) != len(B[0]) or len(A) != len(B):
            raise ValueError("Matrizes devem ser quadradas e de mesmo tamanho")
        
        # Garantir que tamanho é potência de 2 para Strassen
        n = len(A)
        if self.usar_strassen and n & (n - 1) != 0:
            # Expandir para próxima potência de 2
            nova_n = 1
            while nova_n < n:
                nova_n *= 2
            
            A = self._expandir_matriz(A, nova_n)
            B = self._expandir_matriz(B, nova_n)
        
        resultado = self.resolver((A, B))
        
        # Cortar resultado para tamanho original
        if self.usar_strassen and len(resultado) > n:
            resultado = [[resultado[i][j] for j in range(n)] for i in range(n)]
        
        return resultado
    
    def _expandir_matriz(self, matriz: List[List[int]], novo_tamanho: int) -> List[List[int]]:
        """Expande matriz com zeros para novo tamanho."""
        n = len(matriz)
        nova_matriz = [[0] * novo_tamanho for _ in range(novo_tamanho)]
        
        for i in range(n):
            for j in range(n):
                nova_matriz[i][j] = matriz[i][j]
        
        return nova_matriz


class MaximumSubarray(DivideConquerBase):
    """
    Encontra subarray com soma máxima usando dividir e conquistar.
    """
    
    def __init__(self):
        super().__init__()
        self.tipo = TipoProblema.NUMERICO
    
    def caso_base(self, dados: Tuple[List[int], int, int]) -> bool:
        """Caso base: array com um elemento."""
        array, inicio, fim = dados
        return inicio == fim
    
    def resolver_caso_base(self, dados: Tuple[List[int], int, int]) -> Tuple[int, int, int]:
        """Retorna (soma, inicio, fim) para elemento único."""
        array, inicio, fim = dados
        return (array[inicio], inicio, fim)
    
    def dividir(self, dados: Tuple[List[int], int, int]) -> List[Tuple[List[int], int, int]]:
        """Divide array no meio."""
        array, inicio, fim = dados
        meio = (inicio + fim) // 2
        
        return [
            (array, inicio, meio),      # Esquerda
            (array, meio + 1, fim)      # Direita
        ]
    
    def conquistar(self, subproblema: Tuple[List[int], int, int], profundidade: int) -> Tuple[int, int, int]:
        """Resolve subproblema recursivamente."""
        return self._dc_recursivo(subproblema, profundidade)
    
    def combinar(self, solucoes: List[Tuple[int, int, int]]) -> Tuple[int, int, int]:
        """Combina soluções considerando subarray que cruza o meio."""
        (soma_esq, inicio_esq, fim_esq), (soma_dir, inicio_dir, fim_dir) = solucoes
        
        # Encontrar subarray que cruza o meio
        array = self._array_atual
        meio = fim_esq
        
        # Máximo à esquerda do meio
        soma_esq_max = float('-inf')
        soma_atual = 0
        max_esq_idx = meio
        
        for i in range(meio, inicio_esq - 1, -1):
            soma_atual += array[i]
            if soma_atual > soma_esq_max:
                soma_esq_max = soma_atual
                max_esq_idx = i
        
        # Máximo à direita do meio
        soma_dir_max = float('-inf')
        soma_atual = 0
        max_dir_idx = meio + 1
        
        for i in range(meio + 1, fim_dir + 1):
            soma_atual += array[i]
            if soma_atual > soma_dir_max:
                soma_dir_max = soma_atual
                max_dir_idx = i
        
        soma_cruzada = soma_esq_max + soma_dir_max
        
        # Retornar melhor das três opções
        if soma_esq >= soma_dir and soma_esq >= soma_cruzada:
            return (soma_esq, inicio_esq, fim_esq)
        elif soma_dir >= soma_esq and soma_dir >= soma_cruzada:
            return (soma_dir, inicio_dir, fim_dir)
        else:
            return (soma_cruzada, max_esq_idx, max_dir_idx)
    
    def encontrar_subarray_maximo(self, array: List[int]) -> Tuple[int, int, int]:
        """
        Encontra subarray com soma máxima.
        
        Args:
            array: Array de inteiros
        
        Returns:
            Tupla (soma_maxima, indice_inicio, indice_fim)
        """
        self._array_atual = array  # Armazenar para uso em combinar
        return self.resolver((array, 0, len(array) - 1))


class ClosestPairPoints(DivideConquerBase):
    """
    Encontra par de pontos mais próximos usando dividir e conquistar.
    """
    
    def __init__(self):
        super().__init__()
        self.tipo = TipoProblema.GEOMETRICO
    
    def caso_base(self, dados: List[Tuple[float, float]]) -> bool:
        """Caso base: 3 ou menos pontos."""
        return len(dados) <= 3
    
    def resolver_caso_base(self, dados: List[Tuple[float, float]]) -> Tuple[float, Tuple[float, float], Tuple[float, float]]:
        """Força bruta para poucos pontos."""
        pontos = dados
        min_dist = float('inf')
        par_mais_proximo = (None, None)
        
        for i in range(len(pontos)):
            for j in range(i + 1, len(pontos)):
                dist = self._distancia(pontos[i], pontos[j])
                self.stats.comparacoes += 1
                if dist < min_dist:
                    min_dist = dist
                    par_mais_proximo = (pontos[i], pontos[j])
        
        return (min_dist, par_mais_proximo[0], par_mais_proximo[1])
    
    def dividir(self, dados: List[Tuple[float, float]]) -> List[List[Tuple[float, float]]]:
        """Divide pontos pela coordenada x."""
        pontos = sorted(dados, key=lambda p: p[0])  # Ordenar por x
        meio = len(pontos) // 2
        
        return [
            pontos[:meio],      # Esquerda
            pontos[meio:]       # Direita
        ]
    
    def conquistar(self, subproblema: List[Tuple[float, float]], profundidade: int) -> Tuple[float, Tuple[float, float], Tuple[float, float]]:
        """Resolve subproblema recursivamente."""
        return self._dc_recursivo(subproblema, profundidade)
    
    def combinar(self, solucoes: List[Tuple[float, Tuple[float, float], Tuple[float, float]]]) -> Tuple[float, Tuple[float, float], Tuple[float, float]]:
        """Combina soluções verificando pontos na faixa central."""
        (dist_esq, p1_esq, p2_esq), (dist_dir, p1_dir, p2_dir) = solucoes
        
        # Melhor distância das duas metades
        if dist_esq <= dist_dir:
            min_dist = dist_esq
            melhor_par = (p1_esq, p2_esq)
        else:
            min_dist = dist_dir
            melhor_par = (p1_dir, p2_dir)
        
        # Verificar pontos na faixa central
        pontos_esq = self._pontos_esquerda
        pontos_dir = self._pontos_direita
        linha_divisao = (pontos_esq[-1][0] + pontos_dir[0][0]) / 2
        
        # Pontos na faixa central
        faixa = []
        for ponto in pontos_esq + pontos_dir:
            if abs(ponto[0] - linha_divisao) < min_dist:
                faixa.append(ponto)
        
        # Ordenar por y
        faixa.sort(key=lambda p: p[1])
        
        # Verificar pontos próximos na faixa
        for i in range(len(faixa)):
            j = i + 1
            while j < len(faixa) and (faixa[j][1] - faixa[i][1]) < min_dist:
                dist = self._distancia(faixa[i], faixa[j])
                self.stats.comparacoes += 1
                if dist < min_dist:
                    min_dist = dist
                    melhor_par = (faixa[i], faixa[j])
                j += 1
        
        return (min_dist, melhor_par[0], melhor_par[1])
    
    def _distancia(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Calcula distância euclidiana entre dois pontos."""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def encontrar_par_mais_proximo(self, pontos: List[Tuple[float, float]]) -> Tuple[float, Tuple[float, float], Tuple[float, float]]:
        """
        Encontra par de pontos mais próximos.
        
        Args:
            pontos: Lista de pontos (x, y)
        
        Returns:
            Tupla (distancia_minima, ponto1, ponto2)
        """
        if len(pontos) < 2:
            raise ValueError("Necessário pelo menos 2 pontos")
        
        # Armazenar para uso em combinar
        pontos_ordenados = sorted(pontos, key=lambda p: p[0])
        meio = len(pontos_ordenados) // 2
        self._pontos_esquerda = pontos_ordenados[:meio]
        self._pontos_direita = pontos_ordenados[meio:]
        
        return self.resolver(pontos)


# Funções de Demonstração
def demonstrar_merge_sort():
    """Demonstra Merge Sort."""
    print("=== DEMONSTRAÇÃO: MERGE SORT ===\n")
    
    casos_teste = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 4, 6, 1, 3],
        [1],
        [],
        [3, 3, 3, 3]
    ]
    
    merge_sort = MergeSort()
    
    for i, lista in enumerate(casos_teste):
        print(f"Caso {i+1}: {lista}")
        
        start_time = time.time()
        resultado = merge_sort.ordenar(lista)
        tempo = time.time() - start_time
        
        print(f"  Resultado: {resultado}")
        print(f"  Tempo: {tempo:.6f}s")
        print(f"  Divisões: {merge_sort.stats.divisoes}")
        print(f"  Comparações: {merge_sort.stats.comparacoes}")
        print(f"  Profundidade: {merge_sort.stats.profundidade_maxima}")
        print()


def demonstrar_quick_sort():
    """Demonstra Quick Sort com diferentes estratégias de pivot."""
    print("=== DEMONSTRAÇÃO: QUICK SORT ===\n")
    
    lista_teste = [64, 34, 25, 12, 22, 11, 90, 5, 77, 30]
    estrategias = ["primeiro", "ultimo", "meio", "aleatorio"]
    
    print(f"Lista original: {lista_teste}\n")
    
    for estrategia in estrategias:
        print(f"Estratégia de pivot: {estrategia}")
        
        quick_sort = QuickSort(estrategia)
        
        start_time = time.time()
        resultado = quick_sort.ordenar(lista_teste)
        tempo = time.time() - start_time
        
        print(f"  Resultado: {resultado}")
        print(f"  Tempo: {tempo:.6f}s")
        print(f"  Divisões: {quick_sort.stats.divisoes}")
        print(f"  Comparações: {quick_sort.stats.comparacoes}")
        print(f"  Trocas: {quick_sort.stats.trocas}")
        print(f"  Profundidade: {quick_sort.stats.profundidade_maxima}")
        print()


def demonstrar_binary_search():
    """Demonstra busca binária."""
    print("=== DEMONSTRAÇÃO: BINARY SEARCH ===\n")
    
    lista_ordenada = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    valores_busca = [7, 2, 19, 1, 20]
    
    print(f"Lista ordenada: {lista_ordenada}")
    print(f"Valores a buscar: {valores_busca}\n")
    
    binary_search = BinarySearch()
    
    for valor in valores_busca:
        start_time = time.time()
        indice = binary_search.buscar(lista_ordenada, valor)
        tempo = time.time() - start_time
        
        if indice != -1:
            print(f"Valor {valor}: encontrado no índice {indice}")
        else:
            print(f"Valor {valor}: não encontrado")
        
        print(f"  Tempo: {tempo:.6f}s")
        print(f"  Comparações: {binary_search.stats.comparacoes}")
        print(f"  Profundidade: {binary_search.stats.profundidade_maxima}")
        print()


def demonstrar_matrix_multiplication():
    """Demonstra multiplicação de matrizes."""
    print("=== DEMONSTRAÇÃO: MATRIX MULTIPLICATION ===\n")
    
    # Matrizes pequenas para teste
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    
    print("Matriz A:")
    for linha in A:
        print(f"  {linha}")
    
    print("\nMatriz B:")
    for linha in B:
        print(f"  {linha}")
    
    # Teste método tradicional
    print("\nMétodo Tradicional:")
    mult_tradicional = MatrixMultiplication(usar_strassen=False)
    
    start_time = time.time()
    resultado_trad = mult_tradicional.multiplicar(A, B)
    tempo_trad = time.time() - start_time
    
    print("Resultado:")
    for linha in resultado_trad:
        print(f"  {linha}")
    print(f"Tempo: {tempo_trad:.6f}s")
    print(f"Comparações: {mult_tradicional.stats.comparacoes}")
    
    # Teste Strassen (para matrizes maiores)
    print("\nAlgoritmo de Strassen (matriz 4x4):")
    
    # Criar matrizes 4x4
    A4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    B4 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    
    mult_strassen = MatrixMultiplication(usar_strassen=True)
    mult_strassen.limite_strassen = 2  # Forçar uso do Strassen
    
    start_time = time.time()
    resultado_strassen = mult_strassen.multiplicar(A4, B4)
    tempo_strassen = time.time() - start_time
    
    print("Resultado (A4 * I):")
    for linha in resultado_strassen:
        print(f"  {linha}")
    print(f"Tempo: {tempo_strassen:.6f}s")
    print(f"Divisões: {mult_strassen.stats.divisoes}")


def demonstrar_maximum_subarray():
    """Demonstra problema do subarray máximo."""
    print("\n=== DEMONSTRAÇÃO: MAXIMUM SUBARRAY ===\n")
    
    casos_teste = [
        [-2, 1, -3, 4, -1, 2, 1, -5, 4],
        [1, 2, 3, 4, 5],
        [-1, -2, -3, -4],
        [5],
        [-2, -1]
    ]
    
    max_subarray = MaximumSubarray()
    
    for i, array in enumerate(casos_teste):
        print(f"Caso {i+1}: {array}")
        
        start_time = time.time()
        soma, inicio, fim = max_subarray.encontrar_subarray_maximo(array)
        tempo = time.time() - start_time
        
        subarray = array[inicio:fim+1]
        
        print(f"  Subarray máximo: {subarray}")
        print(f"  Soma máxima: {soma}")
        print(f"  Índices: [{inicio}, {fim}]")
        print(f"  Tempo: {tempo:.6f}s")
        print(f"  Divisões: {max_subarray.stats.divisoes}")
        print()


def demonstrar_closest_pair():
    """Demonstra par de pontos mais próximos."""
    print("=== DEMONSTRAÇÃO: CLOSEST PAIR OF POINTS ===\n")
    
    # Gerar pontos aleatórios
    random.seed(42)
    pontos = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(10)]
    
    print("Pontos:")
    for i, ponto in enumerate(pontos):
        print(f"  P{i}: ({ponto[0]:.2f}, {ponto[1]:.2f})")
    
    closest_pair = ClosestPairPoints()
    
    start_time = time.time()
    distancia, p1, p2 = closest_pair.encontrar_par_mais_proximo(pontos)
    tempo = time.time() - start_time
    
    print(f"\nPar mais próximo:")
    print(f"  P1: ({p1[0]:.2f}, {p1[1]:.2f})")
    print(f"  P2: ({p2[0]:.2f}, {p2[1]:.2f})")
    print(f"  Distância: {distancia:.4f}")
    print(f"  Tempo: {tempo:.6f}s")
    print(f"  Divisões: {closest_pair.stats.divisoes}")
    print(f"  Comparações: {closest_pair.stats.comparacoes}")


def benchmark_divide_conquer():
    """Compara performance dos algoritmos."""
    print("\n=== BENCHMARK: DIVIDIR E CONQUISTAR ===\n")
    
    # Benchmark ordenação
    print("Benchmark Ordenação:")
    tamanhos = [100, 500, 1000]
    
    for n in tamanhos:
        lista = [random.randint(1, 1000) for _ in range(n)]
        
        # Merge Sort
        merge_sort = MergeSort()
        start_time = time.time()
        merge_sort.ordenar(lista.copy())
        tempo_merge = time.time() - start_time
        
        # Quick Sort
        quick_sort = QuickSort("aleatorio")
        start_time = time.time()
        quick_sort.ordenar(lista.copy())
        tempo_quick = time.time() - start_time
        
        print(f"  n={n}:")
        print(f"    Merge Sort: {tempo_merge:.4f}s, comparações: {merge_sort.stats.comparacoes}")
        print(f"    Quick Sort: {tempo_quick:.4f}s, comparações: {quick_sort.stats.comparacoes}")
    
    # Benchmark busca
    print("\nBenchmark Busca Binária:")
    for n in [1000, 10000, 100000]:
        lista_ordenada = list(range(n))
        valor = n // 2
        
        binary_search = BinarySearch()
        start_time = time.time()
        binary_search.buscar(lista_ordenada, valor)
        tempo = time.time() - start_time
        
        print(f"  n={n}: {tempo:.6f}s, comparações: {binary_search.stats.comparacoes}")


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 06.4 - DIVIDIR E CONQUISTAR")
    print("=" * 50)
    
    demonstrar_merge_sort()
    demonstrar_quick_sort()
    demonstrar_binary_search()
    demonstrar_matrix_multiplication()
    demonstrar_maximum_subarray()
    demonstrar_closest_pair()
    benchmark_divide_conquer()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 06.4")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. PARADIGMA DIVIDIR E CONQUISTAR:
   • Divisão: quebrar problema em subproblemas menores
   • Conquista: resolver subproblemas recursivamente
   • Combinação: unir soluções para resolver problema original
   • Casos base: condições de parada da recursão

2. ALGORITMOS CLÁSSICOS IMPLEMENTADOS:
   • Merge Sort: ordenação estável O(n log n)
   • Quick Sort: ordenação in-place O(n log n) médio
   • Binary Search: busca eficiente O(log n)
   • Matrix Multiplication: Strassen O(n^2.807)
   • Maximum Subarray: soma máxima O(n log n)
   • Closest Pair: geometria computacional O(n log n)

3. ANÁLISE DE COMPLEXIDADE:
   • Master Theorem para recorrências
   • T(n) = aT(n/b) + f(n)
   • Casos: f(n) dominante, balanceado, ou recursão dominante
   • Merge Sort: T(n) = 2T(n/2) + O(n) = O(n log n)
   • Quick Sort: T(n) = 2T(n/2) + O(n) = O(n log n) médio

4. VANTAGENS DO PARADIGMA:
   • Complexidade ótima para muitos problemas
   • Paralelização natural (subproblemas independentes)
   • Estrutura recursiva elegante
   • Reutilização de soluções de subproblemas

5. TÉCNICAS DE OTIMIZAÇÃO:
   • Escolha inteligente de pivot (Quick Sort)
   • Limite para casos base (evitar overhead)
   • Algoritmo de Strassen para multiplicação
   • Poda geométrica (Closest Pair)

6. ESTRATÉGIAS DE IMPLEMENTAÇÃO:
   • Template method pattern para estrutura comum
   • Separação clara entre divisão, conquista e combinação
   • Tratamento cuidadoso de casos base
   • Controle de profundidade de recursão

7. COMPARAÇÃO ENTRE ALGORITMOS:
   • Merge Sort: estável, O(n log n) garantido, O(n) espaço
   • Quick Sort: in-place, O(n log n) médio, O(n²) pior caso
   • Binary Search: O(log n), requer array ordenado
   • Strassen: melhor que O(n³) para matrizes grandes

8. APLICAÇÕES PRÁTICAS:
   • Ordenação de grandes datasets
   • Busca em bases de dados indexadas
   • Processamento de imagens (FFT)
   • Geometria computacional
   • Multiplicação de números grandes

9. LIMITAÇÕES E CONSIDERAÇÕES:
   • Overhead de recursão para problemas pequenos
   • Uso de memória para pilha de chamadas
   • Nem todos os problemas se beneficiam da divisão
   • Balanceamento importante para eficiência

10. HEURÍSTICAS IMPORTANTES:
    • Pivot aleatório para evitar pior caso
    • Híbrido com insertion sort para arrays pequenos
    • Iterativo vs recursivo para controle de memória
    • Paralelização de subproblemas independentes

11. ESTRUTURAS DE DADOS AUXILIARES:
    • Arrays temporários para merge
    • Pilha implícita de recursão
    • Índices para delimitar subproblemas
    • Estruturas para combinar resultados

12. PADRÕES DE DESIGN:
    • Template Method: estrutura comum
    • Strategy: diferentes estratégias de divisão
    • Factory: criação de algoritmos específicos
    • Observer: monitoramento de estatísticas

O paradigma dividir e conquistar é fundamental na ciência da
computação, fornecendo soluções elegantes e eficientes para
uma ampla gama de problemas. A chave está em identificar
como dividir o problema de forma balanceada e como combinar
as soluções eficientemente.

Próximo arquivo: Teoria de Grafos Avançada
    """)


if __name__ == "__main__":
    main()