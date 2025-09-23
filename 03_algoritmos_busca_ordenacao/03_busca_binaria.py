"""
Módulo: Algoritmos de Busca Binária
Tópico: Algoritmos de Busca e Ordenação - Busca Logarítmica
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário

Objetivos de Aprendizado:
- Compreender o conceito de busca binária
- Implementar busca binária iterativa e recursiva
- Analisar complexidade logarítmica O(log n)
- Comparar performance com busca linear
- Identificar pré-requisitos e limitações
- Aplicar busca binária em problemas reais
- Implementar variações avançadas
- Desenvolver intuição sobre algoritmos "divide e conquista"

Conceitos Abordados:
- Algoritmo divide e conquista
- Busca binária iterativa
- Busca binária recursiva
- Análise de complexidade O(log n)
- Pré-requisitos (dados ordenados)
- Variações (primeira/última ocorrência)
- Busca em intervalos
- Aplicações práticas

Pré-requisitos:
- Módulos 3.1 e 3.2 completos
- Compreensão de recursão
- Conhecimento de listas ordenadas
- Familiaridade com complexidade logarítmica

Complexidade:
- Temporal: O(log n) - logarítmica
- Espacial: O(1) iterativa, O(log n) recursiva
- Melhor caso: O(1) - elemento no meio
- Pior caso: O(log n) - elemento nas extremidades
"""

import time
import random
import math
from typing import List, Optional, Tuple, Union

def conceito_busca_binaria():
    """
    Introduz o conceito fundamental de busca binária.
    
    Analogia: Busca binária é como procurar uma palavra no dicionário
    abrindo sempre no meio e decidindo se vai para a metade anterior
    ou posterior, eliminando metade das possibilidades a cada passo.
    """
    print("=== CONCEITO DE BUSCA BINÁRIA ===")
    print()
    
    print("1. DEFINIÇÃO:")
    print("   A busca binária é um algoritmo eficiente para encontrar")
    print("   um elemento em uma lista ORDENADA, usando a estratégia")
    print("   'divide e conquista' para eliminar metade das possibilidades")
    print("   a cada comparação.")
    print()
    
    print("2. CARACTERÍSTICAS:")
    print("   ✅ Eficiência: O(log n) - muito rápido para grandes datasets")
    print("   ✅ Escalabilidade: Performance cresce logaritmicamente")
    print("   ✅ Previsibilidade: Número máximo de passos conhecido")
    print("   ❌ Pré-requisito: Requer dados ordenados")
    print("   ❌ Complexidade: Mais difícil de implementar que busca linear")
    print()
    
    print("3. ALGORITMO BÁSICO:")
    print("   1. Definir início (0) e fim (tamanho-1) da busca")
    print("   2. Calcular meio = (início + fim) // 2")
    print("   3. Comparar elemento do meio com valor procurado:")
    print("      - Se igual: encontrou, retornar posição")
    print("      - Se menor: buscar na metade direita (início = meio + 1)")
    print("      - Se maior: buscar na metade esquerda (fim = meio - 1)")
    print("   4. Repetir até encontrar ou início > fim")
    print()
    
    print("4. VISUALIZAÇÃO DO CONCEITO:")
    
    def visualizar_busca_binaria(lista, item):
        """
        Visualiza o processo de busca binária passo a passo.
        """
        print(f"   Buscando {item} em {lista}")
        print("   " + "─" * 60)
        
        inicio, fim = 0, len(lista) - 1
        passo = 1
        
        while inicio <= fim:
            meio = (inicio + fim) // 2
            elemento_meio = lista[meio]
            
            # Visualização da faixa atual
            print(f"   Passo {passo}:")
            print(f"   Faixa: índices {inicio} a {fim}")
            
            # Mostra a lista com marcações
            linha = "   ["
            for i, num in enumerate(lista):
                if i == meio:
                    linha += f" {num}* "  # Elemento do meio
                elif inicio <= i <= fim:
                    linha += f" {num}  "  # Na faixa atual
                else:
                    linha += f"({num}) "  # Fora da faixa
            linha += "]"
            print(linha)
            
            print(f"   Meio: índice {meio}, valor {elemento_meio}")
            
            if elemento_meio == item:
                print(f"   ✓ ENCONTRADO na posição {meio}!")
                return meio
            elif elemento_meio < item:
                print(f"   {elemento_meio} < {item} → Buscar na metade direita")
                inicio = meio + 1
            else:
                print(f"   {elemento_meio} > {item} → Buscar na metade esquerda")
                fim = meio - 1
            
            print("   " + "─" * 60)
            passo += 1
        
        print("   ✗ NÃO ENCONTRADO")
        return -1
    
    # Exemplo prático
    lista_ordenada = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    item_procurado = 13
    
    resultado = visualizar_busca_binaria(lista_ordenada, item_procurado)
    print()
    
    print("5. COMPARAÇÃO COM BUSCA LINEAR:")
    
    def contar_operacoes_linear(lista, item):
        """Conta operações na busca linear"""
        for i, elemento in enumerate(lista):
            if elemento == item:
                return i + 1  # +1 porque começamos do 0
        return len(lista)
    
    def contar_operacoes_binaria(lista, item):
        """Conta operações na busca binária"""
        inicio, fim = 0, len(lista) - 1
        operacoes = 0
        
        while inicio <= fim:
            operacoes += 1
            meio = (inicio + fim) // 2
            
            if lista[meio] == item:
                return operacoes
            elif lista[meio] < item:
                inicio = meio + 1
            else:
                fim = meio - 1
        
        return operacoes
    
    # Teste com diferentes tamanhos
    tamanhos = [10, 100, 1000, 10000]
    
    print("   Comparação de operações necessárias:")
    print("   ┌──────────┬─────────────┬─────────────┬─────────────┐")
    print("   │ TAMANHO  │   LINEAR    │   BINÁRIA   │   SPEEDUP   │")
    print("   ├──────────┼─────────────┼─────────────┼─────────────┤")
    
    for tamanho in tamanhos:
        lista_teste = list(range(0, tamanho * 2, 2))  # Lista ordenada
        item_teste = lista_teste[-1]  # Pior caso - último elemento
        
        ops_linear = contar_operacoes_linear(lista_teste, item_teste)
        ops_binaria = contar_operacoes_binaria(lista_teste, item_teste)
        speedup = ops_linear / ops_binaria
        
        print(f"   │ {tamanho:8} │ {ops_linear:11} │ {ops_binaria:11} │ {speedup:10.1f}x │")
    
    print("   └──────────┴─────────────┴─────────────┴─────────────┘")
    print()
    
    print("6. ANÁLISE MATEMÁTICA:")
    print("   Para uma lista de tamanho n:")
    print(f"   → Busca Linear: até {tamanhos[-1]} operações")
    print(f"   → Busca Binária: até {math.ceil(math.log2(tamanhos[-1]))} operações")
    print(f"   → log₂({tamanhos[-1]}) = {math.log2(tamanhos[-1]):.2f}")
    print()
    print("   Crescimento da complexidade:")
    for n in [100, 1000, 10000, 100000, 1000000]:
        linear = n
        binaria = math.ceil(math.log2(n))
        print(f"   n = {n:7}: Linear = {linear:7}, Binária = {binaria:2}")
    print()

def implementacao_iterativa():
    """
    Implementa busca binária de forma iterativa.
    """
    print("=== IMPLEMENTAÇÃO ITERATIVA ===")
    print()
    
    print("1. VERSÃO BÁSICA:")
    
    def busca_binaria_iterativa(lista, item):
        """
        Implementação iterativa clássica da busca binária.
        
        Args:
            lista: Lista ordenada onde buscar
            item: Item a ser encontrado
            
        Returns:
            int: Índice do item ou -1 se não encontrado
        """
        inicio = 0
        fim = len(lista) - 1
        
        while inicio <= fim:
            meio = (inicio + fim) // 2
            elemento_meio = lista[meio]
            
            if elemento_meio == item:
                return meio
            elif elemento_meio < item:
                inicio = meio + 1
            else:
                fim = meio - 1
        
        return -1
    
    # Teste básico
    numeros = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
    
    testes = [1, 13, 25, 12, 0, 30]
    
    print(f"   Lista: {numeros}")
    print("   Testes:")
    
    for item in testes:
        resultado = busca_binaria_iterativa(numeros, item)
        status = f"✓ índice {resultado}" if resultado != -1 else "✗ não encontrado"
        print(f"   → Buscar {item:2}: {status}")
    print()
    
    print("2. VERSÃO COM DETALHAMENTO:")
    
    def busca_binaria_detalhada(lista, item):
        """
        Versão que retorna informações detalhadas sobre a busca.
        
        Returns:
            dict: Informações sobre a busca realizada
        """
        inicio = 0
        fim = len(lista) - 1
        iteracoes = 0
        historico = []
        
        while inicio <= fim:
            iteracoes += 1
            meio = (inicio + fim) // 2
            elemento_meio = lista[meio]
            
            # Registra o passo atual
            passo = {
                'iteracao': iteracoes,
                'inicio': inicio,
                'fim': fim,
                'meio': meio,
                'elemento_meio': elemento_meio,
                'comparacao': None,
                'acao': None
            }
            
            if elemento_meio == item:
                passo['comparacao'] = f"{elemento_meio} == {item}"
                passo['acao'] = "ENCONTRADO"
                historico.append(passo)
                
                return {
                    'encontrado': True,
                    'posicao': meio,
                    'iteracoes': iteracoes,
                    'historico': historico
                }
            elif elemento_meio < item:
                passo['comparacao'] = f"{elemento_meio} < {item}"
                passo['acao'] = "Buscar à direita"
                inicio = meio + 1
            else:
                passo['comparacao'] = f"{elemento_meio} > {item}"
                passo['acao'] = "Buscar à esquerda"
                fim = meio - 1
            
            historico.append(passo)
        
        return {
            'encontrado': False,
            'posicao': -1,
            'iteracoes': iteracoes,
            'historico': historico
        }
    
    # Demonstração detalhada
    resultado_detalhado = busca_binaria_detalhada(numeros, 7)
    
    print(f"   Busca detalhada por 7:")
    print(f"   Encontrado: {resultado_detalhado['encontrado']}")
    print(f"   Posição: {resultado_detalhado['posicao']}")
    print(f"   Iterações: {resultado_detalhado['iteracoes']}")
    print()
    print("   Histórico:")
    
    for passo in resultado_detalhado['historico']:
        print(f"   {passo['iteracao']}. Faixa [{passo['inicio']}:{passo['fim']}] "
              f"→ meio={passo['meio']} ({passo['elemento_meio']}) "
              f"→ {passo['comparacao']} → {passo['acao']}")
    print()
    
    print("3. VERSÃO OTIMIZADA:")
    
    def busca_binaria_otimizada(lista, item):
        """
        Versão otimizada que evita overflow em listas muito grandes.
        Usa meio = inicio + (fim - inicio) // 2 em vez de (inicio + fim) // 2
        """
        inicio = 0
        fim = len(lista) - 1
        
        while inicio <= fim:
            # Evita overflow: meio = inicio + (fim - inicio) // 2
            meio = inicio + (fim - inicio) // 2
            elemento_meio = lista[meio]
            
            if elemento_meio == item:
                return meio
            elif elemento_meio < item:
                inicio = meio + 1
            else:
                fim = meio - 1
        
        return -1
    
    print("   Diferença na fórmula do meio:")
    print("   → Versão básica: meio = (inicio + fim) // 2")
    print("   → Versão otimizada: meio = inicio + (fim - inicio) // 2")
    print("   → Evita overflow quando inicio + fim > sys.maxsize")
    print()
    
    # Teste de equivalência
    for item in [5, 15, 30]:
        resultado_basico = busca_binaria_iterativa(numeros, item)
        resultado_otimizado = busca_binaria_otimizada(numeros, item)
        
        print(f"   Buscar {item}: básico={resultado_basico}, otimizado={resultado_otimizado} "
              f"{'✓' if resultado_basico == resultado_otimizado else '✗'}")
    print()

def implementacao_recursiva():
    """
    Implementa busca binária de forma recursiva.
    """
    print("=== IMPLEMENTAÇÃO RECURSIVA ===")
    print()
    
    print("1. VERSÃO BÁSICA:")
    
    def busca_binaria_recursiva(lista, item, inicio=0, fim=None):
        """
        Implementação recursiva da busca binária.
        
        Args:
            lista: Lista ordenada onde buscar
            item: Item a ser encontrado
            inicio: Índice inicial da busca
            fim: Índice final da busca
            
        Returns:
            int: Índice do item ou -1 se não encontrado
        """
        if fim is None:
            fim = len(lista) - 1
        
        # Caso base: faixa inválida
        if inicio > fim:
            return -1
        
        meio = inicio + (fim - inicio) // 2
        elemento_meio = lista[meio]
        
        # Caso base: encontrou
        if elemento_meio == item:
            return meio
        
        # Chamadas recursivas
        if elemento_meio < item:
            return busca_binaria_recursiva(lista, item, meio + 1, fim)
        else:
            return busca_binaria_recursiva(lista, item, inicio, meio - 1)
    
    # Teste da versão recursiva
    numeros = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    
    print(f"   Lista: {numeros}")
    print("   Testes recursivos:")
    
    for item in [2, 10, 20, 5, 25]:
        resultado = busca_binaria_recursiva(numeros, item)
        status = f"✓ índice {resultado}" if resultado != -1 else "✗ não encontrado"
        print(f"   → Buscar {item:2}: {status}")
    print()
    
    print("2. VERSÃO COM RASTREAMENTO:")
    
    def busca_binaria_recursiva_trace(lista, item, inicio=0, fim=None, nivel=0):
        """
        Versão recursiva que mostra o trace das chamadas.
        """
        if fim is None:
            fim = len(lista) - 1
        
        indent = "  " * nivel
        print(f"{indent}Nível {nivel}: buscar {item} em [{inicio}:{fim}]")
        
        # Caso base: faixa inválida
        if inicio > fim:
            print(f"{indent}→ Faixa inválida, retornando -1")
            return -1
        
        meio = inicio + (fim - inicio) // 2
        elemento_meio = lista[meio]
        
        print(f"{indent}→ Meio: índice {meio}, valor {elemento_meio}")
        
        # Caso base: encontrou
        if elemento_meio == item:
            print(f"{indent}→ ✓ ENCONTRADO!")
            return meio
        
        # Chamadas recursivas
        if elemento_meio < item:
            print(f"{indent}→ {elemento_meio} < {item}, buscar à direita")
            return busca_binaria_recursiva_trace(lista, item, meio + 1, fim, nivel + 1)
        else:
            print(f"{indent}→ {elemento_meio} > {item}, buscar à esquerda")
            return busca_binaria_recursiva_trace(lista, item, inicio, meio - 1, nivel + 1)
    
    print("   Trace da busca recursiva por 14:")
    resultado_trace = busca_binaria_recursiva_trace(numeros, 14)
    print(f"   Resultado final: {resultado_trace}")
    print()
    
    print("3. ANÁLISE DE COMPLEXIDADE ESPACIAL:")
    
    def analisar_profundidade_recursao(tamanho_lista):
        """
        Calcula a profundidade máxima da recursão para uma lista de tamanho n.
        """
        return math.ceil(math.log2(tamanho_lista + 1))
    
    print("   Profundidade máxima da recursão:")
    print("   ┌─────────────┬─────────────────┬─────────────────┐")
    print("   │   TAMANHO   │   PROFUNDIDADE  │   MEMÓRIA STACK │")
    print("   ├─────────────┼─────────────────┼─────────────────┤")
    
    tamanhos = [10, 100, 1000, 10000, 100000]
    
    for tamanho in tamanhos:
        profundidade = analisar_profundidade_recursao(tamanho)
        memoria_aprox = profundidade * 64  # Aproximação em bytes por frame
        
        print(f"   │ {tamanho:11} │ {profundidade:15} │ {memoria_aprox:13} B │")
    
    print("   └─────────────┴─────────────────┴─────────────────┘")
    print()
    
    print("4. COMPARAÇÃO: ITERATIVA vs RECURSIVA:")
    
    # Teste de performance
    lista_grande = list(range(0, 100000, 2))  # 50.000 elementos
    item_teste = 99998  # Último elemento (pior caso)
    
    # Teste iterativo
    start = time.perf_counter()
    for _ in range(1000):
        resultado_iter = busca_binaria_iterativa(lista_grande, item_teste)
    tempo_iterativo = time.perf_counter() - start
    
    # Teste recursivo
    start = time.perf_counter()
    for _ in range(1000):
        resultado_rec = busca_binaria_recursiva(lista_grande, item_teste)
    tempo_recursivo = time.perf_counter() - start
    
    print(f"   Lista de 50.000 elementos (1000 execuções):")
    print(f"   → Iterativa: {tempo_iterativo:.6f}s")
    print(f"   → Recursiva: {tempo_recursivo:.6f}s")
    print(f"   → Diferença: {((tempo_recursivo - tempo_iterativo) / tempo_iterativo * 100):+.1f}%")
    print()
    
    print("   VANTAGENS E DESVANTAGENS:")
    print()
    print("   ITERATIVA:")
    print("   ✅ Menor uso de memória (O(1) espacial)")
    print("   ✅ Sem risco de stack overflow")
    print("   ✅ Geralmente mais rápida")
    print("   ❌ Código menos elegante")
    print()
    print("   RECURSIVA:")
    print("   ✅ Código mais elegante e intuitivo")
    print("   ✅ Mais próxima da definição matemática")
    print("   ✅ Mais fácil de entender o algoritmo")
    print("   ❌ Maior uso de memória (O(log n) espacial)")
    print("   ❌ Risco de stack overflow em listas muito grandes")
    print("   ❌ Overhead das chamadas de função")
    print()

def variacoes_avancadas():
    """
    Implementa variações avançadas da busca binária.
    """
    print("=== VARIAÇÕES AVANÇADAS ===")
    print()
    
    print("1. BUSCA DA PRIMEIRA OCORRÊNCIA:")
    print("   Para listas com elementos duplicados.")
    print()
    
    def busca_primeira_ocorrencia(lista, item):
        """
        Encontra a primeira ocorrência de um item em lista ordenada com duplicatas.
        """
        inicio = 0
        fim = len(lista) - 1
        resultado = -1
        
        while inicio <= fim:
            meio = inicio + (fim - inicio) // 2
            
            if lista[meio] == item:
                resultado = meio  # Guarda a posição encontrada
                fim = meio - 1    # Continua buscando à esquerda
            elif lista[meio] < item:
                inicio = meio + 1
            else:
                fim = meio - 1
        
        return resultado
    
    def busca_ultima_ocorrencia(lista, item):
        """
        Encontra a última ocorrência de um item em lista ordenada com duplicatas.
        """
        inicio = 0
        fim = len(lista) - 1
        resultado = -1
        
        while inicio <= fim:
            meio = inicio + (fim - inicio) // 2
            
            if lista[meio] == item:
                resultado = meio    # Guarda a posição encontrada
                inicio = meio + 1   # Continua buscando à direita
            elif lista[meio] < item:
                inicio = meio + 1
            else:
                fim = meio - 1
        
        return resultado
    
    # Teste com duplicatas
    lista_duplicatas = [1, 2, 2, 2, 3, 4, 4, 5, 5, 5, 5, 6, 7]
    item_duplicado = 5
    
    primeira = busca_primeira_ocorrencia(lista_duplicatas, item_duplicado)
    ultima = busca_ultima_ocorrencia(lista_duplicatas, item_duplicado)
    
    print(f"   Lista: {lista_duplicatas}")
    print(f"   Procurando: {item_duplicado}")
    print(f"   → Primeira ocorrência: índice {primeira}")
    print(f"   → Última ocorrência: índice {ultima}")
    print(f"   → Total de ocorrências: {ultima - primeira + 1 if primeira != -1 else 0}")
    print()
    
    print("2. BUSCA DE INTERVALO:")
    print("   Encontra todos os elementos em um intervalo [min, max].")
    print()
    
    def busca_intervalo(lista, valor_min, valor_max):
        """
        Encontra todos os elementos no intervalo [valor_min, valor_max].
        
        Returns:
            Tuple[int, int]: (índice_início, índice_fim) do intervalo
        """
        # Busca a primeira ocorrência >= valor_min
        inicio_intervalo = busca_limite_inferior(lista, valor_min)
        
        # Busca a última ocorrência <= valor_max
        fim_intervalo = busca_limite_superior(lista, valor_max)
        
        if inicio_intervalo == -1 or fim_intervalo == -1 or inicio_intervalo > fim_intervalo:
            return -1, -1
        
        return inicio_intervalo, fim_intervalo
    
    def busca_limite_inferior(lista, valor):
        """Encontra o primeiro índice onde lista[i] >= valor"""
        inicio = 0
        fim = len(lista) - 1
        resultado = -1
        
        while inicio <= fim:
            meio = inicio + (fim - inicio) // 2
            
            if lista[meio] >= valor:
                resultado = meio
                fim = meio - 1
            else:
                inicio = meio + 1
        
        return resultado
    
    def busca_limite_superior(lista, valor):
        """Encontra o último índice onde lista[i] <= valor"""
        inicio = 0
        fim = len(lista) - 1
        resultado = -1
        
        while inicio <= fim:
            meio = inicio + (fim - inicio) // 2
            
            if lista[meio] <= valor:
                resultado = meio
                inicio = meio + 1
            else:
                fim = meio - 1
        
        return resultado
    
    # Teste de intervalo
    numeros_intervalo = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
    
    intervalos_teste = [(5, 15), (10, 20), (0, 5), (25, 30)]
    
    print(f"   Lista: {numeros_intervalo}")
    print("   Buscas por intervalo:")
    
    for min_val, max_val in intervalos_teste:
        inicio_idx, fim_idx = busca_intervalo(numeros_intervalo, min_val, max_val)
        
        if inicio_idx != -1:
            elementos = numeros_intervalo[inicio_idx:fim_idx + 1]
            print(f"   → [{min_val}, {max_val}]: índices {inicio_idx}-{fim_idx} = {elementos}")
        else:
            print(f"   → [{min_val}, {max_val}]: nenhum elemento encontrado")
    print()
    
    print("3. BUSCA DO ELEMENTO MAIS PRÓXIMO:")
    print("   Encontra o elemento mais próximo quando o valor exato não existe.")
    print()
    
    def busca_mais_proximo(lista, valor):
        """
        Encontra o elemento mais próximo do valor procurado.
        
        Returns:
            Tuple[int, int]: (índice, elemento_mais_próximo)
        """
        if not lista:
            return -1, None
        
        inicio = 0
        fim = len(lista) - 1
        
        # Se valor está fora dos limites
        if valor <= lista[0]:
            return 0, lista[0]
        if valor >= lista[-1]:
            return len(lista) - 1, lista[-1]
        
        while inicio <= fim:
            meio = inicio + (fim - inicio) // 2
            
            if lista[meio] == valor:
                return meio, lista[meio]
            elif lista[meio] < valor:
                inicio = meio + 1
            else:
                fim = meio - 1
        
        # Neste ponto, fim < inicio
        # lista[fim] < valor < lista[inicio]
        
        # Compara distâncias
        if abs(lista[fim] - valor) <= abs(lista[inicio] - valor):
            return fim, lista[fim]
        else:
            return inicio, lista[inicio]
    
    # Teste de proximidade
    numeros_prox = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    valores_teste = [25, 35, 45, 5, 105, 50]
    
    print(f"   Lista: {numeros_prox}")
    print("   Busca por elementos mais próximos:")
    
    for valor in valores_teste:
        idx, elemento = busca_mais_proximo(numeros_prox, valor)
        distancia = abs(elemento - valor)
        print(f"   → Valor {valor}: mais próximo é {elemento} (índice {idx}, distância {distancia})")
    print()
    
    print("4. BUSCA EM LISTA ROTACIONADA:")
    print("   Busca em lista ordenada que foi rotacionada.")
    print()
    
    def busca_em_lista_rotacionada(lista, item):
        """
        Busca em lista ordenada rotacionada.
        Ex: [4, 5, 6, 7, 0, 1, 2] é uma rotação de [0, 1, 2, 4, 5, 6, 7]
        """
        inicio = 0
        fim = len(lista) - 1
        
        while inicio <= fim:
            meio = inicio + (fim - inicio) // 2
            
            if lista[meio] == item:
                return meio
            
            # Determina qual metade está ordenada
            if lista[inicio] <= lista[meio]:  # Metade esquerda ordenada
                if lista[inicio] <= item < lista[meio]:
                    fim = meio - 1
                else:
                    inicio = meio + 1
            else:  # Metade direita ordenada
                if lista[meio] < item <= lista[fim]:
                    inicio = meio + 1
                else:
                    fim = meio - 1
        
        return -1
    
    # Teste com lista rotacionada
    lista_rotacionada = [4, 5, 6, 7, 0, 1, 2]
    
    print(f"   Lista rotacionada: {lista_rotacionada}")
    print("   (Rotação de [0, 1, 2, 4, 5, 6, 7])")
    print("   Testes:")
    
    for item in [0, 4, 6, 3]:
        resultado = busca_em_lista_rotacionada(lista_rotacionada, item)
        status = f"✓ índice {resultado}" if resultado != -1 else "✗ não encontrado"
        print(f"   → Buscar {item}: {status}")
    print()

def aplicacoes_praticas():
    """
    Demonstra aplicações práticas da busca binária.
    """
    print("=== APLICAÇÕES PRÁTICAS ===")
    print()
    
    print("1. SISTEMA DE BUSCA EM CATÁLOGO:")
    print("   Busca eficiente em catálogo de produtos ordenado por preço.")
    print()
    
    class CatalogoProdutos:
        """Sistema de catálogo com busca binária por preço"""
        
        def __init__(self):
            self.produtos = []  # Lista ordenada por preço
        
        def adicionar_produto(self, nome, preco, categoria):
            """Adiciona produto mantendo ordem por preço"""
            produto = {'nome': nome, 'preco': preco, 'categoria': categoria}
            
            # Busca posição para inserção
            posicao = self._buscar_posicao_insercao(preco)
            self.produtos.insert(posicao, produto)
        
        def _buscar_posicao_insercao(self, preco):
            """Encontra posição para inserir mantendo ordem"""
            inicio = 0
            fim = len(self.produtos) - 1
            
            while inicio <= fim:
                meio = inicio + (fim - inicio) // 2
                
                if self.produtos[meio]['preco'] < preco:
                    inicio = meio + 1
                else:
                    fim = meio - 1
            
            return inicio
        
        def buscar_por_preco_exato(self, preco):
            """Busca produtos com preço exato"""
            resultados = []
            
            # Encontra primeira ocorrência
            primeira = self._buscar_primeira_ocorrencia_preco(preco)
            
            if primeira != -1:
                # Coleta todas as ocorrências
                i = primeira
                while i < len(self.produtos) and self.produtos[i]['preco'] == preco:
                    resultados.append(self.produtos[i])
                    i += 1
            
            return resultados
        
        def buscar_por_faixa_preco(self, preco_min, preco_max):
            """Busca produtos em faixa de preço"""
            inicio_idx = self._buscar_limite_inferior_preco(preco_min)
            fim_idx = self._buscar_limite_superior_preco(preco_max)
            
            if inicio_idx == -1 or fim_idx == -1:
                return []
            
            return self.produtos[inicio_idx:fim_idx + 1]
        
        def _buscar_primeira_ocorrencia_preco(self, preco):
            """Busca primeira ocorrência de um preço"""
            inicio = 0
            fim = len(self.produtos) - 1
            resultado = -1
            
            while inicio <= fim:
                meio = inicio + (fim - inicio) // 2
                
                if self.produtos[meio]['preco'] == preco:
                    resultado = meio
                    fim = meio - 1
                elif self.produtos[meio]['preco'] < preco:
                    inicio = meio + 1
                else:
                    fim = meio - 1
            
            return resultado
        
        def _buscar_limite_inferior_preco(self, preco):
            """Busca primeiro produto com preço >= valor"""
            inicio = 0
            fim = len(self.produtos) - 1
            resultado = -1
            
            while inicio <= fim:
                meio = inicio + (fim - inicio) // 2
                
                if self.produtos[meio]['preco'] >= preco:
                    resultado = meio
                    fim = meio - 1
                else:
                    inicio = meio + 1
            
            return resultado
        
        def _buscar_limite_superior_preco(self, preco):
            """Busca último produto com preço <= valor"""
            inicio = 0
            fim = len(self.produtos) - 1
            resultado = -1
            
            while inicio <= fim:
                meio = inicio + (fim - inicio) // 2
                
                if self.produtos[meio]['preco'] <= preco:
                    resultado = meio
                    inicio = meio + 1
                else:
                    fim = meio - 1
            
            return resultado
    
    # Demonstração do catálogo
    catalogo = CatalogoProdutos()
    
    # Adicionando produtos
    produtos_exemplo = [
        ("Notebook Dell", 2500, "Eletrônicos"),
        ("Mouse Logitech", 50, "Eletrônicos"),
        ("Teclado Mecânico", 200, "Eletrônicos"),
        ("Monitor 24\"", 800, "Eletrônicos"),
        ("Cadeira Gamer", 600, "Móveis"),
        ("Mesa de Escritório", 400, "Móveis"),
        ("Smartphone", 1200, "Eletrônicos"),
        ("Tablet", 800, "Eletrônicos")
    ]
    
    for nome, preco, categoria in produtos_exemplo:
        catalogo.adicionar_produto(nome, preco, categoria)
    
    print(f"   Catálogo com {len(catalogo.produtos)} produtos (ordenado por preço):")
    for i, produto in enumerate(catalogo.produtos):
        print(f"   {i+1:2}. {produto['nome']:20} - R$ {produto['preco']:4} ({produto['categoria']})")
    print()
    
    # Testes de busca
    print("   Buscas no catálogo:")
    
    # Busca por preço exato
    produtos_800 = catalogo.buscar_por_preco_exato(800)
    print(f"   → Produtos de R$ 800: {len(produtos_800)} encontrados")
    for produto in produtos_800:
        print(f"     • {produto['nome']}")
    
    # Busca por faixa
    produtos_faixa = catalogo.buscar_por_faixa_preco(200, 800)
    print(f"   → Produtos entre R$ 200-800: {len(produtos_faixa)} encontrados")
    for produto in produtos_faixa:
        print(f"     • {produto['nome']} - R$ {produto['preco']}")
    print()
    
    print("2. SISTEMA DE VERSIONAMENTO:")
    print("   Busca de versões em sistema de controle de versão.")
    print()
    
    class SistemaVersoes:
        """Sistema que gerencia versões usando busca binária"""
        
        def __init__(self):
            self.versoes = []  # Lista ordenada de versões
        
        def adicionar_versao(self, numero_versao, timestamp, descricao):
            """Adiciona versão mantendo ordem cronológica"""
            versao = {
                'numero': numero_versao,
                'timestamp': timestamp,
                'descricao': descricao
            }
            
            # Busca posição para inserção
            posicao = self._buscar_posicao_insercao_timestamp(timestamp)
            self.versoes.insert(posicao, versao)
        
        def _buscar_posicao_insercao_timestamp(self, timestamp):
            """Encontra posição para inserir mantendo ordem cronológica"""
            inicio = 0
            fim = len(self.versoes) - 1
            
            while inicio <= fim:
                meio = inicio + (fim - inicio) // 2
                
                if self.versoes[meio]['timestamp'] < timestamp:
                    inicio = meio + 1
                else:
                    fim = meio - 1
            
            return inicio
        
        def buscar_versao_por_timestamp(self, timestamp):
            """Busca versão mais próxima de um timestamp"""
            if not self.versoes:
                return None
            
            inicio = 0
            fim = len(self.versoes) - 1
            
            # Busca binária por timestamp mais próximo
            while inicio <= fim:
                meio = inicio + (fim - inicio) // 2
                
                if self.versoes[meio]['timestamp'] == timestamp:
                    return self.versoes[meio]
                elif self.versoes[meio]['timestamp'] < timestamp:
                    inicio = meio + 1
                else:
                    fim = meio - 1
            
            # Retorna a versão mais próxima
            if fim >= 0 and inicio < len(self.versoes):
                if abs(self.versoes[fim]['timestamp'] - timestamp) <= abs(self.versoes[inicio]['timestamp'] - timestamp):
                    return self.versoes[fim]
                else:
                    return self.versoes[inicio]
            elif fim >= 0:
                return self.versoes[fim]
            else:
                return self.versoes[inicio]
        
        def buscar_versoes_periodo(self, timestamp_inicio, timestamp_fim):
            """Busca todas as versões em um período"""
            inicio_idx = self._buscar_limite_inferior_timestamp(timestamp_inicio)
            fim_idx = self._buscar_limite_superior_timestamp(timestamp_fim)
            
            if inicio_idx == -1 or fim_idx == -1:
                return []
            
            return self.versoes[inicio_idx:fim_idx + 1]
        
        def _buscar_limite_inferior_timestamp(self, timestamp):
            """Busca primeira versão com timestamp >= valor"""
            inicio = 0
            fim = len(self.versoes) - 1
            resultado = -1
            
            while inicio <= fim:
                meio = inicio + (fim - inicio) // 2
                
                if self.versoes[meio]['timestamp'] >= timestamp:
                    resultado = meio
                    fim = meio - 1
                else:
                    inicio = meio + 1
            
            return resultado
        
        def _buscar_limite_superior_timestamp(self, timestamp):
            """Busca última versão com timestamp <= valor"""
            inicio = 0
            fim = len(self.versoes) - 1
            resultado = -1
            
            while inicio <= fim:
                meio = inicio + (fim - inicio) // 2
                
                if self.versoes[meio]['timestamp'] <= timestamp:
                    resultado = meio
                    inicio = meio + 1
                else:
                    fim = meio - 1
            
            return resultado
    
    # Demonstração do sistema de versões
    sistema = SistemaVersoes()
    
    # Adicionando versões
    versoes_exemplo = [
        ("v1.0.0", 1000, "Versão inicial"),
        ("v1.1.0", 1100, "Correções de bugs"),
        ("v1.2.0", 1200, "Novas funcionalidades"),
        ("v2.0.0", 1300, "Refatoração completa"),
        ("v2.1.0", 1400, "Melhorias de performance"),
        ("v2.2.0", 1500, "Interface atualizada")
    ]
    
    for numero, timestamp, descricao in versoes_exemplo:
        sistema.adicionar_versao(numero, timestamp, descricao)
    
    print(f"   Sistema com {len(sistema.versoes)} versões:")
    for versao in sistema.versoes:
        print(f"   → {versao['numero']} (t={versao['timestamp']}): {versao['descricao']}")
    print()
    
    # Testes de busca
    print("   Buscas no sistema de versões:")
    
    # Busca por timestamp específico
    versao_1250 = sistema.buscar_versao_por_timestamp(1250)
    print(f"   → Versão mais próxima de t=1250: {versao_1250['numero']} (t={versao_1250['timestamp']})")
    
    # Busca por período
    versoes_periodo = sistema.buscar_versoes_periodo(1150, 1350)
    print(f"   → Versões entre t=1150-1350: {len(versoes_periodo)} encontradas")
    for versao in versoes_periodo:
        print(f"     • {versao['numero']} (t={versao['timestamp']})")
    print()

if __name__ == "__main__":
    print("MÓDULO 3.3 - ALGORITMOS DE BUSCA BINÁRIA")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceito_busca_binaria()
    print("\n" + "="*50 + "\n")
    
    implementacao_iterativa()
    print("\n" + "="*50 + "\n")
    
    implementacao_recursiva()
    print("\n" + "="*50 + "\n")
    
    variacoes_avancadas()
    print("\n" + "="*50 + "\n")
    
    aplicacoes_praticas()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 3.3 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceito e implementação de busca binária")
    print("✅ Análise de complexidade O(log n)")
    print("✅ Implementações iterativa e recursiva")
    print("✅ Comparação de performance e uso de memória")
    print("✅ Variações avançadas (primeira/última ocorrência)")
    print("✅ Busca em intervalos e elementos mais próximos")
    print("✅ Aplicações práticas (catálogos, versionamento)")
    print("✅ Pré-requisitos e limitações do algoritmo")
    print("\n➡️  Próximo: Módulo 3.4 - Algoritmos de Ordenação Básicos")