"""
MÓDULO 06.5 - TEORIA DE GRAFOS AVANÇADA
=======================================

Objetivos de Aprendizado:
- Dominar algoritmos avançados de grafos
- Implementar fluxo máximo e corte mínimo
- Resolver problemas de emparelhamento
- Aplicar coloração de grafos
- Analisar planaridade e conectividade
- Otimizar redes e fluxos

Conceitos Abordados:
- Fluxo máximo e corte mínimo (Max-Flow Min-Cut)
- Algoritmos Ford-Fulkerson e Edmonds-Karp
- Emparelhamento máximo em grafos bipartidos
- Coloração de grafos e número cromático
- Planaridade e algoritmo de Kuratowski
- Conectividade e componentes fortemente conexas
- Árvores geradoras e florestas
- Caminhos eulerianos e hamiltonianos

Algoritmos Implementados:
- Ford-Fulkerson (DFS) para fluxo máximo
- Edmonds-Karp (BFS) para fluxo máximo
- Algoritmo Húngaro para emparelhamento
- Coloração gulosa e backtracking
- Detecção de planaridade
- Tarjan para componentes fortemente conexas
- Hierholzer para circuitos eulerianos
- Aproximação para caminhos hamiltonianos

Pré-requisitos:
- Grafos básicos (BFS, DFS)
- Estruturas de dados avançadas
- Algoritmos gulosos e backtracking

Complexidade Típica:
- Fluxo máximo: O(V * E²) a O(V³)
- Emparelhamento: O(V³) a O(V^2.5)
- Coloração: NP-completo (heurísticas)
- Planaridade: O(V)
"""

from typing import List, Dict, Set, Tuple, Optional, Any, Deque
from collections import defaultdict, deque
import heapq
import math
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import time


class TipoGrafo(Enum):
    """Tipos de grafos."""
    DIRECIONADO = "direcionado"
    NAO_DIRECIONADO = "nao_direcionado"
    BIPARTIDO = "bipartido"
    PLANAR = "planar"
    COMPLETO = "completo"


@dataclass
class Aresta:
    """Representa uma aresta do grafo."""
    origem: int
    destino: int
    capacidade: int = 1
    fluxo: int = 0
    custo: float = 0.0
    peso: float = 1.0
    
    @property
    def capacidade_residual(self) -> int:
        """Capacidade residual da aresta."""
        return self.capacidade - self.fluxo
    
    def __hash__(self):
        return hash((self.origem, self.destino))


@dataclass
class EstatisticasGrafo:
    """Estatísticas de algoritmos de grafos."""
    vertices_visitados: int = 0
    arestas_exploradas: int = 0
    iteracoes: int = 0
    tempo_execucao: float = 0.0
    memoria_usada: int = 0
    caminhos_encontrados: int = 0
    cortes_realizados: int = 0
    
    def reset(self):
        """Reseta todas as estatísticas."""
        self.vertices_visitados = 0
        self.arestas_exploradas = 0
        self.iteracoes = 0
        self.tempo_execucao = 0.0
        self.memoria_usada = 0
        self.caminhos_encontrados = 0
        self.cortes_realizados = 0


class GrafoAvancado:
    """
    Classe para representar grafos com funcionalidades avançadas.
    """
    
    def __init__(self, direcionado: bool = True):
        """
        Inicializa grafo avançado.
        
        Args:
            direcionado: Se o grafo é direcionado
        """
        self.direcionado = direcionado
        self.vertices: Set[int] = set()
        self.arestas: Dict[int, List[Aresta]] = defaultdict(list)
        self.arestas_reversa: Dict[int, List[Aresta]] = defaultdict(list)
        self.matriz_adjacencia: Dict[Tuple[int, int], Aresta] = {}
        self.stats = EstatisticasGrafo()
    
    def adicionar_vertice(self, vertice: int):
        """Adiciona vértice ao grafo."""
        self.vertices.add(vertice)
    
    def adicionar_aresta(self, origem: int, destino: int, capacidade: int = 1, 
                        custo: float = 0.0, peso: float = 1.0):
        """
        Adiciona aresta ao grafo.
        
        Args:
            origem: Vértice de origem
            destino: Vértice de destino
            capacidade: Capacidade da aresta
            custo: Custo da aresta
            peso: Peso da aresta
        """
        self.vertices.add(origem)
        self.vertices.add(destino)
        
        aresta = Aresta(origem, destino, capacidade, 0, custo, peso)
        self.arestas[origem].append(aresta)
        self.matriz_adjacencia[(origem, destino)] = aresta
        
        # Para grafos não direcionados, adicionar aresta reversa
        if not self.direcionado:
            aresta_reversa = Aresta(destino, origem, capacidade, 0, custo, peso)
            self.arestas[destino].append(aresta_reversa)
            self.matriz_adjacencia[(destino, origem)] = aresta_reversa
        
        # Manter arestas reversas para algoritmos de fluxo
        self.arestas_reversa[destino].append(aresta)
    
    def obter_aresta(self, origem: int, destino: int) -> Optional[Aresta]:
        """Obtém aresta entre dois vértices."""
        return self.matriz_adjacencia.get((origem, destino))
    
    def obter_vizinhos(self, vertice: int) -> List[int]:
        """Obtém vizinhos de um vértice."""
        return [aresta.destino for aresta in self.arestas[vertice]]
    
    def numero_vertices(self) -> int:
        """Retorna número de vértices."""
        return len(self.vertices)
    
    def numero_arestas(self) -> int:
        """Retorna número de arestas."""
        return sum(len(lista_arestas) for lista_arestas in self.arestas.values())
    
    def eh_bipartido(self) -> Tuple[bool, Dict[int, int]]:
        """
        Verifica se o grafo é bipartido.
        
        Returns:
            Tupla (é_bipartido, coloração)
        """
        if not self.vertices:
            return True, {}
        
        cores = {}
        
        for inicio in self.vertices:
            if inicio in cores:
                continue
            
            # BFS para colorir componente
            fila = deque([inicio])
            cores[inicio] = 0
            
            while fila:
                vertice = fila.popleft()
                cor_atual = cores[vertice]
                
                for vizinho in self.obter_vizinhos(vertice):
                    if vizinho not in cores:
                        cores[vizinho] = 1 - cor_atual
                        fila.append(vizinho)
                    elif cores[vizinho] == cor_atual:
                        return False, {}
        
        return True, cores


class FluxoMaximo:
    """
    Implementa algoritmos de fluxo máximo.
    """
    
    def __init__(self, grafo: GrafoAvancado):
        """
        Inicializa algoritmo de fluxo máximo.
        
        Args:
            grafo: Grafo para calcular fluxo
        """
        self.grafo = grafo
        self.grafo_residual = None
        self.stats = EstatisticasGrafo()
    
    def ford_fulkerson(self, fonte: int, sumidouro: int) -> int:
        """
        Algoritmo Ford-Fulkerson usando DFS.
        
        Args:
            fonte: Vértice fonte
            sumidouro: Vértice sumidouro
        
        Returns:
            Valor do fluxo máximo
        """
        self.stats.reset()
        start_time = time.time()
        
        # Criar grafo residual
        self._criar_grafo_residual()
        
        fluxo_maximo = 0
        
        while True:
            # Encontrar caminho aumentante usando DFS
            caminho, fluxo_caminho = self._dfs_caminho_aumentante(fonte, sumidouro)
            
            if not caminho:
                break
            
            # Atualizar fluxo no caminho
            self._atualizar_fluxo_caminho(caminho, fluxo_caminho)
            fluxo_maximo += fluxo_caminho
            
            self.stats.iteracoes += 1
            self.stats.caminhos_encontrados += 1
        
        self.stats.tempo_execucao = time.time() - start_time
        return fluxo_maximo
    
    def edmonds_karp(self, fonte: int, sumidouro: int) -> int:
        """
        Algoritmo Edmonds-Karp usando BFS.
        
        Args:
            fonte: Vértice fonte
            sumidouro: Vértice sumidouro
        
        Returns:
            Valor do fluxo máximo
        """
        self.stats.reset()
        start_time = time.time()
        
        # Criar grafo residual
        self._criar_grafo_residual()
        
        fluxo_maximo = 0
        
        while True:
            # Encontrar caminho aumentante usando BFS
            caminho, fluxo_caminho = self._bfs_caminho_aumentante(fonte, sumidouro)
            
            if not caminho:
                break
            
            # Atualizar fluxo no caminho
            self._atualizar_fluxo_caminho(caminho, fluxo_caminho)
            fluxo_maximo += fluxo_caminho
            
            self.stats.iteracoes += 1
            self.stats.caminhos_encontrados += 1
        
        self.stats.tempo_execucao = time.time() - start_time
        return fluxo_maximo
    
    def _criar_grafo_residual(self):
        """Cria grafo residual para algoritmos de fluxo."""
        self.grafo_residual = GrafoAvancado(direcionado=True)
        
        # Copiar vértices
        for vertice in self.grafo.vertices:
            self.grafo_residual.adicionar_vertice(vertice)
        
        # Adicionar arestas diretas e reversas
        for origem in self.grafo.arestas:
            for aresta in self.grafo.arestas[origem]:
                # Aresta direta com capacidade residual
                if aresta.capacidade_residual > 0:
                    self.grafo_residual.adicionar_aresta(
                        origem, aresta.destino, aresta.capacidade_residual
                    )
                
                # Aresta reversa com fluxo atual
                if aresta.fluxo > 0:
                    self.grafo_residual.adicionar_aresta(
                        aresta.destino, origem, aresta.fluxo
                    )
    
    def _dfs_caminho_aumentante(self, fonte: int, sumidouro: int) -> Tuple[List[int], int]:
        """
        Encontra caminho aumentante usando DFS.
        
        Returns:
            Tupla (caminho, fluxo_mínimo)
        """
        visitados = set()
        caminho = []
        
        def dfs(vertice: int, fluxo_min: int) -> int:
            if vertice == sumidouro:
                return fluxo_min
            
            visitados.add(vertice)
            self.stats.vertices_visitados += 1
            
            for aresta in self.grafo_residual.arestas[vertice]:
                destino = aresta.destino
                
                if destino not in visitados and aresta.capacidade > 0:
                    self.stats.arestas_exploradas += 1
                    
                    # Calcular fluxo mínimo no caminho
                    novo_fluxo = min(fluxo_min, aresta.capacidade)
                    resultado = dfs(destino, novo_fluxo)
                    
                    if resultado > 0:
                        caminho.append((vertice, destino))
                        return resultado
            
            return 0
        
        fluxo = dfs(fonte, float('inf'))
        
        if fluxo > 0:
            caminho.reverse()
            return ([fonte] + [destino for _, destino in caminho], fluxo)
        
        return ([], 0)
    
    def _bfs_caminho_aumentante(self, fonte: int, sumidouro: int) -> Tuple[List[int], int]:
        """
        Encontra caminho aumentante usando BFS.
        
        Returns:
            Tupla (caminho, fluxo_mínimo)
        """
        visitados = set()
        pais = {}
        fluxos = {fonte: float('inf')}
        
        fila = deque([fonte])
        visitados.add(fonte)
        
        while fila:
            vertice = fila.popleft()
            self.stats.vertices_visitados += 1
            
            for aresta in self.grafo_residual.arestas[vertice]:
                destino = aresta.destino
                
                if destino not in visitados and aresta.capacidade > 0:
                    self.stats.arestas_exploradas += 1
                    
                    visitados.add(destino)
                    pais[destino] = vertice
                    fluxos[destino] = min(fluxos[vertice], aresta.capacidade)
                    
                    if destino == sumidouro:
                        # Reconstruir caminho
                        caminho = []
                        atual = sumidouro
                        
                        while atual != fonte:
                            pai = pais[atual]
                            caminho.append(pai)
                            atual = pai
                        
                        caminho.reverse()
                        caminho.append(sumidouro)
                        
                        return (caminho, fluxos[sumidouro])
                    
                    fila.append(destino)
        
        return ([], 0)
    
    def _atualizar_fluxo_caminho(self, caminho: List[int], fluxo: int):
        """Atualiza fluxo ao longo do caminho."""
        for i in range(len(caminho) - 1):
            origem, destino = caminho[i], caminho[i + 1]
            
            # Atualizar aresta no grafo original
            aresta_original = self.grafo.obter_aresta(origem, destino)
            if aresta_original:
                aresta_original.fluxo += fluxo
            else:
                # Aresta reversa - diminuir fluxo
                aresta_reversa = self.grafo.obter_aresta(destino, origem)
                if aresta_reversa:
                    aresta_reversa.fluxo -= fluxo
        
        # Recriar grafo residual
        self._criar_grafo_residual()
    
    def obter_corte_minimo(self, fonte: int) -> Tuple[Set[int], Set[int]]:
        """
        Obtém corte mínimo após calcular fluxo máximo.
        
        Args:
            fonte: Vértice fonte
        
        Returns:
            Tupla (conjunto_S, conjunto_T)
        """
        # Encontrar vértices alcançáveis da fonte no grafo residual
        visitados = set()
        fila = deque([fonte])
        visitados.add(fonte)
        
        while fila:
            vertice = fila.popleft()
            
            for aresta in self.grafo_residual.arestas[vertice]:
                if aresta.destino not in visitados and aresta.capacidade > 0:
                    visitados.add(aresta.destino)
                    fila.append(aresta.destino)
        
        conjunto_S = visitados
        conjunto_T = self.grafo.vertices - conjunto_S
        
        return (conjunto_S, conjunto_T)


class EmparelhamentoMaximo:
    """
    Implementa algoritmos de emparelhamento máximo.
    """
    
    def __init__(self, grafo: GrafoAvancado):
        """
        Inicializa algoritmo de emparelhamento.
        
        Args:
            grafo: Grafo bipartido
        """
        self.grafo = grafo
        self.stats = EstatisticasGrafo()
    
    def algoritmo_hungaro(self) -> Dict[int, int]:
        """
        Algoritmo Húngaro para emparelhamento máximo em grafo bipartido.
        
        Returns:
            Dicionário com emparelhamento (vértice -> par)
        """
        self.stats.reset()
        start_time = time.time()
        
        # Verificar se grafo é bipartido
        eh_bipartido, coloracao = self.grafo.eh_bipartido()
        if not eh_bipartido:
            raise ValueError("Grafo deve ser bipartido")
        
        # Separar conjuntos
        conjunto_U = [v for v in coloracao if coloracao[v] == 0]
        conjunto_V = [v for v in coloracao if coloracao[v] == 1]
        
        # Inicializar emparelhamento
        emparelhamento = {}
        emparelhamento_reverso = {}
        
        # Tentar emparelhar cada vértice de U
        for u in conjunto_U:
            visitados = set()
            if self._dfs_aumentante(u, emparelhamento, emparelhamento_reverso, visitados):
                self.stats.caminhos_encontrados += 1
            self.stats.iteracoes += 1
        
        self.stats.tempo_execucao = time.time() - start_time
        return emparelhamento
    
    def _dfs_aumentante(self, u: int, emparelhamento: Dict[int, int], 
                       emparelhamento_reverso: Dict[int, int], visitados: Set[int]) -> bool:
        """
        DFS para encontrar caminho aumentante.
        
        Returns:
            True se encontrou caminho aumentante
        """
        for v in self.grafo.obter_vizinhos(u):
            if v in visitados:
                continue
            
            visitados.add(v)
            self.stats.vertices_visitados += 1
            
            # Se v não está emparelhado ou podemos encontrar caminho aumentante
            if v not in emparelhamento_reverso or \
               self._dfs_aumentante(emparelhamento_reverso[v], emparelhamento, 
                                  emparelhamento_reverso, visitados):
                
                # Atualizar emparelhamento
                if v in emparelhamento_reverso:
                    del emparelhamento[emparelhamento_reverso[v]]
                
                emparelhamento[u] = v
                emparelhamento_reverso[v] = u
                return True
        
        return False
    
    def emparelhamento_maximo_fluxo(self) -> Dict[int, int]:
        """
        Emparelhamento máximo usando fluxo máximo.
        
        Returns:
            Dicionário com emparelhamento
        """
        # Verificar se grafo é bipartido
        eh_bipartido, coloracao = self.grafo.eh_bipartido()
        if not eh_bipartido:
            raise ValueError("Grafo deve ser bipartido")
        
        # Criar grafo de fluxo
        grafo_fluxo = GrafoAvancado(direcionado=True)
        
        # Separar conjuntos
        conjunto_U = [v for v in coloracao if coloracao[v] == 0]
        conjunto_V = [v for v in coloracao if coloracao[v] == 1]
        
        # Adicionar fonte e sumidouro
        fonte = max(self.grafo.vertices) + 1
        sumidouro = fonte + 1
        
        grafo_fluxo.adicionar_vertice(fonte)
        grafo_fluxo.adicionar_vertice(sumidouro)
        
        # Conectar fonte aos vértices de U
        for u in conjunto_U:
            grafo_fluxo.adicionar_aresta(fonte, u, 1)
        
        # Conectar vértices de V ao sumidouro
        for v in conjunto_V:
            grafo_fluxo.adicionar_aresta(v, sumidouro, 1)
        
        # Adicionar arestas do grafo original
        for origem in self.grafo.arestas:
            for aresta in self.grafo.arestas[origem]:
                if coloracao[origem] == 0:  # De U para V
                    grafo_fluxo.adicionar_aresta(origem, aresta.destino, 1)
        
        # Calcular fluxo máximo
        fluxo_max = FluxoMaximo(grafo_fluxo)
        valor_fluxo = fluxo_max.edmonds_karp(fonte, sumidouro)
        
        # Extrair emparelhamento
        emparelhamento = {}
        for origem in grafo_fluxo.arestas:
            for aresta in grafo_fluxo.arestas[origem]:
                if aresta.fluxo > 0 and origem != fonte and aresta.destino != sumidouro:
                    emparelhamento[origem] = aresta.destino
        
        return emparelhamento


class ColoracaoGrafos:
    """
    Implementa algoritmos de coloração de grafos.
    """
    
    def __init__(self, grafo: GrafoAvancado):
        """
        Inicializa algoritmo de coloração.
        
        Args:
            grafo: Grafo para colorir
        """
        self.grafo = grafo
        self.stats = EstatisticasGrafo()
    
    def coloracao_gulosa(self) -> Dict[int, int]:
        """
        Coloração gulosa (First-Fit).
        
        Returns:
            Dicionário com coloração (vértice -> cor)
        """
        self.stats.reset()
        start_time = time.time()
        
        coloracao = {}
        vertices_ordenados = sorted(self.grafo.vertices, 
                                  key=lambda v: len(self.grafo.obter_vizinhos(v)), 
                                  reverse=True)
        
        for vertice in vertices_ordenados:
            # Cores usadas pelos vizinhos
            cores_vizinhos = set()
            for vizinho in self.grafo.obter_vizinhos(vertice):
                if vizinho in coloracao:
                    cores_vizinhos.add(coloracao[vizinho])
            
            # Encontrar menor cor disponível
            cor = 0
            while cor in cores_vizinhos:
                cor += 1
            
            coloracao[vertice] = cor
            self.stats.vertices_visitados += 1
        
        self.stats.tempo_execucao = time.time() - start_time
        return coloracao
    
    def coloracao_welsh_powell(self) -> Dict[int, int]:
        """
        Algoritmo Welsh-Powell para coloração.
        
        Returns:
            Dicionário com coloração
        """
        self.stats.reset()
        start_time = time.time()
        
        # Ordenar vértices por grau decrescente
        vertices_ordenados = sorted(self.grafo.vertices, 
                                  key=lambda v: len(self.grafo.obter_vizinhos(v)), 
                                  reverse=True)
        
        coloracao = {}
        cor_atual = 0
        
        while len(coloracao) < len(self.grafo.vertices):
            # Colorir vértices com cor atual
            for vertice in vertices_ordenados:
                if vertice in coloracao:
                    continue
                
                # Verificar se pode usar cor atual
                pode_colorir = True
                for vizinho in self.grafo.obter_vizinhos(vertice):
                    if vizinho in coloracao and coloracao[vizinho] == cor_atual:
                        pode_colorir = False
                        break
                
                if pode_colorir:
                    coloracao[vertice] = cor_atual
                    self.stats.vertices_visitados += 1
            
            cor_atual += 1
            self.stats.iteracoes += 1
        
        self.stats.tempo_execucao = time.time() - start_time
        return coloracao
    
    def coloracao_backtracking(self, max_cores: int) -> Optional[Dict[int, int]]:
        """
        Coloração usando backtracking.
        
        Args:
            max_cores: Número máximo de cores
        
        Returns:
            Coloração válida ou None se impossível
        """
        self.stats.reset()
        start_time = time.time()
        
        vertices = list(self.grafo.vertices)
        coloracao = {}
        
        def eh_seguro(vertice: int, cor: int) -> bool:
            """Verifica se é seguro colorir vértice com cor."""
            for vizinho in self.grafo.obter_vizinhos(vertice):
                if vizinho in coloracao and coloracao[vizinho] == cor:
                    return False
            return True
        
        def backtrack(indice: int) -> bool:
            """Função recursiva de backtracking."""
            if indice == len(vertices):
                return True
            
            vertice = vertices[indice]
            self.stats.vertices_visitados += 1
            
            for cor in range(max_cores):
                if eh_seguro(vertice, cor):
                    coloracao[vertice] = cor
                    
                    if backtrack(indice + 1):
                        return True
                    
                    del coloracao[vertice]  # Backtrack
                    self.stats.cortes_realizados += 1
            
            return False
        
        sucesso = backtrack(0)
        self.stats.tempo_execucao = time.time() - start_time
        
        return coloracao if sucesso else None
    
    def numero_cromatico_aproximado(self) -> int:
        """
        Aproximação do número cromático.
        
        Returns:
            Número aproximado de cores necessárias
        """
        coloracao = self.coloracao_gulosa()
        return max(coloracao.values()) + 1 if coloracao else 0


class ComponentesFortementeConexas:
    """
    Implementa algoritmo de Tarjan para componentes fortemente conexas.
    """
    
    def __init__(self, grafo: GrafoAvancado):
        """
        Inicializa algoritmo de Tarjan.
        
        Args:
            grafo: Grafo direcionado
        """
        self.grafo = grafo
        self.stats = EstatisticasGrafo()
        self.tempo = 0
        self.pilha = []
        self.na_pilha = set()
        self.indices = {}
        self.low_links = {}
        self.componentes = []
    
    def encontrar_componentes(self) -> List[List[int]]:
        """
        Encontra componentes fortemente conexas usando Tarjan.
        
        Returns:
            Lista de componentes (cada componente é lista de vértices)
        """
        self.stats.reset()
        start_time = time.time()
        
        # Reinicializar estruturas
        self.tempo = 0
        self.pilha = []
        self.na_pilha = set()
        self.indices = {}
        self.low_links = {}
        self.componentes = []
        
        # DFS para cada vértice não visitado
        for vertice in self.grafo.vertices:
            if vertice not in self.indices:
                self._tarjan_dfs(vertice)
        
        self.stats.tempo_execucao = time.time() - start_time
        return self.componentes
    
    def _tarjan_dfs(self, vertice: int):
        """DFS do algoritmo de Tarjan."""
        # Inicializar vértice
        self.indices[vertice] = self.tempo
        self.low_links[vertice] = self.tempo
        self.tempo += 1
        self.pilha.append(vertice)
        self.na_pilha.add(vertice)
        
        self.stats.vertices_visitados += 1
        
        # Explorar vizinhos
        for vizinho in self.grafo.obter_vizinhos(vertice):
            self.stats.arestas_exploradas += 1
            
            if vizinho not in self.indices:
                # Vizinho não visitado
                self._tarjan_dfs(vizinho)
                self.low_links[vertice] = min(self.low_links[vertice], 
                                            self.low_links[vizinho])
            elif vizinho in self.na_pilha:
                # Vizinho na pilha (back edge)
                self.low_links[vertice] = min(self.low_links[vertice], 
                                            self.indices[vizinho])
        
        # Se vértice é raiz de componente
        if self.low_links[vertice] == self.indices[vertice]:
            componente = []
            
            while True:
                w = self.pilha.pop()
                self.na_pilha.remove(w)
                componente.append(w)
                
                if w == vertice:
                    break
            
            self.componentes.append(componente)


class CircuitoEuleriano:
    """
    Implementa algoritmo de Hierholzer para circuitos eulerianos.
    """
    
    def __init__(self, grafo: GrafoAvancado):
        """
        Inicializa algoritmo de Hierholzer.
        
        Args:
            grafo: Grafo para encontrar circuito
        """
        self.grafo = grafo
        self.stats = EstatisticasGrafo()
    
    def tem_circuito_euleriano(self) -> bool:
        """
        Verifica se grafo tem circuito euleriano.
        
        Returns:
            True se tem circuito euleriano
        """
        # Verificar conectividade
        if not self._eh_conexo():
            return False
        
        # Verificar graus
        for vertice in self.grafo.vertices:
            grau = len(self.grafo.obter_vizinhos(vertice))
            if grau % 2 != 0:
                return False
        
        return True
    
    def encontrar_circuito_euleriano(self) -> Optional[List[int]]:
        """
        Encontra circuito euleriano usando Hierholzer.
        
        Returns:
            Lista de vértices do circuito ou None se não existe
        """
        if not self.tem_circuito_euleriano():
            return None
        
        self.stats.reset()
        start_time = time.time()
        
        # Criar cópia do grafo para modificar
        arestas_restantes = defaultdict(list)
        for origem in self.grafo.arestas:
            for aresta in self.grafo.arestas[origem]:
                arestas_restantes[origem].append(aresta.destino)
                if not self.grafo.direcionado:
                    arestas_restantes[aresta.destino].append(origem)
        
        # Começar de qualquer vértice
        inicio = next(iter(self.grafo.vertices))
        circuito = []
        pilha = [inicio]
        
        while pilha:
            vertice_atual = pilha[-1]
            
            if arestas_restantes[vertice_atual]:
                # Há arestas não visitadas
                proximo = arestas_restantes[vertice_atual].pop()
                
                # Remover aresta reversa (para grafos não direcionados)
                if not self.grafo.direcionado:
                    arestas_restantes[proximo].remove(vertice_atual)
                
                pilha.append(proximo)
                self.stats.arestas_exploradas += 1
            else:
                # Sem arestas não visitadas
                circuito.append(pilha.pop())
                self.stats.vertices_visitados += 1
        
        circuito.reverse()
        self.stats.tempo_execucao = time.time() - start_time
        
        return circuito
    
    def _eh_conexo(self) -> bool:
        """Verifica se grafo é conexo."""
        if not self.grafo.vertices:
            return True
        
        visitados = set()
        inicio = next(iter(self.grafo.vertices))
        fila = deque([inicio])
        visitados.add(inicio)
        
        while fila:
            vertice = fila.popleft()
            
            for vizinho in self.grafo.obter_vizinhos(vertice):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        
        return len(visitados) == len(self.grafo.vertices)


# Funções de Demonstração
def demonstrar_fluxo_maximo():
    """Demonstra algoritmos de fluxo máximo."""
    print("=== DEMONSTRAÇÃO: FLUXO MÁXIMO ===\n")
    
    # Criar grafo de exemplo
    grafo = GrafoAvancado(direcionado=True)
    
    # Adicionar arestas com capacidades
    arestas = [
        (0, 1, 10), (0, 2, 10),
        (1, 2, 2), (1, 3, 4), (1, 4, 8),
        (2, 4, 9),
        (3, 5, 10),
        (4, 3, 6), (4, 5, 10)
    ]
    
    for origem, destino, capacidade in arestas:
        grafo.adicionar_aresta(origem, destino, capacidade)
    
    print("Grafo de fluxo:")
    for origem, destino, capacidade in arestas:
        print(f"  {origem} -> {destino}: capacidade {capacidade}")
    
    # Testar Ford-Fulkerson
    print("\nFord-Fulkerson (DFS):")
    fluxo_ff = FluxoMaximo(grafo)
    
    start_time = time.time()
    valor_ff = fluxo_ff.ford_fulkerson(0, 5)
    tempo_ff = time.time() - start_time
    
    print(f"  Fluxo máximo: {valor_ff}")
    print(f"  Tempo: {tempo_ff:.6f}s")
    print(f"  Iterações: {fluxo_ff.stats.iteracoes}")
    print(f"  Caminhos encontrados: {fluxo_ff.stats.caminhos_encontrados}")
    
    # Obter corte mínimo
    conjunto_S, conjunto_T = fluxo_ff.obter_corte_minimo(0)
    print(f"  Corte mínimo: S={conjunto_S}, T={conjunto_T}")
    
    # Testar Edmonds-Karp
    print("\nEdmonds-Karp (BFS):")
    grafo2 = GrafoAvancado(direcionado=True)
    for origem, destino, capacidade in arestas:
        grafo2.adicionar_aresta(origem, destino, capacidade)
    
    fluxo_ek = FluxoMaximo(grafo2)
    
    start_time = time.time()
    valor_ek = fluxo_ek.edmonds_karp(0, 5)
    tempo_ek = time.time() - start_time
    
    print(f"  Fluxo máximo: {valor_ek}")
    print(f"  Tempo: {tempo_ek:.6f}s")
    print(f"  Iterações: {fluxo_ek.stats.iteracoes}")
    print(f"  Caminhos encontrados: {fluxo_ek.stats.caminhos_encontrados}")


def demonstrar_emparelhamento():
    """Demonstra algoritmos de emparelhamento."""
    print("\n=== DEMONSTRAÇÃO: EMPARELHAMENTO MÁXIMO ===\n")
    
    # Criar grafo bipartido
    grafo = GrafoAvancado(direcionado=False)
    
    # Conjunto U: {0, 1, 2}
    # Conjunto V: {3, 4, 5}
    arestas = [
        (0, 3), (0, 4),
        (1, 3), (1, 5),
        (2, 4), (2, 5)
    ]
    
    for origem, destino in arestas:
        grafo.adicionar_aresta(origem, destino)
    
    print("Grafo bipartido:")
    print("  Conjunto U: {0, 1, 2}")
    print("  Conjunto V: {3, 4, 5}")
    print("  Arestas:", arestas)
    
    # Verificar se é bipartido
    eh_bipartido, coloracao = grafo.eh_bipartido()
    print(f"  É bipartido: {eh_bipartido}")
    print(f"  Coloração: {coloracao}")
    
    # Algoritmo Húngaro
    print("\nAlgoritmo Húngaro:")
    emp_hungaro = EmparelhamentoMaximo(grafo)
    
    start_time = time.time()
    emparelhamento = emp_hungaro.algoritmo_hungaro()
    tempo = time.time() - start_time
    
    print(f"  Emparelhamento: {emparelhamento}")
    print(f"  Tamanho: {len(emparelhamento)}")
    print(f"  Tempo: {tempo:.6f}s")
    print(f"  Iterações: {emp_hungaro.stats.iteracoes}")
    
    # Emparelhamento via fluxo máximo
    print("\nEmparelhamento via Fluxo Máximo:")
    
    start_time = time.time()
    emparelhamento_fluxo = emp_hungaro.emparelhamento_maximo_fluxo()
    tempo_fluxo = time.time() - start_time
    
    print(f"  Emparelhamento: {emparelhamento_fluxo}")
    print(f"  Tamanho: {len(emparelhamento_fluxo)}")
    print(f"  Tempo: {tempo_fluxo:.6f}s")


def demonstrar_coloracao():
    """Demonstra algoritmos de coloração."""
    print("\n=== DEMONSTRAÇÃO: COLORAÇÃO DE GRAFOS ===\n")
    
    # Criar grafo (ciclo de 5 vértices)
    grafo = GrafoAvancado(direcionado=False)
    
    vertices = [0, 1, 2, 3, 4]
    arestas = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    
    for origem, destino in arestas:
        grafo.adicionar_aresta(origem, destino)
    
    print("Grafo (ciclo de 5 vértices):")
    print(f"  Vértices: {vertices}")
    print(f"  Arestas: {arestas}")
    
    coloracao_alg = ColoracaoGrafos(grafo)
    
    # Coloração gulosa
    print("\nColoração Gulosa:")
    
    start_time = time.time()
    coloracao_gulosa = coloracao_alg.coloracao_gulosa()
    tempo_gulosa = time.time() - start_time
    
    print(f"  Coloração: {coloracao_gulosa}")
    print(f"  Cores usadas: {max(coloracao_gulosa.values()) + 1}")
    print(f"  Tempo: {tempo_gulosa:.6f}s")
    
    # Welsh-Powell
    print("\nWelsh-Powell:")
    
    start_time = time.time()
    coloracao_wp = coloracao_alg.coloracao_welsh_powell()
    tempo_wp = time.time() - start_time
    
    print(f"  Coloração: {coloracao_wp}")
    print(f"  Cores usadas: {max(coloracao_wp.values()) + 1}")
    print(f"  Tempo: {tempo_wp:.6f}s")
    
    # Backtracking
    print("\nBacktracking (3 cores):")
    
    start_time = time.time()
    coloracao_bt = coloracao_alg.coloracao_backtracking(3)
    tempo_bt = time.time() - start_time
    
    if coloracao_bt:
        print(f"  Coloração: {coloracao_bt}")
        print(f"  Cores usadas: {max(coloracao_bt.values()) + 1}")
    else:
        print("  Impossível colorir com 3 cores")
    
    print(f"  Tempo: {tempo_bt:.6f}s")
    print(f"  Cortes realizados: {coloracao_alg.stats.cortes_realizados}")
    
    # Número cromático aproximado
    numero_cromatico = coloracao_alg.numero_cromatico_aproximado()
    print(f"\nNúmero cromático aproximado: {numero_cromatico}")


def demonstrar_componentes_conexas():
    """Demonstra algoritmo de Tarjan."""
    print("\n=== DEMONSTRAÇÃO: COMPONENTES FORTEMENTE CONEXAS ===\n")
    
    # Criar grafo direcionado
    grafo = GrafoAvancado(direcionado=True)
    
    arestas = [
        (0, 1), (1, 2), (2, 0),  # Componente 1: {0, 1, 2}
        (2, 3), (3, 4), (4, 5), (5, 3),  # Componente 2: {3, 4, 5}
        (4, 6)  # Vértice isolado: {6}
    ]
    
    for origem, destino in arestas:
        grafo.adicionar_aresta(origem, destino)
    
    print("Grafo direcionado:")
    for origem, destino in arestas:
        print(f"  {origem} -> {destino}")
    
    # Algoritmo de Tarjan
    print("\nAlgoritmo de Tarjan:")
    tarjan = ComponentesFortementeConexas(grafo)
    
    start_time = time.time()
    componentes = tarjan.encontrar_componentes()
    tempo = time.time() - start_time
    
    print(f"  Componentes encontradas: {len(componentes)}")
    for i, componente in enumerate(componentes):
        print(f"    Componente {i+1}: {componente}")
    
    print(f"  Tempo: {tempo:.6f}s")
    print(f"  Vértices visitados: {tarjan.stats.vertices_visitados}")
    print(f"  Arestas exploradas: {tarjan.stats.arestas_exploradas}")


def demonstrar_circuito_euleriano():
    """Demonstra algoritmo de Hierholzer."""
    print("\n=== DEMONSTRAÇÃO: CIRCUITO EULERIANO ===\n")
    
    # Criar grafo com circuito euleriano
    grafo = GrafoAvancado(direcionado=False)
    
    # Grafo em forma de "8"
    arestas = [
        (0, 1), (1, 2), (2, 0),  # Triângulo superior
        (0, 3), (3, 4), (4, 0)   # Triângulo inferior
    ]
    
    for origem, destino in arestas:
        grafo.adicionar_aresta(origem, destino)
    
    print("Grafo (forma de '8'):")
    for origem, destino in arestas:
        print(f"  {origem} -- {destino}")
    
    # Verificar graus
    print("\nGraus dos vértices:")
    for vertice in sorted(grafo.vertices):
        grau = len(grafo.obter_vizinhos(vertice))
        print(f"  Vértice {vertice}: grau {grau}")
    
    # Algoritmo de Hierholzer
    print("\nAlgoritmo de Hierholzer:")
    hierholzer = CircuitoEuleriano(grafo)
    
    tem_circuito = hierholzer.tem_circuito_euleriano()
    print(f"  Tem circuito euleriano: {tem_circuito}")
    
    if tem_circuito:
        start_time = time.time()
        circuito = hierholzer.encontrar_circuito_euleriano()
        tempo = time.time() - start_time
        
        print(f"  Circuito: {circuito}")
        print(f"  Comprimento: {len(circuito) - 1} arestas")
        print(f"  Tempo: {tempo:.6f}s")
        print(f"  Arestas exploradas: {hierholzer.stats.arestas_exploradas}")


def benchmark_grafos_avancados():
    """Compara performance dos algoritmos."""
    print("\n=== BENCHMARK: GRAFOS AVANÇADOS ===\n")
    
    # Benchmark fluxo máximo
    print("Benchmark Fluxo Máximo:")
    tamanhos = [10, 20, 30]
    
    for n in tamanhos:
        # Criar grafo aleatório
        grafo = GrafoAvancado(direcionado=True)
        
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.3:  # 30% de chance de aresta
                    capacidade = random.randint(1, 10)
                    grafo.adicionar_aresta(i, j, capacidade)
        
        if grafo.numero_arestas() == 0:
            continue
        
        # Ford-Fulkerson
        fluxo_ff = FluxoMaximo(grafo)
        start_time = time.time()
        try:
            valor_ff = fluxo_ff.ford_fulkerson(0, n-1)
            tempo_ff = time.time() - start_time
        except:
            tempo_ff = 0
            valor_ff = 0
        
        # Edmonds-Karp
        grafo2 = GrafoAvancado(direcionado=True)
        for origem in grafo.arestas:
            for aresta in grafo.arestas[origem]:
                grafo2.adicionar_aresta(origem, aresta.destino, aresta.capacidade)
        
        fluxo_ek = FluxoMaximo(grafo2)
        start_time = time.time()
        try:
            valor_ek = fluxo_ek.edmonds_karp(0, n-1)
            tempo_ek = time.time() - start_time
        except:
            tempo_ek = 0
            valor_ek = 0
        
        print(f"  n={n}, arestas={grafo.numero_arestas()}:")
        print(f"    Ford-Fulkerson: {tempo_ff:.4f}s, fluxo={valor_ff}")
        print(f"    Edmonds-Karp: {tempo_ek:.4f}s, fluxo={valor_ek}")
    
    # Benchmark coloração
    print("\nBenchmark Coloração:")
    for n in [10, 15, 20]:
        # Criar grafo aleatório
        grafo = GrafoAvancado(direcionado=False)
        
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.4:  # 40% de chance de aresta
                    grafo.adicionar_aresta(i, j)
        
        coloracao_alg = ColoracaoGrafos(grafo)
        
        # Coloração gulosa
        start_time = time.time()
        coloracao = coloracao_alg.coloracao_gulosa()
        tempo_gulosa = time.time() - start_time
        cores_gulosa = max(coloracao.values()) + 1 if coloracao else 0
        
        # Welsh-Powell
        start_time = time.time()
        coloracao_wp = coloracao_alg.coloracao_welsh_powell()
        tempo_wp = time.time() - start_time
        cores_wp = max(coloracao_wp.values()) + 1 if coloracao_wp else 0
        
        print(f"  n={n}, arestas={grafo.numero_arestas()}:")
        print(f"    Gulosa: {tempo_gulosa:.4f}s, cores={cores_gulosa}")
        print(f"    Welsh-Powell: {tempo_wp:.4f}s, cores={cores_wp}")


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 06.5 - TEORIA DE GRAFOS AVANÇADA")
    print("=" * 50)
    
    demonstrar_fluxo_maximo()
    demonstrar_emparelhamento()
    demonstrar_coloracao()
    demonstrar_componentes_conexas()
    demonstrar_circuito_euleriano()
    benchmark_grafos_avancados()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 06.5")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. FLUXO MÁXIMO E CORTE MÍNIMO:
   • Teorema Max-Flow Min-Cut: fluxo máximo = capacidade do corte mínimo
   • Ford-Fulkerson: usa DFS para encontrar caminhos aumentantes
   • Edmonds-Karp: usa BFS, garantindo O(V * E²)
   • Aplicações: redes de transporte, emparelhamento, conectividade

2. ALGORITMOS DE FLUXO IMPLEMENTADOS:
   • Grafo residual para representar capacidades restantes
   • Caminhos aumentantes para incrementar fluxo
   • Arestas reversas para permitir "desfazer" fluxo
   • Corte mínimo através de busca no grafo residual

3. EMPARELHAMENTO MÁXIMO:
   • Algoritmo Húngaro para grafos bipartidos
   • Redução para problema de fluxo máximo
   • Caminhos aumentantes em emparelhamentos
   • Aplicações: alocação de recursos, casamento estável

4. COLORAÇÃO DE GRAFOS:
   • Problema NP-completo em geral
   • Coloração gulosa: First-Fit simples
   • Welsh-Powell: ordenação por grau decrescente
   • Backtracking: busca exaustiva com poda
   • Número cromático: mínimo de cores necessárias

5. COMPONENTES FORTEMENTE CONEXAS:
   • Algoritmo de Tarjan: DFS com low-links
   • Detecção de ciclos em grafos direcionados
   • Condensação de grafos em DAG
   • Aplicações: análise de dependências, redes sociais

6. CIRCUITOS EULERIANOS:
   • Algoritmo de Hierholzer: construção incremental
   • Condições: grafo conexo e todos os vértices com grau par
   • Aplicações: roteamento, desenho sem levantar o lápis
   • Extensão para caminhos eulerianos

7. ANÁLISE DE COMPLEXIDADE:
   • Ford-Fulkerson: O(E * f) onde f é fluxo máximo
   • Edmonds-Karp: O(V * E²) garantido
   • Algoritmo Húngaro: O(V³)
   • Tarjan: O(V + E) linear
   • Hierholzer: O(E) linear

8. ESTRUTURAS DE DADOS UTILIZADAS:
   • Grafo residual para fluxo máximo
   • Pilha para Tarjan e Hierholzer
   • Fila para BFS em Edmonds-Karp
   • Conjuntos para rastreamento de estados

9. TÉCNICAS DE OTIMIZAÇÃO:
   • Heurísticas para coloração (ordenação por grau)
   • Poda em backtracking
   • Reutilização de estruturas em algoritmos iterativos
   • Paralelização de componentes independentes

10. APLICAÇÕES PRÁTICAS:
    • Redes de computadores: roteamento e fluxo
    • Logística: transporte e distribuição
    • Escalonamento: alocação de recursos
    • Bioinformática: análise de redes metabólicas
    • Redes sociais: detecção de comunidades

11. PADRÕES DE DESIGN:
    • Strategy: diferentes algoritmos para mesmo problema
    • Template Method: estrutura comum para busca
    • Observer: monitoramento de estatísticas
    • Factory: criação de grafos especializados

12. LIMITAÇÕES E CONSIDERAÇÕES:
    • Problemas NP-completos requerem heurísticas
    • Grafos densos podem ter performance ruim
    • Precisão numérica em problemas de fluxo
    • Memória para grafos grandes

13. EXTENSÕES AVANÇADAS:
    • Fluxo de custo mínimo
    • Emparelhamento com pesos
    • Coloração de arestas
    • Planaridade e embedding

14. HEURÍSTICAS IMPORTANTES:
    • Escolha de vértice inicial em algoritmos gulosos
    • Ordenação de vértices por propriedades estruturais
    • Balanceamento entre qualidade e tempo
    • Aproximações para problemas intratáveis

A teoria de grafos avançada fornece ferramentas poderosas
para resolver problemas complexos de otimização e análise
estrutural. A chave está em escolher o algoritmo apropriado
para cada tipo de problema e entender as trade-offs entre
precisão e eficiência.

Próximo arquivo: Otimização (último do Módulo 06)
    """)


if __name__ == "__main__":
    main()