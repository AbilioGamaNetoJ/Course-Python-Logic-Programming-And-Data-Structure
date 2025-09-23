"""
MÓDULO 05.6 - HEAPS E FILAS DE PRIORIDADE
=========================================

Objetivos de Aprendizado:
- Compreender a estrutura de dados Heap
- Implementar Min-Heap e Max-Heap
- Entender operações heapify
- Implementar filas de prioridade
- Aplicar heaps em algoritmos de ordenação
- Usar heaps em problemas práticos

Conceitos Abordados:
- Heap (Min-Heap e Max-Heap)
- Propriedade de heap
- Heapify (sift-up e sift-down)
- Heap Sort
- Filas de prioridade
- Heaps binomial e Fibonacci (conceitos)

Pré-requisitos:
- Árvores binárias
- Arrays e listas
- Conceitos de ordenação

Complexidade das Operações:
- Inserção: O(log n)
- Extração: O(log n)
- Peek (ver topo): O(1)
- Construção: O(n)
- Heapify: O(log n)
"""

from typing import List, Optional, Any, Tuple
import heapq
import time
import random
from datetime import datetime


class MinHeap:
    """
    Implementação de Min-Heap usando array.
    
    Propriedades:
    - Pai sempre menor que filhos
    - Árvore binária completa
    - Representação em array
    """
    
    def __init__(self, capacidade_inicial: int = 10):
        """
        Inicializa min-heap vazio.
        
        Args:
            capacidade_inicial: Capacidade inicial do array
        """
        self.heap = []
        self.tamanho = 0
        
        # Estatísticas
        self.comparacoes = 0
        self.trocas = 0
        self.operacoes_insercao = 0
        self.operacoes_extracao = 0
    
    def _pai(self, indice: int) -> int:
        """Retorna índice do pai."""
        return (indice - 1) // 2
    
    def _filho_esquerdo(self, indice: int) -> int:
        """Retorna índice do filho esquerdo."""
        return 2 * indice + 1
    
    def _filho_direito(self, indice: int) -> int:
        """Retorna índice do filho direito."""
        return 2 * indice + 2
    
    def _tem_pai(self, indice: int) -> bool:
        """Verifica se tem pai."""
        return self._pai(indice) >= 0
    
    def _tem_filho_esquerdo(self, indice: int) -> bool:
        """Verifica se tem filho esquerdo."""
        return self._filho_esquerdo(indice) < self.tamanho
    
    def _tem_filho_direito(self, indice: int) -> bool:
        """Verifica se tem filho direito."""
        return self._filho_direito(indice) < self.tamanho
    
    def _trocar(self, indice1: int, indice2: int):
        """Troca elementos em dois índices."""
        self.heap[indice1], self.heap[indice2] = self.heap[indice2], self.heap[indice1]
        self.trocas += 1
    
    def _comparar(self, valor1: Any, valor2: Any) -> bool:
        """
        Compara dois valores (para min-heap, valor1 < valor2).
        
        Args:
            valor1: Primeiro valor
            valor2: Segundo valor
        
        Returns:
            True se valor1 deve vir antes de valor2
        """
        self.comparacoes += 1
        return valor1 < valor2
    
    def _sift_up(self, indice: int):
        """
        Move elemento para cima até satisfazer propriedade do heap.
        
        Args:
            indice: Índice do elemento a ser movido
        """
        while (self._tem_pai(indice) and 
               self._comparar(self.heap[indice], self.heap[self._pai(indice)])):
            self._trocar(indice, self._pai(indice))
            indice = self._pai(indice)
    
    def _sift_down(self, indice: int):
        """
        Move elemento para baixo até satisfazer propriedade do heap.
        
        Args:
            indice: Índice do elemento a ser movido
        """
        while self._tem_filho_esquerdo(indice):
            menor_filho_indice = self._filho_esquerdo(indice)
            
            # Encontrar o menor filho
            if (self._tem_filho_direito(indice) and 
                self._comparar(self.heap[self._filho_direito(indice)], 
                              self.heap[menor_filho_indice])):
                menor_filho_indice = self._filho_direito(indice)
            
            # Se elemento atual já está na posição correta
            if self._comparar(self.heap[indice], self.heap[menor_filho_indice]):
                break
            
            self._trocar(indice, menor_filho_indice)
            indice = menor_filho_indice
    
    def inserir(self, valor: Any):
        """
        Insere valor no heap.
        
        Args:
            valor: Valor a ser inserido
        """
        self.operacoes_insercao += 1
        self.heap.append(valor)
        self.tamanho += 1
        self._sift_up(self.tamanho - 1)
    
    def extrair_minimo(self) -> Any:
        """
        Remove e retorna o menor elemento.
        
        Returns:
            Menor elemento do heap
        
        Raises:
            IndexError: Se heap estiver vazio
        """
        if self.tamanho == 0:
            raise IndexError("Heap está vazio")
        
        self.operacoes_extracao += 1
        
        # Salvar mínimo
        minimo = self.heap[0]
        
        # Mover último elemento para raiz
        self.heap[0] = self.heap[self.tamanho - 1]
        self.tamanho -= 1
        self.heap.pop()
        
        # Restaurar propriedade do heap
        if self.tamanho > 0:
            self._sift_down(0)
        
        return minimo
    
    def peek(self) -> Any:
        """
        Retorna menor elemento sem removê-lo.
        
        Returns:
            Menor elemento do heap
        
        Raises:
            IndexError: Se heap estiver vazio
        """
        if self.tamanho == 0:
            raise IndexError("Heap está vazio")
        return self.heap[0]
    
    def esta_vazio(self) -> bool:
        """Verifica se heap está vazio."""
        return self.tamanho == 0
    
    def obter_tamanho(self) -> int:
        """Retorna tamanho do heap."""
        return self.tamanho
    
    def construir_heap(self, lista: List[Any]):
        """
        Constrói heap a partir de lista em O(n).
        
        Args:
            lista: Lista de elementos
        """
        self.heap = lista.copy()
        self.tamanho = len(lista)
        
        # Começar do último nó não-folha e fazer sift-down
        for i in range(self._pai(self.tamanho - 1), -1, -1):
            self._sift_down(i)
    
    def alterar_prioridade(self, indice: int, novo_valor: Any):
        """
        Altera valor em índice específico.
        
        Args:
            indice: Índice do elemento
            novo_valor: Novo valor
        """
        if indice < 0 or indice >= self.tamanho:
            raise IndexError("Índice inválido")
        
        valor_antigo = self.heap[indice]
        self.heap[indice] = novo_valor
        
        # Decidir direção do movimento
        if self._comparar(novo_valor, valor_antigo):
            self._sift_up(indice)
        else:
            self._sift_down(indice)
    
    def remover(self, valor: Any) -> bool:
        """
        Remove primeira ocorrência de um valor.
        
        Args:
            valor: Valor a ser removido
        
        Returns:
            True se valor foi removido, False se não encontrado
        """
        try:
            indice = self.heap.index(valor)
        except ValueError:
            return False
        
        # Mover último elemento para posição do removido
        self.heap[indice] = self.heap[self.tamanho - 1]
        self.tamanho -= 1
        self.heap.pop()
        
        if indice < self.tamanho:
            # Tentar ambas as direções
            if (self._tem_pai(indice) and 
                self._comparar(self.heap[indice], self.heap[self._pai(indice)])):
                self._sift_up(indice)
            else:
                self._sift_down(indice)
        
        return True
    
    def validar_heap(self) -> bool:
        """
        Valida se estrutura mantém propriedade do heap.
        
        Returns:
            True se é um heap válido
        """
        for i in range(self.tamanho):
            if self._tem_filho_esquerdo(i):
                if not self._comparar(self.heap[i], self.heap[self._filho_esquerdo(i)]):
                    return False
            
            if self._tem_filho_direito(i):
                if not self._comparar(self.heap[i], self.heap[self._filho_direito(i)]):
                    return False
        
        return True
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas das operações."""
        return {
            'tamanho': self.tamanho,
            'comparacoes': self.comparacoes,
            'trocas': self.trocas,
            'operacoes_insercao': self.operacoes_insercao,
            'operacoes_extracao': self.operacoes_extracao,
            'heap_valido': self.validar_heap()
        }
    
    def visualizar(self) -> str:
        """
        Cria representação visual do heap.
        
        Returns:
            String com visualização em árvore
        """
        if self.tamanho == 0:
            return "Heap vazio"
        
        resultado = []
        self._visualizar_recursivo(0, 0, resultado)
        return "\n".join(resultado)
    
    def _visualizar_recursivo(self, indice: int, nivel: int, resultado: List[str]):
        """Visualiza heap recursivamente."""
        if indice >= self.tamanho:
            return
        
        # Visualizar filho direito primeiro (para aparecer em cima)
        if self._tem_filho_direito(indice):
            self._visualizar_recursivo(self._filho_direito(indice), nivel + 1, resultado)
        
        # Visualizar nó atual
        indent = "    " * nivel
        resultado.append(f"{indent}{self.heap[indice]}")
        
        # Visualizar filho esquerdo
        if self._tem_filho_esquerdo(indice):
            self._visualizar_recursivo(self._filho_esquerdo(indice), nivel + 1, resultado)


class MaxHeap(MinHeap):
    """
    Implementação de Max-Heap herdando de Min-Heap.
    
    Diferença: Inverte a comparação para manter maior elemento no topo.
    """
    
    def _comparar(self, valor1: Any, valor2: Any) -> bool:
        """
        Compara dois valores (para max-heap, valor1 > valor2).
        
        Args:
            valor1: Primeiro valor
            valor2: Segundo valor
        
        Returns:
            True se valor1 deve vir antes de valor2
        """
        self.comparacoes += 1
        return valor1 > valor2
    
    def extrair_maximo(self) -> Any:
        """
        Remove e retorna o maior elemento.
        
        Returns:
            Maior elemento do heap
        """
        return self.extrair_minimo()  # Funcionalidade é a mesma


class FilaPrioridade:
    """
    Fila de prioridade usando Min-Heap.
    
    Elementos com menor prioridade são processados primeiro.
    """
    
    def __init__(self):
        """Inicializa fila de prioridade vazia."""
        self.heap = MinHeap()
        self.contador = 0  # Para desempate (FIFO para mesma prioridade)
    
    def inserir(self, item: Any, prioridade: int):
        """
        Insere item com prioridade.
        
        Args:
            item: Item a ser inserido
            prioridade: Prioridade (menor valor = maior prioridade)
        """
        # Usar contador para desempate (manter ordem FIFO)
        entrada = (prioridade, self.contador, item)
        self.heap.inserir(entrada)
        self.contador += 1
    
    def extrair(self) -> Any:
        """
        Remove e retorna item com maior prioridade.
        
        Returns:
            Item com maior prioridade
        
        Raises:
            IndexError: Se fila estiver vazia
        """
        if self.heap.esta_vazio():
            raise IndexError("Fila de prioridade está vazia")
        
        prioridade, contador, item = self.heap.extrair_minimo()
        return item
    
    def peek(self) -> Any:
        """
        Retorna item com maior prioridade sem removê-lo.
        
        Returns:
            Item com maior prioridade
        """
        if self.heap.esta_vazio():
            raise IndexError("Fila de prioridade está vazia")
        
        prioridade, contador, item = self.heap.peek()
        return item
    
    def esta_vazia(self) -> bool:
        """Verifica se fila está vazia."""
        return self.heap.esta_vazio()
    
    def obter_tamanho(self) -> int:
        """Retorna tamanho da fila."""
        return self.heap.obter_tamanho()
    
    def alterar_prioridade(self, item: Any, nova_prioridade: int) -> bool:
        """
        Altera prioridade de um item (operação custosa).
        
        Args:
            item: Item a ter prioridade alterada
            nova_prioridade: Nova prioridade
        
        Returns:
            True se item foi encontrado e alterado
        """
        # Buscar item no heap (operação O(n))
        for i in range(self.heap.tamanho):
            prioridade, contador, heap_item = self.heap.heap[i]
            if heap_item == item:
                # Alterar prioridade
                nova_entrada = (nova_prioridade, contador, item)
                self.heap.alterar_prioridade(i, nova_entrada)
                return True
        
        return False


class HeapSort:
    """
    Implementação do algoritmo Heap Sort.
    
    Características:
    - Complexidade O(n log n) no pior caso
    - Ordenação in-place
    - Não é estável
    """
    
    @staticmethod
    def ordenar(lista: List[Any], crescente: bool = True) -> List[Any]:
        """
        Ordena lista usando Heap Sort.
        
        Args:
            lista: Lista a ser ordenada
            crescente: Se True, ordem crescente; se False, decrescente
        
        Returns:
            Lista ordenada
        """
        if not lista:
            return lista
        
        lista_copia = lista.copy()
        n = len(lista_copia)
        
        # Construir heap (max-heap para ordem crescente)
        for i in range(n // 2 - 1, -1, -1):
            HeapSort._heapify(lista_copia, n, i, crescente)
        
        # Extrair elementos um por um
        for i in range(n - 1, 0, -1):
            # Mover raiz atual para o final
            lista_copia[0], lista_copia[i] = lista_copia[i], lista_copia[0]
            
            # Chamar heapify na heap reduzida
            HeapSort._heapify(lista_copia, i, 0, crescente)
        
        return lista_copia
    
    @staticmethod
    def _heapify(lista: List[Any], tamanho: int, indice: int, crescente: bool):
        """
        Mantém propriedade do heap.
        
        Args:
            lista: Lista sendo ordenada
            tamanho: Tamanho da heap
            indice: Índice da raiz da subárvore
            crescente: Direção da ordenação
        """
        maior = indice
        esquerdo = 2 * indice + 1
        direito = 2 * indice + 2
        
        # Comparar com filho esquerdo
        if esquerdo < tamanho:
            if crescente:
                if lista[esquerdo] > lista[maior]:
                    maior = esquerdo
            else:
                if lista[esquerdo] < lista[maior]:
                    maior = esquerdo
        
        # Comparar com filho direito
        if direito < tamanho:
            if crescente:
                if lista[direito] > lista[maior]:
                    maior = direito
            else:
                if lista[direito] < lista[maior]:
                    maior = direito
        
        # Se maior não é a raiz
        if maior != indice:
            lista[indice], lista[maior] = lista[maior], lista[indice]
            HeapSort._heapify(lista, tamanho, maior, crescente)
    
    @staticmethod
    def ordenar_in_place(lista: List[Any], crescente: bool = True):
        """
        Ordena lista in-place usando Heap Sort.
        
        Args:
            lista: Lista a ser ordenada (modificada)
            crescente: Se True, ordem crescente; se False, decrescente
        """
        n = len(lista)
        
        # Construir heap
        for i in range(n // 2 - 1, -1, -1):
            HeapSort._heapify(lista, n, i, crescente)
        
        # Extrair elementos
        for i in range(n - 1, 0, -1):
            lista[0], lista[i] = lista[i], lista[0]
            HeapSort._heapify(lista, i, 0, crescente)


# Aplicações Práticas
class SimuladorProcessos:
    """
    Simulador de escalonamento de processos usando fila de prioridade.
    """
    
    def __init__(self):
        """Inicializa simulador."""
        self.fila_processos = FilaPrioridade()
        self.tempo_atual = 0
        self.processos_executados = []
        self.tempo_espera_total = 0
        self.num_processos = 0
    
    def adicionar_processo(self, id_processo: str, prioridade: int, 
                          tempo_chegada: int, tempo_execucao: int):
        """
        Adiciona processo ao sistema.
        
        Args:
            id_processo: Identificador do processo
            prioridade: Prioridade (menor valor = maior prioridade)
            tempo_chegada: Quando processo chega
            tempo_execucao: Tempo necessário para execução
        """
        processo = {
            'id': id_processo,
            'prioridade': prioridade,
            'tempo_chegada': tempo_chegada,
            'tempo_execucao': tempo_execucao,
            'tempo_inicio': None,
            'tempo_fim': None
        }
        
        # Inserir com prioridade combinada (prioridade + tempo_chegada)
        prioridade_combinada = (prioridade, tempo_chegada)
        self.fila_processos.inserir(processo, prioridade)
        self.num_processos += 1
    
    def executar_simulacao(self):
        """Executa simulação do escalonador."""
        print("=== SIMULAÇÃO DE ESCALONAMENTO ===")
        
        while not self.fila_processos.esta_vazia():
            # Obter próximo processo
            processo = self.fila_processos.extrair()
            
            # Ajustar tempo atual se necessário
            if self.tempo_atual < processo['tempo_chegada']:
                self.tempo_atual = processo['tempo_chegada']
            
            # Executar processo
            processo['tempo_inicio'] = self.tempo_atual
            processo['tempo_fim'] = self.tempo_atual + processo['tempo_execucao']
            
            # Calcular tempo de espera
            tempo_espera = processo['tempo_inicio'] - processo['tempo_chegada']
            self.tempo_espera_total += tempo_espera
            
            print(f"Executando {processo['id']} (prioridade {processo['prioridade']}) "
                  f"de {processo['tempo_inicio']} a {processo['tempo_fim']} "
                  f"(espera: {tempo_espera})")
            
            # Avançar tempo
            self.tempo_atual = processo['tempo_fim']
            self.processos_executados.append(processo)
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas da simulação."""
        if self.num_processos == 0:
            return {}
        
        tempo_espera_medio = self.tempo_espera_total / self.num_processos
        tempo_total = self.tempo_atual
        
        return {
            'num_processos': self.num_processos,
            'tempo_total': tempo_total,
            'tempo_espera_medio': tempo_espera_medio,
            'tempo_espera_total': self.tempo_espera_total,
            'throughput': self.num_processos / tempo_total if tempo_total > 0 else 0
        }


class AlgoritmoHuffman:
    """
    Implementação do algoritmo de Huffman para compressão usando heap.
    """
    
    class NoHuffman:
        """Nó da árvore de Huffman."""
        
        def __init__(self, char: Optional[str], freq: int, 
                     esquerdo=None, direito=None):
            self.char = char
            self.freq = freq
            self.esquerdo = esquerdo
            self.direito = direito
        
        def __lt__(self, outro):
            """Comparação para heap (por frequência)."""
            return self.freq < outro.freq
        
        def eh_folha(self) -> bool:
            """Verifica se é nó folha."""
            return self.esquerdo is None and self.direito is None
    
    def __init__(self):
        """Inicializa algoritmo de Huffman."""
        self.arvore_huffman = None
        self.codigos = {}
        self.frequencias = {}
    
    def calcular_frequencias(self, texto: str) -> dict:
        """
        Calcula frequência de cada caractere.
        
        Args:
            texto: Texto a ser analisado
        
        Returns:
            Dicionário com frequências
        """
        self.frequencias = {}
        for char in texto:
            self.frequencias[char] = self.frequencias.get(char, 0) + 1
        return self.frequencias
    
    def construir_arvore(self, frequencias: dict):
        """
        Constrói árvore de Huffman usando heap.
        
        Args:
            frequencias: Dicionário com frequências dos caracteres
        """
        # Criar heap com nós folha
        heap = MinHeap()
        
        for char, freq in frequencias.items():
            no = self.NoHuffman(char, freq)
            heap.inserir(no)
        
        # Construir árvore
        while heap.obter_tamanho() > 1:
            # Extrair dois nós com menor frequência
            no1 = heap.extrair_minimo()
            no2 = heap.extrair_minimo()
            
            # Criar nó interno
            freq_combinada = no1.freq + no2.freq
            no_interno = self.NoHuffman(None, freq_combinada, no1, no2)
            
            heap.inserir(no_interno)
        
        # Raiz da árvore
        self.arvore_huffman = heap.extrair_minimo()
    
    def gerar_codigos(self):
        """Gera códigos de Huffman para cada caractere."""
        self.codigos = {}
        if self.arvore_huffman:
            self._gerar_codigos_recursivo(self.arvore_huffman, "")
    
    def _gerar_codigos_recursivo(self, no: NoHuffman, codigo: str):
        """Gera códigos recursivamente."""
        if no.eh_folha():
            # Caso especial: apenas um caractere
            self.codigos[no.char] = codigo if codigo else "0"
        else:
            if no.esquerdo:
                self._gerar_codigos_recursivo(no.esquerdo, codigo + "0")
            if no.direito:
                self._gerar_codigos_recursivo(no.direito, codigo + "1")
    
    def codificar(self, texto: str) -> str:
        """
        Codifica texto usando códigos de Huffman.
        
        Args:
            texto: Texto a ser codificado
        
        Returns:
            Texto codificado em binário
        """
        if not self.codigos:
            self.calcular_frequencias(texto)
            self.construir_arvore(self.frequencias)
            self.gerar_codigos()
        
        resultado = ""
        for char in texto:
            resultado += self.codigos[char]
        
        return resultado
    
    def decodificar(self, codigo_binario: str) -> str:
        """
        Decodifica código binário usando árvore de Huffman.
        
        Args:
            codigo_binario: Código binário a ser decodificado
        
        Returns:
            Texto decodificado
        """
        if not self.arvore_huffman:
            raise ValueError("Árvore de Huffman não foi construída")
        
        resultado = ""
        no_atual = self.arvore_huffman
        
        for bit in codigo_binario:
            if bit == "0":
                no_atual = no_atual.esquerdo
            else:
                no_atual = no_atual.direito
            
            # Se chegou em folha, encontrou caractere
            if no_atual.eh_folha():
                resultado += no_atual.char
                no_atual = self.arvore_huffman
        
        return resultado
    
    def calcular_compressao(self, texto: str) -> dict:
        """
        Calcula estatísticas de compressão.
        
        Args:
            texto: Texto original
        
        Returns:
            Dicionário com estatísticas
        """
        codigo_binario = self.codificar(texto)
        
        # Tamanhos
        tamanho_original = len(texto) * 8  # ASCII = 8 bits por char
        tamanho_comprimido = len(codigo_binario)
        
        # Taxa de compressão
        taxa_compressao = (tamanho_original - tamanho_comprimido) / tamanho_original
        
        return {
            'tamanho_original_chars': len(texto),
            'tamanho_original_bits': tamanho_original,
            'tamanho_comprimido_bits': tamanho_comprimido,
            'taxa_compressao': taxa_compressao,
            'economia_bits': tamanho_original - tamanho_comprimido,
            'codigos': self.codigos.copy(),
            'frequencias': self.frequencias.copy()
        }


# Funções de Demonstração e Benchmark
def demonstrar_min_max_heap():
    """Demonstra operações básicas de Min-Heap e Max-Heap."""
    print("=== DEMONSTRAÇÃO: MIN-HEAP E MAX-HEAP ===\n")
    
    # Min-Heap
    print("1. MIN-HEAP:")
    min_heap = MinHeap()
    
    valores = [15, 10, 20, 8, 25, 5, 7, 6, 2, 9, 11]
    print(f"Inserindo valores: {valores}")
    
    for valor in valores:
        min_heap.inserir(valor)
    
    print(f"\nVisualizacao do Min-Heap:")
    print(min_heap.visualizar())
    
    print(f"\nExtraindo mínimos:")
    while not min_heap.esta_vazio():
        minimo = min_heap.extrair_minimo()
        print(f"Extraído: {minimo}")
        if min_heap.obter_tamanho() <= 3:  # Mostrar apenas primeiros e últimos
            break
    
    # Max-Heap
    print(f"\n2. MAX-HEAP:")
    max_heap = MaxHeap()
    
    for valor in valores:
        max_heap.inserir(valor)
    
    print(f"Visualização do Max-Heap:")
    print(max_heap.visualizar())
    
    print(f"\nExtraindo máximos:")
    for _ in range(5):  # Extrair apenas alguns
        if not max_heap.esta_vazio():
            maximo = max_heap.extrair_maximo()
            print(f"Extraído: {maximo}")
    
    # Estatísticas
    stats = max_heap.obter_estatisticas()
    print(f"\nEstatísticas do Max-Heap:")
    for chave, valor in stats.items():
        print(f"  {chave}: {valor}")


def demonstrar_fila_prioridade():
    """Demonstra fila de prioridade."""
    print("\n=== DEMONSTRAÇÃO: FILA DE PRIORIDADE ===\n")
    
    fila = FilaPrioridade()
    
    # Adicionar tarefas com diferentes prioridades
    tarefas = [
        ("Backup do sistema", 1),      # Alta prioridade
        ("Enviar email", 3),           # Baixa prioridade
        ("Processar pagamentos", 1),   # Alta prioridade
        ("Gerar relatório", 2),        # Média prioridade
        ("Limpar cache", 3),           # Baixa prioridade
        ("Atualizar banco", 1),        # Alta prioridade
    ]
    
    print("Adicionando tarefas:")
    for tarefa, prioridade in tarefas:
        fila.inserir(tarefa, prioridade)
        print(f"  {tarefa} (prioridade {prioridade})")
    
    print(f"\nProcessando tarefas por prioridade:")
    while not fila.esta_vazia():
        tarefa = fila.extrair()
        print(f"  Executando: {tarefa}")


def demonstrar_heap_sort():
    """Demonstra algoritmo Heap Sort."""
    print("\n=== DEMONSTRAÇÃO: HEAP SORT ===\n")
    
    # Lista desordenada
    lista_original = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42]
    print(f"Lista original: {lista_original}")
    
    # Ordenação crescente
    lista_crescente = HeapSort.ordenar(lista_original, crescente=True)
    print(f"Ordem crescente: {lista_crescente}")
    
    # Ordenação decrescente
    lista_decrescente = HeapSort.ordenar(lista_original, crescente=False)
    print(f"Ordem decrescente: {lista_decrescente}")
    
    # Ordenação in-place
    lista_in_place = lista_original.copy()
    HeapSort.ordenar_in_place(lista_in_place)
    print(f"In-place (crescente): {lista_in_place}")


def demonstrar_aplicacoes_praticas():
    """Demonstra aplicações práticas."""
    print("\n=== DEMONSTRAÇÃO: APLICAÇÕES PRÁTICAS ===\n")
    
    # Simulador de processos
    print("1. SIMULADOR DE ESCALONAMENTO DE PROCESSOS:")
    simulador = SimuladorProcessos()
    
    # Adicionar processos
    processos = [
        ("P1", 2, 0, 5),   # id, prioridade, chegada, execução
        ("P2", 1, 1, 3),   # P2 tem prioridade mais alta
        ("P3", 3, 2, 8),   # P3 tem prioridade mais baixa
        ("P4", 1, 3, 2),   # P4 tem prioridade alta
        ("P5", 2, 4, 4),   # P5 tem prioridade média
    ]
    
    for id_proc, prioridade, chegada, execucao in processos:
        simulador.adicionar_processo(id_proc, prioridade, chegada, execucao)
    
    simulador.executar_simulacao()
    
    stats_sim = simulador.obter_estatisticas()
    print(f"\nEstatísticas da simulação:")
    for chave, valor in stats_sim.items():
        print(f"  {chave}: {valor:.2f}" if isinstance(valor, float) else f"  {chave}: {valor}")
    
    # Algoritmo de Huffman
    print(f"\n2. COMPRESSÃO DE HUFFMAN:")
    huffman = AlgoritmoHuffman()
    
    texto = "this is an example of a huffman tree"
    print(f"Texto original: '{texto}'")
    
    stats_huffman = huffman.calcular_compressao(texto)
    
    print(f"\nFrequências dos caracteres:")
    for char, freq in sorted(stats_huffman['frequencias'].items()):
        print(f"  '{char}': {freq}")
    
    print(f"\nCódigos de Huffman:")
    for char, codigo in sorted(stats_huffman['codigos'].items()):
        print(f"  '{char}': {codigo}")
    
    print(f"\nEstatísticas de compressão:")
    print(f"  Tamanho original: {stats_huffman['tamanho_original_bits']} bits")
    print(f"  Tamanho comprimido: {stats_huffman['tamanho_comprimido_bits']} bits")
    print(f"  Taxa de compressão: {stats_huffman['taxa_compressao']:.2%}")
    print(f"  Economia: {stats_huffman['economia_bits']} bits")
    
    # Teste de codificação/decodificação
    codigo_binario = huffman.codificar(texto)
    texto_decodificado = huffman.decodificar(codigo_binario)
    print(f"\nTeste de integridade:")
    print(f"  Texto original == Decodificado: {texto == texto_decodificado}")


def benchmark_heaps():
    """Compara performance de heaps com outras estruturas."""
    print("\n=== BENCHMARK: HEAPS vs OUTRAS ESTRUTURAS ===\n")
    
    tamanhos = [1000, 5000, 10000]
    
    for n in tamanhos:
        print(f"Testando com {n} elementos:")
        
        # Preparar dados
        dados = list(range(n))
        random.shuffle(dados)
        
        # Min-Heap customizado
        start_time = time.time()
        min_heap = MinHeap()
        for valor in dados:
            min_heap.inserir(valor)
        
        # Extrair alguns elementos
        for _ in range(min(100, n)):
            if not min_heap.esta_vazio():
                min_heap.extrair_minimo()
        
        tempo_custom = time.time() - start_time
        
        # heapq do Python
        start_time = time.time()
        heap_python = []
        for valor in dados:
            heapq.heappush(heap_python, valor)
        
        # Extrair alguns elementos
        for _ in range(min(100, n)):
            if heap_python:
                heapq.heappop(heap_python)
        
        tempo_heapq = time.time() - start_time
        
        # Lista ordenada (para comparação)
        start_time = time.time()
        lista_ordenada = []
        for valor in dados:
            # Inserção ordenada (custosa)
            pos = 0
            while pos < len(lista_ordenada) and lista_ordenada[pos] < valor:
                pos += 1
            lista_ordenada.insert(pos, valor)
        
        # Extrair alguns elementos
        for _ in range(min(100, n)):
            if lista_ordenada:
                lista_ordenada.pop(0)  # Remove menor
        
        tempo_lista = time.time() - start_time
        
        print(f"  Heap customizado: {tempo_custom:.4f}s")
        print(f"  heapq Python:     {tempo_heapq:.4f}s")
        print(f"  Lista ordenada:   {tempo_lista:.4f}s")
        print(f"  Speedup vs lista: {tempo_lista/tempo_custom:.2f}x")
        print()
        
        # Teste específico: construção de heap
        print(f"  Teste de construção de heap:")
        
        # Construção O(n) vs inserções O(n log n)
        dados_construcao = list(range(n))
        random.shuffle(dados_construcao)
        
        # Construção O(n)
        start_time = time.time()
        heap_construido = MinHeap()
        heap_construido.construir_heap(dados_construcao)
        tempo_construcao = time.time() - start_time
        
        # Inserções O(n log n)
        start_time = time.time()
        heap_insercoes = MinHeap()
        for valor in dados_construcao:
            heap_insercoes.inserir(valor)
        tempo_insercoes = time.time() - start_time
        
        print(f"    Construção O(n):     {tempo_construcao:.4f}s")
        print(f"    Inserções O(n log n): {tempo_insercoes:.4f}s")
        print(f"    Speedup:             {tempo_insercoes/tempo_construcao:.2f}x")
        print()


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 05.6 - HEAPS E FILAS DE PRIORIDADE")
    print("=" * 50)
    
    demonstrar_min_max_heap()
    demonstrar_fila_prioridade()
    demonstrar_heap_sort()
    demonstrar_aplicacoes_praticas()
    benchmark_heaps()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 05.6")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. ESTRUTURA HEAP:
   • Árvore binária completa com propriedade de ordem
   • Representação eficiente em array
   • Operações O(log n) para inserção e extração
   • Construção O(n) quando feita corretamente

2. TIPOS DE HEAP:
   • Min-Heap: menor elemento na raiz
   • Max-Heap: maior elemento na raiz
   • Implementação similar, apenas comparação muda

3. OPERAÇÕES FUNDAMENTAIS:
   • Sift-up: move elemento para cima
   • Sift-down: move elemento para baixo
   • Heapify: mantém propriedade do heap
   • Peek: acesso O(1) ao elemento extremo

4. FILAS DE PRIORIDADE:
   • Implementação natural usando heaps
   • Processamento por prioridade, não por ordem de chegada
   • Desempate usando timestamp (FIFO para mesma prioridade)

5. HEAP SORT:
   • Algoritmo de ordenação O(n log n) garantido
   • Ordenação in-place
   • Não é estável, mas tem boa performance

6. APLICAÇÕES PRÁTICAS:
   • Escalonamento de processos
   • Algoritmos de compressão (Huffman)
   • Algoritmos de grafos (Dijkstra, Prim)
   • Sistemas de prioridade em geral

7. VANTAGENS DOS HEAPS:
   • Acesso O(1) ao elemento extremo
   • Inserção e remoção O(log n)
   • Uso eficiente de memória
   • Implementação simples com arrays

8. CONSIDERAÇÕES DE IMPLEMENTAÇÃO:
   • heapq do Python é muito otimizado
   • Construção O(n) é mais eficiente que n inserções
   • Heaps são ideais quando só precisamos do extremo
   • Para busca de elementos arbitrários, outras estruturas são melhores

Próximo módulo: Grafos - Conceitos Fundamentais
    """)


if __name__ == "__main__":
    main()