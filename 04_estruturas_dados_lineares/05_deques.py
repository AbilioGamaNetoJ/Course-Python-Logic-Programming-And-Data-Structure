"""
Módulo: Deques (Double-ended Queues)
Tópico: Estruturas de Dados com Acesso Duplo
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário

Objetivos de Aprendizado:
- Compreender conceito de deque
- Implementar deque com array circular
- Implementar deque com lista duplamente ligada
- Analisar complexidade das operações
- Comparar implementações
- Aplicar em problemas práticos
- Usar collections.deque do Python
- Implementar algoritmos com deques

Conceitos Abordados:
- Double-ended queue (deque)
- Operações: append, appendleft, pop, popleft
- Array circular para deque
- Lista duplamente ligada para deque
- Sliding window com deque
- Monotonic deque
- BFS com deque
- Palindrome checking

Pré-requisitos:
- Arrays dinâmicos
- Listas ligadas
- Pilhas e filas
- Conceitos de ponteiros

Complexidade:
- Inserção/remoção nas extremidades: O(1)
- Acesso por índice: O(1) array, O(n) lista ligada
- Busca: O(n)
- Espaço: O(n)
"""

from typing import Any, Optional, Iterator, Generic, TypeVar, List, Deque
from collections import deque as collections_deque
import sys
import time
import random

T = TypeVar('T')

def conceitos_deques():
    """
    Explica conceitos fundamentais de deques.
    """
    print("=== CONCEITOS FUNDAMENTAIS DE DEQUES ===")
    print()
    
    print("1. O QUE É UM DEQUE?")
    print()
    print("   Deque = Double-Ended Queue (Fila de Duas Pontas)")
    print("   ┌─────────────────────────────────────────────────────────────────┐")
    print("   │                                                                 │")
    print("   │  appendleft()  ←──┐                    ┌──→  append()           │")
    print("   │                   │                    │                        │")
    print("   │  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐                   │")
    print("   │  │  A  │  B  │  C  │  D  │  E  │  F  │  G  │                   │")
    print("   │  └─────┴─────┴─────┴─────┴─────┴─────┴─────┘                   │")
    print("   │                   │                    │                        │")
    print("   │  popleft()     ←──┘                    └──→  pop()              │")
    print("   │                                                                 │")
    print("   │  ← FRONT/LEFT                          RIGHT/REAR →            │")
    print("   └─────────────────────────────────────────────────────────────────┘")
    print()
    
    print("2. COMPARAÇÃO COM OUTRAS ESTRUTURAS:")
    print()
    print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │   OPERAÇÃO      │    ARRAY    │    LISTA    │    PILHA    │    DEQUE    │")
    print("   ├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤")
    print("   │ Inserir início  │    O(n)     │    O(1)     │     N/A     │    O(1)     │")
    print("   │ Inserir final   │  O(1) amort │    O(n)     │    O(1)     │    O(1)     │")
    print("   │ Remover início  │    O(n)     │    O(1)     │     N/A     │    O(1)     │")
    print("   │ Remover final   │    O(1)     │    O(n)     │    O(1)     │    O(1)     │")
    print("   │ Acesso índice   │    O(1)     │    O(n)     │     N/A     │  O(1)/O(n)  │")
    print("   │ Busca elemento  │    O(n)     │    O(n)     │    O(n)     │    O(n)     │")
    print("   └─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘")
    print()
    
    print("3. IMPLEMENTAÇÕES POSSÍVEIS:")
    print()
    print("   a) Array Circular:")
    print("   ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐")
    print("   │  -  │  A  │  B  │  C  │  D  │  -  │  -  │  -  │")
    print("   └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘")
    print("     0     1     2     3     4     5     6     7")
    print("           ↑                       ↑")
    print("         front                   rear")
    print()
    
    print("   b) Lista Duplamente Ligada:")
    print("   ┌────┬─────┬────┐    ┌────┬─────┬────┐    ┌────┬─────┬────┐")
    print("   │NULL│  A  │ ●──┼───→│ ●──│  B  │ ●──┼───→│ ●──│  C  │NULL│")
    print("   └────┴─────┴────┘    └────┴─────┴────┘    └────┴─────┴────┘")
    print("   front                                                 rear")
    print()
    
    print("4. CASOS DE USO TÍPICOS:")
    print("   • Sliding window algorithms")
    print("   • BFS (Breadth-First Search)")
    print("   • Undo/Redo com limite")
    print("   • Cache LRU")
    print("   • Palindrome checking")
    print("   • Monotonic queue problems")
    print("   • Job scheduling")
    print()

class DequeArrayCircular(Generic[T]):
    """
    Implementação de deque usando array circular.
    Oferece O(1) para todas as operações nas extremidades.
    """
    
    def __init__(self, capacidade_inicial: int = 8):
        """
        Inicializa deque com capacidade inicial.
        
        Args:
            capacidade_inicial: Capacidade inicial do array
        """
        self._capacidade = capacidade_inicial
        self._array = [None] * self._capacidade
        self._front = 0
        self._rear = 0
        self._tamanho = 0
        
        # Estatísticas
        self._total_appends = 0
        self._total_pops = 0
        self._total_redimensionamentos = 0
    
    def _redimensionar(self, nova_capacidade: int) -> None:
        """
        Redimensiona o array interno.
        
        Args:
            nova_capacidade: Nova capacidade do array
        """
        novo_array = [None] * nova_capacidade
        
        # Copiar elementos na ordem correta
        for i in range(self._tamanho):
            novo_array[i] = self._array[(self._front + i) % self._capacidade]
        
        self._array = novo_array
        self._capacidade = nova_capacidade
        self._front = 0
        self._rear = self._tamanho
        self._total_redimensionamentos += 1
    
    def append(self, item: T) -> None:
        """
        Adiciona item no final (direita) - O(1) amortizado.
        
        Args:
            item: Item a ser adicionado
        """
        if self._tamanho == self._capacidade:
            self._redimensionar(self._capacidade * 2)
        
        self._array[self._rear] = item
        self._rear = (self._rear + 1) % self._capacidade
        self._tamanho += 1
        self._total_appends += 1
    
    def appendleft(self, item: T) -> None:
        """
        Adiciona item no início (esquerda) - O(1) amortizado.
        
        Args:
            item: Item a ser adicionado
        """
        if self._tamanho == self._capacidade:
            self._redimensionar(self._capacidade * 2)
        
        self._front = (self._front - 1) % self._capacidade
        self._array[self._front] = item
        self._tamanho += 1
        self._total_appends += 1
    
    def pop(self) -> T:
        """
        Remove e retorna item do final (direita) - O(1).
        
        Returns:
            Item removido
            
        Raises:
            IndexError: Se deque estiver vazio
        """
        if self._tamanho == 0:
            raise IndexError("pop from empty deque")
        
        self._rear = (self._rear - 1) % self._capacidade
        item = self._array[self._rear]
        self._array[self._rear] = None  # Limpar referência
        self._tamanho -= 1
        self._total_pops += 1
        
        # Reduzir capacidade se necessário
        if self._tamanho > 0 and self._tamanho <= self._capacidade // 4:
            self._redimensionar(max(8, self._capacidade // 2))
        
        return item
    
    def popleft(self) -> T:
        """
        Remove e retorna item do início (esquerda) - O(1).
        
        Returns:
            Item removido
            
        Raises:
            IndexError: Se deque estiver vazio
        """
        if self._tamanho == 0:
            raise IndexError("popleft from empty deque")
        
        item = self._array[self._front]
        self._array[self._front] = None  # Limpar referência
        self._front = (self._front + 1) % self._capacidade
        self._tamanho -= 1
        self._total_pops += 1
        
        # Reduzir capacidade se necessário
        if self._tamanho > 0 and self._tamanho <= self._capacidade // 4:
            self._redimensionar(max(8, self._capacidade // 2))
        
        return item
    
    def peek_front(self) -> T:
        """
        Retorna item do início sem remover - O(1).
        
        Returns:
            Item do início
            
        Raises:
            IndexError: Se deque estiver vazio
        """
        if self._tamanho == 0:
            raise IndexError("peek from empty deque")
        
        return self._array[self._front]
    
    def peek_rear(self) -> T:
        """
        Retorna item do final sem remover - O(1).
        
        Returns:
            Item do final
            
        Raises:
            IndexError: Se deque estiver vazio
        """
        if self._tamanho == 0:
            raise IndexError("peek from empty deque")
        
        rear_index = (self._rear - 1) % self._capacidade
        return self._array[rear_index]
    
    def __getitem__(self, index: int) -> T:
        """
        Acesso por índice - O(1).
        
        Args:
            index: Índice do elemento (0-indexado)
            
        Returns:
            Elemento no índice
            
        Raises:
            IndexError: Se índice for inválido
        """
        if index < 0:
            index += self._tamanho
        
        if index < 0 or index >= self._tamanho:
            raise IndexError(f"deque index {index} out of range")
        
        pos = (self._front + index) % self._capacidade
        return self._array[pos]
    
    def __setitem__(self, index: int, value: T) -> None:
        """
        Atribuição por índice - O(1).
        
        Args:
            index: Índice do elemento
            value: Novo valor
            
        Raises:
            IndexError: Se índice for inválido
        """
        if index < 0:
            index += self._tamanho
        
        if index < 0 or index >= self._tamanho:
            raise IndexError(f"deque index {index} out of range")
        
        pos = (self._front + index) % self._capacidade
        self._array[pos] = value
    
    def rotate(self, steps: int = 1) -> None:
        """
        Rotaciona deque n passos - O(1) para pequenos steps.
        
        Args:
            steps: Número de passos (positivo = direita, negativo = esquerda)
        """
        if self._tamanho <= 1:
            return
        
        steps = steps % self._tamanho
        if steps == 0:
            return
        
        # Rotação eficiente ajustando ponteiros
        self._front = (self._front - steps) % self._capacidade
        self._rear = (self._rear - steps) % self._capacidade
    
    def reverse(self) -> None:
        """
        Reverte deque in-place - O(n).
        """
        for i in range(self._tamanho // 2):
            left_pos = (self._front + i) % self._capacidade
            right_pos = (self._front + self._tamanho - 1 - i) % self._capacidade
            
            self._array[left_pos], self._array[right_pos] = \
                self._array[right_pos], self._array[left_pos]
    
    def extend(self, iterable) -> None:
        """
        Estende deque com elementos do iterável - O(k) onde k é len(iterable).
        
        Args:
            iterable: Iterável com elementos a serem adicionados
        """
        for item in iterable:
            self.append(item)
    
    def extendleft(self, iterable) -> None:
        """
        Estende deque à esquerda com elementos do iterável - O(k).
        
        Args:
            iterable: Iterável com elementos a serem adicionados
        """
        for item in iterable:
            self.appendleft(item)
    
    def clear(self) -> None:
        """Remove todos os elementos - O(1)"""
        self._array = [None] * self._capacidade
        self._front = 0
        self._rear = 0
        self._tamanho = 0
    
    def count(self, item: T) -> int:
        """
        Conta ocorrências do item - O(n).
        
        Args:
            item: Item a ser contado
            
        Returns:
            Número de ocorrências
        """
        contador = 0
        for elemento in self:
            if elemento == item:
                contador += 1
        return contador
    
    def remove(self, item: T) -> None:
        """
        Remove primeira ocorrência do item - O(n).
        
        Args:
            item: Item a ser removido
            
        Raises:
            ValueError: Se item não for encontrado
        """
        for i in range(self._tamanho):
            pos = (self._front + i) % self._capacidade
            if self._array[pos] == item:
                # Mover elementos para preencher lacuna
                # Escolher direção mais eficiente
                if i < self._tamanho // 2:
                    # Mover elementos da esquerda
                    for j in range(i, 0, -1):
                        pos_atual = (self._front + j) % self._capacidade
                        pos_anterior = (self._front + j - 1) % self._capacidade
                        self._array[pos_atual] = self._array[pos_anterior]
                    self._array[self._front] = None
                    self._front = (self._front + 1) % self._capacidade
                else:
                    # Mover elementos da direita
                    for j in range(i, self._tamanho - 1):
                        pos_atual = (self._front + j) % self._capacidade
                        pos_proximo = (self._front + j + 1) % self._capacidade
                        self._array[pos_atual] = self._array[pos_proximo]
                    self._rear = (self._rear - 1) % self._capacidade
                    self._array[self._rear] = None
                
                self._tamanho -= 1
                return
        
        raise ValueError(f"{item} not in deque")
    
    def is_empty(self) -> bool:
        """Verifica se deque está vazio - O(1)"""
        return self._tamanho == 0
    
    def size(self) -> int:
        """Retorna tamanho do deque - O(1)"""
        return self._tamanho
    
    def capacity(self) -> int:
        """Retorna capacidade atual - O(1)"""
        return self._capacidade
    
    def get_stats(self) -> dict:
        """Retorna estatísticas do deque"""
        return {
            'tamanho': self.size(),
            'capacidade': self.capacity(),
            'fator_carga': self.size() / self.capacity() if self.capacity() > 0 else 0,
            'total_appends': self._total_appends,
            'total_pops': self._total_pops,
            'total_redimensionamentos': self._total_redimensionamentos,
            'memoria_total': sys.getsizeof(self._array)
        }
    
    def __iter__(self) -> Iterator[T]:
        """Suporte à iteração"""
        for i in range(self._tamanho):
            pos = (self._front + i) % self._capacidade
            yield self._array[pos]
    
    def __reversed__(self) -> Iterator[T]:
        """Suporte à iteração reversa"""
        for i in range(self._tamanho - 1, -1, -1):
            pos = (self._front + i) % self._capacidade
            yield self._array[pos]
    
    def __len__(self) -> int:
        """Suporte ao len()"""
        return self.size()
    
    def __bool__(self) -> bool:
        """Suporte ao bool()"""
        return not self.is_empty()
    
    def __str__(self) -> str:
        """Representação string do deque"""
        if self.is_empty():
            return "DequeArrayCircular([])"
        
        elementos = ", ".join(str(item) for item in self)
        return f"DequeArrayCircular([{elementos}])"
    
    def __repr__(self) -> str:
        """Representação detalhada"""
        return self.__str__()

class DequeListaLigada(Generic[T]):
    """
    Implementação de deque usando lista duplamente ligada.
    Oferece O(1) para operações nas extremidades, mas O(n) para acesso por índice.
    """
    
    class _No:
        """Nó interno da lista duplamente ligada"""
        
        def __init__(self, dado: T, anterior=None, proximo=None):
            self.dado = dado
            self.anterior = anterior
            self.proximo = proximo
    
    def __init__(self):
        """Inicializa deque vazio"""
        self._head = None
        self._tail = None
        self._tamanho = 0
        
        # Estatísticas
        self._total_appends = 0
        self._total_pops = 0
    
    def append(self, item: T) -> None:
        """
        Adiciona item no final (direita) - O(1).
        
        Args:
            item: Item a ser adicionado
        """
        novo_no = self._No(item, self._tail, None)
        
        if self._tail is not None:
            self._tail.proximo = novo_no
        else:
            self._head = novo_no
        
        self._tail = novo_no
        self._tamanho += 1
        self._total_appends += 1
    
    def appendleft(self, item: T) -> None:
        """
        Adiciona item no início (esquerda) - O(1).
        
        Args:
            item: Item a ser adicionado
        """
        novo_no = self._No(item, None, self._head)
        
        if self._head is not None:
            self._head.anterior = novo_no
        else:
            self._tail = novo_no
        
        self._head = novo_no
        self._tamanho += 1
        self._total_appends += 1
    
    def pop(self) -> T:
        """
        Remove e retorna item do final (direita) - O(1).
        
        Returns:
            Item removido
            
        Raises:
            IndexError: Se deque estiver vazio
        """
        if self._tail is None:
            raise IndexError("pop from empty deque")
        
        item = self._tail.dado
        self._tail = self._tail.anterior
        
        if self._tail is not None:
            self._tail.proximo = None
        else:
            self._head = None
        
        self._tamanho -= 1
        self._total_pops += 1
        
        return item
    
    def popleft(self) -> T:
        """
        Remove e retorna item do início (esquerda) - O(1).
        
        Returns:
            Item removido
            
        Raises:
            IndexError: Se deque estiver vazio
        """
        if self._head is None:
            raise IndexError("popleft from empty deque")
        
        item = self._head.dado
        self._head = self._head.proximo
        
        if self._head is not None:
            self._head.anterior = None
        else:
            self._tail = None
        
        self._tamanho -= 1
        self._total_pops += 1
        
        return item
    
    def peek_front(self) -> T:
        """
        Retorna item do início sem remover - O(1).
        
        Returns:
            Item do início
            
        Raises:
            IndexError: Se deque estiver vazio
        """
        if self._head is None:
            raise IndexError("peek from empty deque")
        
        return self._head.dado
    
    def peek_rear(self) -> T:
        """
        Retorna item do final sem remover - O(1).
        
        Returns:
            Item do final
            
        Raises:
            IndexError: Se deque estiver vazio
        """
        if self._tail is None:
            raise IndexError("peek from empty deque")
        
        return self._tail.dado
    
    def __getitem__(self, index: int) -> T:
        """
        Acesso por índice - O(n).
        Otimizado para começar do início ou fim.
        
        Args:
            index: Índice do elemento (0-indexado)
            
        Returns:
            Elemento no índice
            
        Raises:
            IndexError: Se índice for inválido
        """
        if index < 0:
            index += self._tamanho
        
        if index < 0 or index >= self._tamanho:
            raise IndexError(f"deque index {index} out of range")
        
        # Otimização: começar do início ou fim
        if index <= self._tamanho // 2:
            # Começar do início
            atual = self._head
            for _ in range(index):
                atual = atual.proximo
        else:
            # Começar do fim
            atual = self._tail
            for _ in range(self._tamanho - index - 1):
                atual = atual.anterior
        
        return atual.dado
    
    def reverse(self) -> None:
        """
        Reverte deque in-place - O(n).
        """
        atual = self._head
        
        while atual is not None:
            # Trocar ponteiros anterior e próximo
            atual.anterior, atual.proximo = atual.proximo, atual.anterior
            atual = atual.anterior  # Que era o próximo antes da troca
        
        # Trocar head e tail
        self._head, self._tail = self._tail, self._head
    
    def clear(self) -> None:
        """Remove todos os elementos - O(1)"""
        self._head = None
        self._tail = None
        self._tamanho = 0
    
    def is_empty(self) -> bool:
        """Verifica se deque está vazio - O(1)"""
        return self._head is None
    
    def size(self) -> int:
        """Retorna tamanho do deque - O(1)"""
        return self._tamanho
    
    def get_stats(self) -> dict:
        """Retorna estatísticas do deque"""
        return {
            'tamanho': self.size(),
            'total_appends': self._total_appends,
            'total_pops': self._total_pops,
            'memoria_por_no': sys.getsizeof(self._No(None)) if self._head else 0
        }
    
    def __iter__(self) -> Iterator[T]:
        """Suporte à iteração"""
        atual = self._head
        while atual is not None:
            yield atual.dado
            atual = atual.proximo
    
    def __reversed__(self) -> Iterator[T]:
        """Suporte à iteração reversa"""
        atual = self._tail
        while atual is not None:
            yield atual.dado
            atual = atual.anterior
    
    def __len__(self) -> int:
        """Suporte ao len()"""
        return self.size()
    
    def __bool__(self) -> bool:
        """Suporte ao bool()"""
        return not self.is_empty()
    
    def __str__(self) -> str:
        """Representação string do deque"""
        if self.is_empty():
            return "DequeListaLigada([])"
        
        elementos = ", ".join(str(item) for item in self)
        return f"DequeListaLigada([{elementos}])"

def algoritmos_com_deques():
    """
    Demonstra algoritmos que usam deques eficientemente.
    """
    print("=== ALGORITMOS COM DEQUES ===")
    print()
    
    print("1. SLIDING WINDOW MAXIMUM:")
    
    def sliding_window_maximum(nums: List[int], k: int) -> List[int]:
        """
        Encontra máximo em cada janela deslizante de tamanho k.
        Usa deque monotônico para O(n).
        
        Args:
            nums: Lista de números
            k: Tamanho da janela
            
        Returns:
            Lista com máximos de cada janela
        """
        if not nums or k == 0:
            return []
        
        dq = collections_deque()  # Armazena índices
        resultado = []
        
        for i in range(len(nums)):
            # Remover elementos fora da janela
            while dq and dq[0] <= i - k:
                dq.popleft()
            
            # Manter deque em ordem decrescente
            while dq and nums[dq[-1]] <= nums[i]:
                dq.pop()
            
            dq.append(i)
            
            # Adicionar resultado quando janela estiver completa
            if i >= k - 1:
                resultado.append(nums[dq[0]])
        
        return resultado
    
    # Demonstração
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    
    print(f"   Array: {nums}")
    print(f"   Tamanho da janela: {k}")
    print(f"   Máximos por janela: {sliding_window_maximum(nums, k)}")
    print()
    
    print("   Visualização das janelas:")
    for i in range(len(nums) - k + 1):
        janela = nums[i:i+k]
        maximo = max(janela)
        print(f"   Janela {i+1}: {janela} → máximo: {maximo}")
    print()
    
    print("2. PALINDROME CHECKER:")
    
    def is_palindrome_deque(s: str) -> bool:
        """
        Verifica se string é palíndromo usando deque.
        
        Args:
            s: String a ser verificada
            
        Returns:
            True se for palíndromo, False caso contrário
        """
        # Limpar string (apenas letras e números)
        chars = collections_deque(c.lower() for c in s if c.isalnum())
        
        while len(chars) > 1:
            if chars.popleft() != chars.pop():
                return False
        
        return True
    
    # Demonstração
    test_strings = [
        "A man a plan a canal Panama",
        "race a car",
        "Was it a car or a cat I saw?",
        "Madam",
        "hello"
    ]
    
    print("   Teste de palíndromos:")
    for s in test_strings:
        resultado = is_palindrome_deque(s)
        print(f"   '{s}' → {'✓ Palíndromo' if resultado else '✗ Não é palíndromo'}")
    print()
    
    print("3. BFS COM DEQUE:")
    
    def bfs_shortest_path(graph: dict, start: str, end: str) -> Optional[List[str]]:
        """
        Encontra caminho mais curto usando BFS com deque.
        
        Args:
            graph: Grafo representado como dicionário de adjacências
            start: Nó inicial
            end: Nó final
            
        Returns:
            Caminho mais curto ou None se não existir
        """
        if start == end:
            return [start]
        
        queue = collections_deque([(start, [start])])
        visited = {start}
        
        while queue:
            node, path = queue.popleft()
            
            for neighbor in graph.get(node, []):
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    # Demonstração
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    print("   Grafo:")
    for node, neighbors in graph.items():
        print(f"   {node}: {neighbors}")
    
    print(f"\n   Caminho mais curto de A para F:")
    path = bfs_shortest_path(graph, 'A', 'F')
    if path:
        print(f"   {' → '.join(path)} (distância: {len(path) - 1})")
    else:
        print("   Nenhum caminho encontrado")
    print()
    
    print("4. UNDO/REDO COM LIMITE:")
    
    class UndoRedoManager:
        """Gerenciador de undo/redo com limite usando deque"""
        
        def __init__(self, max_history: int = 10):
            self.max_history = max_history
            self.history = collections_deque(maxlen=max_history)
            self.redo_stack = collections_deque()
            self.current_state = None
        
        def execute_command(self, command: str, state: Any) -> None:
            """Executa comando e salva estado"""
            if self.current_state is not None:
                self.history.append(self.current_state)
            
            self.current_state = state
            self.redo_stack.clear()  # Limpar redo ao executar novo comando
            
            print(f"   Executado: {command} → Estado: {state}")
        
        def undo(self) -> Optional[Any]:
            """Desfaz última operação"""
            if not self.history:
                print("   Nada para desfazer")
                return None
            
            if self.current_state is not None:
                self.redo_stack.append(self.current_state)
            
            self.current_state = self.history.pop()
            print(f"   Desfeito → Estado: {self.current_state}")
            return self.current_state
        
        def redo(self) -> Optional[Any]:
            """Refaz operação desfeita"""
            if not self.redo_stack:
                print("   Nada para refazer")
                return None
            
            if self.current_state is not None:
                self.history.append(self.current_state)
            
            self.current_state = self.redo_stack.pop()
            print(f"   Refeito → Estado: {self.current_state}")
            return self.current_state
        
        def get_status(self) -> dict:
            """Retorna status atual"""
            return {
                'estado_atual': self.current_state,
                'historico_size': len(self.history),
                'redo_size': len(self.redo_stack),
                'pode_undo': len(self.history) > 0,
                'pode_redo': len(self.redo_stack) > 0
            }
    
    # Demonstração
    manager = UndoRedoManager(max_history=3)
    
    print("   Simulação de editor de texto:")
    manager.execute_command("Digitar 'Hello'", "Hello")
    manager.execute_command("Digitar ' World'", "Hello World")
    manager.execute_command("Digitar '!'", "Hello World!")
    manager.execute_command("Deletar '!'", "Hello World")
    
    print(f"\n   Status: {manager.get_status()}")
    
    print("\n   Testando undo/redo:")
    manager.undo()  # Volta para "Hello World!"
    manager.undo()  # Volta para "Hello World"
    manager.redo()  # Vai para "Hello World!"
    manager.execute_command("Digitar '?'", "Hello World?")  # Limpa redo
    
    print(f"\n   Status final: {manager.get_status()}")
    print()

def benchmark_implementacoes():
    """
    Compara performance das implementações de deque.
    """
    print("=== BENCHMARK DAS IMPLEMENTAÇÕES ===")
    print()
    
    def testar_operacoes_extremidades(deque_impl, nome: str, operacoes: int = 50000):
        """Testa operações nas extremidades"""
        
        # Append/Pop direita
        start = time.perf_counter()
        for i in range(operacoes):
            deque_impl.append(i)
        tempo_append = time.perf_counter() - start
        
        start = time.perf_counter()
        for _ in range(operacoes):
            deque_impl.pop()
        tempo_pop = time.perf_counter() - start
        
        # Append/Pop esquerda
        start = time.perf_counter()
        for i in range(operacoes):
            deque_impl.appendleft(i)
        tempo_appendleft = time.perf_counter() - start
        
        start = time.perf_counter()
        for _ in range(operacoes):
            deque_impl.popleft()
        tempo_popleft = time.perf_counter() - start
        
        return tempo_append, tempo_pop, tempo_appendleft, tempo_popleft
    
    def testar_acesso_indice(deque_impl, nome: str, tamanho: int = 10000):
        """Testa acesso por índice"""
        
        # Preencher deque
        for i in range(tamanho):
            deque_impl.append(i)
        
        # Acesso sequencial
        start = time.perf_counter()
        for i in range(tamanho):
            _ = deque_impl[i]
        tempo_sequencial = time.perf_counter() - start
        
        # Acesso aleatório
        indices = list(range(tamanho))
        random.shuffle(indices)
        
        start = time.perf_counter()
        for i in indices:
            _ = deque_impl[i]
        tempo_aleatorio = time.perf_counter() - start
        
        return tempo_sequencial, tempo_aleatorio
    
    operacoes = 50000
    tamanho_acesso = 5000
    
    print(f"   Performance de operações nas extremidades ({operacoes:,} ops):")
    print("   ┌─────────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │   IMPLEMENTAÇÃO     │ APPEND (ms) │  POP (ms)   │APPENDL (ms) │POPL (ms)    │")
    print("   ├─────────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤")
    
    implementacoes = [
        (DequeArrayCircular[int](), "Array Circular"),
        (DequeListaLigada[int](), "Lista Ligada"),
        (collections_deque(), "collections.deque")
    ]
    
    for deque_impl, nome in implementacoes:
        if nome == "collections.deque":
            # Teste especial para collections.deque
            start = time.perf_counter()
            for i in range(operacoes):
                deque_impl.append(i)
            tempo_append = time.perf_counter() - start
            
            start = time.perf_counter()
            for _ in range(operacoes):
                deque_impl.pop()
            tempo_pop = time.perf_counter() - start
            
            start = time.perf_counter()
            for i in range(operacoes):
                deque_impl.appendleft(i)
            tempo_appendleft = time.perf_counter() - start
            
            start = time.perf_counter()
            for _ in range(operacoes):
                deque_impl.popleft()
            tempo_popleft = time.perf_counter() - start
        else:
            tempo_append, tempo_pop, tempo_appendleft, tempo_popleft = \
                testar_operacoes_extremidades(deque_impl, nome, operacoes)
        
        print(f"   │ {nome:19} │ {tempo_append*1000:9.2f} ms │ {tempo_pop*1000:9.2f} ms │ {tempo_appendleft*1000:9.2f} ms │ {tempo_popleft*1000:9.2f} ms │")
    
    print("   └─────────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘")
    print()
    
    print(f"   Performance de acesso por índice ({tamanho_acesso:,} elementos):")
    print("   ┌─────────────────────┬─────────────────┬─────────────────┐")
    print("   │   IMPLEMENTAÇÃO     │ SEQUENCIAL (ms) │ ALEATÓRIO (ms)  │")
    print("   ├─────────────────────┼─────────────────┼─────────────────┤")
    
    # Testar apenas implementações que suportam acesso por índice
    implementacoes_acesso = [
        (DequeArrayCircular[int](), "Array Circular"),
        (DequeListaLigada[int](), "Lista Ligada")
    ]
    
    for deque_impl, nome in implementacoes_acesso:
        tempo_seq, tempo_alea = testar_acesso_indice(deque_impl, nome, tamanho_acesso)
        print(f"   │ {nome:19} │ {tempo_seq*1000:13.2f} ms │ {tempo_alea*1000:13.2f} ms │")
    
    # Teste especial para collections.deque (acesso por índice é O(n))
    deque_python = collections_deque(range(tamanho_acesso))
    
    start = time.perf_counter()
    for i in range(tamanho_acesso):
        _ = deque_python[i]
    tempo_seq = time.perf_counter() - start
    
    indices = list(range(tamanho_acesso))
    random.shuffle(indices)
    
    start = time.perf_counter()
    for i in indices:
        _ = deque_python[i]
    tempo_alea = time.perf_counter() - start
    
    print(f"   │ {'collections.deque':19} │ {tempo_seq*1000:13.2f} ms │ {tempo_alea*1000:13.2f} ms │")
    
    print("   └─────────────────────┴─────────────────┴─────────────────┘")
    print()
    
    print("   Uso de memória:")
    print("   ┌─────────────────────┬─────────────────┬─────────────────┐")
    print("   │   IMPLEMENTAÇÃO     │  BYTES/ELEMENTO │   OVERHEAD      │")
    print("   ├─────────────────────┼─────────────────┼─────────────────┤")
    
    # Calcular uso de memória
    array_deque = DequeArrayCircular[int]()
    for i in range(1000):
        array_deque.append(i)
    
    lista_deque = DequeListaLigada[int]()
    for i in range(1000):
        lista_deque.append(i)
    
    collections_deque_test = collections_deque(range(1000))
    
    memoria_array = array_deque.get_stats()['memoria_total'] / 1000
    memoria_lista = lista_deque.get_stats()['memoria_por_no']
    memoria_collections = sys.getsizeof(collections_deque_test) / 1000
    
    elemento_base = sys.getsizeof(42)
    
    print(f"   │ {'Array Circular':19} │ {memoria_array:13.1f} B │ {memoria_array - elemento_base:13.1f} B │")
    print(f"   │ {'Lista Ligada':19} │ {memoria_lista:13.1f} B │ {memoria_lista - elemento_base:13.1f} B │")
    print(f"   │ {'collections.deque':19} │ {memoria_collections:13.1f} B │ {memoria_collections - elemento_base:13.1f} B │")
    
    print("   └─────────────────────┴─────────────────┴─────────────────┘")
    print()

if __name__ == "__main__":
    print("MÓDULO 4.5 - DEQUES (DOUBLE-ENDED QUEUES)")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceitos_deques()
    print("\n" + "="*50 + "\n")
    
    # Demonstração das implementações
    print("=== DEMONSTRAÇÃO DAS IMPLEMENTAÇÕES ===")
    print()
    
    print("1. DEQUE COM ARRAY CIRCULAR:")
    deque_array = DequeArrayCircular[str]()
    
    # Operações básicas
    print("   Operações nas extremidades:")
    deque_array.append('C')
    print(f"   append('C'): {deque_array}")
    
    deque_array.appendleft('B')
    print(f"   appendleft('B'): {deque_array}")
    
    deque_array.append('D')
    print(f"   append('D'): {deque_array}")
    
    deque_array.appendleft('A')
    print(f"   appendleft('A'): {deque_array}")
    
    print(f"\n   Peek operations:")
    print(f"   peek_front(): {deque_array.peek_front()}")
    print(f"   peek_rear(): {deque_array.peek_rear()}")
    
    print(f"\n   Acesso por índice:")
    for i in range(len(deque_array)):
        print(f"   deque[{i}]: {deque_array[i]}")
    
    print(f"\n   Remoções:")
    print(f"   pop(): {deque_array.pop()} → {deque_array}")
    print(f"   popleft(): {deque_array.popleft()} → {deque_array}")
    
    print(f"\n   Rotação:")
    deque_array.extend(['E', 'F', 'G'])
    print(f"   Após extend: {deque_array}")
    deque_array.rotate(2)
    print(f"   rotate(2): {deque_array}")
    deque_array.rotate(-1)
    print(f"   rotate(-1): {deque_array}")
    
    print(f"\n   Stats: {deque_array.get_stats()}")
    print()
    
    print("2. DEQUE COM LISTA LIGADA:")
    deque_lista = DequeListaLigada[int]()
    
    # Operações básicas
    print("   Operações nas extremidades:")
    for i in [2, 3, 4]:
        deque_lista.append(i)
        print(f"   append({i}): {deque_lista}")
    
    deque_lista.appendleft(1)
    print(f"   appendleft(1): {deque_lista}")
    
    deque_lista.appendleft(0)
    print(f"   appendleft(0): {deque_lista}")
    
    print(f"\n   Acesso otimizado por índice:")
    print(f"   deque[0] (início): {deque_lista[0]}")
    print(f"   deque[4] (fim): {deque_lista[4]}")
    print(f"   deque[2] (meio): {deque_lista[2]}")
    
    print(f"\n   Iteração reversa:")
    print(f"   Normal: {list(deque_lista)}")
    print(f"   Reversa: {list(reversed(deque_lista))}")
    
    print(f"\n   Stats: {deque_lista.get_stats()}")
    print()
    
    print("3. COLLECTIONS.DEQUE (PYTHON NATIVO):")
    deque_python = collections_deque(['B', 'C'])
    
    print("   Operações básicas:")
    deque_python.appendleft('A')
    deque_python.append('D')
    print(f"   Após operações: {list(deque_python)}")
    
    deque_python.rotate(1)
    print(f"   rotate(1): {list(deque_python)}")
    
    deque_python.extendleft(['Z', 'Y'])
    print(f"   extendleft(['Z', 'Y']): {list(deque_python)}")
    
    print(f"   count('A'): {deque_python.count('A')}")
    print(f"   Tamanho: {len(deque_python)}")
    print()
    
    print("\n" + "="*50 + "\n")
    
    algoritmos_com_deques()
    print("\n" + "="*50 + "\n")
    
    benchmark_implementacoes()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 4.5 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceitos de deque (double-ended queue)")
    print("✅ Implementação com array circular")
    print("✅ Implementação com lista duplamente ligada")
    print("✅ Operações O(1) nas extremidades")
    print("✅ Sliding window algorithms")
    print("✅ Palindrome checking")
    print("✅ BFS com deque")
    print("✅ Undo/Redo systems")
    print("✅ Análise comparativa de implementações")
    print("✅ collections.deque do Python")
    print("\n➡️  Próximo: Módulo 4.6 - Aplicações Práticas das Estruturas Lineares")