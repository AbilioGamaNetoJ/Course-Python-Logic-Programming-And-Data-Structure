"""
Módulo: Estruturas de Dados Não-Lineares - Árvores (Conceitos Fundamentais)
Tópico: Introdução às Árvores e Terminologia
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário

Objetivos de Aprendizado:
- Compreender o conceito de estruturas não-lineares
- Dominar a terminologia de árvores
- Implementar árvore binária básica
- Entender diferentes tipos de travessia
- Analisar propriedades das árvores
- Implementar operações fundamentais
- Visualizar estruturas de árvore
- Comparar com estruturas lineares

Conceitos Abordados:
- Definição de árvore
- Terminologia (nó, raiz, folha, altura, profundidade)
- Árvore binária
- Travessias (in-order, pre-order, post-order, level-order)
- Propriedades matemáticas
- Representações em memória
- Operações básicas (inserção, busca, remoção)
- Balanceamento

Pré-requisitos:
- Estruturas lineares (listas, pilhas, filas)
- Recursão
- Conceitos de ponteiros/referências
- Análise de complexidade

Complexidade:
- Busca: O(n) no pior caso, O(log n) em árvore balanceada
- Inserção: O(n) no pior caso, O(log n) em árvore balanceada
- Remoção: O(n) no pior caso, O(log n) em árvore balanceada
- Travessia: O(n) para visitar todos os nós
- Espaço: O(n) para armazenar n nós, O(h) para recursão (h = altura)
"""

from typing import Optional, List, Any, Callable, Iterator, Tuple, Dict
from collections import deque
from dataclasses import dataclass
import math
import json

def introducao_arvores():
    """
    Introduz os conceitos fundamentais de árvores.
    """
    print("=== ESTRUTURAS DE DADOS NÃO-LINEARES: ÁRVORES ===")
    print()
    
    print("1. DEFINIÇÃO E CONCEITOS:")
    print()
    print("   Uma ÁRVORE é uma estrutura de dados hierárquica composta por nós")
    print("   conectados por arestas, onde:")
    print("   • Existe exatamente um nó raiz")
    print("   • Cada nó pode ter zero ou mais filhos")
    print("   • Não existem ciclos (estrutura acíclica)")
    print("   • Existe exatamente um caminho entre quaisquer dois nós")
    print()
    
    print("2. TERMINOLOGIA FUNDAMENTAL:")
    print()
    print("   ┌─────────────────────────────────────────────────────────────────────────────┐")
    print("   │                            ÁRVORE EXEMPLO                                  │")
    print("   │                                                                             │")
    print("   │                                  A (raiz)                                   │")
    print("   │                                 ╱ ╲                                        │")
    print("   │                                B   C                                       │")
    print("   │                               ╱ ╲   ╲                                      │")
    print("   │                              D   E   F                                     │")
    print("   │                                 ╱ ╲                                        │")
    print("   │                                G   H (folhas)                              │")
    print("   │                                                                             │")
    print("   │  TERMOS:                                                                    │")
    print("   │  • Nó (Node): Elemento da árvore (A, B, C, D, E, F, G, H)                 │")
    print("   │  • Raiz (Root): Nó sem pai (A)                                             │")
    print("   │  • Folha (Leaf): Nó sem filhos (D, G, H, F)                               │")
    print("   │  • Pai (Parent): Nó com filhos (A é pai de B e C)                         │")
    print("   │  • Filho (Child): Nó com pai (B e C são filhos de A)                      │")
    print("   │  • Irmão (Sibling): Nós com mesmo pai (B e C são irmãos)                  │")
    print("   │  • Ancestral: Nó no caminho até a raiz (A é ancestral de G)               │")
    print("   │  • Descendente: Nó alcançável descendo (G é descendente de A)             │")
    print("   │  • Subárvore: Árvore formada por um nó e seus descendentes                │")
    print("   │                                                                             │")
    print("   └─────────────────────────────────────────────────────────────────────────────┘")
    print()
    
    print("3. PROPRIEDADES IMPORTANTES:")
    print()
    print("   • Altura (Height): Maior distância da raiz até uma folha")
    print("   • Profundidade (Depth): Distância de um nó até a raiz")
    print("   • Nível (Level): Profundidade + 1")
    print("   • Grau: Número máximo de filhos de qualquer nó")
    print("   • Tamanho: Número total de nós")
    print()
    print("   Exemplo da árvore acima:")
    print("   • Altura: 3 (caminho A → B → E → G)")
    print("   • Profundidade de G: 3")
    print("   • Nível de G: 4")
    print("   • Grau: 2 (máximo de filhos)")
    print("   • Tamanho: 8 nós")
    print()
    
    print("4. TIPOS DE ÁRVORES:")
    print()
    print("   ┌─────────────────┬─────────────────┬─────────────────────────────────────────┐")
    print("   │      TIPO       │   RESTRIÇÃO     │              CARACTERÍSTICAS            │")
    print("   ├─────────────────┼─────────────────┼─────────────────────────────────────────┤")
    print("   │ Árvore Geral    │ Nenhuma         │ Qualquer número de filhos               │")
    print("   │ Árvore Binária  │ ≤ 2 filhos      │ Cada nó tem no máximo 2 filhos          │")
    print("   │ Árvore Completa │ Todos níveis    │ Todos os níveis preenchidos             │")
    print("   │                 │ preenchidos     │ exceto possivelmente o último           │")
    print("   │ Árvore Cheia    │ 0 ou 2 filhos   │ Cada nó tem 0 ou exatamente 2 filhos    │")
    print("   │ Árvore Perfeita │ Completa +      │ Todos os níveis completamente           │")
    print("   │                 │ todas folhas    │ preenchidos                             │")
    print("   │                 │ no mesmo nível  │                                         │")
    print("   │ Árvore Balanceada│ Diferença de   │ Altura das subárvores difere            │")
    print("   │                 │ altura ≤ 1      │ no máximo em 1                          │")
    print("   └─────────────────┴─────────────────┴─────────────────────────────────────────┘")
    print()

class NoArvore:
    """
    Nó básico para árvore binária.
    """
    
    def __init__(self, valor: Any):
        """
        Inicializa nó da árvore.
        
        Args:
            valor: Valor armazenado no nó
        """
        self.valor = valor
        self.esquerda: Optional['NoArvore'] = None
        self.direita: Optional['NoArvore'] = None
        self.pai: Optional['NoArvore'] = None
    
    def eh_folha(self) -> bool:
        """Verifica se o nó é uma folha"""
        return self.esquerda is None and self.direita is None
    
    def eh_raiz(self) -> bool:
        """Verifica se o nó é a raiz"""
        return self.pai is None
    
    def tem_filho_esquerdo(self) -> bool:
        """Verifica se tem filho esquerdo"""
        return self.esquerda is not None
    
    def tem_filho_direito(self) -> bool:
        """Verifica se tem filho direito"""
        return self.direita is not None
    
    def tem_ambos_filhos(self) -> bool:
        """Verifica se tem ambos os filhos"""
        return self.esquerda is not None and self.direita is not None
    
    def tem_um_filho(self) -> bool:
        """Verifica se tem exatamente um filho"""
        return (self.esquerda is None) != (self.direita is None)
    
    def obter_filho_unico(self) -> Optional['NoArvore']:
        """Retorna o único filho se existir"""
        if self.esquerda is not None and self.direita is None:
            return self.esquerda
        elif self.direita is not None and self.esquerda is None:
            return self.direita
        return None
    
    def __str__(self) -> str:
        return str(self.valor)
    
    def __repr__(self) -> str:
        return f"NoArvore({self.valor})"

class ArvoreBinaria:
    """
    Implementação de árvore binária com operações fundamentais.
    """
    
    def __init__(self):
        """Inicializa árvore vazia"""
        self.raiz: Optional[NoArvore] = None
        self._tamanho = 0
    
    def esta_vazia(self) -> bool:
        """Verifica se a árvore está vazia"""
        return self.raiz is None
    
    def tamanho(self) -> int:
        """Retorna o número de nós na árvore"""
        return self._tamanho
    
    def inserir(self, valor: Any) -> NoArvore:
        """
        Insere valor na árvore (inserção simples, não ordenada).
        
        Args:
            valor: Valor a ser inserido
            
        Returns:
            Nó inserido
        """
        novo_no = NoArvore(valor)
        
        if self.esta_vazia():
            self.raiz = novo_no
        else:
            # Inserção level-order (primeiro espaço disponível)
            fila = deque([self.raiz])
            
            while fila:
                no_atual = fila.popleft()
                
                if no_atual.esquerda is None:
                    no_atual.esquerda = novo_no
                    novo_no.pai = no_atual
                    break
                elif no_atual.direita is None:
                    no_atual.direita = novo_no
                    novo_no.pai = no_atual
                    break
                else:
                    fila.append(no_atual.esquerda)
                    fila.append(no_atual.direita)
        
        self._tamanho += 1
        return novo_no
    
    def buscar(self, valor: Any) -> Optional[NoArvore]:
        """
        Busca valor na árvore.
        
        Args:
            valor: Valor a ser buscado
            
        Returns:
            Nó encontrado ou None
        """
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, no: Optional[NoArvore], valor: Any) -> Optional[NoArvore]:
        """Busca recursiva"""
        if no is None:
            return None
        
        if no.valor == valor:
            return no
        
        # Buscar na subárvore esquerda
        resultado = self._buscar_recursivo(no.esquerda, valor)
        if resultado is not None:
            return resultado
        
        # Buscar na subárvore direita
        return self._buscar_recursivo(no.direita, valor)
    
    def remover(self, valor: Any) -> bool:
        """
        Remove valor da árvore.
        
        Args:
            valor: Valor a ser removido
            
        Returns:
            True se removido, False se não encontrado
        """
        no_para_remover = self.buscar(valor)
        if no_para_remover is None:
            return False
        
        self._remover_no(no_para_remover)
        self._tamanho -= 1
        return True
    
    def _remover_no(self, no: NoArvore) -> None:
        """Remove nó específico da árvore"""
        if no.eh_folha():
            # Caso 1: Nó é folha
            if no.eh_raiz():
                self.raiz = None
            elif no.pai.esquerda == no:
                no.pai.esquerda = None
            else:
                no.pai.direita = None
        
        elif no.tem_um_filho():
            # Caso 2: Nó tem um filho
            filho = no.obter_filho_unico()
            
            if no.eh_raiz():
                self.raiz = filho
                filho.pai = None
            elif no.pai.esquerda == no:
                no.pai.esquerda = filho
                filho.pai = no.pai
            else:
                no.pai.direita = filho
                filho.pai = no.pai
        
        else:
            # Caso 3: Nó tem dois filhos
            # Encontrar sucessor in-order (menor valor na subárvore direita)
            sucessor = self._encontrar_minimo(no.direita)
            
            # Substituir valor do nó pelo valor do sucessor
            no.valor = sucessor.valor
            
            # Remover sucessor (que tem no máximo um filho)
            self._remover_no(sucessor)
    
    def _encontrar_minimo(self, no: NoArvore) -> NoArvore:
        """Encontra o nó com menor valor na subárvore"""
        while no.esquerda is not None:
            no = no.esquerda
        return no
    
    def altura(self) -> int:
        """Calcula altura da árvore"""
        return self._altura_recursiva(self.raiz)
    
    def _altura_recursiva(self, no: Optional[NoArvore]) -> int:
        """Calcula altura recursivamente"""
        if no is None:
            return -1  # Convenção: árvore vazia tem altura -1
        
        altura_esquerda = self._altura_recursiva(no.esquerda)
        altura_direita = self._altura_recursiva(no.direita)
        
        return 1 + max(altura_esquerda, altura_direita)
    
    def profundidade(self, valor: Any) -> int:
        """
        Calcula profundidade de um nó.
        
        Args:
            valor: Valor do nó
            
        Returns:
            Profundidade do nó ou -1 se não encontrado
        """
        return self._profundidade_recursiva(self.raiz, valor, 0)
    
    def _profundidade_recursiva(self, no: Optional[NoArvore], valor: Any, prof_atual: int) -> int:
        """Calcula profundidade recursivamente"""
        if no is None:
            return -1
        
        if no.valor == valor:
            return prof_atual
        
        # Buscar na subárvore esquerda
        prof_esquerda = self._profundidade_recursiva(no.esquerda, valor, prof_atual + 1)
        if prof_esquerda != -1:
            return prof_esquerda
        
        # Buscar na subárvore direita
        return self._profundidade_recursiva(no.direita, valor, prof_atual + 1)
    
    def eh_balanceada(self) -> bool:
        """Verifica se a árvore está balanceada"""
        return self._verificar_balanceamento(self.raiz) != -1
    
    def _verificar_balanceamento(self, no: Optional[NoArvore]) -> int:
        """
        Verifica balanceamento recursivamente.
        
        Returns:
            Altura se balanceada, -1 se não balanceada
        """
        if no is None:
            return 0
        
        altura_esquerda = self._verificar_balanceamento(no.esquerda)
        if altura_esquerda == -1:
            return -1
        
        altura_direita = self._verificar_balanceamento(no.direita)
        if altura_direita == -1:
            return -1
        
        # Verificar se diferença de altura é maior que 1
        if abs(altura_esquerda - altura_direita) > 1:
            return -1
        
        return 1 + max(altura_esquerda, altura_direita)
    
    def eh_completa(self) -> bool:
        """Verifica se a árvore é completa"""
        if self.esta_vazia():
            return True
        
        fila = deque([self.raiz])
        encontrou_no_incompleto = False
        
        while fila:
            no_atual = fila.popleft()
            
            # Verificar filho esquerdo
            if no_atual.esquerda is not None:
                if encontrou_no_incompleto:
                    return False
                fila.append(no_atual.esquerda)
            else:
                encontrou_no_incompleto = True
            
            # Verificar filho direito
            if no_atual.direita is not None:
                if encontrou_no_incompleto:
                    return False
                fila.append(no_atual.direita)
            else:
                encontrou_no_incompleto = True
        
        return True
    
    def eh_cheia(self) -> bool:
        """Verifica se a árvore é cheia (cada nó tem 0 ou 2 filhos)"""
        return self._verificar_arvore_cheia(self.raiz)
    
    def _verificar_arvore_cheia(self, no: Optional[NoArvore]) -> bool:
        """Verifica se árvore é cheia recursivamente"""
        if no is None:
            return True
        
        # Se é folha, está OK
        if no.eh_folha():
            return True
        
        # Se tem apenas um filho, não é cheia
        if no.tem_um_filho():
            return False
        
        # Se tem dois filhos, verificar recursivamente
        return (self._verificar_arvore_cheia(no.esquerda) and 
                self._verificar_arvore_cheia(no.direita))
    
    def eh_perfeita(self) -> bool:
        """Verifica se a árvore é perfeita"""
        altura = self.altura()
        return self._verificar_arvore_perfeita(self.raiz, altura, 0)
    
    def _verificar_arvore_perfeita(self, no: Optional[NoArvore], altura: int, nivel: int) -> bool:
        """Verifica se árvore é perfeita recursivamente"""
        if no is None:
            return True
        
        # Se é folha, deve estar no último nível
        if no.eh_folha():
            return nivel == altura
        
        # Se não é folha, deve ter ambos os filhos
        if not no.tem_ambos_filhos():
            return False
        
        # Verificar recursivamente
        return (self._verificar_arvore_perfeita(no.esquerda, altura, nivel + 1) and
                self._verificar_arvore_perfeita(no.direita, altura, nivel + 1))
    
    # Métodos de travessia
    def travessia_in_order(self) -> List[Any]:
        """Travessia in-order (esquerda, raiz, direita)"""
        resultado = []
        self._in_order_recursivo(self.raiz, resultado)
        return resultado
    
    def _in_order_recursivo(self, no: Optional[NoArvore], resultado: List[Any]) -> None:
        """Travessia in-order recursiva"""
        if no is not None:
            self._in_order_recursivo(no.esquerda, resultado)
            resultado.append(no.valor)
            self._in_order_recursivo(no.direita, resultado)
    
    def travessia_pre_order(self) -> List[Any]:
        """Travessia pre-order (raiz, esquerda, direita)"""
        resultado = []
        self._pre_order_recursivo(self.raiz, resultado)
        return resultado
    
    def _pre_order_recursivo(self, no: Optional[NoArvore], resultado: List[Any]) -> None:
        """Travessia pre-order recursiva"""
        if no is not None:
            resultado.append(no.valor)
            self._pre_order_recursivo(no.esquerda, resultado)
            self._pre_order_recursivo(no.direita, resultado)
    
    def travessia_post_order(self) -> List[Any]:
        """Travessia post-order (esquerda, direita, raiz)"""
        resultado = []
        self._post_order_recursivo(self.raiz, resultado)
        return resultado
    
    def _post_order_recursivo(self, no: Optional[NoArvore], resultado: List[Any]) -> None:
        """Travessia post-order recursiva"""
        if no is not None:
            self._post_order_recursivo(no.esquerda, resultado)
            self._post_order_recursivo(no.direita, resultado)
            resultado.append(no.valor)
    
    def travessia_level_order(self) -> List[Any]:
        """Travessia level-order (por níveis)"""
        if self.esta_vazia():
            return []
        
        resultado = []
        fila = deque([self.raiz])
        
        while fila:
            no_atual = fila.popleft()
            resultado.append(no_atual.valor)
            
            if no_atual.esquerda is not None:
                fila.append(no_atual.esquerda)
            if no_atual.direita is not None:
                fila.append(no_atual.direita)
        
        return resultado
    
    def obter_nos_por_nivel(self) -> List[List[Any]]:
        """Retorna nós agrupados por nível"""
        if self.esta_vazia():
            return []
        
        resultado = []
        fila = deque([(self.raiz, 0)])
        nivel_atual = 0
        nos_nivel_atual = []
        
        while fila:
            no, nivel = fila.popleft()
            
            if nivel > nivel_atual:
                resultado.append(nos_nivel_atual)
                nos_nivel_atual = []
                nivel_atual = nivel
            
            nos_nivel_atual.append(no.valor)
            
            if no.esquerda is not None:
                fila.append((no.esquerda, nivel + 1))
            if no.direita is not None:
                fila.append((no.direita, nivel + 1))
        
        if nos_nivel_atual:
            resultado.append(nos_nivel_atual)
        
        return resultado
    
    def visualizar(self) -> str:
        """Cria representação visual da árvore"""
        if self.esta_vazia():
            return "Árvore vazia"
        
        linhas = []
        self._construir_visualizacao(self.raiz, "", True, linhas)
        return "\n".join(linhas)
    
    def _construir_visualizacao(self, no: Optional[NoArvore], prefixo: str, 
                               eh_ultimo: bool, linhas: List[str]) -> None:
        """Constrói visualização recursivamente"""
        if no is not None:
            linhas.append(prefixo + ("└── " if eh_ultimo else "├── ") + str(no.valor))
            
            # Preparar prefixo para filhos
            prefixo_filho = prefixo + ("    " if eh_ultimo else "│   ")
            
            # Adicionar filhos (direita primeiro para visualização correta)
            filhos = []
            if no.esquerda is not None:
                filhos.append(("E", no.esquerda))
            if no.direita is not None:
                filhos.append(("D", no.direita))
            
            for i, (lado, filho) in enumerate(filhos):
                eh_ultimo_filho = (i == len(filhos) - 1)
                linhas.append(prefixo_filho + ("└── " if eh_ultimo_filho else "├── ") + f"({lado})")
                self._construir_visualizacao(filho, prefixo_filho + ("    " if eh_ultimo_filho else "│   "), 
                                           True, linhas)
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas da árvore"""
        if self.esta_vazia():
            return {
                'tamanho': 0,
                'altura': -1,
                'eh_balanceada': True,
                'eh_completa': True,
                'eh_cheia': True,
                'eh_perfeita': True,
                'numero_folhas': 0,
                'numero_nos_internos': 0
            }
        
        folhas = self._contar_folhas(self.raiz)
        nos_internos = self.tamanho() - folhas
        
        return {
            'tamanho': self.tamanho(),
            'altura': self.altura(),
            'eh_balanceada': self.eh_balanceada(),
            'eh_completa': self.eh_completa(),
            'eh_cheia': self.eh_cheia(),
            'eh_perfeita': self.eh_perfeita(),
            'numero_folhas': folhas,
            'numero_nos_internos': nos_internos,
            'fator_ramificacao': nos_internos / self.tamanho() if self.tamanho() > 0 else 0
        }
    
    def _contar_folhas(self, no: Optional[NoArvore]) -> int:
        """Conta número de folhas recursivamente"""
        if no is None:
            return 0
        
        if no.eh_folha():
            return 1
        
        return self._contar_folhas(no.esquerda) + self._contar_folhas(no.direita)
    
    def __str__(self) -> str:
        if self.esta_vazia():
            return "ArvoreBinaria(vazia)"
        return f"ArvoreBinaria(tamanho={self.tamanho()}, altura={self.altura()})"
    
    def __len__(self) -> int:
        return self.tamanho()

def demonstrar_conceitos_arvores():
    """
    Demonstra os conceitos fundamentais de árvores.
    """
    print("=== DEMONSTRAÇÃO DOS CONCEITOS ===")
    print()
    
    # Criar árvore exemplo
    arvore = ArvoreBinaria()
    
    print("1. CONSTRUINDO ÁRVORE:")
    print()
    
    # Inserir valores
    valores = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    for valor in valores:
        arvore.inserir(valor)
        print(f"   Inserindo '{valor}' → Tamanho: {arvore.tamanho()}")
    
    print(f"\n   Árvore construída:")
    print("   " + "\n   ".join(arvore.visualizar().split("\n")))
    print()
    
    print("2. PROPRIEDADES DA ÁRVORE:")
    print()
    stats = arvore.obter_estatisticas()
    print(f"   • Tamanho: {stats['tamanho']} nós")
    print(f"   • Altura: {stats['altura']}")
    print(f"   • Número de folhas: {stats['numero_folhas']}")
    print(f"   • Número de nós internos: {stats['numero_nos_internos']}")
    print(f"   • É balanceada: {stats['eh_balanceada']}")
    print(f"   • É completa: {stats['eh_completa']}")
    print(f"   • É cheia: {stats['eh_cheia']}")
    print(f"   • É perfeita: {stats['eh_perfeita']}")
    print()
    
    print("3. TRAVESSIAS:")
    print()
    print(f"   • In-order:    {arvore.travessia_in_order()}")
    print(f"   • Pre-order:   {arvore.travessia_pre_order()}")
    print(f"   • Post-order:  {arvore.travessia_post_order()}")
    print(f"   • Level-order: {arvore.travessia_level_order()}")
    print()
    
    print("4. NÍVEL POR NÍVEL:")
    print()
    niveis = arvore.obter_nos_por_nivel()
    for i, nivel in enumerate(niveis):
        print(f"   Nível {i}: {nivel}")
    print()
    
    print("5. OPERAÇÕES DE BUSCA:")
    print()
    for valor in ['A', 'E', 'X']:
        no_encontrado = arvore.buscar(valor)
        if no_encontrado:
            profundidade = arvore.profundidade(valor)
            print(f"   Buscar '{valor}': Encontrado na profundidade {profundidade}")
        else:
            print(f"   Buscar '{valor}': Não encontrado")
    print()
    
    print("6. REMOÇÃO:")
    print()
    print(f"   Antes da remoção: {arvore.travessia_level_order()}")
    
    # Remover um nó folha
    arvore.remover('G')
    print(f"   Após remover 'G': {arvore.travessia_level_order()}")
    
    # Remover um nó com um filho
    arvore.remover('C')
    print(f"   Após remover 'C': {arvore.travessia_level_order()}")
    
    print(f"\n   Árvore final:")
    print("   " + "\n   ".join(arvore.visualizar().split("\n")))
    print()

def comparar_travessias():
    """
    Compara diferentes tipos de travessia com exemplos visuais.
    """
    print("=== COMPARAÇÃO DE TRAVESSIAS ===")
    print()
    
    # Criar árvore específica para demonstrar travessias
    arvore = ArvoreBinaria()
    
    # Construir árvore manualmente para ter controle da estrutura
    arvore.raiz = NoArvore('F')
    arvore.raiz.esquerda = NoArvore('B')
    arvore.raiz.direita = NoArvore('G')
    arvore.raiz.esquerda.esquerda = NoArvore('A')
    arvore.raiz.esquerda.direita = NoArvore('D')
    arvore.raiz.esquerda.direita.esquerda = NoArvore('C')
    arvore.raiz.esquerda.direita.direita = NoArvore('E')
    arvore.raiz.direita.direita = NoArvore('I')
    arvore.raiz.direita.direita.esquerda = NoArvore('H')
    arvore._tamanho = 9
    
    print("   ÁRVORE PARA DEMONSTRAÇÃO:")
    print()
    print("                F")
    print("              /   \\")
    print("             B     G")
    print("           /  \\     \\")
    print("          A    D     I")
    print("              / \\   /")
    print("             C   E H")
    print()
    
    print("   TRAVESSIAS E SUAS APLICAÇÕES:")
    print()
    
    print("   1. IN-ORDER (Esquerda → Raiz → Direita):")
    in_order = arvore.travessia_in_order()
    print(f"      Resultado: {in_order}")
    print("      Aplicação: Em árvores de busca binária, produz sequência ordenada")
    print("      Uso: Imprimir elementos em ordem, validar BST")
    print()
    
    print("   2. PRE-ORDER (Raiz → Esquerda → Direita):")
    pre_order = arvore.travessia_pre_order()
    print(f"      Resultado: {pre_order}")
    print("      Aplicação: Criar cópia da árvore, serialização")
    print("      Uso: Backup, transmissão de dados, parsing de expressões")
    print()
    
    print("   3. POST-ORDER (Esquerda → Direita → Raiz):")
    post_order = arvore.travessia_post_order()
    print(f"      Resultado: {post_order}")
    print("      Aplicação: Deletar árvore, calcular tamanho, avaliação de expressões")
    print("      Uso: Limpeza de memória, cálculos bottom-up")
    print()
    
    print("   4. LEVEL-ORDER (Por níveis):")
    level_order = arvore.travessia_level_order()
    print(f"      Resultado: {level_order}")
    print("      Aplicação: Busca em largura, imprimir por níveis")
    print("      Uso: Encontrar caminho mais curto, visualização")
    print()
    
    print("   COMPLEXIDADE DAS TRAVESSIAS:")
    print("   • Tempo: O(n) - visita cada nó exatamente uma vez")
    print("   • Espaço: O(h) - pilha de recursão proporcional à altura")
    print("   • Espaço level-order: O(w) - fila proporcional à largura máxima")
    print()

if __name__ == "__main__":
    print("MÓDULO 5.1 - ÁRVORES: CONCEITOS FUNDAMENTAIS")
    print("=" * 60)
    print()
    
    # Executando todas as seções
    introducao_arvores()
    print("\n" + "="*60 + "\n")
    
    demonstrar_conceitos_arvores()
    print("\n" + "="*60 + "\n")
    
    comparar_travessias()
    print("\n" + "="*60 + "\n")
    
    print("🎓 MÓDULO 5.1 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceitos fundamentais de árvores")
    print("✅ Terminologia (nó, raiz, folha, altura, profundidade)")
    print("✅ Tipos de árvores (completa, cheia, perfeita, balanceada)")
    print("✅ Implementação de árvore binária")
    print("✅ Operações básicas (inserção, busca, remoção)")
    print("✅ Travessias (in-order, pre-order, post-order, level-order)")
    print("✅ Propriedades e estatísticas")
    print("✅ Visualização de árvores")
    print("✅ Análise de complexidade")
    print()
    print("➡️  Próximo: Módulo 5.2 - Árvores de Busca Binária (BST)")