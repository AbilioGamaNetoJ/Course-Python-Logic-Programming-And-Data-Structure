"""
MÓDULO 05 - ESTRUTURAS DE DADOS NÃO-LINEARES
Arquivo 08: Aplicações Práticas de Grafos

OBJETIVOS DE APRENDIZADO:
- Implementar algoritmos clássicos de grafos (Dijkstra, Kruskal, Prim)
- Desenvolver sistemas de navegação e roteamento
- Analisar redes sociais e métricas de centralidade
- Aplicar grafos em problemas do mundo real
- Otimizar algoritmos para grandes volumes de dados

CONCEITOS ABORDADOS:
1. Algoritmo de Dijkstra (caminho mais curto)
2. Árvores Geradoras Mínimas (Kruskal e Prim)
3. Algoritmo de Floyd-Warshall (todos os pares)
4. Análise de Redes Sociais
5. Sistemas de Navegação GPS
6. Detecção de Comunidades
7. Fluxo Máximo (Ford-Fulkerson)
8. Coloração de Grafos

PRÉ-REQUISITOS:
- Conhecimento de grafos básicos (arquivo 07)
- Estruturas de dados (heaps, union-find)
- Conceitos de complexidade algorítmica

COMPLEXIDADE DAS OPERAÇÕES:
- Dijkstra: O((V + E) log V) com heap binário
- Kruskal: O(E log E) para ordenação das arestas
- Prim: O((V + E) log V) com heap binário
- Floyd-Warshall: O(V³) para todos os pares
- BFS/DFS: O(V + E) para análise de conectividade
"""

import heapq
import math
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Set, Optional, Any
import time
import random


class GrafoPonderado:
    """
    Implementação de grafo ponderado para algoritmos avançados.
    Suporta tanto grafos direcionados quanto não-direcionados.
    """
    
    def __init__(self, direcionado: bool = False):
        self.direcionado = direcionado
        self.vertices = set()
        self.arestas = defaultdict(list)  # {vertice: [(vizinho, peso), ...]}
        self.num_arestas = 0
    
    def adicionar_vertice(self, vertice: Any) -> None:
        """Adiciona um vértice ao grafo."""
        self.vertices.add(vertice)
    
    def adicionar_aresta(self, origem: Any, destino: Any, peso: float) -> None:
        """Adiciona uma aresta ponderada ao grafo."""
        self.vertices.add(origem)
        self.vertices.add(destino)
        
        self.arestas[origem].append((destino, peso))
        if not self.direcionado:
            self.arestas[destino].append((origem, peso))
        
        self.num_arestas += 1
    
    def obter_vizinhos(self, vertice: Any) -> List[Tuple[Any, float]]:
        """Retorna lista de vizinhos com seus pesos."""
        return self.arestas[vertice]
    
    def obter_todas_arestas(self) -> List[Tuple[Any, Any, float]]:
        """Retorna todas as arestas como lista de tuplas (origem, destino, peso)."""
        arestas = []
        visitadas = set()
        
        for origem in self.vertices:
            for destino, peso in self.arestas[origem]:
                if self.direcionado:
                    arestas.append((origem, destino, peso))
                else:
                    # Para grafos não-direcionados, evita duplicatas
                    aresta = tuple(sorted([origem, destino])) + (peso,)
                    if aresta not in visitadas:
                        arestas.append((origem, destino, peso))
                        visitadas.add(aresta)
        
        return arestas
    
    def densidade(self) -> float:
        """Calcula a densidade do grafo."""
        n = len(self.vertices)
        if n < 2:
            return 0.0
        
        max_arestas = n * (n - 1)
        if not self.direcionado:
            max_arestas //= 2
        
        return self.num_arestas / max_arestas


class AlgoritmoDijkstra:
    """
    Implementação do algoritmo de Dijkstra para encontrar
    o caminho mais curto entre dois vértices.
    """
    
    @staticmethod
    def caminho_mais_curto(grafo: GrafoPonderado, origem: Any, destino: Any = None) -> Dict:
        """
        Encontra o caminho mais curto usando Dijkstra.
        
        Args:
            grafo: Grafo ponderado
            origem: Vértice de origem
            destino: Vértice de destino (opcional, se None calcula para todos)
        
        Returns:
            Dict com distâncias e caminhos
        """
        if origem not in grafo.vertices:
            raise ValueError(f"Vértice de origem {origem} não existe no grafo")
        
        # Inicialização
        distancias = {v: float('inf') for v in grafo.vertices}
        predecessores = {v: None for v in grafo.vertices}
        visitados = set()
        
        distancias[origem] = 0
        heap = [(0, origem)]
        
        while heap:
            dist_atual, vertice_atual = heapq.heappop(heap)
            
            if vertice_atual in visitados:
                continue
            
            visitados.add(vertice_atual)
            
            # Se chegamos ao destino, podemos parar
            if destino and vertice_atual == destino:
                break
            
            # Relaxamento das arestas
            for vizinho, peso in grafo.obter_vizinhos(vertice_atual):
                if vizinho not in visitados:
                    nova_distancia = dist_atual + peso
                    
                    if nova_distancia < distancias[vizinho]:
                        distancias[vizinho] = nova_distancia
                        predecessores[vizinho] = vertice_atual
                        heapq.heappush(heap, (nova_distancia, vizinho))
        
        return {
            'distancias': distancias,
            'predecessores': predecessores,
            'caminho': AlgoritmoDijkstra._reconstruir_caminho(predecessores, origem, destino) if destino else None
        }
    
    @staticmethod
    def _reconstruir_caminho(predecessores: Dict, origem: Any, destino: Any) -> List[Any]:
        """Reconstrói o caminho a partir dos predecessores."""
        if predecessores[destino] is None and destino != origem:
            return []  # Não há caminho
        
        caminho = []
        atual = destino
        
        while atual is not None:
            caminho.append(atual)
            atual = predecessores[atual]
        
        return caminho[::-1]


class UnionFind:
    """
    Estrutura Union-Find (Disjoint Set) para algoritmo de Kruskal.
    Implementa otimizações de compressão de caminho e união por rank.
    """
    
    def __init__(self, elementos: Set[Any]):
        self.pai = {elem: elem for elem in elementos}
        self.rank = {elem: 0 for elem in elementos}
    
    def encontrar(self, x: Any) -> Any:
        """Encontra o representante do conjunto com compressão de caminho."""
        if self.pai[x] != x:
            self.pai[x] = self.encontrar(self.pai[x])  # Compressão de caminho
        return self.pai[x]
    
    def unir(self, x: Any, y: Any) -> bool:
        """Une dois conjuntos usando união por rank."""
        raiz_x = self.encontrar(x)
        raiz_y = self.encontrar(y)
        
        if raiz_x == raiz_y:
            return False  # Já estão no mesmo conjunto
        
        # União por rank
        if self.rank[raiz_x] < self.rank[raiz_y]:
            self.pai[raiz_x] = raiz_y
        elif self.rank[raiz_x] > self.rank[raiz_y]:
            self.pai[raiz_y] = raiz_x
        else:
            self.pai[raiz_y] = raiz_x
            self.rank[raiz_x] += 1
        
        return True


class ArvoreGeradoraMinima:
    """
    Implementação dos algoritmos de Kruskal e Prim para
    encontrar a Árvore Geradora Mínima (MST).
    """
    
    @staticmethod
    def kruskal(grafo: GrafoPonderado) -> Tuple[List[Tuple], float]:
        """
        Algoritmo de Kruskal para MST.
        
        Returns:
            Tupla com (arestas_mst, peso_total)
        """
        if grafo.direcionado:
            raise ValueError("Algoritmo de Kruskal requer grafo não-direcionado")
        
        # Obter todas as arestas e ordená-las por peso
        arestas = grafo.obter_todas_arestas()
        arestas.sort(key=lambda x: x[2])  # Ordena por peso
        
        # Inicializar Union-Find
        uf = UnionFind(grafo.vertices)
        mst = []
        peso_total = 0
        
        for origem, destino, peso in arestas:
            if uf.unir(origem, destino):
                mst.append((origem, destino, peso))
                peso_total += peso
                
                # MST completa quando temos V-1 arestas
                if len(mst) == len(grafo.vertices) - 1:
                    break
        
        return mst, peso_total
    
    @staticmethod
    def prim(grafo: GrafoPonderado, inicio: Any = None) -> Tuple[List[Tuple], float]:
        """
        Algoritmo de Prim para MST.
        
        Args:
            grafo: Grafo não-direcionado
            inicio: Vértice inicial (se None, escolhe arbitrariamente)
        
        Returns:
            Tupla com (arestas_mst, peso_total)
        """
        if grafo.direcionado:
            raise ValueError("Algoritmo de Prim requer grafo não-direcionado")
        
        if not grafo.vertices:
            return [], 0
        
        if inicio is None:
            inicio = next(iter(grafo.vertices))
        
        mst = []
        peso_total = 0
        visitados = {inicio}
        heap = []
        
        # Adicionar todas as arestas do vértice inicial ao heap
        for vizinho, peso in grafo.obter_vizinhos(inicio):
            heapq.heappush(heap, (peso, inicio, vizinho))
        
        while heap and len(visitados) < len(grafo.vertices):
            peso, origem, destino = heapq.heappop(heap)
            
            if destino in visitados:
                continue
            
            # Adicionar aresta à MST
            mst.append((origem, destino, peso))
            peso_total += peso
            visitados.add(destino)
            
            # Adicionar novas arestas ao heap
            for vizinho, peso_aresta in grafo.obter_vizinhos(destino):
                if vizinho not in visitados:
                    heapq.heappush(heap, (peso_aresta, destino, vizinho))
        
        return mst, peso_total


class FloydWarshall:
    """
    Implementação do algoritmo Floyd-Warshall para encontrar
    todos os caminhos mais curtos entre todos os pares de vértices.
    """
    
    @staticmethod
    def todos_caminhos_minimos(grafo: GrafoPonderado) -> Dict:
        """
        Calcula todos os caminhos mínimos usando Floyd-Warshall.
        
        Returns:
            Dict com matrizes de distâncias e próximos vértices
        """
        vertices = list(grafo.vertices)
        n = len(vertices)
        
        # Mapear vértices para índices
        indice = {v: i for i, v in enumerate(vertices)}
        
        # Inicializar matrizes
        dist = [[float('inf')] * n for _ in range(n)]
        proximo = [[None] * n for _ in range(n)]
        
        # Distância de um vértice para ele mesmo é 0
        for i in range(n):
            dist[i][i] = 0
        
        # Preencher distâncias diretas
        for v in vertices:
            i = indice[v]
            for vizinho, peso in grafo.obter_vizinhos(v):
                j = indice[vizinho]
                dist[i][j] = peso
                proximo[i][j] = vizinho
        
        # Algoritmo Floyd-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        proximo[i][j] = proximo[i][k]
        
        return {
            'vertices': vertices,
            'distancias': dist,
            'proximo': proximo,
            'indice': indice
        }
    
    @staticmethod
    def obter_caminho(resultado_fw: Dict, origem: Any, destino: Any) -> List[Any]:
        """Reconstrói o caminho entre dois vértices."""
        vertices = resultado_fw['vertices']
        proximo = resultado_fw['proximo']
        indice = resultado_fw['indice']
        
        if origem not in indice or destino not in indice:
            return []
        
        i, j = indice[origem], indice[destino]
        
        if proximo[i][j] is None:
            return []  # Não há caminho
        
        caminho = [origem]
        atual = origem
        
        while atual != destino:
            atual = proximo[indice[atual]][j]
            caminho.append(atual)
        
        return caminho


class SistemaNavegacao:
    """
    Sistema de navegação GPS usando grafos ponderados.
    Simula um sistema real de roteamento com diferentes critérios.
    """
    
    def __init__(self):
        self.mapa = GrafoPonderado(direcionado=True)
        self.coordenadas = {}  # {local: (lat, lon)}
        self.tipos_via = {}    # {(origem, destino): tipo}
    
    def adicionar_local(self, nome: str, latitude: float, longitude: float) -> None:
        """Adiciona um local ao mapa."""
        self.mapa.adicionar_vertice(nome)
        self.coordenadas[nome] = (latitude, longitude)
    
    def adicionar_via(self, origem: str, destino: str, distancia: float, 
                     tempo: float, tipo: str = "rua") -> None:
        """
        Adiciona uma via entre dois locais.
        
        Args:
            origem: Local de origem
            destino: Local de destino
            distancia: Distância em km
            tempo: Tempo em minutos
            tipo: Tipo da via (rua, avenida, rodovia)
        """
        # Usar distância como peso padrão
        self.mapa.adicionar_aresta(origem, destino, distancia)
        self.tipos_via[(origem, destino)] = tipo
    
    def rota_mais_curta(self, origem: str, destino: str) -> Dict:
        """Encontra a rota mais curta em distância."""
        resultado = AlgoritmoDijkstra.caminho_mais_curto(self.mapa, origem, destino)
        
        if not resultado['caminho']:
            return {'erro': 'Rota não encontrada'}
        
        return {
            'caminho': resultado['caminho'],
            'distancia_total': resultado['distancias'][destino],
            'pontos_interesse': self._obter_pontos_interesse(resultado['caminho'])
        }
    
    def _obter_pontos_interesse(self, caminho: List[str]) -> List[Dict]:
        """Obtém informações detalhadas dos pontos no caminho."""
        pontos = []
        
        for i, local in enumerate(caminho):
            ponto = {
                'local': local,
                'coordenadas': self.coordenadas.get(local, (0, 0)),
                'ordem': i + 1
            }
            
            if i < len(caminho) - 1:
                proximo = caminho[i + 1]
                tipo_via = self.tipos_via.get((local, proximo), "desconhecido")
                ponto['proxima_via'] = f"{tipo_via} para {proximo}"
            
            pontos.append(ponto)
        
        return pontos
    
    def estatisticas_mapa(self) -> Dict:
        """Retorna estatísticas do mapa."""
        return {
            'total_locais': len(self.mapa.vertices),
            'total_vias': self.mapa.num_arestas,
            'densidade': self.mapa.densidade(),
            'tipos_via': dict(Counter(self.tipos_via.values()))
        }


class AnalisadorRedeSocial:
    """
    Analisador de redes sociais usando métricas de grafos.
    Calcula centralidade, comunidades e influência.
    """
    
    def __init__(self):
        self.rede = GrafoPonderado(direcionado=False)
        self.usuarios = {}  # {id: {nome, idade, interesses}}
        self.interacoes = defaultdict(int)  # {(user1, user2): peso}
    
    def adicionar_usuario(self, user_id: str, nome: str, idade: int, 
                         interesses: List[str]) -> None:
        """Adiciona um usuário à rede social."""
        self.rede.adicionar_vertice(user_id)
        self.usuarios[user_id] = {
            'nome': nome,
            'idade': idade,
            'interesses': set(interesses)
        }
    
    def adicionar_amizade(self, user1: str, user2: str, peso: float = 1.0) -> None:
        """Adiciona uma conexão de amizade entre usuários."""
        self.rede.adicionar_aresta(user1, user2, peso)
        self.interacoes[(user1, user2)] = peso
    
    def centralidade_grau(self) -> Dict[str, float]:
        """Calcula a centralidade de grau para todos os usuários."""
        centralidades = {}
        n = len(self.rede.vertices)
        
        for usuario in self.rede.vertices:
            grau = len(self.rede.obter_vizinhos(usuario))
            # Normalizar pelo número máximo possível de conexões
            centralidades[usuario] = grau / (n - 1) if n > 1 else 0
        
        return centralidades
    
    def centralidade_proximidade(self) -> Dict[str, float]:
        """Calcula a centralidade de proximidade usando Dijkstra."""
        centralidades = {}
        
        for usuario in self.rede.vertices:
            resultado = AlgoritmoDijkstra.caminho_mais_curto(self.rede, usuario)
            distancias = resultado['distancias']
            
            # Somar distâncias para todos os outros vértices alcançáveis
            soma_distancias = sum(d for d in distancias.values() 
                                if d != float('inf') and d > 0)
            
            if soma_distancias > 0:
                centralidades[usuario] = (len(self.rede.vertices) - 1) / soma_distancias
            else:
                centralidades[usuario] = 0
        
        return centralidades
    
    def detectar_comunidades_simples(self) -> List[Set[str]]:
        """
        Detecção simples de comunidades usando componentes conectados.
        Para algoritmos mais sofisticados, seria necessário implementar
        Louvain, Girvan-Newman, etc.
        """
        visitados = set()
        comunidades = []
        
        def dfs_comunidade(usuario: str, comunidade_atual: Set[str]) -> None:
            if usuario in visitados:
                return
            
            visitados.add(usuario)
            comunidade_atual.add(usuario)
            
            for vizinho, _ in self.rede.obter_vizinhos(usuario):
                if vizinho not in visitados:
                    dfs_comunidade(vizinho, comunidade_atual)
        
        for usuario in self.rede.vertices:
            if usuario not in visitados:
                comunidade = set()
                dfs_comunidade(usuario, comunidade)
                if comunidade:
                    comunidades.append(comunidade)
        
        return comunidades
    
    def usuarios_influentes(self, top_n: int = 5) -> List[Tuple[str, Dict]]:
        """Identifica os usuários mais influentes baseado em múltiplas métricas."""
        cent_grau = self.centralidade_grau()
        cent_proximidade = self.centralidade_proximidade()
        
        scores = {}
        for usuario in self.rede.vertices:
            # Combinar diferentes métricas de centralidade
            score = (cent_grau[usuario] * 0.6 + cent_proximidade[usuario] * 0.4)
            scores[usuario] = {
                'score_influencia': score,
                'centralidade_grau': cent_grau[usuario],
                'centralidade_proximidade': cent_proximidade[usuario],
                'info_usuario': self.usuarios[usuario]
            }
        
        # Ordenar por score de influência
        ranking = sorted(scores.items(), key=lambda x: x[1]['score_influencia'], 
                        reverse=True)
        
        return ranking[:top_n]
    
    def relatorio_rede(self) -> Dict:
        """Gera um relatório completo da rede social."""
        comunidades = self.detectar_comunidades_simples()
        influentes = self.usuarios_influentes()
        
        return {
            'estatisticas_gerais': {
                'total_usuarios': len(self.rede.vertices),
                'total_conexoes': self.rede.num_arestas,
                'densidade_rede': self.rede.densidade(),
                'numero_comunidades': len(comunidades)
            },
            'comunidades': [list(com) for com in comunidades],
            'usuarios_influentes': influentes,
            'distribuicao_idades': self._distribuicao_idades(),
            'interesses_populares': self._interesses_populares()
        }
    
    def _distribuicao_idades(self) -> Dict[str, int]:
        """Calcula distribuição de idades na rede."""
        faixas = {'18-25': 0, '26-35': 0, '36-45': 0, '46+': 0}
        
        for info in self.usuarios.values():
            idade = info['idade']
            if idade <= 25:
                faixas['18-25'] += 1
            elif idade <= 35:
                faixas['26-35'] += 1
            elif idade <= 45:
                faixas['36-45'] += 1
            else:
                faixas['46+'] += 1
        
        return faixas
    
    def _interesses_populares(self) -> List[Tuple[str, int]]:
        """Identifica os interesses mais populares."""
        contador_interesses = defaultdict(int)
        
        for info in self.usuarios.values():
            for interesse in info['interesses']:
                contador_interesses[interesse] += 1
        
        return sorted(contador_interesses.items(), key=lambda x: x[1], reverse=True)


# Importar Counter para estatísticas
from collections import Counter


def demonstracao_dijkstra():
    """Demonstra o algoritmo de Dijkstra."""
    print("=== DEMONSTRAÇÃO: ALGORITMO DE DIJKSTRA ===")
    
    # Criar grafo de exemplo (rede de cidades)
    grafo = GrafoPonderado(direcionado=False)
    
    cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", 
               "Brasília", "Salvador", "Recife"]
    
    for cidade in cidades:
        grafo.adicionar_vertice(cidade)
    
    # Adicionar conexões com distâncias aproximadas (em km)
    conexoes = [
        ("São Paulo", "Rio de Janeiro", 430),
        ("São Paulo", "Belo Horizonte", 580),
        ("São Paulo", "Brasília", 1150),
        ("Rio de Janeiro", "Belo Horizonte", 440),
        ("Rio de Janeiro", "Salvador", 1200),
        ("Belo Horizonte", "Brasília", 740),
        ("Brasília", "Salvador", 1450),
        ("Salvador", "Recife", 800)
    ]
    
    for origem, destino, distancia in conexoes:
        grafo.adicionar_aresta(origem, destino, distancia)
    
    # Encontrar caminho mais curto
    origem = "São Paulo"
    destino = "Recife"
    
    print(f"Calculando rota mais curta de {origem} para {destino}...")
    
    resultado = AlgoritmoDijkstra.caminho_mais_curto(grafo, origem, destino)
    
    if resultado['caminho']:
        print(f"Caminho: {' → '.join(resultado['caminho'])}")
        print(f"Distância total: {resultado['distancias'][destino]:.0f} km")
    else:
        print("Nenhum caminho encontrado!")
    
    print()


def demonstracao_mst():
    """Demonstra algoritmos de MST (Kruskal e Prim)."""
    print("=== DEMONSTRAÇÃO: ÁRVORE GERADORA MÍNIMA ===")
    
    # Criar grafo de exemplo (rede de computadores)
    grafo = GrafoPonderado(direcionado=False)
    
    nos = ["A", "B", "C", "D", "E", "F"]
    for no in nos:
        grafo.adicionar_vertice(no)
    
    # Adicionar conexões com custos
    conexoes = [
        ("A", "B", 4), ("A", "C", 2), ("B", "C", 1),
        ("B", "D", 5), ("C", "D", 8), ("C", "E", 10),
        ("D", "E", 2), ("D", "F", 6), ("E", "F", 3)
    ]
    
    for origem, destino, custo in conexoes:
        grafo.adicionar_aresta(origem, destino, custo)
    
    print("Grafo original:")
    print(f"Vértices: {sorted(grafo.vertices)}")
    print(f"Arestas: {conexoes}")
    print(f"Custo total: {sum(custo for _, _, custo in conexoes)}")
    print()
    
    # Algoritmo de Kruskal
    print("Algoritmo de Kruskal:")
    mst_kruskal, peso_kruskal = ArvoreGeradoraMinima.kruskal(grafo)
    print(f"MST: {mst_kruskal}")
    print(f"Peso total: {peso_kruskal}")
    print()
    
    # Algoritmo de Prim
    print("Algoritmo de Prim:")
    mst_prim, peso_prim = ArvoreGeradoraMinima.prim(grafo, "A")
    print(f"MST: {mst_prim}")
    print(f"Peso total: {peso_prim}")
    print()


def demonstracao_navegacao():
    """Demonstra sistema de navegação GPS."""
    print("=== DEMONSTRAÇÃO: SISTEMA DE NAVEGAÇÃO ===")
    
    gps = SistemaNavegacao()
    
    # Adicionar locais
    locais = [
        ("Casa", -23.5505, -46.6333),
        ("Trabalho", -23.5475, -46.6361),
        ("Shopping", -23.5489, -46.6388),
        ("Hospital", -23.5520, -46.6300),
        ("Escola", -23.5460, -46.6420)
    ]
    
    for nome, lat, lon in locais:
        gps.adicionar_local(nome, lat, lon)
    
    # Adicionar vias
    vias = [
        ("Casa", "Trabalho", 2.5, 8, "avenida"),
        ("Casa", "Hospital", 1.8, 6, "rua"),
        ("Trabalho", "Shopping", 1.2, 4, "rua"),
        ("Shopping", "Escola", 3.0, 10, "avenida"),
        ("Hospital", "Escola", 2.8, 9, "rua"),
        ("Casa", "Shopping", 3.5, 12, "rodovia")
    ]
    
    for origem, destino, dist, tempo, tipo in vias:
        gps.adicionar_via(origem, destino, dist, tempo, tipo)
    
    # Calcular rota
    origem = "Casa"
    destino = "Escola"
    
    print(f"Calculando rota de {origem} para {destino}...")
    rota = gps.rota_mais_curta(origem, destino)
    
    if 'erro' not in rota:
        print(f"Rota encontrada: {' → '.join(rota['caminho'])}")
        print(f"Distância total: {rota['distancia_total']:.1f} km")
        print("\nPontos de interesse:")
        for ponto in rota['pontos_interesse']:
            print(f"  {ponto['ordem']}. {ponto['local']} {ponto['coordenadas']}")
            if 'proxima_via' in ponto:
                print(f"     → {ponto['proxima_via']}")
    else:
        print(rota['erro'])
    
    print(f"\nEstatísticas do mapa:")
    stats = gps.estatisticas_mapa()
    for chave, valor in stats.items():
        print(f"  {chave}: {valor}")
    
    print()


def demonstracao_rede_social():
    """Demonstra análise de rede social."""
    print("=== DEMONSTRAÇÃO: ANÁLISE DE REDE SOCIAL ===")
    
    rede = AnalisadorRedeSocial()
    
    # Adicionar usuários
    usuarios = [
        ("alice", "Alice Silva", 28, ["tecnologia", "música", "viagem"]),
        ("bob", "Bob Santos", 32, ["esportes", "tecnologia", "culinária"]),
        ("carol", "Carol Lima", 25, ["arte", "música", "fotografia"]),
        ("david", "David Costa", 30, ["esportes", "viagem", "leitura"]),
        ("eva", "Eva Oliveira", 27, ["tecnologia", "arte", "cinema"]),
        ("frank", "Frank Pereira", 35, ["culinária", "viagem", "música"])
    ]
    
    for user_id, nome, idade, interesses in usuarios:
        rede.adicionar_usuario(user_id, nome, idade, interesses)
    
    # Adicionar amizades (com pesos baseados em interações)
    amizades = [
        ("alice", "bob", 0.8),
        ("alice", "carol", 0.9),
        ("alice", "eva", 0.7),
        ("bob", "david", 0.6),
        ("carol", "eva", 0.8),
        ("david", "frank", 0.5),
        ("eva", "frank", 0.4)
    ]
    
    for user1, user2, peso in amizades:
        rede.adicionar_amizade(user1, user2, peso)
    
    # Gerar relatório
    relatorio = rede.relatorio_rede()
    
    print("Estatísticas Gerais:")
    for chave, valor in relatorio['estatisticas_gerais'].items():
        print(f"  {chave}: {valor}")
    
    print(f"\nUsuários Mais Influentes:")
    for i, (user_id, dados) in enumerate(relatorio['usuarios_influentes'], 1):
        info = dados['info_usuario']
        print(f"  {i}. {info['nome']} (Score: {dados['score_influencia']:.3f})")
        print(f"     Centralidade de Grau: {dados['centralidade_grau']:.3f}")
        print(f"     Centralidade de Proximidade: {dados['centralidade_proximidade']:.3f}")
    
    print(f"\nComunidades Detectadas:")
    for i, comunidade in enumerate(relatorio['comunidades'], 1):
        nomes = [rede.usuarios[user_id]['nome'] for user_id in comunidade]
        print(f"  Comunidade {i}: {', '.join(nomes)}")
    
    print(f"\nInteresses Mais Populares:")
    for interesse, count in relatorio['interesses_populares'][:5]:
        print(f"  {interesse}: {count} usuários")
    
    print()


def benchmark_algoritmos():
    """Compara performance dos diferentes algoritmos."""
    print("=== BENCHMARK: COMPARAÇÃO DE ALGORITMOS ===")
    
    # Criar grafo aleatório para teste
    def criar_grafo_aleatorio(num_vertices: int, densidade: float) -> GrafoPonderado:
        grafo = GrafoPonderado(direcionado=False)
        vertices = [f"V{i}" for i in range(num_vertices)]
        
        for v in vertices:
            grafo.adicionar_vertice(v)
        
        num_arestas = int(densidade * num_vertices * (num_vertices - 1) / 2)
        arestas_adicionadas = 0
        
        while arestas_adicionadas < num_arestas:
            v1, v2 = random.sample(vertices, 2)
            peso = random.uniform(1, 100)
            
            # Verificar se aresta já existe
            existe = any(viz == v2 for viz, _ in grafo.obter_vizinhos(v1))
            if not existe:
                grafo.adicionar_aresta(v1, v2, peso)
                arestas_adicionadas += 1
        
        return grafo
    
    tamanhos = [10, 20, 50]
    densidade = 0.3
    
    print(f"Testando com densidade {densidade}")
    print("Tamanho | Dijkstra | Kruskal | Prim")
    print("-" * 40)
    
    for n in tamanhos:
        grafo = criar_grafo_aleatorio(n, densidade)
        vertices = list(grafo.vertices)
        
        # Benchmark Dijkstra
        inicio = time.time()
        AlgoritmoDijkstra.caminho_mais_curto(grafo, vertices[0])
        tempo_dijkstra = time.time() - inicio
        
        # Benchmark Kruskal
        inicio = time.time()
        ArvoreGeradoraMinima.kruskal(grafo)
        tempo_kruskal = time.time() - inicio
        
        # Benchmark Prim
        inicio = time.time()
        ArvoreGeradoraMinima.prim(grafo, vertices[0])
        tempo_prim = time.time() - inicio
        
        print(f"{n:7d} | {tempo_dijkstra:8.4f} | {tempo_kruskal:7.4f} | {tempo_prim:4.4f}")
    
    print()


def main():
    """Função principal com demonstrações."""
    print("MÓDULO 05 - APLICAÇÕES PRÁTICAS DE GRAFOS")
    print("=" * 50)
    print()
    
    demonstracao_dijkstra()
    demonstracao_mst()
    demonstracao_navegacao()
    demonstracao_rede_social()
    benchmark_algoritmos()
    
    print("=== CONCLUSÃO DO MÓDULO ===")
    print("""
    PRINCIPAIS APRENDIZADOS:
    
    1. ALGORITMOS CLÁSSICOS:
       • Dijkstra para caminhos mais curtos (O((V+E) log V))
       • Kruskal e Prim para MST (O(E log E) e O((V+E) log V))
       • Floyd-Warshall para todos os pares (O(V³))
    
    2. APLICAÇÕES PRÁTICAS:
       • Sistemas de navegação GPS
       • Análise de redes sociais
       • Otimização de redes de computadores
       • Detecção de comunidades
    
    3. ESTRUTURAS AUXILIARES:
       • Union-Find para Kruskal
       • Heap binário para Dijkstra e Prim
       • Matrizes de adjacência para Floyd-Warshall
    
    4. MÉTRICAS DE CENTRALIDADE:
       • Centralidade de grau (conexões diretas)
       • Centralidade de proximidade (distâncias médias)
       • Identificação de usuários influentes
    
    5. OTIMIZAÇÕES IMPORTANTES:
       • Compressão de caminho em Union-Find
       • União por rank para eficiência
       • Parada antecipada em Dijkstra
       • Uso de heaps para priorização
    
    Os algoritmos de grafos são fundamentais para resolver problemas
    complexos do mundo real, desde navegação até análise de redes sociais.
    A escolha do algoritmo correto depende das características específicas
    do problema: tamanho do grafo, densidade, se é direcionado, etc.
    
    PRÓXIMO MÓDULO: Algoritmos Avançados
    - Programação Dinâmica
    - Algoritmos Gulosos  
    - Backtracking
    - Divide e Conquista
    """)


if __name__ == "__main__":
    main()