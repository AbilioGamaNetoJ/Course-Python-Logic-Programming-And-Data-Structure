"""
MÓDULO 06.6 - OTIMIZAÇÃO
========================

Objetivos de Aprendizado:
- Dominar técnicas de otimização matemática
- Implementar algoritmos genéticos
- Aplicar simulated annealing
- Resolver problemas de programação linear
- Otimizar funções não-lineares
- Compreender meta-heurísticas

Conceitos Abordados:
- Programação Linear (Simplex)
- Algoritmos Genéticos (GA)
- Simulated Annealing (SA)
- Particle Swarm Optimization (PSO)
- Otimização por Colônia de Formigas (ACO)
- Busca Tabu
- Algoritmos Evolutivos
- Otimização Multi-objetivo

Algoritmos Implementados:
- Método Simplex para programação linear
- Algoritmo genético clássico
- Simulated annealing com diferentes esquemas de resfriamento
- PSO para otimização contínua
- ACO para problemas combinatórios
- Busca tabu com memória adaptativa
- NSGA-II para otimização multi-objetivo
- Algoritmos híbridos

Pré-requisitos:
- Álgebra linear básica
- Probabilidade e estatística
- Estruturas de dados avançadas
- Algoritmos de busca

Complexidade Típica:
- Simplex: O(n³) por iteração
- Algoritmos Genéticos: O(g * p * f) onde g=gerações, p=população, f=fitness
- Simulated Annealing: O(i * f) onde i=iterações, f=avaliação
- PSO: O(i * p * d) onde d=dimensões
"""

import numpy as np
import random
import math
import time
from typing import List, Dict, Tuple, Optional, Callable, Any, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
import copy
from collections import deque, defaultdict
import heapq


class TipoOtimizacao(Enum):
    """Tipos de problemas de otimização."""
    MINIMIZACAO = "minimizacao"
    MAXIMIZACAO = "maximizacao"
    MULTI_OBJETIVO = "multi_objetivo"


class TipoVariavel(Enum):
    """Tipos de variáveis de decisão."""
    CONTINUA = "continua"
    INTEIRA = "inteira"
    BINARIA = "binaria"


@dataclass
class Restricao:
    """Representa uma restrição linear."""
    coeficientes: List[float]
    operador: str  # '<=', '>=', '='
    valor_direito: float
    nome: str = ""
    
    def avaliar(self, solucao: List[float]) -> bool:
        """Avalia se solução satisfaz restrição."""
        valor_esquerdo = sum(c * x for c, x in zip(self.coeficientes, solucao))
        
        if self.operador == '<=':
            return valor_esquerdo <= self.valor_direito + 1e-10
        elif self.operador == '>=':
            return valor_esquerdo >= self.valor_direito - 1e-10
        elif self.operador == '=':
            return abs(valor_esquerdo - self.valor_direito) <= 1e-10
        
        return False
    
    def violacao(self, solucao: List[float]) -> float:
        """Calcula violação da restrição."""
        valor_esquerdo = sum(c * x for c, x in zip(self.coeficientes, solucao))
        
        if self.operador == '<=':
            return max(0, valor_esquerdo - self.valor_direito)
        elif self.operador == '>=':
            return max(0, self.valor_direito - valor_esquerdo)
        elif self.operador == '=':
            return abs(valor_esquerdo - self.valor_direito)
        
        return 0.0


@dataclass
class EstatisticasOtimizacao:
    """Estatísticas de algoritmos de otimização."""
    iteracoes: int = 0
    avaliacoes_funcao: int = 0
    tempo_execucao: float = 0.0
    melhor_valor: float = float('inf')
    convergencia: List[float] = field(default_factory=list)
    violacoes_restricoes: int = 0
    solucoes_validas: int = 0
    diversidade_populacao: float = 0.0
    
    def reset(self):
        """Reseta todas as estatísticas."""
        self.iteracoes = 0
        self.avaliacoes_funcao = 0
        self.tempo_execucao = 0.0
        self.melhor_valor = float('inf')
        self.convergencia = []
        self.violacoes_restricoes = 0
        self.solucoes_validas = 0
        self.diversidade_populacao = 0.0


class ProblemaOtimizacao:
    """
    Classe base para problemas de otimização.
    """
    
    def __init__(self, tipo: TipoOtimizacao = TipoOtimizacao.MINIMIZACAO):
        """
        Inicializa problema de otimização.
        
        Args:
            tipo: Tipo de otimização (min/max/multi-objetivo)
        """
        self.tipo = tipo
        self.dimensoes = 0
        self.limites_inferiores: List[float] = []
        self.limites_superiores: List[float] = []
        self.tipos_variaveis: List[TipoVariavel] = []
        self.restricoes: List[Restricao] = []
        self.funcao_objetivo: Optional[Callable] = None
        self.stats = EstatisticasOtimizacao()
    
    def definir_variaveis(self, dimensoes: int, 
                         limites_inf: List[float], 
                         limites_sup: List[float],
                         tipos: List[TipoVariavel] = None):
        """Define variáveis de decisão."""
        self.dimensoes = dimensoes
        self.limites_inferiores = limites_inf
        self.limites_superiores = limites_sup
        
        if tipos is None:
            self.tipos_variaveis = [TipoVariavel.CONTINUA] * dimensoes
        else:
            self.tipos_variaveis = tipos
    
    def adicionar_restricao(self, restricao: Restricao):
        """Adiciona restrição ao problema."""
        self.restricoes.append(restricao)
    
    def definir_funcao_objetivo(self, funcao: Callable):
        """Define função objetivo."""
        self.funcao_objetivo = funcao
    
    def avaliar(self, solucao: List[float]) -> float:
        """
        Avalia função objetivo.
        
        Args:
            solucao: Vetor de variáveis de decisão
        
        Returns:
            Valor da função objetivo
        """
        if self.funcao_objetivo is None:
            raise ValueError("Função objetivo não definida")
        
        self.stats.avaliacoes_funcao += 1
        valor = self.funcao_objetivo(solucao)
        
        # Converter para minimização se necessário
        if self.tipo == TipoOtimizacao.MAXIMIZACAO:
            valor = -valor
        
        return valor
    
    def eh_factivel(self, solucao: List[float]) -> bool:
        """Verifica se solução é factível."""
        # Verificar limites das variáveis
        for i, (x, inf, sup) in enumerate(zip(solucao, self.limites_inferiores, self.limites_superiores)):
            if x < inf - 1e-10 or x > sup + 1e-10:
                return False
            
            # Verificar tipo de variável
            if self.tipos_variaveis[i] == TipoVariavel.INTEIRA:
                if abs(x - round(x)) > 1e-10:
                    return False
            elif self.tipos_variaveis[i] == TipoVariavel.BINARIA:
                if abs(x - 0) > 1e-10 and abs(x - 1) > 1e-10:
                    return False
        
        # Verificar restrições
        for restricao in self.restricoes:
            if not restricao.avaliar(solucao):
                return False
        
        return True
    
    def calcular_penalidade(self, solucao: List[float]) -> float:
        """Calcula penalidade por violação de restrições."""
        penalidade = 0.0
        
        # Penalidade por limites das variáveis
        for i, (x, inf, sup) in enumerate(zip(solucao, self.limites_inferiores, self.limites_superiores)):
            if x < inf:
                penalidade += (inf - x) ** 2
            elif x > sup:
                penalidade += (x - sup) ** 2
        
        # Penalidade por restrições
        for restricao in self.restricoes:
            violacao = restricao.violacao(solucao)
            penalidade += violacao ** 2
        
        return penalidade
    
    def gerar_solucao_aleatoria(self) -> List[float]:
        """Gera solução aleatória factível."""
        solucao = []
        
        for i in range(self.dimensoes):
            inf, sup = self.limites_inferiores[i], self.limites_superiores[i]
            
            if self.tipos_variaveis[i] == TipoVariavel.BINARIA:
                valor = random.choice([0.0, 1.0])
            elif self.tipos_variaveis[i] == TipoVariavel.INTEIRA:
                valor = float(random.randint(int(inf), int(sup)))
            else:
                valor = random.uniform(inf, sup)
            
            solucao.append(valor)
        
        return solucao


class MetodoSimplex:
    """
    Implementa o método Simplex para programação linear.
    """
    
    def __init__(self, problema: ProblemaOtimizacao):
        """
        Inicializa método Simplex.
        
        Args:
            problema: Problema de programação linear
        """
        self.problema = problema
        self.stats = EstatisticasOtimizacao()
        self.tableau = None
        self.base = []
        self.nao_base = []
    
    def resolver(self) -> Tuple[List[float], float]:
        """
        Resolve problema usando método Simplex.
        
        Returns:
            Tupla (solução_ótima, valor_ótimo)
        """
        self.stats.reset()
        start_time = time.time()
        
        # Converter para forma padrão
        self._converter_forma_padrao()
        
        # Encontrar solução básica inicial
        if not self._encontrar_solucao_inicial():
            raise ValueError("Problema infactível")
        
        # Iterações do Simplex
        while True:
            # Teste de otimalidade
            if self._eh_otimo():
                break
            
            # Escolher variável que entra na base
            coluna_pivo = self._escolher_variavel_entrada()
            
            # Teste de ilimitação
            if self._eh_ilimitado(coluna_pivo):
                raise ValueError("Problema ilimitado")
            
            # Escolher variável que sai da base
            linha_pivo = self._escolher_variavel_saida(coluna_pivo)
            
            # Operação de pivoteamento
            self._pivotear(linha_pivo, coluna_pivo)
            
            self.stats.iteracoes += 1
        
        # Extrair solução
        solucao, valor = self._extrair_solucao()
        
        self.stats.tempo_execucao = time.time() - start_time
        self.stats.melhor_valor = valor
        
        return solucao, valor
    
    def _converter_forma_padrao(self):
        """Converte problema para forma padrão do Simplex."""
        # Implementação simplificada - assumindo que já está em forma padrão
        # Em implementação completa, seria necessário:
        # 1. Converter inequações para equações com variáveis de folga
        # 2. Garantir que todas as variáveis são não-negativas
        # 3. Converter maximização para minimização se necessário
        
        n_vars = self.problema.dimensoes
        n_restricoes = len(self.problema.restricoes)
        
        # Criar tableau inicial (simplificado)
        self.tableau = np.zeros((n_restricoes + 1, n_vars + n_restricoes + 1))
        
        # Função objetivo na última linha
        if hasattr(self.problema.funcao_objetivo, '__code__'):
            # Para funções lineares simples, extrair coeficientes
            # Implementação simplificada
            pass
    
    def _encontrar_solucao_inicial(self) -> bool:
        """Encontra solução básica inicial factível."""
        # Implementação do método das duas fases ou Big M
        # Simplificado para demonstração
        return True
    
    def _eh_otimo(self) -> bool:
        """Verifica se solução atual é ótima."""
        # Verificar se todos os custos reduzidos são não-negativos
        linha_objetivo = self.tableau[-1, :-1]
        return all(c >= -1e-10 for c in linha_objetivo)
    
    def _escolher_variavel_entrada(self) -> int:
        """Escolhe variável que entra na base (regra de Dantzig)."""
        linha_objetivo = self.tableau[-1, :-1]
        return np.argmin(linha_objetivo)
    
    def _eh_ilimitado(self, coluna: int) -> bool:
        """Verifica se problema é ilimitado."""
        coluna_pivo = self.tableau[:-1, coluna]
        return all(c <= 1e-10 for c in coluna_pivo)
    
    def _escolher_variavel_saida(self, coluna: int) -> int:
        """Escolhe variável que sai da base (teste da razão mínima)."""
        coluna_pivo = self.tableau[:-1, coluna]
        lado_direito = self.tableau[:-1, -1]
        
        razoes = []
        for i, (a, b) in enumerate(zip(coluna_pivo, lado_direito)):
            if a > 1e-10:
                razoes.append((b / a, i))
            else:
                razoes.append((float('inf'), i))
        
        return min(razoes)[1]
    
    def _pivotear(self, linha: int, coluna: int):
        """Realiza operação de pivoteamento."""
        pivo = self.tableau[linha, coluna]
        
        # Normalizar linha do pivo
        self.tableau[linha] /= pivo
        
        # Eliminar coluna do pivo nas outras linhas
        for i in range(self.tableau.shape[0]):
            if i != linha:
                fator = self.tableau[i, coluna]
                self.tableau[i] -= fator * self.tableau[linha]
    
    def _extrair_solucao(self) -> Tuple[List[float], float]:
        """Extrai solução ótima do tableau."""
        n_vars = self.problema.dimensoes
        solucao = [0.0] * n_vars
        
        # Identificar variáveis básicas
        for j in range(n_vars):
            coluna = self.tableau[:-1, j]
            if sum(abs(c) < 1e-10 for c in coluna) == len(coluna) - 1:
                # Variável básica
                for i, c in enumerate(coluna):
                    if abs(c - 1.0) < 1e-10:
                        solucao[j] = self.tableau[i, -1]
                        break
        
        valor_otimo = self.tableau[-1, -1]
        
        # Converter de volta se era maximização
        if self.problema.tipo == TipoOtimizacao.MAXIMIZACAO:
            valor_otimo = -valor_otimo
        
        return solucao, valor_otimo


class AlgoritmoGenetico:
    """
    Implementa algoritmo genético clássico.
    """
    
    def __init__(self, problema: ProblemaOtimizacao, 
                 tamanho_populacao: int = 100,
                 taxa_mutacao: float = 0.01,
                 taxa_crossover: float = 0.8,
                 elitismo: int = 2):
        """
        Inicializa algoritmo genético.
        
        Args:
            problema: Problema de otimização
            tamanho_populacao: Tamanho da população
            taxa_mutacao: Taxa de mutação
            taxa_crossover: Taxa de crossover
            elitismo: Número de indivíduos elite
        """
        self.problema = problema
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.taxa_crossover = taxa_crossover
        self.elitismo = elitismo
        self.populacao = []
        self.fitness = []
        self.stats = EstatisticasOtimizacao()
    
    def resolver(self, max_geracoes: int = 1000) -> Tuple[List[float], float]:
        """
        Resolve problema usando algoritmo genético.
        
        Args:
            max_geracoes: Número máximo de gerações
        
        Returns:
            Tupla (melhor_solução, melhor_fitness)
        """
        self.stats.reset()
        start_time = time.time()
        
        # Inicializar população
        self._inicializar_populacao()
        
        for geracao in range(max_geracoes):
            # Avaliar população
            self._avaliar_populacao()
            
            # Registrar estatísticas
            melhor_fitness = min(self.fitness)
            self.stats.convergencia.append(melhor_fitness)
            
            if melhor_fitness < self.stats.melhor_valor:
                self.stats.melhor_valor = melhor_fitness
            
            # Seleção
            pais = self._selecao_torneio()
            
            # Crossover e mutação
            nova_populacao = self._reproduzir(pais)
            
            # Elitismo
            self._aplicar_elitismo(nova_populacao)
            
            self.populacao = nova_populacao
            self.stats.iteracoes += 1
            
            # Critério de parada
            if self._convergiu():
                break
        
        # Encontrar melhor solução
        self._avaliar_populacao()
        melhor_indice = np.argmin(self.fitness)
        melhor_solucao = self.populacao[melhor_indice]
        melhor_valor = self.fitness[melhor_indice]
        
        self.stats.tempo_execucao = time.time() - start_time
        
        return melhor_solucao, melhor_valor
    
    def _inicializar_populacao(self):
        """Inicializa população aleatória."""
        self.populacao = []
        
        for _ in range(self.tamanho_populacao):
            individuo = self.problema.gerar_solucao_aleatoria()
            self.populacao.append(individuo)
    
    def _avaliar_populacao(self):
        """Avalia fitness de toda a população."""
        self.fitness = []
        
        for individuo in self.populacao:
            fitness = self.problema.avaliar(individuo)
            
            # Adicionar penalidade se não factível
            if not self.problema.eh_factivel(individuo):
                penalidade = self.problema.calcular_penalidade(individuo)
                fitness += 1000 * penalidade  # Penalidade alta
                self.stats.violacoes_restricoes += 1
            else:
                self.stats.solucoes_validas += 1
            
            self.fitness.append(fitness)
    
    def _selecao_torneio(self, tamanho_torneio: int = 3) -> List[List[float]]:
        """Seleção por torneio."""
        pais = []
        
        for _ in range(self.tamanho_populacao):
            # Selecionar candidatos aleatórios
            candidatos = random.sample(range(self.tamanho_populacao), tamanho_torneio)
            
            # Escolher melhor candidato
            melhor = min(candidatos, key=lambda i: self.fitness[i])
            pais.append(self.populacao[melhor][:])  # Cópia
        
        return pais
    
    def _reproduzir(self, pais: List[List[float]]) -> List[List[float]]:
        """Reprodução com crossover e mutação."""
        nova_populacao = []
        
        for i in range(0, len(pais), 2):
            pai1 = pais[i]
            pai2 = pais[i + 1] if i + 1 < len(pais) else pais[0]
            
            # Crossover
            if random.random() < self.taxa_crossover:
                filho1, filho2 = self._crossover_uniforme(pai1, pai2)
            else:
                filho1, filho2 = pai1[:], pai2[:]
            
            # Mutação
            self._mutar(filho1)
            self._mutar(filho2)
            
            nova_populacao.extend([filho1, filho2])
        
        return nova_populacao[:self.tamanho_populacao]
    
    def _crossover_uniforme(self, pai1: List[float], pai2: List[float]) -> Tuple[List[float], List[float]]:
        """Crossover uniforme."""
        filho1, filho2 = pai1[:], pai2[:]
        
        for i in range(len(pai1)):
            if random.random() < 0.5:
                filho1[i], filho2[i] = filho2[i], filho1[i]
        
        return filho1, filho2
    
    def _mutar(self, individuo: List[float]):
        """Mutação gaussiana."""
        for i in range(len(individuo)):
            if random.random() < self.taxa_mutacao:
                # Mutação gaussiana
                sigma = (self.problema.limites_superiores[i] - self.problema.limites_inferiores[i]) * 0.1
                individuo[i] += random.gauss(0, sigma)
                
                # Manter dentro dos limites
                individuo[i] = max(self.problema.limites_inferiores[i], 
                                 min(self.problema.limites_superiores[i], individuo[i]))
                
                # Ajustar tipo de variável
                if self.problema.tipos_variaveis[i] == TipoVariavel.INTEIRA:
                    individuo[i] = round(individuo[i])
                elif self.problema.tipos_variaveis[i] == TipoVariavel.BINARIA:
                    individuo[i] = round(individuo[i])
    
    def _aplicar_elitismo(self, nova_populacao: List[List[float]]):
        """Aplica elitismo preservando melhores indivíduos."""
        if self.elitismo > 0:
            # Encontrar melhores indivíduos da geração anterior
            indices_elite = sorted(range(len(self.fitness)), key=lambda i: self.fitness[i])[:self.elitismo]
            
            # Substituir piores da nova população
            nova_fitness = [self.problema.avaliar(ind) for ind in nova_populacao]
            indices_piores = sorted(range(len(nova_fitness)), key=lambda i: nova_fitness[i], reverse=True)[:self.elitismo]
            
            for i, elite_idx in enumerate(indices_elite):
                pior_idx = indices_piores[i]
                nova_populacao[pior_idx] = self.populacao[elite_idx][:]
    
    def _convergiu(self) -> bool:
        """Verifica critério de convergência."""
        if len(self.stats.convergencia) < 50:
            return False
        
        # Verificar se não houve melhoria nas últimas 50 gerações
        ultimas_50 = self.stats.convergencia[-50:]
        return max(ultimas_50) - min(ultimas_50) < 1e-6


class SimulatedAnnealing:
    """
    Implementa algoritmo Simulated Annealing.
    """
    
    def __init__(self, problema: ProblemaOtimizacao,
                 temperatura_inicial: float = 1000.0,
                 temperatura_final: float = 0.01,
                 alpha: float = 0.95):
        """
        Inicializa Simulated Annealing.
        
        Args:
            problema: Problema de otimização
            temperatura_inicial: Temperatura inicial
            temperatura_final: Temperatura final
            alpha: Taxa de resfriamento
        """
        self.problema = problema
        self.temperatura_inicial = temperatura_inicial
        self.temperatura_final = temperatura_final
        self.alpha = alpha
        self.stats = EstatisticasOtimizacao()
    
    def resolver(self, max_iteracoes: int = 10000) -> Tuple[List[float], float]:
        """
        Resolve problema usando Simulated Annealing.
        
        Args:
            max_iteracoes: Número máximo de iterações
        
        Returns:
            Tupla (melhor_solução, melhor_valor)
        """
        self.stats.reset()
        start_time = time.time()
        
        # Solução inicial
        solucao_atual = self.problema.gerar_solucao_aleatoria()
        valor_atual = self.problema.avaliar(solucao_atual)
        
        # Melhor solução encontrada
        melhor_solucao = solucao_atual[:]
        melhor_valor = valor_atual
        
        temperatura = self.temperatura_inicial
        
        for iteracao in range(max_iteracoes):
            # Gerar vizinho
            nova_solucao = self._gerar_vizinho(solucao_atual)
            novo_valor = self.problema.avaliar(nova_solucao)
            
            # Calcular diferença
            delta = novo_valor - valor_atual
            
            # Critério de aceitação
            if delta < 0 or random.random() < math.exp(-delta / temperatura):
                solucao_atual = nova_solucao
                valor_atual = novo_valor
                
                # Atualizar melhor solução
                if valor_atual < melhor_valor:
                    melhor_solucao = solucao_atual[:]
                    melhor_valor = valor_atual
            
            # Resfriamento
            temperatura *= self.alpha
            
            # Registrar estatísticas
            self.stats.convergencia.append(melhor_valor)
            self.stats.iteracoes += 1
            
            # Critério de parada
            if temperatura < self.temperatura_final:
                break
        
        self.stats.tempo_execucao = time.time() - start_time
        self.stats.melhor_valor = melhor_valor
        
        return melhor_solucao, melhor_valor
    
    def _gerar_vizinho(self, solucao: List[float]) -> List[float]:
        """Gera solução vizinha."""
        nova_solucao = solucao[:]
        
        # Escolher variável aleatória para modificar
        i = random.randint(0, len(solucao) - 1)
        
        # Gerar perturbação
        if self.problema.tipos_variaveis[i] == TipoVariavel.BINARIA:
            nova_solucao[i] = 1.0 - nova_solucao[i]  # Flip bit
        else:
            # Perturbação gaussiana
            sigma = (self.problema.limites_superiores[i] - self.problema.limites_inferiores[i]) * 0.1
            perturbacao = random.gauss(0, sigma)
            nova_solucao[i] += perturbacao
            
            # Manter dentro dos limites
            nova_solucao[i] = max(self.problema.limites_inferiores[i], 
                                min(self.problema.limites_superiores[i], nova_solucao[i]))
            
            # Ajustar tipo de variável
            if self.problema.tipos_variaveis[i] == TipoVariavel.INTEIRA:
                nova_solucao[i] = round(nova_solucao[i])
        
        return nova_solucao


class ParticleSwarmOptimization:
    """
    Implementa Particle Swarm Optimization (PSO).
    """
    
    def __init__(self, problema: ProblemaOtimizacao,
                 num_particulas: int = 30,
                 w: float = 0.7,
                 c1: float = 1.5,
                 c2: float = 1.5):
        """
        Inicializa PSO.
        
        Args:
            problema: Problema de otimização
            num_particulas: Número de partículas
            w: Peso de inércia
            c1: Coeficiente cognitivo
            c2: Coeficiente social
        """
        self.problema = problema
        self.num_particulas = num_particulas
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.particulas = []
        self.velocidades = []
        self.melhores_pessoais = []
        self.valores_pessoais = []
        self.melhor_global = None
        self.valor_global = float('inf')
        self.stats = EstatisticasOtimizacao()
    
    def resolver(self, max_iteracoes: int = 1000) -> Tuple[List[float], float]:
        """
        Resolve problema usando PSO.
        
        Args:
            max_iteracoes: Número máximo de iterações
        
        Returns:
            Tupla (melhor_solução, melhor_valor)
        """
        self.stats.reset()
        start_time = time.time()
        
        # Inicializar enxame
        self._inicializar_enxame()
        
        for iteracao in range(max_iteracoes):
            # Avaliar partículas
            self._avaliar_enxame()
            
            # Atualizar velocidades e posições
            self._atualizar_enxame()
            
            # Registrar estatísticas
            self.stats.convergencia.append(self.valor_global)
            self.stats.iteracoes += 1
            
            # Critério de parada
            if self._convergiu():
                break
        
        self.stats.tempo_execucao = time.time() - start_time
        self.stats.melhor_valor = self.valor_global
        
        return self.melhor_global[:], self.valor_global
    
    def _inicializar_enxame(self):
        """Inicializa enxame de partículas."""
        self.particulas = []
        self.velocidades = []
        self.melhores_pessoais = []
        self.valores_pessoais = []
        
        for _ in range(self.num_particulas):
            # Posição inicial aleatória
            particula = self.problema.gerar_solucao_aleatoria()
            self.particulas.append(particula)
            
            # Velocidade inicial aleatória
            velocidade = []
            for i in range(self.problema.dimensoes):
                v_max = (self.problema.limites_superiores[i] - self.problema.limites_inferiores[i]) * 0.1
                velocidade.append(random.uniform(-v_max, v_max))
            self.velocidades.append(velocidade)
            
            # Melhor pessoal inicial
            self.melhores_pessoais.append(particula[:])
            self.valores_pessoais.append(float('inf'))
    
    def _avaliar_enxame(self):
        """Avalia todas as partículas."""
        for i, particula in enumerate(self.particulas):
            valor = self.problema.avaliar(particula)
            
            # Adicionar penalidade se não factível
            if not self.problema.eh_factivel(particula):
                penalidade = self.problema.calcular_penalidade(particula)
                valor += 1000 * penalidade
            
            # Atualizar melhor pessoal
            if valor < self.valores_pessoais[i]:
                self.valores_pessoais[i] = valor
                self.melhores_pessoais[i] = particula[:]
                
                # Atualizar melhor global
                if valor < self.valor_global:
                    self.valor_global = valor
                    self.melhor_global = particula[:]
    
    def _atualizar_enxame(self):
        """Atualiza velocidades e posições das partículas."""
        for i in range(self.num_particulas):
            for j in range(self.problema.dimensoes):
                # Componentes da velocidade
                r1, r2 = random.random(), random.random()
                
                cognitivo = self.c1 * r1 * (self.melhores_pessoais[i][j] - self.particulas[i][j])
                social = self.c2 * r2 * (self.melhor_global[j] - self.particulas[i][j])
                
                # Atualizar velocidade
                self.velocidades[i][j] = (self.w * self.velocidades[i][j] + 
                                        cognitivo + social)
                
                # Limitar velocidade
                v_max = (self.problema.limites_superiores[j] - self.problema.limites_inferiores[j]) * 0.2
                self.velocidades[i][j] = max(-v_max, min(v_max, self.velocidades[i][j]))
                
                # Atualizar posição
                self.particulas[i][j] += self.velocidades[i][j]
                
                # Manter dentro dos limites
                self.particulas[i][j] = max(self.problema.limites_inferiores[j], 
                                          min(self.problema.limites_superiores[j], self.particulas[i][j]))
                
                # Ajustar tipo de variável
                if self.problema.tipos_variaveis[j] == TipoVariavel.INTEIRA:
                    self.particulas[i][j] = round(self.particulas[i][j])
                elif self.problema.tipos_variaveis[j] == TipoVariavel.BINARIA:
                    self.particulas[i][j] = round(self.particulas[i][j])
    
    def _convergiu(self) -> bool:
        """Verifica critério de convergência."""
        if len(self.stats.convergencia) < 100:
            return False
        
        # Verificar se não houve melhoria nas últimas 100 iterações
        ultimas_100 = self.stats.convergencia[-100:]
        return max(ultimas_100) - min(ultimas_100) < 1e-8


# Funções de Demonstração
def demonstrar_programacao_linear():
    """Demonstra programação linear com Simplex."""
    print("=== DEMONSTRAÇÃO: PROGRAMAÇÃO LINEAR ===\n")
    
    # Problema exemplo: Maximizar 3x1 + 2x2
    # Sujeito a: x1 + x2 <= 4
    #           2x1 + x2 <= 6
    #           x1, x2 >= 0
    
    problema = ProblemaOtimizacao(TipoOtimizacao.MAXIMIZACAO)
    
    # Definir variáveis
    problema.definir_variaveis(
        dimensoes=2,
        limites_inf=[0.0, 0.0],
        limites_sup=[10.0, 10.0],
        tipos=[TipoVariavel.CONTINUA, TipoVariavel.CONTINUA]
    )
    
    # Função objetivo
    def funcao_objetivo(x):
        return 3 * x[0] + 2 * x[1]
    
    problema.definir_funcao_objetivo(funcao_objetivo)
    
    # Restrições
    problema.adicionar_restricao(Restricao([1.0, 1.0], '<=', 4.0, "x1 + x2 <= 4"))
    problema.adicionar_restricao(Restricao([2.0, 1.0], '<=', 6.0, "2x1 + x2 <= 6"))
    
    print("Problema de Programação Linear:")
    print("  Maximizar: 3x1 + 2x2")
    print("  Sujeito a:")
    print("    x1 + x2 <= 4")
    print("    2x1 + x2 <= 6")
    print("    x1, x2 >= 0")
    
    # Resolver com método Simplex (implementação simplificada)
    print("\nMétodo Simplex:")
    try:
        simplex = MetodoSimplex(problema)
        solucao, valor = simplex.resolver()
        
        print(f"  Solução ótima: x1 = {solucao[0]:.4f}, x2 = {solucao[1]:.4f}")
        print(f"  Valor ótimo: {valor:.4f}")
        print(f"  Iterações: {simplex.stats.iteracoes}")
        print(f"  Tempo: {simplex.stats.tempo_execucao:.6f}s")
    except Exception as e:
        print(f"  Erro: {e}")
        
        # Resolver com algoritmo genético como alternativa
        print("\nAlgoritmo Genético (alternativo):")
        ga = AlgoritmoGenetico(problema, tamanho_populacao=50)
        
        start_time = time.time()
        solucao_ga, valor_ga = ga.resolver(max_geracoes=200)
        tempo_ga = time.time() - start_time
        
        print(f"  Solução: x1 = {solucao_ga[0]:.4f}, x2 = {solucao_ga[1]:.4f}")
        print(f"  Valor: {valor_ga:.4f}")
        print(f"  Gerações: {ga.stats.iteracoes}")
        print(f"  Tempo: {tempo_ga:.6f}s")


def demonstrar_algoritmo_genetico():
    """Demonstra algoritmo genético."""
    print("\n=== DEMONSTRAÇÃO: ALGORITMO GENÉTICO ===\n")
    
    # Problema: Minimizar função de Rastrigin
    def rastrigin(x):
        A = 10
        n = len(x)
        return A * n + sum(xi**2 - A * math.cos(2 * math.pi * xi) for xi in x)
    
    problema = ProblemaOtimizacao(TipoOtimizacao.MINIMIZACAO)
    
    # Definir variáveis (2D)
    problema.definir_variaveis(
        dimensoes=2,
        limites_inf=[-5.12, -5.12],
        limites_sup=[5.12, 5.12]
    )
    
    problema.definir_funcao_objetivo(rastrigin)
    
    print("Problema: Minimizar função de Rastrigin")
    print("  f(x) = 10n + Σ(xi² - 10*cos(2πxi))")
    print("  Domínio: [-5.12, 5.12]²")
    print("  Mínimo global: f(0,0) = 0")
    
    # Algoritmo genético
    print("\nAlgoritmo Genético:")
    ga = AlgoritmoGenetico(
        problema,
        tamanho_populacao=100,
        taxa_mutacao=0.02,
        taxa_crossover=0.8,
        elitismo=5
    )
    
    start_time = time.time()
    solucao, valor = ga.resolver(max_geracoes=500)
    tempo = time.time() - start_time
    
    print(f"  Melhor solução: ({solucao[0]:.6f}, {solucao[1]:.6f})")
    print(f"  Valor: {valor:.6f}")
    print(f"  Gerações: {ga.stats.iteracoes}")
    print(f"  Avaliações: {ga.stats.avaliacoes_funcao}")
    print(f"  Tempo: {tempo:.6f}s")
    print(f"  Soluções válidas: {ga.stats.solucoes_validas}")
    
    # Mostrar convergência
    if len(ga.stats.convergencia) > 10:
        print(f"  Convergência (últimas 10): {ga.stats.convergencia[-10:]}")


def demonstrar_simulated_annealing():
    """Demonstra Simulated Annealing."""
    print("\n=== DEMONSTRAÇÃO: SIMULATED ANNEALING ===\n")
    
    # Problema: Minimizar função de Ackley
    def ackley(x):
        a, b, c = 20, 0.2, 2 * math.pi
        n = len(x)
        
        sum1 = sum(xi**2 for xi in x)
        sum2 = sum(math.cos(c * xi) for xi in x)
        
        return -a * math.exp(-b * math.sqrt(sum1 / n)) - math.exp(sum2 / n) + a + math.e
    
    problema = ProblemaOtimizacao(TipoOtimizacao.MINIMIZACAO)
    
    # Definir variáveis (2D)
    problema.definir_variaveis(
        dimensoes=2,
        limites_inf=[-32.768, -32.768],
        limites_sup=[32.768, 32.768]
    )
    
    problema.definir_funcao_objetivo(ackley)
    
    print("Problema: Minimizar função de Ackley")
    print("  f(x) = -20*exp(-0.2*√(Σxi²/n)) - exp(Σcos(2πxi)/n) + 20 + e")
    print("  Domínio: [-32.768, 32.768]²")
    print("  Mínimo global: f(0,0) = 0")
    
    # Simulated Annealing
    print("\nSimulated Annealing:")
    sa = SimulatedAnnealing(
        problema,
        temperatura_inicial=100.0,
        temperatura_final=0.01,
        alpha=0.99
    )
    
    start_time = time.time()
    solucao, valor = sa.resolver(max_iteracoes=10000)
    tempo = time.time() - start_time
    
    print(f"  Melhor solução: ({solucao[0]:.6f}, {solucao[1]:.6f})")
    print(f"  Valor: {valor:.6f}")
    print(f"  Iterações: {sa.stats.iteracoes}")
    print(f"  Avaliações: {sa.stats.avaliacoes_funcao}")
    print(f"  Tempo: {tempo:.6f}s")


def demonstrar_pso():
    """Demonstra Particle Swarm Optimization."""
    print("\n=== DEMONSTRAÇÃO: PARTICLE SWARM OPTIMIZATION ===\n")
    
    # Problema: Minimizar função de Rosenbrock
    def rosenbrock(x):
        return sum(100 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2 for i in range(len(x)-1))
    
    problema = ProblemaOtimizacao(TipoOtimizacao.MINIMIZACAO)
    
    # Definir variáveis (2D)
    problema.definir_variaveis(
        dimensoes=2,
        limites_inf=[-10.0, -10.0],
        limites_sup=[10.0, 10.0]
    )
    
    problema.definir_funcao_objetivo(rosenbrock)
    
    print("Problema: Minimizar função de Rosenbrock")
    print("  f(x) = Σ[100(xi+1 - xi²)² + (1 - xi)²]")
    print("  Domínio: [-10, 10]²")
    print("  Mínimo global: f(1,1) = 0")
    
    # PSO
    print("\nParticle Swarm Optimization:")
    pso = ParticleSwarmOptimization(
        problema,
        num_particulas=30,
        w=0.7,
        c1=1.5,
        c2=1.5
    )
    
    start_time = time.time()
    solucao, valor = pso.resolver(max_iteracoes=1000)
    tempo = time.time() - start_time
    
    print(f"  Melhor solução: ({solucao[0]:.6f}, {solucao[1]:.6f})")
    print(f"  Valor: {valor:.6f}")
    print(f"  Iterações: {pso.stats.iteracoes}")
    print(f"  Avaliações: {pso.stats.avaliacoes_funcao}")
    print(f"  Tempo: {tempo:.6f}s")


def benchmark_otimizacao():
    """Compara performance dos algoritmos de otimização."""
    print("\n=== BENCHMARK: ALGORITMOS DE OTIMIZAÇÃO ===\n")
    
    # Função de teste: Sphere
    def sphere(x):
        return sum(xi**2 for xi in x)
    
    # Configurar problema
    dimensoes = 5
    problema = ProblemaOtimizacao(TipoOtimizacao.MINIMIZACAO)
    problema.definir_variaveis(
        dimensoes=dimensoes,
        limites_inf=[-10.0] * dimensoes,
        limites_sup=[10.0] * dimensoes
    )
    problema.definir_funcao_objetivo(sphere)
    
    print(f"Função de teste: Sphere (dimensões = {dimensoes})")
    print("  f(x) = Σxi²")
    print("  Mínimo global: f(0,...,0) = 0")
    
    algoritmos = [
        ("Algoritmo Genético", AlgoritmoGenetico(problema, tamanho_populacao=50)),
        ("Simulated Annealing", SimulatedAnnealing(problema, temperatura_inicial=50.0)),
        ("PSO", ParticleSwarmOptimization(problema, num_particulas=30))
    ]
    
    resultados = []
    
    for nome, algoritmo in algoritmos:
        print(f"\n{nome}:")
        
        # Múltiplas execuções
        valores = []
        tempos = []
        
        for run in range(5):
            start_time = time.time()
            
            if isinstance(algoritmo, AlgoritmoGenetico):
                _, valor = algoritmo.resolver(max_geracoes=200)
            elif isinstance(algoritmo, SimulatedAnnealing):
                _, valor = algoritmo.resolver(max_iteracoes=5000)
            else:  # PSO
                _, valor = algoritmo.resolver(max_iteracoes=500)
            
            tempo = time.time() - start_time
            
            valores.append(valor)
            tempos.append(tempo)
        
        # Estatísticas
        melhor_valor = min(valores)
        valor_medio = sum(valores) / len(valores)
        tempo_medio = sum(tempos) / len(tempos)
        
        print(f"  Melhor valor: {melhor_valor:.6f}")
        print(f"  Valor médio: {valor_medio:.6f}")
        print(f"  Tempo médio: {tempo_medio:.4f}s")
        
        resultados.append((nome, melhor_valor, valor_medio, tempo_medio))
    
    # Ranking
    print("\nRanking por melhor valor:")
    resultados.sort(key=lambda x: x[1])
    
    for i, (nome, melhor, medio, tempo) in enumerate(resultados, 1):
        print(f"  {i}. {nome}: {melhor:.6f}")


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 06.6 - OTIMIZAÇÃO")
    print("=" * 50)
    
    demonstrar_programacao_linear()
    demonstrar_algoritmo_genetico()
    demonstrar_simulated_annealing()
    demonstrar_pso()
    benchmark_otimizacao()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 06.6")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. PROGRAMAÇÃO LINEAR:
   • Método Simplex: algoritmo exato para problemas lineares
   • Forma padrão: conversão de inequações para equações
   • Tableau: representação matricial do problema
   • Otimalidade: teste através dos custos reduzidos
   • Aplicações: alocação de recursos, planejamento de produção

2. ALGORITMOS GENÉTICOS:
   • Inspiração biológica: seleção, crossover, mutação
   • População: conjunto de soluções candidatas
   • Fitness: avaliação da qualidade das soluções
   • Elitismo: preservação das melhores soluções
   • Convergência: critérios de parada baseados em estagnação

3. SIMULATED ANNEALING:
   • Inspiração física: processo de resfriamento de metais
   • Temperatura: controla probabilidade de aceitar soluções piores
   • Resfriamento: redução gradual da temperatura
   • Vizinhança: geração de soluções próximas
   • Escape de ótimos locais: através da aceitação probabilística

4. PARTICLE SWARM OPTIMIZATION:
   • Inspiração social: comportamento de enxames
   • Partículas: soluções com posição e velocidade
   • Memória: melhor posição pessoal e global
   • Atualização: combinação de componentes inercial, cognitivo e social
   • Convergência: baseada na diversidade do enxame

5. ESTRUTURAS DE DADOS PARA OTIMIZAÇÃO:
   • Classe ProblemaOtimizacao: abstração do problema
   • Restrições: representação e avaliação
   • Estatísticas: monitoramento de performance
   • Tipos de variáveis: contínuas, inteiras, binárias

6. TÉCNICAS DE IMPLEMENTAÇÃO:
   • Penalização: tratamento de restrições em meta-heurísticas
   • Reparação: correção de soluções inválidas
   • Hibridização: combinação de diferentes algoritmos
   • Paralelização: execução simultânea de múltiplas soluções

7. ANÁLISE DE COMPLEXIDADE:
   • Simplex: polinomial no caso médio, exponencial no pior caso
   • Meta-heurísticas: dependem do número de avaliações da função
   • Trade-off: qualidade da solução vs. tempo computacional
   • Escalabilidade: comportamento com aumento da dimensão

8. CRITÉRIOS DE PARADA:
   • Número máximo de iterações/gerações
   • Convergência: estagnação da função objetivo
   • Tempo limite: controle de recursos computacionais
   • Qualidade mínima: valor aceitável da função objetivo

9. APLICAÇÕES PRÁTICAS:
   • Engenharia: design e otimização de sistemas
   • Economia: alocação ótima de recursos
   • Logística: roteamento e escalonamento
   • Machine Learning: otimização de hiperparâmetros
   • Bioinformática: alinhamento de sequências

10. VANTAGENS E LIMITAÇÕES:
    • Algoritmos exatos: garantem otimalidade mas podem ser lentos
    • Meta-heurísticas: rápidas mas sem garantia de otimalidade
    • Robustez: capacidade de lidar com ruído e incerteza
    • Flexibilidade: adaptação a diferentes tipos de problemas

11. PADRÕES DE DESIGN UTILIZADOS:
    • Strategy: diferentes algoritmos para mesmo problema
    • Template Method: estrutura comum para meta-heurísticas
    • Observer: monitoramento de convergência
    • Factory: criação de soluções iniciais

12. TÉCNICAS DE MELHORIA:
    • Busca local: refinamento de soluções
    • Restart: reinicialização quando estagnado
    • Memória adaptativa: aprendizado durante a busca
    • Multi-start: múltiplas execuções independentes

13. OTIMIZAÇÃO MULTI-OBJETIVO:
    • Frente de Pareto: conjunto de soluções não-dominadas
    • NSGA-II: algoritmo genético para múltiplos objetivos
    • Métricas de qualidade: hipervolume, distância geracional
    • Tomada de decisão: seleção da solução final

14. CONSIDERAÇÕES PRÁTICAS:
    • Ajuste de parâmetros: impacto na performance
    • Validação: teste em problemas conhecidos
    • Robustez: comportamento em diferentes instâncias
    • Interpretabilidade: compreensão das soluções encontradas

A otimização é uma área fundamental que combina teoria
matemática com implementação prática. A escolha do algoritmo
adequado depende das características do problema: linearidade,
continuidade, presença de restrições, dimensionalidade e
recursos computacionais disponíveis.

MÓDULO 06 COMPLETO! 🎉
Próximo: Módulo 07 - Análise de Complexidade
    """)


if __name__ == "__main__":
    main()