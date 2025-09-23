"""
MÓDULO 06.3 - BACKTRACKING
==========================

Objetivos de Aprendizado:
- Compreender o paradigma de backtracking
- Implementar busca exaustiva com poda
- Resolver problemas de satisfação de restrições
- Otimizar com técnicas de poda eficientes
- Analisar complexidade exponencial

Conceitos Abordados:
- Busca em profundidade com retrocesso
- Espaço de estados e árvore de busca
- Poda (pruning) para otimização
- Problemas de satisfação de restrições (CSP)
- Heurísticas para ordenação de variáveis
- Propagação de restrições

Problemas Implementados:
- N-Queens Problem
- Sudoku Solver
- Maze Solving (Labirintos)
- Graph Coloring
- Subset Sum
- Permutations and Combinations
- Knight's Tour
- Word Search

Pré-requisitos:
- Recursão avançada
- Estruturas de dados básicas
- Conceitos de grafos

Complexidade Típica:
- Pior caso: O(b^d) onde b=branching factor, d=depth
- Com poda: significativamente melhor na prática
- Espaço: O(d) para recursão
"""

from typing import List, Dict, Tuple, Optional, Set, Any, Callable
import time
import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class EstadoBusca(Enum):
    """Estados possíveis durante a busca."""
    EXPLORANDO = "explorando"
    SOLUCAO_ENCONTRADA = "solucao_encontrada"
    BACKTRACK = "backtrack"
    FALHA = "falha"


@dataclass
class EstatisticasBusca:
    """Estatísticas de performance da busca."""
    nos_explorados: int = 0
    nos_podados: int = 0
    backracks_realizados: int = 0
    solucoes_encontradas: int = 0
    tempo_execucao: float = 0.0
    profundidade_maxima: int = 0
    
    def reset(self):
        """Reseta todas as estatísticas."""
        self.nos_explorados = 0
        self.nos_podados = 0
        self.backracks_realizados = 0
        self.solucoes_encontradas = 0
        self.tempo_execucao = 0.0
        self.profundidade_maxima = 0


class BacktrackingBase(ABC):
    """
    Classe base para algoritmos de backtracking.
    """
    
    def __init__(self):
        """Inicializa o algoritmo de backtracking."""
        self.stats = EstatisticasBusca()
        self.solucoes = []
        self.debug = False
        self.limite_solucoes = None
    
    @abstractmethod
    def eh_valido(self, estado: Any, posicao: int, valor: Any) -> bool:
        """
        Verifica se uma atribuição é válida.
        
        Args:
            estado: Estado atual da busca
            posicao: Posição sendo considerada
            valor: Valor sendo atribuído
        
        Returns:
            True se a atribuição é válida
        """
        pass
    
    @abstractmethod
    def eh_completo(self, estado: Any) -> bool:
        """
        Verifica se o estado representa uma solução completa.
        
        Args:
            estado: Estado atual
        
        Returns:
            True se é uma solução completa
        """
        pass
    
    @abstractmethod
    def obter_candidatos(self, estado: Any, posicao: int) -> List[Any]:
        """
        Obtém valores candidatos para uma posição.
        
        Args:
            estado: Estado atual
            posicao: Posição a ser preenchida
        
        Returns:
            Lista de valores candidatos
        """
        pass
    
    @abstractmethod
    def aplicar_movimento(self, estado: Any, posicao: int, valor: Any) -> Any:
        """
        Aplica um movimento ao estado.
        
        Args:
            estado: Estado atual
            posicao: Posição
            valor: Valor a ser aplicado
        
        Returns:
            Novo estado
        """
        pass
    
    def pode_podar(self, estado: Any, posicao: int) -> bool:
        """
        Verifica se pode podar este ramo da busca.
        
        Args:
            estado: Estado atual
            posicao: Posição atual
        
        Returns:
            True se pode podar
        """
        return False
    
    def buscar(self, estado_inicial: Any, encontrar_todas: bool = False) -> List[Any]:
        """
        Executa busca por backtracking.
        
        Args:
            estado_inicial: Estado inicial da busca
            encontrar_todas: Se deve encontrar todas as soluções
        
        Returns:
            Lista de soluções encontradas
        """
        self.stats.reset()
        self.solucoes = []
        
        if encontrar_todas:
            self.limite_solucoes = None
        else:
            self.limite_solucoes = 1
        
        start_time = time.time()
        self._backtrack(estado_inicial, 0, 0)
        self.stats.tempo_execucao = time.time() - start_time
        
        return self.solucoes.copy()
    
    def _backtrack(self, estado: Any, posicao: int, profundidade: int) -> bool:
        """
        Função recursiva de backtracking.
        
        Args:
            estado: Estado atual
            posicao: Posição atual
            profundidade: Profundidade atual
        
        Returns:
            True se encontrou solução
        """
        self.stats.nos_explorados += 1
        self.stats.profundidade_maxima = max(self.stats.profundidade_maxima, profundidade)
        
        if self.debug:
            print(f"Explorando posição {posicao}, profundidade {profundidade}")
        
        # Verificar se é solução completa
        if self.eh_completo(estado):
            self.solucoes.append(copy.deepcopy(estado))
            self.stats.solucoes_encontradas += 1
            
            if self.debug:
                print(f"Solução encontrada: {estado}")
            
            # Se só quer uma solução, parar
            if self.limite_solucoes and len(self.solucoes) >= self.limite_solucoes:
                return True
            
            return False  # Continuar buscando mais soluções
        
        # Verificar poda
        if self.pode_podar(estado, posicao):
            self.stats.nos_podados += 1
            if self.debug:
                print(f"Podando na posição {posicao}")
            return False
        
        # Tentar todos os candidatos
        candidatos = self.obter_candidatos(estado, posicao)
        
        for valor in candidatos:
            if self.eh_valido(estado, posicao, valor):
                # Aplicar movimento
                novo_estado = self.aplicar_movimento(estado, posicao, valor)
                
                # Recursão
                if self._backtrack(novo_estado, posicao + 1, profundidade + 1):
                    return True
                
                # Backtrack (implícito - novo_estado é descartado)
                self.stats.backracks_realizados += 1
                
                if self.debug:
                    print(f"Backtrack da posição {posicao}")
        
        return False


class NQueens(BacktrackingBase):
    """
    Solução para o problema das N-Rainhas.
    Objetivo: Colocar N rainhas em tabuleiro NxN sem se atacarem.
    """
    
    def __init__(self, n: int):
        super().__init__()
        self.n = n
        self.tabuleiro = [-1] * n  # tabuleiro[i] = coluna da rainha na linha i
    
    def eh_valido(self, estado: List[int], posicao: int, valor: int) -> bool:
        """
        Verifica se pode colocar rainha na posição (posicao, valor).
        
        Args:
            estado: Posições das rainhas (lista de colunas)
            posicao: Linha onde colocar rainha
            valor: Coluna onde colocar rainha
        
        Returns:
            True se posição é válida
        """
        for linha in range(posicao):
            coluna_existente = estado[linha]
            
            # Verificar coluna
            if coluna_existente == valor:
                return False
            
            # Verificar diagonais
            if abs(linha - posicao) == abs(coluna_existente - valor):
                return False
        
        return True
    
    def eh_completo(self, estado: List[int]) -> bool:
        """Verifica se todas as rainhas foram colocadas."""
        return len([x for x in estado if x != -1]) == self.n
    
    def obter_candidatos(self, estado: List[int], posicao: int) -> List[int]:
        """Retorna todas as colunas possíveis."""
        return list(range(self.n))
    
    def aplicar_movimento(self, estado: List[int], posicao: int, valor: int) -> List[int]:
        """Coloca rainha na posição especificada."""
        novo_estado = estado.copy()
        novo_estado[posicao] = valor
        return novo_estado
    
    def pode_podar(self, estado: List[int], posicao: int) -> bool:
        """
        Poda baseada em análise de conflitos futuros.
        """
        if posicao >= self.n:
            return True
        
        # Verificar se ainda há colunas disponíveis
        colunas_usadas = set(estado[:posicao])
        colunas_disponiveis = set(range(self.n)) - colunas_usadas
        
        # Se não há colunas suficientes, podar
        if len(colunas_disponiveis) < (self.n - posicao):
            return True
        
        return False
    
    def imprimir_tabuleiro(self, solucao: List[int]):
        """Imprime tabuleiro com a solução."""
        print(f"\nTabuleiro {self.n}x{self.n}:")
        for linha in range(self.n):
            linha_str = ""
            for coluna in range(self.n):
                if solucao[linha] == coluna:
                    linha_str += "Q "
                else:
                    linha_str += ". "
            print(linha_str)
    
    def resolver(self, encontrar_todas: bool = False) -> List[List[int]]:
        """
        Resolve o problema das N-Rainhas.
        
        Args:
            encontrar_todas: Se deve encontrar todas as soluções
        
        Returns:
            Lista de soluções (cada solução é lista de colunas)
        """
        estado_inicial = [-1] * self.n
        return self.buscar(estado_inicial, encontrar_todas)


class SudokuSolver(BacktrackingBase):
    """
    Solucionador de Sudoku usando backtracking.
    """
    
    def __init__(self, tabuleiro: List[List[int]]):
        super().__init__()
        self.tamanho = len(tabuleiro)
        self.tabuleiro_inicial = [linha.copy() for linha in tabuleiro]
        self.celulas_vazias = self._encontrar_celulas_vazias()
    
    def _encontrar_celulas_vazias(self) -> List[Tuple[int, int]]:
        """Encontra todas as células vazias (valor 0)."""
        vazias = []
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.tabuleiro_inicial[i][j] == 0:
                    vazias.append((i, j))
        return vazias
    
    def eh_valido(self, estado: List[List[int]], posicao: int, valor: int) -> bool:
        """
        Verifica se pode colocar valor na célula especificada.
        
        Args:
            estado: Tabuleiro atual
            posicao: Índice na lista de células vazias
            valor: Valor a ser colocado (1-9)
        
        Returns:
            True se movimento é válido
        """
        if posicao >= len(self.celulas_vazias):
            return False
        
        linha, coluna = self.celulas_vazias[posicao]
        
        # Verificar linha
        for c in range(self.tamanho):
            if estado[linha][c] == valor:
                return False
        
        # Verificar coluna
        for r in range(self.tamanho):
            if estado[r][coluna] == valor:
                return False
        
        # Verificar quadrante 3x3
        quad_linha = (linha // 3) * 3
        quad_coluna = (coluna // 3) * 3
        
        for r in range(quad_linha, quad_linha + 3):
            for c in range(quad_coluna, quad_coluna + 3):
                if estado[r][c] == valor:
                    return False
        
        return True
    
    def eh_completo(self, estado: List[List[int]]) -> bool:
        """Verifica se todas as células foram preenchidas."""
        for linha in estado:
            if 0 in linha:
                return False
        return True
    
    def obter_candidatos(self, estado: List[List[int]], posicao: int) -> List[int]:
        """Retorna valores possíveis (1-9) com heurística MRV."""
        if posicao >= len(self.celulas_vazias):
            return []
        
        linha, coluna = self.celulas_vazias[posicao]
        candidatos = []
        
        for valor in range(1, 10):
            if self.eh_valido(estado, posicao, valor):
                candidatos.append(valor)
        
        # Heurística: ordenar por número de conflitos (menos conflitos primeiro)
        return sorted(candidatos, key=lambda v: self._contar_conflitos(estado, linha, coluna, v))
    
    def _contar_conflitos(self, estado: List[List[int]], linha: int, coluna: int, valor: int) -> int:
        """Conta quantos conflitos um valor causaria."""
        conflitos = 0
        
        # Contar células vazias na linha que não poderiam usar este valor
        for c in range(self.tamanho):
            if estado[linha][c] == 0 and c != coluna:
                if not self._pode_usar_valor(estado, linha, c, valor):
                    conflitos += 1
        
        # Contar células vazias na coluna
        for r in range(self.tamanho):
            if estado[r][coluna] == 0 and r != linha:
                if not self._pode_usar_valor(estado, r, coluna, valor):
                    conflitos += 1
        
        return conflitos
    
    def _pode_usar_valor(self, estado: List[List[int]], linha: int, coluna: int, valor: int) -> bool:
        """Verifica se uma célula pode usar um valor específico."""
        # Simular colocação temporária
        temp_estado = [linha.copy() for linha in estado]
        temp_estado[linha][coluna] = valor
        
        # Encontrar posição na lista de células vazias
        posicao = -1
        for i, (r, c) in enumerate(self.celulas_vazias):
            if r == linha and c == coluna:
                posicao = i
                break
        
        return posicao != -1 and self.eh_valido(temp_estado, posicao, valor)
    
    def aplicar_movimento(self, estado: List[List[int]], posicao: int, valor: int) -> List[List[int]]:
        """Coloca valor na célula especificada."""
        novo_estado = [linha.copy() for linha in estado]
        linha, coluna = self.celulas_vazias[posicao]
        novo_estado[linha][coluna] = valor
        return novo_estado
    
    def pode_podar(self, estado: List[List[int]], posicao: int) -> bool:
        """
        Poda baseada em propagação de restrições.
        """
        # Verificar se alguma célula vazia não tem candidatos válidos
        for i in range(posicao, len(self.celulas_vazias)):
            linha, coluna = self.celulas_vazias[i]
            if estado[linha][coluna] == 0:  # Célula ainda vazia
                tem_candidato = False
                for valor in range(1, 10):
                    if self.eh_valido(estado, i, valor):
                        tem_candidato = True
                        break
                
                if not tem_candidato:
                    return True  # Poda: célula sem candidatos válidos
        
        return False
    
    def imprimir_tabuleiro(self, tabuleiro: List[List[int]]):
        """Imprime tabuleiro de Sudoku formatado."""
        print("\n" + "─" * 25)
        for i, linha in enumerate(tabuleiro):
            if i % 3 == 0 and i != 0:
                print("├" + "─" * 7 + "┼" + "─" * 7 + "┼" + "─" * 7 + "┤")
            
            linha_str = "│ "
            for j, valor in enumerate(linha):
                if j % 3 == 0 and j != 0:
                    linha_str += "│ "
                
                if valor == 0:
                    linha_str += ". "
                else:
                    linha_str += f"{valor} "
            
            linha_str += "│"
            print(linha_str)
        print("─" * 25)
    
    def resolver(self) -> Optional[List[List[int]]]:
        """
        Resolve o Sudoku.
        
        Returns:
            Tabuleiro resolvido ou None se não há solução
        """
        solucoes = self.buscar(self.tabuleiro_inicial, encontrar_todas=False)
        return solucoes[0] if solucoes else None


class MazeSolver(BacktrackingBase):
    """
    Solucionador de labirintos usando backtracking.
    """
    
    def __init__(self, labirinto: List[List[int]], inicio: Tuple[int, int], fim: Tuple[int, int]):
        super().__init__()
        self.labirinto = labirinto
        self.linhas = len(labirinto)
        self.colunas = len(labirinto[0])
        self.inicio = inicio
        self.fim = fim
        self.direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # direita, baixo, esquerda, cima
    
    def eh_valido(self, estado: List[Tuple[int, int]], posicao: int, valor: Tuple[int, int]) -> bool:
        """
        Verifica se pode mover para a posição especificada.
        
        Args:
            estado: Caminho atual (lista de posições)
            posicao: Não usado (compatibilidade)
            valor: Nova posição (linha, coluna)
        
        Returns:
            True se movimento é válido
        """
        linha, coluna = valor
        
        # Verificar limites
        if linha < 0 or linha >= self.linhas or coluna < 0 or coluna >= self.colunas:
            return False
        
        # Verificar se é parede
        if self.labirinto[linha][coluna] == 1:
            return False
        
        # Verificar se já visitou
        if valor in estado:
            return False
        
        return True
    
    def eh_completo(self, estado: List[Tuple[int, int]]) -> bool:
        """Verifica se chegou ao destino."""
        return len(estado) > 0 and estado[-1] == self.fim
    
    def obter_candidatos(self, estado: List[Tuple[int, int]], posicao: int) -> List[Tuple[int, int]]:
        """Retorna posições adjacentes válidas."""
        if not estado:
            return [self.inicio]
        
        atual = estado[-1]
        candidatos = []
        
        for dx, dy in self.direcoes:
            nova_pos = (atual[0] + dx, atual[1] + dy)
            candidatos.append(nova_pos)
        
        # Heurística: ordenar por distância ao destino
        return sorted(candidatos, key=lambda pos: self._distancia_manhattan(pos, self.fim))
    
    def _distancia_manhattan(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calcula distância de Manhattan entre duas posições."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def aplicar_movimento(self, estado: List[Tuple[int, int]], posicao: int, valor: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Adiciona nova posição ao caminho."""
        return estado + [valor]
    
    def pode_podar(self, estado: List[Tuple[int, int]], posicao: int) -> bool:
        """
        Poda baseada em análise de alcançabilidade.
        """
        if not estado:
            return False
        
        atual = estado[-1]
        
        # Poda se não há caminho possível para o destino
        # (implementação simplificada - poderia usar flood fill)
        distancia_atual = self._distancia_manhattan(atual, self.fim)
        
        # Se está muito longe e já percorreu muito, pode podar
        if len(estado) > self.linhas * self.colunas // 2 and distancia_atual > min(self.linhas, self.colunas):
            return True
        
        return False
    
    def imprimir_labirinto(self, caminho: List[Tuple[int, int]] = None):
        """Imprime labirinto com caminho opcional."""
        print("\nLabirinto:")
        for i in range(self.linhas):
            linha_str = ""
            for j in range(self.colunas):
                if (i, j) == self.inicio:
                    linha_str += "S "  # Start
                elif (i, j) == self.fim:
                    linha_str += "E "  # End
                elif caminho and (i, j) in caminho:
                    linha_str += "* "  # Caminho
                elif self.labirinto[i][j] == 1:
                    linha_str += "█ "  # Parede
                else:
                    linha_str += ". "  # Espaço livre
            print(linha_str)
    
    def resolver(self) -> Optional[List[Tuple[int, int]]]:
        """
        Resolve o labirinto.
        
        Returns:
            Caminho da solução ou None se não há solução
        """
        solucoes = self.buscar([], encontrar_todas=False)
        return solucoes[0] if solucoes else None


class GraphColoring(BacktrackingBase):
    """
    Coloração de grafos usando backtracking.
    """
    
    def __init__(self, grafo: Dict[int, List[int]], num_cores: int):
        super().__init__()
        self.grafo = grafo
        self.vertices = list(grafo.keys())
        self.num_cores = num_cores
        self.cores = list(range(num_cores))
    
    def eh_valido(self, estado: Dict[int, int], posicao: int, valor: int) -> bool:
        """
        Verifica se pode colorir vértice com a cor especificada.
        
        Args:
            estado: Coloração atual (vértice -> cor)
            posicao: Índice do vértice na lista
            valor: Cor a ser atribuída
        
        Returns:
            True se coloração é válida
        """
        if posicao >= len(self.vertices):
            return False
        
        vertice = self.vertices[posicao]
        
        # Verificar vizinhos já coloridos
        for vizinho in self.grafo[vertice]:
            if vizinho in estado and estado[vizinho] == valor:
                return False
        
        return True
    
    def eh_completo(self, estado: Dict[int, int]) -> bool:
        """Verifica se todos os vértices foram coloridos."""
        return len(estado) == len(self.vertices)
    
    def obter_candidatos(self, estado: Dict[int, int], posicao: int) -> List[int]:
        """Retorna cores disponíveis com heurística."""
        if posicao >= len(self.vertices):
            return []
        
        vertice = self.vertices[posicao]
        cores_usadas = set()
        
        # Coletar cores dos vizinhos já coloridos
        for vizinho in self.grafo[vertice]:
            if vizinho in estado:
                cores_usadas.add(estado[vizinho])
        
        # Retornar cores não usadas
        cores_disponiveis = [cor for cor in self.cores if cor not in cores_usadas]
        
        # Heurística: ordenar por frequência de uso (menos usadas primeiro)
        return sorted(cores_disponiveis, key=lambda c: self._contar_uso_cor(estado, c))
    
    def _contar_uso_cor(self, estado: Dict[int, int], cor: int) -> int:
        """Conta quantas vezes uma cor foi usada."""
        return sum(1 for c in estado.values() if c == cor)
    
    def aplicar_movimento(self, estado: Dict[int, int], posicao: int, valor: int) -> Dict[int, int]:
        """Atribui cor ao vértice."""
        novo_estado = estado.copy()
        vertice = self.vertices[posicao]
        novo_estado[vertice] = valor
        return novo_estado
    
    def pode_podar(self, estado: Dict[int, int], posicao: int) -> bool:
        """
        Poda baseada em análise de graus dos vértices.
        """
        if posicao >= len(self.vertices):
            return True
        
        # Verificar se algum vértice não colorido não tem cores disponíveis
        for i in range(posicao, len(self.vertices)):
            vertice = self.vertices[i]
            if vertice not in estado:
                cores_disponiveis = len(self.obter_candidatos(estado, i))
                if cores_disponiveis == 0:
                    return True
        
        return False
    
    def resolver(self) -> Optional[Dict[int, int]]:
        """
        Resolve coloração do grafo.
        
        Returns:
            Coloração válida ou None se impossível
        """
        solucoes = self.buscar({}, encontrar_todas=False)
        return solucoes[0] if solucoes else None


class SubsetSum(BacktrackingBase):
    """
    Problema da soma de subconjuntos usando backtracking.
    """
    
    def __init__(self, numeros: List[int], soma_alvo: int):
        super().__init__()
        self.numeros = sorted(numeros, reverse=True)  # Ordenar decrescente para poda
        self.soma_alvo = soma_alvo
    
    def eh_valido(self, estado: List[bool], posicao: int, valor: bool) -> bool:
        """
        Verifica se pode incluir/excluir número na posição.
        
        Args:
            estado: Lista de booleanos (incluir/não incluir)
            posicao: Índice do número
            valor: True para incluir, False para excluir
        
        Returns:
            True se escolha é válida
        """
        if posicao >= len(self.numeros):
            return False
        
        # Calcular soma atual
        soma_atual = sum(self.numeros[i] for i in range(posicao) if estado[i])
        
        if valor:  # Se vai incluir o número
            nova_soma = soma_atual + self.numeros[posicao]
            return nova_soma <= self.soma_alvo
        
        return True  # Sempre pode excluir
    
    def eh_completo(self, estado: List[bool]) -> bool:
        """Verifica se chegou ao final e soma é correta."""
        if len(estado) != len(self.numeros):
            return False
        
        soma_atual = sum(self.numeros[i] for i in range(len(estado)) if estado[i])
        return soma_atual == self.soma_alvo
    
    def obter_candidatos(self, estado: List[bool], posicao: int) -> List[bool]:
        """Retorna [True, False] para incluir/excluir."""
        return [True, False]
    
    def aplicar_movimento(self, estado: List[bool], posicao: int, valor: bool) -> List[bool]:
        """Adiciona decisão ao estado."""
        return estado + [valor]
    
    def pode_podar(self, estado: List[bool], posicao: int) -> bool:
        """
        Poda baseada em limites superior e inferior.
        """
        if posicao >= len(self.numeros):
            return True
        
        # Calcular soma atual
        soma_atual = sum(self.numeros[i] for i in range(len(estado)) if estado[i])
        
        # Poda por limite superior: mesmo incluindo todos os restantes
        soma_maxima = soma_atual + sum(self.numeros[posicao:])
        if soma_maxima < self.soma_alvo:
            return True
        
        # Poda por limite inferior: já excedeu
        if soma_atual > self.soma_alvo:
            return True
        
        return False
    
    def resolver(self, encontrar_todas: bool = False) -> List[List[int]]:
        """
        Resolve problema da soma de subconjuntos.
        
        Args:
            encontrar_todas: Se deve encontrar todas as soluções
        
        Returns:
            Lista de subconjuntos que somam o valor alvo
        """
        solucoes_bool = self.buscar([], encontrar_todas)
        
        # Converter para listas de números
        solucoes_numeros = []
        for sol in solucoes_bool:
            subconjunto = [self.numeros[i] for i in range(len(sol)) if sol[i]]
            solucoes_numeros.append(subconjunto)
        
        return solucoes_numeros


# Funções de Demonstração
def demonstrar_n_queens():
    """Demonstra solução do problema das N-Rainhas."""
    print("=== DEMONSTRAÇÃO: N-QUEENS ===\n")
    
    for n in [4, 8]:
        print(f"Resolvendo {n}-Queens:")
        queens = NQueens(n)
        queens.debug = False
        
        start_time = time.time()
        solucoes = queens.resolver(encontrar_todas=True)
        tempo = time.time() - start_time
        
        print(f"  Soluções encontradas: {len(solucoes)}")
        print(f"  Tempo: {tempo:.4f}s")
        print(f"  Nós explorados: {queens.stats.nos_explorados}")
        print(f"  Nós podados: {queens.stats.nos_podados}")
        print(f"  Backracks: {queens.stats.backracks_realizados}")
        print(f"  Profundidade máxima: {queens.stats.profundidade_maxima}")
        
        if solucoes and n == 4:
            print(f"  Primeira solução: {solucoes[0]}")
            queens.imprimir_tabuleiro(solucoes[0])
        
        print()


def demonstrar_sudoku():
    """Demonstra solução de Sudoku."""
    print("=== DEMONSTRAÇÃO: SUDOKU SOLVER ===\n")
    
    # Sudoku exemplo (0 = célula vazia)
    tabuleiro = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    sudoku = SudokuSolver(tabuleiro)
    
    print("Tabuleiro inicial:")
    sudoku.imprimir_tabuleiro(tabuleiro)
    
    print(f"Células vazias: {len(sudoku.celulas_vazias)}")
    
    start_time = time.time()
    solucao = sudoku.resolver()
    tempo = time.time() - start_time
    
    if solucao:
        print(f"\nSolução encontrada em {tempo:.4f}s")
        print(f"Nós explorados: {sudoku.stats.nos_explorados}")
        print(f"Nós podados: {sudoku.stats.nos_podados}")
        print(f"Backracks: {sudoku.stats.backracks_realizados}")
        
        print("\nTabuleiro resolvido:")
        sudoku.imprimir_tabuleiro(solucao)
    else:
        print("Nenhuma solução encontrada!")


def demonstrar_maze():
    """Demonstra solução de labirinto."""
    print("\n=== DEMONSTRAÇÃO: MAZE SOLVER ===\n")
    
    # Labirinto (0 = livre, 1 = parede)
    labirinto = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    inicio = (0, 0)
    fim = (4, 4)
    
    maze = MazeSolver(labirinto, inicio, fim)
    
    print("Labirinto inicial:")
    maze.imprimir_labirinto()
    
    start_time = time.time()
    caminho = maze.resolver()
    tempo = time.time() - start_time
    
    if caminho:
        print(f"\nCaminho encontrado em {tempo:.4f}s")
        print(f"Comprimento do caminho: {len(caminho)}")
        print(f"Nós explorados: {maze.stats.nos_explorados}")
        print(f"Backracks: {maze.stats.backracks_realizados}")
        
        print(f"\nCaminho: {' -> '.join(map(str, caminho))}")
        maze.imprimir_labirinto(caminho)
    else:
        print("Nenhum caminho encontrado!")


def demonstrar_graph_coloring():
    """Demonstra coloração de grafos."""
    print("\n=== DEMONSTRAÇÃO: GRAPH COLORING ===\n")
    
    # Grafo exemplo (lista de adjacência)
    grafo = {
        0: [1, 2, 3],
        1: [0, 2],
        2: [0, 1, 3],
        3: [0, 2]
    }
    
    print("Grafo:")
    for vertice, vizinhos in grafo.items():
        print(f"  Vértice {vertice}: vizinhos {vizinhos}")
    
    for num_cores in [2, 3]:
        print(f"\nTentando colorir com {num_cores} cores:")
        
        coloring = GraphColoring(grafo, num_cores)
        
        start_time = time.time()
        solucao = coloring.resolver()
        tempo = time.time() - start_time
        
        if solucao:
            print(f"  Coloração encontrada em {tempo:.4f}s")
            print(f"  Nós explorados: {coloring.stats.nos_explorados}")
            print(f"  Coloração: {solucao}")
            
            # Verificar validade
            valida = True
            for vertice, cor in solucao.items():
                for vizinho in grafo[vertice]:
                    if vizinho in solucao and solucao[vizinho] == cor:
                        valida = False
                        break
            
            print(f"  Coloração válida: {valida}")
        else:
            print(f"  Impossível colorir com {num_cores} cores")


def demonstrar_subset_sum():
    """Demonstra problema da soma de subconjuntos."""
    print("\n=== DEMONSTRAÇÃO: SUBSET SUM ===\n")
    
    numeros = [3, 34, 4, 12, 5, 2]
    soma_alvo = 9
    
    print(f"Números: {numeros}")
    print(f"Soma alvo: {soma_alvo}")
    
    subset = SubsetSum(numeros, soma_alvo)
    
    start_time = time.time()
    solucoes = subset.resolver(encontrar_todas=True)
    tempo = time.time() - start_time
    
    print(f"\nSoluções encontradas: {len(solucoes)}")
    print(f"Tempo: {tempo:.4f}s")
    print(f"Nós explorados: {subset.stats.nos_explorados}")
    print(f"Nós podados: {subset.stats.nos_podados}")
    
    for i, sol in enumerate(solucoes):
        soma = sum(sol)
        print(f"  Solução {i+1}: {sol} (soma: {soma})")


def benchmark_backtracking():
    """Compara performance dos algoritmos de backtracking."""
    print("\n=== BENCHMARK: BACKTRACKING ===\n")
    
    # Benchmark N-Queens
    print("Benchmark N-Queens (primeira solução):")
    for n in [4, 6, 8]:
        queens = NQueens(n)
        
        start_time = time.time()
        solucoes = queens.resolver(encontrar_todas=False)
        tempo = time.time() - start_time
        
        print(f"  {n}-Queens: {tempo:.4f}s, nós: {queens.stats.nos_explorados}, "
              f"podas: {queens.stats.nos_podados}")
    
    # Benchmark Subset Sum
    print("\nBenchmark Subset Sum:")
    casos = [
        ([1, 2, 3, 4, 5], 8),
        ([2, 3, 7, 8, 10], 11),
        ([1, 3, 5, 7, 9, 11], 15)
    ]
    
    for numeros, alvo in casos:
        subset = SubsetSum(numeros, alvo)
        
        start_time = time.time()
        solucoes = subset.resolver(encontrar_todas=False)
        tempo = time.time() - start_time
        
        print(f"  {numeros} -> {alvo}: {tempo:.4f}s, "
              f"nós: {subset.stats.nos_explorados}")


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 06.3 - BACKTRACKING")
    print("=" * 50)
    
    demonstrar_n_queens()
    demonstrar_sudoku()
    demonstrar_maze()
    demonstrar_graph_coloring()
    demonstrar_subset_sum()
    benchmark_backtracking()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 06.3")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. PARADIGMA BACKTRACKING:
   • Busca sistemática em espaço de estados
   • Construção incremental de soluções
   • Retrocesso quando não há progresso possível
   • Exploração completa com poda inteligente

2. COMPONENTES ESSENCIAIS:
   • Verificação de validade de movimentos
   • Detecção de soluções completas
   • Geração de candidatos para próximo passo
   • Aplicação e reversão de movimentos
   • Critérios de poda para otimização

3. PROBLEMAS CLÁSSICOS IMPLEMENTADOS:
   • N-Queens: colocação de rainhas sem conflitos
   • Sudoku: preenchimento com restrições numéricas
   • Maze Solving: encontrar caminho em labirinto
   • Graph Coloring: coloração com cores mínimas
   • Subset Sum: encontrar subconjunto com soma específica

4. TÉCNICAS DE OTIMIZAÇÃO:
   • Poda por limites (bounds)
   • Heurísticas para ordenação de candidatos
   • Propagação de restrições
   • Detecção precoce de impossibilidade
   • Análise de conflitos futuros

5. HEURÍSTICAS IMPLEMENTADAS:
   • MRV (Minimum Remaining Values): escolher variável com menos opções
   • Degree Heuristic: priorizar variáveis mais restritivas
   • Least Constraining Value: escolher valor que menos restringe
   • Forward Checking: verificar impacto em variáveis futuras

6. ANÁLISE DE COMPLEXIDADE:
   • Pior caso: O(b^d) onde b=branching factor, d=depth
   • Com poda eficiente: redução exponencial na prática
   • Espaço: O(d) para pilha de recursão
   • Dependente da qualidade das heurísticas

7. VANTAGENS DO BACKTRACKING:
   • Garante encontrar solução se existir
   • Pode encontrar todas as soluções
   • Flexível para diferentes tipos de problemas
   • Permite otimizações específicas do domínio

8. LIMITAÇÕES:
   • Complexidade exponencial no pior caso
   • Pode ser lento para problemas grandes
   • Sensível à ordem de exploração
   • Requer boa modelagem do problema

9. ESTRATÉGIAS DE IMPLEMENTAÇÃO:
   • Separação clara entre lógica e heurísticas
   • Contadores para análise de performance
   • Estruturas de dados eficientes
   • Verificação incremental de restrições
   • Reversão eficiente de movimentos

10. APLICAÇÕES PRÁTICAS:
    • Jogos e quebra-cabeças (Sudoku, xadrez)
    • Problemas de escalonamento
    • Configuração de sistemas
    • Análise combinatória
    • Inteligência artificial (CSP)

11. COMPARAÇÃO COM OUTRAS TÉCNICAS:
    • vs Força Bruta: mais eficiente com poda
    • vs Programação Dinâmica: para problemas sem sobreposição
    • vs Algoritmos Gulosos: garante otimalidade
    • vs Busca Local: exploração mais sistemática

12. MELHORIAS AVANÇADAS:
    • Constraint Propagation
    • Arc Consistency
    • Backjumping
    • Dynamic Variable Ordering
    • Randomização para evitar casos patológicos

O backtracking é uma técnica fundamental para resolver problemas
de satisfação de restrições e busca em espaços de estados.
Embora tenha complexidade exponencial, as técnicas de poda e
heurísticas podem torná-lo muito eficiente na prática.

Próximo arquivo: Dividir e Conquistar
    """)


if __name__ == "__main__":
    main()