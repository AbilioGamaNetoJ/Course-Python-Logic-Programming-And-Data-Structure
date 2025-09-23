"""
=============================================================================
CURSO DE LÓGICA DE PROGRAMAÇÃO E ESTRUTURAS DE DADOS EM PYTHON
Professor: Especialista em Estruturas de Dados e Algoritmos

MÓDULO 05: ESTRUTURAS DE DADOS NÃO-LINEARES
Arquivo 05.4: Árvores Rubro-Negras (Red-Black Trees)
=============================================================================

OBJETIVOS DE APRENDIZADO:
- Compreender as propriedades das árvores rubro-negras
- Implementar inserção com correção de cores
- Implementar remoção com rebalanceamento
- Comparar com AVL em termos de performance e uso
- Aplicar em estruturas de dados de sistemas operacionais

CONCEITOS ABORDADOS:
1. Propriedades das árvores rubro-negras
2. Coloração de nós e invariantes
3. Rotações e recoloração
4. Inserção com correção automática
5. Remoção com casos complexos
6. Comparação com outras árvores balanceadas

PRÉ-REQUISITOS:
- Módulo 05.3 (Árvores AVL)
- Compreensão de rotações em árvores
- Análise de invariantes de estruturas de dados

COMPLEXIDADE DAS OPERAÇÕES (GARANTIDA):
- Busca: O(log n) sempre
- Inserção: O(log n) sempre
- Remoção: O(log n) sempre
- Espaço: O(n) para armazenamento
- Altura máxima: 2 * log₂(n + 1)
=============================================================================
"""

from typing import Optional, List, Tuple, Any
from enum import Enum
import time
import random

class Cor(Enum):
    """Enumeração para as cores dos nós."""
    VERMELHO = "VERMELHO"
    PRETO = "PRETO"

class NoRubroNegro:
    """
    Nó para Árvore Rubro-Negra.
    
    Cada nó possui:
    - valor: dados armazenados
    - cor: VERMELHO ou PRETO
    - pai: referência para o nó pai
    - esquerda/direita: filhos
    """
    
    def __init__(self, valor: Any, cor: Cor = Cor.VERMELHO):
        self.valor = valor
        self.cor = cor
        self.pai: Optional['NoRubroNegro'] = None
        self.esquerda: Optional['NoRubroNegro'] = None
        self.direita: Optional['NoRubroNegro'] = None
    
    def eh_vermelho(self) -> bool:
        """Verifica se o nó é vermelho."""
        return self.cor == Cor.VERMELHO
    
    def eh_preto(self) -> bool:
        """Verifica se o nó é preto."""
        return self.cor == Cor.PRETO
    
    def eh_folha(self) -> bool:
        """Verifica se o nó é uma folha (não tem filhos reais)."""
        return self.esquerda is None and self.direita is None
    
    def eh_filho_esquerdo(self) -> bool:
        """Verifica se é filho esquerdo do pai."""
        return self.pai is not None and self.pai.esquerda == self
    
    def eh_filho_direito(self) -> bool:
        """Verifica se é filho direito do pai."""
        return self.pai is not None and self.pai.direita == self
    
    def obter_avo(self) -> Optional['NoRubroNegro']:
        """Retorna o avô (pai do pai)."""
        return self.pai.pai if self.pai else None
    
    def obter_tio(self) -> Optional['NoRubroNegro']:
        """Retorna o tio (irmão do pai)."""
        avo = self.obter_avo()
        if avo is None:
            return None
        
        if self.pai.eh_filho_esquerdo():
            return avo.direita
        else:
            return avo.esquerda
    
    def obter_irmao(self) -> Optional['NoRubroNegro']:
        """Retorna o irmão."""
        if self.pai is None:
            return None
        
        if self.eh_filho_esquerdo():
            return self.pai.direita
        else:
            return self.pai.esquerda
    
    def trocar_cor(self) -> None:
        """Troca a cor do nó."""
        self.cor = Cor.PRETO if self.cor == Cor.VERMELHO else Cor.VERMELHO
    
    def definir_cor(self, cor: Cor) -> None:
        """Define a cor do nó."""
        self.cor = cor
    
    def __str__(self) -> str:
        cor_str = "V" if self.eh_vermelho() else "P"
        return f"{self.valor}({cor_str})"
    
    def __repr__(self) -> str:
        return f"NoRN({self.valor}, {self.cor.value})"

class ArvoreRubroNegra:
    """
    Implementação completa de Árvore Rubro-Negra.
    
    PROPRIEDADES RUBRO-NEGRAS:
    1. Todo nó é vermelho ou preto
    2. A raiz é sempre preta
    3. Todas as folhas (NIL) são pretas
    4. Se um nó é vermelho, seus filhos são pretos
    5. Todo caminho da raiz até uma folha contém o mesmo número de nós pretos
    
    Essas propriedades garantem que a árvore seja aproximadamente balanceada.
    """
    
    def __init__(self):
        self.raiz: Optional[NoRubroNegro] = None
        self.tamanho = 0
        self._rotacoes_realizadas = 0
        self._recoloracoes_realizadas = 0
        self._tipos_correcao = {
            'insercao_caso1': 0,  # Nó é raiz
            'insercao_caso2': 0,  # Pai é preto
            'insercao_caso3': 0,  # Pai e tio são vermelhos
            'insercao_caso4': 0,  # Pai vermelho, tio preto, rotação necessária
            'insercao_caso5': 0,  # Continuação do caso 4
            'remocao_casos': 0    # Casos de remoção
        }
    
    def esta_vazia(self) -> bool:
        """Verifica se a árvore está vazia."""
        return self.raiz is None
    
    def obter_tamanho(self) -> int:
        """Retorna o número de elementos na árvore."""
        return self.tamanho
    
    def calcular_altura(self) -> int:
        """Calcula a altura da árvore."""
        return self._calcular_altura_recursivo(self.raiz)
    
    def _calcular_altura_recursivo(self, no: Optional[NoRubroNegro]) -> int:
        """Calcula altura recursivamente."""
        if no is None:
            return -1
        
        altura_esq = self._calcular_altura_recursivo(no.esquerda)
        altura_dir = self._calcular_altura_recursivo(no.direita)
        return 1 + max(altura_esq, altura_dir)
    
    def calcular_altura_preta(self) -> int:
        """
        Calcula a altura preta (número de nós pretos em qualquer caminho).
        
        Em uma árvore rubro-negra válida, todos os caminhos têm a mesma altura preta.
        """
        return self._calcular_altura_preta_recursivo(self.raiz)
    
    def _calcular_altura_preta_recursivo(self, no: Optional[NoRubroNegro]) -> int:
        """Calcula altura preta recursivamente."""
        if no is None:
            return 0  # Folhas NIL são pretas
        
        altura_esq = self._calcular_altura_preta_recursivo(no.esquerda)
        incremento = 1 if no.eh_preto() else 0
        return altura_esq + incremento
    
    # ========================================================================
    # ROTAÇÕES - OPERAÇÕES FUNDAMENTAIS
    # ========================================================================
    
    def rotacao_esquerda(self, no: NoRubroNegro) -> None:
        """
        Rotação à esquerda.
        
        Antes:   x              Depois:    y
                / \                       / \
               A   y                     x   C
                  / \                   / \
                 B   C                 A   B
        """
        y = no.direita
        no.direita = y.esquerda
        
        if y.esquerda is not None:
            y.esquerda.pai = no
        
        y.pai = no.pai
        
        if no.pai is None:
            self.raiz = y
        elif no.eh_filho_esquerdo():
            no.pai.esquerda = y
        else:
            no.pai.direita = y
        
        y.esquerda = no
        no.pai = y
        
        self._rotacoes_realizadas += 1
    
    def rotacao_direita(self, no: NoRubroNegro) -> None:
        """
        Rotação à direita.
        
        Antes:     y            Depois:  x
                  / \                   / \
                 x   C                 A   y
                / \                       / \
               A   B                     B   C
        """
        x = no.esquerda
        no.esquerda = x.direita
        
        if x.direita is not None:
            x.direita.pai = no
        
        x.pai = no.pai
        
        if no.pai is None:
            self.raiz = x
        elif no.eh_filho_direito():
            no.pai.direita = x
        else:
            no.pai.esquerda = x
        
        x.direita = no
        no.pai = x
        
        self._rotacoes_realizadas += 1
    
    # ========================================================================
    # BUSCA - OPERAÇÃO BÁSICA
    # ========================================================================
    
    def buscar(self, valor: Any) -> Optional[NoRubroNegro]:
        """Busca um valor na árvore."""
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, no: Optional[NoRubroNegro], valor: Any) -> Optional[NoRubroNegro]:
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
    
    # ========================================================================
    # INSERÇÃO COM CORREÇÃO DE CORES
    # ========================================================================
    
    def inserir(self, valor: Any) -> bool:
        """
        Insere um valor na árvore com correção automática das propriedades RB.
        
        Processo:
        1. Inserção BST normal (nó vermelho)
        2. Correção das propriedades rubro-negras
        """
        if self.raiz is None:
            self.raiz = NoRubroNegro(valor, Cor.PRETO)  # Raiz sempre preta
            self.tamanho += 1
            self._tipos_correcao['insercao_caso1'] += 1
            return True
        
        # Busca posição de inserção
        pai = None
        atual = self.raiz
        
        while atual is not None:
            pai = atual
            if valor < atual.valor:
                atual = atual.esquerda
            elif valor > atual.valor:
                atual = atual.direita
            else:
                return False  # Valor já existe
        
        # Cria novo nó vermelho
        novo_no = NoRubroNegro(valor, Cor.VERMELHO)
        novo_no.pai = pai
        
        if valor < pai.valor:
            pai.esquerda = novo_no
        else:
            pai.direita = novo_no
        
        self.tamanho += 1
        
        # Corrige propriedades rubro-negras
        self._corrigir_insercao(novo_no)
        
        return True
    
    def _corrigir_insercao(self, no: NoRubroNegro) -> None:
        """
        Corrige as propriedades rubro-negras após inserção.
        
        Casos a considerar:
        1. Nó é raiz → pintar de preto
        2. Pai é preto → nada a fazer
        3. Pai e tio são vermelhos → recolorir
        4. Pai vermelho, tio preto → rotações necessárias
        """
        while no != self.raiz and no.pai.eh_vermelho():
            if no.pai.eh_filho_esquerdo():
                tio = no.pai.pai.direita
                
                if tio is not None and tio.eh_vermelho():
                    # Caso 3: Pai e tio vermelhos
                    no.pai.definir_cor(Cor.PRETO)
                    tio.definir_cor(Cor.PRETO)
                    no.pai.pai.definir_cor(Cor.VERMELHO)
                    no = no.pai.pai
                    self._tipos_correcao['insercao_caso3'] += 1
                    self._recoloracoes_realizadas += 3
                else:
                    # Caso 4: Pai vermelho, tio preto
                    if no.eh_filho_direito():
                        no = no.pai
                        self.rotacao_esquerda(no)
                        self._tipos_correcao['insercao_caso4'] += 1
                    
                    # Caso 5: Continuação
                    no.pai.definir_cor(Cor.PRETO)
                    no.pai.pai.definir_cor(Cor.VERMELHO)
                    self.rotacao_direita(no.pai.pai)
                    self._tipos_correcao['insercao_caso5'] += 1
                    self._recoloracoes_realizadas += 2
            else:
                # Simétrico para o lado direito
                tio = no.pai.pai.esquerda
                
                if tio is not None and tio.eh_vermelho():
                    # Caso 3: Pai e tio vermelhos
                    no.pai.definir_cor(Cor.PRETO)
                    tio.definir_cor(Cor.PRETO)
                    no.pai.pai.definir_cor(Cor.VERMELHO)
                    no = no.pai.pai
                    self._tipos_correcao['insercao_caso3'] += 1
                    self._recoloracoes_realizadas += 3
                else:
                    # Caso 4: Pai vermelho, tio preto
                    if no.eh_filho_esquerdo():
                        no = no.pai
                        self.rotacao_direita(no)
                        self._tipos_correcao['insercao_caso4'] += 1
                    
                    # Caso 5: Continuação
                    no.pai.definir_cor(Cor.PRETO)
                    no.pai.pai.definir_cor(Cor.VERMELHO)
                    self.rotacao_esquerda(no.pai.pai)
                    self._tipos_correcao['insercao_caso5'] += 1
                    self._recoloracoes_realizadas += 2
        
        # Caso 1: Garantir que a raiz seja preta
        if self.raiz.eh_vermelho():
            self.raiz.definir_cor(Cor.PRETO)
            self._tipos_correcao['insercao_caso1'] += 1
            self._recoloracoes_realizadas += 1
    
    # ========================================================================
    # REMOÇÃO COM CORREÇÃO DE CORES
    # ========================================================================
    
    def remover(self, valor: Any) -> bool:
        """
        Remove um valor da árvore com correção automática das propriedades RB.
        
        A remoção em árvores rubro-negras é mais complexa que a inserção.
        """
        no_remover = self.buscar(valor)
        if no_remover is None:
            return False
        
        self._remover_no(no_remover)
        self.tamanho -= 1
        return True
    
    def _remover_no(self, no: NoRubroNegro) -> None:
        """
        Remove um nó específico da árvore.
        
        Casos:
        1. Nó folha
        2. Nó com um filho
        3. Nó com dois filhos (substitui pelo sucessor)
        """
        cor_original = no.cor
        no_substituto = None
        
        if no.esquerda is None:
            # Caso 1 ou 2: sem filho esquerdo
            no_substituto = no.direita
            self._transplantar(no, no.direita)
        elif no.direita is None:
            # Caso 2: sem filho direito
            no_substituto = no.esquerda
            self._transplantar(no, no.esquerda)
        else:
            # Caso 3: dois filhos
            sucessor = self._encontrar_minimo(no.direita)
            cor_original = sucessor.cor
            no_substituto = sucessor.direita
            
            if sucessor.pai == no:
                if no_substituto:
                    no_substituto.pai = sucessor
            else:
                self._transplantar(sucessor, sucessor.direita)
                sucessor.direita = no.direita
                sucessor.direita.pai = sucessor
            
            self._transplantar(no, sucessor)
            sucessor.esquerda = no.esquerda
            sucessor.esquerda.pai = sucessor
            sucessor.cor = no.cor
        
        # Se removemos um nó preto, precisamos corrigir
        if cor_original == Cor.PRETO:
            self._corrigir_remocao(no_substituto)
    
    def _transplantar(self, u: Optional[NoRubroNegro], v: Optional[NoRubroNegro]) -> None:
        """Substitui a subárvore u pela subárvore v."""
        if u.pai is None:
            self.raiz = v
        elif u.eh_filho_esquerdo():
            u.pai.esquerda = v
        else:
            u.pai.direita = v
        
        if v is not None:
            v.pai = u.pai
    
    def _corrigir_remocao(self, no: Optional[NoRubroNegro]) -> None:
        """
        Corrige as propriedades rubro-negras após remoção.
        
        A remoção de um nó preto pode violar a propriedade 5
        (mesmo número de nós pretos em todos os caminhos).
        """
        while no != self.raiz and (no is None or no.eh_preto()):
            if no is None or no.eh_filho_esquerdo():
                irmao = no.pai.direita if no else None
                
                if irmao and irmao.eh_vermelho():
                    irmao.definir_cor(Cor.PRETO)
                    no.pai.definir_cor(Cor.VERMELHO)
                    self.rotacao_esquerda(no.pai)
                    irmao = no.pai.direita if no else None
                
                if irmao and ((irmao.esquerda is None or irmao.esquerda.eh_preto()) and
                             (irmao.direita is None or irmao.direita.eh_preto())):
                    irmao.definir_cor(Cor.VERMELHO)
                    no = no.pai if no else None
                else:
                    if irmao and (irmao.direita is None or irmao.direita.eh_preto()):
                        if irmao.esquerda:
                            irmao.esquerda.definir_cor(Cor.PRETO)
                        irmao.definir_cor(Cor.VERMELHO)
                        self.rotacao_direita(irmao)
                        irmao = no.pai.direita if no else None
                    
                    if irmao:
                        irmao.cor = no.pai.cor
                        no.pai.definir_cor(Cor.PRETO)
                        if irmao.direita:
                            irmao.direita.definir_cor(Cor.PRETO)
                        self.rotacao_esquerda(no.pai)
                    no = self.raiz
            else:
                # Simétrico para o lado direito
                irmao = no.pai.esquerda
                
                if irmao and irmao.eh_vermelho():
                    irmao.definir_cor(Cor.PRETO)
                    no.pai.definir_cor(Cor.VERMELHO)
                    self.rotacao_direita(no.pai)
                    irmao = no.pai.esquerda
                
                if irmao and ((irmao.direita is None or irmao.direita.eh_preto()) and
                             (irmao.esquerda is None or irmao.esquerda.eh_preto())):
                    irmao.definir_cor(Cor.VERMELHO)
                    no = no.pai
                else:
                    if irmao and (irmao.esquerda is None or irmao.esquerda.eh_preto()):
                        if irmao.direita:
                            irmao.direita.definir_cor(Cor.PRETO)
                        irmao.definir_cor(Cor.VERMELHO)
                        self.rotacao_esquerda(irmao)
                        irmao = no.pai.esquerda
                    
                    if irmao:
                        irmao.cor = no.pai.cor
                        no.pai.definir_cor(Cor.PRETO)
                        if irmao.esquerda:
                            irmao.esquerda.definir_cor(Cor.PRETO)
                        self.rotacao_direita(no.pai)
                    no = self.raiz
        
        if no:
            no.definir_cor(Cor.PRETO)
        
        self._tipos_correcao['remocao_casos'] += 1
    
    def _encontrar_minimo(self, no: NoRubroNegro) -> NoRubroNegro:
        """Encontra o nó com menor valor a partir de um nó."""
        while no.esquerda is not None:
            no = no.esquerda
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
        
        no = self.raiz
        while no.direita is not None:
            no = no.direita
        return no.valor
    
    def travessia_in_order(self) -> List[Any]:
        """Travessia in-order (valores em ordem crescente)."""
        resultado = []
        self._in_order_recursivo(self.raiz, resultado)
        return resultado
    
    def _in_order_recursivo(self, no: Optional[NoRubroNegro], resultado: List[Any]) -> None:
        """Implementação recursiva da travessia in-order."""
        if no is not None:
            self._in_order_recursivo(no.esquerda, resultado)
            resultado.append(no.valor)
            self._in_order_recursivo(no.direita, resultado)
    
    def travessia_com_cores(self) -> List[Tuple[Any, str]]:
        """Travessia in-order retornando valores com suas cores."""
        resultado = []
        self._in_order_com_cores_recursivo(self.raiz, resultado)
        return resultado
    
    def _in_order_com_cores_recursivo(self, no: Optional[NoRubroNegro], resultado: List[Tuple[Any, str]]) -> None:
        """Travessia in-order com informação de cores."""
        if no is not None:
            self._in_order_com_cores_recursivo(no.esquerda, resultado)
            cor_str = "V" if no.eh_vermelho() else "P"
            resultado.append((no.valor, cor_str))
            self._in_order_com_cores_recursivo(no.direita, resultado)
    
    # ========================================================================
    # VALIDAÇÃO DAS PROPRIEDADES RUBRO-NEGRAS
    # ========================================================================
    
    def eh_rubro_negra_valida(self) -> bool:
        """
        Verifica se a árvore satisfaz todas as propriedades rubro-negras.
        
        Propriedades verificadas:
        1. Raiz é preta
        2. Não há dois nós vermelhos consecutivos
        3. Todos os caminhos têm a mesma altura preta
        4. Propriedade BST
        """
        if self.raiz is None:
            return True
        
        # Propriedade 2: Raiz é preta
        if self.raiz.eh_vermelho():
            return False
        
        # Verifica outras propriedades
        return (self._verificar_nos_vermelhos_consecutivos(self.raiz) and
                self._verificar_altura_preta_uniforme(self.raiz)[0] and
                self._verificar_propriedade_bst(self.raiz, float('-inf'), float('inf')))
    
    def _verificar_nos_vermelhos_consecutivos(self, no: Optional[NoRubroNegro]) -> bool:
        """Verifica se não há dois nós vermelhos consecutivos."""
        if no is None:
            return True
        
        # Se o nó é vermelho, seus filhos devem ser pretos
        if no.eh_vermelho():
            if ((no.esquerda and no.esquerda.eh_vermelho()) or
                (no.direita and no.direita.eh_vermelho())):
                return False
        
        return (self._verificar_nos_vermelhos_consecutivos(no.esquerda) and
                self._verificar_nos_vermelhos_consecutivos(no.direita))
    
    def _verificar_altura_preta_uniforme(self, no: Optional[NoRubroNegro]) -> Tuple[bool, int]:
        """
        Verifica se todos os caminhos têm a mesma altura preta.
        
        Retorna (é_válida, altura_preta).
        """
        if no is None:
            return True, 0
        
        esq_valida, altura_esq = self._verificar_altura_preta_uniforme(no.esquerda)
        if not esq_valida:
            return False, 0
        
        dir_valida, altura_dir = self._verificar_altura_preta_uniforme(no.direita)
        if not dir_valida:
            return False, 0
        
        # Alturas pretas devem ser iguais
        if altura_esq != altura_dir:
            return False, 0
        
        incremento = 1 if no.eh_preto() else 0
        return True, altura_esq + incremento
    
    def _verificar_propriedade_bst(self, no: Optional[NoRubroNegro], min_val: float, max_val: float) -> bool:
        """Verifica se a propriedade BST é mantida."""
        if no is None:
            return True
        
        if no.valor <= min_val or no.valor >= max_val:
            return False
        
        return (self._verificar_propriedade_bst(no.esquerda, min_val, no.valor) and
                self._verificar_propriedade_bst(no.direita, no.valor, max_val))
    
    # ========================================================================
    # ESTATÍSTICAS E ANÁLISE
    # ========================================================================
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas detalhadas da árvore rubro-negra."""
        if self.raiz is None:
            return {
                'tamanho': 0,
                'altura': -1,
                'altura_preta': 0,
                'altura_maxima_teorica': 0,
                'nos_vermelhos': 0,
                'nos_pretos': 0,
                'eh_rubro_negra_valida': True,
                'rotacoes_realizadas': self._rotacoes_realizadas,
                'recoloracoes_realizadas': self._recoloracoes_realizadas,
                'tipos_correcao': dict(self._tipos_correcao)
            }
        
        nos_v, nos_p = self._contar_cores(self.raiz)
        altura_maxima_teorica = 2 * (self.calcular_altura_preta() + 1) - 1
        
        return {
            'tamanho': self.tamanho,
            'altura': self.calcular_altura(),
            'altura_preta': self.calcular_altura_preta(),
            'altura_maxima_teorica': altura_maxima_teorica,
            'nos_vermelhos': nos_v,
            'nos_pretos': nos_p,
            'eh_rubro_negra_valida': self.eh_rubro_negra_valida(),
            'rotacoes_realizadas': self._rotacoes_realizadas,
            'recoloracoes_realizadas': self._recoloracoes_realizadas,
            'tipos_correcao': dict(self._tipos_correcao)
        }
    
    def _contar_cores(self, no: Optional[NoRubroNegro]) -> Tuple[int, int]:
        """Conta nós vermelhos e pretos."""
        if no is None:
            return 0, 0
        
        v_esq, p_esq = self._contar_cores(no.esquerda)
        v_dir, p_dir = self._contar_cores(no.direita)
        
        if no.eh_vermelho():
            return v_esq + v_dir + 1, p_esq + p_dir
        else:
            return v_esq + v_dir, p_esq + p_dir + 1
    
    def resetar_estatisticas(self) -> None:
        """Reseta as estatísticas de operações."""
        self._rotacoes_realizadas = 0
        self._recoloracoes_realizadas = 0
        self._tipos_correcao = {
            'insercao_caso1': 0,
            'insercao_caso2': 0,
            'insercao_caso3': 0,
            'insercao_caso4': 0,
            'insercao_caso5': 0,
            'remocao_casos': 0
        }
    
    # ========================================================================
    # VISUALIZAÇÃO
    # ========================================================================
    
    def imprimir_arvore(self) -> None:
        """Imprime a árvore com informações de cores."""
        if self.raiz is None:
            print("Árvore Rubro-Negra vazia")
            return
        
        print("Árvore Rubro-Negra (valor(cor)):")
        linhas = self._gerar_representacao_visual(self.raiz)
        for linha in linhas:
            print(linha)
    
    def _gerar_representacao_visual(self, no: NoRubroNegro, prefixo: str = "", eh_ultimo: bool = True) -> List[str]:
        """Gera representação visual da árvore com cores."""
        linhas = []
        
        if no is not None:
            conector = "└── " if eh_ultimo else "├── "
            cor_str = "V" if no.eh_vermelho() else "P"
            linhas.append(prefixo + conector + f"{no.valor}({cor_str})")
            
            novo_prefixo = prefixo + ("    " if eh_ultimo else "│   ")
            
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
    
    def imprimir_cores_por_nivel(self) -> None:
        """Imprime a árvore organizada por níveis com cores."""
        if self.raiz is None:
            print("Árvore vazia")
            return
        
        print("Árvore por níveis (valor:cor):")
        fila = [(self.raiz, 0)]
        nivel_atual = 0
        
        while fila:
            no, nivel = fila.pop(0)
            
            if nivel > nivel_atual:
                print()
                nivel_atual = nivel
                print(f"Nível {nivel}: ", end="")
            
            cor_str = "V" if no.eh_vermelho() else "P"
            print(f"{no.valor}:{cor_str} ", end="")
            
            if no.esquerda:
                fila.append((no.esquerda, nivel + 1))
            if no.direita:
                fila.append((no.direita, nivel + 1))
        
        print()  # Nova linha final
    
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
            return "RN(vazia)"
        
        valores_cores = self.travessia_com_cores()
        return f"RN({valores_cores})"
    
    def __repr__(self) -> str:
        return self.__str__()

# ============================================================================
# APLICAÇÕES PRÁTICAS
# ============================================================================

class MapaOrdenado:
    """
    Mapa ordenado usando árvore rubro-negra.
    
    Aplicação: Implementação de std::map em C++ ou TreeMap em Java.
    Garante operações O(log n) com overhead menor que AVL.
    """
    
    def __init__(self):
        self.arvore = ArvoreRubroNegra()
        self.mapeamento = {}  # chave -> valor
    
    def inserir(self, chave: Any, valor: Any) -> None:
        """Insere um par chave-valor no mapa."""
        if self.arvore.inserir(chave):
            self.mapeamento[chave] = valor
        else:
            # Chave já existe, atualiza valor
            self.mapeamento[chave] = valor
    
    def obter(self, chave: Any) -> Optional[Any]:
        """Obtém o valor associado a uma chave."""
        if self.arvore.contem(chave):
            return self.mapeamento[chave]
        return None
    
    def remover(self, chave: Any) -> bool:
        """Remove um par chave-valor do mapa."""
        if self.arvore.remover(chave):
            del self.mapeamento[chave]
            return True
        return False
    
    def chaves_ordenadas(self) -> List[Any]:
        """Retorna todas as chaves em ordem."""
        return self.arvore.travessia_in_order()
    
    def valores_ordenados(self) -> List[Any]:
        """Retorna todos os valores ordenados por chave."""
        chaves = self.chaves_ordenadas()
        return [self.mapeamento[chave] for chave in chaves]
    
    def itens_ordenados(self) -> List[Tuple[Any, Any]]:
        """Retorna todos os pares (chave, valor) ordenados."""
        chaves = self.chaves_ordenadas()
        return [(chave, self.mapeamento[chave]) for chave in chaves]
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas do mapa."""
        stats_arvore = self.arvore.obter_estatisticas()
        return {
            'pares_chave_valor': len(self.mapeamento),
            'altura_arvore': stats_arvore['altura'],
            'nos_vermelhos': stats_arvore['nos_vermelhos'],
            'nos_pretos': stats_arvore['nos_pretos'],
            'rotacoes_realizadas': stats_arvore['rotacoes_realizadas'],
            'eh_valida': stats_arvore['eh_rubro_negra_valida']
        }

class ConjuntoOrdenado:
    """
    Conjunto ordenado usando árvore rubro-negra.
    
    Aplicação: Implementação de std::set em C++ ou TreeSet em Java.
    """
    
    def __init__(self):
        self.arvore = ArvoreRubroNegra()
    
    def adicionar(self, elemento: Any) -> bool:
        """Adiciona um elemento ao conjunto."""
        return self.arvore.inserir(elemento)
    
    def remover(self, elemento: Any) -> bool:
        """Remove um elemento do conjunto."""
        return self.arvore.remover(elemento)
    
    def contem(self, elemento: Any) -> bool:
        """Verifica se um elemento está no conjunto."""
        return self.arvore.contem(elemento)
    
    def elementos_ordenados(self) -> List[Any]:
        """Retorna todos os elementos em ordem."""
        return self.arvore.travessia_in_order()
    
    def tamanho(self) -> int:
        """Retorna o número de elementos."""
        return self.arvore.obter_tamanho()
    
    def minimo(self) -> Optional[Any]:
        """Retorna o menor elemento."""
        return self.arvore.encontrar_minimo()
    
    def maximo(self) -> Optional[Any]:
        """Retorna o maior elemento."""
        return self.arvore.encontrar_maximo()
    
    def uniao(self, outro: 'ConjuntoOrdenado') -> 'ConjuntoOrdenado':
        """Retorna a união com outro conjunto."""
        resultado = ConjuntoOrdenado()
        
        for elemento in self.elementos_ordenados():
            resultado.adicionar(elemento)
        
        for elemento in outro.elementos_ordenados():
            resultado.adicionar(elemento)
        
        return resultado
    
    def intersecao(self, outro: 'ConjuntoOrdenado') -> 'ConjuntoOrdenado':
        """Retorna a interseção com outro conjunto."""
        resultado = ConjuntoOrdenado()
        
        for elemento in self.elementos_ordenados():
            if outro.contem(elemento):
                resultado.adicionar(elemento)
        
        return resultado
    
    def diferenca(self, outro: 'ConjuntoOrdenado') -> 'ConjuntoOrdenado':
        """Retorna a diferença com outro conjunto."""
        resultado = ConjuntoOrdenado()
        
        for elemento in self.elementos_ordenados():
            if not outro.contem(elemento):
                resultado.adicionar(elemento)
        
        return resultado

# ============================================================================
# FUNÇÕES DE DEMONSTRAÇÃO E BENCHMARK
# ============================================================================

def demonstrar_rubro_negra_basica():
    """Demonstra operações básicas da árvore rubro-negra."""
    print("=== DEMONSTRAÇÃO: Rubro-Negra Básica ===")
    
    rn = ArvoreRubroNegra()
    valores = [10, 20, 30, 40, 50, 25, 15, 35]
    
    print("Inserindo valores:", valores)
    for valor in valores:
        print(f"\nInserindo {valor}:")
        rn.inserir(valor)
        rn.imprimir_arvore()
        
        stats = rn.obter_estatisticas()
        print(f"Altura: {stats['altura']}, Altura Preta: {stats['altura_preta']}")
        print(f"Vermelhos: {stats['nos_vermelhos']}, Pretos: {stats['nos_pretos']}")
    
    print(f"\nÁrvore final:")
    rn.imprimir_arvore()
    
    print(f"\nValores em ordem: {rn.travessia_in_order()}")
    print(f"Valores com cores: {rn.travessia_com_cores()}")
    
    print("\nEstatísticas finais:")
    stats = rn.obter_estatisticas()
    for chave, valor in stats.items():
        print(f"  {chave}: {valor}")

def demonstrar_propriedades_rubro_negras():
    """Demonstra as propriedades das árvores rubro-negras."""
    print("\n=== DEMONSTRAÇÃO: Propriedades Rubro-Negras ===")
    
    rn = ArvoreRubroNegra()
    valores = list(range(1, 16))  # 1 a 15
    
    print("Inserindo valores 1 a 15:")
    for valor in valores:
        rn.inserir(valor)
    
    rn.imprimir_cores_por_nivel()
    
    print(f"\nVerificação das propriedades:")
    print(f"É rubro-negra válida: {rn.eh_rubro_negra_valida()}")
    
    stats = rn.obter_estatisticas()
    print(f"Altura atual: {stats['altura']}")
    print(f"Altura preta: {stats['altura_preta']}")
    print(f"Altura máxima teórica: {stats['altura_maxima_teorica']}")
    print(f"Nós vermelhos: {stats['nos_vermelhos']}")
    print(f"Nós pretos: {stats['nos_pretos']}")
    
    # Teste de remoção
    print(f"\nRemovendo alguns valores...")
    for valor in [5, 10, 15]:
        print(f"Removendo {valor}")
        rn.remover(valor)
        print(f"Ainda válida: {rn.eh_rubro_negra_valida()}")

def demonstrar_aplicacoes_praticas():
    """Demonstra aplicações práticas das árvores rubro-negras."""
    print("\n=== DEMONSTRAÇÃO: Aplicações Práticas ===")
    
    # Mapa ordenado
    print("1. Mapa Ordenado (Dicionário com chaves ordenadas):")
    mapa = MapaOrdenado()
    
    funcionarios = [
        ("Ana", {"idade": 30, "salario": 5000}),
        ("Bruno", {"idade": 25, "salario": 4500}),
        ("Carlos", {"idade": 35, "salario": 6000}),
        ("Diana", {"idade": 28, "salario": 5500}),
        ("Eduardo", {"idade": 32, "salario": 5800})
    ]
    
    for nome, dados in funcionarios:
        mapa.inserir(nome, dados)
    
    print("Funcionários em ordem alfabética:")
    for nome, dados in mapa.itens_ordenados():
        print(f"  {nome}: {dados['idade']} anos, R$ {dados['salario']}")
    
    print(f"\nBuscar 'Carlos': {mapa.obter('Carlos')}")
    
    print("\nEstatísticas do Mapa:")
    stats_mapa = mapa.obter_estatisticas()
    for chave, valor in stats_mapa.items():
        print(f"  {chave}: {valor}")
    
    # Conjunto ordenado
    print("\n2. Conjunto Ordenado:")
    conjunto1 = ConjuntoOrdenado()
    conjunto2 = ConjuntoOrdenado()
    
    # Adiciona elementos aos conjuntos
    for x in [1, 3, 5, 7, 9]:
        conjunto1.adicionar(x)
    
    for x in [2, 3, 6, 7, 10]:
        conjunto2.adicionar(x)
    
    print(f"Conjunto 1: {conjunto1.elementos_ordenados()}")
    print(f"Conjunto 2: {conjunto2.elementos_ordenados()}")
    
    uniao = conjunto1.uniao(conjunto2)
    intersecao = conjunto1.intersecao(conjunto2)
    diferenca = conjunto1.diferenca(conjunto2)
    
    print(f"União: {uniao.elementos_ordenados()}")
    print(f"Interseção: {intersecao.elementos_ordenados()}")
    print(f"Diferença (1 - 2): {diferenca.elementos_ordenados()}")

def benchmark_rubro_negra_vs_avl():
    """Compara performance da Rubro-Negra com AVL."""
    print("\n=== BENCHMARK: Rubro-Negra vs AVL ===")
    
    from .arvores_avl import ArvoreAVL  # Importa AVL do módulo anterior
    
    tamanhos = [1000, 5000, 10000]
    
    for n in tamanhos:
        print(f"\nTamanho: {n} elementos")
        
        # Dados aleatórios
        dados = list(range(n))
        random.shuffle(dados)
        
        # Teste Rubro-Negra
        rn = ArvoreRubroNegra()
        rn.resetar_estatisticas()
        
        inicio = time.time()
        for valor in dados:
            rn.inserir(valor)
        tempo_insercao_rn = time.time() - inicio
        
        inicio = time.time()
        for _ in range(100):
            valor = random.choice(dados)
            rn.buscar(valor)
        tempo_busca_rn = time.time() - inicio
        
        # Teste AVL
        avl = ArvoreAVL()
        avl.resetar_estatisticas_rotacao()
        
        inicio = time.time()
        for valor in dados:
            avl.inserir(valor)
        tempo_insercao_avl = time.time() - inicio
        
        inicio = time.time()
        for _ in range(100):
            valor = random.choice(dados)
            avl.buscar(valor)
        tempo_busca_avl = time.time() - inicio
        
        # Estatísticas
        stats_rn = rn.obter_estatisticas()
        stats_avl = avl.obter_estatisticas()
        
        print(f"  Inserção (dados aleatórios):")
        print(f"    Rubro-Negra: {tempo_insercao_rn:.4f}s (altura: {stats_rn['altura']})")
        print(f"    AVL: {tempo_insercao_avl:.4f}s (altura: {stats_avl['altura']})")
        
        print(f"  Busca (100 operações):")
        print(f"    Rubro-Negra: {tempo_busca_rn:.4f}s")
        print(f"    AVL: {tempo_busca_avl:.4f}s")
        
        print(f"  Operações de balanceamento:")
        print(f"    Rubro-Negra: {stats_rn['rotacoes_realizadas']} rotações, {stats_rn['recoloracoes_realizadas']} recolorações")
        print(f"    AVL: {stats_avl['rotacoes_realizadas']} rotações")

def main():
    """Função principal para demonstrar todos os conceitos."""
    print("MÓDULO 05.4: ÁRVORES RUBRO-NEGRAS")
    print("=" * 60)
    
    demonstrar_rubro_negra_basica()
    demonstrar_propriedades_rubro_negras()
    demonstrar_aplicacoes_praticas()
    benchmark_rubro_negra_vs_avl()
    
    print("\n" + "=" * 60)
    print("CONCLUSÃO DO MÓDULO 05.4")
    print("=" * 60)
    print("""
    Neste módulo, exploramos as Árvores Rubro-Negras:
    
    ✅ PROPRIEDADES FUNDAMENTAIS:
    • Todo nó é vermelho ou preto
    • Raiz é sempre preta
    • Folhas (NIL) são pretas
    • Nós vermelhos têm filhos pretos
    • Todos os caminhos têm a mesma altura preta
    
    ✅ OPERAÇÕES IMPLEMENTADAS:
    • Inserção com correção automática de cores
    • Remoção com rebalanceamento complexo
    • Rotações e recolorações eficientes
    • Validação completa das propriedades
    
    ✅ ALGORITMOS DE CORREÇÃO:
    • 5 casos de correção na inserção
    • Múltiplos casos na remoção
    • Balanceamento por cores (menos rotações que AVL)
    • Manutenção automática das invariantes
    
    ✅ ANÁLISE DE PERFORMANCE:
    • Altura máxima: 2 * log₂(n + 1)
    • Menos rotações que AVL na inserção
    • Melhor para aplicações com muitas inserções
    • Overhead de cor por nó
    
    ✅ APLICAÇÕES PRÁTICAS:
    • std::map e std::set em C++
    • TreeMap e TreeSet em Java
    • Implementações de kernel Linux
    • Sistemas que precisam de inserções eficientes
    
    ✅ VANTAGENS DA RUBRO-NEGRA:
    • Menos rotações na inserção que AVL
    • Boa para aplicações write-heavy
    • Balanceamento "relaxado" mas eficiente
    • Amplamente usada em bibliotecas padrão
    
    🎯 PRÓXIMO MÓDULO: 05.5 - Árvores B e B+
    """)

if __name__ == "__main__":
    main()