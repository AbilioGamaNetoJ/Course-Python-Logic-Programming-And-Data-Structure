"""
Módulo: Pilhas (Stacks)
Tópico: Estrutura de Dados LIFO - Last In, First Out
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário

Objetivos de Aprendizado:
- Compreender o conceito LIFO (Last In, First Out)
- Implementar pilha usando array e lista ligada
- Analisar complexidade das operações
- Aplicar pilhas em problemas práticos
- Implementar pilha thread-safe
- Otimizar para diferentes cenários de uso
- Resolver problemas clássicos com pilhas
- Comparar implementações e trade-offs

Conceitos Abordados:
- Princípio LIFO
- Operações fundamentais (push, pop, peek, isEmpty)
- Implementação com array dinâmico
- Implementação com lista ligada
- Pilha limitada vs ilimitada
- Thread safety e concorrência
- Aplicações práticas (parsing, backtracking, etc.)
- Análise de complexidade

Pré-requisitos:
- Arrays e listas dinâmicas
- Conceitos básicos de POO
- Noções de complexidade temporal
- Compreensão de recursão

Complexidade:
- Push: O(1)
- Pop: O(1)
- Peek/Top: O(1)
- isEmpty: O(1)
- Espaço: O(n)
"""

import threading
import time
import random
from typing import Any, Optional, List, Generic, TypeVar
from collections import deque
import sys

T = TypeVar('T')

def conceitos_pilhas():
    """
    Explica conceitos fundamentais de pilhas.
    """
    print("=== CONCEITOS FUNDAMENTAIS DE PILHAS ===")
    print()
    
    print("1. PRINCÍPIO LIFO (Last In, First Out):")
    print()
    print("   Visualização de uma pilha:")
    print("   ┌─────────────────────────────────────┐")
    print("   │              TOPO                   │")
    print("   ├─────────────────────────────────────┤")
    print("   │  [5] ← Último elemento inserido     │")
    print("   │  [4]                                │")
    print("   │  [3]                                │")
    print("   │  [2]                                │")
    print("   │  [1] ← Primeiro elemento inserido   │")
    print("   └─────────────────────────────────────┘")
    print("              BASE")
    print()
    
    print("2. OPERAÇÕES FUNDAMENTAIS:")
    print("   ┌─────────────┬─────────────────────────────────────────┬─────────────┐")
    print("   │  OPERAÇÃO   │               DESCRIÇÃO                 │ COMPLEXIDADE│")
    print("   ├─────────────┼─────────────────────────────────────────┼─────────────┤")
    print("   │ push(item)  │ Adiciona item no topo da pilha          │    O(1)     │")
    print("   │ pop()       │ Remove e retorna item do topo           │    O(1)     │")
    print("   │ peek/top()  │ Retorna item do topo sem remover        │    O(1)     │")
    print("   │ isEmpty()   │ Verifica se a pilha está vazia          │    O(1)     │")
    print("   │ size()      │ Retorna número de elementos             │    O(1)     │")
    print("   └─────────────┴─────────────────────────────────────────┴─────────────┘")
    print()
    
    print("3. DEMONSTRAÇÃO VISUAL DAS OPERAÇÕES:")
    
    def demonstrar_operacoes():
        """Demonstra operações básicas visualmente"""
        
        pilha_visual = []
        
        def mostrar_pilha(operacao=""):
            """Mostra estado atual da pilha"""
            print(f"   {operacao}")
            if not pilha_visual:
                print("   ┌─────────┐")
                print("   │  VAZIA  │")
                print("   └─────────┘")
            else:
                print("   ┌─────────┐")
                for i in range(len(pilha_visual) - 1, -1, -1):
                    marcador = " ← TOPO" if i == len(pilha_visual) - 1 else ""
                    print(f"   │   {pilha_visual[i]:2}    │{marcador}")
                print("   └─────────┘")
            print()
        
        # Estado inicial
        mostrar_pilha("Estado inicial:")
        
        # Push operations
        for valor in [10, 20, 30]:
            pilha_visual.append(valor)
            mostrar_pilha(f"push({valor}):")
        
        # Pop operations
        for _ in range(2):
            if pilha_visual:
                valor = pilha_visual.pop()
                mostrar_pilha(f"pop() → {valor}:")
        
        # Peek operation
        if pilha_visual:
            mostrar_pilha(f"peek() → {pilha_visual[-1]} (sem remover):")
    
    demonstrar_operacoes()

class PilhaArray(Generic[T]):
    """
    Implementação de pilha usando array dinâmico.
    Oferece melhor performance para a maioria dos casos.
    """
    
    def __init__(self, capacidade_inicial: int = 10):
        """
        Inicializa pilha com capacidade inicial.
        
        Args:
            capacidade_inicial: Capacidade inicial do array
        """
        self._dados: List[Optional[T]] = [None] * capacidade_inicial
        self._topo = -1  # Índice do elemento no topo
        self._capacidade = capacidade_inicial
        
        # Estatísticas
        self._total_pushes = 0
        self._total_pops = 0
        self._redimensionamentos = 0
    
    def push(self, item: T) -> None:
        """
        Adiciona item no topo da pilha - O(1) amortizado.
        
        Args:
            item: Item a ser adicionado
        """
        # Verificar se precisa redimensionar
        if self._topo + 1 >= self._capacidade:
            self._redimensionar()
        
        self._topo += 1
        self._dados[self._topo] = item
        self._total_pushes += 1
    
    def pop(self) -> T:
        """
        Remove e retorna item do topo - O(1).
        
        Returns:
            Item removido do topo
            
        Raises:
            IndexError: Se a pilha estiver vazia
        """
        if self.is_empty():
            raise IndexError("pop de pilha vazia")
        
        item = self._dados[self._topo]
        self._dados[self._topo] = None  # Limpar referência
        self._topo -= 1
        self._total_pops += 1
        
        # Reduzir capacidade se muito subutilizada
        if (self._topo + 1) < self._capacidade // 4 and self._capacidade > 10:
            self._redimensionar(self._capacidade // 2)
        
        return item
    
    def peek(self) -> T:
        """
        Retorna item do topo sem remover - O(1).
        
        Returns:
            Item no topo da pilha
            
        Raises:
            IndexError: Se a pilha estiver vazia
        """
        if self.is_empty():
            raise IndexError("peek de pilha vazia")
        
        return self._dados[self._topo]
    
    def is_empty(self) -> bool:
        """Verifica se a pilha está vazia - O(1)"""
        return self._topo == -1
    
    def size(self) -> int:
        """Retorna número de elementos - O(1)"""
        return self._topo + 1
    
    def clear(self) -> None:
        """Remove todos os elementos - O(1)"""
        for i in range(self._topo + 1):
            self._dados[i] = None
        self._topo = -1
    
    def _redimensionar(self, nova_capacidade: Optional[int] = None) -> None:
        """Redimensiona o array interno"""
        if nova_capacidade is None:
            nova_capacidade = self._capacidade * 2
        
        novos_dados = [None] * nova_capacidade
        
        # Copiar elementos existentes
        for i in range(self._topo + 1):
            novos_dados[i] = self._dados[i]
        
        self._dados = novos_dados
        self._capacidade = nova_capacidade
        self._redimensionamentos += 1
    
    def get_stats(self) -> dict:
        """Retorna estatísticas da pilha"""
        return {
            'tamanho': self.size(),
            'capacidade': self._capacidade,
            'utilizacao': (self.size() / self._capacidade) * 100,
            'total_pushes': self._total_pushes,
            'total_pops': self._total_pops,
            'redimensionamentos': self._redimensionamentos
        }
    
    def __str__(self) -> str:
        """Representação string da pilha"""
        if self.is_empty():
            return "PilhaArray(vazia)"
        
        elementos = [str(self._dados[i]) for i in range(self._topo + 1)]
        return f"PilhaArray([{' <- '.join(elementos)}] <- TOPO)"
    
    def __len__(self) -> int:
        """Suporte ao len()"""
        return self.size()

class No(Generic[T]):
    """Nó para lista ligada"""
    
    def __init__(self, dado: T, proximo: Optional['No[T]'] = None):
        self.dado = dado
        self.proximo = proximo

class PilhaListaLigada(Generic[T]):
    """
    Implementação de pilha usando lista ligada.
    Melhor para casos com tamanho muito variável.
    """
    
    def __init__(self):
        """Inicializa pilha vazia"""
        self._topo: Optional[No[T]] = None
        self._tamanho = 0
        
        # Estatísticas
        self._total_pushes = 0
        self._total_pops = 0
    
    def push(self, item: T) -> None:
        """
        Adiciona item no topo da pilha - O(1).
        
        Args:
            item: Item a ser adicionado
        """
        novo_no = No(item, self._topo)
        self._topo = novo_no
        self._tamanho += 1
        self._total_pushes += 1
    
    def pop(self) -> T:
        """
        Remove e retorna item do topo - O(1).
        
        Returns:
            Item removido do topo
            
        Raises:
            IndexError: Se a pilha estiver vazia
        """
        if self.is_empty():
            raise IndexError("pop de pilha vazia")
        
        item = self._topo.dado
        self._topo = self._topo.proximo
        self._tamanho -= 1
        self._total_pops += 1
        
        return item
    
    def peek(self) -> T:
        """
        Retorna item do topo sem remover - O(1).
        
        Returns:
            Item no topo da pilha
            
        Raises:
            IndexError: Se a pilha estiver vazia
        """
        if self.is_empty():
            raise IndexError("peek de pilha vazia")
        
        return self._topo.dado
    
    def is_empty(self) -> bool:
        """Verifica se a pilha está vazia - O(1)"""
        return self._topo is None
    
    def size(self) -> int:
        """Retorna número de elementos - O(1)"""
        return self._tamanho
    
    def clear(self) -> None:
        """Remove todos os elementos - O(1)"""
        self._topo = None
        self._tamanho = 0
    
    def get_stats(self) -> dict:
        """Retorna estatísticas da pilha"""
        return {
            'tamanho': self.size(),
            'total_pushes': self._total_pushes,
            'total_pops': self._total_pops,
            'memoria_por_no': sys.getsizeof(No(None)) if self._topo else 0
        }
    
    def __str__(self) -> str:
        """Representação string da pilha"""
        if self.is_empty():
            return "PilhaListaLigada(vazia)"
        
        elementos = []
        atual = self._topo
        while atual:
            elementos.append(str(atual.dado))
            atual = atual.proximo
        
        return f"PilhaListaLigada([{' <- '.join(elementos)}] <- TOPO)"
    
    def __len__(self) -> int:
        """Suporte ao len()"""
        return self.size()

class PilhaThreadSafe(Generic[T]):
    """
    Pilha thread-safe usando locks.
    """
    
    def __init__(self, capacidade_inicial: int = 10):
        """Inicializa pilha thread-safe"""
        self._pilha = PilhaArray[T](capacidade_inicial)
        self._lock = threading.RLock()  # Reentrant lock
    
    def push(self, item: T) -> None:
        """Thread-safe push"""
        with self._lock:
            self._pilha.push(item)
    
    def pop(self) -> T:
        """Thread-safe pop"""
        with self._lock:
            return self._pilha.pop()
    
    def peek(self) -> T:
        """Thread-safe peek"""
        with self._lock:
            return self._pilha.peek()
    
    def is_empty(self) -> bool:
        """Thread-safe isEmpty"""
        with self._lock:
            return self._pilha.is_empty()
    
    def size(self) -> int:
        """Thread-safe size"""
        with self._lock:
            return self._pilha.size()
    
    def clear(self) -> None:
        """Thread-safe clear"""
        with self._lock:
            self._pilha.clear()

def aplicacoes_praticas():
    """
    Demonstra aplicações práticas de pilhas.
    """
    print("=== APLICAÇÕES PRÁTICAS DE PILHAS ===")
    print()
    
    print("1. VERIFICAÇÃO DE PARÊNTESES BALANCEADOS:")
    
    def verificar_parenteses(expressao: str) -> bool:
        """
        Verifica se parênteses estão balanceados.
        
        Args:
            expressao: String com parênteses para verificar
            
        Returns:
            True se balanceados, False caso contrário
        """
        pilha = PilhaArray[str]()
        pares = {'(': ')', '[': ']', '{': '}'}
        
        for char in expressao:
            if char in pares:  # Abertura
                pilha.push(char)
            elif char in pares.values():  # Fechamento
                if pilha.is_empty():
                    return False
                
                abertura = pilha.pop()
                if pares[abertura] != char:
                    return False
        
        return pilha.is_empty()
    
    # Testes de parênteses
    testes_parenteses = [
        "()",
        "()[]{}",
        "([{}])",
        "((()))",
        "([)]",
        "(((",
        "))",
        "{[()]}",
        ""
    ]
    
    print("   Testes de verificação:")
    print("   ┌─────────────────┬─────────────┬─────────────────────────┐")
    print("   │   EXPRESSÃO     │  RESULTADO  │       EXPLICAÇÃO        │")
    print("   ├─────────────────┼─────────────┼─────────────────────────┤")
    
    for expr in testes_parenteses:
        resultado = verificar_parenteses(expr)
        status = "✓ Válido" if resultado else "✗ Inválido"
        
        if not expr:
            explicacao = "String vazia é válida"
        elif resultado:
            explicacao = "Todos os pares fechados"
        else:
            explicacao = "Parênteses desbalanceados"
        
        print(f"   │ {expr:15} │ {status:11} │ {explicacao:23} │")
    
    print("   └─────────────────┴─────────────┴─────────────────────────┘")
    print()
    
    print("2. AVALIAÇÃO DE EXPRESSÕES POSTFIX (RPN):")
    
    def avaliar_postfix(expressao: str) -> float:
        """
        Avalia expressão em notação postfix (Reverse Polish Notation).
        
        Args:
            expressao: Expressão postfix separada por espaços
            
        Returns:
            Resultado da avaliação
        """
        pilha = PilhaArray[float]()
        operadores = {'+', '-', '*', '/', '^'}
        
        tokens = expressao.split()
        
        for token in tokens:
            if token in operadores:
                if pilha.size() < 2:
                    raise ValueError("Expressão inválida")
                
                b = pilha.pop()
                a = pilha.pop()
                
                if token == '+':
                    resultado = a + b
                elif token == '-':
                    resultado = a - b
                elif token == '*':
                    resultado = a * b
                elif token == '/':
                    if b == 0:
                        raise ValueError("Divisão por zero")
                    resultado = a / b
                elif token == '^':
                    resultado = a ** b
                
                pilha.push(resultado)
            else:
                try:
                    numero = float(token)
                    pilha.push(numero)
                except ValueError:
                    raise ValueError(f"Token inválido: {token}")
        
        if pilha.size() != 1:
            raise ValueError("Expressão inválida")
        
        return pilha.pop()
    
    # Testes de expressões postfix
    testes_postfix = [
        ("3 4 +", "3 + 4"),
        ("15 7 1 1 + - / 3 * 2 1 1 + + -", "((15 / (7 - (1 + 1))) * 3) - (2 + (1 + 1))"),
        ("5 1 2 + 4 * + 3 -", "5 + ((1 + 2) * 4) - 3"),
        ("2 3 ^", "2 ^ 3"),
        ("10 2 /", "10 / 2")
    ]
    
    print("   Avaliação de expressões postfix:")
    print("   ┌─────────────────────────────┬─────────────┬─────────────────────────────┐")
    print("   │       EXPRESSÃO POSTFIX     │  RESULTADO  │      EXPRESSÃO INFIX        │")
    print("   ├─────────────────────────────┼─────────────┼─────────────────────────────┤")
    
    for postfix, infix in testes_postfix:
        try:
            resultado = avaliar_postfix(postfix)
            print(f"   │ {postfix:27} │ {resultado:11.2f} │ {infix:27} │")
        except Exception as e:
            print(f"   │ {postfix:27} │ {'ERRO':11} │ {str(e):27} │")
    
    print("   └─────────────────────────────┴─────────────┴─────────────────────────────┘")
    print()
    
    print("3. ALGORITMO DE BACKTRACKING - LABIRINTO:")
    
    def resolver_labirinto(labirinto: List[List[int]], inicio: tuple, fim: tuple) -> Optional[List[tuple]]:
        """
        Resolve labirinto usando pilha para backtracking.
        
        Args:
            labirinto: Matriz onde 0=caminho, 1=parede
            inicio: Posição inicial (linha, coluna)
            fim: Posição final (linha, coluna)
            
        Returns:
            Lista de posições do caminho ou None se não houver solução
        """
        linhas, colunas = len(labirinto), len(labirinto[0])
        visitados = set()
        pilha = PilhaArray[tuple]()
        caminho = PilhaArray[tuple]()
        
        pilha.push(inicio)
        
        while not pilha.is_empty():
            atual = pilha.pop()
            
            if atual == fim:
                # Reconstruir caminho
                resultado = []
                while not caminho.is_empty():
                    resultado.append(caminho.pop())
                resultado.append(atual)
                return list(reversed(resultado))
            
            if atual in visitados:
                if not caminho.is_empty():
                    caminho.pop()
                continue
            
            visitados.add(atual)
            caminho.push(atual)
            
            linha, coluna = atual
            
            # Explorar vizinhos (cima, direita, baixo, esquerda)
            for dl, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nova_linha, nova_coluna = linha + dl, coluna + dc
                
                if (0 <= nova_linha < linhas and 
                    0 <= nova_coluna < colunas and
                    labirinto[nova_linha][nova_coluna] == 0 and
                    (nova_linha, nova_coluna) not in visitados):
                    
                    pilha.push((nova_linha, nova_coluna))
        
        return None
    
    # Exemplo de labirinto
    labirinto_exemplo = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ]
    
    def mostrar_labirinto_com_caminho(labirinto, caminho=None):
        """Mostra labirinto com caminho marcado"""
        print("   Labirinto (0=caminho, 1=parede, *=solução):")
        
        caminho_set = set(caminho) if caminho else set()
        
        for i, linha in enumerate(labirinto):
            print("   ", end="")
            for j, celula in enumerate(linha):
                if (i, j) in caminho_set:
                    print("* ", end="")
                elif celula == 0:
                    print(". ", end="")
                else:
                    print("█ ", end="")
            print()
        print()
    
    inicio = (0, 0)
    fim = (4, 2)
    
    print(f"   Resolvendo labirinto de {inicio} para {fim}:")
    mostrar_labirinto_com_caminho(labirinto_exemplo)
    
    solucao = resolver_labirinto(labirinto_exemplo, inicio, fim)
    
    if solucao:
        print(f"   ✓ Solução encontrada com {len(solucao)} passos:")
        mostrar_labirinto_com_caminho(labirinto_exemplo, solucao)
        print(f"   Caminho: {' → '.join(map(str, solucao))}")
    else:
        print("   ✗ Nenhuma solução encontrada")
    
    print()

def benchmark_implementacoes():
    """
    Compara performance das diferentes implementações.
    """
    print("=== BENCHMARK DAS IMPLEMENTAÇÕES ===")
    print()
    
    def testar_performance(pilha_class, nome: str, operacoes: int = 100000):
        """Testa performance de uma implementação"""
        
        pilha = pilha_class()
        
        # Teste de push
        start = time.perf_counter()
        for i in range(operacoes):
            pilha.push(i)
        tempo_push = time.perf_counter() - start
        
        # Teste de pop
        start = time.perf_counter()
        for _ in range(operacoes):
            pilha.pop()
        tempo_pop = time.perf_counter() - start
        
        return tempo_push, tempo_pop
    
    operacoes = 100000
    
    print(f"   Performance com {operacoes:,} operações:")
    print("   ┌─────────────────────┬─────────────────┬─────────────────┬─────────────────┐")
    print("   │   IMPLEMENTAÇÃO     │   PUSH (ms)     │    POP (ms)     │   TOTAL (ms)    │")
    print("   ├─────────────────────┼─────────────────┼─────────────────┼─────────────────┤")
    
    implementacoes = [
        (PilhaArray, "Array Dinâmico"),
        (PilhaListaLigada, "Lista Ligada"),
        (lambda: deque(), "deque (Python)")  # Para comparação
    ]
    
    for pilha_class, nome in implementacoes:
        if nome == "deque (Python)":
            # Teste especial para deque
            pilha = deque()
            
            start = time.perf_counter()
            for i in range(operacoes):
                pilha.append(i)
            tempo_push = time.perf_counter() - start
            
            start = time.perf_counter()
            for _ in range(operacoes):
                pilha.pop()
            tempo_pop = time.perf_counter() - start
        else:
            tempo_push, tempo_pop = testar_performance(pilha_class, nome, operacoes)
        
        total = tempo_push + tempo_pop
        
        print(f"   │ {nome:19} │ {tempo_push*1000:13.2f} ms │ {tempo_pop*1000:13.2f} ms │ {total*1000:13.2f} ms │")
    
    print("   └─────────────────────┴─────────────────┴─────────────────┴─────────────────┘")
    print()
    
    print("   Análise de uso de memória:")
    
    # Teste de memória
    tamanhos = [1000, 10000, 100000]
    
    print("   ┌─────────────┬─────────────────┬─────────────────┬─────────────────┐")
    print("   │   TAMANHO   │ ARRAY DINÂMICO  │  LISTA LIGADA   │ DEQUE (PYTHON)  │")
    print("   ├─────────────┼─────────────────┼─────────────────┼─────────────────┤")
    
    for tamanho in tamanhos:
        # Array dinâmico
        pilha_array = PilhaArray()
        for i in range(tamanho):
            pilha_array.push(i)
        memoria_array = sys.getsizeof(pilha_array._dados)
        
        # Lista ligada
        pilha_lista = PilhaListaLigada()
        for i in range(tamanho):
            pilha_lista.push(i)
        # Estimativa baseada no número de nós
        memoria_lista = tamanho * sys.getsizeof(No(None))
        
        # Deque
        pilha_deque = deque()
        for i in range(tamanho):
            pilha_deque.append(i)
        memoria_deque = sys.getsizeof(pilha_deque)
        
        print(f"   │ {tamanho:11,} │ {memoria_array:13,} B │ {memoria_lista:13,} B │ {memoria_deque:13,} B │")
    
    print("   └─────────────┴─────────────────┴─────────────────┴─────────────────┘")
    print()

if __name__ == "__main__":
    print("MÓDULO 4.2 - PILHAS (STACKS)")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceitos_pilhas()
    print("\n" + "="*50 + "\n")
    
    # Demonstração das implementações
    print("=== DEMONSTRAÇÃO DAS IMPLEMENTAÇÕES ===")
    print()
    
    print("1. PILHA COM ARRAY DINÂMICO:")
    pilha_array = PilhaArray[int]()
    
    # Operações básicas
    for i in [10, 20, 30, 40, 50]:
        pilha_array.push(i)
        print(f"   push({i}): {pilha_array}")
    
    print(f"   peek(): {pilha_array.peek()}")
    
    for _ in range(3):
        valor = pilha_array.pop()
        print(f"   pop(): {valor} → {pilha_array}")
    
    print(f"   Stats: {pilha_array.get_stats()}")
    print()
    
    print("2. PILHA COM LISTA LIGADA:")
    pilha_lista = PilhaListaLigada[str]()
    
    for item in ['A', 'B', 'C', 'D']:
        pilha_lista.push(item)
        print(f"   push('{item}'): {pilha_lista}")
    
    print(f"   peek(): '{pilha_lista.peek()}'")
    
    for _ in range(2):
        valor = pilha_lista.pop()
        print(f"   pop(): '{valor}' → {pilha_lista}")
    
    print(f"   Stats: {pilha_lista.get_stats()}")
    print()
    
    print("\n" + "="*50 + "\n")
    
    aplicacoes_praticas()
    print("\n" + "="*50 + "\n")
    
    benchmark_implementacoes()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 4.2 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceito LIFO e operações fundamentais")
    print("✅ Implementação com array dinâmico")
    print("✅ Implementação com lista ligada")
    print("✅ Pilha thread-safe com locks")
    print("✅ Verificação de parênteses balanceados")
    print("✅ Avaliação de expressões postfix (RPN)")
    print("✅ Algoritmo de backtracking para labirintos")
    print("✅ Análise comparativa de performance")
    print("✅ Trade-offs entre implementações")
    print("\n➡️  Próximo: Módulo 4.3 - Filas (Queues)")