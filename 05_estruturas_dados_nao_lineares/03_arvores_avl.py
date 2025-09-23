"""
=============================================================================
CURSO DE LÓGICA DE PROGRAMAÇÃO E ESTRUTURAS DE DADOS EM PYTHON
Professor: Especialista em Estruturas de Dados e Algoritmos

MÓDULO 05: ESTRUTURAS DE DADOS NÃO-LINEARES
Arquivo 05.3: Árvores AVL (Auto-balanceadas)
=============================================================================

OBJETIVOS DE APRENDIZADO:
- Compreender o conceito de árvores auto-balanceadas
- Implementar rotações simples e duplas
- Analisar fatores de balanceamento
- Garantir complexidade O(log n) para todas as operações
- Comparar AVL com BST comum e outras estruturas

CONCEITOS ABORDADOS:
1. Propriedade AVL e fator de balanceamento
2. Rotações: simples à esquerda/direita, duplas
3. Inserção com rebalanceamento automático
4. Remoção com rebalanceamento automático
5. Análise de altura e complexidade
6. Aplicações práticas de árvores balanceadas

PRÉ-REQUISITOS:
- Módulo 05.2 (Árvores de Busca Binária)
- Compreensão de rotações em árvores
- Análise de complexidade algorítmica

COMPLEXIDADE DAS OPERAÇÕES (GARANTIDA):
- Busca: O(log n) sempre
- Inserção: O(log n) sempre
- Remoção: O(log n) sempre
- Espaço: O(n) para armazenamento
- Altura máxima: 1.44 * log₂(n)
=============================================================================
"""

from typing import Optional, List, Tuple, Any
import math
import time
import random

class NoAVL:
    """
    Nó para Árvore AVL.
    
    Além dos campos básicos de BST, mantém:
    - altura: altura do nó na árvore
    - fator_balanceamento: diferença entre altura das subárvores
    """
    
    def __init__(self, valor: Any):
        self.valor = valor
        self.esquerda: Optional['NoAVL'] = None
        self.direita: Optional['NoAVL'] = None
        self.altura = 0
        self.fator_balanceamento = 0
    
    def eh_folha(self) -> bool:
        """Verifica se o nó é uma folha."""
        return self.esquerda is None and self.direita is None
    
    def tem_filho_esquerdo(self) -> bool:
        """Verifica se tem filho esquerdo."""
        return self.esquerda is not None
    
    def tem_filho_direito(self) -> bool:
        """Verifica se tem filho direito."""
        return self.direita is not None
    
    def tem_ambos_filhos(self) -> bool:
        """Verifica se tem ambos os filhos."""
        return self.esquerda is not None and self.direita is not None
    
    def obter_altura_esquerda(self) -> int:
        """Retorna altura da subárvore esquerda."""
        return self.esquerda.altura if self.esquerda else -1
    
    def obter_altura_direita(self) -> int:
        """Retorna altura da subárvore direita."""
        return self.direita.altura if self.direita else -1
    
    def calcular_altura(self) -> int:
        """Calcula e atualiza a altura do nó."""
        altura_esq = self.obter_altura_esquerda()
        altura_dir = self.obter_altura_direita()
        self.altura = 1 + max(altura_esq, altura_dir)
        return self.altura
    
    def calcular_fator_balanceamento(self) -> int:
        """
        Calcula e atualiza o fator de balanceamento.
        
        Fator = altura_esquerda - altura_direita
        - Positivo: árvore pende para esquerda
        - Negativo: árvore pende para direita
        - Zero: perfeitamente balanceada
        """
        altura_esq = self.obter_altura_esquerda()
        altura_dir = self.obter_altura_direita()
        self.fator_balanceamento = altura_esq - altura_dir
        return self.fator_balanceamento
    
    def atualizar_metricas(self) -> None:
        """Atualiza altura e fator de balanceamento."""
        self.calcular_altura()
        self.calcular_fator_balanceamento()
    
    def esta_desbalanceado(self) -> bool:
        """Verifica se o nó está desbalanceado (|fator| > 1)."""
        return abs(self.fator_balanceamento) > 1
    
    def tipo_desbalanceamento(self) -> str:
        """
        Identifica o tipo de desbalanceamento.
        
        Retorna:
        - 'LL': Left-Left (rotação simples à direita)
        - 'RR': Right-Right (rotação simples à esquerda)
        - 'LR': Left-Right (rotação dupla: esq-dir)
        - 'RL': Right-Left (rotação dupla: dir-esq)
        - 'BALANCED': balanceado
        """
        if not self.esta_desbalanceado():
            return 'BALANCED'
        
        if self.fator_balanceamento > 1:  # Pende para esquerda
            if self.esquerda and self.esquerda.fator_balanceamento >= 0:
                return 'LL'  # Left-Left
            else:
                return 'LR'  # Left-Right
        else:  # Pende para direita
            if self.direita and self.direita.fator_balanceamento <= 0:
                return 'RR'  # Right-Right
            else:
                return 'RL'  # Right-Left
    
    def __str__(self) -> str:
        return f"{self.valor}(h:{self.altura},fb:{self.fator_balanceamento})"
    
    def __repr__(self) -> str:
        return f"NoAVL({self.valor})"

class ArvoreAVL:
    """
    Implementação completa de Árvore AVL (Adelson-Velsky e Landis).
    
    Propriedades AVL:
    1. É uma BST válida
    2. Para cada nó, |altura_esquerda - altura_direita| ≤ 1
    3. Ambas as subárvores são AVL válidas
    
    Garante O(log n) para todas as operações através de rebalanceamento automático.
    """
    
    def __init__(self):
        self.raiz: Optional[NoAVL] = None
        self.tamanho = 0
        self._rotacoes_realizadas = 0  # Para estatísticas
        self._tipos_rotacao = {'LL': 0, 'RR': 0, 'LR': 0, 'RL': 0}
    
    def esta_vazia(self) -> bool:
        """Verifica se a árvore está vazia."""
        return self.raiz is None
    
    def obter_tamanho(self) -> int:
        """Retorna o número de elementos na árvore."""
        return self.tamanho
    
    def obter_altura(self) -> int:
        """Retorna a altura da árvore."""
        return self.raiz.altura if self.raiz else -1
    
    # ========================================================================
    # ROTAÇÕES - OPERAÇÕES FUNDAMENTAIS PARA BALANCEAMENTO
    # ========================================================================
    
    def rotacao_simples_direita(self, no: NoAVL) -> NoAVL:
        """
        Rotação simples à direita (para corrigir desbalanceamento LL).
        
        Antes:     y              Depois:    x
                  / \                       / \
                 x   C                     A   y
                / \                           / \
               A   B                         B   C
        
        Complexidade: O(1)
        """
        # Guarda referências
        nova_raiz = no.esquerda
        no.esquerda = nova_raiz.direita
        nova_raiz.direita = no
        
        # Atualiza métricas (ordem importa!)
        no.atualizar_metricas()
        nova_raiz.atualizar_metricas()
        
        # Estatísticas
        self._rotacoes_realizadas += 1
        self._tipos_rotacao['LL'] += 1
        
        return nova_raiz
    
    def rotacao_simples_esquerda(self, no: NoAVL) -> NoAVL:
        """
        Rotação simples à esquerda (para corrigir desbalanceamento RR).
        
        Antes:   x                Depois:      y
                / \                           / \
               A   y                         x   C
                  / \                       / \
                 B   C                     A   B
        
        Complexidade: O(1)
        """
        # Guarda referências
        nova_raiz = no.direita
        no.direita = nova_raiz.esquerda
        nova_raiz.esquerda = no
        
        # Atualiza métricas (ordem importa!)
        no.atualizar_metricas()
        nova_raiz.atualizar_metricas()
        
        # Estatísticas
        self._rotacoes_realizadas += 1
        self._tipos_rotacao['RR'] += 1
        
        return nova_raiz
    
    def rotacao_dupla_esquerda_direita(self, no: NoAVL) -> NoAVL:
        """
        Rotação dupla esquerda-direita (para corrigir desbalanceamento LR).
        
        Primeiro: rotação esquerda no filho esquerdo
        Segundo: rotação direita no nó atual
        
        Complexidade: O(1)
        """
        # Primeira rotação: esquerda no filho esquerdo
        no.esquerda = self.rotacao_simples_esquerda(no.esquerda)
        
        # Segunda rotação: direita no nó atual
        resultado = self.rotacao_simples_direita(no)
        
        # Ajusta estatísticas (já contadas nas rotações simples)
        self._tipos_rotacao['LL'] -= 1  # Remove contagem da rotação direita
        self._tipos_rotacao['RR'] -= 1  # Remove contagem da rotação esquerda
        self._tipos_rotacao['LR'] += 1  # Adiciona contagem da rotação dupla
        
        return resultado
    
    def rotacao_dupla_direita_esquerda(self, no: NoAVL) -> NoAVL:
        """
        Rotação dupla direita-esquerda (para corrigir desbalanceamento RL).
        
        Primeiro: rotação direita no filho direito
        Segundo: rotação esquerda no nó atual
        
        Complexidade: O(1)
        """
        # Primeira rotação: direita no filho direito
        no.direita = self.rotacao_simples_direita(no.direita)
        
        # Segunda rotação: esquerda no nó atual
        resultado = self.rotacao_simples_esquerda(no)
        
        # Ajusta estatísticas (já contadas nas rotações simples)
        self._tipos_rotacao['RR'] -= 1  # Remove contagem da rotação esquerda
        self._tipos_rotacao['LL'] -= 1  # Remove contagem da rotação direita
        self._tipos_rotacao['RL'] += 1  # Adiciona contagem da rotação dupla
        
        return resultado
    
    def rebalancear(self, no: NoAVL) -> NoAVL:
        """
        Rebalanceia um nó se necessário.
        
        Identifica o tipo de desbalanceamento e aplica a rotação apropriada.
        """
        if not no.esta_desbalanceado():
            return no
        
        tipo = no.tipo_desbalanceamento()
        
        if tipo == 'LL':
            return self.rotacao_simples_direita(no)
        elif tipo == 'RR':
            return self.rotacao_simples_esquerda(no)
        elif tipo == 'LR':
            return self.rotacao_dupla_esquerda_direita(no)
        elif tipo == 'RL':
            return self.rotacao_dupla_direita_esquerda(no)
        
        return no  # Não deveria chegar aqui
    
    # ========================================================================
    # OPERAÇÕES BÁSICAS COM REBALANCEAMENTO AUTOMÁTICO
    # ========================================================================
    
    def buscar(self, valor: Any) -> Optional[NoAVL]:
        """
        Busca um valor na árvore AVL.
        
        Complexidade: O(log n) garantida
        """
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, no: Optional[NoAVL], valor: Any) -> Optional[NoAVL]:
        """Implementação recursiva da busca."""
        if no is None or no.valor == valor:
            return no
        
        if valor < no.valor:
            return self._buscar_recursivo(no.esquerda, valor)
        else:
            return self._buscar_recursivo(no.direita, valor)
    
    def contem(self, valor: Any) -> bool:
        """Verifica se um valor existe na árvore."""
        return self.buscar(valor) is not None
    
    def inserir(self, valor: Any) -> bool:
        """
        Insere um valor na árvore AVL com rebalanceamento automático.
        
        Complexidade: O(log n) garantida
        """
        tamanho_inicial = self.tamanho
        self.raiz = self._inserir_recursivo(self.raiz, valor)
        return self.tamanho > tamanho_inicial
    
    def _inserir_recursivo(self, no: Optional[NoAVL], valor: Any) -> NoAVL:
        """
        Inserção recursiva com rebalanceamento.
        
        Passos:
        1. Inserção BST normal
        2. Atualização de métricas
        3. Rebalanceamento se necessário
        """
        # Passo 1: Inserção BST normal
        if no is None:
            self.tamanho += 1
            return NoAVL(valor)
        
        if valor < no.valor:
            no.esquerda = self._inserir_recursivo(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self._inserir_recursivo(no.direita, valor)
        else:
            # Valor já existe, não insere
            return no
        
        # Passo 2: Atualiza métricas
        no.atualizar_metricas()
        
        # Passo 3: Rebalanceia se necessário
        return self.rebalancear(no)
    
    def remover(self, valor: Any) -> bool:
        """
        Remove um valor da árvore AVL com rebalanceamento automático.
        
        Complexidade: O(log n) garantida
        """
        tamanho_inicial = self.tamanho
        self.raiz = self._remover_recursivo(self.raiz, valor)
        return self.tamanho < tamanho_inicial
    
    def _remover_recursivo(self, no: Optional[NoAVL], valor: Any) -> Optional[NoAVL]:
        """
        Remoção recursiva com rebalanceamento.
        
        Passos:
        1. Remoção BST normal
        2. Atualização de métricas
        3. Rebalanceamento se necessário
        """
        # Passo 1: Remoção BST normal
        if no is None:
            return None
        
        if valor < no.valor:
            no.esquerda = self._remover_recursivo(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self._remover_recursivo(no.direita, valor)
        else:
            # Nó encontrado, remove
            self.tamanho -= 1
            
            # Caso 1: Nó folha ou com um filho
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            
            # Caso 2: Nó com dois filhos
            # Encontra o sucessor (menor valor na subárvore direita)
            sucessor = self._encontrar_minimo(no.direita)
            no.valor = sucessor.valor
            no.direita = self._remover_recursivo(no.direita, sucessor.valor)
        
        # Passo 2: Atualiza métricas
        no.atualizar_metricas()
        
        # Passo 3: Rebalanceia se necessário
        return self.rebalancear(no)
    
    def _encontrar_minimo(self, no: NoAVL) -> NoAVL:
        """Encontra o nó com menor valor a partir de um nó."""
        while no.esquerda is not None:
            no = no.esquerda
        return no
    
    def _encontrar_maximo(self, no: NoAVL) -> NoAVL:
        """Encontra o nó com maior valor a partir de um nó."""
        while no.direita is not None:
            no = no.direita
        return no
    
    # ========================================================================
    # OPERAÇÕES DE CONSULTA
    # ========================================================================
    
    def encontrar_minimo(self) -> Optional[Any]:
        """Encontra o menor valor na árvore."""
        if self.raiz is None:
            return None
        return self._encontrar_minimo(self.raiz).valor
    
    def encontrar_maximo(self) -> Optional[Any]:
        """Encontra o maior valor na árvore."""
        if self.raiz is None:
            return None
        return self._encontrar_maximo(self.raiz).valor
    
    def travessia_in_order(self) -> List[Any]:
        """Travessia in-order (valores em ordem crescente)."""
        resultado = []
        self._in_order_recursivo(self.raiz, resultado)
        return resultado
    
    def _in_order_recursivo(self, no: Optional[NoAVL], resultado: List[Any]) -> None:
        """Implementação recursiva da travessia in-order."""
        if no is not None:
            self._in_order_recursivo(no.esquerda, resultado)
            resultado.append(no.valor)
            self._in_order_recursivo(no.direita, resultado)
    
    def buscar_range(self, min_val: Any, max_val: Any) -> List[Any]:
        """Busca todos os valores em um intervalo."""
        resultado = []
        self._buscar_range_recursivo(self.raiz, min_val, max_val, resultado)
        return resultado
    
    def _buscar_range_recursivo(self, no: Optional[NoAVL], min_val: Any, max_val: Any, resultado: List[Any]) -> None:
        """Busca recursiva em range."""
        if no is None:
            return
        
        if min_val <= no.valor <= max_val:
            resultado.append(no.valor)
        
        if no.valor > min_val:
            self._buscar_range_recursivo(no.esquerda, min_val, max_val, resultado)
        
        if no.valor < max_val:
            self._buscar_range_recursivo(no.direita, min_val, max_val, resultado)
    
    # ========================================================================
    # VALIDAÇÃO E PROPRIEDADES AVL
    # ========================================================================
    
    def eh_avl_valida(self) -> bool:
        """
        Verifica se a árvore é uma AVL válida.
        
        Verifica:
        1. Propriedade BST
        2. Propriedade AVL (balanceamento)
        3. Consistência das métricas
        """
        return (self._eh_bst_valida(self.raiz, float('-inf'), float('inf')) and
                self._eh_balanceamento_valido(self.raiz)[0] and
                self._metricas_consistentes(self.raiz))
    
    def _eh_bst_valida(self, no: Optional[NoAVL], min_val: float, max_val: float) -> bool:
        """Verifica propriedade BST."""
        if no is None:
            return True
        
        if no.valor <= min_val or no.valor >= max_val:
            return False
        
        return (self._eh_bst_valida(no.esquerda, min_val, no.valor) and
                self._eh_bst_valida(no.direita, no.valor, max_val))
    
    def _eh_balanceamento_valido(self, no: Optional[NoAVL]) -> Tuple[bool, int]:
        """
        Verifica propriedade AVL e retorna (é_válida, altura).
        
        Uma árvore AVL é válida se:
        - Para cada nó, |altura_esq - altura_dir| ≤ 1
        - Ambas as subárvores são AVL válidas
        """
        if no is None:
            return True, -1
        
        # Verifica subárvores recursivamente
        esq_valida, altura_esq = self._eh_balanceamento_valido(no.esquerda)
        if not esq_valida:
            return False, 0
        
        dir_valida, altura_dir = self._eh_balanceamento_valido(no.direita)
        if not dir_valida:
            return False, 0
        
        # Verifica balanceamento do nó atual
        fator_balanceamento = altura_esq - altura_dir
        if abs(fator_balanceamento) > 1:
            return False, 0
        
        altura_atual = 1 + max(altura_esq, altura_dir)
        return True, altura_atual
    
    def _metricas_consistentes(self, no: Optional[NoAVL]) -> bool:
        """Verifica se as métricas armazenadas estão corretas."""
        if no is None:
            return True
        
        # Verifica recursivamente
        if not (self._metricas_consistentes(no.esquerda) and
                self._metricas_consistentes(no.direita)):
            return False
        
        # Calcula métricas esperadas
        altura_esq = no.obter_altura_esquerda()
        altura_dir = no.obter_altura_direita()
        altura_esperada = 1 + max(altura_esq, altura_dir)
        fator_esperado = altura_esq - altura_dir
        
        # Verifica consistência
        return (no.altura == altura_esperada and
                no.fator_balanceamento == fator_esperado)
    
    def calcular_altura_maxima_teorica(self) -> float:
        """
        Calcula a altura máxima teórica para uma AVL com n nós.
        
        Fórmula: h ≤ 1.44 * log₂(n + 2) - 0.328
        """
        if self.tamanho == 0:
            return -1
        
        return 1.44 * math.log2(self.tamanho + 2) - 0.328
    
    def eficiencia_altura(self) -> float:
        """
        Calcula a eficiência da altura atual vs. altura ótima.
        
        Retorna valor entre 0 e 1 (1 = altura ótima).
        """
        if self.tamanho == 0:
            return 1.0
        
        altura_otima = math.log2(self.tamanho + 1) - 1
        altura_atual = self.obter_altura()
        
        if altura_atual <= altura_otima:
            return 1.0
        
        altura_maxima = self.calcular_altura_maxima_teorica()
        return (altura_maxima - altura_atual) / (altura_maxima - altura_otima)
    
    # ========================================================================
    # ESTATÍSTICAS E ANÁLISE
    # ========================================================================
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas detalhadas da árvore AVL."""
        if self.raiz is None:
            return {
                'tamanho': 0,
                'altura': -1,
                'altura_maxima_teorica': -1,
                'eficiencia_altura': 1.0,
                'eh_avl_valida': True,
                'rotacoes_realizadas': self._rotacoes_realizadas,
                'tipos_rotacao': dict(self._tipos_rotacao),
                'fator_balanceamento_raiz': 0,
                'nos_balanceados': 0,
                'nos_desbalanceados': 0
            }
        
        nos_bal, nos_desbal = self._contar_balanceamento(self.raiz)
        
        return {
            'tamanho': self.tamanho,
            'altura': self.obter_altura(),
            'altura_maxima_teorica': self.calcular_altura_maxima_teorica(),
            'eficiencia_altura': self.eficiencia_altura(),
            'eh_avl_valida': self.eh_avl_valida(),
            'rotacoes_realizadas': self._rotacoes_realizadas,
            'tipos_rotacao': dict(self._tipos_rotacao),
            'fator_balanceamento_raiz': self.raiz.fator_balanceamento,
            'nos_balanceados': nos_bal,
            'nos_desbalanceados': nos_desbal
        }
    
    def _contar_balanceamento(self, no: Optional[NoAVL]) -> Tuple[int, int]:
        """Conta nós balanceados e desbalanceados."""
        if no is None:
            return 0, 0
        
        bal_esq, desbal_esq = self._contar_balanceamento(no.esquerda)
        bal_dir, desbal_dir = self._contar_balanceamento(no.direita)
        
        if no.esta_desbalanceado():
            return bal_esq + bal_dir, desbal_esq + desbal_dir + 1
        else:
            return bal_esq + bal_dir + 1, desbal_esq + desbal_dir
    
    def resetar_estatisticas_rotacao(self) -> None:
        """Reseta as estatísticas de rotação."""
        self._rotacoes_realizadas = 0
        self._tipos_rotacao = {'LL': 0, 'RR': 0, 'LR': 0, 'RL': 0}
    
    # ========================================================================
    # VISUALIZAÇÃO E DEBUG
    # ========================================================================
    
    def imprimir_arvore(self) -> None:
        """Imprime a árvore com informações de balanceamento."""
        if self.raiz is None:
            print("Árvore AVL vazia")
            return
        
        print("Árvore AVL (valor(altura,fator_balanceamento)):")
        linhas = self._gerar_representacao_visual(self.raiz)
        for linha in linhas:
            print(linha)
    
    def _gerar_representacao_visual(self, no: NoAVL, prefixo: str = "", eh_ultimo: bool = True) -> List[str]:
        """Gera representação visual da árvore."""
        linhas = []
        
        if no is not None:
            # Linha atual com métricas
            conector = "└── " if eh_ultimo else "├── "
            info_no = f"{no.valor}(h:{no.altura},fb:{no.fator_balanceamento})"
            linhas.append(prefixo + conector + info_no)
            
            # Prepara prefixo para filhos
            novo_prefixo = prefixo + ("    " if eh_ultimo else "│   ")
            
            # Adiciona filhos
            filhos = []
            if no.esquerda is not None:
                filhos.append(no.esquerda)
            if no.direita is not None:
                filhos.append(no.direita)
            
            for i, filho in enumerate(filhos):
                eh_ultimo_filho = (i == len(filhos) - 1)
                linhas_filho = self._gerar_representacao_visual(filho, novo_prefixo, eh_ultimo_filho)
                linhas.extend(linhas_filho)
        
        return linhas
    
    def imprimir_fatores_balanceamento(self) -> None:
        """Imprime apenas os fatores de balanceamento."""
        if self.raiz is None:
            print("Árvore vazia")
            return
        
        print("Fatores de balanceamento:")
        self._imprimir_fatores_recursivo(self.raiz, 0)
    
    def _imprimir_fatores_recursivo(self, no: Optional[NoAVL], nivel: int) -> None:
        """Imprime fatores de balanceamento recursivamente."""
        if no is not None:
            self._imprimir_fatores_recursivo(no.direita, nivel + 1)
            print("  " * nivel + f"{no.valor}: {no.fator_balanceamento}")
            self._imprimir_fatores_recursivo(no.esquerda, nivel + 1)
    
    # ========================================================================
    # MÉTODOS MÁGICOS
    # ========================================================================
    
    def __len__(self) -> int:
        """Retorna o tamanho da árvore."""
        return self.tamanho
    
    def __contains__(self, valor: Any) -> bool:
        """Permite usar 'in' para verificar se valor existe."""
        return self.contem(valor)
    
    def __str__(self) -> str:
        """Representação string da árvore."""
        if self.raiz is None:
            return "AVL(vazia)"
        
        valores = self.travessia_in_order()
        return f"AVL({valores})"
    
    def __repr__(self) -> str:
        return self.__str__()

# ============================================================================
# APLICAÇÕES PRÁTICAS
# ============================================================================

class IndiceBalanceado:
    """
    Índice balanceado usando AVL para garantir performance consistente.
    
    Aplicação: Sistemas de banco de dados que precisam de garantias de performance.
    """
    
    def __init__(self):
        self.avl = ArvoreAVL()
        self.dados = {}  # Mapeia chave -> dados completos
    
    def inserir(self, chave: Any, dados: Any) -> bool:
        """Insere um registro no índice."""
        if self.avl.inserir(chave):
            self.dados[chave] = dados
            return True
        return False
    
    def buscar(self, chave: Any) -> Optional[Any]:
        """Busca um registro pela chave - O(log n) garantido."""
        if self.avl.contem(chave):
            return self.dados[chave]
        return None
    
    def remover(self, chave: Any) -> bool:
        """Remove um registro do índice - O(log n) garantido."""
        if self.avl.remover(chave):
            del self.dados[chave]
            return True
        return False
    
    def buscar_range(self, min_chave: Any, max_chave: Any) -> List[Tuple[Any, Any]]:
        """Busca registros em um intervalo - O(log n + k) garantido."""
        chaves = self.avl.buscar_range(min_chave, max_chave)
        return [(chave, self.dados[chave]) for chave in chaves]
    
    def obter_estatisticas_performance(self) -> dict:
        """Retorna estatísticas de performance do índice."""
        stats_avl = self.avl.obter_estatisticas()
        return {
            'registros': len(self.dados),
            'altura_arvore': stats_avl['altura'],
            'eficiencia_altura': stats_avl['eficiencia_altura'],
            'rotacoes_realizadas': stats_avl['rotacoes_realizadas'],
            'garantia_performance': 'O(log n) para todas as operações'
        }

class CacheBalanceado:
    """
    Cache com estrutura balanceada para acesso eficiente por prioridade.
    
    Aplicação: Sistemas de cache que precisam de acesso rápido e ordenado.
    """
    
    def __init__(self, capacidade_maxima: int = 1000):
        self.avl = ArvoreAVL()
        self.cache = {}  # prioridade -> dados
        self.capacidade_maxima = capacidade_maxima
        self.contador_acesso = 0
    
    def inserir(self, chave: Any, dados: Any, prioridade: int = None) -> None:
        """Insere um item no cache com prioridade."""
        if prioridade is None:
            prioridade = self.contador_acesso
            self.contador_acesso += 1
        
        # Remove item com menor prioridade se necessário
        if len(self.cache) >= self.capacidade_maxima:
            menor_prioridade = self.avl.encontrar_minimo()
            if menor_prioridade is not None:
                self.remover_por_prioridade(menor_prioridade)
        
        # Insere novo item
        self.avl.inserir(prioridade)
        self.cache[prioridade] = {'chave': chave, 'dados': dados}
    
    def buscar(self, chave: Any) -> Optional[Any]:
        """Busca um item no cache."""
        for prioridade, item in self.cache.items():
            if item['chave'] == chave:
                return item['dados']
        return None
    
    def remover_por_prioridade(self, prioridade: int) -> bool:
        """Remove um item pela prioridade."""
        if self.avl.remover(prioridade):
            del self.cache[prioridade]
            return True
        return False
    
    def obter_itens_alta_prioridade(self, limite: int = 10) -> List[Any]:
        """Retorna os itens de maior prioridade."""
        todas_prioridades = self.avl.travessia_in_order()
        altas_prioridades = todas_prioridades[-limite:]
        
        return [self.cache[p]['dados'] for p in altas_prioridades if p in self.cache]
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas do cache."""
        stats_avl = self.avl.obter_estatisticas()
        return {
            'itens_cache': len(self.cache),
            'capacidade_maxima': self.capacidade_maxima,
            'altura_indice': stats_avl['altura'],
            'eficiencia_altura': stats_avl['eficiencia_altura'],
            'rotacoes_realizadas': stats_avl['rotacoes_realizadas']
        }

# ============================================================================
# FUNÇÕES DE DEMONSTRAÇÃO E BENCHMARK
# ============================================================================

def demonstrar_avl_basica():
    """Demonstra operações básicas da AVL."""
    print("=== DEMONSTRAÇÃO: AVL Básica ===")
    
    avl = ArvoreAVL()
    valores = [10, 20, 30, 40, 50, 25]  # Sequência que causaria desbalanceamento em BST
    
    print("Inserindo valores:", valores)
    for valor in valores:
        print(f"\nInserindo {valor}:")
        avl.inserir(valor)
        avl.imprimir_arvore()
        
        stats = avl.obter_estatisticas()
        print(f"Altura: {stats['altura']}, Rotações: {stats['rotacoes_realizadas']}")
    
    print(f"\nÁrvore final:")
    avl.imprimir_arvore()
    
    print(f"\nValores em ordem: {avl.travessia_in_order()}")
    
    print("\nEstatísticas finais:")
    stats = avl.obter_estatisticas()
    for chave, valor in stats.items():
        print(f"  {chave}: {valor}")

def demonstrar_rotacoes():
    """Demonstra diferentes tipos de rotações."""
    print("\n=== DEMONSTRAÇÃO: Tipos de Rotações ===")
    
    # Rotação LL (simples direita)
    print("1. Rotação LL (Left-Left):")
    avl_ll = ArvoreAVL()
    avl_ll.resetar_estatisticas_rotacao()
    for valor in [30, 20, 10]:  # Inserção decrescente
        avl_ll.inserir(valor)
    avl_ll.imprimir_arvore()
    print(f"Rotações: {avl_ll.obter_estatisticas()['tipos_rotacao']}")
    
    # Rotação RR (simples esquerda)
    print("\n2. Rotação RR (Right-Right):")
    avl_rr = ArvoreAVL()
    avl_rr.resetar_estatisticas_rotacao()
    for valor in [10, 20, 30]:  # Inserção crescente
        avl_rr.inserir(valor)
    avl_rr.imprimir_arvore()
    print(f"Rotações: {avl_rr.obter_estatisticas()['tipos_rotacao']}")
    
    # Rotação LR (dupla esquerda-direita)
    print("\n3. Rotação LR (Left-Right):")
    avl_lr = ArvoreAVL()
    avl_lr.resetar_estatisticas_rotacao()
    for valor in [30, 10, 20]:  # Padrão LR
        avl_lr.inserir(valor)
    avl_lr.imprimir_arvore()
    print(f"Rotações: {avl_lr.obter_estatisticas()['tipos_rotacao']}")
    
    # Rotação RL (dupla direita-esquerda)
    print("\n4. Rotação RL (Right-Left):")
    avl_rl = ArvoreAVL()
    avl_rl.resetar_estatisticas_rotacao()
    for valor in [10, 30, 20]:  # Padrão RL
        avl_rl.inserir(valor)
    avl_rl.imprimir_arvore()
    print(f"Rotações: {avl_rl.obter_estatisticas()['tipos_rotacao']}")

def demonstrar_aplicacoes_praticas():
    """Demonstra aplicações práticas da AVL."""
    print("\n=== DEMONSTRAÇÃO: Aplicações Práticas ===")
    
    # Índice balanceado
    print("1. Índice Balanceado (Sistema de Banco de Dados):")
    indice = IndiceBalanceado()
    
    # Simula inserção de registros de funcionários
    funcionarios = [
        (1001, {"nome": "Ana Silva", "salario": 5000}),
        (1005, {"nome": "Bruno Costa", "salario": 6000}),
        (1003, {"nome": "Carlos Lima", "salario": 5500}),
        (1007, {"nome": "Diana Santos", "salario": 7000}),
        (1002, {"nome": "Eduardo Rocha", "salario": 4500}),
        (1006, {"nome": "Fernanda Alves", "salario": 6500}),
        (1004, {"nome": "Gabriel Souza", "salario": 5200})
    ]
    
    for id_func, dados in funcionarios:
        indice.inserir(id_func, dados)
    
    print("Funcionários por ID (ordenado):")
    for id_func in sorted([f[0] for f in funcionarios]):
        dados = indice.buscar(id_func)
        print(f"  {id_func}: {dados['nome']} - R$ {dados['salario']}")
    
    print(f"\nBuscar funcionários na faixa 1003-1006:")
    for id_func, dados in indice.buscar_range(1003, 1006):
        print(f"  {id_func}: {dados['nome']}")
    
    print("\nEstatísticas de Performance:")
    stats = indice.obter_estatisticas_performance()
    for chave, valor in stats.items():
        print(f"  {chave}: {valor}")
    
    # Cache balanceado
    print("\n2. Cache Balanceado:")
    cache = CacheBalanceado(capacidade_maxima=5)
    
    # Simula inserção de dados com diferentes prioridades
    dados_cache = [
        ("user_123", {"perfil": "admin"}, 100),
        ("user_456", {"perfil": "user"}, 50),
        ("user_789", {"perfil": "guest"}, 10),
        ("user_321", {"perfil": "moderator"}, 75),
        ("user_654", {"perfil": "premium"}, 90)
    ]
    
    for chave, dados, prioridade in dados_cache:
        cache.inserir(chave, dados, prioridade)
    
    print("Itens de alta prioridade:")
    itens_alta = cache.obter_itens_alta_prioridade(3)
    for item in itens_alta:
        print(f"  {item}")
    
    print("\nEstatísticas do Cache:")
    stats_cache = cache.obter_estatisticas()
    for chave, valor in stats_cache.items():
        print(f"  {chave}: {valor}")

def benchmark_avl_vs_bst():
    """Compara performance da AVL com BST comum."""
    print("\n=== BENCHMARK: AVL vs BST Comum ===")
    
    from .arvores_busca_binaria import ArvoreBuscaBinaria  # Importa BST do módulo anterior
    
    tamanhos = [1000, 5000, 10000]
    
    for n in tamanhos:
        print(f"\nTamanho: {n} elementos")
        
        # Dados ordenados (pior caso para BST)
        dados_ordenados = list(range(n))
        
        # Teste AVL
        avl = ArvoreAVL()
        inicio = time.time()
        for valor in dados_ordenados:
            avl.inserir(valor)
        tempo_insercao_avl = time.time() - inicio
        
        inicio = time.time()
        for _ in range(100):
            valor = random.choice(dados_ordenados)
            avl.buscar(valor)
        tempo_busca_avl = time.time() - inicio
        
        # Teste BST
        bst = ArvoreBuscaBinaria()
        inicio = time.time()
        for valor in dados_ordenados:
            bst.inserir(valor)
        tempo_insercao_bst = time.time() - inicio
        
        inicio = time.time()
        for _ in range(100):
            valor = random.choice(dados_ordenados)
            bst.buscar(valor)
        tempo_busca_bst = time.time() - inicio
        
        print(f"  Inserção (dados ordenados):")
        print(f"    AVL: {tempo_insercao_avl:.4f}s (altura: {avl.obter_altura()})")
        print(f"    BST: {tempo_insercao_bst:.4f}s (altura: {bst.calcular_altura()})")
        
        print(f"  Busca (100 operações):")
        print(f"    AVL: {tempo_busca_avl:.4f}s")
        print(f"    BST: {tempo_busca_bst:.4f}s")
        
        print(f"  Rotações realizadas na AVL: {avl.obter_estatisticas()['rotacoes_realizadas']}")

def main():
    """Função principal para demonstrar todos os conceitos."""
    print("MÓDULO 05.3: ÁRVORES AVL (AUTO-BALANCEADAS)")
    print("=" * 60)
    
    demonstrar_avl_basica()
    demonstrar_rotacoes()
    demonstrar_aplicacoes_praticas()
    benchmark_avl_vs_bst()
    
    print("\n" + "=" * 60)
    print("CONCLUSÃO DO MÓDULO 05.3")
    print("=" * 60)
    print("""
    Neste módulo, exploramos as Árvores AVL (Auto-balanceadas):
    
    ✅ CONCEITOS FUNDAMENTAIS:
    • Propriedade AVL: |altura_esq - altura_dir| ≤ 1
    • Fator de balanceamento e sua manutenção
    • Garantia de O(log n) para todas as operações
    
    ✅ ROTAÇÕES IMPLEMENTADAS:
    • Rotação simples à direita (LL)
    • Rotação simples à esquerda (RR)
    • Rotação dupla esquerda-direita (LR)
    • Rotação dupla direita-esquerda (RL)
    
    ✅ REBALANCEAMENTO AUTOMÁTICO:
    • Detecção automática de desbalanceamento
    • Aplicação da rotação apropriada
    • Manutenção das métricas (altura, fator)
    • Estatísticas de rotações realizadas
    
    ✅ VALIDAÇÃO E ANÁLISE:
    • Verificação de propriedades AVL
    • Cálculo de eficiência de altura
    • Análise de performance garantida
    • Comparação com altura teórica máxima
    
    ✅ APLICAÇÕES PRÁTICAS:
    • Índices balanceados para bancos de dados
    • Caches com acesso ordenado eficiente
    • Sistemas que precisam de garantias de performance
    • Estruturas de dados críticas para tempo real
    
    ✅ VANTAGENS DA AVL:
    • Performance consistente O(log n)
    • Altura máxima limitada: 1.44 * log₂(n)
    • Ideal para aplicações com muitas consultas
    • Balanceamento rigoroso garante eficiência
    
    🎯 PRÓXIMO MÓDULO: 05.4 - Árvores Rubro-Negras
    """)

if __name__ == "__main__":
    main()