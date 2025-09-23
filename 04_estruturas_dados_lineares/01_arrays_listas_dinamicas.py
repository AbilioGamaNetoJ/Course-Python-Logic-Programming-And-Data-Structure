"""
Módulo: Arrays e Listas Dinâmicas
Tópico: Implementação e Otimização de Estruturas Sequenciais
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário a Avançado

Objetivos de Aprendizado:
- Compreender diferenças entre arrays e listas
- Implementar lista dinâmica do zero
- Analisar complexidade de operações
- Otimizar operações de redimensionamento
- Implementar variações especializadas
- Comparar com implementações nativas
- Aplicar em problemas práticos
- Gerenciar memória eficientemente

Conceitos Abordados:
- Arrays estáticos vs dinâmicos
- Estratégias de redimensionamento
- Amortized analysis
- Memory layout e cache locality
- Implementação de iteradores
- Operações batch e lazy evaluation
- Estruturas especializadas (CircularArray, etc.)
- Benchmarking e profiling

Pré-requisitos:
- Conceitos básicos de listas Python
- Noções de complexidade temporal
- Compreensão de gerenciamento de memória
- Familiaridade com POO

Complexidade:
- Acesso: O(1)
- Inserção no final: O(1) amortizado
- Inserção no meio: O(n)
- Remoção: O(n) no pior caso
- Busca: O(n) linear, O(log n) se ordenado
"""

import sys
import time
import random
import gc
from typing import Any, Iterator, Optional, List, Tuple
import psutil
import os

def conceitos_arrays_listas():
    """
    Explica conceitos fundamentais de arrays e listas dinâmicas.
    """
    print("=== CONCEITOS FUNDAMENTAIS ===")
    print()
    
    print("1. ARRAYS vs LISTAS DINÂMICAS:")
    print("   ┌─────────────────┬─────────────────┬─────────────────┐")
    print("   │   CARACTERÍSTICA │      ARRAY      │ LISTA DINÂMICA  │")
    print("   ├─────────────────┼─────────────────┼─────────────────┤")
    print("   │ Tamanho         │ Fixo            │ Variável        │")
    print("   │ Memória         │ Contígua        │ Contígua        │")
    print("   │ Redimensionar   │ Não             │ Sim             │")
    print("   │ Overhead        │ Baixo           │ Médio           │")
    print("   │ Cache Locality  │ Excelente       │ Boa             │")
    print("   │ Inserção Final  │ N/A             │ O(1) amortizado │")
    print("   │ Inserção Meio   │ N/A             │ O(n)            │")
    print("   └─────────────────┴─────────────────┴─────────────────┘")
    print()
    
    print("2. ESTRATÉGIAS DE REDIMENSIONAMENTO:")
    
    def demonstrar_estrategias():
        """Demonstra diferentes estratégias de crescimento"""
        
        estrategias = [
            ("Incremento Fixo (+10)", lambda size: size + 10),
            ("Dobrar Tamanho (×2)", lambda size: size * 2),
            ("Crescimento 1.5×", lambda size: int(size * 1.5)),
            ("Crescimento Fibonacci", lambda size: size + (size // 2))
        ]
        
        print("   Análise de crescimento (partindo de 10 elementos):")
        print("   ┌─────────────────────┬─────┬─────┬─────┬─────┬─────┬─────┐")
        print("   │     ESTRATÉGIA      │  1  │  2  │  3  │  4  │  5  │  6  │")
        print("   ├─────────────────────┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        for nome, funcao in estrategias:
            tamanhos = [10]
            for _ in range(5):
                novo_tamanho = funcao(tamanhos[-1])
                tamanhos.append(novo_tamanho)
            
            linha = f"   │ {nome:19} │"
            for tamanho in tamanhos[1:]:
                linha += f" {tamanho:3} │"
            print(linha)
        
        print("   └─────────────────────┴─────┴─────┴─────┴─────┴─────┴─────┘")
        print()
        
        # Análise de complexidade amortizada
        print("   ANÁLISE AMORTIZADA (1000 inserções):")
        
        def simular_insercoes(estrategia_func, nome):
            """Simula inserções com uma estratégia"""
            capacidade = 10
            tamanho = 0
            total_copias = 0
            redimensionamentos = 0
            
            for i in range(1000):
                if tamanho >= capacidade:
                    nova_capacidade = estrategia_func(capacidade)
                    total_copias += tamanho  # Copiar elementos existentes
                    capacidade = nova_capacidade
                    redimensionamentos += 1
                
                tamanho += 1
            
            custo_amortizado = total_copias / 1000
            return redimensionamentos, total_copias, custo_amortizado
        
        print("   ┌─────────────────────┬─────────────┬─────────────┬─────────────┐")
        print("   │     ESTRATÉGIA      │ REDIMENS.   │ TOTAL CÓPIAS│ CUSTO AMORT.│")
        print("   ├─────────────────────┼─────────────┼─────────────┼─────────────┤")
        
        for nome, funcao in estrategias:
            redim, copias, custo = simular_insercoes(funcao, nome)
            print(f"   │ {nome:19} │ {redim:11} │ {copias:11} │ {custo:11.2f} │")
        
        print("   └─────────────────────┴─────────────┴─────────────┴─────────────┘")
        print("   → Crescimento exponencial oferece melhor complexidade amortizada")
        print()
    
    demonstrar_estrategias()
    
    print("3. MEMORY LAYOUT E CACHE LOCALITY:")
    
    def demonstrar_cache_locality():
        """Demonstra impacto da localidade de cache"""
        
        # Criar arrays de diferentes tamanhos
        tamanhos = [1000, 10000, 100000, 1000000]
        
        print("   Impacto do acesso sequencial vs aleatório:")
        print("   ┌─────────────┬─────────────────┬─────────────────┬─────────────┐")
        print("   │   TAMANHO   │   SEQUENCIAL    │    ALEATÓRIO    │   SPEEDUP   │")
        print("   ├─────────────┼─────────────────┼─────────────────┼─────────────┤")
        
        for tamanho in tamanhos:
            dados = list(range(tamanho))
            indices_aleatorios = list(range(tamanho))
            random.shuffle(indices_aleatorios)
            
            # Acesso sequencial
            start = time.perf_counter()
            soma_seq = 0
            for i in range(tamanho):
                soma_seq += dados[i]
            tempo_seq = time.perf_counter() - start
            
            # Acesso aleatório
            start = time.perf_counter()
            soma_rand = 0
            for i in indices_aleatorios:
                soma_rand += dados[i]
            tempo_rand = time.perf_counter() - start
            
            speedup = tempo_rand / tempo_seq
            
            print(f"   │ {tamanho:11,} │ {tempo_seq*1000:13.2f} ms │ {tempo_rand*1000:13.2f} ms │ {speedup:9.2f}x │")
        
        print("   └─────────────┴─────────────────┴─────────────────┴─────────────┘")
        print("   → Acesso sequencial é mais eficiente devido ao cache do CPU")
        print()
    
    demonstrar_cache_locality()

class ListaDinamica:
    """
    Implementação completa de uma lista dinâmica.
    """
    
    def __init__(self, capacidade_inicial=10, fator_crescimento=2.0):
        """
        Inicializa lista dinâmica.
        
        Args:
            capacidade_inicial: Capacidade inicial do array
            fator_crescimento: Fator de crescimento quando redimensionar
        """
        self._capacidade = capacidade_inicial
        self._tamanho = 0
        self._fator_crescimento = fator_crescimento
        self._dados = [None] * self._capacidade
        
        # Estatísticas para análise
        self._redimensionamentos = 0
        self._total_copias = 0
    
    def __len__(self):
        """Retorna tamanho da lista"""
        return self._tamanho
    
    def __getitem__(self, indice):
        """Acesso por índice com suporte a índices negativos"""
        if isinstance(indice, slice):
            return self._get_slice(indice)
        
        indice = self._normalizar_indice(indice)
        return self._dados[indice]
    
    def __setitem__(self, indice, valor):
        """Atribuição por índice"""
        indice = self._normalizar_indice(indice)
        self._dados[indice] = valor
    
    def __iter__(self):
        """Iterador para a lista"""
        for i in range(self._tamanho):
            yield self._dados[i]
    
    def __str__(self):
        """Representação string da lista"""
        elementos = [str(self._dados[i]) for i in range(self._tamanho)]
        return f"[{', '.join(elementos)}]"
    
    def __repr__(self):
        """Representação detalhada"""
        return f"ListaDinamica(tamanho={self._tamanho}, capacidade={self._capacidade})"
    
    def _normalizar_indice(self, indice):
        """Normaliza índice negativo e verifica bounds"""
        if indice < 0:
            indice += self._tamanho
        
        if indice < 0 or indice >= self._tamanho:
            raise IndexError(f"Índice {indice} fora do range [0, {self._tamanho-1}]")
        
        return indice
    
    def _redimensionar(self, nova_capacidade=None):
        """Redimensiona o array interno"""
        if nova_capacidade is None:
            nova_capacidade = int(self._capacidade * self._fator_crescimento)
        
        # Criar novo array
        novos_dados = [None] * nova_capacidade
        
        # Copiar dados existentes
        for i in range(self._tamanho):
            novos_dados[i] = self._dados[i]
        
        # Atualizar referências
        self._dados = novos_dados
        self._capacidade = nova_capacidade
        
        # Estatísticas
        self._redimensionamentos += 1
        self._total_copias += self._tamanho
    
    def _get_slice(self, slice_obj):
        """Implementa slicing"""
        start, stop, step = slice_obj.indices(self._tamanho)
        resultado = ListaDinamica()
        
        for i in range(start, stop, step):
            resultado.append(self._dados[i])
        
        return resultado
    
    def append(self, elemento):
        """Adiciona elemento no final - O(1) amortizado"""
        if self._tamanho >= self._capacidade:
            self._redimensionar()
        
        self._dados[self._tamanho] = elemento
        self._tamanho += 1
    
    def insert(self, indice, elemento):
        """Insere elemento em posição específica - O(n)"""
        if indice < 0:
            indice = max(0, self._tamanho + indice + 1)
        elif indice > self._tamanho:
            indice = self._tamanho
        
        if self._tamanho >= self._capacidade:
            self._redimensionar()
        
        # Deslocar elementos para a direita
        for i in range(self._tamanho, indice, -1):
            self._dados[i] = self._dados[i - 1]
        
        self._dados[indice] = elemento
        self._tamanho += 1
    
    def remove(self, elemento):
        """Remove primeira ocorrência do elemento - O(n)"""
        for i in range(self._tamanho):
            if self._dados[i] == elemento:
                self.pop(i)
                return
        
        raise ValueError(f"Elemento {elemento} não encontrado")
    
    def pop(self, indice=-1):
        """Remove e retorna elemento em índice específico - O(n)"""
        if self._tamanho == 0:
            raise IndexError("pop de lista vazia")
        
        indice = self._normalizar_indice(indice)
        elemento = self._dados[indice]
        
        # Deslocar elementos para a esquerda
        for i in range(indice, self._tamanho - 1):
            self._dados[i] = self._dados[i + 1]
        
        self._tamanho -= 1
        self._dados[self._tamanho] = None  # Limpar referência
        
        # Reduzir capacidade se muito subutilizada
        if self._tamanho < self._capacidade // 4 and self._capacidade > 10:
            self._redimensionar(self._capacidade // 2)
        
        return elemento
    
    def index(self, elemento, inicio=0, fim=None):
        """Encontra índice da primeira ocorrência - O(n)"""
        if fim is None:
            fim = self._tamanho
        
        for i in range(inicio, min(fim, self._tamanho)):
            if self._dados[i] == elemento:
                return i
        
        raise ValueError(f"Elemento {elemento} não encontrado")
    
    def count(self, elemento):
        """Conta ocorrências do elemento - O(n)"""
        contador = 0
        for i in range(self._tamanho):
            if self._dados[i] == elemento:
                contador += 1
        return contador
    
    def extend(self, iteravel):
        """Estende lista com elementos de iterável - O(k)"""
        for elemento in iteravel:
            self.append(elemento)
    
    def clear(self):
        """Remove todos os elementos - O(1)"""
        for i in range(self._tamanho):
            self._dados[i] = None
        self._tamanho = 0
    
    def reverse(self):
        """Inverte ordem dos elementos in-place - O(n)"""
        for i in range(self._tamanho // 2):
            j = self._tamanho - 1 - i
            self._dados[i], self._dados[j] = self._dados[j], self._dados[i]
    
    def sort(self, key=None, reverse=False):
        """Ordena lista in-place - O(n log n)"""
        # Extrair elementos válidos
        elementos = [self._dados[i] for i in range(self._tamanho)]
        
        # Ordenar
        elementos.sort(key=key, reverse=reverse)
        
        # Recolocar na lista
        for i, elemento in enumerate(elementos):
            self._dados[i] = elemento
    
    def copy(self):
        """Cria cópia shallow da lista - O(n)"""
        nova_lista = ListaDinamica(self._capacidade, self._fator_crescimento)
        for i in range(self._tamanho):
            nova_lista.append(self._dados[i])
        return nova_lista
    
    # Métodos de análise e debugging
    def get_stats(self):
        """Retorna estatísticas da lista"""
        return {
            'tamanho': self._tamanho,
            'capacidade': self._capacidade,
            'utilizacao': self._tamanho / self._capacidade * 100,
            'redimensionamentos': self._redimensionamentos,
            'total_copias': self._total_copias,
            'fator_crescimento': self._fator_crescimento
        }
    
    def get_memory_usage(self):
        """Estima uso de memória"""
        # Tamanho aproximado em bytes
        overhead_objeto = sys.getsizeof(self)
        tamanho_array = sys.getsizeof(self._dados)
        tamanho_elementos = sum(sys.getsizeof(self._dados[i]) 
                              for i in range(self._tamanho) 
                              if self._dados[i] is not None)
        
        return {
            'overhead_objeto': overhead_objeto,
            'array_interno': tamanho_array,
            'elementos': tamanho_elementos,
            'total': overhead_objeto + tamanho_array + tamanho_elementos,
            'desperdicio': (self._capacidade - self._tamanho) * 8  # Aproximado
        }

def demonstrar_lista_dinamica():
    """
    Demonstra uso e performance da lista dinâmica implementada.
    """
    print("=== DEMONSTRAÇÃO DA LISTA DINÂMICA ===")
    print()
    
    print("1. OPERAÇÕES BÁSICAS:")
    
    # Criar lista
    lista = ListaDinamica(capacidade_inicial=5, fator_crescimento=2.0)
    
    print(f"   Lista inicial: {lista}")
    print(f"   Stats: {lista.get_stats()}")
    print()
    
    # Adicionar elementos
    print("   Adicionando elementos 1-10:")
    for i in range(1, 11):
        lista.append(i)
        if i in [5, 8, 10]:  # Mostrar redimensionamentos
            print(f"   → Após adicionar {i}: {lista}")
            print(f"     Stats: capacidade={lista._capacidade}, redimensionamentos={lista._redimensionamentos}")
    
    print()
    
    # Operações diversas
    print("   Operações diversas:")
    print(f"   → Elemento no índice 3: {lista[3]}")
    print(f"   → Slice [2:7]: {lista[2:7]}")
    print(f"   → Índice do elemento 7: {lista.index(7)}")
    print(f"   → Contagem do elemento 5: {lista.count(5)}")
    print()
    
    # Inserção no meio
    print("   Inserindo 99 no índice 3:")
    lista.insert(3, 99)
    print(f"   → Resultado: {lista}")
    print()
    
    # Remoção
    print("   Removendo elemento 99:")
    lista.remove(99)
    print(f"   → Resultado: {lista}")
    print()
    
    print("2. COMPARAÇÃO DE PERFORMANCE:")
    
    def benchmark_operacoes():
        """Compara performance com lista nativa do Python"""
        
        tamanhos = [1000, 10000, 100000]
        
        print("   Tempo de inserção no final (ms):")
        print("   ┌─────────────┬─────────────────┬─────────────────┬─────────────┐")
        print("   │   TAMANHO   │ LISTA DINÂMICA  │  LISTA PYTHON   │   SPEEDUP   │")
        print("   ├─────────────┼─────────────────┼─────────────────┼─────────────┤")
        
        for tamanho in tamanhos:
            # Lista dinâmica
            lista_din = ListaDinamica()
            start = time.perf_counter()
            for i in range(tamanho):
                lista_din.append(i)
            tempo_din = time.perf_counter() - start
            
            # Lista Python
            lista_py = []
            start = time.perf_counter()
            for i in range(tamanho):
                lista_py.append(i)
            tempo_py = time.perf_counter() - start
            
            speedup = tempo_din / tempo_py
            
            print(f"   │ {tamanho:11,} │ {tempo_din*1000:13.2f} ms │ {tempo_py*1000:13.2f} ms │ {speedup:9.2f}x │")
        
        print("   └─────────────┴─────────────────┴─────────────────┴─────────────┘")
        print()
        
        # Teste de acesso aleatório
        print("   Tempo de acesso aleatório (1M acessos):")
        
        tamanho_teste = 10000
        num_acessos = 1000000
        
        # Preparar dados
        lista_din = ListaDinamica()
        lista_py = []
        for i in range(tamanho_teste):
            lista_din.append(i)
            lista_py.append(i)
        
        indices = [random.randint(0, tamanho_teste-1) for _ in range(num_acessos)]
        
        # Lista dinâmica
        start = time.perf_counter()
        soma_din = 0
        for idx in indices:
            soma_din += lista_din[idx]
        tempo_din = time.perf_counter() - start
        
        # Lista Python
        start = time.perf_counter()
        soma_py = 0
        for idx in indices:
            soma_py += lista_py[idx]
        tempo_py = time.perf_counter() - start
        
        print(f"   → Lista Dinâmica: {tempo_din*1000:.2f}ms")
        print(f"   → Lista Python:   {tempo_py*1000:.2f}ms")
        print(f"   → Speedup:        {tempo_din/tempo_py:.2f}x")
        print()
    
    benchmark_operacoes()
    
    print("3. ANÁLISE DE MEMÓRIA:")
    
    def analisar_memoria():
        """Analisa uso de memória"""
        
        tamanhos = [100, 1000, 10000]
        
        print("   Uso de memória por tamanho:")
        print("   ┌─────────────┬─────────────────┬─────────────────┬─────────────┐")
        print("   │   TAMANHO   │ LISTA DINÂMICA  │  LISTA PYTHON   │ OVERHEAD %  │")
        print("   ├─────────────┼─────────────────┼─────────────────┼─────────────┤")
        
        for tamanho in tamanhos:
            # Lista dinâmica
            lista_din = ListaDinamica()
            for i in range(tamanho):
                lista_din.append(i)
            
            memoria_din = lista_din.get_memory_usage()['total']
            
            # Lista Python
            lista_py = list(range(tamanho))
            memoria_py = sys.getsizeof(lista_py)
            for item in lista_py:
                memoria_py += sys.getsizeof(item)
            
            overhead = (memoria_din / memoria_py - 1) * 100
            
            print(f"   │ {tamanho:11,} │ {memoria_din:13,} B │ {memoria_py:13,} B │ {overhead:9.1f}% │")
        
        print("   └─────────────┴─────────────────┴─────────────────┴─────────────┘")
        print()
        
        # Análise detalhada para um caso
        lista_exemplo = ListaDinamica()
        for i in range(1000):
            lista_exemplo.append(i)
        
        stats = lista_exemplo.get_stats()
        memoria = lista_exemplo.get_memory_usage()
        
        print("   Análise detalhada (1000 elementos):")
        print(f"   → Utilização da capacidade: {stats['utilizacao']:.1f}%")
        print(f"   → Redimensionamentos: {stats['redimensionamentos']}")
        print(f"   → Total de cópias: {stats['total_copias']}")
        print(f"   → Desperdício de memória: {memoria['desperdicio']} bytes")
        print()
    
    analisar_memoria()

if __name__ == "__main__":
    print("MÓDULO 4.1 - ARRAYS E LISTAS DINÂMICAS")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceitos_arrays_listas()
    print("\n" + "="*50 + "\n")
    
    demonstrar_lista_dinamica()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 4.1 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Diferenças entre arrays e listas dinâmicas")
    print("✅ Estratégias de redimensionamento e análise amortizada")
    print("✅ Implementação completa de lista dinâmica")
    print("✅ Cache locality e otimizações de memória")
    print("✅ Comparação de performance com listas nativas")
    print("✅ Análise de uso de memória e overhead")
    print("✅ Operações avançadas (slicing, iteradores)")
    print("✅ Debugging e profiling de estruturas de dados")
    print("\n➡️  Próximo: Módulo 4.2 - Pilhas (Stacks)")