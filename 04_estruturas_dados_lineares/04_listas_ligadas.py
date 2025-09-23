"""
Módulo: Listas Ligadas (Linked Lists)
Tópico: Estruturas de Dados Dinâmicas com Ponteiros
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário

Objetivos de Aprendizado:
- Compreender conceitos de ponteiros e referências
- Implementar lista ligada simples
- Implementar lista duplamente ligada
- Implementar lista circular
- Analisar complexidade das operações
- Comparar com arrays dinâmicos
- Aplicar em problemas práticos
- Implementar operações avançadas

Conceitos Abordados:
- Nós e ponteiros/referências
- Lista ligada simples (singly linked)
- Lista duplamente ligada (doubly linked)
- Lista circular
- Operações: inserção, remoção, busca
- Traversal (percorrimento)
- Reversão de lista
- Detecção de ciclos
- Merge de listas ordenadas

Pré-requisitos:
- Conceitos de POO
- Compreensão de referências
- Arrays e listas dinâmicas
- Recursão (para algumas operações)

Complexidade:
- Inserção no início: O(1)
- Inserção no final: O(n) sem tail, O(1) com tail
- Inserção no meio: O(n)
- Remoção: O(n) para busca + O(1) para remoção
- Busca: O(n)
- Espaço: O(n)
"""

from typing import Any, Optional, Iterator, Generic, TypeVar, List, Tuple
import sys
import time
import random

T = TypeVar('T')

def conceitos_listas_ligadas():
    """
    Explica conceitos fundamentais de listas ligadas.
    """
    print("=== CONCEITOS FUNDAMENTAIS DE LISTAS LIGADAS ===")
    print()
    
    print("1. ESTRUTURA DE NÓS E PONTEIROS:")
    print()
    print("   Array vs Lista Ligada:")
    print("   ┌─────────────────────────────────────────────────────────────────┐")
    print("   │ ARRAY (contíguo na memória):                                    │")
    print("   │ ┌───┬───┬───┬───┬───┐                                           │")
    print("   │ │ A │ B │ C │ D │ E │  ← Elementos adjacentes                  │")
    print("   │ └───┴───┴───┴───┴───┘                                           │")
    print("   │   0   1   2   3   4    ← Índices diretos                       │")
    print("   │                                                                 │")
    print("   │ LISTA LIGADA (espalhada na memória):                           │")
    print("   │ ┌─────┬────┐    ┌─────┬────┐    ┌─────┬────┐                   │")
    print("   │ │  A  │ ●──┼───→│  B  │ ●──┼───→│  C  │ ●──┼───→ NULL          │")
    print("   │ └─────┴────┘    └─────┴────┘    └─────┴────┘                   │")
    print("   │  dado  next      dado  next      dado  next                    │")
    print("   └─────────────────────────────────────────────────────────────────┘")
    print()
    
    print("2. TIPOS DE LISTAS LIGADAS:")
    print()
    print("   a) Lista Ligada Simples:")
    print("   ┌─────┬────┐    ┌─────┬────┐    ┌─────┬────┐")
    print("   │  1  │ ●──┼───→│  2  │ ●──┼───→│  3  │NULL│")
    print("   └─────┴────┘    └─────┴────┘    └─────┴────┘")
    print("   head                                    tail")
    print()
    
    print("   b) Lista Duplamente Ligada:")
    print("   ┌────┬─────┬────┐    ┌────┬─────┬────┐    ┌────┬─────┬────┐")
    print("   │NULL│  1  │ ●──┼───→│ ●──│  2  │ ●──┼───→│ ●──│  3  │NULL│")
    print("   └────┴─────┴────┘    └────┴─────┴────┘    └────┴─────┴────┘")
    print("        prev data next       prev data next       prev data next")
    print("   head                                                    tail")
    print()
    
    print("   c) Lista Circular:")
    print("   ┌─────┬────┐    ┌─────┬────┐    ┌─────┬────┐")
    print("   │  1  │ ●──┼───→│  2  │ ●──┼───→│  3  │ ●──┼─┐")
    print("   └─────┴────┘    └─────┴────┘    └─────┴────┘ │")
    print("     ↑                                          │")
    print("     └──────────────────────────────────────────┘")
    print()
    
    print("3. VANTAGENS E DESVANTAGENS:")
    print("   ┌─────────────────────┬─────────────────────┬─────────────────────┐")
    print("   │      ASPECTO        │       ARRAY         │   LISTA LIGADA      │")
    print("   ├─────────────────────┼─────────────────────┼─────────────────────┤")
    print("   │ Acesso por índice   │        O(1)         │        O(n)         │")
    print("   │ Inserção no início  │        O(n)         │        O(1)         │")
    print("   │ Inserção no final   │     O(1) amort.     │    O(n) ou O(1)*    │")
    print("   │ Remoção no início   │        O(n)         │        O(1)         │")
    print("   │ Uso de memória      │      Eficiente      │   Overhead ponteiros │")
    print("   │ Cache locality      │        Boa          │        Ruim         │")
    print("   │ Tamanho dinâmico    │    Redimensiona     │      Verdadeiro     │")
    print("   └─────────────────────┴─────────────────────┴─────────────────────┘")
    print("   * O(1) se mantiver referência para tail")
    print()

class No(Generic[T]):
    """Nó para lista ligada simples"""
    
    def __init__(self, dado: T, proximo: Optional['No[T]'] = None):
        self.dado = dado
        self.proximo = proximo
    
    def __str__(self) -> str:
        return f"No({self.dado})"
    
    def __repr__(self) -> str:
        return self.__str__()

class ListaLigadaSimples(Generic[T]):
    """
    Implementação de lista ligada simples.
    Mantém referência apenas para o head.
    """
    
    def __init__(self):
        """Inicializa lista vazia"""
        self._head: Optional[No[T]] = None
        self._tamanho = 0
        
        # Estatísticas
        self._total_insercoes = 0
        self._total_remocoes = 0
        self._total_buscas = 0
    
    def inserir_inicio(self, item: T) -> None:
        """
        Insere item no início da lista - O(1).
        
        Args:
            item: Item a ser inserido
        """
        novo_no = No(item, self._head)
        self._head = novo_no
        self._tamanho += 1
        self._total_insercoes += 1
    
    def inserir_final(self, item: T) -> None:
        """
        Insere item no final da lista - O(n).
        
        Args:
            item: Item a ser inserido
        """
        novo_no = No(item)
        
        if self._head is None:
            self._head = novo_no
        else:
            atual = self._head
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no
        
        self._tamanho += 1
        self._total_insercoes += 1
    
    def inserir_posicao(self, posicao: int, item: T) -> None:
        """
        Insere item em posição específica - O(n).
        
        Args:
            posicao: Posição para inserção (0-indexada)
            item: Item a ser inserido
            
        Raises:
            IndexError: Se posição for inválida
        """
        if posicao < 0 or posicao > self._tamanho:
            raise IndexError(f"Posição {posicao} inválida para lista de tamanho {self._tamanho}")
        
        if posicao == 0:
            self.inserir_inicio(item)
            return
        
        novo_no = No(item)
        atual = self._head
        
        # Navegar até posição anterior
        for _ in range(posicao - 1):
            atual = atual.proximo
        
        novo_no.proximo = atual.proximo
        atual.proximo = novo_no
        
        self._tamanho += 1
        self._total_insercoes += 1
    
    def remover_inicio(self) -> T:
        """
        Remove e retorna item do início - O(1).
        
        Returns:
            Item removido
            
        Raises:
            IndexError: Se lista estiver vazia
        """
        if self._head is None:
            raise IndexError("Lista vazia")
        
        item = self._head.dado
        self._head = self._head.proximo
        self._tamanho -= 1
        self._total_remocoes += 1
        
        return item
    
    def remover_final(self) -> T:
        """
        Remove e retorna item do final - O(n).
        
        Returns:
            Item removido
            
        Raises:
            IndexError: Se lista estiver vazia
        """
        if self._head is None:
            raise IndexError("Lista vazia")
        
        if self._head.proximo is None:
            # Apenas um elemento
            item = self._head.dado
            self._head = None
            self._tamanho -= 1
            self._total_remocoes += 1
            return item
        
        # Encontrar penúltimo nó
        atual = self._head
        while atual.proximo.proximo is not None:
            atual = atual.proximo
        
        item = atual.proximo.dado
        atual.proximo = None
        self._tamanho -= 1
        self._total_remocoes += 1
        
        return item
    
    def remover_item(self, item: T) -> bool:
        """
        Remove primeira ocorrência do item - O(n).
        
        Args:
            item: Item a ser removido
            
        Returns:
            True se item foi removido, False caso contrário
        """
        if self._head is None:
            return False
        
        # Remover do início
        if self._head.dado == item:
            self._head = self._head.proximo
            self._tamanho -= 1
            self._total_remocoes += 1
            return True
        
        # Procurar no resto da lista
        atual = self._head
        while atual.proximo is not None:
            if atual.proximo.dado == item:
                atual.proximo = atual.proximo.proximo
                self._tamanho -= 1
                self._total_remocoes += 1
                return True
            atual = atual.proximo
        
        return False
    
    def buscar(self, item: T) -> int:
        """
        Busca item e retorna posição - O(n).
        
        Args:
            item: Item a ser buscado
            
        Returns:
            Posição do item ou -1 se não encontrado
        """
        self._total_buscas += 1
        
        atual = self._head
        posicao = 0
        
        while atual is not None:
            if atual.dado == item:
                return posicao
            atual = atual.proximo
            posicao += 1
        
        return -1
    
    def obter(self, posicao: int) -> T:
        """
        Obtém item em posição específica - O(n).
        
        Args:
            posicao: Posição do item (0-indexada)
            
        Returns:
            Item na posição
            
        Raises:
            IndexError: Se posição for inválida
        """
        if posicao < 0 or posicao >= self._tamanho:
            raise IndexError(f"Posição {posicao} inválida para lista de tamanho {self._tamanho}")
        
        atual = self._head
        for _ in range(posicao):
            atual = atual.proximo
        
        return atual.dado
    
    def reverter(self) -> None:
        """
        Reverte a lista in-place - O(n).
        """
        anterior = None
        atual = self._head
        
        while atual is not None:
            proximo = atual.proximo
            atual.proximo = anterior
            anterior = atual
            atual = proximo
        
        self._head = anterior
    
    def is_empty(self) -> bool:
        """Verifica se lista está vazia - O(1)"""
        return self._head is None
    
    def size(self) -> int:
        """Retorna tamanho da lista - O(1)"""
        return self._tamanho
    
    def clear(self) -> None:
        """Remove todos os elementos - O(1)"""
        self._head = None
        self._tamanho = 0
    
    def to_list(self) -> List[T]:
        """Converte para lista Python - O(n)"""
        resultado = []
        atual = self._head
        while atual is not None:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado
    
    def get_stats(self) -> dict:
        """Retorna estatísticas da lista"""
        return {
            'tamanho': self.size(),
            'total_insercoes': self._total_insercoes,
            'total_remocoes': self._total_remocoes,
            'total_buscas': self._total_buscas,
            'memoria_por_no': sys.getsizeof(No(None)) if self._head else 0
        }
    
    def __iter__(self) -> Iterator[T]:
        """Suporte à iteração"""
        atual = self._head
        while atual is not None:
            yield atual.dado
            atual = atual.proximo
    
    def __len__(self) -> int:
        """Suporte ao len()"""
        return self.size()
    
    def __str__(self) -> str:
        """Representação string da lista"""
        if self.is_empty():
            return "ListaLigadaSimples([])"
        
        elementos = " -> ".join(str(item) for item in self)
        return f"ListaLigadaSimples([{elementos}])"
    
    def __getitem__(self, posicao: int) -> T:
        """Suporte ao acesso por índice"""
        return self.obter(posicao)

class NoDuplo(Generic[T]):
    """Nó para lista duplamente ligada"""
    
    def __init__(self, dado: T, anterior: Optional['NoDuplo[T]'] = None, 
                 proximo: Optional['NoDuplo[T]'] = None):
        self.dado = dado
        self.anterior = anterior
        self.proximo = proximo
    
    def __str__(self) -> str:
        return f"NoDuplo({self.dado})"

class ListaDuplamenteLigada(Generic[T]):
    """
    Implementação de lista duplamente ligada.
    Mantém referências para head e tail.
    """
    
    def __init__(self):
        """Inicializa lista vazia"""
        self._head: Optional[NoDuplo[T]] = None
        self._tail: Optional[NoDuplo[T]] = None
        self._tamanho = 0
        
        # Estatísticas
        self._total_insercoes = 0
        self._total_remocoes = 0
    
    def inserir_inicio(self, item: T) -> None:
        """
        Insere item no início da lista - O(1).
        
        Args:
            item: Item a ser inserido
        """
        novo_no = NoDuplo(item, None, self._head)
        
        if self._head is not None:
            self._head.anterior = novo_no
        else:
            self._tail = novo_no
        
        self._head = novo_no
        self._tamanho += 1
        self._total_insercoes += 1
    
    def inserir_final(self, item: T) -> None:
        """
        Insere item no final da lista - O(1).
        
        Args:
            item: Item a ser inserido
        """
        novo_no = NoDuplo(item, self._tail, None)
        
        if self._tail is not None:
            self._tail.proximo = novo_no
        else:
            self._head = novo_no
        
        self._tail = novo_no
        self._tamanho += 1
        self._total_insercoes += 1
    
    def inserir_posicao(self, posicao: int, item: T) -> None:
        """
        Insere item em posição específica - O(n).
        
        Args:
            posicao: Posição para inserção (0-indexada)
            item: Item a ser inserido
            
        Raises:
            IndexError: Se posição for inválida
        """
        if posicao < 0 or posicao > self._tamanho:
            raise IndexError(f"Posição {posicao} inválida para lista de tamanho {self._tamanho}")
        
        if posicao == 0:
            self.inserir_inicio(item)
            return
        
        if posicao == self._tamanho:
            self.inserir_final(item)
            return
        
        # Otimização: começar do início ou fim dependendo da posição
        if posicao <= self._tamanho // 2:
            # Começar do início
            atual = self._head
            for _ in range(posicao):
                atual = atual.proximo
        else:
            # Começar do fim
            atual = self._tail
            for _ in range(self._tamanho - posicao - 1):
                atual = atual.anterior
        
        novo_no = NoDuplo(item, atual.anterior, atual)
        atual.anterior.proximo = novo_no
        atual.anterior = novo_no
        
        self._tamanho += 1
        self._total_insercoes += 1
    
    def remover_inicio(self) -> T:
        """
        Remove e retorna item do início - O(1).
        
        Returns:
            Item removido
            
        Raises:
            IndexError: Se lista estiver vazia
        """
        if self._head is None:
            raise IndexError("Lista vazia")
        
        item = self._head.dado
        self._head = self._head.proximo
        
        if self._head is not None:
            self._head.anterior = None
        else:
            self._tail = None
        
        self._tamanho -= 1
        self._total_remocoes += 1
        
        return item
    
    def remover_final(self) -> T:
        """
        Remove e retorna item do final - O(1).
        
        Returns:
            Item removido
            
        Raises:
            IndexError: Se lista estiver vazia
        """
        if self._tail is None:
            raise IndexError("Lista vazia")
        
        item = self._tail.dado
        self._tail = self._tail.anterior
        
        if self._tail is not None:
            self._tail.proximo = None
        else:
            self._head = None
        
        self._tamanho -= 1
        self._total_remocoes += 1
        
        return item
    
    def remover_item(self, item: T) -> bool:
        """
        Remove primeira ocorrência do item - O(n).
        
        Args:
            item: Item a ser removido
            
        Returns:
            True se item foi removido, False caso contrário
        """
        atual = self._head
        
        while atual is not None:
            if atual.dado == item:
                # Ajustar ponteiros
                if atual.anterior:
                    atual.anterior.proximo = atual.proximo
                else:
                    self._head = atual.proximo
                
                if atual.proximo:
                    atual.proximo.anterior = atual.anterior
                else:
                    self._tail = atual.anterior
                
                self._tamanho -= 1
                self._total_remocoes += 1
                return True
            
            atual = atual.proximo
        
        return False
    
    def buscar(self, item: T) -> int:
        """
        Busca item e retorna posição - O(n).
        
        Args:
            item: Item a ser buscado
            
        Returns:
            Posição do item ou -1 se não encontrado
        """
        atual = self._head
        posicao = 0
        
        while atual is not None:
            if atual.dado == item:
                return posicao
            atual = atual.proximo
            posicao += 1
        
        return -1
    
    def obter(self, posicao: int) -> T:
        """
        Obtém item em posição específica - O(n).
        Otimizado para começar do início ou fim.
        
        Args:
            posicao: Posição do item (0-indexada)
            
        Returns:
            Item na posição
            
        Raises:
            IndexError: Se posição for inválida
        """
        if posicao < 0 or posicao >= self._tamanho:
            raise IndexError(f"Posição {posicao} inválida para lista de tamanho {self._tamanho}")
        
        # Otimização: começar do início ou fim
        if posicao <= self._tamanho // 2:
            # Começar do início
            atual = self._head
            for _ in range(posicao):
                atual = atual.proximo
        else:
            # Começar do fim
            atual = self._tail
            for _ in range(self._tamanho - posicao - 1):
                atual = atual.anterior
        
        return atual.dado
    
    def reverter(self) -> None:
        """
        Reverte a lista in-place - O(n).
        """
        atual = self._head
        
        while atual is not None:
            # Trocar ponteiros anterior e próximo
            atual.anterior, atual.proximo = atual.proximo, atual.anterior
            atual = atual.anterior  # Que era o próximo antes da troca
        
        # Trocar head e tail
        self._head, self._tail = self._tail, self._head
    
    def is_empty(self) -> bool:
        """Verifica se lista está vazia - O(1)"""
        return self._head is None
    
    def size(self) -> int:
        """Retorna tamanho da lista - O(1)"""
        return self._tamanho
    
    def clear(self) -> None:
        """Remove todos os elementos - O(1)"""
        self._head = None
        self._tail = None
        self._tamanho = 0
    
    def to_list(self) -> List[T]:
        """Converte para lista Python - O(n)"""
        resultado = []
        atual = self._head
        while atual is not None:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado
    
    def to_list_reverse(self) -> List[T]:
        """Converte para lista Python em ordem reversa - O(n)"""
        resultado = []
        atual = self._tail
        while atual is not None:
            resultado.append(atual.dado)
            atual = atual.anterior
        return resultado
    
    def get_stats(self) -> dict:
        """Retorna estatísticas da lista"""
        return {
            'tamanho': self.size(),
            'total_insercoes': self._total_insercoes,
            'total_remocoes': self._total_remocoes,
            'memoria_por_no': sys.getsizeof(NoDuplo(None)) if self._head else 0
        }
    
    def __iter__(self) -> Iterator[T]:
        """Suporte à iteração (do início ao fim)"""
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
    
    def __str__(self) -> str:
        """Representação string da lista"""
        if self.is_empty():
            return "ListaDuplamenteLigada([])"
        
        elementos = " <-> ".join(str(item) for item in self)
        return f"ListaDuplamenteLigada([{elementos}])"
    
    def __getitem__(self, posicao: int) -> T:
        """Suporte ao acesso por índice"""
        return self.obter(posicao)

def algoritmos_avancados():
    """
    Demonstra algoritmos avançados com listas ligadas.
    """
    print("=== ALGORITMOS AVANÇADOS COM LISTAS LIGADAS ===")
    print()
    
    print("1. DETECÇÃO DE CICLO (Algoritmo de Floyd):")
    
    def detectar_ciclo_floyd(lista: ListaLigadaSimples[T]) -> bool:
        """
        Detecta ciclo usando algoritmo de Floyd (tartaruga e lebre).
        
        Args:
            lista: Lista ligada a ser verificada
            
        Returns:
            True se houver ciclo, False caso contrário
        """
        if lista._head is None or lista._head.proximo is None:
            return False
        
        lento = lista._head  # Tartaruga
        rapido = lista._head  # Lebre
        
        while rapido is not None and rapido.proximo is not None:
            lento = lento.proximo
            rapido = rapido.proximo.proximo
            
            if lento == rapido:
                return True
        
        return False
    
    # Demonstração
    lista_sem_ciclo = ListaLigadaSimples[int]()
    for i in [1, 2, 3, 4, 5]:
        lista_sem_ciclo.inserir_final(i)
    
    print(f"   Lista sem ciclo: {lista_sem_ciclo}")
    print(f"   Tem ciclo? {detectar_ciclo_floyd(lista_sem_ciclo)}")
    
    # Criar lista com ciclo manualmente
    lista_com_ciclo = ListaLigadaSimples[int]()
    for i in [1, 2, 3, 4]:
        lista_com_ciclo.inserir_final(i)
    
    # Criar ciclo: último nó aponta para o segundo
    atual = lista_com_ciclo._head
    segundo_no = atual.proximo
    while atual.proximo is not None:
        atual = atual.proximo
    atual.proximo = segundo_no  # Criar ciclo
    
    print(f"   Lista com ciclo: 1 -> 2 -> 3 -> 4 -> 2 (ciclo)")
    print(f"   Tem ciclo? {detectar_ciclo_floyd(lista_com_ciclo)}")
    print()
    
    print("2. MERGE DE LISTAS ORDENADAS:")
    
    def merge_listas_ordenadas(lista1: ListaLigadaSimples[int], 
                              lista2: ListaLigadaSimples[int]) -> ListaLigadaSimples[int]:
        """
        Faz merge de duas listas ligadas ordenadas.
        
        Args:
            lista1: Primeira lista ordenada
            lista2: Segunda lista ordenada
            
        Returns:
            Nova lista com elementos mesclados em ordem
        """
        resultado = ListaLigadaSimples[int]()
        
        # Usar ponteiros para percorrer as listas
        p1 = lista1._head
        p2 = lista2._head
        
        # Merge enquanto ambas têm elementos
        while p1 is not None and p2 is not None:
            if p1.dado <= p2.dado:
                resultado.inserir_final(p1.dado)
                p1 = p1.proximo
            else:
                resultado.inserir_final(p2.dado)
                p2 = p2.proximo
        
        # Adicionar elementos restantes
        while p1 is not None:
            resultado.inserir_final(p1.dado)
            p1 = p1.proximo
        
        while p2 is not None:
            resultado.inserir_final(p2.dado)
            p2 = p2.proximo
        
        return resultado
    
    # Demonstração
    lista_a = ListaLigadaSimples[int]()
    for i in [1, 3, 5, 7]:
        lista_a.inserir_final(i)
    
    lista_b = ListaLigadaSimples[int]()
    for i in [2, 4, 6, 8, 9]:
        lista_b.inserir_final(i)
    
    print(f"   Lista A: {lista_a}")
    print(f"   Lista B: {lista_b}")
    
    lista_merged = merge_listas_ordenadas(lista_a, lista_b)
    print(f"   Merge: {lista_merged}")
    print()
    
    print("3. ENCONTRAR MEIO DA LISTA (Técnica dos Dois Ponteiros):")
    
    def encontrar_meio(lista: ListaLigadaSimples[T]) -> Optional[T]:
        """
        Encontra elemento do meio usando técnica dos dois ponteiros.
        
        Args:
            lista: Lista ligada
            
        Returns:
            Elemento do meio ou None se lista vazia
        """
        if lista._head is None:
            return None
        
        lento = lista._head
        rapido = lista._head
        
        while rapido.proximo is not None and rapido.proximo.proximo is not None:
            lento = lento.proximo
            rapido = rapido.proximo.proximo
        
        return lento.dado
    
    # Demonstração
    lista_teste = ListaLigadaSimples[str]()
    elementos = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    
    for elem in elementos:
        lista_teste.inserir_final(elem)
        meio = encontrar_meio(lista_teste)
        print(f"   Lista: {lista_teste.to_list()} → Meio: {meio}")
    
    print()
    
    print("4. REMOVER DUPLICATAS DE LISTA ORDENADA:")
    
    def remover_duplicatas_ordenada(lista: ListaLigadaSimples[T]) -> None:
        """
        Remove duplicatas de lista ordenada in-place.
        
        Args:
            lista: Lista ligada ordenada
        """
        if lista._head is None:
            return
        
        atual = lista._head
        
        while atual.proximo is not None:
            if atual.dado == atual.proximo.dado:
                # Remover duplicata
                atual.proximo = atual.proximo.proximo
                lista._tamanho -= 1
            else:
                atual = atual.proximo
    
    # Demonstração
    lista_dup = ListaLigadaSimples[int]()
    elementos_dup = [1, 1, 2, 3, 3, 3, 4, 5, 5]
    
    for elem in elementos_dup:
        lista_dup.inserir_final(elem)
    
    print(f"   Lista com duplicatas: {lista_dup}")
    remover_duplicatas_ordenada(lista_dup)
    print(f"   Lista sem duplicatas: {lista_dup}")
    print()

def aplicacoes_praticas():
    """
    Demonstra aplicações práticas de listas ligadas.
    """
    print("=== APLICAÇÕES PRÁTICAS ===")
    print()
    
    print("1. HISTÓRICO DE NAVEGAÇÃO (Browser):")
    
    class HistoricoNavegacao:
        """Simula histórico de navegação usando lista duplamente ligada"""
        
        def __init__(self):
            self._historico = ListaDuplamenteLigada[str]()
            self._posicao_atual = -1
        
        def visitar(self, url: str) -> None:
            """Visita nova URL"""
            # Remover histórico futuro se existir
            while self._posicao_atual < len(self._historico) - 1:
                self._historico.remover_final()
            
            self._historico.inserir_final(url)
            self._posicao_atual = len(self._historico) - 1
        
        def voltar(self) -> Optional[str]:
            """Volta uma página"""
            if self._posicao_atual > 0:
                self._posicao_atual -= 1
                return self._historico.obter(self._posicao_atual)
            return None
        
        def avancar(self) -> Optional[str]:
            """Avança uma página"""
            if self._posicao_atual < len(self._historico) - 1:
                self._posicao_atual += 1
                return self._historico.obter(self._posicao_atual)
            return None
        
        def atual(self) -> Optional[str]:
            """Retorna página atual"""
            if 0 <= self._posicao_atual < len(self._historico):
                return self._historico.obter(self._posicao_atual)
            return None
        
        def mostrar_historico(self) -> None:
            """Mostra histórico completo"""
            print("   Histórico de navegação:")
            for i, url in enumerate(self._historico):
                marcador = " ← ATUAL" if i == self._posicao_atual else ""
                print(f"   {i+1}. {url}{marcador}")
    
    # Demonstração
    browser = HistoricoNavegacao()
    
    # Simular navegação
    urls = [
        "https://google.com",
        "https://github.com",
        "https://stackoverflow.com",
        "https://python.org"
    ]
    
    print("   Simulação de navegação:")
    for url in urls:
        browser.visitar(url)
        print(f"   Visitando: {url}")
    
    browser.mostrar_historico()
    print()
    
    # Testar navegação
    print("   Testando navegação:")
    print(f"   Voltar: {browser.voltar()}")
    print(f"   Voltar: {browser.voltar()}")
    print(f"   Avançar: {browser.avancar()}")
    print(f"   Atual: {browser.atual()}")
    print()
    
    print("2. LISTA DE REPRODUÇÃO (Playlist):")
    
    class Playlist:
        """Playlist de música usando lista circular"""
        
        def __init__(self, nome: str):
            self.nome = nome
            self._musicas = ListaLigadaSimples[str]()
            self._atual = None
            self._posicao_atual = 0
        
        def adicionar_musica(self, musica: str) -> None:
            """Adiciona música à playlist"""
            self._musicas.inserir_final(musica)
            if self._atual is None:
                self._atual = musica
                self._posicao_atual = 0
        
        def proxima(self) -> Optional[str]:
            """Vai para próxima música (circular)"""
            if self._musicas.is_empty():
                return None
            
            self._posicao_atual = (self._posicao_atual + 1) % len(self._musicas)
            self._atual = self._musicas.obter(self._posicao_atual)
            return self._atual
        
        def anterior(self) -> Optional[str]:
            """Vai para música anterior (circular)"""
            if self._musicas.is_empty():
                return None
            
            self._posicao_atual = (self._posicao_atual - 1) % len(self._musicas)
            self._atual = self._musicas.obter(self._posicao_atual)
            return self._atual
        
        def atual(self) -> Optional[str]:
            """Retorna música atual"""
            return self._atual
        
        def shuffle(self) -> None:
            """Embaralha playlist"""
            if len(self._musicas) <= 1:
                return
            
            # Converter para lista, embaralhar e recriar
            musicas_list = self._musicas.to_list()
            random.shuffle(musicas_list)
            
            self._musicas.clear()
            for musica in musicas_list:
                self._musicas.inserir_final(musica)
            
            self._posicao_atual = 0
            self._atual = self._musicas.obter(0) if not self._musicas.is_empty() else None
        
        def mostrar_playlist(self) -> None:
            """Mostra playlist completa"""
            print(f"   🎵 Playlist: {self.nome}")
            for i, musica in enumerate(self._musicas):
                marcador = " ♪ TOCANDO" if i == self._posicao_atual else ""
                print(f"   {i+1}. {musica}{marcador}")
    
    # Demonstração
    playlist = Playlist("Minha Playlist")
    
    musicas = [
        "Bohemian Rhapsody - Queen",
        "Stairway to Heaven - Led Zeppelin",
        "Hotel California - Eagles",
        "Sweet Child O' Mine - Guns N' Roses",
        "Imagine - John Lennon"
    ]
    
    print("   Criando playlist:")
    for musica in musicas:
        playlist.adicionar_musica(musica)
        print(f"   Adicionada: {musica}")
    
    playlist.mostrar_playlist()
    print()
    
    print("   Testando navegação:")
    print(f"   Atual: {playlist.atual()}")
    print(f"   Próxima: {playlist.proxima()}")
    print(f"   Próxima: {playlist.proxima()}")
    print(f"   Anterior: {playlist.anterior()}")
    
    # Testar comportamento circular
    print("\n   Testando comportamento circular:")
    for _ in range(len(musicas) + 2):  # Mais que o tamanho da playlist
        print(f"   Próxima: {playlist.proxima()}")
    
    print()

def benchmark_implementacoes():
    """
    Compara performance das implementações.
    """
    print("=== BENCHMARK DAS IMPLEMENTAÇÕES ===")
    print()
    
    def testar_insercoes(estrutura, nome: str, operacoes: int = 10000):
        """Testa performance de inserções"""
        
        # Inserção no início
        start = time.perf_counter()
        for i in range(operacoes):
            estrutura.inserir_inicio(i)
        tempo_inicio = time.perf_counter() - start
        
        estrutura.clear()
        
        # Inserção no final
        start = time.perf_counter()
        for i in range(operacoes):
            estrutura.inserir_final(i)
        tempo_final = time.perf_counter() - start
        
        return tempo_inicio, tempo_final
    
    def testar_acessos(estrutura, nome: str, operacoes: int = 1000):
        """Testa performance de acessos"""
        
        # Preencher estrutura
        for i in range(operacoes):
            estrutura.inserir_final(i)
        
        # Acesso sequencial
        start = time.perf_counter()
        for i in range(operacoes):
            _ = estrutura.obter(i)
        tempo_sequencial = time.perf_counter() - start
        
        # Acesso aleatório
        indices = list(range(operacoes))
        random.shuffle(indices)
        
        start = time.perf_counter()
        for i in indices:
            _ = estrutura.obter(i)
        tempo_aleatorio = time.perf_counter() - start
        
        return tempo_sequencial, tempo_aleatorio
    
    operacoes_insercao = 10000
    operacoes_acesso = 1000
    
    print(f"   Performance de inserções ({operacoes_insercao:,} operações):")
    print("   ┌─────────────────────┬─────────────────┬─────────────────┐")
    print("   │   IMPLEMENTAÇÃO     │  INÍCIO (ms)    │   FINAL (ms)    │")
    print("   ├─────────────────────┼─────────────────┼─────────────────┤")
    
    implementacoes = [
        (ListaLigadaSimples[int](), "Lista Simples"),
        (ListaDuplamenteLigada[int](), "Lista Dupla"),
        (list(), "list (Python)")
    ]
    
    for estrutura, nome in implementacoes:
        if nome == "list (Python)":
            # Teste especial para list
            start = time.perf_counter()
            for i in range(operacoes_insercao):
                estrutura.insert(0, i)
            tempo_inicio = time.perf_counter() - start
            
            estrutura.clear()
            
            start = time.perf_counter()
            for i in range(operacoes_insercao):
                estrutura.append(i)
            tempo_final = time.perf_counter() - start
        else:
            tempo_inicio, tempo_final = testar_insercoes(estrutura, nome, operacoes_insercao)
        
        print(f"   │ {nome:19} │ {tempo_inicio*1000:13.2f} ms │ {tempo_final*1000:13.2f} ms │")
    
    print("   └─────────────────────┴─────────────────┴─────────────────┘")
    print()
    
    print(f"   Performance de acessos ({operacoes_acesso:,} operações):")
    print("   ┌─────────────────────┬─────────────────┬─────────────────┐")
    print("   │   IMPLEMENTAÇÃO     │ SEQUENCIAL (ms) │ ALEATÓRIO (ms)  │")
    print("   ├─────────────────────┼─────────────────┼─────────────────┤")
    
    # Recriar estruturas para teste de acesso
    implementacoes_acesso = [
        (ListaLigadaSimples[int](), "Lista Simples"),
        (ListaDuplamenteLigada[int](), "Lista Dupla")
    ]
    
    for estrutura, nome in implementacoes_acesso:
        tempo_seq, tempo_alea = testar_acessos(estrutura, nome, operacoes_acesso)
        print(f"   │ {nome:19} │ {tempo_seq*1000:13.2f} ms │ {tempo_alea*1000:13.2f} ms │")
    
    # Teste especial para list
    lista_python = list(range(operacoes_acesso))
    
    start = time.perf_counter()
    for i in range(operacoes_acesso):
        _ = lista_python[i]
    tempo_seq = time.perf_counter() - start
    
    indices = list(range(operacoes_acesso))
    random.shuffle(indices)
    
    start = time.perf_counter()
    for i in indices:
        _ = lista_python[i]
    tempo_alea = time.perf_counter() - start
    
    print(f"   │ {'list (Python)':19} │ {tempo_seq*1000:13.2f} ms │ {tempo_alea*1000:13.2f} ms │")
    
    print("   └─────────────────────┴─────────────────┴─────────────────┘")
    print()
    
    print("   Uso de memória por elemento:")
    print("   ┌─────────────────────┬─────────────────┬─────────────────┐")
    print("   │   IMPLEMENTAÇÃO     │  BYTES/ELEMENTO │   OVERHEAD      │")
    print("   ├─────────────────────┼─────────────────┼─────────────────┤")
    
    # Calcular uso de memória
    no_simples = sys.getsizeof(No(42))
    no_duplo = sys.getsizeof(NoDuplo(42))
    elemento_list = sys.getsizeof(42)
    
    print(f"   │ {'Lista Simples':19} │ {no_simples:13} B │ {no_simples - elemento_list:13} B │")
    print(f"   │ {'Lista Dupla':19} │ {no_duplo:13} B │ {no_duplo - elemento_list:13} B │")
    print(f"   │ {'list (Python)':19} │ {elemento_list:13} B │ {0:13} B │")
    
    print("   └─────────────────────┴─────────────────┴─────────────────┘")
    print()

if __name__ == "__main__":
    print("MÓDULO 4.4 - LISTAS LIGADAS")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceitos_listas_ligadas()
    print("\n" + "="*50 + "\n")
    
    # Demonstração das implementações
    print("=== DEMONSTRAÇÃO DAS IMPLEMENTAÇÕES ===")
    print()
    
    print("1. LISTA LIGADA SIMPLES:")
    lista_simples = ListaLigadaSimples[int]()
    
    # Operações básicas
    print("   Inserções:")
    for i in [10, 20, 30]:
        lista_simples.inserir_final(i)
        print(f"   inserir_final({i}): {lista_simples}")
    
    lista_simples.inserir_inicio(5)
    print(f"   inserir_inicio(5): {lista_simples}")
    
    lista_simples.inserir_posicao(2, 15)
    print(f"   inserir_posicao(2, 15): {lista_simples}")
    
    print(f"\n   Acessos:")
    print(f"   obter(0): {lista_simples.obter(0)}")
    print(f"   obter(2): {lista_simples.obter(2)}")
    print(f"   buscar(20): posição {lista_simples.buscar(20)}")
    
    print(f"\n   Remoções:")
    print(f"   remover_inicio(): {lista_simples.remover_inicio()} → {lista_simples}")
    print(f"   remover_final(): {lista_simples.remover_final()} → {lista_simples}")
    print(f"   remover_item(20): {lista_simples.remover_item(20)} → {lista_simples}")
    
    print(f"\n   Reversão:")
    print(f"   Antes: {lista_simples}")
    lista_simples.reverter()
    print(f"   Depois: {lista_simples}")
    
    print(f"\n   Stats: {lista_simples.get_stats()}")
    print()
    
    print("2. LISTA DUPLAMENTE LIGADA:")
    lista_dupla = ListaDuplamenteLigada[str]()
    
    # Operações básicas
    print("   Inserções:")
    for item in ['A', 'B', 'C', 'D']:
        lista_dupla.inserir_final(item)
        print(f"   inserir_final('{item}'): {lista_dupla}")
    
    lista_dupla.inserir_inicio('Z')
    print(f"   inserir_inicio('Z'): {lista_dupla}")
    
    lista_dupla.inserir_posicao(3, 'X')
    print(f"   inserir_posicao(3, 'X'): {lista_dupla}")
    
    print(f"\n   Navegação bidirecional:")
    print(f"   Lista normal: {lista_dupla.to_list()}")
    print(f"   Lista reversa: {lista_dupla.to_list_reverse()}")
    
    print(f"\n   Acesso otimizado:")
    print(f"   obter(1) (do início): {lista_dupla.obter(1)}")
    print(f"   obter(5) (do fim): {lista_dupla.obter(5)}")
    
    print(f"\n   Stats: {lista_dupla.get_stats()}")
    print()
    
    print("\n" + "="*50 + "\n")
    
    algoritmos_avancados()
    print("\n" + "="*50 + "\n")
    
    aplicacoes_praticas()
    print("\n" + "="*50 + "\n")
    
    benchmark_implementacoes()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 4.4 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceitos de nós e ponteiros")
    print("✅ Lista ligada simples")
    print("✅ Lista duplamente ligada")
    print("✅ Algoritmos avançados (Floyd, merge, etc.)")
    print("✅ Detecção de ciclos")
    print("✅ Aplicações práticas (histórico, playlist)")
    print("✅ Análise comparativa de performance")
    print("✅ Trade-offs vs arrays dinâmicos")
    print("\n➡️  Próximo: Módulo 4.5 - Deques (Double-ended Queues)")