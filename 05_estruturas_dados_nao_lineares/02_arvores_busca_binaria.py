"""
=============================================================================
CURSO DE LÓGICA DE PROGRAMAÇÃO E ESTRUTURAS DE DADOS EM PYTHON
Professor: Especialista em Estruturas de Dados e Algoritmos

MÓDULO 05: ESTRUTURAS DE DADOS NÃO-LINEARES
Arquivo 05.2: Árvores de Busca Binária (BST)
=============================================================================

OBJETIVOS DE APRENDIZADO:
- Compreender as propriedades das Árvores de Busca Binária
- Implementar operações eficientes (busca, inserção, remoção)
- Analisar complexidade temporal e espacial das operações
- Aplicar BST em problemas práticos do mundo real
- Comparar BST com outras estruturas de dados

CONCEITOS ABORDADOS:
1. Propriedade fundamental da BST
2. Operações básicas otimizadas
3. Travessias específicas para BST
4. Validação de BST
5. Conversões e transformações
6. Aplicações práticas

PRÉ-REQUISITOS:
- Módulo 05.1 (Conceitos de Árvores)
- Conhecimento de recursão
- Compreensão de complexidade algorítmica

COMPLEXIDADE DAS OPERAÇÕES:
- Busca: O(log n) médio, O(n) pior caso
- Inserção: O(log n) médio, O(n) pior caso  
- Remoção: O(log n) médio, O(n) pior caso
- Travessia: O(n) sempre
- Espaço: O(n) para armazenamento, O(log n) para recursão
=============================================================================
"""

from typing import Optional, List, Tuple, Iterator, Any
from collections import deque
import time
import random
import sys

class NoBST:
    """
    Nó para Árvore de Busca Binária.
    
    Propriedades:
    - valor: dado armazenado no nó
    - esquerda: referência para subárvore esquerda (valores menores)
    - direita: referência para subárvore direita (valores maiores)
    - pai: referência para nó pai (opcional, para operações otimizadas)
    """
    
    def __init__(self, valor: Any, pai: Optional['NoBST'] = None):
        self.valor = valor
        self.esquerda: Optional['NoBST'] = None
        self.direita: Optional['NoBST'] = None
        self.pai = pai
    
    def eh_folha(self) -> bool:
        """Verifica se o nó é uma folha."""
        return self.esquerda is None and self.direita is None
    
    def tem_um_filho(self) -> bool:
        """Verifica se o nó tem exatamente um filho."""
        return (self.esquerda is None) != (self.direita is None)
    
    def tem_dois_filhos(self) -> bool:
        """Verifica se o nó tem dois filhos."""
        return self.esquerda is not None and self.direita is not None
    
    def obter_filho_unico(self) -> Optional['NoBST']:
        """Retorna o único filho do nó (se existir)."""
        return self.esquerda if self.esquerda else self.direita
    
    def eh_filho_esquerdo(self) -> bool:
        """Verifica se é filho esquerdo do pai."""
        return self.pai and self.pai.esquerda == self
    
    def eh_filho_direito(self) -> bool:
        """Verifica se é filho direito do pai."""
        return self.pai and self.pai.direita == self
    
    def __str__(self) -> str:
        return str(self.valor)
    
    def __repr__(self) -> str:
        return f"NoBST({self.valor})"

class ArvoreBuscaBinaria:
    """
    Implementação completa de Árvore de Busca Binária.
    
    Propriedade BST: Para cada nó N:
    - Todos os valores na subárvore esquerda são menores que N
    - Todos os valores na subárvore direita são maiores que N
    - Ambas as subárvores são BSTs válidas
    """
    
    def __init__(self):
        self.raiz: Optional[NoBST] = None
        self.tamanho = 0
        self._modificacoes = 0  # Para detectar modificações durante iteração
    
    def esta_vazia(self) -> bool:
        """Verifica se a árvore está vazia."""
        return self.raiz is None
    
    def obter_tamanho(self) -> int:
        """Retorna o número de elementos na árvore."""
        return self.tamanho
    
    # ========================================================================
    # OPERAÇÕES BÁSICAS
    # ========================================================================
    
    def buscar(self, valor: Any) -> Optional[NoBST]:
        """
        Busca um valor na BST.
        
        Complexidade: O(log n) médio, O(n) pior caso
        """
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, no: Optional[NoBST], valor: Any) -> Optional[NoBST]:
        """Implementação recursiva da busca."""
        if no is None or no.valor == valor:
            return no
        
        if valor < no.valor:
            return self._buscar_recursivo(no.esquerda, valor)
        else:
            return self._buscar_recursivo(no.direita, valor)
    
    def buscar_iterativo(self, valor: Any) -> Optional[NoBST]:
        """
        Busca iterativa (mais eficiente em memória).
        
        Complexidade: O(log n) médio, O(n) pior caso
        Espaço: O(1)
        """
        atual = self.raiz
        
        while atual is not None:
            if valor == atual.valor:
                return atual
            elif valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita
        
        return None
    
    def contem(self, valor: Any) -> bool:
        """Verifica se um valor existe na árvore."""
        return self.buscar(valor) is not None
    
    def inserir(self, valor: Any) -> bool:
        """
        Insere um valor na BST.
        
        Retorna True se inseriu, False se já existia.
        Complexidade: O(log n) médio, O(n) pior caso
        """
        if self.raiz is None:
            self.raiz = NoBST(valor)
            self.tamanho += 1
            self._modificacoes += 1
            return True
        
        return self._inserir_recursivo(self.raiz, valor)
    
    def _inserir_recursivo(self, no: NoBST, valor: Any) -> bool:
        """Implementação recursiva da inserção."""
        if valor == no.valor:
            return False  # Valor já existe
        
        if valor < no.valor:
            if no.esquerda is None:
                no.esquerda = NoBST(valor, no)
                self.tamanho += 1
                self._modificacoes += 1
                return True
            else:
                return self._inserir_recursivo(no.esquerda, valor)
        else:
            if no.direita is None:
                no.direita = NoBST(valor, no)
                self.tamanho += 1
                self._modificacoes += 1
                return True
            else:
                return self._inserir_recursivo(no.direita, valor)
    
    def remover(self, valor: Any) -> bool:
        """
        Remove um valor da BST.
        
        Retorna True se removeu, False se não encontrou.
        Complexidade: O(log n) médio, O(n) pior caso
        """
        no = self.buscar(valor)
        if no is None:
            return False
        
        self._remover_no(no)
        self.tamanho -= 1
        self._modificacoes += 1
        return True
    
    def _remover_no(self, no: NoBST) -> None:
        """
        Remove um nó específico da BST.
        
        Casos:
        1. Nó folha: simplesmente remove
        2. Nó com um filho: substitui pelo filho
        3. Nó com dois filhos: substitui pelo sucessor in-order
        """
        if no.eh_folha():
            self._remover_folha(no)
        elif no.tem_um_filho():
            self._remover_no_um_filho(no)
        else:
            self._remover_no_dois_filhos(no)
    
    def _remover_folha(self, no: NoBST) -> None:
        """Remove um nó folha."""
        if no == self.raiz:
            self.raiz = None
        elif no.eh_filho_esquerdo():
            no.pai.esquerda = None
        else:
            no.pai.direita = None
    
    def _remover_no_um_filho(self, no: NoBST) -> None:
        """Remove um nó com um filho."""
        filho = no.obter_filho_unico()
        
        if no == self.raiz:
            self.raiz = filho
            if filho:
                filho.pai = None
        elif no.eh_filho_esquerdo():
            no.pai.esquerda = filho
            if filho:
                filho.pai = no.pai
        else:
            no.pai.direita = filho
            if filho:
                filho.pai = no.pai
    
    def _remover_no_dois_filhos(self, no: NoBST) -> None:
        """Remove um nó com dois filhos usando sucessor in-order."""
        sucessor = self._encontrar_minimo(no.direita)
        no.valor = sucessor.valor
        self._remover_no(sucessor)
    
    # ========================================================================
    # OPERAÇÕES AUXILIARES
    # ========================================================================
    
    def encontrar_minimo(self) -> Optional[Any]:
        """Encontra o menor valor na árvore."""
        if self.raiz is None:
            return None
        return self._encontrar_minimo(self.raiz).valor
    
    def _encontrar_minimo(self, no: NoBST) -> NoBST:
        """Encontra o nó com menor valor a partir de um nó."""
        while no.esquerda is not None:
            no = no.esquerda
        return no
    
    def encontrar_maximo(self) -> Optional[Any]:
        """Encontra o maior valor na árvore."""
        if self.raiz is None:
            return None
        return self._encontrar_maximo(self.raiz).valor
    
    def _encontrar_maximo(self, no: NoBST) -> NoBST:
        """Encontra o nó com maior valor a partir de um nó."""
        while no.direita is not None:
            no = no.direita
        return no
    
    def encontrar_sucessor(self, valor: Any) -> Optional[Any]:
        """
        Encontra o sucessor in-order de um valor.
        
        O sucessor é o menor valor maior que o valor dado.
        """
        no = self.buscar(valor)
        if no is None:
            return None
        
        sucessor = self._encontrar_sucessor(no)
        return sucessor.valor if sucessor else None
    
    def _encontrar_sucessor(self, no: NoBST) -> Optional[NoBST]:
        """Encontra o sucessor in-order de um nó."""
        # Se tem subárvore direita, sucessor é o mínimo da direita
        if no.direita is not None:
            return self._encontrar_minimo(no.direita)
        
        # Senão, sobe até encontrar um ancestral que seja filho esquerdo
        atual = no
        while atual.pai is not None and atual.eh_filho_direito():
            atual = atual.pai
        
        return atual.pai
    
    def encontrar_predecessor(self, valor: Any) -> Optional[Any]:
        """
        Encontra o predecessor in-order de um valor.
        
        O predecessor é o maior valor menor que o valor dado.
        """
        no = self.buscar(valor)
        if no is None:
            return None
        
        predecessor = self._encontrar_predecessor(no)
        return predecessor.valor if predecessor else None
    
    def _encontrar_predecessor(self, no: NoBST) -> Optional[NoBST]:
        """Encontra o predecessor in-order de um nó."""
        # Se tem subárvore esquerda, predecessor é o máximo da esquerda
        if no.esquerda is not None:
            return self._encontrar_maximo(no.esquerda)
        
        # Senão, sobe até encontrar um ancestral que seja filho direito
        atual = no
        while atual.pai is not None and atual.eh_filho_esquerdo():
            atual = atual.pai
        
        return atual.pai
    
    # ========================================================================
    # TRAVESSIAS
    # ========================================================================
    
    def travessia_in_order(self) -> List[Any]:
        """
        Travessia in-order (esquerda, raiz, direita).
        
        Para BST, retorna valores em ordem crescente.
        Complexidade: O(n)
        """
        resultado = []
        self._in_order_recursivo(self.raiz, resultado)
        return resultado
    
    def _in_order_recursivo(self, no: Optional[NoBST], resultado: List[Any]) -> None:
        """Implementação recursiva da travessia in-order."""
        if no is not None:
            self._in_order_recursivo(no.esquerda, resultado)
            resultado.append(no.valor)
            self._in_order_recursivo(no.direita, resultado)
    
    def travessia_in_order_iterativa(self) -> List[Any]:
        """
        Travessia in-order iterativa usando pilha.
        
        Mais eficiente em memória para árvores desbalanceadas.
        """
        if self.raiz is None:
            return []
        
        resultado = []
        pilha = []
        atual = self.raiz
        
        while pilha or atual:
            # Vai para o nó mais à esquerda
            while atual:
                pilha.append(atual)
                atual = atual.esquerda
            
            # Processa o nó atual
            atual = pilha.pop()
            resultado.append(atual.valor)
            
            # Move para a subárvore direita
            atual = atual.direita
        
        return resultado
    
    def obter_valores_ordenados(self) -> List[Any]:
        """Retorna todos os valores em ordem crescente."""
        return self.travessia_in_order()
    
    def obter_valores_decrescentes(self) -> List[Any]:
        """Retorna todos os valores em ordem decrescente."""
        resultado = []
        self._travessia_reversa(self.raiz, resultado)
        return resultado
    
    def _travessia_reversa(self, no: Optional[NoBST], resultado: List[Any]) -> None:
        """Travessia in-order reversa (direita, raiz, esquerda)."""
        if no is not None:
            self._travessia_reversa(no.direita, resultado)
            resultado.append(no.valor)
            self._travessia_reversa(no.esquerda, resultado)
    
    # ========================================================================
    # VALIDAÇÃO E PROPRIEDADES
    # ========================================================================
    
    def eh_bst_valida(self) -> bool:
        """
        Verifica se a árvore é uma BST válida.
        
        Método eficiente usando limites min/max.
        """
        return self._eh_bst_valida_recursivo(self.raiz, float('-inf'), float('inf'))
    
    def _eh_bst_valida_recursivo(self, no: Optional[NoBST], min_val: float, max_val: float) -> bool:
        """Validação recursiva com limites."""
        if no is None:
            return True
        
        if no.valor <= min_val or no.valor >= max_val:
            return False
        
        return (self._eh_bst_valida_recursivo(no.esquerda, min_val, no.valor) and
                self._eh_bst_valida_recursivo(no.direita, no.valor, max_val))
    
    def calcular_altura(self) -> int:
        """Calcula a altura da árvore."""
        return self._calcular_altura_recursivo(self.raiz)
    
    def _calcular_altura_recursivo(self, no: Optional[NoBST]) -> int:
        """Cálculo recursivo da altura."""
        if no is None:
            return -1
        
        altura_esq = self._calcular_altura_recursivo(no.esquerda)
        altura_dir = self._calcular_altura_recursivo(no.direita)
        
        return 1 + max(altura_esq, altura_dir)
    
    def eh_balanceada(self) -> bool:
        """
        Verifica se a árvore está balanceada.
        
        Uma árvore é balanceada se a diferença de altura entre
        subárvores esquerda e direita é no máximo 1.
        """
        return self._verificar_balanceamento(self.raiz)[0]
    
    def _verificar_balanceamento(self, no: Optional[NoBST]) -> Tuple[bool, int]:
        """
        Verifica balanceamento e retorna (é_balanceada, altura).
        
        Otimização: calcula altura e verifica balanceamento em uma passada.
        """
        if no is None:
            return True, -1
        
        bal_esq, alt_esq = self._verificar_balanceamento(no.esquerda)
        if not bal_esq:
            return False, 0
        
        bal_dir, alt_dir = self._verificar_balanceamento(no.direita)
        if not bal_dir:
            return False, 0
        
        balanceada = abs(alt_esq - alt_dir) <= 1
        altura = 1 + max(alt_esq, alt_dir)
        
        return balanceada, altura
    
    # ========================================================================
    # OPERAÇÕES DE RANGE
    # ========================================================================
    
    def buscar_range(self, min_val: Any, max_val: Any) -> List[Any]:
        """
        Busca todos os valores em um intervalo [min_val, max_val].
        
        Complexidade: O(log n + k), onde k é o número de elementos no range.
        """
        resultado = []
        self._buscar_range_recursivo(self.raiz, min_val, max_val, resultado)
        return resultado
    
    def _buscar_range_recursivo(self, no: Optional[NoBST], min_val: Any, max_val: Any, resultado: List[Any]) -> None:
        """Busca recursiva em range."""
        if no is None:
            return
        
        # Se o valor atual está no range, adiciona ao resultado
        if min_val <= no.valor <= max_val:
            resultado.append(no.valor)
        
        # Recursão condicional para otimizar
        if no.valor > min_val:
            self._buscar_range_recursivo(no.esquerda, min_val, max_val, resultado)
        
        if no.valor < max_val:
            self._buscar_range_recursivo(no.direita, min_val, max_val, resultado)
    
    def contar_menores_que(self, valor: Any) -> int:
        """Conta quantos valores são menores que o valor dado."""
        return self._contar_menores_recursivo(self.raiz, valor)
    
    def _contar_menores_recursivo(self, no: Optional[NoBST], valor: Any) -> int:
        """Contagem recursiva de valores menores."""
        if no is None:
            return 0
        
        if no.valor < valor:
            # Conta o nó atual + toda subárvore esquerda + parte da direita
            return 1 + self._contar_nos(no.esquerda) + self._contar_menores_recursivo(no.direita, valor)
        else:
            # Só conta na subárvore esquerda
            return self._contar_menores_recursivo(no.esquerda, valor)
    
    def _contar_nos(self, no: Optional[NoBST]) -> int:
        """Conta o número de nós em uma subárvore."""
        if no is None:
            return 0
        return 1 + self._contar_nos(no.esquerda) + self._contar_nos(no.direita)
    
    # ========================================================================
    # CONVERSÕES E TRANSFORMAÇÕES
    # ========================================================================
    
    def para_lista_ordenada(self) -> List[Any]:
        """Converte a BST para uma lista ordenada."""
        return self.travessia_in_order()
    
    def para_array_balanceado(self) -> List[Any]:
        """
        Converte para array que representa uma árvore balanceada.
        
        Útil para serialização ou conversão para heap.
        """
        valores = self.travessia_in_order()
        if not valores:
            return []
        
        # Reconstrói como árvore balanceada
        bst_temp = ArvoreBuscaBinaria()
        bst_temp._construir_balanceada(valores, 0, len(valores) - 1)
        
        # Retorna em level-order
        return bst_temp._travessia_level_order()
    
    def _construir_balanceada(self, valores: List[Any], inicio: int, fim: int) -> Optional[NoBST]:
        """Constrói BST balanceada a partir de array ordenado."""
        if inicio > fim:
            return None
        
        meio = (inicio + fim) // 2
        no = NoBST(valores[meio])
        
        if self.raiz is None:
            self.raiz = no
        
        no.esquerda = self._construir_balanceada(valores, inicio, meio - 1)
        if no.esquerda:
            no.esquerda.pai = no
        
        no.direita = self._construir_balanceada(valores, meio + 1, fim)
        if no.direita:
            no.direita.pai = no
        
        return no
    
    def _travessia_level_order(self) -> List[Any]:
        """Travessia por níveis."""
        if self.raiz is None:
            return []
        
        resultado = []
        fila = deque([self.raiz])
        
        while fila:
            no = fila.popleft()
            resultado.append(no.valor)
            
            if no.esquerda:
                fila.append(no.esquerda)
            if no.direita:
                fila.append(no.direita)
        
        return resultado
    
    # ========================================================================
    # VISUALIZAÇÃO E DEBUG
    # ========================================================================
    
    def imprimir_arvore(self) -> None:
        """Imprime a árvore de forma visual."""
        if self.raiz is None:
            print("Árvore vazia")
            return
        
        linhas = self._gerar_representacao_visual(self.raiz)
        for linha in linhas:
            print(linha)
    
    def _gerar_representacao_visual(self, no: NoBST, prefixo: str = "", eh_ultimo: bool = True) -> List[str]:
        """Gera representação visual da árvore."""
        linhas = []
        
        if no is not None:
            # Linha atual
            conector = "└── " if eh_ultimo else "├── "
            linhas.append(prefixo + conector + str(no.valor))
            
            # Prepara prefixo para filhos
            novo_prefixo = prefixo + ("    " if eh_ultimo else "│   ")
            
            # Adiciona filhos (direita primeiro para visualização melhor)
            filhos = []
            if no.esquerda is not None:
                filhos.append(('esq', no.esquerda))
            if no.direita is not None:
                filhos.append(('dir', no.direita))
            
            for i, (lado, filho) in enumerate(filhos):
                eh_ultimo_filho = (i == len(filhos) - 1)
                linhas_filho = self._gerar_representacao_visual(filho, novo_prefixo, eh_ultimo_filho)
                linhas.extend(linhas_filho)
        
        return linhas
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas detalhadas da árvore."""
        if self.raiz is None:
            return {
                'tamanho': 0,
                'altura': -1,
                'eh_balanceada': True,
                'eh_bst_valida': True,
                'minimo': None,
                'maximo': None,
                'folhas': 0,
                'nos_internos': 0
            }
        
        return {
            'tamanho': self.tamanho,
            'altura': self.calcular_altura(),
            'eh_balanceada': self.eh_balanceada(),
            'eh_bst_valida': self.eh_bst_valida(),
            'minimo': self.encontrar_minimo(),
            'maximo': self.encontrar_maximo(),
            'folhas': self._contar_folhas(self.raiz),
            'nos_internos': self.tamanho - self._contar_folhas(self.raiz)
        }
    
    def _contar_folhas(self, no: Optional[NoBST]) -> int:
        """Conta o número de folhas na árvore."""
        if no is None:
            return 0
        if no.eh_folha():
            return 1
        return self._contar_folhas(no.esquerda) + self._contar_folhas(no.direita)
    
    # ========================================================================
    # ITERADORES
    # ========================================================================
    
    def __iter__(self) -> Iterator[Any]:
        """Permite iteração sobre a BST em ordem crescente."""
        modificacoes_iniciais = self._modificacoes
        
        def gerador():
            if self.raiz is None:
                return
            
            pilha = []
            atual = self.raiz
            
            while pilha or atual:
                if self._modificacoes != modificacoes_iniciais:
                    raise RuntimeError("BST foi modificada durante iteração")
                
                while atual:
                    pilha.append(atual)
                    atual = atual.esquerda
                
                atual = pilha.pop()
                yield atual.valor
                atual = atual.direita
        
        return gerador()
    
    def __contains__(self, valor: Any) -> bool:
        """Permite usar 'in' para verificar se valor existe."""
        return self.contem(valor)
    
    def __len__(self) -> int:
        """Retorna o tamanho da árvore."""
        return self.tamanho
    
    def __str__(self) -> str:
        """Representação string da árvore."""
        if self.raiz is None:
            return "BST(vazia)"
        
        valores = self.travessia_in_order()
        return f"BST({valores})"
    
    def __repr__(self) -> str:
        return self.__str__()

# ============================================================================
# APLICAÇÕES PRÁTICAS
# ============================================================================

class IndiceOrdenado:
    """
    Índice ordenado usando BST para busca eficiente.
    
    Aplicação: Sistema de banco de dados, catálogo de produtos.
    """
    
    def __init__(self):
        self.bst = ArvoreBuscaBinaria()
        self.dados = {}  # Mapeia chave -> dados completos
    
    def inserir(self, chave: Any, dados: Any) -> bool:
        """Insere um registro no índice."""
        if self.bst.inserir(chave):
            self.dados[chave] = dados
            return True
        return False
    
    def buscar(self, chave: Any) -> Optional[Any]:
        """Busca um registro pela chave."""
        if self.bst.contem(chave):
            return self.dados[chave]
        return None
    
    def remover(self, chave: Any) -> bool:
        """Remove um registro do índice."""
        if self.bst.remover(chave):
            del self.dados[chave]
            return True
        return False
    
    def buscar_range(self, min_chave: Any, max_chave: Any) -> List[Tuple[Any, Any]]:
        """Busca registros em um intervalo de chaves."""
        chaves = self.bst.buscar_range(min_chave, max_chave)
        return [(chave, self.dados[chave]) for chave in chaves]
    
    def obter_todos_ordenados(self) -> List[Tuple[Any, Any]]:
        """Retorna todos os registros ordenados por chave."""
        chaves = self.bst.obter_valores_ordenados()
        return [(chave, self.dados[chave]) for chave in chaves]

class ValidadorExpressao:
    """
    Validador de expressões usando BST para símbolos válidos.
    
    Aplicação: Compiladores, interpretadores, validação de entrada.
    """
    
    def __init__(self):
        self.simbolos_validos = ArvoreBuscaBinaria()
        self.operadores = ArvoreBuscaBinaria()
        self.palavras_reservadas = ArvoreBuscaBinaria()
    
    def adicionar_simbolo(self, simbolo: str) -> None:
        """Adiciona um símbolo válido."""
        self.simbolos_validos.inserir(simbolo)
    
    def adicionar_operador(self, operador: str) -> None:
        """Adiciona um operador válido."""
        self.operadores.inserir(operador)
    
    def adicionar_palavra_reservada(self, palavra: str) -> None:
        """Adiciona uma palavra reservada."""
        self.palavras_reservadas.inserir(palavra)
    
    def eh_simbolo_valido(self, simbolo: str) -> bool:
        """Verifica se um símbolo é válido."""
        return simbolo in self.simbolos_validos
    
    def eh_operador(self, token: str) -> bool:
        """Verifica se um token é um operador."""
        return token in self.operadores
    
    def eh_palavra_reservada(self, palavra: str) -> bool:
        """Verifica se uma palavra é reservada."""
        return palavra in self.palavras_reservadas
    
    def validar_tokens(self, tokens: List[str]) -> Tuple[bool, List[str]]:
        """
        Valida uma lista de tokens.
        
        Retorna (é_válido, lista_de_erros).
        """
        erros = []
        
        for i, token in enumerate(tokens):
            if not (self.eh_simbolo_valido(token) or 
                   self.eh_operador(token) or 
                   self.eh_palavra_reservada(token)):
                erros.append(f"Token inválido '{token}' na posição {i}")
        
        return len(erros) == 0, erros

# ============================================================================
# FUNÇÕES DE DEMONSTRAÇÃO E BENCHMARK
# ============================================================================

def demonstrar_bst_basica():
    """Demonstra operações básicas da BST."""
    print("=== DEMONSTRAÇÃO: BST Básica ===")
    
    bst = ArvoreBuscaBinaria()
    valores = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    
    print("Inserindo valores:", valores)
    for valor in valores:
        bst.inserir(valor)
    
    print(f"\nTamanho da árvore: {len(bst)}")
    print("Árvore:")
    bst.imprimir_arvore()
    
    print(f"\nValores em ordem: {bst.obter_valores_ordenados()}")
    print(f"Valores decrescentes: {bst.obter_valores_decrescentes()}")
    
    print(f"\nMínimo: {bst.encontrar_minimo()}")
    print(f"Máximo: {bst.encontrar_maximo()}")
    
    valor_teste = 40
    print(f"\nSucessor de {valor_teste}: {bst.encontrar_sucessor(valor_teste)}")
    print(f"Predecessor de {valor_teste}: {bst.encontrar_predecessor(valor_teste)}")
    
    print(f"\nBuscar range [25, 65]: {bst.buscar_range(25, 65)}")
    print(f"Valores menores que 50: {bst.contar_menores_que(50)}")
    
    print("\nEstatísticas:")
    stats = bst.obter_estatisticas()
    for chave, valor in stats.items():
        print(f"  {chave}: {valor}")

def demonstrar_operacoes_avancadas():
    """Demonstra operações avançadas da BST."""
    print("\n=== DEMONSTRAÇÃO: Operações Avançadas ===")
    
    bst = ArvoreBuscaBinaria()
    
    # Cria árvore desbalanceada
    print("Criando árvore desbalanceada (inserção sequencial):")
    for i in range(1, 8):
        bst.inserir(i)
    
    print("Árvore desbalanceada:")
    bst.imprimir_arvore()
    
    stats = bst.obter_estatisticas()
    print(f"Altura: {stats['altura']}, Balanceada: {stats['eh_balanceada']}")
    
    # Converte para array balanceado e reconstrói
    print("\nConvertendo para árvore balanceada:")
    valores = bst.para_lista_ordenada()
    
    bst_balanceada = ArvoreBuscaBinaria()
    bst_balanceada._construir_balanceada(valores, 0, len(valores) - 1)
    bst_balanceada.tamanho = len(valores)
    
    print("Árvore balanceada:")
    bst_balanceada.imprimir_arvore()
    
    stats_bal = bst_balanceada.obter_estatisticas()
    print(f"Altura: {stats_bal['altura']}, Balanceada: {stats_bal['eh_balanceada']}")

def demonstrar_aplicacoes_praticas():
    """Demonstra aplicações práticas da BST."""
    print("\n=== DEMONSTRAÇÃO: Aplicações Práticas ===")
    
    # Índice ordenado
    print("1. Índice Ordenado (Catálogo de Produtos):")
    catalogo = IndiceOrdenado()
    
    produtos = [
        (100, {"nome": "Notebook", "preco": 2500.00}),
        (50, {"nome": "Mouse", "preco": 25.00}),
        (200, {"nome": "Monitor", "preco": 800.00}),
        (75, {"nome": "Teclado", "preco": 150.00}),
        (150, {"nome": "Impressora", "preco": 400.00})
    ]
    
    for codigo, dados in produtos:
        catalogo.inserir(codigo, dados)
    
    print("Produtos ordenados por código:")
    for codigo, dados in catalogo.obter_todos_ordenados():
        print(f"  {codigo}: {dados['nome']} - R$ {dados['preco']}")
    
    print(f"\nBuscar produto 75: {catalogo.buscar(75)}")
    print(f"Produtos na faixa 60-120:")
    for codigo, dados in catalogo.buscar_range(60, 120):
        print(f"  {codigo}: {dados['nome']}")
    
    # Validador de expressão
    print("\n2. Validador de Expressão:")
    validador = ValidadorExpressao()
    
    # Configura símbolos válidos
    for simbolo in ['x', 'y', 'z', 'a', 'b', 'c']:
        validador.adicionar_simbolo(simbolo)
    
    for op in ['+', '-', '*', '/', '(', ')']:
        validador.adicionar_operador(op)
    
    for palavra in ['if', 'else', 'while', 'for']:
        validador.adicionar_palavra_reservada(palavra)
    
    # Testa expressões
    expressoes = [
        ['x', '+', 'y', '*', 'z'],  # Válida
        ['if', '(', 'x', '>', 'y', ')'],  # Válida
        ['x', '+', 'invalid_token', '*', 'y'],  # Inválida
    ]
    
    for expr in expressoes:
        valida, erros = validador.validar_tokens(expr)
        print(f"Expressão {expr}: {'Válida' if valida else 'Inválida'}")
        if erros:
            for erro in erros:
                print(f"  Erro: {erro}")

def benchmark_bst_vs_lista():
    """Compara performance da BST com lista Python."""
    print("\n=== BENCHMARK: BST vs Lista Python ===")
    
    tamanhos = [1000, 5000, 10000]
    
    for n in tamanhos:
        print(f"\nTamanho: {n} elementos")
        
        # Gera dados aleatórios
        dados = random.sample(range(n * 10), n)
        
        # Teste BST
        bst = ArvoreBuscaBinaria()
        
        inicio = time.time()
        for valor in dados:
            bst.inserir(valor)
        tempo_insercao_bst = time.time() - inicio
        
        inicio = time.time()
        for _ in range(100):
            valor = random.choice(dados)
            bst.buscar(valor)
        tempo_busca_bst = time.time() - inicio
        
        # Teste Lista
        lista = []
        
        inicio = time.time()
        for valor in dados:
            lista.append(valor)
        lista.sort()
        tempo_insercao_lista = time.time() - inicio
        
        inicio = time.time()
        for _ in range(100):
            valor = random.choice(dados)
            # Busca binária na lista ordenada
            esquerda, direita = 0, len(lista) - 1
            while esquerda <= direita:
                meio = (esquerda + direita) // 2
                if lista[meio] == valor:
                    break
                elif lista[meio] < valor:
                    esquerda = meio + 1
                else:
                    direita = meio - 1
        tempo_busca_lista = time.time() - inicio
        
        print(f"  Inserção + Ordenação:")
        print(f"    BST: {tempo_insercao_bst:.4f}s")
        print(f"    Lista: {tempo_insercao_lista:.4f}s")
        print(f"  Busca (100 operações):")
        print(f"    BST: {tempo_busca_bst:.4f}s")
        print(f"    Lista: {tempo_busca_lista:.4f}s")
        
        # Uso de memória (aproximado)
        memoria_bst = sys.getsizeof(bst) + n * sys.getsizeof(NoBST(0))
        memoria_lista = sys.getsizeof(lista) + n * sys.getsizeof(0)
        
        print(f"  Uso de memória (aproximado):")
        print(f"    BST: {memoria_bst} bytes")
        print(f"    Lista: {memoria_lista} bytes")

def main():
    """Função principal para demonstrar todos os conceitos."""
    print("MÓDULO 05.2: ÁRVORES DE BUSCA BINÁRIA (BST)")
    print("=" * 60)
    
    demonstrar_bst_basica()
    demonstrar_operacoes_avancadas()
    demonstrar_aplicacoes_praticas()
    benchmark_bst_vs_lista()
    
    print("\n" + "=" * 60)
    print("CONCLUSÃO DO MÓDULO 05.2")
    print("=" * 60)
    print("""
    Neste módulo, exploramos as Árvores de Busca Binária (BST):
    
    ✅ CONCEITOS FUNDAMENTAIS:
    • Propriedade BST: esquerda < raiz < direita
    • Operações básicas: busca, inserção, remoção
    • Complexidade: O(log n) médio, O(n) pior caso
    
    ✅ IMPLEMENTAÇÕES AVANÇADAS:
    • Busca iterativa e recursiva
    • Remoção com três casos distintos
    • Travessias otimizadas (in-order, reversa)
    • Operações de range eficientes
    
    ✅ VALIDAÇÃO E PROPRIEDADES:
    • Verificação de BST válida
    • Análise de balanceamento
    • Cálculo de estatísticas
    • Conversões e transformações
    
    ✅ APLICAÇÕES PRÁTICAS:
    • Índices ordenados para bancos de dados
    • Validadores de expressões
    • Catálogos de produtos
    • Sistemas de busca eficiente
    
    ✅ ANÁLISE DE PERFORMANCE:
    • Comparação com listas ordenadas
    • Análise de uso de memória
    • Identificação de casos de uso ideais
    
    🎯 PRÓXIMO MÓDULO: 05.3 - Árvores AVL (Auto-balanceadas)
    """)

if __name__ == "__main__":
    main()