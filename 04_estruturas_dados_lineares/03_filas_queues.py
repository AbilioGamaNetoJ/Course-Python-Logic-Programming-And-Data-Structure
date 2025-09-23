"""
Módulo: Filas (Queues)
Tópico: Estrutura de Dados FIFO - First In, First Out
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário

Objetivos de Aprendizado:
- Compreender o conceito FIFO (First In, First Out)
- Implementar fila usando array circular
- Implementar fila usando lista ligada
- Analisar complexidade das operações
- Implementar fila de prioridade
- Aplicar filas em problemas práticos
- Implementar fila thread-safe
- Comparar diferentes implementações

Conceitos Abordados:
- Princípio FIFO
- Operações fundamentais (enqueue, dequeue, front, isEmpty)
- Array circular vs lista ligada
- Fila de prioridade (heap)
- Fila dupla (deque)
- Thread safety
- Aplicações (BFS, scheduling, buffering)
- Análise de complexidade

Pré-requisitos:
- Arrays e listas dinâmicas
- Conceitos de pilhas
- Noções de heap/árvore binária
- Compreensão de POO

Complexidade:
- Enqueue: O(1)
- Dequeue: O(1)
- Front/Rear: O(1)
- isEmpty: O(1)
- Espaço: O(n)
"""

import threading
import time
import random
import heapq
from typing import Any, Optional, List, Generic, TypeVar, Tuple
from collections import deque
from dataclasses import dataclass, field
import sys

T = TypeVar('T')

def conceitos_filas():
    """
    Explica conceitos fundamentais de filas.
    """
    print("=== CONCEITOS FUNDAMENTAIS DE FILAS ===")
    print()
    
    print("1. PRINCÍPIO FIFO (First In, First Out):")
    print()
    print("   Visualização de uma fila:")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │  REAR                                           FRONT   │")
    print("   │   ↓                                               ↓     │")
    print("   │  [5] [4] [3] [2] [1] ← Primeiro elemento inserido       │")
    print("   │   ↑                                               ↑     │")
    print("   │ Enqueue                                        Dequeue   │")
    print("   │ (inserir)                                      (remover) │")
    print("   └─────────────────────────────────────────────────────────┘")
    print()
    
    print("2. OPERAÇÕES FUNDAMENTAIS:")
    print("   ┌─────────────────┬─────────────────────────────────────────┬─────────────┐")
    print("   │    OPERAÇÃO     │               DESCRIÇÃO                 │ COMPLEXIDADE│")
    print("   ├─────────────────┼─────────────────────────────────────────┼─────────────┤")
    print("   │ enqueue(item)   │ Adiciona item no final da fila          │    O(1)     │")
    print("   │ dequeue()       │ Remove e retorna item do início         │    O(1)     │")
    print("   │ front()         │ Retorna item do início sem remover      │    O(1)     │")
    print("   │ rear()          │ Retorna item do final sem remover       │    O(1)     │")
    print("   │ isEmpty()       │ Verifica se a fila está vazia           │    O(1)     │")
    print("   │ size()          │ Retorna número de elementos             │    O(1)     │")
    print("   └─────────────────┴─────────────────────────────────────────┴─────────────┘")
    print()
    
    print("3. DEMONSTRAÇÃO VISUAL DAS OPERAÇÕES:")
    
    def demonstrar_operacoes():
        """Demonstra operações básicas visualmente"""
        
        fila_visual = []
        
        def mostrar_fila(operacao=""):
            """Mostra estado atual da fila"""
            print(f"   {operacao}")
            if not fila_visual:
                print("   ┌─────────┐")
                print("   │  VAZIA  │")
                print("   └─────────┘")
            else:
                print("   ┌─────────┬─────────┬─────────┬─────────┬─────────┐")
                print("   │ FRONT   │         │         │         │  REAR   │")
                print("   ├─────────┼─────────┼─────────┼─────────┼─────────┤")
                
                # Mostrar elementos
                linha = "   │"
                for i in range(5):  # Mostrar até 5 elementos
                    if i < len(fila_visual):
                        linha += f"   {fila_visual[i]:2}    │"
                    else:
                        linha += "         │"
                print(linha)
                
                print("   └─────────┴─────────┴─────────┴─────────┴─────────┘")
            print()
        
        # Estado inicial
        mostrar_fila("Estado inicial:")
        
        # Enqueue operations
        for valor in [10, 20, 30]:
            fila_visual.append(valor)
            mostrar_fila(f"enqueue({valor}):")
        
        # Dequeue operations
        for _ in range(2):
            if fila_visual:
                valor = fila_visual.pop(0)
                mostrar_fila(f"dequeue() → {valor}:")
        
        # Front operation
        if fila_visual:
            mostrar_fila(f"front() → {fila_visual[0]} (sem remover):")
    
    demonstrar_operacoes()
    
    print("4. PROBLEMA DO ARRAY SIMPLES:")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │ Array simples com dequeue ineficiente:                 │")
    print("   │                                                         │")
    print("   │ Inicial: [A][B][C][D][ ][ ][ ]                          │")
    print("   │          ↑front                                         │")
    print("   │                                                         │")
    print("   │ Após dequeue(): [ ][B][C][D][ ][ ][ ]                   │")
    print("   │                 ↑front (desperdiça espaço)              │")
    print("   │                                                         │")
    print("   │ Solução: Array Circular!                                │")
    print("   └─────────────────────────────────────────────────────────┘")
    print()

class FilaArrayCircular(Generic[T]):
    """
    Implementação de fila usando array circular.
    Evita desperdício de espaço e operações custosas.
    """
    
    def __init__(self, capacidade: int = 10):
        """
        Inicializa fila com capacidade fixa.
        
        Args:
            capacidade: Capacidade máxima da fila
        """
        self._dados: List[Optional[T]] = [None] * capacidade
        self._capacidade = capacidade
        self._front = 0  # Índice do primeiro elemento
        self._rear = 0   # Índice após o último elemento
        self._tamanho = 0
        
        # Estatísticas
        self._total_enqueues = 0
        self._total_dequeues = 0
    
    def enqueue(self, item: T) -> None:
        """
        Adiciona item no final da fila - O(1).
        
        Args:
            item: Item a ser adicionado
            
        Raises:
            OverflowError: Se a fila estiver cheia
        """
        if self.is_full():
            raise OverflowError("Fila cheia")
        
        self._dados[self._rear] = item
        self._rear = (self._rear + 1) % self._capacidade
        self._tamanho += 1
        self._total_enqueues += 1
    
    def dequeue(self) -> T:
        """
        Remove e retorna item do início da fila - O(1).
        
        Returns:
            Item removido do início
            
        Raises:
            IndexError: Se a fila estiver vazia
        """
        if self.is_empty():
            raise IndexError("dequeue de fila vazia")
        
        item = self._dados[self._front]
        self._dados[self._front] = None  # Limpar referência
        self._front = (self._front + 1) % self._capacidade
        self._tamanho -= 1
        self._total_dequeues += 1
        
        return item
    
    def front(self) -> T:
        """
        Retorna item do início sem remover - O(1).
        
        Returns:
            Item no início da fila
            
        Raises:
            IndexError: Se a fila estiver vazia
        """
        if self.is_empty():
            raise IndexError("front de fila vazia")
        
        return self._dados[self._front]
    
    def rear(self) -> T:
        """
        Retorna item do final sem remover - O(1).
        
        Returns:
            Item no final da fila
            
        Raises:
            IndexError: Se a fila estiver vazia
        """
        if self.is_empty():
            raise IndexError("rear de fila vazia")
        
        rear_index = (self._rear - 1) % self._capacidade
        return self._dados[rear_index]
    
    def is_empty(self) -> bool:
        """Verifica se a fila está vazia - O(1)"""
        return self._tamanho == 0
    
    def is_full(self) -> bool:
        """Verifica se a fila está cheia - O(1)"""
        return self._tamanho == self._capacidade
    
    def size(self) -> int:
        """Retorna número de elementos - O(1)"""
        return self._tamanho
    
    def clear(self) -> None:
        """Remove todos os elementos - O(1)"""
        for i in range(self._capacidade):
            self._dados[i] = None
        self._front = 0
        self._rear = 0
        self._tamanho = 0
    
    def get_stats(self) -> dict:
        """Retorna estatísticas da fila"""
        return {
            'tamanho': self.size(),
            'capacidade': self._capacidade,
            'utilizacao': (self.size() / self._capacidade) * 100,
            'total_enqueues': self._total_enqueues,
            'total_dequeues': self._total_dequeues,
            'front_index': self._front,
            'rear_index': self._rear
        }
    
    def visualizar_array(self) -> str:
        """Visualiza o estado interno do array circular"""
        visual = []
        for i in range(self._capacidade):
            if self._dados[i] is not None:
                marcador = ""
                if i == self._front and i == (self._rear - 1) % self._capacidade:
                    marcador = "F&R"
                elif i == self._front:
                    marcador = "F"
                elif i == (self._rear - 1) % self._capacidade:
                    marcador = "R"
                
                visual.append(f"[{self._dados[i]}{marcador}]")
            else:
                visual.append("[ ]")
        
        return " ".join(visual)
    
    def __str__(self) -> str:
        """Representação string da fila"""
        if self.is_empty():
            return "FilaArrayCircular(vazia)"
        
        elementos = []
        atual = self._front
        for _ in range(self._tamanho):
            elementos.append(str(self._dados[atual]))
            atual = (atual + 1) % self._capacidade
        
        return f"FilaArrayCircular([{' <- '.join(elementos)}] <- REAR)"
    
    def __len__(self) -> int:
        """Suporte ao len()"""
        return self.size()

class NoFila(Generic[T]):
    """Nó para lista ligada da fila"""
    
    def __init__(self, dado: T, proximo: Optional['NoFila[T]'] = None):
        self.dado = dado
        self.proximo = proximo

class FilaListaLigada(Generic[T]):
    """
    Implementação de fila usando lista ligada.
    Sem limitação de tamanho, mas com overhead de ponteiros.
    """
    
    def __init__(self):
        """Inicializa fila vazia"""
        self._front: Optional[NoFila[T]] = None
        self._rear: Optional[NoFila[T]] = None
        self._tamanho = 0
        
        # Estatísticas
        self._total_enqueues = 0
        self._total_dequeues = 0
    
    def enqueue(self, item: T) -> None:
        """
        Adiciona item no final da fila - O(1).
        
        Args:
            item: Item a ser adicionado
        """
        novo_no = NoFila(item)
        
        if self.is_empty():
            self._front = self._rear = novo_no
        else:
            self._rear.proximo = novo_no
            self._rear = novo_no
        
        self._tamanho += 1
        self._total_enqueues += 1
    
    def dequeue(self) -> T:
        """
        Remove e retorna item do início da fila - O(1).
        
        Returns:
            Item removido do início
            
        Raises:
            IndexError: Se a fila estiver vazia
        """
        if self.is_empty():
            raise IndexError("dequeue de fila vazia")
        
        item = self._front.dado
        self._front = self._front.proximo
        
        if self._front is None:  # Fila ficou vazia
            self._rear = None
        
        self._tamanho -= 1
        self._total_dequeues += 1
        
        return item
    
    def front(self) -> T:
        """
        Retorna item do início sem remover - O(1).
        
        Returns:
            Item no início da fila
            
        Raises:
            IndexError: Se a fila estiver vazia
        """
        if self.is_empty():
            raise IndexError("front de fila vazia")
        
        return self._front.dado
    
    def rear(self) -> T:
        """
        Retorna item do final sem remover - O(1).
        
        Returns:
            Item no final da fila
            
        Raises:
            IndexError: Se a fila estiver vazia
        """
        if self.is_empty():
            raise IndexError("rear de fila vazia")
        
        return self._rear.dado
    
    def is_empty(self) -> bool:
        """Verifica se a fila está vazia - O(1)"""
        return self._front is None
    
    def size(self) -> int:
        """Retorna número de elementos - O(1)"""
        return self._tamanho
    
    def clear(self) -> None:
        """Remove todos os elementos - O(1)"""
        self._front = None
        self._rear = None
        self._tamanho = 0
    
    def get_stats(self) -> dict:
        """Retorna estatísticas da fila"""
        return {
            'tamanho': self.size(),
            'total_enqueues': self._total_enqueues,
            'total_dequeues': self._total_dequeues,
            'memoria_por_no': sys.getsizeof(NoFila(None)) if self._front else 0
        }
    
    def __str__(self) -> str:
        """Representação string da fila"""
        if self.is_empty():
            return "FilaListaLigada(vazia)"
        
        elementos = []
        atual = self._front
        while atual:
            elementos.append(str(atual.dado))
            atual = atual.proximo
        
        return f"FilaListaLigada([{' <- '.join(elementos)}] <- REAR)"
    
    def __len__(self) -> int:
        """Suporte ao len()"""
        return self.size()

@dataclass
class ItemPrioridade(Generic[T]):
    """Item com prioridade para fila de prioridade"""
    prioridade: int
    item: T
    ordem_insercao: int = field(default=0)
    
    def __lt__(self, other):
        # Menor prioridade = maior precedência
        # Em caso de empate, usar ordem de inserção
        if self.prioridade == other.prioridade:
            return self.ordem_insercao < other.ordem_insercao
        return self.prioridade < other.prioridade

class FilaPrioridade(Generic[T]):
    """
    Fila de prioridade usando heap binário.
    Elementos com menor valor de prioridade saem primeiro.
    """
    
    def __init__(self):
        """Inicializa fila de prioridade vazia"""
        self._heap: List[ItemPrioridade[T]] = []
        self._contador = 0  # Para manter ordem de inserção
        
        # Estatísticas
        self._total_enqueues = 0
        self._total_dequeues = 0
    
    def enqueue(self, item: T, prioridade: int) -> None:
        """
        Adiciona item com prioridade - O(log n).
        
        Args:
            item: Item a ser adicionado
            prioridade: Prioridade do item (menor = maior precedência)
        """
        item_prioridade = ItemPrioridade(prioridade, item, self._contador)
        heapq.heappush(self._heap, item_prioridade)
        
        self._contador += 1
        self._total_enqueues += 1
    
    def dequeue(self) -> T:
        """
        Remove e retorna item de maior prioridade - O(log n).
        
        Returns:
            Item de maior prioridade
            
        Raises:
            IndexError: Se a fila estiver vazia
        """
        if self.is_empty():
            raise IndexError("dequeue de fila vazia")
        
        item_prioridade = heapq.heappop(self._heap)
        self._total_dequeues += 1
        
        return item_prioridade.item
    
    def front(self) -> Tuple[T, int]:
        """
        Retorna item de maior prioridade sem remover - O(1).
        
        Returns:
            Tupla (item, prioridade)
            
        Raises:
            IndexError: Se a fila estiver vazia
        """
        if self.is_empty():
            raise IndexError("front de fila vazia")
        
        item_prioridade = self._heap[0]
        return item_prioridade.item, item_prioridade.prioridade
    
    def is_empty(self) -> bool:
        """Verifica se a fila está vazia - O(1)"""
        return len(self._heap) == 0
    
    def size(self) -> int:
        """Retorna número de elementos - O(1)"""
        return len(self._heap)
    
    def clear(self) -> None:
        """Remove todos os elementos - O(1)"""
        self._heap.clear()
        self._contador = 0
    
    def get_stats(self) -> dict:
        """Retorna estatísticas da fila"""
        return {
            'tamanho': self.size(),
            'total_enqueues': self._total_enqueues,
            'total_dequeues': self._total_dequeues,
            'contador_insercao': self._contador
        }
    
    def __str__(self) -> str:
        """Representação string da fila"""
        if self.is_empty():
            return "FilaPrioridade(vazia)"
        
        # Mostrar elementos ordenados por prioridade
        elementos = [(item.item, item.prioridade) for item in sorted(self._heap)]
        elementos_str = [f"{item}(p:{prio})" for item, prio in elementos]
        
        return f"FilaPrioridade([{', '.join(elementos_str)}])"
    
    def __len__(self) -> int:
        """Suporte ao len()"""
        return self.size()

def aplicacoes_praticas():
    """
    Demonstra aplicações práticas de filas.
    """
    print("=== APLICAÇÕES PRÁTICAS DE FILAS ===")
    print()
    
    print("1. SIMULAÇÃO DE SISTEMA DE ATENDIMENTO:")
    
    def simular_atendimento():
        """Simula sistema de atendimento com fila"""
        
        @dataclass
        class Cliente:
            id: int
            tempo_chegada: float
            tempo_servico: float
            
            def __str__(self):
                return f"Cliente{self.id}"
        
        # Configuração da simulação
        tempo_simulacao = 60  # 60 segundos
        tempo_medio_chegada = 5  # Cliente a cada 5 segundos em média
        tempo_medio_servico = 8  # 8 segundos de atendimento em média
        
        fila_atendimento = FilaListaLigada[Cliente]()
        clientes_atendidos = []
        
        tempo_atual = 0
        proximo_cliente_id = 1
        tempo_proximo_cliente = random.expovariate(1/tempo_medio_chegada)
        tempo_fim_atendimento = float('inf')
        
        print("   Simulação de sistema de atendimento:")
        print("   ┌─────────┬─────────────────┬─────────────────┬─────────────────┐")
        print("   │  TEMPO  │     EVENTO      │   FILA ATUAL    │   ESTATÍSTICAS  │")
        print("   ├─────────┼─────────────────┼─────────────────┼─────────────────┤")
        
        while tempo_atual < tempo_simulacao:
            # Próximo evento: chegada de cliente ou fim de atendimento
            if tempo_proximo_cliente <= tempo_fim_atendimento:
                # Chegada de cliente
                tempo_atual = tempo_proximo_cliente
                
                cliente = Cliente(
                    id=proximo_cliente_id,
                    tempo_chegada=tempo_atual,
                    tempo_servico=random.expovariate(1/tempo_medio_servico)
                )
                
                fila_atendimento.enqueue(cliente)
                
                # Agendar próximo cliente
                proximo_cliente_id += 1
                tempo_proximo_cliente = tempo_atual + random.expovariate(1/tempo_medio_chegada)
                
                # Se não há atendimento em andamento, iniciar
                if tempo_fim_atendimento == float('inf') and not fila_atendimento.is_empty():
                    cliente_atendimento = fila_atendimento.dequeue()
                    tempo_fim_atendimento = tempo_atual + cliente_atendimento.tempo_servico
                
                fila_str = f"{fila_atendimento.size()} clientes"
                stats_str = f"{len(clientes_atendidos)} atendidos"
                
                print(f"   │ {tempo_atual:5.1f}s │ {cliente} chegou │ {fila_str:15} │ {stats_str:15} │")
            
            else:
                # Fim de atendimento
                tempo_atual = tempo_fim_atendimento
                
                # Iniciar próximo atendimento se houver fila
                if not fila_atendimento.is_empty():
                    cliente_atendimento = fila_atendimento.dequeue()
                    tempo_fim_atendimento = tempo_atual + cliente_atendimento.tempo_servico
                    clientes_atendidos.append(cliente_atendimento)
                else:
                    tempo_fim_atendimento = float('inf')
                
                fila_str = f"{fila_atendimento.size()} clientes"
                stats_str = f"{len(clientes_atendidos)} atendidos"
                
                print(f"   │ {tempo_atual:5.1f}s │ Atendimento fim │ {fila_str:15} │ {stats_str:15} │")
            
            if tempo_atual >= tempo_simulacao:
                break
        
        print("   └─────────┴─────────────────┴─────────────────┴─────────────────┘")
        
        # Estatísticas finais
        if clientes_atendidos:
            tempo_medio_espera = sum(
                (c.tempo_chegada for c in clientes_atendidos), 0
            ) / len(clientes_atendidos)
            
            print(f"\n   📊 Estatísticas finais:")
            print(f"   → Clientes atendidos: {len(clientes_atendidos)}")
            print(f"   → Clientes na fila: {fila_atendimento.size()}")
            print(f"   → Taxa de atendimento: {len(clientes_atendidos)/tempo_simulacao:.2f} clientes/s")
        
        print()
    
    simular_atendimento()
    
    print("2. ALGORITMO BFS (Busca em Largura):")
    
    def bfs_grafo(grafo: dict, inicio: str, objetivo: str) -> Optional[List[str]]:
        """
        Busca em largura usando fila.
        
        Args:
            grafo: Dicionário de adjacências
            inicio: Nó inicial
            objetivo: Nó objetivo
            
        Returns:
            Caminho encontrado ou None
        """
        if inicio == objetivo:
            return [inicio]
        
        fila = FilaListaLigada[str]()
        visitados = set()
        pais = {}
        
        fila.enqueue(inicio)
        visitados.add(inicio)
        
        while not fila.is_empty():
            atual = fila.dequeue()
            
            for vizinho in grafo.get(atual, []):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    pais[vizinho] = atual
                    fila.enqueue(vizinho)
                    
                    if vizinho == objetivo:
                        # Reconstruir caminho
                        caminho = []
                        no = objetivo
                        while no is not None:
                            caminho.append(no)
                            no = pais.get(no)
                        return list(reversed(caminho))
        
        return None
    
    # Exemplo de grafo
    grafo_exemplo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    def visualizar_grafo():
        """Visualiza o grafo exemplo"""
        print("   Grafo exemplo:")
        print("   ┌─────────────────────────────────────┐")
        print("   │        A                            │")
        print("   │       / \\                           │")
        print("   │      B   C                          │")
        print("   │     /|   |\\                         │")
        print("   │    D E   F                          │")
        print("   │      \\   /                          │")
        print("   │       \\ /                           │")
        print("   │        E                            │")
        print("   └─────────────────────────────────────┘")
        print()
    
    visualizar_grafo()
    
    # Testes de BFS
    testes_bfs = [
        ('A', 'F'),
        ('B', 'C'),
        ('D', 'F'),
        ('A', 'A')
    ]
    
    print("   Resultados da busca BFS:")
    print("   ┌─────────────┬─────────────────────────────────────┐")
    print("   │   BUSCA     │              CAMINHO                │")
    print("   ├─────────────┼─────────────────────────────────────┤")
    
    for inicio, fim in testes_bfs:
        caminho = bfs_grafo(grafo_exemplo, inicio, fim)
        caminho_str = " → ".join(caminho) if caminho else "Não encontrado"
        print(f"   │ {inicio} → {fim:8} │ {caminho_str:35} │")
    
    print("   └─────────────┴─────────────────────────────────────┘")
    print()
    
    print("3. SISTEMA DE PRIORIDADES - PRONTO SOCORRO:")
    
    def simular_pronto_socorro():
        """Simula sistema de prioridades de pronto socorro"""
        
        @dataclass
        class Paciente:
            nome: str
            sintomas: str
            prioridade: int  # 1=crítico, 2=urgente, 3=normal
            
            def __str__(self):
                return f"{self.nome} ({self.sintomas})"
        
        # Níveis de prioridade
        CRITICO = 1
        URGENTE = 2
        NORMAL = 3
        
        fila_ps = FilaPrioridade[Paciente]()
        
        # Chegada de pacientes
        pacientes = [
            Paciente("João", "dor no peito", CRITICO),
            Paciente("Maria", "febre alta", URGENTE),
            Paciente("Pedro", "dor de cabeça", NORMAL),
            Paciente("Ana", "fratura exposta", CRITICO),
            Paciente("Carlos", "vômito", URGENTE),
            Paciente("Lucia", "gripe", NORMAL),
            Paciente("Roberto", "infarto", CRITICO),
        ]
        
        print("   Simulação de pronto socorro:")
        print("   ┌─────────────────────────────────────────────────────────────┐")
        print("   │ Prioridades: 1=Crítico, 2=Urgente, 3=Normal                │")
        print("   └─────────────────────────────────────────────────────────────┘")
        print()
        
        # Adicionar pacientes
        print("   Chegada de pacientes:")
        for paciente in pacientes:
            fila_ps.enqueue(paciente, paciente.prioridade)
            prio_str = {1: "CRÍTICO", 2: "URGENTE", 3: "NORMAL"}[paciente.prioridade]
            print(f"   → {paciente} - Prioridade: {prio_str}")
        
        print(f"\n   Fila atual: {fila_ps}")
        print()
        
        # Atendimento por ordem de prioridade
        print("   Ordem de atendimento:")
        print("   ┌─────────────────────────────────────┬─────────────────┐")
        print("   │              PACIENTE               │   PRIORIDADE    │")
        print("   ├─────────────────────────────────────┼─────────────────┤")
        
        ordem = 1
        while not fila_ps.is_empty():
            paciente = fila_ps.dequeue()
            prio_str = {1: "CRÍTICO", 2: "URGENTE", 3: "NORMAL"}[paciente.prioridade]
            print(f"   │ {ordem}. {str(paciente):30} │ {prio_str:15} │")
            ordem += 1
        
        print("   └─────────────────────────────────────┴─────────────────┘")
        print()
    
    simular_pronto_socorro()

def benchmark_implementacoes():
    """
    Compara performance das diferentes implementações.
    """
    print("=== BENCHMARK DAS IMPLEMENTAÇÕES ===")
    print()
    
    def testar_performance_fila(fila_class, nome: str, operacoes: int = 50000):
        """Testa performance de uma implementação de fila"""
        
        if nome == "Array Circular":
            fila = fila_class(operacoes)  # Capacidade suficiente
        else:
            fila = fila_class()
        
        # Teste de enqueue
        start = time.perf_counter()
        for i in range(operacoes):
            if nome == "Fila Prioridade":
                fila.enqueue(i, random.randint(1, 100))
            else:
                fila.enqueue(i)
        tempo_enqueue = time.perf_counter() - start
        
        # Teste de dequeue
        start = time.perf_counter()
        for _ in range(operacoes):
            fila.dequeue()
        tempo_dequeue = time.perf_counter() - start
        
        return tempo_enqueue, tempo_dequeue
    
    operacoes = 50000
    
    print(f"   Performance com {operacoes:,} operações:")
    print("   ┌─────────────────────┬─────────────────┬─────────────────┬─────────────────┐")
    print("   │   IMPLEMENTAÇÃO     │  ENQUEUE (ms)   │  DEQUEUE (ms)   │   TOTAL (ms)    │")
    print("   ├─────────────────────┼─────────────────┼─────────────────┼─────────────────┤")
    
    implementacoes = [
        (FilaArrayCircular, "Array Circular"),
        (FilaListaLigada, "Lista Ligada"),
        (FilaPrioridade, "Fila Prioridade"),
        (lambda: deque(), "deque (Python)")
    ]
    
    for fila_class, nome in implementacoes:
        if nome == "deque (Python)":
            # Teste especial para deque
            fila = deque()
            
            start = time.perf_counter()
            for i in range(operacoes):
                fila.append(i)
            tempo_enqueue = time.perf_counter() - start
            
            start = time.perf_counter()
            for _ in range(operacoes):
                fila.popleft()
            tempo_dequeue = time.perf_counter() - start
        else:
            tempo_enqueue, tempo_dequeue = testar_performance_fila(fila_class, nome, operacoes)
        
        total = tempo_enqueue + tempo_dequeue
        
        print(f"   │ {nome:19} │ {tempo_enqueue*1000:13.2f} ms │ {tempo_dequeue*1000:13.2f} ms │ {total*1000:13.2f} ms │")
    
    print("   └─────────────────────┴─────────────────┴─────────────────┴─────────────────┘")
    print()
    
    print("   Análise de complexidade:")
    print("   ┌─────────────────────┬─────────────────┬─────────────────┬─────────────────┐")
    print("   │   IMPLEMENTAÇÃO     │    ENQUEUE      │    DEQUEUE      │     ESPAÇO      │")
    print("   ├─────────────────────┼─────────────────┼─────────────────┼─────────────────┤")
    print("   │ Array Circular      │      O(1)       │      O(1)       │      O(n)       │")
    print("   │ Lista Ligada        │      O(1)       │      O(1)       │      O(n)       │")
    print("   │ Fila Prioridade     │    O(log n)     │    O(log n)     │      O(n)       │")
    print("   │ deque (Python)      │      O(1)       │      O(1)       │      O(n)       │")
    print("   └─────────────────────┴─────────────────┴─────────────────┴─────────────────┘")
    print()

if __name__ == "__main__":
    print("MÓDULO 4.3 - FILAS (QUEUES)")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceitos_filas()
    print("\n" + "="*50 + "\n")
    
    # Demonstração das implementações
    print("=== DEMONSTRAÇÃO DAS IMPLEMENTAÇÕES ===")
    print()
    
    print("1. FILA COM ARRAY CIRCULAR:")
    fila_array = FilaArrayCircular[int](8)
    
    # Operações básicas
    for i in [10, 20, 30, 40, 50]:
        fila_array.enqueue(i)
        print(f"   enqueue({i}): {fila_array}")
        print(f"   Array interno: {fila_array.visualizar_array()}")
    
    print(f"   front(): {fila_array.front()}")
    print(f"   rear(): {fila_array.rear()}")
    
    for _ in range(3):
        valor = fila_array.dequeue()
        print(f"   dequeue(): {valor} → {fila_array}")
        print(f"   Array interno: {fila_array.visualizar_array()}")
    
    print(f"   Stats: {fila_array.get_stats()}")
    print()
    
    print("2. FILA COM LISTA LIGADA:")
    fila_lista = FilaListaLigada[str]()
    
    for item in ['A', 'B', 'C', 'D']:
        fila_lista.enqueue(item)
        print(f"   enqueue('{item}'): {fila_lista}")
    
    print(f"   front(): '{fila_lista.front()}'")
    print(f"   rear(): '{fila_lista.rear()}'")
    
    for _ in range(2):
        valor = fila_lista.dequeue()
        print(f"   dequeue(): '{valor}' → {fila_lista}")
    
    print(f"   Stats: {fila_lista.get_stats()}")
    print()
    
    print("3. FILA DE PRIORIDADE:")
    fila_prio = FilaPrioridade[str]()
    
    itens_prio = [
        ("Tarefa A", 3),
        ("Tarefa B", 1),
        ("Tarefa C", 2),
        ("Tarefa D", 1),
        ("Tarefa E", 3)
    ]
    
    for item, prio in itens_prio:
        fila_prio.enqueue(item, prio)
        print(f"   enqueue('{item}', {prio}): {fila_prio}")
    
    print(f"   front(): {fila_prio.front()}")
    
    print("   Ordem de saída:")
    while not fila_prio.is_empty():
        item = fila_prio.dequeue()
        print(f"   → {item}")
    
    print()
    
    print("\n" + "="*50 + "\n")
    
    aplicacoes_praticas()
    print("\n" + "="*50 + "\n")
    
    benchmark_implementacoes()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 4.3 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceito FIFO e operações fundamentais")
    print("✅ Implementação com array circular")
    print("✅ Implementação com lista ligada")
    print("✅ Fila de prioridade com heap")
    print("✅ Simulação de sistema de atendimento")
    print("✅ Algoritmo BFS (Busca em Largura)")
    print("✅ Sistema de prioridades médicas")
    print("✅ Análise comparativa de performance")
    print("✅ Trade-offs entre implementações")
    print("\n➡️  Próximo: Módulo 4.4 - Listas Ligadas")