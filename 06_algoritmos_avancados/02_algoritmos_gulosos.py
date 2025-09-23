"""
MÓDULO 06.2 - ALGORITMOS GULOSOS
================================

Objetivos de Aprendizado:
- Compreender a estratégia gulosa (greedy)
- Identificar quando usar algoritmos gulosos
- Implementar algoritmos gulosos clássicos
- Analisar correção e otimalidade
- Comparar com programação dinâmica

Conceitos Abordados:
- Estratégia gulosa vs ótima global
- Propriedade de escolha gulosa
- Subestrutura ótima
- Algoritmos de escalonamento
- Algoritmos em grafos (MST, caminho mínimo)
- Códigos de Huffman
- Problemas de particionamento

Algoritmos Implementados:
- Activity Selection Problem
- Fractional Knapsack
- Job Scheduling
- Huffman Coding
- Minimum Spanning Tree (Kruskal, Prim)
- Dijkstra's Algorithm
- Interval Scheduling
- Gas Station Problem

Pré-requisitos:
- Estruturas de dados (heap, union-find)
- Algoritmos de ordenação
- Conceitos básicos de grafos

Complexidade Típica:
- Ordenação: O(n log n)
- Processamento: O(n) ou O(n log n)
- Total: geralmente O(n log n)
"""

from typing import List, Dict, Tuple, Optional, Set, Any
import heapq
import time
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Atividade:
    """Representa uma atividade com tempo de início e fim."""
    id: int
    inicio: int
    fim: int
    nome: str = ""
    
    def __post_init__(self):
        if not self.nome:
            self.nome = f"Atividade_{self.id}"
    
    def duracao(self) -> int:
        """Retorna a duração da atividade."""
        return self.fim - self.inicio
    
    def sobrepoe(self, outra: 'Atividade') -> bool:
        """Verifica se esta atividade se sobrepõe com outra."""
        return not (self.fim <= outra.inicio or outra.fim <= self.inicio)


@dataclass
class Item:
    """Representa um item com peso, valor e densidade."""
    id: int
    peso: float
    valor: float
    nome: str = ""
    
    def __post_init__(self):
        if not self.nome:
            self.nome = f"Item_{self.id}"
        self.densidade = self.valor / self.peso if self.peso > 0 else 0
    
    def __lt__(self, other):
        """Comparação para ordenação por densidade (decrescente)."""
        return self.densidade > other.densidade


@dataclass
class Trabalho:
    """Representa um trabalho com deadline e penalidade."""
    id: int
    deadline: int
    penalidade: int
    duracao: int = 1
    nome: str = ""
    
    def __post_init__(self):
        if not self.nome:
            self.nome = f"Trabalho_{self.id}"


class AlgoritmosGulosos:
    """
    Classe base para implementação de algoritmos gulosos.
    """
    
    def __init__(self):
        """Inicializa contadores para análise."""
        self.comparacoes = 0
        self.operacoes = 0
    
    def reset_contadores(self):
        """Reseta contadores de performance."""
        self.comparacoes = 0
        self.operacoes = 0


class ActivitySelection(AlgoritmosGulosos):
    """
    Implementação do problema de seleção de atividades.
    Objetivo: Selecionar máximo número de atividades não sobrepostas.
    """
    
    def __init__(self):
        super().__init__()
        self.atividades = []
    
    def adicionar_atividade(self, inicio: int, fim: int, nome: str = "") -> int:
        """
        Adiciona uma atividade.
        
        Args:
            inicio: Tempo de início
            fim: Tempo de fim
            nome: Nome da atividade
        
        Returns:
            ID da atividade adicionada
        """
        atividade_id = len(self.atividades)
        atividade = Atividade(atividade_id, inicio, fim, nome)
        self.atividades.append(atividade)
        return atividade_id
    
    def selecionar_atividades_guloso(self) -> Tuple[List[Atividade], int]:
        """
        Seleciona atividades usando estratégia gulosa.
        Estratégia: Sempre escolher atividade que termina mais cedo.
        
        Returns:
            Tupla com (atividades selecionadas, valor total)
        """
        if not self.atividades:
            return [], 0
        
        # Ordenar por tempo de fim (estratégia gulosa)
        atividades_ordenadas = sorted(self.atividades, key=lambda a: a.fim)
        self.operacoes += len(self.atividades)
        
        selecionadas = [atividades_ordenadas[0]]
        ultimo_fim = atividades_ordenadas[0].fim
        
        # Selecionar atividades compatíveis
        for atividade in atividades_ordenadas[1:]:
            self.comparacoes += 1
            self.operacoes += 1
            
            if atividade.inicio >= ultimo_fim:
                selecionadas.append(atividade)
                ultimo_fim = atividade.fim
        
        return selecionadas, len(selecionadas)
    
    def selecionar_atividades_recursivo(self, atividades: List[Atividade] = None, 
                                      indice: int = 0) -> List[Atividade]:
        """
        Versão recursiva do algoritmo guloso.
        
        Args:
            atividades: Lista de atividades ordenadas
            indice: Índice atual
        
        Returns:
            Lista de atividades selecionadas
        """
        if atividades is None:
            atividades = sorted(self.atividades, key=lambda a: a.fim)
        
        self.operacoes += 1
        
        # Caso base
        if indice >= len(atividades):
            return []
        
        # Encontrar próxima atividade compatível
        proximo_compativel = indice + 1
        while (proximo_compativel < len(atividades) and 
               atividades[proximo_compativel].inicio < atividades[indice].fim):
            proximo_compativel += 1
            self.comparacoes += 1
        
        # Incluir atividade atual + recursão
        return [atividades[indice]] + self.selecionar_atividades_recursivo(
            atividades, proximo_compativel)
    
    def analisar_sobreposicoes(self) -> Dict[str, Any]:
        """
        Analisa padrões de sobreposição entre atividades.
        
        Returns:
            Dicionário com estatísticas de sobreposição
        """
        if len(self.atividades) < 2:
            return {"total_pares": 0, "sobreposicoes": 0, "taxa_sobreposicao": 0}
        
        total_pares = 0
        sobreposicoes = 0
        matriz_sobreposicao = []
        
        for i, ativ1 in enumerate(self.atividades):
            linha = []
            for j, ativ2 in enumerate(self.atividades):
                if i != j:
                    total_pares += 1
                    sobrepoe = ativ1.sobrepoe(ativ2)
                    if sobrepoe:
                        sobreposicoes += 1
                    linha.append(sobrepoe)
                    self.comparacoes += 1
                else:
                    linha.append(False)
            matriz_sobreposicao.append(linha)
        
        # Ajustar para não contar pares duplicados
        total_pares //= 2
        sobreposicoes //= 2
        
        return {
            "total_pares": total_pares,
            "sobreposicoes": sobreposicoes,
            "taxa_sobreposicao": sobreposicoes / total_pares if total_pares > 0 else 0,
            "matriz_sobreposicao": matriz_sobreposicao
        }


class FractionalKnapsack(AlgoritmosGulosos):
    """
    Implementação do problema da mochila fracionária.
    Diferente da mochila 0/1, permite pegar frações de itens.
    """
    
    def __init__(self, capacidade: float):
        super().__init__()
        self.capacidade = capacidade
        self.itens = []
    
    def adicionar_item(self, peso: float, valor: float, nome: str = "") -> int:
        """
        Adiciona um item à mochila.
        
        Args:
            peso: Peso do item
            valor: Valor do item
            nome: Nome do item
        
        Returns:
            ID do item adicionado
        """
        item_id = len(self.itens)
        item = Item(item_id, peso, valor, nome)
        self.itens.append(item)
        return item_id
    
    def resolver_guloso(self) -> Tuple[float, List[Tuple[Item, float]]]:
        """
        Resolve usando estratégia gulosa.
        Estratégia: Ordenar por densidade (valor/peso) decrescente.
        
        Returns:
            Tupla com (valor total, lista de (item, fração_usada))
        """
        if not self.itens:
            return 0.0, []
        
        # Ordenar por densidade decrescente
        itens_ordenados = sorted(self.itens, reverse=True)
        self.operacoes += len(self.itens)
        
        valor_total = 0.0
        peso_usado = 0.0
        solucao = []
        
        for item in itens_ordenados:
            self.operacoes += 1
            
            # Se item cabe completamente
            if peso_usado + item.peso <= self.capacidade:
                solucao.append((item, 1.0))  # 100% do item
                valor_total += item.valor
                peso_usado += item.peso
                self.comparacoes += 1
            
            # Se item cabe parcialmente
            elif peso_usado < self.capacidade:
                fracao = (self.capacidade - peso_usado) / item.peso
                solucao.append((item, fracao))
                valor_total += item.valor * fracao
                peso_usado = self.capacidade
                self.comparacoes += 1
                break
            
            # Se não cabe, parar
            else:
                self.comparacoes += 1
                break
        
        return valor_total, solucao
    
    def comparar_com_01_knapsack(self) -> Dict[str, Any]:
        """
        Compara resultado com mochila 0/1 usando programação dinâmica.
        
        Returns:
            Dicionário com comparação dos resultados
        """
        # Resolver mochila fracionária
        valor_fracionario, solucao_fracionaria = self.resolver_guloso()
        
        # Resolver mochila 0/1 (versão simplificada)
        valor_01 = self._resolver_01_knapsack()
        
        return {
            "valor_fracionario": valor_fracionario,
            "valor_01": valor_01,
            "diferenca": valor_fracionario - valor_01,
            "razao": valor_fracionario / valor_01 if valor_01 > 0 else float('inf'),
            "solucao_fracionaria": [(item.nome, fracao) for item, fracao in solucao_fracionaria]
        }
    
    def _resolver_01_knapsack(self) -> float:
        """Resolve mochila 0/1 usando DP (versão simplificada)."""
        if not self.itens:
            return 0.0
        
        capacidade_int = int(self.capacidade)
        n = len(self.itens)
        
        # DP table
        dp = [[0.0] * (capacidade_int + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            item = self.itens[i - 1]
            peso_int = int(item.peso)
            
            for w in range(capacidade_int + 1):
                # Não incluir item
                dp[i][w] = dp[i - 1][w]
                
                # Incluir item se couber
                if peso_int <= w:
                    dp[i][w] = max(dp[i][w], dp[i - 1][w - peso_int] + item.valor)
        
        return dp[n][capacidade_int]


class JobScheduling(AlgoritmosGulosos):
    """
    Implementação de algoritmos de escalonamento de trabalhos.
    """
    
    def __init__(self):
        super().__init__()
        self.trabalhos = []
    
    def adicionar_trabalho(self, deadline: int, penalidade: int, 
                          duracao: int = 1, nome: str = "") -> int:
        """
        Adiciona um trabalho.
        
        Args:
            deadline: Prazo limite
            penalidade: Penalidade por atraso
            duracao: Duração do trabalho
            nome: Nome do trabalho
        
        Returns:
            ID do trabalho adicionado
        """
        trabalho_id = len(self.trabalhos)
        trabalho = Trabalho(trabalho_id, deadline, penalidade, duracao, nome)
        self.trabalhos.append(trabalho)
        return trabalho_id
    
    def minimizar_penalidade_guloso(self) -> Tuple[List[Trabalho], int]:
        """
        Minimiza penalidade total usando estratégia gulosa.
        Estratégia: Ordenar por penalidade decrescente.
        
        Returns:
            Tupla com (trabalhos escalonados, penalidade total)
        """
        if not self.trabalhos:
            return [], 0
        
        # Ordenar por penalidade decrescente
        trabalhos_ordenados = sorted(self.trabalhos, 
                                   key=lambda t: t.penalidade, reverse=True)
        self.operacoes += len(self.trabalhos)
        
        # Encontrar deadline máximo
        max_deadline = max(t.deadline for t in self.trabalhos)
        
        # Array para rastrear slots ocupados
        slots = [False] * max_deadline
        escalonados = []
        penalidade_total = 0
        
        for trabalho in trabalhos_ordenados:
            self.operacoes += 1
            
            # Tentar agendar no último slot possível antes do deadline
            agendado = False
            for slot in range(min(trabalho.deadline - 1, max_deadline - 1), -1, -1):
                self.comparacoes += 1
                
                if not slots[slot]:
                    slots[slot] = True
                    escalonados.append(trabalho)
                    agendado = True
                    break
            
            # Se não conseguiu agendar, adicionar penalidade
            if not agendado:
                penalidade_total += trabalho.penalidade
        
        return escalonados, penalidade_total
    
    def escalonamento_edf(self) -> List[Trabalho]:
        """
        Earliest Deadline First (EDF) scheduling.
        
        Returns:
            Lista de trabalhos ordenados por deadline
        """
        trabalhos_ordenados = sorted(self.trabalhos, key=lambda t: t.deadline)
        self.operacoes += len(self.trabalhos)
        
        return trabalhos_ordenados
    
    def escalonamento_sjf(self) -> List[Trabalho]:
        """
        Shortest Job First (SJF) scheduling.
        
        Returns:
            Lista de trabalhos ordenados por duração
        """
        trabalhos_ordenados = sorted(self.trabalhos, key=lambda t: t.duracao)
        self.operacoes += len(self.trabalhos)
        
        return trabalhos_ordenados


class HuffmanCoding(AlgoritmosGulosos):
    """
    Implementação do algoritmo de codificação de Huffman.
    """
    
    class No:
        """Nó da árvore de Huffman."""
        
        def __init__(self, char: str = None, freq: int = 0, 
                     esquerda=None, direita=None):
            self.char = char
            self.freq = freq
            self.esquerda = esquerda
            self.direita = direita
        
        def __lt__(self, other):
            return self.freq < other.freq
        
        def eh_folha(self) -> bool:
            return self.esquerda is None and self.direita is None
    
    def __init__(self):
        super().__init__()
        self.arvore_raiz = None
        self.codigos = {}
        self.frequencias = {}
    
    def calcular_frequencias(self, texto: str) -> Dict[str, int]:
        """
        Calcula frequências dos caracteres no texto.
        
        Args:
            texto: Texto para análise
        
        Returns:
            Dicionário com frequências
        """
        self.frequencias = {}
        
        for char in texto:
            self.frequencias[char] = self.frequencias.get(char, 0) + 1
            self.operacoes += 1
        
        return self.frequencias
    
    def construir_arvore(self, frequencias: Dict[str, int] = None) -> 'No':
        """
        Constrói árvore de Huffman usando estratégia gulosa.
        Estratégia: Sempre combinar dois nós com menor frequência.
        
        Args:
            frequencias: Dicionário de frequências
        
        Returns:
            Raiz da árvore de Huffman
        """
        if frequencias is None:
            frequencias = self.frequencias
        
        if not frequencias:
            return None
        
        # Criar heap com nós folha
        heap = []
        for char, freq in frequencias.items():
            no = self.No(char, freq)
            heapq.heappush(heap, no)
            self.operacoes += 1
        
        # Construir árvore
        while len(heap) > 1:
            self.operacoes += 1
            
            # Pegar dois nós com menor frequência
            no1 = heapq.heappop(heap)
            no2 = heapq.heappop(heap)
            
            # Criar nó interno
            no_interno = self.No(freq=no1.freq + no2.freq,
                               esquerda=no1, direita=no2)
            
            heapq.heappush(heap, no_interno)
            self.comparacoes += 1
        
        self.arvore_raiz = heap[0] if heap else None
        return self.arvore_raiz
    
    def gerar_codigos(self, no: 'No' = None, codigo: str = "") -> Dict[str, str]:
        """
        Gera códigos de Huffman percorrendo a árvore.
        
        Args:
            no: Nó atual (None para começar da raiz)
            codigo: Código atual sendo construído
        
        Returns:
            Dicionário com códigos dos caracteres
        """
        if no is None:
            no = self.arvore_raiz
            self.codigos = {}
        
        if no is None:
            return {}
        
        self.operacoes += 1
        
        # Se é folha, armazenar código
        if no.eh_folha():
            self.codigos[no.char] = codigo if codigo else "0"
            return self.codigos
        
        # Recursão para filhos
        if no.esquerda:
            self.gerar_codigos(no.esquerda, codigo + "0")
        if no.direita:
            self.gerar_codigos(no.direita, codigo + "1")
        
        return self.codigos
    
    def codificar(self, texto: str) -> Tuple[str, Dict[str, str], float]:
        """
        Codifica texto usando Huffman.
        
        Args:
            texto: Texto para codificar
        
        Returns:
            Tupla com (texto codificado, códigos, taxa de compressão)
        """
        if not texto:
            return "", {}, 0.0
        
        # Calcular frequências e construir árvore
        self.calcular_frequencias(texto)
        self.construir_arvore()
        self.gerar_codigos()
        
        # Codificar texto
        texto_codificado = ""
        for char in texto:
            texto_codificado += self.codigos.get(char, "")
            self.operacoes += 1
        
        # Calcular taxa de compressão
        bits_originais = len(texto) * 8  # ASCII
        bits_codificados = len(texto_codificado)
        taxa_compressao = 1 - (bits_codificados / bits_originais) if bits_originais > 0 else 0
        
        return texto_codificado, self.codigos, taxa_compressao
    
    def decodificar(self, texto_codificado: str) -> str:
        """
        Decodifica texto usando árvore de Huffman.
        
        Args:
            texto_codificado: Texto em binário
        
        Returns:
            Texto decodificado
        """
        if not texto_codificado or not self.arvore_raiz:
            return ""
        
        texto_decodificado = ""
        no_atual = self.arvore_raiz
        
        for bit in texto_codificado:
            self.operacoes += 1
            
            # Navegar na árvore
            if bit == "0" and no_atual.esquerda:
                no_atual = no_atual.esquerda
            elif bit == "1" and no_atual.direita:
                no_atual = no_atual.direita
            
            # Se chegou em folha, adicionar caractere
            if no_atual.eh_folha():
                texto_decodificado += no_atual.char
                no_atual = self.arvore_raiz
        
        return texto_decodificado


class MinimumSpanningTree(AlgoritmosGulosos):
    """
    Implementação de algoritmos para Árvore Geradora Mínima.
    """
    
    class UnionFind:
        """Estrutura Union-Find para detectar ciclos."""
        
        def __init__(self, n: int):
            self.parent = list(range(n))
            self.rank = [0] * n
        
        def find(self, x: int) -> int:
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])  # Path compression
            return self.parent[x]
        
        def union(self, x: int, y: int) -> bool:
            px, py = self.find(x), self.find(y)
            
            if px == py:
                return False  # Já estão no mesmo conjunto
            
            # Union by rank
            if self.rank[px] < self.rank[py]:
                px, py = py, px
            
            self.parent[py] = px
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
            
            return True
    
    def __init__(self, num_vertices: int):
        super().__init__()
        self.num_vertices = num_vertices
        self.arestas = []
        self.grafo_adj = defaultdict(list)
    
    def adicionar_aresta(self, u: int, v: int, peso: float):
        """
        Adiciona aresta ao grafo.
        
        Args:
            u: Vértice origem
            v: Vértice destino
            peso: Peso da aresta
        """
        self.arestas.append((peso, u, v))
        self.grafo_adj[u].append((v, peso))
        self.grafo_adj[v].append((u, peso))
    
    def kruskal(self) -> Tuple[List[Tuple[int, int, float]], float]:
        """
        Algoritmo de Kruskal para MST.
        Estratégia: Ordenar arestas por peso e adicionar se não formar ciclo.
        
        Returns:
            Tupla com (arestas da MST, peso total)
        """
        # Ordenar arestas por peso
        arestas_ordenadas = sorted(self.arestas)
        self.operacoes += len(self.arestas)
        
        # Inicializar Union-Find
        uf = self.UnionFind(self.num_vertices)
        mst = []
        peso_total = 0.0
        
        for peso, u, v in arestas_ordenadas:
            self.operacoes += 1
            self.comparacoes += 1
            
            # Se não formar ciclo, adicionar à MST
            if uf.union(u, v):
                mst.append((u, v, peso))
                peso_total += peso
                
                # MST completa quando tem n-1 arestas
                if len(mst) == self.num_vertices - 1:
                    break
        
        return mst, peso_total
    
    def prim(self, inicio: int = 0) -> Tuple[List[Tuple[int, int, float]], float]:
        """
        Algoritmo de Prim para MST.
        Estratégia: Começar de um vértice e sempre adicionar aresta mínima.
        
        Args:
            inicio: Vértice inicial
        
        Returns:
            Tupla com (arestas da MST, peso total)
        """
        if inicio >= self.num_vertices:
            return [], 0.0
        
        # Conjunto de vértices na MST
        na_mst = [False] * self.num_vertices
        na_mst[inicio] = True
        
        # Heap com arestas candidatas (peso, u, v)
        heap = []
        for v, peso in self.grafo_adj[inicio]:
            heapq.heappush(heap, (peso, inicio, v))
            self.operacoes += 1
        
        mst = []
        peso_total = 0.0
        
        while heap and len(mst) < self.num_vertices - 1:
            peso, u, v = heapq.heappop(heap)
            self.operacoes += 1
            self.comparacoes += 1
            
            # Se vértice já está na MST, pular
            if na_mst[v]:
                continue
            
            # Adicionar à MST
            mst.append((u, v, peso))
            peso_total += peso
            na_mst[v] = True
            
            # Adicionar novas arestas candidatas
            for w, peso_aresta in self.grafo_adj[v]:
                if not na_mst[w]:
                    heapq.heappush(heap, (peso_aresta, v, w))
                    self.operacoes += 1
        
        return mst, peso_total


class DijkstraAlgorithm(AlgoritmosGulosos):
    """
    Implementação do algoritmo de Dijkstra para caminho mínimo.
    """
    
    def __init__(self, num_vertices: int):
        super().__init__()
        self.num_vertices = num_vertices
        self.grafo = defaultdict(list)
    
    def adicionar_aresta(self, u: int, v: int, peso: float):
        """
        Adiciona aresta direcionada ao grafo.
        
        Args:
            u: Vértice origem
            v: Vértice destino
            peso: Peso da aresta
        """
        self.grafo[u].append((v, peso))
    
    def caminho_minimo(self, origem: int, destino: int = None) -> Dict[str, Any]:
        """
        Encontra caminho mínimo usando Dijkstra.
        Estratégia: Sempre processar vértice com menor distância.
        
        Args:
            origem: Vértice de origem
            destino: Vértice de destino (None para todos)
        
        Returns:
            Dicionário com distâncias e caminhos
        """
        if origem >= self.num_vertices:
            return {}
        
        # Inicializar distâncias
        distancias = [float('inf')] * self.num_vertices
        distancias[origem] = 0.0
        
        # Predecessores para reconstruir caminho
        predecessores = [-1] * self.num_vertices
        
        # Heap com (distância, vértice)
        heap = [(0.0, origem)]
        visitados = [False] * self.num_vertices
        
        while heap:
            dist_atual, u = heapq.heappop(heap)
            self.operacoes += 1
            
            # Se já foi processado, pular
            if visitados[u]:
                continue
            
            visitados[u] = True
            
            # Se chegou no destino específico, pode parar
            if destino is not None and u == destino:
                break
            
            # Relaxar arestas adjacentes
            for v, peso in self.grafo[u]:
                self.comparacoes += 1
                self.operacoes += 1
                
                nova_distancia = dist_atual + peso
                
                if nova_distancia < distancias[v]:
                    distancias[v] = nova_distancia
                    predecessores[v] = u
                    heapq.heappush(heap, (nova_distancia, v))
        
        # Construir resultado
        resultado = {
            "distancias": distancias,
            "predecessores": predecessores,
            "origem": origem
        }
        
        # Se destino específico, adicionar caminho
        if destino is not None:
            caminho = self._reconstruir_caminho(predecessores, origem, destino)
            resultado["caminho"] = caminho
            resultado["distancia_destino"] = distancias[destino]
        
        return resultado
    
    def _reconstruir_caminho(self, predecessores: List[int], 
                           origem: int, destino: int) -> List[int]:
        """Reconstrói caminho a partir dos predecessores."""
        if predecessores[destino] == -1 and destino != origem:
            return []  # Não há caminho
        
        caminho = []
        atual = destino
        
        while atual != -1:
            caminho.append(atual)
            atual = predecessores[atual]
        
        caminho.reverse()
        return caminho


# Funções de Demonstração
def demonstrar_activity_selection():
    """Demonstra seleção de atividades."""
    print("=== DEMONSTRAÇÃO: SELEÇÃO DE ATIVIDADES ===\n")
    
    activity_sel = ActivitySelection()
    
    # Adicionar atividades
    atividades_exemplo = [
        (1, 4, "Reunião A"),
        (3, 5, "Apresentação"),
        (0, 6, "Workshop"),
        (5, 7, "Treinamento"),
        (3, 9, "Conferência"),
        (5, 9, "Seminário"),
        (6, 10, "Palestra"),
        (8, 11, "Mesa Redonda"),
        (8, 12, "Debate"),
        (2, 14, "Curso"),
        (12, 16, "Networking")
    ]
    
    for inicio, fim, nome in atividades_exemplo:
        activity_sel.adicionar_atividade(inicio, fim, nome)
    
    print("Atividades disponíveis:")
    for ativ in activity_sel.atividades:
        print(f"  {ativ.nome}: [{ativ.inicio}, {ativ.fim}] (duração: {ativ.duracao()})")
    
    # Resolver com algoritmo guloso
    activity_sel.reset_contadores()
    start_time = time.time()
    selecionadas, total = activity_sel.selecionar_atividades_guloso()
    tempo_guloso = time.time() - start_time
    
    print(f"\nSolução Gulosa:")
    print(f"  Atividades selecionadas: {total}")
    print(f"  Tempo: {tempo_guloso:.6f}s")
    print(f"  Operações: {activity_sel.operacoes}")
    print(f"  Comparações: {activity_sel.comparacoes}")
    
    print(f"\nAtividades escolhidas:")
    for ativ in selecionadas:
        print(f"  {ativ.nome}: [{ativ.inicio}, {ativ.fim}]")
    
    # Analisar sobreposições
    analise = activity_sel.analisar_sobreposicoes()
    print(f"\nAnálise de Sobreposições:")
    print(f"  Total de pares: {analise['total_pares']}")
    print(f"  Sobreposições: {analise['sobreposicoes']}")
    print(f"  Taxa de sobreposição: {analise['taxa_sobreposicao']:.2%}")


def demonstrar_fractional_knapsack():
    """Demonstra mochila fracionária."""
    print("\n=== DEMONSTRAÇÃO: MOCHILA FRACIONÁRIA ===\n")
    
    knapsack = FractionalKnapsack(50.0)
    
    # Adicionar itens
    itens_exemplo = [
        (20, 100, "Ouro"),
        (30, 120, "Prata"),
        (10, 60, "Diamante"),
        (15, 40, "Rubi"),
        (25, 80, "Esmeralda")
    ]
    
    for peso, valor, nome in itens_exemplo:
        knapsack.adicionar_item(peso, valor, nome)
    
    print("Itens disponíveis:")
    for item in knapsack.itens:
        print(f"  {item.nome}: peso={item.peso}, valor={item.valor}, "
              f"densidade={item.densidade:.2f}")
    
    print(f"\nCapacidade da mochila: {knapsack.capacidade}")
    
    # Resolver
    knapsack.reset_contadores()
    start_time = time.time()
    valor_total, solucao = knapsack.resolver_guloso()
    tempo = time.time() - start_time
    
    print(f"\nSolução Gulosa:")
    print(f"  Valor total: {valor_total:.2f}")
    print(f"  Tempo: {tempo:.6f}s")
    print(f"  Operações: {knapsack.operacoes}")
    
    print(f"\nItens selecionados:")
    peso_usado = 0
    for item, fracao in solucao:
        peso_item = item.peso * fracao
        valor_item = item.valor * fracao
        peso_usado += peso_item
        print(f"  {item.nome}: {fracao:.1%} (peso={peso_item:.1f}, valor={valor_item:.1f})")
    
    print(f"\nPeso total usado: {peso_usado:.1f}/{knapsack.capacidade}")
    
    # Comparar com mochila 0/1
    comparacao = knapsack.comparar_com_01_knapsack()
    print(f"\nComparação com Mochila 0/1:")
    print(f"  Valor fracionário: {comparacao['valor_fracionario']:.2f}")
    print(f"  Valor 0/1: {comparacao['valor_01']:.2f}")
    print(f"  Diferença: {comparacao['diferenca']:.2f}")
    print(f"  Razão: {comparacao['razao']:.2f}")


def demonstrar_job_scheduling():
    """Demonstra escalonamento de trabalhos."""
    print("\n=== DEMONSTRAÇÃO: ESCALONAMENTO DE TRABALHOS ===\n")
    
    scheduler = JobScheduling()
    
    # Adicionar trabalhos
    trabalhos_exemplo = [
        (4, 20, 1, "Relatório A"),
        (1, 10, 1, "Email B"),
        (4, 40, 1, "Apresentação C"),
        (3, 30, 1, "Reunião D"),
        (2, 15, 1, "Ligação E")
    ]
    
    for deadline, penalidade, duracao, nome in trabalhos_exemplo:
        scheduler.adicionar_trabalho(deadline, penalidade, duracao, nome)
    
    print("Trabalhos disponíveis:")
    for trabalho in scheduler.trabalhos:
        print(f"  {trabalho.nome}: deadline={trabalho.deadline}, "
              f"penalidade={trabalho.penalidade}")
    
    # Minimizar penalidade
    scheduler.reset_contadores()
    start_time = time.time()
    escalonados, penalidade = scheduler.minimizar_penalidade_guloso()
    tempo = time.time() - start_time
    
    print(f"\nEscalonamento para Minimizar Penalidade:")
    print(f"  Trabalhos escalonados: {len(escalonados)}")
    print(f"  Penalidade total: {penalidade}")
    print(f"  Tempo: {tempo:.6f}s")
    print(f"  Operações: {scheduler.operacoes}")
    
    print(f"\nTrabalhos escalonados:")
    for i, trabalho in enumerate(escalonados):
        print(f"  Slot {i+1}: {trabalho.nome}")
    
    # Outros algoritmos
    edf = scheduler.escalonamento_edf()
    sjf = scheduler.escalonamento_sjf()
    
    print(f"\nEarliest Deadline First:")
    for trabalho in edf:
        print(f"  {trabalho.nome} (deadline: {trabalho.deadline})")
    
    print(f"\nShortest Job First:")
    for trabalho in sjf:
        print(f"  {trabalho.nome} (duração: {trabalho.duracao})")


def demonstrar_huffman():
    """Demonstra codificação de Huffman."""
    print("\n=== DEMONSTRAÇÃO: CODIFICAÇÃO DE HUFFMAN ===\n")
    
    huffman = HuffmanCoding()
    
    texto = "ABRACADABRA"
    print(f"Texto original: '{texto}'")
    print(f"Tamanho original: {len(texto)} caracteres ({len(texto) * 8} bits)")
    
    # Calcular frequências
    frequencias = huffman.calcular_frequencias(texto)
    print(f"\nFrequências:")
    for char, freq in sorted(frequencias.items()):
        print(f"  '{char}': {freq}")
    
    # Codificar
    huffman.reset_contadores()
    start_time = time.time()
    texto_codificado, codigos, taxa_compressao = huffman.codificar(texto)
    tempo = time.time() - start_time
    
    print(f"\nCódigos de Huffman:")
    for char, codigo in sorted(codigos.items()):
        print(f"  '{char}': {codigo}")
    
    print(f"\nResultado da Codificação:")
    print(f"  Texto codificado: {texto_codificado}")
    print(f"  Tamanho codificado: {len(texto_codificado)} bits")
    print(f"  Taxa de compressão: {taxa_compressao:.2%}")
    print(f"  Tempo: {tempo:.6f}s")
    print(f"  Operações: {huffman.operacoes}")
    
    # Decodificar
    texto_decodificado = huffman.decodificar(texto_codificado)
    print(f"\nDecodificação:")
    print(f"  Texto decodificado: '{texto_decodificado}'")
    print(f"  Correto: {texto == texto_decodificado}")


def demonstrar_mst():
    """Demonstra algoritmos de MST."""
    print("\n=== DEMONSTRAÇÃO: ÁRVORE GERADORA MÍNIMA ===\n")
    
    # Criar grafo
    mst = MinimumSpanningTree(6)
    
    # Adicionar arestas
    arestas_exemplo = [
        (0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5),
        (2, 3, 8), (2, 4, 10), (3, 4, 2), (3, 5, 6), (4, 5, 3)
    ]
    
    for u, v, peso in arestas_exemplo:
        mst.adicionar_aresta(u, v, peso)
    
    print("Grafo:")
    for u, v, peso in arestas_exemplo:
        print(f"  {u} -- {v}: {peso}")
    
    # Kruskal
    mst.reset_contadores()
    start_time = time.time()
    mst_kruskal, peso_kruskal = mst.kruskal()
    tempo_kruskal = time.time() - start_time
    
    print(f"\nAlgoritmo de Kruskal:")
    print(f"  Peso total: {peso_kruskal}")
    print(f"  Tempo: {tempo_kruskal:.6f}s")
    print(f"  Operações: {mst.operacoes}")
    print(f"  Comparações: {mst.comparacoes}")
    
    print(f"  Arestas da MST:")
    for u, v, peso in mst_kruskal:
        print(f"    {u} -- {v}: {peso}")
    
    # Prim
    mst.reset_contadores()
    start_time = time.time()
    mst_prim, peso_prim = mst.prim()
    tempo_prim = time.time() - start_time
    
    print(f"\nAlgoritmo de Prim:")
    print(f"  Peso total: {peso_prim}")
    print(f"  Tempo: {tempo_prim:.6f}s")
    print(f"  Operações: {mst.operacoes}")
    print(f"  Comparações: {mst.comparacoes}")
    
    print(f"  Arestas da MST:")
    for u, v, peso in mst_prim:
        print(f"    {u} -- {v}: {peso}")


def demonstrar_dijkstra():
    """Demonstra algoritmo de Dijkstra."""
    print("\n=== DEMONSTRAÇÃO: ALGORITMO DE DIJKSTRA ===\n")
    
    # Criar grafo direcionado
    dijkstra = DijkstraAlgorithm(6)
    
    # Adicionar arestas
    arestas_exemplo = [
        (0, 1, 4), (0, 2, 2), (1, 2, 3), (1, 3, 2), (1, 4, 3),
        (2, 3, 4), (2, 4, 5), (3, 4, 1), (3, 5, 6), (4, 5, 2)
    ]
    
    for u, v, peso in arestas_exemplo:
        dijkstra.adicionar_aresta(u, v, peso)
    
    print("Grafo direcionado:")
    for u, v, peso in arestas_exemplo:
        print(f"  {u} -> {v}: {peso}")
    
    # Encontrar caminhos mínimos
    origem = 0
    destino = 5
    
    dijkstra.reset_contadores()
    start_time = time.time()
    resultado = dijkstra.caminho_minimo(origem, destino)
    tempo = time.time() - start_time
    
    print(f"\nCaminho Mínimo de {origem} para {destino}:")
    print(f"  Distância: {resultado['distancia_destino']}")
    print(f"  Caminho: {' -> '.join(map(str, resultado['caminho']))}")
    print(f"  Tempo: {tempo:.6f}s")
    print(f"  Operações: {dijkstra.operacoes}")
    print(f"  Comparações: {dijkstra.comparacoes}")
    
    # Todas as distâncias
    resultado_completo = dijkstra.caminho_minimo(origem)
    print(f"\nDistâncias de {origem} para todos os vértices:")
    for i, dist in enumerate(resultado_completo['distancias']):
        if dist == float('inf'):
            print(f"  {origem} -> {i}: ∞")
        else:
            print(f"  {origem} -> {i}: {dist}")


def benchmark_algoritmos_gulosos():
    """Compara performance dos algoritmos gulosos."""
    print("\n=== BENCHMARK: ALGORITMOS GULOSOS ===\n")
    
    # Benchmark Activity Selection
    print("Benchmark Activity Selection:")
    for n in [100, 500, 1000]:
        activity_sel = ActivitySelection()
        
        # Gerar atividades aleatórias
        import random
        random.seed(42)
        
        for i in range(n):
            inicio = random.randint(0, 100)
            fim = inicio + random.randint(1, 20)
            activity_sel.adicionar_atividade(inicio, fim)
        
        activity_sel.reset_contadores()
        start_time = time.time()
        activity_sel.selecionar_atividades_guloso()
        tempo = time.time() - start_time
        
        print(f"  n={n}: {tempo:.6f}s, operações={activity_sel.operacoes}")
    
    # Benchmark Huffman
    print("\nBenchmark Huffman Coding:")
    textos = [
        "A" * 100,
        "ABCDEFGHIJ" * 50,
        "The quick brown fox jumps over the lazy dog. " * 20
    ]
    
    for i, texto in enumerate(textos):
        huffman = HuffmanCoding()
        huffman.reset_contadores()
        
        start_time = time.time()
        huffman.codificar(texto)
        tempo = time.time() - start_time
        
        print(f"  Texto {i+1} (len={len(texto)}): {tempo:.6f}s, "
              f"operações={huffman.operacoes}")


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 06.2 - ALGORITMOS GULOSOS")
    print("=" * 50)
    
    demonstrar_activity_selection()
    demonstrar_fractional_knapsack()
    demonstrar_job_scheduling()
    demonstrar_huffman()
    demonstrar_mst()
    demonstrar_dijkstra()
    benchmark_algoritmos_gulosos()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 06.2")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. ESTRATÉGIA GULOSA:
   • Fazer escolha localmente ótima em cada passo
   • Não reconsiderar decisões anteriores
   • Nem sempre produz solução globalmente ótima
   • Eficiente quando aplicável (geralmente O(n log n))

2. QUANDO USAR ALGORITMOS GULOSOS:
   • Problema tem propriedade de escolha gulosa
   • Subestrutura ótima está presente
   • Escolha local leva à solução global ótima
   • Eficiência é prioritária sobre otimalidade absoluta

3. PROBLEMAS CLÁSSICOS IMPLEMENTADOS:
   • Activity Selection: máximo de atividades não sobrepostas
   • Fractional Knapsack: mochila com frações permitidas
   • Job Scheduling: minimizar penalidades ou tempo
   • Huffman Coding: compressão ótima de dados
   • MST (Kruskal/Prim): árvore geradora mínima
   • Dijkstra: caminho mínimo em grafos

4. TÉCNICAS DE IMPLEMENTAÇÃO:
   • Ordenação como estratégia principal
   • Uso de estruturas auxiliares (heap, union-find)
   • Critérios de seleção gulosa específicos
   • Verificação de viabilidade em cada passo

5. ANÁLISE DE CORREÇÃO:
   • Propriedade de escolha gulosa: escolha local é segura
   • Subestrutura ótima: problema reduzido mantém otimalidade
   • Prova por indução ou contradição
   • Comparação com solução ótima conhecida

6. VANTAGENS DOS ALGORITMOS GULOSOS:
   • Simplicidade de implementação
   • Eficiência temporal excelente
   • Uso de memória reduzido
   • Fácil compreensão e manutenção

7. LIMITAÇÕES:
   • Nem sempre produzem solução ótima
   • Difícil provar correção em alguns casos
   • Podem ser míopes (visão local)
   • Sensíveis à ordem de processamento

8. APLICAÇÕES PRÁTICAS:
   • Algoritmos de compressão (Huffman, LZ)
   • Roteamento em redes (Dijkstra, OSPF)
   • Escalonamento de processos
   • Otimização de recursos
   • Algoritmos de aproximação

9. COMPARAÇÃO COM OUTRAS TÉCNICAS:
   • vs DP: mais rápido, mas nem sempre ótimo
   • vs Força Bruta: muito mais eficiente
   • vs Backtracking: não explora todas possibilidades
   • vs Heurísticas: mais fundamentado teoricamente

10. ESTRATÉGIAS DE OTIMIZAÇÃO:
    • Escolher critério guloso adequado
    • Usar estruturas de dados eficientes
    • Pré-processar dados quando possível
    • Combinar com outras técnicas quando necessário

Os algoritmos gulosos são fundamentais em ciência da computação,
oferecendo soluções eficientes para muitos problemas de otimização.
Embora nem sempre garantam a solução ótima, sua simplicidade e
eficiência os tornam escolhas valiosas em muitos cenários práticos.

Próximo arquivo: Backtracking
    """)


if __name__ == "__main__":
    main()