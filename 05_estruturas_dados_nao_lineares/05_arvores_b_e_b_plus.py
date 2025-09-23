"""
MÓDULO 05.5 - ÁRVORES B E B+
============================

Objetivos de Aprendizado:
- Compreender árvores B e suas propriedades
- Implementar operações em árvores B
- Entender árvores B+ e suas vantagens
- Aplicar em sistemas de banco de dados
- Comparar com outras estruturas de árvore

Conceitos Abordados:
- Definição e propriedades das árvores B
- Operações: busca, inserção, remoção
- Divisão e merge de nós
- Árvores B+ e suas características
- Otimização para acessos a disco
- Índices de banco de dados
- Paginação e cache

Pré-requisitos:
- Árvores binárias de busca
- Conceitos de balanceamento
- Estruturas de dados básicas

Complexidade das Operações:
- Busca: O(log n)
- Inserção: O(log n)
- Remoção: O(log n)
- Todas garantidas mesmo no pior caso
"""

from typing import List, Optional, Any, Tuple
import math
import time
import random


class NoB:
    """
    Nó de uma Árvore B.
    
    Propriedades:
    - Contém múltiplas chaves (até 2t-1)
    - Pode ter múltiplos filhos (até 2t)
    - Todas as folhas estão no mesmo nível
    """
    
    def __init__(self, grau_minimo: int, folha: bool = False):
        """
        Inicializa nó da árvore B.
        
        Args:
            grau_minimo: Grau mínimo t da árvore
            folha: Se o nó é uma folha
        """
        self.grau_minimo = grau_minimo
        self.chaves = []  # Lista de chaves
        self.filhos = []  # Lista de filhos
        self.folha = folha
        
        # Limites baseados no grau mínimo t:
        # - Mínimo de chaves: t-1 (exceto raiz)
        # - Máximo de chaves: 2t-1
        # - Mínimo de filhos: t (exceto raiz e folhas)
        # - Máximo de filhos: 2t
        self.max_chaves = 2 * grau_minimo - 1
        self.min_chaves = grau_minimo - 1
    
    def esta_cheio(self) -> bool:
        """Verifica se o nó está cheio."""
        return len(self.chaves) == self.max_chaves
    
    def esta_minimo(self) -> bool:
        """Verifica se o nó tem o mínimo de chaves."""
        return len(self.chaves) == self.min_chaves
    
    def buscar(self, chave: Any) -> Tuple[Optional['NoB'], int]:
        """
        Busca uma chave no nó e seus descendentes.
        
        Args:
            chave: Chave a ser buscada
        
        Returns:
            Tupla (nó, índice) onde a chave foi encontrada, ou (None, -1)
        """
        i = 0
        # Encontrar posição onde a chave deveria estar
        while i < len(self.chaves) and chave > self.chaves[i]:
            i += 1
        
        # Se encontrou a chave
        if i < len(self.chaves) and chave == self.chaves[i]:
            return (self, i)
        
        # Se é folha e não encontrou, a chave não existe
        if self.folha:
            return (None, -1)
        
        # Buscar no filho apropriado
        return self.filhos[i].buscar(chave)
    
    def inserir_nao_cheio(self, chave: Any):
        """
        Insere chave em nó que não está cheio.
        
        Args:
            chave: Chave a ser inserida
        """
        i = len(self.chaves) - 1
        
        if self.folha:
            # Inserir na folha
            self.chaves.append(None)
            while i >= 0 and self.chaves[i] > chave:
                self.chaves[i + 1] = self.chaves[i]
                i -= 1
            self.chaves[i + 1] = chave
        else:
            # Encontrar filho onde inserir
            while i >= 0 and self.chaves[i] > chave:
                i -= 1
            i += 1
            
            # Se filho está cheio, dividir primeiro
            if self.filhos[i].esta_cheio():
                self.dividir_filho(i)
                if self.chaves[i] < chave:
                    i += 1
            
            self.filhos[i].inserir_nao_cheio(chave)
    
    def dividir_filho(self, indice: int):
        """
        Divide um filho cheio.
        
        Args:
            indice: Índice do filho a ser dividido
        """
        t = self.grau_minimo
        filho_cheio = self.filhos[indice]
        novo_filho = NoB(t, filho_cheio.folha)
        
        # Mover metade das chaves para o novo nó
        novo_filho.chaves = filho_cheio.chaves[t:]
        filho_cheio.chaves = filho_cheio.chaves[:t-1]
        
        # Se não é folha, mover metade dos filhos também
        if not filho_cheio.folha:
            novo_filho.filhos = filho_cheio.filhos[t:]
            filho_cheio.filhos = filho_cheio.filhos[:t]
        
        # Inserir novo filho na posição correta
        self.filhos.insert(indice + 1, novo_filho)
        
        # Mover chave do meio para cima
        chave_meio = filho_cheio.chaves[t-1] if len(filho_cheio.chaves) >= t else filho_cheio.chaves[-1]
        self.chaves.insert(indice, chave_meio)
    
    def remover(self, chave: Any):
        """
        Remove uma chave do nó.
        
        Args:
            chave: Chave a ser removida
        """
        i = 0
        while i < len(self.chaves) and self.chaves[i] < chave:
            i += 1
        
        if i < len(self.chaves) and self.chaves[i] == chave:
            # Chave encontrada neste nó
            if self.folha:
                # Caso 1: Chave em folha
                self.chaves.pop(i)
            else:
                # Caso 2: Chave em nó interno
                self._remover_de_no_interno(i)
        elif not self.folha:
            # Caso 3: Chave não está neste nó
            # Verificar se precisa fazer merge ou empréstimo
            if len(self.filhos[i].chaves) == self.min_chaves:
                self._corrigir_filho_minimo(i)
            
            # Reajustar índice se houve mudanças
            if i > len(self.chaves):
                i = len(self.chaves)
            
            self.filhos[i].remover(chave)
    
    def _remover_de_no_interno(self, indice: int):
        """Remove chave de nó interno."""
        chave = self.chaves[indice]
        
        # Caso 2a: Filho esquerdo tem chaves suficientes
        if len(self.filhos[indice].chaves) > self.min_chaves:
            predecessor = self._obter_predecessor(indice)
            self.chaves[indice] = predecessor
            self.filhos[indice].remover(predecessor)
        
        # Caso 2b: Filho direito tem chaves suficientes
        elif len(self.filhos[indice + 1].chaves) > self.min_chaves:
            sucessor = self._obter_sucessor(indice)
            self.chaves[indice] = sucessor
            self.filhos[indice + 1].remover(sucessor)
        
        # Caso 2c: Ambos os filhos têm mínimo de chaves
        else:
            self._merge_filhos(indice)
            self.filhos[indice].remover(chave)
    
    def _obter_predecessor(self, indice: int) -> Any:
        """Obtém predecessor de uma chave."""
        atual = self.filhos[indice]
        while not atual.folha:
            atual = atual.filhos[-1]
        return atual.chaves[-1]
    
    def _obter_sucessor(self, indice: int) -> Any:
        """Obtém sucessor de uma chave."""
        atual = self.filhos[indice + 1]
        while not atual.folha:
            atual = atual.filhos[0]
        return atual.chaves[0]
    
    def _corrigir_filho_minimo(self, indice: int):
        """Corrige filho que tem menos que o mínimo de chaves."""
        # Tentar emprestar do irmão esquerdo
        if indice > 0 and len(self.filhos[indice - 1].chaves) > self.min_chaves:
            self._emprestar_do_anterior(indice)
        
        # Tentar emprestar do irmão direito
        elif indice < len(self.filhos) - 1 and len(self.filhos[indice + 1].chaves) > self.min_chaves:
            self._emprestar_do_proximo(indice)
        
        # Fazer merge com irmão
        else:
            if indice < len(self.filhos) - 1:
                self._merge_filhos(indice)
            else:
                self._merge_filhos(indice - 1)
    
    def _emprestar_do_anterior(self, indice: int):
        """Empresta chave do irmão anterior."""
        filho = self.filhos[indice]
        irmao = self.filhos[indice - 1]
        
        # Mover chave do pai para o filho
        filho.chaves.insert(0, self.chaves[indice - 1])
        
        # Mover última chave do irmão para o pai
        self.chaves[indice - 1] = irmao.chaves.pop()
        
        # Se não é folha, mover último filho também
        if not filho.folha:
            filho.filhos.insert(0, irmao.filhos.pop())
    
    def _emprestar_do_proximo(self, indice: int):
        """Empresta chave do próximo irmão."""
        filho = self.filhos[indice]
        irmao = self.filhos[indice + 1]
        
        # Mover chave do pai para o filho
        filho.chaves.append(self.chaves[indice])
        
        # Mover primeira chave do irmão para o pai
        self.chaves[indice] = irmao.chaves.pop(0)
        
        # Se não é folha, mover primeiro filho também
        if not filho.folha:
            filho.filhos.append(irmao.filhos.pop(0))
    
    def _merge_filhos(self, indice: int):
        """Faz merge de dois filhos."""
        filho = self.filhos[indice]
        irmao = self.filhos[indice + 1]
        
        # Mover chave do pai para o filho
        filho.chaves.append(self.chaves[indice])
        
        # Mover todas as chaves do irmão para o filho
        filho.chaves.extend(irmao.chaves)
        
        # Se não é folha, mover filhos também
        if not filho.folha:
            filho.filhos.extend(irmao.filhos)
        
        # Remover chave e filho do nó atual
        self.chaves.pop(indice)
        self.filhos.pop(indice + 1)


class ArvoreB:
    """
    Implementação de Árvore B.
    
    Propriedades:
    - Todas as folhas estão no mesmo nível
    - Nós têm entre t-1 e 2t-1 chaves (exceto raiz)
    - Nós internos têm entre t e 2t filhos
    - Operações garantem O(log n)
    """
    
    def __init__(self, grau_minimo: int = 3):
        """
        Inicializa árvore B.
        
        Args:
            grau_minimo: Grau mínimo t (padrão 3)
        """
        self.grau_minimo = grau_minimo
        self.raiz = NoB(grau_minimo, folha=True)
        self.altura = 1
        
        # Estatísticas
        self.num_nos = 1
        self.num_chaves = 0
        self.operacoes_busca = 0
        self.operacoes_insercao = 0
        self.operacoes_remocao = 0
    
    def buscar(self, chave: Any) -> bool:
        """
        Busca uma chave na árvore.
        
        Args:
            chave: Chave a ser buscada
        
        Returns:
            True se a chave existe, False caso contrário
        """
        self.operacoes_busca += 1
        no, indice = self.raiz.buscar(chave)
        return no is not None
    
    def inserir(self, chave: Any):
        """
        Insere uma chave na árvore.
        
        Args:
            chave: Chave a ser inserida
        """
        self.operacoes_insercao += 1
        
        # Se raiz está cheia, criar nova raiz
        if self.raiz.esta_cheio():
            nova_raiz = NoB(self.grau_minimo, folha=False)
            nova_raiz.filhos.append(self.raiz)
            nova_raiz.dividir_filho(0)
            self.raiz = nova_raiz
            self.altura += 1
            self.num_nos += 1
        
        self.raiz.inserir_nao_cheio(chave)
        self.num_chaves += 1
    
    def remover(self, chave: Any):
        """
        Remove uma chave da árvore.
        
        Args:
            chave: Chave a ser removida
        """
        self.operacoes_remocao += 1
        self.raiz.remover(chave)
        
        # Se raiz ficou vazia e não é folha, ajustar
        if len(self.raiz.chaves) == 0 and not self.raiz.folha:
            self.raiz = self.raiz.filhos[0]
            self.altura -= 1
            self.num_nos -= 1
        
        self.num_chaves -= 1
    
    def listar_ordenado(self) -> List[Any]:
        """
        Retorna todas as chaves em ordem.
        
        Returns:
            Lista ordenada de chaves
        """
        resultado = []
        self._percorrer_em_ordem(self.raiz, resultado)
        return resultado
    
    def _percorrer_em_ordem(self, no: NoB, resultado: List[Any]):
        """Percorre árvore em ordem."""
        i = 0
        while i < len(no.chaves):
            # Visitar filho esquerdo
            if not no.folha:
                self._percorrer_em_ordem(no.filhos[i], resultado)
            
            # Visitar chave atual
            resultado.append(no.chaves[i])
            i += 1
        
        # Visitar último filho
        if not no.folha:
            self._percorrer_em_ordem(no.filhos[i], resultado)
    
    def buscar_range(self, min_chave: Any, max_chave: Any) -> List[Any]:
        """
        Busca chaves em um intervalo.
        
        Args:
            min_chave: Chave mínima
            max_chave: Chave máxima
        
        Returns:
            Lista de chaves no intervalo
        """
        resultado = []
        self._buscar_range_recursivo(self.raiz, min_chave, max_chave, resultado)
        return resultado
    
    def _buscar_range_recursivo(self, no: NoB, min_chave: Any, max_chave: Any, resultado: List[Any]):
        """Busca range recursivamente."""
        i = 0
        
        while i < len(no.chaves):
            # Se não é folha, visitar filho esquerdo se necessário
            if not no.folha and no.chaves[i] > min_chave:
                self._buscar_range_recursivo(no.filhos[i], min_chave, max_chave, resultado)
            
            # Se chave está no range, adicionar
            if min_chave <= no.chaves[i] <= max_chave:
                resultado.append(no.chaves[i])
            
            # Se chave é maior que max, parar
            if no.chaves[i] > max_chave:
                return
            
            i += 1
        
        # Visitar último filho se necessário
        if not no.folha and (not no.chaves or no.chaves[-1] < max_chave):
            self._buscar_range_recursivo(no.filhos[i], min_chave, max_chave, resultado)
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas da árvore."""
        return {
            'altura': self.altura,
            'num_nos': self.num_nos,
            'num_chaves': self.num_chaves,
            'grau_minimo': self.grau_minimo,
            'operacoes_busca': self.operacoes_busca,
            'operacoes_insercao': self.operacoes_insercao,
            'operacoes_remocao': self.operacoes_remocao,
            'fator_ocupacao': self._calcular_fator_ocupacao()
        }
    
    def _calcular_fator_ocupacao(self) -> float:
        """Calcula fator de ocupação médio dos nós."""
        if self.num_nos == 0:
            return 0.0
        
        max_chaves_por_no = 2 * self.grau_minimo - 1
        max_chaves_total = self.num_nos * max_chaves_por_no
        
        return self.num_chaves / max_chaves_total if max_chaves_total > 0 else 0.0
    
    def visualizar(self) -> str:
        """
        Cria representação visual da árvore.
        
        Returns:
            String com visualização da árvore
        """
        if not self.raiz:
            return "Árvore vazia"
        
        resultado = []
        self._visualizar_recursivo(self.raiz, 0, resultado)
        return "\n".join(resultado)
    
    def _visualizar_recursivo(self, no: NoB, nivel: int, resultado: List[str]):
        """Visualiza árvore recursivamente."""
        indent = "  " * nivel
        chaves_str = ", ".join(str(chave) for chave in no.chaves)
        tipo = "FOLHA" if no.folha else "INTERNO"
        resultado.append(f"{indent}[{tipo}] {chaves_str}")
        
        if not no.folha:
            for filho in no.filhos:
                self._visualizar_recursivo(filho, nivel + 1, resultado)


class NoBPlus:
    """
    Nó de uma Árvore B+.
    
    Diferenças da Árvore B:
    - Dados apenas nas folhas
    - Nós internos só para navegação
    - Folhas ligadas em lista
    """
    
    def __init__(self, grau_minimo: int, folha: bool = False):
        """
        Inicializa nó da árvore B+.
        
        Args:
            grau_minimo: Grau mínimo da árvore
            folha: Se o nó é uma folha
        """
        self.grau_minimo = grau_minimo
        self.chaves = []
        self.folha = folha
        
        if folha:
            self.valores = []  # Dados nas folhas
            self.proximo = None  # Ponteiro para próxima folha
        else:
            self.filhos = []  # Ponteiros para filhos
        
        self.max_chaves = 2 * grau_minimo - 1
        self.min_chaves = grau_minimo - 1
    
    def esta_cheio(self) -> bool:
        """Verifica se o nó está cheio."""
        return len(self.chaves) == self.max_chaves
    
    def buscar(self, chave: Any) -> Optional[Any]:
        """
        Busca uma chave no nó.
        
        Args:
            chave: Chave a ser buscada
        
        Returns:
            Valor associado à chave ou None
        """
        if self.folha:
            # Buscar nas folhas
            for i, k in enumerate(self.chaves):
                if k == chave:
                    return self.valores[i]
            return None
        else:
            # Buscar no filho apropriado
            i = 0
            while i < len(self.chaves) and chave >= self.chaves[i]:
                i += 1
            return self.filhos[i].buscar(chave)


class ArvoreBPlus:
    """
    Implementação de Árvore B+.
    
    Vantagens sobre Árvore B:
    - Range queries mais eficientes
    - Scans sequenciais otimizados
    - Melhor para sistemas de banco de dados
    """
    
    def __init__(self, grau_minimo: int = 3):
        """
        Inicializa árvore B+.
        
        Args:
            grau_minimo: Grau mínimo (padrão 3)
        """
        self.grau_minimo = grau_minimo
        self.raiz = NoBPlus(grau_minimo, folha=True)
        self.primeira_folha = self.raiz
        
        # Estatísticas
        self.num_chaves = 0
        self.altura = 1
        self.operacoes_busca = 0
        self.operacoes_insercao = 0
    
    def buscar(self, chave: Any) -> Optional[Any]:
        """
        Busca uma chave na árvore.
        
        Args:
            chave: Chave a ser buscada
        
        Returns:
            Valor associado à chave ou None
        """
        self.operacoes_busca += 1
        return self.raiz.buscar(chave)
    
    def inserir(self, chave: Any, valor: Any):
        """
        Insere par chave-valor na árvore.
        
        Args:
            chave: Chave a ser inserida
            valor: Valor associado
        """
        self.operacoes_insercao += 1
        
        if self.raiz.esta_cheio():
            # Criar nova raiz
            nova_raiz = NoBPlus(self.grau_minimo, folha=False)
            nova_raiz.filhos.append(self.raiz)
            self._dividir_filho_b_plus(nova_raiz, 0)
            self.raiz = nova_raiz
            self.altura += 1
        
        self._inserir_nao_cheio_b_plus(self.raiz, chave, valor)
        self.num_chaves += 1
    
    def _inserir_nao_cheio_b_plus(self, no: NoBPlus, chave: Any, valor: Any):
        """Insere em nó não cheio da B+."""
        if no.folha:
            # Inserir na folha mantendo ordem
            i = 0
            while i < len(no.chaves) and no.chaves[i] < chave:
                i += 1
            
            no.chaves.insert(i, chave)
            no.valores.insert(i, valor)
        else:
            # Encontrar filho apropriado
            i = 0
            while i < len(no.chaves) and chave >= no.chaves[i]:
                i += 1
            
            if no.filhos[i].esta_cheio():
                self._dividir_filho_b_plus(no, i)
                if chave >= no.chaves[i]:
                    i += 1
            
            self._inserir_nao_cheio_b_plus(no.filhos[i], chave, valor)
    
    def _dividir_filho_b_plus(self, pai: NoBPlus, indice: int):
        """Divide filho cheio na B+."""
        t = self.grau_minimo
        filho_cheio = pai.filhos[indice]
        novo_filho = NoBPlus(t, filho_cheio.folha)
        
        meio = len(filho_cheio.chaves) // 2
        
        if filho_cheio.folha:
            # Dividir folha
            novo_filho.chaves = filho_cheio.chaves[meio:]
            novo_filho.valores = filho_cheio.valores[meio:]
            filho_cheio.chaves = filho_cheio.chaves[:meio]
            filho_cheio.valores = filho_cheio.valores[:meio]
            
            # Ligar folhas
            novo_filho.proximo = filho_cheio.proximo
            filho_cheio.proximo = novo_filho
            
            # Chave para subir é a primeira do novo nó
            chave_subir = novo_filho.chaves[0]
        else:
            # Dividir nó interno
            novo_filho.chaves = filho_cheio.chaves[meio+1:]
            novo_filho.filhos = filho_cheio.filhos[meio+1:]
            chave_subir = filho_cheio.chaves[meio]
            filho_cheio.chaves = filho_cheio.chaves[:meio]
            filho_cheio.filhos = filho_cheio.filhos[:meio+1]
        
        # Inserir novo filho no pai
        pai.filhos.insert(indice + 1, novo_filho)
        pai.chaves.insert(indice, chave_subir)
    
    def buscar_range(self, min_chave: Any, max_chave: Any) -> List[Tuple[Any, Any]]:
        """
        Busca eficiente por intervalo usando lista ligada de folhas.
        
        Args:
            min_chave: Chave mínima
            max_chave: Chave máxima
        
        Returns:
            Lista de tuplas (chave, valor) no intervalo
        """
        resultado = []
        
        # Encontrar primeira folha com chaves >= min_chave
        folha_atual = self._encontrar_folha_inicial(min_chave)
        
        # Percorrer folhas sequencialmente
        while folha_atual:
            for i, chave in enumerate(folha_atual.chaves):
                if chave > max_chave:
                    return resultado
                if chave >= min_chave:
                    resultado.append((chave, folha_atual.valores[i]))
            
            folha_atual = folha_atual.proximo
        
        return resultado
    
    def _encontrar_folha_inicial(self, chave: Any) -> Optional[NoBPlus]:
        """Encontra primeira folha que pode conter a chave."""
        atual = self.raiz
        
        while not atual.folha:
            i = 0
            while i < len(atual.chaves) and chave >= atual.chaves[i]:
                i += 1
            atual = atual.filhos[i]
        
        return atual
    
    def listar_todos(self) -> List[Tuple[Any, Any]]:
        """
        Lista todos os pares chave-valor em ordem.
        
        Returns:
            Lista ordenada de tuplas (chave, valor)
        """
        resultado = []
        folha_atual = self.primeira_folha
        
        while folha_atual:
            for i, chave in enumerate(folha_atual.chaves):
                resultado.append((chave, folha_atual.valores[i]))
            folha_atual = folha_atual.proximo
        
        return resultado
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas da árvore B+."""
        return {
            'altura': self.altura,
            'num_chaves': self.num_chaves,
            'grau_minimo': self.grau_minimo,
            'operacoes_busca': self.operacoes_busca,
            'operacoes_insercao': self.operacoes_insercao
        }


# Aplicações Práticas
class IndiceBaseDados:
    """
    Simulação de índice de banco de dados usando Árvore B+.
    """
    
    def __init__(self, grau_minimo: int = 50):
        """
        Inicializa índice.
        
        Args:
            grau_minimo: Grau mínimo otimizado para disco
        """
        self.indice = ArvoreBPlus(grau_minimo)
        self.cache_hits = 0
        self.cache_misses = 0
        self.cache = {}  # Simulação de cache
        self.max_cache_size = 100
    
    def inserir_registro(self, id_registro: int, dados: dict):
        """
        Insere registro no índice.
        
        Args:
            id_registro: ID único do registro
            dados: Dados do registro
        """
        self.indice.inserir(id_registro, dados)
        
        # Invalidar cache se necessário
        if id_registro in self.cache:
            del self.cache[id_registro]
    
    def buscar_registro(self, id_registro: int) -> Optional[dict]:
        """
        Busca registro por ID.
        
        Args:
            id_registro: ID do registro
        
        Returns:
            Dados do registro ou None
        """
        # Verificar cache primeiro
        if id_registro in self.cache:
            self.cache_hits += 1
            return self.cache[id_registro]
        
        # Buscar no índice
        self.cache_misses += 1
        dados = self.indice.buscar(id_registro)
        
        # Adicionar ao cache
        if dados and len(self.cache) < self.max_cache_size:
            self.cache[id_registro] = dados
        
        return dados
    
    def buscar_range_ids(self, min_id: int, max_id: int) -> List[dict]:
        """
        Busca registros em um intervalo de IDs.
        
        Args:
            min_id: ID mínimo
            max_id: ID máximo
        
        Returns:
            Lista de registros no intervalo
        """
        resultados = self.indice.buscar_range(min_id, max_id)
        return [dados for _, dados in resultados]
    
    def obter_estatisticas_cache(self) -> dict:
        """Retorna estatísticas do cache."""
        total_acessos = self.cache_hits + self.cache_misses
        hit_rate = self.cache_hits / total_acessos if total_acessos > 0 else 0
        
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate': hit_rate,
            'cache_size': len(self.cache)
        }


class CacheMultiNivel:
    """
    Sistema de cache multi-nível usando árvores B.
    """
    
    def __init__(self):
        """Inicializa cache com 3 níveis."""
        # L1: Cache rápido (pequeno)
        self.l1 = ArvoreB(grau_minimo=2)
        self.l1_max_size = 10
        self.l1_size = 0
        
        # L2: Cache médio
        self.l2 = ArvoreB(grau_minimo=3)
        self.l2_max_size = 50
        self.l2_size = 0
        
        # Storage: Armazenamento principal
        self.storage = ArvoreB(grau_minimo=10)
        
        # Estatísticas
        self.l1_hits = 0
        self.l2_hits = 0
        self.storage_hits = 0
        self.misses = 0
    
    def get(self, chave: Any) -> Optional[Any]:
        """
        Busca valor no cache multi-nível.
        
        Args:
            chave: Chave a ser buscada
        
        Returns:
            Valor encontrado ou None
        """
        # Tentar L1 primeiro
        if self.l1.buscar(chave):
            self.l1_hits += 1
            return f"L1_DATA_{chave}"
        
        # Tentar L2
        if self.l2.buscar(chave):
            self.l2_hits += 1
            # Promover para L1 se houver espaço
            if self.l1_size < self.l1_max_size:
                self.l1.inserir(chave)
                self.l1_size += 1
            return f"L2_DATA_{chave}"
        
        # Tentar Storage
        if self.storage.buscar(chave):
            self.storage_hits += 1
            # Promover para L2 se houver espaço
            if self.l2_size < self.l2_max_size:
                self.l2.inserir(chave)
                self.l2_size += 1
            return f"STORAGE_DATA_{chave}"
        
        # Não encontrado
        self.misses += 1
        return None
    
    def put(self, chave: Any):
        """
        Armazena valor no storage.
        
        Args:
            chave: Chave a ser armazenada
        """
        self.storage.inserir(chave)
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas do cache."""
        total = self.l1_hits + self.l2_hits + self.storage_hits + self.misses
        
        return {
            'l1_hits': self.l1_hits,
            'l2_hits': self.l2_hits,
            'storage_hits': self.storage_hits,
            'misses': self.misses,
            'total_requests': total,
            'l1_hit_rate': self.l1_hits / total if total > 0 else 0,
            'l2_hit_rate': self.l2_hits / total if total > 0 else 0,
            'overall_hit_rate': (self.l1_hits + self.l2_hits + self.storage_hits) / total if total > 0 else 0
        }


# Funções de Demonstração e Benchmark
def demonstrar_arvore_b():
    """Demonstra operações básicas da Árvore B."""
    print("=== DEMONSTRAÇÃO: ÁRVORE B ===\n")
    
    # Criar árvore B com grau mínimo 3
    arvore = ArvoreB(grau_minimo=3)
    
    # Inserir valores
    valores = [10, 20, 5, 6, 12, 30, 7, 17, 15, 18, 22, 25, 35, 40]
    print("Inserindo valores:", valores)
    
    for valor in valores:
        arvore.inserir(valor)
    
    print(f"\nÁrvore após inserções:")
    print(arvore.visualizar())
    
    # Buscar valores
    print(f"\nBuscas:")
    for valor in [15, 25, 100]:
        encontrado = arvore.buscar(valor)
        print(f"Buscar {valor}: {'Encontrado' if encontrado else 'Não encontrado'}")
    
    # Listar em ordem
    print(f"\nValores em ordem: {arvore.listar_ordenado()}")
    
    # Busca por range
    range_resultado = arvore.buscar_range(10, 25)
    print(f"Range [10, 25]: {range_resultado}")
    
    # Estatísticas
    stats = arvore.obter_estatisticas()
    print(f"\nEstatísticas:")
    for chave, valor in stats.items():
        print(f"  {chave}: {valor}")


def demonstrar_arvore_b_plus():
    """Demonstra operações da Árvore B+."""
    print("\n=== DEMONSTRAÇÃO: ÁRVORE B+ ===\n")
    
    # Criar árvore B+
    arvore_plus = ArvoreBPlus(grau_minimo=3)
    
    # Inserir pares chave-valor
    dados = [
        (1, "Alice"),
        (5, "Bob"),
        (10, "Carol"),
        (15, "David"),
        (20, "Eve"),
        (25, "Frank"),
        (30, "Grace"),
        (35, "Henry")
    ]
    
    print("Inserindo pares chave-valor:")
    for chave, valor in dados:
        arvore_plus.inserir(chave, valor)
        print(f"  {chave}: {valor}")
    
    # Buscar valores específicos
    print(f"\nBuscas:")
    for chave in [10, 25, 100]:
        valor = arvore_plus.buscar(chave)
        print(f"Chave {chave}: {valor if valor else 'Não encontrado'}")
    
    # Busca por range (muito eficiente na B+)
    print(f"\nBusca por range [10, 25]:")
    range_resultado = arvore_plus.buscar_range(10, 25)
    for chave, valor in range_resultado:
        print(f"  {chave}: {valor}")
    
    # Listar todos (scan sequencial eficiente)
    print(f"\nTodos os registros (scan sequencial):")
    todos = arvore_plus.listar_todos()
    for chave, valor in todos:
        print(f"  {chave}: {valor}")


def demonstrar_aplicacoes_praticas():
    """Demonstra aplicações práticas."""
    print("\n=== DEMONSTRAÇÃO: APLICAÇÕES PRÁTICAS ===\n")
    
    # Índice de banco de dados
    print("1. ÍNDICE DE BANCO DE DADOS:")
    indice = IndiceBaseDados(grau_minimo=5)
    
    # Inserir registros
    registros = [
        (1001, {"nome": "João", "idade": 30, "cidade": "São Paulo"}),
        (1005, {"nome": "Maria", "idade": 25, "cidade": "Rio de Janeiro"}),
        (1010, {"nome": "Pedro", "idade": 35, "cidade": "Belo Horizonte"}),
        (1015, {"nome": "Ana", "idade": 28, "cidade": "Salvador"}),
        (1020, {"nome": "Carlos", "idade": 32, "cidade": "Brasília"})
    ]
    
    for id_reg, dados in registros:
        indice.inserir_registro(id_reg, dados)
    
    # Buscar registros
    print("Buscando registro 1010:")
    registro = indice.buscar_registro(1010)
    print(f"  {registro}")
    
    # Buscar por range
    print("\nRegistros com ID entre 1005 e 1015:")
    range_registros = indice.buscar_range_ids(1005, 1015)
    for reg in range_registros:
        print(f"  {reg}")
    
    # Estatísticas do cache
    stats_cache = indice.obter_estatisticas_cache()
    print(f"\nEstatísticas do cache:")
    for chave, valor in stats_cache.items():
        print(f"  {chave}: {valor}")
    
    # Cache multi-nível
    print("\n2. CACHE MULTI-NÍVEL:")
    cache = CacheMultiNivel()
    
    # Armazenar dados
    for i in range(1, 21):
        cache.put(i)
    
    # Simular acessos
    acessos = [1, 2, 3, 1, 2, 4, 5, 1, 6, 7, 2, 8, 9, 1]
    print(f"Simulando acessos: {acessos}")
    
    for chave in acessos:
        valor = cache.get(chave)
        print(f"  get({chave}): {valor}")
    
    # Estatísticas do cache
    stats_multi = cache.obter_estatisticas()
    print(f"\nEstatísticas do cache multi-nível:")
    for chave, valor in stats_multi.items():
        print(f"  {chave}: {valor:.3f}" if isinstance(valor, float) else f"  {chave}: {valor}")


def benchmark_arvores_b():
    """Compara performance das árvores B e B+ com outras estruturas."""
    print("\n=== BENCHMARK: ÁRVORES B vs OUTRAS ESTRUTURAS ===\n")
    
    tamanhos = [1000, 5000, 10000]
    
    for n in tamanhos:
        print(f"Testando com {n} elementos:")
        
        # Preparar dados
        dados = list(range(n))
        random.shuffle(dados)
        
        # Árvore B
        start_time = time.time()
        arvore_b = ArvoreB(grau_minimo=10)
        for valor in dados:
            arvore_b.inserir(valor)
        
        # Teste de busca
        for _ in range(100):
            chave = random.randint(0, n-1)
            arvore_b.buscar(chave)
        
        tempo_b = time.time() - start_time
        
        # Árvore B+
        start_time = time.time()
        arvore_b_plus = ArvoreBPlus(grau_minimo=10)
        for valor in dados:
            arvore_b_plus.inserir(valor, f"dados_{valor}")
        
        # Teste de busca
        for _ in range(100):
            chave = random.randint(0, n-1)
            arvore_b_plus.buscar(chave)
        
        tempo_b_plus = time.time() - start_time
        
        # Lista Python (para comparação)
        start_time = time.time()
        lista = []
        for valor in dados:
            lista.append(valor)
        lista.sort()
        
        # Teste de busca binária
        import bisect
        for _ in range(100):
            chave = random.randint(0, n-1)
            pos = bisect.bisect_left(lista, chave)
            if pos < len(lista) and lista[pos] == chave:
                pass  # Encontrado
        
        tempo_lista = time.time() - start_time
        
        # Dicionário Python
        start_time = time.time()
        dicionario = {}
        for valor in dados:
            dicionario[valor] = f"dados_{valor}"
        
        # Teste de busca
        for _ in range(100):
            chave = random.randint(0, n-1)
            if chave in dicionario:
                pass  # Encontrado
        
        tempo_dict = time.time() - start_time
        
        print(f"  Árvore B:      {tempo_b:.4f}s")
        print(f"  Árvore B+:     {tempo_b_plus:.4f}s")
        print(f"  Lista Python:  {tempo_lista:.4f}s")
        print(f"  Dict Python:   {tempo_dict:.4f}s")
        print()
        
        # Teste específico de range query para B+
        print(f"  Teste de Range Query (100 ranges):")
        
        # B+ Tree
        start_time = time.time()
        for _ in range(100):
            min_val = random.randint(0, n//2)
            max_val = min_val + random.randint(1, n//10)
            arvore_b_plus.buscar_range(min_val, max_val)
        tempo_range_b_plus = time.time() - start_time
        
        # Lista Python
        start_time = time.time()
        for _ in range(100):
            min_val = random.randint(0, n//2)
            max_val = min_val + random.randint(1, n//10)
            # Simular range query em lista
            resultado = [x for x in lista if min_val <= x <= max_val]
        tempo_range_lista = time.time() - start_time
        
        print(f"    B+ Range:    {tempo_range_b_plus:.4f}s")
        print(f"    Lista Range: {tempo_range_lista:.4f}s")
        print(f"    Speedup:     {tempo_range_lista/tempo_range_b_plus:.2f}x")
        print()


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 05.5 - ÁRVORES B E B+")
    print("=" * 40)
    
    demonstrar_arvore_b()
    demonstrar_arvore_b_plus()
    demonstrar_aplicacoes_praticas()
    benchmark_arvores_b()
    
    print("\n" + "=" * 40)
    print("CONCLUSÃO DO MÓDULO 05.5")
    print("=" * 40)
    print("""
Principais Aprendizados:

1. ÁRVORES B:
   • Otimizadas para minimizar acessos ao disco
   • Nós com múltiplas chaves reduzem altura da árvore
   • Operações O(log n) garantidas
   • Ideais para sistemas de armazenamento

2. ÁRVORES B+:
   • Dados apenas nas folhas
   • Nós internos só para navegação
   • Folhas ligadas para range queries eficientes
   • Melhor para scans sequenciais

3. APLICAÇÕES PRÁTICAS:
   • Índices de banco de dados
   • Sistemas de arquivos
   • Caches multi-nível
   • Qualquer sistema que precisa de acesso eficiente a disco

4. VANTAGENS SOBRE OUTRAS ESTRUTURAS:
   • Menos acessos ao disco que árvores binárias
   • Range queries muito eficientes (especialmente B+)
   • Melhor localidade de referência
   • Otimizadas para hardware moderno

5. CONSIDERAÇÕES DE IMPLEMENTAÇÃO:
   • Grau mínimo deve ser escolhido baseado no tamanho da página
   • B+ é preferível quando range queries são comuns
   • Cache pode melhorar significativamente a performance

Próximo módulo: Heaps e Filas de Prioridade
    """)


if __name__ == "__main__":
    main()