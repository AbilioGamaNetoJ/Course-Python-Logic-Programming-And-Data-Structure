"""
Módulo: Introdução aos Algoritmos de Busca e Ordenação
Tópico: Algoritmos de Busca e Ordenação - Fundamentos
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário

Objetivos de Aprendizado:
- Compreender o conceito de algoritmo
- Entender a importância da busca e ordenação
- Conhecer critérios de avaliação de algoritmos
- Identificar diferentes tipos de algoritmos
- Analisar complexidade temporal e espacial
- Reconhecer trade-offs entre algoritmos
- Aplicar conceitos na escolha de algoritmos
- Desenvolver pensamento algorítmico

Conceitos Abordados:
- Definição de algoritmo
- Características de bons algoritmos
- Classificação de algoritmos
- Análise de complexidade
- Estabilidade em ordenação
- Algoritmos in-place vs out-of-place
- Casos: melhor, médio e pior
- Benchmarking de algoritmos

Pré-requisitos:
- Módulos 01 e 02 completos
- Conhecimento de estruturas de dados nativas
- Compreensão de loops e funções
- Noções básicas de matemática

Complexidade dos Algoritmos Abordados:
- Busca Linear: O(n)
- Busca Binária: O(log n)
- Bubble Sort: O(n²)
- Selection Sort: O(n²)
- Insertion Sort: O(n²)
- Merge Sort: O(n log n)
- Quick Sort: O(n log n) médio, O(n²) pior caso
"""

import time
import random
import math
import sys
from typing import List, Tuple, Any, Callable
import matplotlib.pyplot as plt
import numpy as np

def conceito_algoritmo():
    """
    Introduz o conceito fundamental de algoritmo.
    
    Analogia: Um algoritmo é como uma receita de culinária - 
    um conjunto de instruções precisas para resolver um problema.
    """
    print("=== CONCEITO DE ALGORITMO ===")
    print()
    
    print("1. DEFINIÇÃO:")
    print("   Um algoritmo é uma sequência finita de instruções bem definidas")
    print("   para resolver um problema ou realizar uma tarefa específica.")
    print()
    
    print("2. CARACTERÍSTICAS DE UM BOM ALGORITMO:")
    print("   ┌─────────────────┬─────────────────────────────────────────┐")
    print("   │ CARACTERÍSTICA  │               DESCRIÇÃO                 │")
    print("   ├─────────────────┼─────────────────────────────────────────┤")
    print("   │ Finitude        │ Deve terminar após um número finito    │")
    print("   │                 │ de passos                               │")
    print("   ├─────────────────┼─────────────────────────────────────────┤")
    print("   │ Definição       │ Cada passo deve ser precisamente        │")
    print("   │                 │ definido                                │")
    print("   ├─────────────────┼─────────────────────────────────────────┤")
    print("   │ Entrada         │ Deve aceitar zero ou mais entradas      │")
    print("   ├─────────────────┼─────────────────────────────────────────┤")
    print("   │ Saída           │ Deve produzir pelo menos uma saída      │")
    print("   ├─────────────────┼─────────────────────────────────────────┤")
    print("   │ Efetividade     │ Cada operação deve ser básica o         │")
    print("   │                 │ suficiente para ser executada          │")
    print("   └─────────────────┴─────────────────────────────────────────┘")
    print()
    
    print("3. EXEMPLO PRÁTICO - ALGORITMO PARA FAZER CHÁ:")
    print("   Entrada: Água, saquinho de chá, açúcar (opcional)")
    print("   Algoritmo:")
    print("   1. Ferva a água")
    print("   2. Coloque o saquinho de chá na xícara")
    print("   3. Despeje a água fervente na xícara")
    print("   4. Deixe em infusão por 3-5 minutos")
    print("   5. Remova o saquinho de chá")
    print("   6. Se desejar, adicione açúcar")
    print("   7. Mexa bem")
    print("   Saída: Chá pronto para consumo")
    print()
    
    print("4. ALGORITMO EM PROGRAMAÇÃO - ENCONTRAR O MAIOR NÚMERO:")
    
    def encontrar_maior_numero(numeros):
        """
        Algoritmo para encontrar o maior número em uma lista.
        
        Entrada: Lista de números
        Saída: O maior número da lista
        """
        if not numeros:  # Verificação de entrada válida
            return None
        
        maior = numeros[0]  # Inicialização
        
        for numero in numeros[1:]:  # Iteração
            if numero > maior:  # Comparação
                maior = numero  # Atualização
        
        return maior  # Retorno do resultado
    
    # Demonstração
    lista_exemplo = [3, 7, 2, 9, 1, 5, 8]
    resultado = encontrar_maior_numero(lista_exemplo)
    
    print("   Exemplo prático:")
    print(f"   → Lista: {lista_exemplo}")
    print(f"   → Maior número: {resultado}")
    print()
    
    print("5. PASSOS DO ALGORITMO:")
    print("   1. Verificar se a lista não está vazia")
    print("   2. Assumir que o primeiro elemento é o maior")
    print("   3. Comparar cada elemento seguinte com o maior atual")
    print("   4. Se encontrar um número maior, atualizá-lo")
    print("   5. Retornar o maior número encontrado")
    print()
    
    print("6. ANÁLISE DO ALGORITMO:")
    print(f"   → Complexidade temporal: O(n) - visita cada elemento uma vez")
    print(f"   → Complexidade espacial: O(1) - usa espaço constante")
    print(f"   → Número de comparações: {len(lista_exemplo) - 1}")
    print(f"   → É ótimo? Sim, não há como fazer melhor que O(n)")
    print()

def tipos_algoritmos():
    """
    Apresenta diferentes tipos e classificações de algoritmos.
    """
    print("=== TIPOS E CLASSIFICAÇÕES DE ALGORITMOS ===")
    print()
    
    print("1. CLASSIFICAÇÃO POR PARADIGMA:")
    print()
    
    print("   A) ALGORITMOS ITERATIVOS:")
    print("      → Usam loops (for, while)")
    print("      → Controle explícito do fluxo")
    print("      → Geralmente mais eficientes em espaço")
    
    def busca_iterativa(lista, item):
        """Busca iterativa - usa loop"""
        for i, elemento in enumerate(lista):
            if elemento == item:
                return i
        return -1
    
    print("      Exemplo - Busca Linear Iterativa:")
    lista = [1, 3, 5, 7, 9]
    resultado = busca_iterativa(lista, 5)
    print(f"      → Buscar 5 em {lista}: índice {resultado}")
    print()
    
    print("   B) ALGORITMOS RECURSIVOS:")
    print("      → Função chama a si mesma")
    print("      → Caso base para parar a recursão")
    print("      → Elegantes mas podem usar mais memória")
    
    def busca_recursiva(lista, item, inicio=0):
        """Busca recursiva - função chama a si mesma"""
        if inicio >= len(lista):
            return -1
        if lista[inicio] == item:
            return inicio
        return busca_recursiva(lista, item, inicio + 1)
    
    resultado_rec = busca_recursiva(lista, 5)
    print("      Exemplo - Busca Linear Recursiva:")
    print(f"      → Buscar 5 em {lista}: índice {resultado_rec}")
    print()
    
    print("2. CLASSIFICAÇÃO POR ESTRATÉGIA:")
    print()
    
    print("   A) FORÇA BRUTA (BRUTE FORCE):")
    print("      → Testa todas as possibilidades")
    print("      → Simples de implementar")
    print("      → Pode ser ineficiente")
    
    def ordenacao_bruta(lista):
        """Ordenação por força bruta - testa todas as permutações"""
        import itertools
        
        if len(lista) <= 1:
            return lista
        
        # Para listas pequenas, gera todas as permutações
        if len(lista) <= 8:  # Limitando para evitar explosão combinatória
            for permutacao in itertools.permutations(lista):
                if list(permutacao) == sorted(lista):
                    return list(permutacao)
        
        # Para listas maiores, usa algoritmo mais eficiente
        return sorted(lista)
    
    lista_pequena = [3, 1, 4, 2]
    resultado_bruta = ordenacao_bruta(lista_pequena)
    print(f"      → Ordenar {lista_pequena}: {resultado_bruta}")
    print()
    
    print("   B) DIVIDIR E CONQUISTAR:")
    print("      → Divide o problema em subproblemas menores")
    print("      → Resolve os subproblemas recursivamente")
    print("      → Combina as soluções")
    
    def busca_binaria_recursiva(lista, item, inicio=0, fim=None):
        """Busca binária - dividir e conquistar"""
        if fim is None:
            fim = len(lista) - 1
        
        if inicio > fim:
            return -1
        
        meio = (inicio + fim) // 2
        
        if lista[meio] == item:
            return meio
        elif lista[meio] > item:
            return busca_binaria_recursiva(lista, item, inicio, meio - 1)
        else:
            return busca_binaria_recursiva(lista, item, meio + 1, fim)
    
    lista_ordenada = [1, 3, 5, 7, 9, 11, 13, 15]
    resultado_binaria = busca_binaria_recursiva(lista_ordenada, 7)
    print(f"      → Busca binária de 7 em {lista_ordenada}: índice {resultado_binaria}")
    print()
    
    print("   C) ALGORITMOS GULOSOS (GREEDY):")
    print("      → Fazem a escolha localmente ótima")
    print("      → Esperam que leve à solução global ótima")
    print("      → Rápidos mas nem sempre ótimos")
    
    def troco_guloso(valor, moedas):
        """Algoritmo guloso para dar troco"""
        moedas_ordenadas = sorted(moedas, reverse=True)
        troco = []
        
        for moeda in moedas_ordenadas:
            while valor >= moeda:
                troco.append(moeda)
                valor -= moeda
        
        return troco if valor == 0 else None
    
    moedas_disponiveis = [1, 5, 10, 25, 50, 100]
    troco_resultado = troco_guloso(67, moedas_disponiveis)
    print(f"      → Troco de 67 centavos: {troco_resultado}")
    print()
    
    print("3. CLASSIFICAÇÃO POR COMPLEXIDADE:")
    print()
    
    complexidades = [
        ("O(1)", "Constante", "Acesso a array por índice"),
        ("O(log n)", "Logarítmica", "Busca binária"),
        ("O(n)", "Linear", "Busca linear"),
        ("O(n log n)", "Linearítmica", "Merge sort, heap sort"),
        ("O(n²)", "Quadrática", "Bubble sort, selection sort"),
        ("O(n³)", "Cúbica", "Multiplicação de matrizes ingênua"),
        ("O(2ⁿ)", "Exponencial", "Subconjuntos, Torre de Hanói"),
        ("O(n!)", "Fatorial", "Problema do caixeiro viajante")
    ]
    
    print("   ┌─────────────┬─────────────────┬─────────────────────────────┐")
    print("   │ COMPLEXIDADE│   DESCRIÇÃO     │         EXEMPLO             │")
    print("   ├─────────────┼─────────────────┼─────────────────────────────┤")
    
    for complexidade, descricao, exemplo in complexidades:
        print(f"   │ {complexidade:11} │ {descricao:15} │ {exemplo:27} │")
    
    print("   └─────────────┴─────────────────┴─────────────────────────────┘")
    print()
    
    print("4. VISUALIZAÇÃO DE CRESCIMENTO:")
    
    # Simulando crescimento para diferentes tamanhos
    tamanhos = [1, 10, 100, 1000]
    
    print("   Operações necessárias para diferentes tamanhos:")
    print("   ┌─────────┬─────────┬─────────┬─────────┬─────────┐")
    print("   │    n    │  O(1)   │ O(log n)│  O(n)   │ O(n²)   │")
    print("   ├─────────┼─────────┼─────────┼─────────┼─────────┤")
    
    for n in tamanhos:
        o1 = 1
        olog = math.ceil(math.log2(n)) if n > 0 else 0
        on = n
        on2 = n * n
        
        print(f"   │ {n:7} │ {o1:7} │ {olog:7} │ {on:7} │ {on2:7} │")
    
    print("   └─────────┴─────────┴─────────┴─────────┴─────────┘")
    print()

def analise_complexidade():
    """
    Ensina análise de complexidade temporal e espacial.
    """
    print("=== ANÁLISE DE COMPLEXIDADE ===")
    print()
    
    print("1. COMPLEXIDADE TEMPORAL:")
    print("   → Mede quanto tempo um algoritmo leva para executar")
    print("   → Expressa em função do tamanho da entrada (n)")
    print("   → Foca no crescimento assintótico")
    print("   → Ignora constantes e termos de menor ordem")
    print()
    
    print("2. COMO ANALISAR:")
    print()
    
    print("   A) CONTAR OPERAÇÕES BÁSICAS:")
    
    def exemplo_analise_1(lista):
        """Exemplo 1: Análise de complexidade O(n)"""
        contador = 0  # 1 operação
        
        for elemento in lista:  # n iterações
            contador += elemento  # 1 operação por iteração
        
        return contador  # 1 operação
        # Total: 1 + n + 1 = n + 2 = O(n)
    
    print("      Função que soma elementos de uma lista:")
    print("      → Inicialização: 1 operação")
    print("      → Loop: n iterações")
    print("      → Soma por iteração: 1 operação")
    print("      → Retorno: 1 operação")
    print("      → Total: 1 + n×1 + 1 = n + 2 = O(n)")
    print()
    
    print("   B) LOOPS ANINHADOS:")
    
    def exemplo_analise_2(matriz):
        """Exemplo 2: Análise de complexidade O(n²)"""
        soma = 0  # 1 operação
        
        for i in range(len(matriz)):  # n iterações
            for j in range(len(matriz[i])):  # n iterações para cada i
                soma += matriz[i][j]  # 1 operação por par (i,j)
        
        return soma  # 1 operação
        # Total: 1 + n×n×1 + 1 = n² + 2 = O(n²)
    
    print("      Função que soma elementos de uma matriz n×n:")
    print("      → Loop externo: n iterações")
    print("      → Loop interno: n iterações para cada externa")
    print("      → Operação interna: 1 por par (i,j)")
    print("      → Total: n × n × 1 = n² = O(n²)")
    print()
    
    print("3. CASOS DE ANÁLISE:")
    print()
    
    def busca_linear_casos(lista, item):
        """Demonstra diferentes casos de complexidade"""
        comparacoes = 0
        
        for i, elemento in enumerate(lista):
            comparacoes += 1
            if elemento == item:
                return i, comparacoes
        
        return -1, comparacoes
    
    lista_teste = [1, 3, 5, 7, 9, 11, 13, 15]
    
    # Melhor caso: item no início
    pos_melhor, comp_melhor = busca_linear_casos(lista_teste, 1)
    print(f"   MELHOR CASO (item no início):")
    print(f"   → Buscar {1} em {lista_teste}")
    print(f"   → Posição: {pos_melhor}, Comparações: {comp_melhor}")
    print(f"   → Complexidade: O(1)")
    print()
    
    # Caso médio: item no meio
    pos_medio, comp_medio = busca_linear_casos(lista_teste, 7)
    print(f"   CASO MÉDIO (item no meio):")
    print(f"   → Buscar {7} em {lista_teste}")
    print(f"   → Posição: {pos_medio}, Comparações: {comp_medio}")
    print(f"   → Complexidade: O(n/2) = O(n)")
    print()
    
    # Pior caso: item no final ou não existe
    pos_pior, comp_pior = busca_linear_casos(lista_teste, 15)
    print(f"   PIOR CASO (item no final):")
    print(f"   → Buscar {15} em {lista_teste}")
    print(f"   → Posição: {pos_pior}, Comparações: {comp_pior}")
    print(f"   → Complexidade: O(n)")
    print()
    
    # Item não existe
    pos_inexistente, comp_inexistente = busca_linear_casos(lista_teste, 20)
    print(f"   PIOR CASO (item não existe):")
    print(f"   → Buscar {20} em {lista_teste}")
    print(f"   → Posição: {pos_inexistente}, Comparações: {comp_inexistente}")
    print(f"   → Complexidade: O(n)")
    print()
    
    print("4. COMPLEXIDADE ESPACIAL:")
    print("   → Mede quanto espaço adicional um algoritmo usa")
    print("   → Também expressa em função do tamanho da entrada")
    print("   → Considera apenas espaço adicional, não a entrada")
    print()
    
    def exemplo_espaco_constante(lista):
        """Espaço O(1) - constante"""
        maior = lista[0]  # 1 variável
        for elemento in lista[1:]:
            if elemento > maior:
                maior = elemento
        return maior
        # Espaço: O(1) - apenas uma variável adicional
    
    def exemplo_espaco_linear(lista):
        """Espaço O(n) - linear"""
        copia = []  # Lista que cresce com n
        for elemento in lista:
            copia.append(elemento * 2)
        return copia
        # Espaço: O(n) - lista do mesmo tamanho da entrada
    
    print("   Exemplo - Espaço Constante O(1):")
    print("   → Encontrar maior elemento usando apenas uma variável")
    print("   → Não importa o tamanho da lista, usa sempre o mesmo espaço")
    print()
    
    print("   Exemplo - Espaço Linear O(n):")
    print("   → Criar cópia da lista com elementos dobrados")
    print("   → Espaço cresce proporcionalmente ao tamanho da entrada")
    print()
    
    print("5. TRADE-OFFS TEMPO vs ESPAÇO:")
    print()
    
    # Fibonacci - versão recursiva (tempo exponencial, espaço linear)
    def fibonacci_recursivo(n):
        """Fibonacci recursivo - O(2^n) tempo, O(n) espaço"""
        if n <= 1:
            return n
        return fibonacci_recursivo(n-1) + fibonacci_recursivo(n-2)
    
    # Fibonacci - versão com memoização (tempo linear, espaço linear)
    def fibonacci_memoizado(n, memo={}):
        """Fibonacci memoizado - O(n) tempo, O(n) espaço"""
        if n in memo:
            return memo[n]
        if n <= 1:
            memo[n] = n
            return n
        memo[n] = fibonacci_memoizado(n-1, memo) + fibonacci_memoizado(n-2, memo)
        return memo[n]
    
    # Fibonacci - versão iterativa (tempo linear, espaço constante)
    def fibonacci_iterativo(n):
        """Fibonacci iterativo - O(n) tempo, O(1) espaço"""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    n_teste = 10
    
    print(f"   Calculando Fibonacci({n_teste}):")
    print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │    VERSÃO       │    TEMPO    │   ESPAÇO    │ RESULTADO   │")
    print("   ├─────────────────┼─────────────┼─────────────┼─────────────┤")
    print("   │ Recursiva       │    O(2ⁿ)    │    O(n)     │     ?       │")
    print("   │ Memoizada       │    O(n)     │    O(n)     │     ?       │")
    print("   │ Iterativa       │    O(n)     │    O(1)     │     ?       │")
    print("   └─────────────────┴─────────────┴─────────────┴─────────────┘")
    
    # Calculando resultados (apenas para versões eficientes)
    resultado_memo = fibonacci_memoizado(n_teste)
    resultado_iter = fibonacci_iterativo(n_teste)
    
    print(f"   → Memoizada: {resultado_memo}")
    print(f"   → Iterativa: {resultado_iter}")
    print("   → Recursiva: muito lenta para n > 30")
    print()

def criterios_avaliacao():
    """
    Apresenta critérios para avaliar e comparar algoritmos.
    """
    print("=== CRITÉRIOS DE AVALIAÇÃO DE ALGORITMOS ===")
    print()
    
    print("1. CRITÉRIOS PRINCIPAIS:")
    print()
    
    criterios = [
        ("Correção", "O algoritmo produz a saída correta para todas as entradas válidas"),
        ("Eficiência Temporal", "Quão rápido o algoritmo executa"),
        ("Eficiência Espacial", "Quanta memória o algoritmo usa"),
        ("Simplicidade", "Quão fácil é entender e implementar"),
        ("Generalidade", "Quão amplo é o conjunto de problemas que resolve"),
        ("Estabilidade", "Mantém ordem relativa de elementos iguais (ordenação)"),
        ("Adaptabilidade", "Performance em dados já parcialmente ordenados"),
        ("In-place", "Modifica a estrutura original sem usar espaço extra")
    ]
    
    print("   ┌─────────────────┬─────────────────────────────────────────────┐")
    print("   │   CRITÉRIO      │                DESCRIÇÃO                    │")
    print("   ├─────────────────┼─────────────────────────────────────────────┤")
    
    for criterio, descricao in criterios:
        print(f"   │ {criterio:15} │ {descricao:43} │")
    
    print("   └─────────────────┴─────────────────────────────────────────────┘")
    print()
    
    print("2. EXEMPLO PRÁTICO - COMPARANDO ALGORITMOS DE ORDENAÇÃO:")
    print()
    
    def bubble_sort(lista):
        """Bubble Sort - simples mas ineficiente"""
        n = len(lista)
        lista_copia = lista.copy()
        comparacoes = 0
        trocas = 0
        
        for i in range(n):
            for j in range(0, n - i - 1):
                comparacoes += 1
                if lista_copia[j] > lista_copia[j + 1]:
                    lista_copia[j], lista_copia[j + 1] = lista_copia[j + 1], lista_copia[j]
                    trocas += 1
        
        return lista_copia, comparacoes, trocas
    
    def selection_sort(lista):
        """Selection Sort - menos trocas que bubble sort"""
        n = len(lista)
        lista_copia = lista.copy()
        comparacoes = 0
        trocas = 0
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                comparacoes += 1
                if lista_copia[j] < lista_copia[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                lista_copia[i], lista_copia[min_idx] = lista_copia[min_idx], lista_copia[i]
                trocas += 1
        
        return lista_copia, comparacoes, trocas
    
    def insertion_sort(lista):
        """Insertion Sort - eficiente para listas pequenas"""
        lista_copia = lista.copy()
        comparacoes = 0
        trocas = 0
        
        for i in range(1, len(lista_copia)):
            chave = lista_copia[i]
            j = i - 1
            
            while j >= 0:
                comparacoes += 1
                if lista_copia[j] > chave:
                    lista_copia[j + 1] = lista_copia[j]
                    trocas += 1
                    j -= 1
                else:
                    break
            
            lista_copia[j + 1] = chave
        
        return lista_copia, comparacoes, trocas
    
    # Testando com uma lista pequena
    lista_teste = [64, 34, 25, 12, 22, 11, 90]
    print(f"   Lista original: {lista_teste}")
    print()
    
    # Executando algoritmos
    resultado_bubble, comp_bubble, troca_bubble = bubble_sort(lista_teste)
    resultado_selection, comp_selection, troca_selection = selection_sort(lista_teste)
    resultado_insertion, comp_insertion, troca_insertion = insertion_sort(lista_teste)
    
    print("   Comparação dos algoritmos:")
    print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │   ALGORITMO     │ COMPARAÇÕES │   TROCAS    │ COMPLEXIDADE│")
    print("   ├─────────────────┼─────────────┼─────────────┼─────────────┤")
    print(f"   │ Bubble Sort     │ {comp_bubble:11} │ {troca_bubble:11} │    O(n²)    │")
    print(f"   │ Selection Sort  │ {comp_selection:11} │ {troca_selection:11} │    O(n²)    │")
    print(f"   │ Insertion Sort  │ {comp_insertion:11} │ {troca_insertion:11} │    O(n²)    │")
    print("   └─────────────────┴─────────────┴─────────────┴─────────────┘")
    print()
    
    print("3. ANÁLISE DOS RESULTADOS:")
    print(f"   → Todos produziram o resultado correto: {resultado_bubble}")
    print(f"   → Selection Sort fez menos trocas: {troca_selection} vs {troca_bubble} (Bubble)")
    print(f"   → Insertion Sort foi mais eficiente neste caso: {comp_insertion} comparações")
    print("   → Para listas pequenas, Insertion Sort é frequentemente o melhor")
    print()
    
    print("4. ESTABILIDADE EM ORDENAÇÃO:")
    print()
    
    # Demonstrando estabilidade
    class Pessoa:
        def __init__(self, nome, idade):
            self.nome = nome
            self.idade = idade
        
        def __repr__(self):
            return f"{self.nome}({self.idade})"
    
    pessoas = [
        Pessoa("Ana", 25),
        Pessoa("Bruno", 30),
        Pessoa("Carlos", 25),
        Pessoa("Diana", 30)
    ]
    
    print("   Lista de pessoas (nome, idade):")
    print(f"   Original: {pessoas}")
    
    # Ordenação estável por idade (mantém ordem original para idades iguais)
    def ordenacao_estavel_por_idade(pessoas):
        """Insertion sort é estável"""
        lista_copia = pessoas.copy()
        
        for i in range(1, len(lista_copia)):
            chave = lista_copia[i]
            j = i - 1
            
            while j >= 0 and lista_copia[j].idade > chave.idade:
                lista_copia[j + 1] = lista_copia[j]
                j -= 1
            
            lista_copia[j + 1] = chave
        
        return lista_copia
    
    pessoas_ordenadas = ordenacao_estavel_por_idade(pessoas)
    print(f"   Ordenado por idade (estável): {pessoas_ordenadas}")
    print("   → Ana(25) vem antes de Carlos(25) - ordem original mantida")
    print("   → Bruno(30) vem antes de Diana(30) - ordem original mantida")
    print()
    
    print("5. ALGORITMOS IN-PLACE vs OUT-OF-PLACE:")
    print()
    
    def ordenacao_in_place(lista):
        """Modifica a lista original - O(1) espaço extra"""
        n = len(lista)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista[j] > lista[j + 1]:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
        return lista
    
    def ordenacao_out_of_place(lista):
        """Cria nova lista - O(n) espaço extra"""
        return sorted(lista)
    
    lista_original = [3, 1, 4, 1, 5, 9, 2, 6]
    lista_copia = lista_original.copy()
    
    print(f"   Lista original: {lista_original}")
    
    # In-place
    resultado_in_place = ordenacao_in_place(lista_copia)
    print(f"   In-place: {resultado_in_place}")
    print(f"   Lista original modificada: {lista_copia}")
    
    # Out-of-place
    resultado_out_of_place = ordenacao_out_of_place(lista_original)
    print(f"   Out-of-place: {resultado_out_of_place}")
    print(f"   Lista original preservada: {lista_original}")
    print()

if __name__ == "__main__":
    print("MÓDULO 3.1 - INTRODUÇÃO AOS ALGORITMOS")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceito_algoritmo()
    print("\n" + "="*50 + "\n")
    
    tipos_algoritmos()
    print("\n" + "="*50 + "\n")
    
    analise_complexidade()
    print("\n" + "="*50 + "\n")
    
    criterios_avaliacao()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 3.1 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceito fundamental de algoritmo")
    print("✅ Tipos e classificações de algoritmos")
    print("✅ Análise de complexidade temporal e espacial")
    print("✅ Critérios de avaliação de algoritmos")
    print("✅ Estabilidade e algoritmos in-place")
    print("✅ Trade-offs entre tempo e espaço")
    print("✅ Casos: melhor, médio e pior")
    print("\n➡️  Próximo: Módulo 3.2 - Algoritmos de Busca Linear")