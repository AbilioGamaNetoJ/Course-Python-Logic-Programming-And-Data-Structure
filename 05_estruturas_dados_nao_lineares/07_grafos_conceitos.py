"""
MÓDULO 05.7 - GRAFOS: CONCEITOS FUNDAMENTAIS
==========================================

Objetivos de Aprendizado:
- Compreender a estrutura e terminologia de grafos
- Implementar diferentes representações de grafos
- Dominar algoritmos de travessia (DFS e BFS)
- Analisar conectividade e componentes
- Aplicar conceitos em problemas práticos

Conceitos Abordados:
- Grafos direcionados e não-direcionados
- Representação por matriz de adjacência
- Representação por lista de adjacência
- Busca em Profundidade (DFS)
- Busca em Largura (BFS)
- Componentes conectados
- Detecção de ciclos
- Ordenação topológica
- Caminhos e distâncias

Pré-requisitos:
- Estruturas de dados básicas (listas, pilhas, filas)
- Conceitos de recursão
- Algoritmos de busca

Complexidade das Operações:
- Adição de vértice: O(1) - lista adj, O(V) - matriz adj
- Adição de aresta: O(1) - ambas representações
- Busca de aresta: O(1) - matriz adj, O(grau) - lista adj
- DFS/BFS: O(V + E) onde V = vértices, E = arestas
"""

from collections import defaultdict, deque
from typing import List, Dict, Set, Tuple, Optional, Any
import time
import random


class GrafoMatrizAdjacencia:
    """
    Implementação de grafo usando matriz de adjacência.
    
    Vantagens:
    - Verificação rápida de existência de aresta: O(1)
    - Simples de implementar
    - Bom para grafos densos
    
    Desvantagens:
    - Uso de memória: O(V²)
    - Adição de vértice: O(V)
    - Ineficiente para grafos esparsos
    """
    
    def __init__(self, num_vertices: int, direcionado: bool = False):
        """
        Inicializa grafo com matriz de adjacência.
        
        Args:
            num_vertices: Número inicial de vértices
            direcionado: Se o grafo é direcionado
        """
        self.num_vertices = num_vertices
        self.direcionado = direcionado
        self.matriz = [[0] * num_vertices for _ in range(num_vertices)]
        self.vertices = list(range(num_vertices))
        self.num_arestas = 0
        
        # Estatísticas
        self.operacoes_busca = 0
        self.operacoes_insercao = 0
    
    def adicionar_vertice(self) -> int:
        """Adiciona novo vértice ao grafo."""
        novo_id = self.num_vertices
        self.num_vertices += 1
        self.vertices.append(novo_id)
        
        # Expandir matriz
        for linha in self.matriz:
            linha.append(0)
        self.matriz.append([0] * self.num_vertices)
        
        self.operacoes_insercao += self.num_vertices  # O(V) para expansão
        return novo_id
    
    def adicionar_aresta(self, origem: int, destino: int, peso: int = 1):
        """
        Adiciona aresta entre dois vértices.
        
        Args:
            origem: Vértice de origem
            destino: Vértice de destino
            peso: Peso da aresta (padrão 1)
        """
        if not (0 <= origem < self.num_vertices and 0 <= destino < self.num_vertices):
            raise ValueError("Vértices inválidos")
        
        if self.matriz[origem][destino] == 0:
            self.num_arestas += 1
        
        self.matriz[origem][destino] = peso
        if not self.direcionado:
            self.matriz[destino][origem] = peso
        
        self.operacoes_insercao += 1
    
    def remover_aresta(self, origem: int, destino: int):
        """Remove aresta entre dois vértices."""
        if not (0 <= origem < self.num_vertices and 0 <= destino < self.num_vertices):
            raise ValueError("Vértices inválidos")
        
        if self.matriz[origem][destino] != 0:
            self.num_arestas -= 1
            self.matriz[origem][destino] = 0
            if not self.direcionado:
                self.matriz[destino][origem] = 0
    
    def existe_aresta(self, origem: int, destino: int) -> bool:
        """Verifica se existe aresta entre dois vértices."""
        if not (0 <= origem < self.num_vertices and 0 <= destino < self.num_vertices):
            return False
        
        self.operacoes_busca += 1
        return self.matriz[origem][destino] != 0
    
    def obter_vizinhos(self, vertice: int) -> List[int]:
        """Retorna lista de vizinhos de um vértice."""
        if not (0 <= vertice < self.num_vertices):
            return []
        
        vizinhos = []
        for i in range(self.num_vertices):
            if self.matriz[vertice][i] != 0:
                vizinhos.append(i)
                self.operacoes_busca += 1
        
        return vizinhos
    
    def grau_vertice(self, vertice: int) -> int:
        """Retorna o grau de um vértice."""
        return len(self.obter_vizinhos(vertice))
    
    def densidade(self) -> float:
        """Calcula a densidade do grafo."""
        max_arestas = self.num_vertices * (self.num_vertices - 1)
        if not self.direcionado:
            max_arestas //= 2
        
        return self.num_arestas / max_arestas if max_arestas > 0 else 0
    
    def __str__(self) -> str:
        """Representação em string da matriz."""
        resultado = f"Grafo ({'direcionado' if self.direcionado else 'não-direcionado'}):\n"
        resultado += f"Vértices: {self.num_vertices}, Arestas: {self.num_arestas}\n"
        resultado += "Matriz de Adjacência:\n"
        
        for linha in self.matriz:
            resultado += " ".join(f"{val:2}" for val in linha) + "\n"
        
        return resultado


class GrafoListaAdjacencia:
    """
    Implementação de grafo usando lista de adjacência.
    
    Vantagens:
    - Uso eficiente de memória: O(V + E)
    - Rápida iteração sobre vizinhos
    - Bom para grafos esparsos
    
    Desvantagens:
    - Verificação de aresta: O(grau do vértice)
    - Mais complexo para alguns algoritmos
    """
    
    def __init__(self, direcionado: bool = False):
        """
        Inicializa grafo com lista de adjacência.
        
        Args:
            direcionado: Se o grafo é direcionado
        """
        self.direcionado = direcionado
        self.lista_adj = defaultdict(list)
        self.vertices = set()
        self.num_arestas = 0
        
        # Para arestas com peso
        self.pesos = {}
        
        # Estatísticas
        self.operacoes_busca = 0
        self.operacoes_insercao = 0
    
    def adicionar_vertice(self, vertice: Any):
        """Adiciona vértice ao grafo."""
        if vertice not in self.vertices:
            self.vertices.add(vertice)
            self.lista_adj[vertice] = []
            self.operacoes_insercao += 1
    
    def adicionar_aresta(self, origem: Any, destino: Any, peso: int = 1):
        """
        Adiciona aresta entre dois vértices.
        
        Args:
            origem: Vértice de origem
            destino: Vértice de destino
            peso: Peso da aresta
        """
        # Adicionar vértices se não existirem
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        
        # Verificar se aresta já existe
        if destino not in self.lista_adj[origem]:
            self.lista_adj[origem].append(destino)
            self.pesos[(origem, destino)] = peso
            self.num_arestas += 1
            
            if not self.direcionado and origem != destino:
                self.lista_adj[destino].append(origem)
                self.pesos[(destino, origem)] = peso
        
        self.operacoes_insercao += 1
    
    def remover_aresta(self, origem: Any, destino: Any):
        """Remove aresta entre dois vértices."""
        if origem in self.lista_adj and destino in self.lista_adj[origem]:
            self.lista_adj[origem].remove(destino)
            del self.pesos[(origem, destino)]
            self.num_arestas -= 1
            
            if not self.direcionado:
                self.lista_adj[destino].remove(origem)
                del self.pesos[(destino, origem)]
    
    def existe_aresta(self, origem: Any, destino: Any) -> bool:
        """Verifica se existe aresta entre dois vértices."""
        self.operacoes_busca += len(self.lista_adj[origem])
        return destino in self.lista_adj[origem]
    
    def obter_vizinhos(self, vertice: Any) -> List[Any]:
        """Retorna lista de vizinhos de um vértice."""
        return list(self.lista_adj[vertice])
    
    def obter_peso(self, origem: Any, destino: Any) -> Optional[int]:
        """Retorna o peso da aresta entre dois vértices."""
        return self.pesos.get((origem, destino))
    
    def grau_vertice(self, vertice: Any) -> int:
        """Retorna o grau de um vértice."""
        return len(self.lista_adj[vertice])
    
    def densidade(self) -> float:
        """Calcula a densidade do grafo."""
        num_vertices = len(self.vertices)
        if num_vertices <= 1:
            return 0
        
        max_arestas = num_vertices * (num_vertices - 1)
        if not self.direcionado:
            max_arestas //= 2
        
        return self.num_arestas / max_arestas
    
    def __str__(self) -> str:
        """Representação em string da lista de adjacência."""
        resultado = f"Grafo ({'direcionado' if self.direcionado else 'não-direcionado'}):\n"
        resultado += f"Vértices: {len(self.vertices)}, Arestas: {self.num_arestas}\n"
        resultado += "Lista de Adjacência:\n"
        
        for vertice in sorted(self.vertices):
            vizinhos = self.lista_adj[vertice]
            if vizinhos:
                vizinhos_str = ", ".join(str(v) for v in vizinhos)
                resultado += f"{vertice}: [{vizinhos_str}]\n"
            else:
                resultado += f"{vertice}: []\n"
        
        return resultado


class AlgoritmosGrafo:
    """
    Implementação de algoritmos fundamentais para grafos.
    """
    
    @staticmethod
    def dfs_recursivo(grafo: GrafoListaAdjacencia, inicio: Any, 
                     visitados: Optional[Set] = None) -> List[Any]:
        """
        Busca em Profundidade (DFS) recursiva.
        
        Args:
            grafo: Grafo para busca
            inicio: Vértice inicial
            visitados: Conjunto de vértices já visitados
        
        Returns:
            Lista de vértices na ordem de visitação
        """
        if visitados is None:
            visitados = set()
        
        caminho = []
        
        def dfs_helper(vertice):
            visitados.add(vertice)
            caminho.append(vertice)
            
            for vizinho in grafo.obter_vizinhos(vertice):
                if vizinho not in visitados:
                    dfs_helper(vizinho)
        
        dfs_helper(inicio)
        return caminho
    
    @staticmethod
    def dfs_iterativo(grafo: GrafoListaAdjacencia, inicio: Any) -> List[Any]:
        """
        Busca em Profundidade (DFS) iterativa usando pilha.
        
        Args:
            grafo: Grafo para busca
            inicio: Vértice inicial
        
        Returns:
            Lista de vértices na ordem de visitação
        """
        visitados = set()
        pilha = [inicio]
        caminho = []
        
        while pilha:
            vertice = pilha.pop()
            
            if vertice not in visitados:
                visitados.add(vertice)
                caminho.append(vertice)
                
                # Adicionar vizinhos na pilha (ordem reversa para manter ordem)
                vizinhos = grafo.obter_vizinhos(vertice)
                for vizinho in reversed(vizinhos):
                    if vizinho not in visitados:
                        pilha.append(vizinho)
        
        return caminho
    
    @staticmethod
    def bfs(grafo: GrafoListaAdjacencia, inicio: Any) -> List[Any]:
        """
        Busca em Largura (BFS) usando fila.
        
        Args:
            grafo: Grafo para busca
            inicio: Vértice inicial
        
        Returns:
            Lista de vértices na ordem de visitação
        """
        visitados = set()
        fila = deque([inicio])
        caminho = []
        
        visitados.add(inicio)
        
        while fila:
            vertice = fila.popleft()
            caminho.append(vertice)
            
            for vizinho in grafo.obter_vizinhos(vertice):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        
        return caminho
    
    @staticmethod
    def componentes_conectados(grafo: GrafoListaAdjacencia) -> List[List[Any]]:
        """
        Encontra todos os componentes conectados do grafo.
        
        Args:
            grafo: Grafo para análise
        
        Returns:
            Lista de componentes (cada componente é uma lista de vértices)
        """
        visitados = set()
        componentes = []
        
        for vertice in grafo.vertices:
            if vertice not in visitados:
                # DFS para encontrar componente conectado
                componente = AlgoritmosGrafo.dfs_recursivo(grafo, vertice, visitados)
                componentes.append(componente)
        
        return componentes
    
    @staticmethod
    def tem_ciclo_nao_direcionado(grafo: GrafoListaAdjacencia) -> bool:
        """
        Detecta ciclo em grafo não-direcionado usando DFS.
        
        Args:
            grafo: Grafo não-direcionado
        
        Returns:
            True se há ciclo, False caso contrário
        """
        if grafo.direcionado:
            raise ValueError("Use tem_ciclo_direcionado para grafos direcionados")
        
        visitados = set()
        
        def dfs_ciclo(vertice, pai):
            visitados.add(vertice)
            
            for vizinho in grafo.obter_vizinhos(vertice):
                if vizinho not in visitados:
                    if dfs_ciclo(vizinho, vertice):
                        return True
                elif vizinho != pai:  # Back edge encontrada
                    return True
            
            return False
        
        for vertice in grafo.vertices:
            if vertice not in visitados:
                if dfs_ciclo(vertice, None):
                    return True
        
        return False
    
    @staticmethod
    def tem_ciclo_direcionado(grafo: GrafoListaAdjacencia) -> bool:
        """
        Detecta ciclo em grafo direcionado usando DFS com cores.
        
        Args:
            grafo: Grafo direcionado
        
        Returns:
            True se há ciclo, False caso contrário
        """
        if not grafo.direcionado:
            raise ValueError("Use tem_ciclo_nao_direcionado para grafos não-direcionados")
        
        # Cores: 0=branco (não visitado), 1=cinza (visitando), 2=preto (visitado)
        cores = {vertice: 0 for vertice in grafo.vertices}
        
        def dfs_ciclo(vertice):
            cores[vertice] = 1  # Cinza
            
            for vizinho in grafo.obter_vizinhos(vertice):
                if cores[vizinho] == 1:  # Back edge para vértice cinza
                    return True
                elif cores[vizinho] == 0 and dfs_ciclo(vizinho):
                    return True
            
            cores[vertice] = 2  # Preto
            return False
        
        for vertice in grafo.vertices:
            if cores[vertice] == 0:
                if dfs_ciclo(vertice):
                    return True
        
        return False
    
    @staticmethod
    def ordenacao_topologica(grafo: GrafoListaAdjacencia) -> Optional[List[Any]]:
        """
        Ordenação topológica usando DFS.
        
        Args:
            grafo: Grafo direcionado acíclico (DAG)
        
        Returns:
            Lista com ordenação topológica ou None se há ciclo
        """
        if not grafo.direcionado:
            raise ValueError("Ordenação topológica só funciona em grafos direcionados")
        
        if AlgoritmosGrafo.tem_ciclo_direcionado(grafo):
            return None
        
        visitados = set()
        pilha = []
        
        def dfs_topologico(vertice):
            visitados.add(vertice)
            
            for vizinho in grafo.obter_vizinhos(vertice):
                if vizinho not in visitados:
                    dfs_topologico(vizinho)
            
            pilha.append(vertice)
        
        for vertice in grafo.vertices:
            if vertice not in visitados:
                dfs_topologico(vertice)
        
        return pilha[::-1]  # Reverter para obter ordem topológica
    
    @staticmethod
    def caminho_existe(grafo: GrafoListaAdjacencia, origem: Any, destino: Any) -> bool:
        """
        Verifica se existe caminho entre dois vértices.
        
        Args:
            grafo: Grafo para busca
            origem: Vértice de origem
            destino: Vértice de destino
        
        Returns:
            True se existe caminho, False caso contrário
        """
        if origem not in grafo.vertices or destino not in grafo.vertices:
            return False
        
        visitados = set()
        fila = deque([origem])
        visitados.add(origem)
        
        while fila:
            vertice = fila.popleft()
            
            if vertice == destino:
                return True
            
            for vizinho in grafo.obter_vizinhos(vertice):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        
        return False
    
    @staticmethod
    def distancia_minima(grafo: GrafoListaAdjacencia, origem: Any, destino: Any) -> int:
        """
        Calcula distância mínima entre dois vértices (BFS).
        
        Args:
            grafo: Grafo para busca
            origem: Vértice de origem
            destino: Vértice de destino
        
        Returns:
            Distância mínima ou -1 se não há caminho
        """
        if origem not in grafo.vertices or destino not in grafo.vertices:
            return -1
        
        if origem == destino:
            return 0
        
        visitados = set()
        fila = deque([(origem, 0)])
        visitados.add(origem)
        
        while fila:
            vertice, distancia = fila.popleft()
            
            for vizinho in grafo.obter_vizinhos(vertice):
                if vizinho == destino:
                    return distancia + 1
                
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append((vizinho, distancia + 1))
        
        return -1


# Aplicações Práticas
class RedeAmizade:
    """
    Simulação de rede social usando grafo.
    """
    
    def __init__(self):
        self.grafo = GrafoListaAdjacencia(direcionado=False)
        self.usuarios = {}
    
    def adicionar_usuario(self, id_usuario: str, nome: str):
        """Adiciona usuário à rede."""
        self.grafo.adicionar_vertice(id_usuario)
        self.usuarios[id_usuario] = nome
    
    def adicionar_amizade(self, usuario1: str, usuario2: str):
        """Cria amizade entre dois usuários."""
        if usuario1 in self.usuarios and usuario2 in self.usuarios:
            self.grafo.adicionar_aresta(usuario1, usuario2)
    
    def obter_amigos(self, usuario: str) -> List[str]:
        """Retorna lista de amigos de um usuário."""
        return self.grafo.obter_vizinhos(usuario)
    
    def sugerir_amigos(self, usuario: str) -> List[str]:
        """Sugere amigos baseado em amigos em comum."""
        amigos = set(self.obter_amigos(usuario))
        sugestoes = set()
        
        for amigo in amigos:
            amigos_do_amigo = set(self.obter_amigos(amigo))
            # Amigos de amigos que não são amigos diretos
            sugestoes.update(amigos_do_amigo - amigos - {usuario})
        
        return list(sugestoes)
    
    def grau_separacao(self, usuario1: str, usuario2: str) -> int:
        """Calcula graus de separação entre dois usuários."""
        return AlgoritmosGrafo.distancia_minima(self.grafo, usuario1, usuario2)
    
    def comunidades(self) -> List[List[str]]:
        """Identifica comunidades (componentes conectados)."""
        return AlgoritmosGrafo.componentes_conectados(self.grafo)


class SistemaPreRequisitos:
    """
    Sistema de pré-requisitos de disciplinas usando grafo direcionado.
    """
    
    def __init__(self):
        self.grafo = GrafoListaAdjacencia(direcionado=True)
        self.disciplinas = {}
    
    def adicionar_disciplina(self, codigo: str, nome: str):
        """Adiciona disciplina ao sistema."""
        self.grafo.adicionar_vertice(codigo)
        self.disciplinas[codigo] = nome
    
    def adicionar_prerequisito(self, disciplina: str, prerequisito: str):
        """Adiciona pré-requisito para uma disciplina."""
        if disciplina in self.disciplinas and prerequisito in self.disciplinas:
            self.grafo.adicionar_aresta(prerequisito, disciplina)
    
    def ordem_cursamento(self) -> Optional[List[str]]:
        """Retorna ordem possível para cursar todas as disciplinas."""
        return AlgoritmosGrafo.ordenacao_topologica(self.grafo)
    
    def pode_cursar(self, disciplina: str, cursadas: Set[str]) -> bool:
        """Verifica se pode cursar disciplina dados os pré-requisitos."""
        prerequisitos = set()
        
        # Encontrar todos os pré-requisitos (busca reversa)
        for disc in self.disciplinas:
            if AlgoritmosGrafo.caminho_existe(self.grafo, disc, disciplina):
                prerequisitos.add(disc)
        
        return prerequisitos.issubset(cursadas)
    
    def tem_ciclo_prerequisitos(self) -> bool:
        """Verifica se há ciclo nos pré-requisitos."""
        return AlgoritmosGrafo.tem_ciclo_direcionado(self.grafo)


# Funções de Demonstração e Benchmark
def demonstrar_representacoes():
    """Demonstra diferentes representações de grafos."""
    print("=== DEMONSTRAÇÃO: REPRESENTAÇÕES DE GRAFOS ===\n")
    
    # Criar grafo com matriz de adjacência
    print("1. MATRIZ DE ADJACÊNCIA:")
    grafo_matriz = GrafoMatrizAdjacencia(4, direcionado=False)
    grafo_matriz.adicionar_aresta(0, 1)
    grafo_matriz.adicionar_aresta(0, 2)
    grafo_matriz.adicionar_aresta(1, 3)
    grafo_matriz.adicionar_aresta(2, 3)
    
    print(grafo_matriz)
    print(f"Densidade: {grafo_matriz.densidade():.2f}")
    print(f"Grau do vértice 0: {grafo_matriz.grau_vertice(0)}")
    
    # Criar grafo com lista de adjacência
    print("\n2. LISTA DE ADJACÊNCIA:")
    grafo_lista = GrafoListaAdjacencia(direcionado=False)
    grafo_lista.adicionar_aresta('A', 'B')
    grafo_lista.adicionar_aresta('A', 'C')
    grafo_lista.adicionar_aresta('B', 'D')
    grafo_lista.adicionar_aresta('C', 'D')
    
    print(grafo_lista)
    print(f"Densidade: {grafo_lista.densidade():.2f}")
    print(f"Grau do vértice A: {grafo_lista.grau_vertice('A')}")


def demonstrar_algoritmos_travessia():
    """Demonstra algoritmos de travessia."""
    print("\n=== DEMONSTRAÇÃO: ALGORITMOS DE TRAVESSIA ===\n")
    
    # Criar grafo para demonstração
    grafo = GrafoListaAdjacencia(direcionado=False)
    arestas = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), 
               ('C', 'F'), ('D', 'G'), ('E', 'G'), ('F', 'G')]
    
    for origem, destino in arestas:
        grafo.adicionar_aresta(origem, destino)
    
    print("Grafo para travessia:")
    print(grafo)
    
    # DFS Recursivo
    print("1. DFS RECURSIVO (a partir de A):")
    dfs_rec = AlgoritmosGrafo.dfs_recursivo(grafo, 'A')
    print(f"Ordem de visitação: {' -> '.join(dfs_rec)}")
    
    # DFS Iterativo
    print("\n2. DFS ITERATIVO (a partir de A):")
    dfs_iter = AlgoritmosGrafo.dfs_iterativo(grafo, 'A')
    print(f"Ordem de visitação: {' -> '.join(dfs_iter)}")
    
    # BFS
    print("\n3. BFS (a partir de A):")
    bfs = AlgoritmosGrafo.bfs(grafo, 'A')
    print(f"Ordem de visitação: {' -> '.join(bfs)}")
    
    # Componentes conectados
    print("\n4. COMPONENTES CONECTADOS:")
    componentes = AlgoritmosGrafo.componentes_conectados(grafo)
    for i, comp in enumerate(componentes, 1):
        print(f"Componente {i}: {comp}")


def demonstrar_deteccao_ciclos():
    """Demonstra detecção de ciclos."""
    print("\n=== DEMONSTRAÇÃO: DETECÇÃO DE CICLOS ===\n")
    
    # Grafo não-direcionado sem ciclo
    print("1. GRAFO NÃO-DIRECIONADO SEM CICLO:")
    grafo_sem_ciclo = GrafoListaAdjacencia(direcionado=False)
    grafo_sem_ciclo.adicionar_aresta('A', 'B')
    grafo_sem_ciclo.adicionar_aresta('B', 'C')
    grafo_sem_ciclo.adicionar_aresta('C', 'D')
    
    print(f"Tem ciclo: {AlgoritmosGrafo.tem_ciclo_nao_direcionado(grafo_sem_ciclo)}")
    
    # Grafo não-direcionado com ciclo
    print("\n2. GRAFO NÃO-DIRECIONADO COM CICLO:")
    grafo_com_ciclo = GrafoListaAdjacencia(direcionado=False)
    grafo_com_ciclo.adicionar_aresta('A', 'B')
    grafo_com_ciclo.adicionar_aresta('B', 'C')
    grafo_com_ciclo.adicionar_aresta('C', 'A')
    
    print(f"Tem ciclo: {AlgoritmosGrafo.tem_ciclo_nao_direcionado(grafo_com_ciclo)}")
    
    # Grafo direcionado com ordenação topológica
    print("\n3. GRAFO DIRECIONADO - ORDENAÇÃO TOPOLÓGICA:")
    dag = GrafoListaAdjacencia(direcionado=True)
    dag.adicionar_aresta('Cálculo I', 'Cálculo II')
    dag.adicionar_aresta('Cálculo II', 'Cálculo III')
    dag.adicionar_aresta('Álgebra', 'Cálculo II')
    dag.adicionar_aresta('Programação I', 'Programação II')
    dag.adicionar_aresta('Programação II', 'Estruturas de Dados')
    
    ordem = AlgoritmosGrafo.ordenacao_topologica(dag)
    if ordem:
        print("Ordem topológica:")
        for i, disciplina in enumerate(ordem, 1):
            print(f"{i}. {disciplina}")
    else:
        print("Grafo tem ciclo - não é possível ordenação topológica")


def demonstrar_aplicacoes_praticas():
    """Demonstra aplicações práticas."""
    print("\n=== DEMONSTRAÇÃO: APLICAÇÕES PRÁTICAS ===\n")
    
    # Rede de amizade
    print("1. REDE SOCIAL:")
    rede = RedeAmizade()
    
    usuarios = [
        ('alice', 'Alice Silva'),
        ('bob', 'Bob Santos'),
        ('carol', 'Carol Lima'),
        ('david', 'David Costa'),
        ('eve', 'Eve Oliveira')
    ]
    
    for id_user, nome in usuarios:
        rede.adicionar_usuario(id_user, nome)
    
    amizades = [
        ('alice', 'bob'),
        ('alice', 'carol'),
        ('bob', 'david'),
        ('carol', 'eve'),
        ('david', 'eve')
    ]
    
    for u1, u2 in amizades:
        rede.adicionar_amizade(u1, u2)
    
    print(f"Amigos de Alice: {rede.obter_amigos('alice')}")
    print(f"Sugestões para Alice: {rede.sugerir_amigos('alice')}")
    print(f"Graus de separação Alice-Eve: {rede.grau_separacao('alice', 'eve')}")
    
    # Sistema de pré-requisitos
    print("\n2. SISTEMA DE PRÉ-REQUISITOS:")
    sistema = SistemaPreRequisitos()
    
    disciplinas = [
        ('MAT101', 'Cálculo I'),
        ('MAT102', 'Cálculo II'),
        ('MAT201', 'Álgebra Linear'),
        ('CS101', 'Programação I'),
        ('CS102', 'Programação II'),
        ('CS201', 'Estruturas de Dados')
    ]
    
    for codigo, nome in disciplinas:
        sistema.adicionar_disciplina(codigo, nome)
    
    prerequisitos = [
        ('MAT102', 'MAT101'),
        ('CS102', 'CS101'),
        ('CS201', 'CS102'),
        ('CS201', 'MAT201')
    ]
    
    for disc, prereq in prerequisitos:
        sistema.adicionar_prerequisito(disc, prereq)
    
    ordem = sistema.ordem_cursamento()
    if ordem:
        print("Ordem sugerida de cursamento:")
        for i, codigo in enumerate(ordem, 1):
            print(f"{i}. {codigo} - {sistema.disciplinas[codigo]}")
    
    cursadas = {'MAT101', 'CS101'}
    print(f"\nPode cursar CS201 tendo cursado {cursadas}: {sistema.pode_cursar('CS201', cursadas)}")


def benchmark_representacoes():
    """Compara performance das representações."""
    print("\n=== BENCHMARK: REPRESENTAÇÕES ===\n")
    
    tamanhos = [100, 500, 1000]
    
    for n in tamanhos:
        print(f"Testando com {n} vértices:")
        
        # Matriz de adjacência
        start_time = time.time()
        grafo_matriz = GrafoMatrizAdjacencia(n, direcionado=False)
        
        # Adicionar arestas aleatórias
        num_arestas = n * 2
        for _ in range(num_arestas):
            origem = random.randint(0, n-1)
            destino = random.randint(0, n-1)
            if origem != destino:
                grafo_matriz.adicionar_aresta(origem, destino)
        
        # Teste de busca
        for _ in range(1000):
            origem = random.randint(0, n-1)
            destino = random.randint(0, n-1)
            grafo_matriz.existe_aresta(origem, destino)
        
        tempo_matriz = time.time() - start_time
        
        # Lista de adjacência
        start_time = time.time()
        grafo_lista = GrafoListaAdjacencia(direcionado=False)
        
        # Adicionar arestas aleatórias
        for _ in range(num_arestas):
            origem = random.randint(0, n-1)
            destino = random.randint(0, n-1)
            if origem != destino:
                grafo_lista.adicionar_aresta(origem, destino)
        
        # Teste de busca
        for _ in range(1000):
            origem = random.randint(0, n-1)
            destino = random.randint(0, n-1)
            grafo_lista.existe_aresta(origem, destino)
        
        tempo_lista = time.time() - start_time
        
        print(f"  Matriz de adjacência: {tempo_matriz:.4f}s")
        print(f"  Lista de adjacência:  {tempo_lista:.4f}s")
        print(f"  Razão (matriz/lista): {tempo_matriz/tempo_lista:.2f}x")
        print()


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 05.7 - GRAFOS: CONCEITOS FUNDAMENTAIS")
    print("=" * 50)
    
    demonstrar_representacoes()
    demonstrar_algoritmos_travessia()
    demonstrar_deteccao_ciclos()
    demonstrar_aplicacoes_praticas()
    benchmark_representacoes()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 05.7")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. REPRESENTAÇÕES:
   • Matriz de adjacência: O(V²) espaço, O(1) busca de aresta
   • Lista de adjacência: O(V+E) espaço, O(grau) busca de aresta
   • Escolha depende da densidade do grafo

2. ALGORITMOS DE TRAVESSIA:
   • DFS: Explora profundidade, usa pilha (recursão ou iteração)
   • BFS: Explora largura, usa fila, encontra caminhos mínimos
   • Ambos têm complexidade O(V + E)

3. ANÁLISE DE CONECTIVIDADE:
   • Componentes conectados identificam grupos isolados
   • Detecção de ciclos é fundamental para validação
   • Ordenação topológica resolve dependências

4. APLICAÇÕES PRÁTICAS:
   • Redes sociais: Sugestões de amizade, graus de separação
   • Sistemas acadêmicos: Pré-requisitos, ordem de cursamento
   • Muitas outras: Redes de computadores, mapas, etc.

5. CONSIDERAÇÕES DE PERFORMANCE:
   • Grafos esparsos: Prefira lista de adjacência
   • Grafos densos: Matriz pode ser mais eficiente
   • Algoritmos têm complexidade linear no tamanho do grafo

Próximo módulo: Aplicações avançadas de grafos (Dijkstra, MST, etc.)
    """)


if __name__ == "__main__":
    main()