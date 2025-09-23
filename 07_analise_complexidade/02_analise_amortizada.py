"""
MÓDULO 07.2 - ANÁLISE AMORTIZADA
================================

Objetivos de Aprendizado:
- Compreender análise amortizada vs análise de pior caso
- Dominar método agregado de análise
- Aplicar método contábil (accounting method)
- Utilizar método do potencial (potential method)
- Analisar estruturas de dados dinâmicas
- Implementar estruturas com análise amortizada
- Comparar diferentes métodos de análise

Conceitos Abordados:
- Análise amortizada vs pior caso
- Método agregado (aggregate method)
- Método contábil (accounting method)
- Método do potencial (potential method)
- Custo amortizado
- Invariantes de custo
- Estruturas dinâmicas
- Redimensionamento automático

Estruturas Analisadas:
- Array dinâmico (Dynamic Array)
- Pilha com multipop
- Contador binário
- Árvore splay
- Tabela hash com redimensionamento
- Union-Find com compressão de caminho

Pré-requisitos:
- Notação Big O
- Estruturas de dados básicas
- Análise de algoritmos
- Matemática discreta
"""

import time
import math
import random
import matplotlib.pyplot as plt
from typing import List, Optional, Any, Tuple, Dict
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import numpy as np


class TipoAnalise(Enum):
    """Tipos de análise de complexidade."""
    PIOR_CASO = "Pior Caso"
    CASO_MEDIO = "Caso Médio"
    AMORTIZADA = "Amortizada"


@dataclass
class OperacaoAnalise:
    """Representa uma operação para análise."""
    nome: str
    custo_real: int
    custo_amortizado: int
    credito_usado: int = 0
    credito_armazenado: int = 0
    potencial_antes: int = 0
    potencial_depois: int = 0
    observacoes: str = ""


@dataclass
class ResultadoAnaliseAmortizada:
    """Resultado da análise amortizada."""
    estrutura: str
    metodo_analise: str
    operacoes: List[OperacaoAnalise] = field(default_factory=list)
    custo_total_real: int = 0
    custo_total_amortizado: int = 0
    custo_amortizado_por_operacao: float = 0.0
    invariante_mantido: bool = True
    observacoes: str = ""


class AnalisadorAmortizado:
    """
    Classe para análise amortizada de estruturas de dados.
    """
    
    def __init__(self):
        """Inicializa o analisador."""
        self.resultados: List[ResultadoAnaliseAmortizada] = []
        self.operacoes_atuais: List[OperacaoAnalise] = []
    
    def iniciar_analise(self, estrutura: str, metodo: str):
        """
        Inicia uma nova análise.
        
        Args:
            estrutura: Nome da estrutura de dados
            metodo: Método de análise (agregado, contábil, potencial)
        """
        self.operacoes_atuais = []
        self.estrutura_atual = estrutura
        self.metodo_atual = metodo
    
    def registrar_operacao(self, operacao: OperacaoAnalise):
        """
        Registra uma operação na análise atual.
        
        Args:
            operacao: Operação a ser registrada
        """
        self.operacoes_atuais.append(operacao)
    
    def finalizar_analise(self, observacoes: str = "") -> ResultadoAnaliseAmortizada:
        """
        Finaliza a análise atual e calcula resultados.
        
        Args:
            observacoes: Observações sobre a análise
        
        Returns:
            Resultado da análise amortizada
        """
        custo_total_real = sum(op.custo_real for op in self.operacoes_atuais)
        custo_total_amortizado = sum(op.custo_amortizado for op in self.operacoes_atuais)
        
        resultado = ResultadoAnaliseAmortizada(
            estrutura=self.estrutura_atual,
            metodo_analise=self.metodo_atual,
            operacoes=self.operacoes_atuais.copy(),
            custo_total_real=custo_total_real,
            custo_total_amortizado=custo_total_amortizado,
            custo_amortizado_por_operacao=custo_total_amortizado / len(self.operacoes_atuais) if self.operacoes_atuais else 0,
            observacoes=observacoes
        )
        
        self.resultados.append(resultado)
        return resultado
    
    def plotar_custos(self, resultado: ResultadoAnaliseAmortizada):
        """
        Plota gráfico comparando custos reais vs amortizados.
        
        Args:
            resultado: Resultado da análise
        """
        operacoes = list(range(1, len(resultado.operacoes) + 1))
        custos_reais = [op.custo_real for op in resultado.operacoes]
        custos_amortizados = [op.custo_amortizado for op in resultado.operacoes]
        
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 1, 1)
        plt.plot(operacoes, custos_reais, 'r-o', label='Custo Real', alpha=0.7)
        plt.plot(operacoes, custos_amortizados, 'b-s', label='Custo Amortizado', alpha=0.7)
        plt.xlabel('Operação')
        plt.ylabel('Custo')
        plt.title(f'Análise Amortizada: {resultado.estrutura} ({resultado.metodo_analise})')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Custo acumulado
        custos_reais_acum = np.cumsum(custos_reais)
        custos_amortizados_acum = np.cumsum(custos_amortizados)
        
        plt.subplot(2, 1, 2)
        plt.plot(operacoes, custos_reais_acum, 'r-', label='Custo Real Acumulado', linewidth=2)
        plt.plot(operacoes, custos_amortizados_acum, 'b--', label='Custo Amortizado Acumulado', linewidth=2)
        plt.xlabel('Operação')
        plt.ylabel('Custo Acumulado')
        plt.title('Custos Acumulados')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()


class ArrayDinamico:
    """
    Array dinâmico com redimensionamento automático.
    Demonstra análise amortizada de operações de inserção.
    """
    
    def __init__(self, analisador: AnalisadorAmortizado, capacidade_inicial: int = 1):
        """
        Inicializa array dinâmico.
        
        Args:
            analisador: Analisador para registrar operações
            capacidade_inicial: Capacidade inicial do array
        """
        self.analisador = analisador
        self.capacidade = capacidade_inicial
        self.tamanho = 0
        self.dados = [None] * self.capacidade
        self.num_redimensionamentos = 0
    
    def inserir(self, valor: Any) -> int:
        """
        Insere valor no final do array.
        
        Args:
            valor: Valor a ser inserido
        
        Returns:
            Custo real da operação
        """
        custo_real = 1  # Custo base da inserção
        
        # Verificar se precisa redimensionar
        if self.tamanho == self.capacidade:
            custo_real += self._redimensionar()
        
        # Inserir elemento
        self.dados[self.tamanho] = valor
        self.tamanho += 1
        
        return custo_real
    
    def _redimensionar(self) -> int:
        """
        Redimensiona o array dobrando a capacidade.
        
        Returns:
            Custo do redimensionamento
        """
        nova_capacidade = self.capacidade * 2
        novos_dados = [None] * nova_capacidade
        
        # Copiar elementos existentes
        custo_copia = 0
        for i in range(self.tamanho):
            novos_dados[i] = self.dados[i]
            custo_copia += 1
        
        self.dados = novos_dados
        self.capacidade = nova_capacidade
        self.num_redimensionamentos += 1
        
        return custo_copia
    
    def analisar_metodo_agregado(self, n: int) -> ResultadoAnaliseAmortizada:
        """
        Analisa inserções usando método agregado.
        
        Args:
            n: Número de inserções
        
        Returns:
            Resultado da análise
        """
        self.analisador.iniciar_analise("Array Dinâmico", "Método Agregado")
        
        for i in range(n):
            custo_real = self.inserir(f"item_{i}")
            
            # Custo amortizado é constante no método agregado
            custo_amortizado = 3  # Será justificado na análise
            
            operacao = OperacaoAnalise(
                nome=f"inserir({i})",
                custo_real=custo_real,
                custo_amortizado=custo_amortizado,
                observacoes=f"Redimensionamento: {'Sim' if custo_real > 1 else 'Não'}"
            )
            
            self.analisador.registrar_operacao(operacao)
        
        observacoes = f"""
        MÉTODO AGREGADO:
        
        Análise do custo total de {n} inserções:
        - Inserções simples: {n} operações × 1 = {n}
        - Redimensionamentos: {self.num_redimensionamentos} × custo variável
        
        Custo dos redimensionamentos:
        - 1º redimensionamento: copia 1 elemento
        - 2º redimensionamento: copia 2 elementos  
        - 3º redimensionamento: copia 4 elementos
        - ...
        - kº redimensionamento: copia 2^(k-1) elementos
        
        Total de cópias: 1 + 2 + 4 + ... + 2^(k-1) = 2^k - 1 < n
        
        Custo total: n (inserções) + n (cópias) = 2n
        Custo amortizado por operação: 2n/n = 2 = O(1)
        
        Na prática, usamos custo amortizado = 3 para ter margem de segurança.
        """
        
        return self.analisador.finalizar_analise(observacoes)
    
    def analisar_metodo_contabil(self, n: int) -> ResultadoAnaliseAmortizada:
        """
        Analisa inserções usando método contábil.
        
        Args:
            n: Número de inserções
        
        Returns:
            Resultado da análise
        """
        self.analisador.iniciar_analise("Array Dinâmico", "Método Contábil")
        self.tamanho = 0
        self.capacidade = 1
        self.dados = [None]
        self.num_redimensionamentos = 0
        
        credito_total = 0
        
        for i in range(n):
            custo_real = self.inserir(f"item_{i}")
            custo_amortizado = 3  # Cobramos 3 por inserção
            
            # Calcular créditos
            credito_usado = max(0, custo_real - 1)  # Crédito usado para redimensionamento
            credito_armazenado = custo_amortizado - custo_real  # Crédito armazenado
            credito_total += credito_armazenado - credito_usado
            
            operacao = OperacaoAnalise(
                nome=f"inserir({i})",
                custo_real=custo_real,
                custo_amortizado=custo_amortizado,
                credito_usado=credito_usado,
                credito_armazenado=credito_armazenado,
                observacoes=f"Crédito total: {credito_total}"
            )
            
            self.analisador.registrar_operacao(operacao)
        
        observacoes = f"""
        MÉTODO CONTÁBIL:
        
        Esquema de cobrança:
        - Cobramos 3 unidades por inserção
        - 1 unidade paga a inserção atual
        - 2 unidades ficam como crédito
        
        Uso do crédito:
        - Quando redimensionamos de tamanho k para 2k:
        - Precisamos copiar k elementos (custo k)
        - Cada elemento inserido deixou 2 créditos
        - Total de créditos disponíveis: 2k ≥ k (suficiente)
        
        Invariante: Crédito total ≥ 0 (sempre mantido)
        Custo amortizado: O(1) por inserção
        """
        
        return self.analisador.finalizar_analise(observacoes)
    
    def analisar_metodo_potencial(self, n: int) -> ResultadoAnaliseAmortizada:
        """
        Analisa inserções usando método do potencial.
        
        Args:
            n: Número de inserções
        
        Returns:
            Resultado da análise
        """
        self.analisador.iniciar_analise("Array Dinâmico", "Método do Potencial")
        self.tamanho = 0
        self.capacidade = 1
        self.dados = [None]
        self.num_redimensionamentos = 0
        
        def funcao_potencial(tamanho: int, capacidade: int) -> int:
            """Função potencial: Φ(D) = 2 × tamanho - capacidade"""
            return 2 * tamanho - capacidade
        
        potencial_inicial = funcao_potencial(0, 1)
        
        for i in range(n):
            potencial_antes = funcao_potencial(self.tamanho, self.capacidade)
            custo_real = self.inserir(f"item_{i}")
            potencial_depois = funcao_potencial(self.tamanho, self.capacidade)
            
            # Custo amortizado = custo real + mudança no potencial
            custo_amortizado = custo_real + (potencial_depois - potencial_antes)
            
            operacao = OperacaoAnalise(
                nome=f"inserir({i})",
                custo_real=custo_real,
                custo_amortizado=custo_amortizado,
                potencial_antes=potencial_antes,
                potencial_depois=potencial_depois,
                observacoes=f"ΔΦ = {potencial_depois - potencial_antes}"
            )
            
            self.analisador.registrar_operacao(operacao)
        
        potencial_final = funcao_potencial(self.tamanho, self.capacidade)
        
        observacoes = f"""
        MÉTODO DO POTENCIAL:
        
        Função potencial: Φ(D) = 2 × tamanho - capacidade
        
        Análise por caso:
        
        1. Inserção sem redimensionamento:
           - Custo real: 1
           - ΔΦ = 2×(i+1) - cap - (2×i - cap) = 2
           - Custo amortizado: 1 + 2 = 3
        
        2. Inserção com redimensionamento (tamanho = capacidade = i):
           - Custo real: 1 + i (inserção + cópia)
           - ΔΦ = 2×(i+1) - 2i - (2×i - i) = 2 + 2 - i = 4 - i
           - Custo amortizado: (1 + i) + (4 - i) = 5
        
        Potencial inicial: {potencial_inicial}
        Potencial final: {potencial_final}
        
        Invariante: Φ(D) ≥ Φ(D₀) (potencial nunca fica negativo)
        Custo amortizado: O(1) por inserção
        """
        
        return self.analisador.finalizar_analise(observacoes)


class PilhaMultipop:
    """
    Pilha com operação multipop que remove k elementos.
    Demonstra análise amortizada de operações variáveis.
    """
    
    def __init__(self, analisador: AnalisadorAmortizado):
        """
        Inicializa pilha.
        
        Args:
            analisador: Analisador para registrar operações
        """
        self.analisador = analisador
        self.pilha = []
    
    def push(self, valor: Any) -> int:
        """
        Empilha um valor.
        
        Args:
            valor: Valor a ser empilhado
        
        Returns:
            Custo da operação (sempre 1)
        """
        self.pilha.append(valor)
        return 1
    
    def pop(self) -> Tuple[Any, int]:
        """
        Desempilha um valor.
        
        Returns:
            Tupla (valor, custo)
        """
        if self.pilha:
            return self.pilha.pop(), 1
        return None, 0
    
    def multipop(self, k: int) -> Tuple[List[Any], int]:
        """
        Remove até k elementos da pilha.
        
        Args:
            k: Número máximo de elementos a remover
        
        Returns:
            Tupla (elementos_removidos, custo)
        """
        elementos = []
        custo = 0
        
        while self.pilha and k > 0:
            elementos.append(self.pilha.pop())
            custo += 1
            k -= 1
        
        return elementos, custo
    
    def analisar_sequencia_operacoes(self, operacoes: List[Tuple[str, Any]]) -> ResultadoAnaliseAmortizada:
        """
        Analisa uma sequência de operações usando método contábil.
        
        Args:
            operacoes: Lista de tuplas (operacao, parametro)
        
        Returns:
            Resultado da análise
        """
        self.analisador.iniciar_analise("Pilha Multipop", "Método Contábil")
        self.pilha = []
        
        for i, (op, param) in enumerate(operacoes):
            if op == "push":
                custo_real = self.push(param)
                custo_amortizado = 2  # Cobramos 2: 1 para push, 1 crédito para futuro pop
                credito_armazenado = 1
                credito_usado = 0
                
                operacao = OperacaoAnalise(
                    nome=f"push({param})",
                    custo_real=custo_real,
                    custo_amortizado=custo_amortizado,
                    credito_armazenado=credito_armazenado,
                    credito_usado=credito_usado,
                    observacoes=f"Pilha: {len(self.pilha)} elementos"
                )
                
            elif op == "pop":
                valor, custo_real = self.pop()
                custo_amortizado = 0  # Pago com crédito do push
                credito_usado = custo_real
                credito_armazenado = 0
                
                operacao = OperacaoAnalise(
                    nome=f"pop() → {valor}",
                    custo_real=custo_real,
                    custo_amortizado=custo_amortizado,
                    credito_usado=credito_usado,
                    credito_armazenado=credito_armazenado,
                    observacoes=f"Pilha: {len(self.pilha)} elementos"
                )
                
            elif op == "multipop":
                elementos, custo_real = self.multipop(param)
                custo_amortizado = 0  # Pago com créditos dos pushes
                credito_usado = custo_real
                credito_armazenado = 0
                
                operacao = OperacaoAnalise(
                    nome=f"multipop({param}) → {len(elementos)} elementos",
                    custo_real=custo_real,
                    custo_amortizado=custo_amortizado,
                    credito_usado=credito_usado,
                    credito_armazenado=credito_armazenado,
                    observacoes=f"Removidos: {elementos}, Pilha: {len(self.pilha)} elementos"
                )
            
            self.analisador.registrar_operacao(operacao)
        
        observacoes = """
        ANÁLISE AMORTIZADA DA PILHA MULTIPOP:
        
        Método Contábil:
        - Push: cobramos 2 (1 para operação + 1 crédito)
        - Pop: cobramos 0 (pago com crédito)
        - Multipop: cobramos 0 (pago com créditos)
        
        Invariante: Cada elemento na pilha tem 1 crédito associado
        
        Propriedades:
        - Cada elemento é empilhado exatamente uma vez
        - Cada elemento é desempilhado no máximo uma vez
        - Crédito do push paga o pop correspondente
        
        Custo amortizado:
        - Push: O(1)
        - Pop: O(1) 
        - Multipop: O(1)
        
        Sequência de n operações: O(n) amortizado
        """
        
        return self.analisador.finalizar_analise(observacoes)


class ContadorBinario:
    """
    Contador binário que demonstra análise amortizada.
    Operação increment pode causar cascata de carries.
    """
    
    def __init__(self, analisador: AnalisadorAmortizado, num_bits: int = 8):
        """
        Inicializa contador binário.
        
        Args:
            analisador: Analisador para registrar operações
            num_bits: Número de bits do contador
        """
        self.analisador = analisador
        self.num_bits = num_bits
        self.bits = [0] * num_bits
        self.valor = 0
    
    def increment(self) -> int:
        """
        Incrementa o contador em 1.
        
        Returns:
            Custo da operação (número de bits alterados)
        """
        custo = 0
        carry = 1
        
        for i in range(self.num_bits):
            if carry == 0:
                break
                
            if self.bits[i] == 0:
                self.bits[i] = 1
                carry = 0
                custo += 1
            else:
                self.bits[i] = 0
                carry = 1
                custo += 1
        
        self.valor += 1
        return custo
    
    def reset(self):
        """Reseta o contador para zero."""
        self.bits = [0] * self.num_bits
        self.valor = 0
    
    def __str__(self) -> str:
        """Representação string do contador."""
        return ''.join(str(bit) for bit in reversed(self.bits))
    
    def analisar_incrementos(self, n: int) -> ResultadoAnaliseAmortizada:
        """
        Analisa n incrementos usando método agregado.
        
        Args:
            n: Número de incrementos
        
        Returns:
            Resultado da análise
        """
        self.analisador.iniciar_analise("Contador Binário", "Método Agregado")
        self.reset()
        
        for i in range(n):
            custo_real = self.increment()
            
            # Custo amortizado é 2 (será justificado)
            custo_amortizado = 2
            
            operacao = OperacaoAnalise(
                nome=f"increment() → {self.valor}",
                custo_real=custo_real,
                custo_amortizado=custo_amortizado,
                observacoes=f"Bits: {self}, Flips: {custo_real}"
            )
            
            self.analisador.registrar_operacao(operacao)
        
        # Calcular estatísticas dos bits
        estatisticas_bits = []
        for bit_pos in range(self.num_bits):
            flips = n // (2 ** bit_pos)  # Bit i flipa a cada 2^i incrementos
            estatisticas_bits.append(f"Bit {bit_pos}: {flips} flips")
        
        total_flips = sum(n // (2 ** i) for i in range(self.num_bits))
        
        observacoes = f"""
        ANÁLISE AGREGADA DO CONTADOR BINÁRIO:
        
        Análise por bit:
        {chr(10).join(estatisticas_bits)}
        
        Total de flips em {n} incrementos: {total_flips}
        
        Padrão de flips:
        - Bit 0: flipa a cada incremento (n vezes)
        - Bit 1: flipa a cada 2 incrementos (n/2 vezes)
        - Bit 2: flipa a cada 4 incrementos (n/4 vezes)
        - Bit i: flipa a cada 2^i incrementos (n/2^i vezes)
        
        Custo total: Σ(n/2^i) para i=0 até log(n)
                   = n × Σ(1/2^i) 
                   = n × (1 + 1/2 + 1/4 + ...)
                   = n × 2 = 2n
        
        Custo amortizado por incremento: 2n/n = 2 = O(1)
        """
        
        return self.analisador.finalizar_analise(observacoes)
    
    def analisar_metodo_potencial(self, n: int) -> ResultadoAnaliseAmortizada:
        """
        Analisa incrementos usando método do potencial.
        
        Args:
            n: Número de incrementos
        
        Returns:
            Resultado da análise
        """
        self.analisador.iniciar_analise("Contador Binário", "Método do Potencial")
        self.reset()
        
        def funcao_potencial(bits: List[int]) -> int:
            """Função potencial: número de bits 1 no contador."""
            return sum(bits)
        
        for i in range(n):
            potencial_antes = funcao_potencial(self.bits)
            custo_real = self.increment()
            potencial_depois = funcao_potencial(self.bits)
            
            # Custo amortizado = custo real + mudança no potencial
            custo_amortizado = custo_real + (potencial_depois - potencial_antes)
            
            operacao = OperacaoAnalise(
                nome=f"increment() → {self.valor}",
                custo_real=custo_real,
                custo_amortizado=custo_amortizado,
                potencial_antes=potencial_antes,
                potencial_depois=potencial_depois,
                observacoes=f"Bits: {self}, ΔΦ = {potencial_depois - potencial_antes}"
            )
            
            self.analisador.registrar_operacao(operacao)
        
        observacoes = f"""
        MÉTODO DO POTENCIAL PARA CONTADOR BINÁRIO:
        
        Função potencial: Φ(D) = número de bits 1 no contador
        
        Análise do increment:
        - Suponha que temos t bits 1 consecutivos à direita
        - Custo real: t + 1 (flipar t bits 1→0 e 1 bit 0→1)
        - Mudança no potencial: -t + 1 = 1 - t
        - Custo amortizado: (t + 1) + (1 - t) = 2
        
        Propriedades:
        - Φ(D) ≥ 0 sempre (número de bits 1 ≥ 0)
        - Φ(D₀) = 0 (contador inicia zerado)
        - Custo amortizado constante: O(1)
        
        Invariante mantido: potencial nunca negativo
        """
        
        return self.analisador.finalizar_analise(observacoes)


class TabelaHashDinamica:
    """
    Tabela hash com redimensionamento dinâmico.
    Demonstra análise amortizada com expansão e contração.
    """
    
    def __init__(self, analisador: AnalisadorAmortizado, tamanho_inicial: int = 8):
        """
        Inicializa tabela hash dinâmica.
        
        Args:
            analisador: Analisador para registrar operações
            tamanho_inicial: Tamanho inicial da tabela
        """
        self.analisador = analisador
        self.tamanho = tamanho_inicial
        self.num_elementos = 0
        self.tabela = [[] for _ in range(self.tamanho)]
        self.fator_carga_max = 0.75
        self.fator_carga_min = 0.25
    
    def _hash(self, chave: Any) -> int:
        """Função hash simples."""
        return hash(chave) % self.tamanho
    
    def _redimensionar(self, novo_tamanho: int) -> int:
        """
        Redimensiona a tabela hash.
        
        Args:
            novo_tamanho: Novo tamanho da tabela
        
        Returns:
            Custo do redimensionamento
        """
        tabela_antiga = self.tabela
        self.tamanho = novo_tamanho
        self.tabela = [[] for _ in range(self.tamanho)]
        
        custo = 0
        
        # Reinserir todos os elementos
        for bucket in tabela_antiga:
            for chave, valor in bucket:
                novo_indice = self._hash(chave)
                self.tabela[novo_indice].append((chave, valor))
                custo += 1
        
        return custo
    
    def inserir(self, chave: Any, valor: Any) -> int:
        """
        Insere par chave-valor na tabela.
        
        Args:
            chave: Chave do elemento
            valor: Valor do elemento
        
        Returns:
            Custo da operação
        """
        custo = 1  # Custo base da inserção
        
        # Verificar se precisa expandir
        if self.num_elementos >= self.fator_carga_max * self.tamanho:
            custo += self._redimensionar(self.tamanho * 2)
        
        # Inserir elemento
        indice = self._hash(chave)
        
        # Verificar se chave já existe
        for i, (k, v) in enumerate(self.tabela[indice]):
            if k == chave:
                self.tabela[indice][i] = (chave, valor)
                return custo
        
        # Chave nova
        self.tabela[indice].append((chave, valor))
        self.num_elementos += 1
        
        return custo
    
    def remover(self, chave: Any) -> Tuple[Any, int]:
        """
        Remove elemento da tabela.
        
        Args:
            chave: Chave do elemento a remover
        
        Returns:
            Tupla (valor_removido, custo)
        """
        custo = 1  # Custo base da remoção
        indice = self._hash(chave)
        
        # Procurar e remover elemento
        for i, (k, v) in enumerate(self.tabela[indice]):
            if k == chave:
                valor = self.tabela[indice].pop(i)[1]
                self.num_elementos -= 1
                
                # Verificar se precisa contrair
                if (self.num_elementos <= self.fator_carga_min * self.tamanho and 
                    self.tamanho > 8):  # Manter tamanho mínimo
                    custo += self._redimensionar(self.tamanho // 2)
                
                return valor, custo
        
        return None, custo
    
    def analisar_operacoes_mistas(self, operacoes: List[Tuple[str, Any, Any]]) -> ResultadoAnaliseAmortizada:
        """
        Analisa sequência de inserções e remoções.
        
        Args:
            operacoes: Lista de tuplas (operacao, chave, valor)
        
        Returns:
            Resultado da análise
        """
        self.analisador.iniciar_analise("Tabela Hash Dinâmica", "Método do Potencial")
        
        def funcao_potencial(num_elementos: int, tamanho: int) -> int:
            """
            Função potencial para tabela hash dinâmica.
            Φ(T) = |2×num_elementos - tamanho|
            """
            return abs(2 * num_elementos - tamanho)
        
        for op, chave, valor in operacoes:
            potencial_antes = funcao_potencial(self.num_elementos, self.tamanho)
            
            if op == "inserir":
                custo_real = self.inserir(chave, valor)
                nome_op = f"inserir({chave}, {valor})"
            elif op == "remover":
                valor_removido, custo_real = self.remover(chave)
                nome_op = f"remover({chave}) → {valor_removido}"
            else:
                continue
            
            potencial_depois = funcao_potencial(self.num_elementos, self.tamanho)
            custo_amortizado = custo_real + (potencial_depois - potencial_antes)
            
            operacao = OperacaoAnalise(
                nome=nome_op,
                custo_real=custo_real,
                custo_amortizado=custo_amortizado,
                potencial_antes=potencial_antes,
                potencial_depois=potencial_depois,
                observacoes=f"Elementos: {self.num_elementos}, Tamanho: {self.tamanho}, "
                           f"Fator: {self.num_elementos/self.tamanho:.2f}"
            )
            
            self.analisador.registrar_operacao(operacao)
        
        observacoes = """
        ANÁLISE AMORTIZADA DA TABELA HASH DINÂMICA:
        
        Função potencial: Φ(T) = |2×num_elementos - tamanho|
        
        Estratégia de redimensionamento:
        - Expandir quando fator_carga > 0.75
        - Contrair quando fator_carga < 0.25
        
        Análise por operação:
        
        1. Inserção sem redimensionamento:
           - Custo real: O(1)
           - ΔΦ ≤ 2 (no pior caso)
           - Custo amortizado: O(1)
        
        2. Inserção com expansão:
           - Custo real: O(n) (reinserir n elementos)
           - ΔΦ = mudança significativa no potencial
           - Custo amortizado: O(1) (potencial paga o redimensionamento)
        
        3. Remoção sem contração:
           - Custo real: O(1)
           - ΔΦ ≤ 2
           - Custo amortizado: O(1)
        
        4. Remoção com contração:
           - Custo real: O(n)
           - ΔΦ compensa o custo
           - Custo amortizado: O(1)
        
        Propriedades:
        - Fator de carga mantido entre 0.25 e 0.75
        - Espaço desperdiçado limitado
        - Todas as operações são O(1) amortizado
        """
        
        return self.analisador.finalizar_analise(observacoes)


class UnionFind:
    """
    Estrutura Union-Find com compressão de caminho.
    Demonstra análise amortizada com função de Ackermann.
    """
    
    def __init__(self, analisador: AnalisadorAmortizado, n: int):
        """
        Inicializa Union-Find.
        
        Args:
            analisador: Analisador para registrar operações
            n: Número de elementos
        """
        self.analisador = analisador
        self.parent = list(range(n))
        self.rank = [0] * n
        self.n = n
    
    def find(self, x: int) -> Tuple[int, int]:
        """
        Encontra representante do conjunto com compressão de caminho.
        
        Args:
            x: Elemento a buscar
        
        Returns:
            Tupla (representante, custo)
        """
        custo = 1
        
        if self.parent[x] != x:
            representante, custo_recursivo = self.find(self.parent[x])
            self.parent[x] = representante  # Compressão de caminho
            custo += custo_recursivo
        
        return self.parent[x], custo
    
    def union(self, x: int, y: int) -> int:
        """
        Une dois conjuntos usando union by rank.
        
        Args:
            x: Primeiro elemento
            y: Segundo elemento
        
        Returns:
            Custo da operação
        """
        root_x, custo_x = self.find(x)
        root_y, custo_y = self.find(y)
        custo_total = custo_x + custo_y
        
        if root_x == root_y:
            return custo_total
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return custo_total + 1
    
    def analisar_sequencia(self, operacoes: List[Tuple[str, int, int]]) -> ResultadoAnaliseAmortizada:
        """
        Analisa sequência de operações Union-Find.
        
        Args:
            operacoes: Lista de tuplas (operacao, x, y)
        
        Returns:
            Resultado da análise
        """
        self.analisador.iniciar_analise("Union-Find", "Análise com Função de Ackermann")
        
        for op, x, y in operacoes:
            if op == "union":
                custo_real = self.union(x, y)
                # Custo amortizado é O(α(n)) onde α é inverso de Ackermann
                custo_amortizado = 4  # Aproximação para α(n) ≤ 4 para valores práticos
                nome_op = f"union({x}, {y})"
                
            elif op == "find":
                representante, custo_real = self.find(x)
                custo_amortizado = 4  # O(α(n))
                nome_op = f"find({x}) → {representante}"
            
            else:
                continue
            
            operacao = OperacaoAnalise(
                nome=nome_op,
                custo_real=custo_real,
                custo_amortizado=custo_amortizado,
                observacoes=f"Estrutura da floresta alterada"
            )
            
            self.analisador.registrar_operacao(operacao)
        
        observacoes = f"""
        ANÁLISE AMORTIZADA DO UNION-FIND:
        
        Otimizações implementadas:
        1. Union by rank: une árvore menor à maior
        2. Compressão de caminho: achata caminhos durante find
        
        Análise de complexidade:
        - Sem otimizações: O(n) por operação no pior caso
        - Com union by rank: O(log n) por operação
        - Com compressão de caminho: O(α(n)) amortizado
        
        Função de Ackermann inversa α(n):
        - α(n) ≤ 4 para todos os valores práticos de n
        - α(2^65536) = 4
        - Cresce extremamente devagar
        
        Resultado:
        - m operações em n elementos: O(m × α(n))
        - Na prática: quase O(m) (constante muito pequena)
        
        Aplicações:
        - Algoritmo de Kruskal (MST)
        - Detecção de ciclos em grafos
        - Componentes conexas dinâmicas
        - Problemas de conectividade
        """
        
        return self.analisador.finalizar_analise(observacoes)


# Funções de Demonstração
def demonstrar_array_dinamico():
    """Demonstra análise amortizada de array dinâmico."""
    print("=== DEMONSTRAÇÃO: ARRAY DINÂMICO ===\n")
    
    analisador = AnalisadorAmortizado()
    array = ArrayDinamico(analisador)
    
    print("1. MÉTODO AGREGADO:")
    resultado1 = array.analisar_metodo_agregado(16)
    print(f"   Custo total real: {resultado1.custo_total_real}")
    print(f"   Custo total amortizado: {resultado1.custo_total_amortizado}")
    print(f"   Custo amortizado por operação: {resultado1.custo_amortizado_por_operacao:.2f}")
    
    print("\n2. MÉTODO CONTÁBIL:")
    array2 = ArrayDinamico(analisador)
    resultado2 = array2.analisar_metodo_contabil(16)
    print(f"   Custo total real: {resultado2.custo_total_real}")
    print(f"   Custo total amortizado: {resultado2.custo_total_amortizado}")
    print(f"   Custo amortizado por operação: {resultado2.custo_amortizado_por_operacao:.2f}")
    
    print("\n3. MÉTODO DO POTENCIAL:")
    array3 = ArrayDinamico(analisador)
    resultado3 = array3.analisar_metodo_potencial(16)
    print(f"   Custo total real: {resultado3.custo_total_real}")
    print(f"   Custo total amortizado: {resultado3.custo_total_amortizado}")
    print(f"   Custo amortizado por operação: {resultado3.custo_amortizado_por_operacao:.2f}")
    
    # Plotar resultados
    try:
        analisador.plotar_custos(resultado1)
    except Exception as e:
        print(f"Erro ao plotar gráfico: {e}")


def demonstrar_pilha_multipop():
    """Demonstra análise amortizada de pilha com multipop."""
    print("\n=== DEMONSTRAÇÃO: PILHA MULTIPOP ===\n")
    
    analisador = AnalisadorAmortizado()
    pilha = PilhaMultipop(analisador)
    
    # Sequência de operações
    operacoes = [
        ("push", 1), ("push", 2), ("push", 3), ("push", 4), ("push", 5),
        ("multipop", 3), ("push", 6), ("push", 7), ("pop", None),
        ("multipop", 2), ("push", 8), ("multipop", 10)
    ]
    
    resultado = pilha.analisar_sequencia_operacoes(operacoes)
    
    print("Sequência de operações analisada:")
    for i, op in enumerate(resultado.operacoes):
        print(f"   {i+1:2d}. {op.nome:20s} | Real: {op.custo_real:2d} | "
              f"Amortizado: {op.custo_amortizado:2d} | {op.observacoes}")
    
    print(f"\nResumo:")
    print(f"   Custo total real: {resultado.custo_total_real}")
    print(f"   Custo total amortizado: {resultado.custo_total_amortizado}")
    print(f"   Custo amortizado por operação: {resultado.custo_amortizado_por_operacao:.2f}")


def demonstrar_contador_binario():
    """Demonstra análise amortizada de contador binário."""
    print("\n=== DEMONSTRAÇÃO: CONTADOR BINÁRIO ===\n")
    
    analisador = AnalisadorAmortizado()
    contador = ContadorBinario(analisador, 8)
    
    print("1. MÉTODO AGREGADO:")
    resultado1 = contador.analisar_incrementos(16)
    
    print("   Sequência de incrementos:")
    for i, op in enumerate(resultado1.operacoes[:8]):  # Mostrar apenas os primeiros 8
        print(f"   {i:2d}. {op.nome:15s} | {op.observacoes}")
    print("   ...")
    
    print(f"\n   Custo total real: {resultado1.custo_total_real}")
    print(f"   Custo amortizado por operação: {resultado1.custo_amortizado_por_operacao:.2f}")
    
    print("\n2. MÉTODO DO POTENCIAL:")
    contador2 = ContadorBinario(analisador, 8)
    resultado2 = contador2.analisar_metodo_potencial(16)
    
    print("   Análise com função potencial:")
    for i, op in enumerate(resultado2.operacoes[:8]):
        print(f"   {i:2d}. {op.nome:15s} | Φ: {op.potencial_antes}→{op.potencial_depois} | "
              f"Amortizado: {op.custo_amortizado}")
    print("   ...")


def demonstrar_tabela_hash_dinamica():
    """Demonstra análise amortizada de tabela hash dinâmica."""
    print("\n=== DEMONSTRAÇÃO: TABELA HASH DINÂMICA ===\n")
    
    analisador = AnalisadorAmortizado()
    tabela = TabelaHashDinamica(analisador, 4)
    
    # Sequência de operações que força redimensionamentos
    operacoes = [
        ("inserir", "a", 1), ("inserir", "b", 2), ("inserir", "c", 3),
        ("inserir", "d", 4),  # Força expansão
        ("inserir", "e", 5), ("inserir", "f", 6),
        ("remover", "a", None), ("remover", "b", None),
        ("remover", "c", None), ("remover", "d", None),  # Força contração
        ("inserir", "g", 7), ("inserir", "h", 8)
    ]
    
    resultado = tabela.analisar_operacoes_mistas(operacoes)
    
    print("Sequência de operações com redimensionamentos:")
    for i, op in enumerate(resultado.operacoes):
        redim = "REDIM" if op.custo_real > 1 else ""
        print(f"   {i+1:2d}. {op.nome:20s} | Real: {op.custo_real:2d} | "
              f"Amortizado: {op.custo_amortizado:2d} | {redim} {op.observacoes}")
    
    print(f"\nResumo:")
    print(f"   Custo total real: {resultado.custo_total_real}")
    print(f"   Custo total amortizado: {resultado.custo_total_amortizado}")
    print(f"   Custo amortizado por operação: {resultado.custo_amortizado_por_operacao:.2f}")


def demonstrar_union_find():
    """Demonstra análise amortizada de Union-Find."""
    print("\n=== DEMONSTRAÇÃO: UNION-FIND ===\n")
    
    analisador = AnalisadorAmortizado()
    uf = UnionFind(analisador, 10)
    
    # Sequência de operações
    operacoes = [
        ("union", 0, 1), ("union", 2, 3), ("union", 4, 5),
        ("union", 1, 3), ("find", 0), ("find", 2),
        ("union", 5, 7), ("find", 4), ("union", 0, 4),
        ("find", 7), ("find", 3), ("find", 5)
    ]
    
    resultado = uf.analisar_sequencia(operacoes)
    
    print("Sequência de operações Union-Find:")
    for i, op in enumerate(resultado.operacoes):
        print(f"   {i+1:2d}. {op.nome:15s} | Real: {op.custo_real:2d} | "
              f"Amortizado: {op.custo_amortizado:2d}")
    
    print(f"\nResumo:")
    print(f"   Custo total real: {resultado.custo_total_real}")
    print(f"   Custo total amortizado: {resultado.custo_total_amortizado}")
    print(f"   Custo amortizado por operação: {resultado.custo_amortizado_por_operacao:.2f}")


def comparar_metodos_analise():
    """Compara os três métodos de análise amortizada."""
    print("\n=== COMPARAÇÃO: MÉTODOS DE ANÁLISE AMORTIZADA ===\n")
    
    print("MÉTODO AGREGADO:")
    print("   • Analisa custo total de sequência de operações")
    print("   • Divide custo total pelo número de operações")
    print("   • Mais simples, mas menos detalhado")
    print("   • Bom para análise inicial e compreensão geral")
    
    print("\nMÉTODO CONTÁBIL (ACCOUNTING):")
    print("   • Atribui custo amortizado a cada operação")
    print("   • Operações 'baratas' pagam por operações 'caras'")
    print("   • Usa sistema de créditos/débitos")
    print("   • Intuitivo, fácil de explicar")
    print("   • Invariante: crédito total ≥ 0")
    
    print("\nMÉTODO DO POTENCIAL:")
    print("   • Define função potencial Φ(D) sobre estrutura")
    print("   • Custo amortizado = custo real + ΔΦ")
    print("   • Mais matemático e rigoroso")
    print("   • Permite análise mais sofisticada")
    print("   • Invariante: Φ(D) ≥ Φ(D₀)")
    
    print("\nQUANDO USAR CADA MÉTODO:")
    print("   • Agregado: análise rápida, casos simples")
    print("   • Contábil: explicações didáticas, casos intuitivos")
    print("   • Potencial: análises complexas, provas rigorosas")
    
    print("\nEXEMPLOS DE APLICAÇÃO:")
    print("   • Array dinâmico: todos os métodos funcionam bem")
    print("   • Pilha multipop: contábil é mais natural")
    print("   • Contador binário: potencial é mais elegante")
    print("   • Árvore splay: potencial é essencial")
    print("   • Union-Find: análise especializada necessária")


def benchmark_estruturas_amortizadas():
    """Benchmark de estruturas com análise amortizada."""
    print("\n=== BENCHMARK: ESTRUTURAS AMORTIZADAS ===\n")
    
    tamanhos = [100, 500, 1000, 2000]
    
    print("Comparação empírica de estruturas amortizadas:")
    print("(Tempo médio por operação em microssegundos)")
    print()
    
    for n in tamanhos:
        print(f"n = {n}:")
        
        # Array dinâmico
        analisador = AnalisadorAmortizado()
        array = ArrayDinamico(analisador)
        
        inicio = time.perf_counter()
        for i in range(n):
            array.inserir(i)
        fim = time.perf_counter()
        
        tempo_array = (fim - inicio) * 1000000 / n  # microssegundos por operação
        print(f"   Array Dinâmico: {tempo_array:.2f} μs/op")
        
        # Contador binário
        contador = ContadorBinario(analisador)
        
        inicio = time.perf_counter()
        for i in range(n):
            contador.increment()
        fim = time.perf_counter()
        
        tempo_contador = (fim - inicio) * 1000000 / n
        print(f"   Contador Binário: {tempo_contador:.2f} μs/op")
        
        # Tabela hash dinâmica
        tabela = TabelaHashDinamica(analisador)
        
        inicio = time.perf_counter()
        for i in range(n):
            tabela.inserir(f"key_{i}", i)
        fim = time.perf_counter()
        
        tempo_tabela = (fim - inicio) * 1000000 / n
        print(f"   Tabela Hash: {tempo_tabela:.2f} μs/op")
        
        print()


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 07.2 - ANÁLISE AMORTIZADA")
    print("=" * 50)
    
    demonstrar_array_dinamico()
    demonstrar_pilha_multipop()
    demonstrar_contador_binario()
    demonstrar_tabela_hash_dinamica()
    demonstrar_union_find()
    comparar_metodos_analise()
    benchmark_estruturas_amortizadas()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 07.2")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. CONCEITO DE ANÁLISE AMORTIZADA:
   • Analisa custo médio de operações em sequência
   • Diferente de análise de pior caso isolado
   • Operações caras são compensadas por operações baratas
   • Fornece garantias mais realistas de performance

2. TRÊS MÉTODOS DE ANÁLISE:
   • Método Agregado: análise global do custo total
   • Método Contábil: sistema de créditos e débitos
   • Método do Potencial: função matemática sobre estrutura

3. ESTRUTURAS COM ANÁLISE AMORTIZADA:
   • Array Dinâmico: O(1) amortizado para inserção
   • Pilha Multipop: O(1) amortizado para todas operações
   • Contador Binário: O(1) amortizado para incremento
   • Tabela Hash Dinâmica: O(1) amortizado para inserção/remoção
   • Union-Find: O(α(n)) amortizado com otimizações

4. VANTAGENS DA ANÁLISE AMORTIZADA:
   • Análise mais precisa que pior caso
   • Justifica uso de estruturas dinâmicas
   • Permite otimizações agressivas
   • Fundamental para algoritmos eficientes

5. APLICAÇÕES PRÁTICAS:
   • Linguagens de programação (garbage collection)
   • Sistemas de banco de dados (B-trees)
   • Estruturas de dados da biblioteca padrão
   • Algoritmos de grafos (Union-Find)

6. INVARIANTES E PROPRIEDADES:
   • Método Contábil: crédito total ≥ 0
   • Método Potencial: Φ(D) ≥ Φ(D₀)
   • Custo amortizado ≥ custo real médio
   • Análise válida para qualquer sequência de operações

7. LIMITAÇÕES:
   • Não garante performance de operação individual
   • Análise pode ser complexa para estruturas sofisticadas
   • Requer escolha cuidadosa de função potencial
   • Nem sempre aplicável a todos os problemas

8. TÉCNICAS DE IMPLEMENTAÇÃO:
   • Redimensionamento por fatores (dobrar/dividir por 2)
   • Limiares para expansão/contração diferentes
   • Compressão de caminho em estruturas hierárquicas
   • Balanceamento automático em árvores

A análise amortizada é essencial para:
- Projetar estruturas de dados eficientes
- Compreender performance real de algoritmos
- Otimizar sistemas com operações variáveis
- Justificar escolhas de design em software

Próximo: Módulo 07.3 - Complexidade Espacial
    """)


if __name__ == "__main__":
    main()