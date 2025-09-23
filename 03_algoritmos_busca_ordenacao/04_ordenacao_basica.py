"""
Módulo: Algoritmos de Ordenação Básicos
Tópico: Algoritmos de Busca e Ordenação - Bubble, Selection e Insertion Sort
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico a Intermediário

Objetivos de Aprendizado:
- Compreender conceitos fundamentais de ordenação
- Implementar algoritmos básicos de ordenação
- Analisar complexidade temporal e espacial
- Comparar performance entre algoritmos
- Visualizar processo de ordenação
- Identificar casos de uso apropriados
- Desenvolver intuição sobre estabilidade
- Aplicar otimizações práticas

Conceitos Abordados:
- Bubble Sort (ordenação por bolha)
- Selection Sort (ordenação por seleção)
- Insertion Sort (ordenação por inserção)
- Análise de complexidade O(n²)
- Estabilidade de algoritmos
- Otimizações práticas
- Comparação de performance
- Casos de uso específicos

Pré-requisitos:
- Módulos 3.1, 3.2 e 3.3 completos
- Compreensão de loops aninhados
- Conhecimento de complexidade quadrática
- Familiaridade com comparações

Complexidade:
- Temporal: O(n²) para todos os algoritmos básicos
- Espacial: O(1) - ordenação in-place
- Melhor caso varia por algoritmo
- Pior caso: O(n²) para todos
"""

import time
import random
import copy
from typing import List, Tuple, Callable

def conceitos_fundamentais():
    """
    Introduz conceitos fundamentais de ordenação.
    """
    print("=== CONCEITOS FUNDAMENTAIS DE ORDENAÇÃO ===")
    print()
    
    print("1. DEFINIÇÃO DE ORDENAÇÃO:")
    print("   Ordenação é o processo de reorganizar elementos de uma")
    print("   coleção em uma ordem específica (crescente ou decrescente)")
    print("   baseada em um critério de comparação.")
    print()
    
    print("2. CARACTERÍSTICAS IMPORTANTES:")
    print()
    
    print("   ESTABILIDADE:")
    print("   → Estável: Mantém ordem relativa de elementos iguais")
    print("   → Instável: Pode alterar ordem relativa de elementos iguais")
    print()
    
    # Demonstração de estabilidade
    def demonstrar_estabilidade():
        """Demonstra conceito de estabilidade"""
        # Lista com elementos iguais mas com identificadores
        pessoas = [
            ("Ana", 25, "A"),
            ("Bruno", 30, "B"), 
            ("Carlos", 25, "C"),
            ("Diana", 25, "D")
        ]
        
        print("   Exemplo com pessoas (nome, idade, id):")
        print(f"   Original: {[(p[0], p[1], p[2]) for p in pessoas]}")
        
        # Ordenação estável por idade (mantém ordem original para idades iguais)
        estavel = sorted(pessoas, key=lambda x: x[1])
        print(f"   Estável:  {[(p[0], p[1], p[2]) for p in estavel]}")
        print("   → Pessoas com 25 anos mantiveram ordem: Ana(A), Carlos(C), Diana(D)")
        print()
    
    demonstrar_estabilidade()
    
    print("   ORDENAÇÃO IN-PLACE:")
    print("   → In-place: Usa apenas O(1) espaço extra")
    print("   → Out-of-place: Usa O(n) espaço extra")
    print()
    
    print("   ADAPTABILIDADE:")
    print("   → Adaptativo: Performance melhora com dados parcialmente ordenados")
    print("   → Não-adaptativo: Performance constante independente da entrada")
    print()
    
    print("3. CLASSIFICAÇÃO DOS ALGORITMOS BÁSICOS:")
    print()
    
    algoritmos_info = [
        ("Bubble Sort", "O(n²)", "O(1)", "Estável", "Adaptativo"),
        ("Selection Sort", "O(n²)", "O(1)", "Instável", "Não-adaptativo"),
        ("Insertion Sort", "O(n²)", "O(1)", "Estável", "Adaptativo")
    ]
    
    print("   ┌─────────────────┬──────────┬──────────┬────────────┬──────────────┐")
    print("   │   ALGORITMO     │   TEMPO  │  ESPAÇO  │ ESTABILID. │ ADAPTABILID. │")
    print("   ├─────────────────┼──────────┼──────────┼────────────┼──────────────┤")
    
    for nome, tempo, espaco, estabilidade, adaptabilidade in algoritmos_info:
        print(f"   │ {nome:15} │ {tempo:8} │ {espaco:8} │ {estabilidade:10} │ {adaptabilidade:12} │")
    
    print("   └─────────────────┴──────────┴──────────┴────────────┴──────────────┘")
    print()
    
    print("4. QUANDO USAR ALGORITMOS BÁSICOS:")
    print()
    
    casos_uso = [
        "✅ Listas pequenas (< 50 elementos)",
        "✅ Dados quase ordenados (Insertion Sort)",
        "✅ Implementação simples necessária",
        "✅ Restrições de memória severas",
        "✅ Fins educacionais",
        "✅ Estabilidade é crucial",
        "❌ Listas grandes (> 1000 elementos)",
        "❌ Performance crítica",
        "❌ Dados completamente aleatórios"
    ]
    
    for caso in casos_uso:
        print(f"   {caso}")
    print()

def bubble_sort_implementacao():
    """
    Implementa e analisa o algoritmo Bubble Sort.
    """
    print("=== BUBBLE SORT (ORDENAÇÃO POR BOLHA) ===")
    print()
    
    print("1. CONCEITO:")
    print("   O Bubble Sort compara elementos adjacentes e os troca")
    print("   se estiverem na ordem errada. Os maiores elementos")
    print("   'borbulham' para o final da lista como bolhas de ar.")
    print()
    
    print("2. ALGORITMO:")
    print("   1. Percorrer a lista comparando pares adjacentes")
    print("   2. Trocar se estiverem na ordem errada")
    print("   3. Repetir até nenhuma troca ser necessária")
    print("   4. A cada passada, o maior elemento vai para o final")
    print()
    
    print("3. IMPLEMENTAÇÃO BÁSICA:")
    
    def bubble_sort_basico(lista):
        """
        Implementação básica do Bubble Sort.
        
        Args:
            lista: Lista a ser ordenada
            
        Returns:
            List: Lista ordenada
        """
        n = len(lista)
        lista_copia = lista.copy()
        
        # Percorre toda a lista
        for i in range(n):
            # Últimos i elementos já estão ordenados
            for j in range(0, n - i - 1):
                # Compara elementos adjacentes
                if lista_copia[j] > lista_copia[j + 1]:
                    # Troca se estiverem na ordem errada
                    lista_copia[j], lista_copia[j + 1] = lista_copia[j + 1], lista_copia[j]
        
        return lista_copia
    
    # Demonstração básica
    numeros = [64, 34, 25, 12, 22, 11, 90]
    print(f"   Lista original: {numeros}")
    
    resultado = bubble_sort_basico(numeros)
    print(f"   Lista ordenada: {resultado}")
    print()
    
    print("4. VISUALIZAÇÃO PASSO A PASSO:")
    
    def bubble_sort_visualizado(lista):
        """
        Bubble Sort com visualização do processo.
        """
        n = len(lista)
        lista_copia = lista.copy()
        
        print(f"   Ordenando: {lista_copia}")
        print("   " + "─" * 50)
        
        for i in range(n):
            print(f"   Passada {i + 1}:")
            trocas_feitas = False
            
            for j in range(0, n - i - 1):
                # Mostra comparação atual
                print(f"   → Comparar {lista_copia[j]} e {lista_copia[j + 1]}: ", end="")
                
                if lista_copia[j] > lista_copia[j + 1]:
                    # Faz a troca
                    lista_copia[j], lista_copia[j + 1] = lista_copia[j + 1], lista_copia[j]
                    print(f"trocar → {lista_copia}")
                    trocas_feitas = True
                else:
                    print(f"manter → {lista_copia}")
            
            if not trocas_feitas:
                print("   → Nenhuma troca necessária, lista ordenada!")
                break
            
            print(f"   Resultado da passada: {lista_copia}")
            print("   " + "─" * 50)
        
        return lista_copia
    
    # Exemplo visual
    numeros_pequenos = [5, 2, 8, 1, 9]
    bubble_sort_visualizado(numeros_pequenos)
    print()
    
    print("5. VERSÃO OTIMIZADA:")
    
    def bubble_sort_otimizado(lista):
        """
        Versão otimizada que para quando não há mais trocas.
        """
        n = len(lista)
        lista_copia = lista.copy()
        
        for i in range(n):
            trocas_feitas = False
            
            # Últimos i elementos já estão no lugar certo
            for j in range(0, n - i - 1):
                if lista_copia[j] > lista_copia[j + 1]:
                    lista_copia[j], lista_copia[j + 1] = lista_copia[j + 1], lista_copia[j]
                    trocas_feitas = True
            
            # Se não houve trocas, a lista está ordenada
            if not trocas_feitas:
                break
        
        return lista_copia
    
    def bubble_sort_com_contador(lista):
        """Versão que conta operações realizadas"""
        n = len(lista)
        lista_copia = lista.copy()
        comparacoes = 0
        trocas = 0
        passadas = 0
        
        for i in range(n):
            passadas += 1
            trocas_na_passada = False
            
            for j in range(0, n - i - 1):
                comparacoes += 1
                if lista_copia[j] > lista_copia[j + 1]:
                    lista_copia[j], lista_copia[j + 1] = lista_copia[j + 1], lista_copia[j]
                    trocas += 1
                    trocas_na_passada = True
            
            if not trocas_na_passada:
                break
        
        return lista_copia, comparacoes, trocas, passadas
    
    # Teste com diferentes cenários
    cenarios = [
        ("Aleatório", [3, 7, 1, 9, 4]),
        ("Ordenado", [1, 3, 4, 7, 9]),
        ("Reverso", [9, 7, 4, 3, 1])
    ]
    
    print("   Análise de performance:")
    print("   ┌─────────────┬─────────────┬─────────┬──────────┐")
    print("   │   CENÁRIO   │ COMPARAÇÕES │ TROCAS  │ PASSADAS │")
    print("   ├─────────────┼─────────────┼─────────┼──────────┤")
    
    for nome, lista_teste in cenarios:
        _, comp, trocas_count, passadas = bubble_sort_com_contador(lista_teste)
        print(f"   │ {nome:11} │ {comp:11} │ {trocas_count:7} │ {passadas:8} │")
    
    print("   └─────────────┴─────────────┴─────────┴──────────┘")
    print()

def selection_sort_implementacao():
    """
    Implementa e analisa o algoritmo Selection Sort.
    """
    print("=== SELECTION SORT (ORDENAÇÃO POR SELEÇÃO) ===")
    print()
    
    print("1. CONCEITO:")
    print("   O Selection Sort encontra o menor elemento da lista")
    print("   e o coloca na primeira posição, depois encontra o")
    print("   segundo menor e o coloca na segunda posição, e assim")
    print("   por diante até ordenar toda a lista.")
    print()
    
    print("2. ALGORITMO:")
    print("   1. Encontrar o menor elemento da lista")
    print("   2. Trocar com o primeiro elemento")
    print("   3. Encontrar o menor elemento do restante da lista")
    print("   4. Trocar com o segundo elemento")
    print("   5. Repetir até ordenar toda a lista")
    print()
    
    print("3. IMPLEMENTAÇÃO BÁSICA:")
    
    def selection_sort_basico(lista):
        """
        Implementação básica do Selection Sort.
        
        Args:
            lista: Lista a ser ordenada
            
        Returns:
            List: Lista ordenada
        """
        n = len(lista)
        lista_copia = lista.copy()
        
        # Percorre toda a lista
        for i in range(n):
            # Encontra o índice do menor elemento no restante
            min_idx = i
            
            for j in range(i + 1, n):
                if lista_copia[j] < lista_copia[min_idx]:
                    min_idx = j
            
            # Troca o menor elemento encontrado com o primeiro elemento
            lista_copia[i], lista_copia[min_idx] = lista_copia[min_idx], lista_copia[i]
        
        return lista_copia
    
    # Demonstração básica
    numeros = [64, 25, 12, 22, 11]
    print(f"   Lista original: {numeros}")
    
    resultado = selection_sort_basico(numeros)
    print(f"   Lista ordenada: {resultado}")
    print()
    
    print("4. VISUALIZAÇÃO PASSO A PASSO:")
    
    def selection_sort_visualizado(lista):
        """
        Selection Sort com visualização do processo.
        """
        n = len(lista)
        lista_copia = lista.copy()
        
        print(f"   Ordenando: {lista_copia}")
        print("   " + "─" * 60)
        
        for i in range(n):
            print(f"   Passo {i + 1}: Procurar menor elemento a partir da posição {i}")
            
            # Encontra o menor elemento
            min_idx = i
            min_valor = lista_copia[i]
            
            print(f"   → Menor atual: {min_valor} (posição {i})")
            
            for j in range(i + 1, n):
                print(f"   → Comparar com {lista_copia[j]} (posição {j}): ", end="")
                
                if lista_copia[j] < lista_copia[min_idx]:
                    min_idx = j
                    min_valor = lista_copia[j]
                    print(f"novo menor!")
                else:
                    print("manter atual")
            
            # Faz a troca se necessário
            if min_idx != i:
                print(f"   → Trocar {lista_copia[i]} (pos {i}) com {lista_copia[min_idx]} (pos {min_idx})")
                lista_copia[i], lista_copia[min_idx] = lista_copia[min_idx], lista_copia[i]
            else:
                print(f"   → Elemento {lista_copia[i]} já está no lugar correto")
            
            print(f"   Estado atual: {lista_copia}")
            print("   " + "─" * 60)
        
        return lista_copia
    
    # Exemplo visual
    numeros_pequenos = [7, 2, 8, 1, 5]
    selection_sort_visualizado(numeros_pequenos)
    print()
    
    print("5. ANÁLISE DE PERFORMANCE:")
    
    def selection_sort_com_contador(lista):
        """Versão que conta operações realizadas"""
        n = len(lista)
        lista_copia = lista.copy()
        comparacoes = 0
        trocas = 0
        
        for i in range(n):
            min_idx = i
            
            # Conta comparações para encontrar o mínimo
            for j in range(i + 1, n):
                comparacoes += 1
                if lista_copia[j] < lista_copia[min_idx]:
                    min_idx = j
            
            # Conta trocas (sempre uma por iteração, exceto se já estiver no lugar)
            if min_idx != i:
                lista_copia[i], lista_copia[min_idx] = lista_copia[min_idx], lista_copia[i]
                trocas += 1
        
        return lista_copia, comparacoes, trocas
    
    # Teste com diferentes cenários
    cenarios = [
        ("Aleatório", [3, 7, 1, 9, 4]),
        ("Ordenado", [1, 3, 4, 7, 9]),
        ("Reverso", [9, 7, 4, 3, 1])
    ]
    
    print("   Análise de performance:")
    print("   ┌─────────────┬─────────────┬─────────┐")
    print("   │   CENÁRIO   │ COMPARAÇÕES │ TROCAS  │")
    print("   ├─────────────┼─────────────┼─────────┤")
    
    for nome, lista_teste in cenarios:
        _, comp, trocas_count = selection_sort_com_contador(lista_teste)
        print(f"   │ {nome:11} │ {comp:11} │ {trocas_count:7} │")
    
    print("   └─────────────┴─────────────┴─────────┘")
    print()
    
    print("6. CARACTERÍSTICAS DO SELECTION SORT:")
    print("   ✅ Sempre faz exatamente n-1 trocas")
    print("   ✅ Número de comparações é sempre O(n²)")
    print("   ✅ Performance consistente (não-adaptativo)")
    print("   ❌ Não é estável (pode alterar ordem de elementos iguais)")
    print("   ❌ Não aproveita dados parcialmente ordenados")
    print()

def insertion_sort_implementacao():
    """
    Implementa e analisa o algoritmo Insertion Sort.
    """
    print("=== INSERTION SORT (ORDENAÇÃO POR INSERÇÃO) ===")
    print()
    
    print("1. CONCEITO:")
    print("   O Insertion Sort constrói a lista ordenada um elemento")
    print("   por vez, inserindo cada novo elemento na posição correta")
    print("   dentro da parte já ordenada da lista.")
    print()
    print("   Analogia: Como ordenar cartas na mão - você pega uma")
    print("   carta por vez e a insere na posição correta entre as")
    print("   cartas já ordenadas.")
    print()
    
    print("2. ALGORITMO:")
    print("   1. Começar com o segundo elemento (primeiro já está 'ordenado')")
    print("   2. Comparar com elementos anteriores")
    print("   3. Mover elementos maiores uma posição à direita")
    print("   4. Inserir o elemento na posição correta")
    print("   5. Repetir para todos os elementos")
    print()
    
    print("3. IMPLEMENTAÇÃO BÁSICA:")
    
    def insertion_sort_basico(lista):
        """
        Implementação básica do Insertion Sort.
        
        Args:
            lista: Lista a ser ordenada
            
        Returns:
            List: Lista ordenada
        """
        lista_copia = lista.copy()
        
        # Percorre a partir do segundo elemento
        for i in range(1, len(lista_copia)):
            chave = lista_copia[i]  # Elemento a ser inserido
            j = i - 1  # Índice do último elemento da parte ordenada
            
            # Move elementos maiores que a chave uma posição à direita
            while j >= 0 and lista_copia[j] > chave:
                lista_copia[j + 1] = lista_copia[j]
                j -= 1
            
            # Insere a chave na posição correta
            lista_copia[j + 1] = chave
        
        return lista_copia
    
    # Demonstração básica
    numeros = [5, 2, 4, 6, 1, 3]
    print(f"   Lista original: {numeros}")
    
    resultado = insertion_sort_basico(numeros)
    print(f"   Lista ordenada: {resultado}")
    print()
    
    print("4. VISUALIZAÇÃO PASSO A PASSO:")
    
    def insertion_sort_visualizado(lista):
        """
        Insertion Sort com visualização do processo.
        """
        lista_copia = lista.copy()
        n = len(lista_copia)
        
        print(f"   Ordenando: {lista_copia}")
        print("   " + "─" * 70)
        
        for i in range(1, n):
            chave = lista_copia[i]
            j = i - 1
            
            print(f"   Passo {i}: Inserir {chave} na parte ordenada {lista_copia[:i]}")
            
            # Visualiza a busca da posição correta
            posicao_original = i
            movimentos = 0
            
            while j >= 0 and lista_copia[j] > chave:
                print(f"   → {lista_copia[j]} > {chave}, mover {lista_copia[j]} para direita")
                lista_copia[j + 1] = lista_copia[j]
                j -= 1
                movimentos += 1
                
                # Mostra estado intermediário
                temp_lista = lista_copia.copy()
                temp_lista[j + 1] = f"[{chave}]"  # Mostra onde a chave será inserida
                print(f"   Estado: {temp_lista}")
            
            # Insere a chave
            lista_copia[j + 1] = chave
            
            if movimentos == 0:
                print(f"   → {chave} já está na posição correta")
            else:
                print(f"   → Inserir {chave} na posição {j + 1}")
            
            print(f"   Resultado: {lista_copia}")
            print(f"   Parte ordenada: {lista_copia[:i+1]} | Parte não ordenada: {lista_copia[i+1:]}")
            print("   " + "─" * 70)
        
        return lista_copia
    
    # Exemplo visual
    numeros_pequenos = [4, 2, 7, 1, 5]
    insertion_sort_visualizado(numeros_pequenos)
    print()
    
    print("5. VERSÃO OTIMIZADA (BUSCA BINÁRIA):")
    
    def insertion_sort_busca_binaria(lista):
        """
        Versão otimizada que usa busca binária para encontrar posição de inserção.
        Reduz comparações de O(n) para O(log n), mas ainda precisa mover elementos.
        """
        def busca_posicao_insercao(arr, val, inicio, fim):
            """Encontra posição para inserir val mantendo ordem"""
            if inicio == fim:
                return inicio if arr[inicio] > val else inicio + 1
            
            if inicio > fim:
                return inicio
            
            meio = (inicio + fim) // 2
            
            if arr[meio] < val:
                return busca_posicao_insercao(arr, val, meio + 1, fim)
            elif arr[meio] > val:
                return busca_posicao_insercao(arr, val, inicio, meio - 1)
            else:
                return meio
        
        lista_copia = lista.copy()
        
        for i in range(1, len(lista_copia)):
            chave = lista_copia[i]
            j = busca_posicao_insercao(lista_copia, chave, 0, i - 1)
            
            # Move elementos para abrir espaço
            lista_copia[j + 1:i + 1] = lista_copia[j:i]
            lista_copia[j] = chave
        
        return lista_copia
    
    print("   Comparação: Insertion Sort normal vs com busca binária")
    
    def insertion_sort_com_contador(lista, usar_busca_binaria=False):
        """Versão que conta operações"""
        lista_copia = lista.copy()
        comparacoes = 0
        movimentos = 0
        
        if usar_busca_binaria:
            # Implementação simplificada para contagem
            for i in range(1, len(lista_copia)):
                chave = lista_copia[i]
                
                # Busca binária (aproximação de comparações)
                comparacoes += max(1, int(math.log2(i + 1)))
                
                # Encontra posição e move elementos
                j = i - 1
                while j >= 0 and lista_copia[j] > chave:
                    lista_copia[j + 1] = lista_copia[j]
                    movimentos += 1
                    j -= 1
                
                lista_copia[j + 1] = chave
        else:
            # Versão normal
            for i in range(1, len(lista_copia)):
                chave = lista_copia[i]
                j = i - 1
                
                while j >= 0 and lista_copia[j] > chave:
                    comparacoes += 1
                    lista_copia[j + 1] = lista_copia[j]
                    movimentos += 1
                    j -= 1
                
                if j >= 0:  # Comparação final que falhou
                    comparacoes += 1
                
                lista_copia[j + 1] = chave
        
        return lista_copia, comparacoes, movimentos
    
    # Teste com lista maior
    lista_teste = [8, 3, 7, 1, 9, 2, 6, 4, 5]
    
    _, comp_normal, mov_normal = insertion_sort_com_contador(lista_teste, False)
    _, comp_binaria, mov_binaria = insertion_sort_com_contador(lista_teste, True)
    
    print(f"   Lista teste: {lista_teste}")
    print(f"   → Normal: {comp_normal} comparações, {mov_normal} movimentos")
    print(f"   → Busca binária: {comp_binaria} comparações, {mov_binaria} movimentos")
    print()
    
    print("6. CARACTERÍSTICAS DO INSERTION SORT:")
    print("   ✅ Estável (mantém ordem de elementos iguais)")
    print("   ✅ Adaptativo (O(n) para dados quase ordenados)")
    print("   ✅ In-place (O(1) espaço extra)")
    print("   ✅ Eficiente para listas pequenas")
    print("   ✅ Funciona bem com dados chegando em tempo real")
    print("   ❌ O(n²) para dados aleatórios ou reversos")
    print()

def comparacao_algoritmos():
    """
    Compara os três algoritmos básicos de ordenação.
    """
    print("=== COMPARAÇÃO DOS ALGORITMOS BÁSICOS ===")
    print()
    
    print("1. IMPLEMENTAÇÕES PARA COMPARAÇÃO:")
    
    def bubble_sort(lista):
        """Bubble Sort otimizado"""
        lista_copia = lista.copy()
        n = len(lista_copia)
        
        for i in range(n):
            trocou = False
            for j in range(0, n - i - 1):
                if lista_copia[j] > lista_copia[j + 1]:
                    lista_copia[j], lista_copia[j + 1] = lista_copia[j + 1], lista_copia[j]
                    trocou = True
            if not trocou:
                break
        
        return lista_copia
    
    def selection_sort(lista):
        """Selection Sort"""
        lista_copia = lista.copy()
        n = len(lista_copia)
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if lista_copia[j] < lista_copia[min_idx]:
                    min_idx = j
            lista_copia[i], lista_copia[min_idx] = lista_copia[min_idx], lista_copia[i]
        
        return lista_copia
    
    def insertion_sort(lista):
        """Insertion Sort"""
        lista_copia = lista.copy()
        
        for i in range(1, len(lista_copia)):
            chave = lista_copia[i]
            j = i - 1
            
            while j >= 0 and lista_copia[j] > chave:
                lista_copia[j + 1] = lista_copia[j]
                j -= 1
            
            lista_copia[j + 1] = chave
        
        return lista_copia
    
    print("2. TESTE DE PERFORMANCE:")
    
    # Função para medir tempo
    def medir_tempo(algoritmo, lista, nome):
        """Mede tempo de execução de um algoritmo"""
        start = time.perf_counter()
        resultado = algoritmo(lista)
        tempo = time.perf_counter() - start
        return tempo, resultado
    
    # Diferentes cenários de teste
    cenarios = {
        "Pequena Aleatória": [random.randint(1, 100) for _ in range(20)],
        "Pequena Ordenada": list(range(1, 21)),
        "Pequena Reversa": list(range(20, 0, -1)),
        "Média Aleatória": [random.randint(1, 1000) for _ in range(100)],
        "Média Ordenada": list(range(1, 101)),
        "Média Reversa": list(range(100, 0, -1))
    }
    
    algoritmos = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort)
    ]
    
    print("   Tempos de execução (em segundos):")
    print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │    CENÁRIO      │ BUBBLE SORT │SELECT. SORT │INSERT. SORT │")
    print("   ├─────────────────┼─────────────┼─────────────┼─────────────┤")
    
    for nome_cenario, lista_teste in cenarios.items():
        tempos = []
        
        for nome_algo, algoritmo in algoritmos:
            tempo, _ = medir_tempo(algoritmo, lista_teste, nome_algo)
            tempos.append(tempo)
        
        print(f"   │ {nome_cenario:15} │ {tempos[0]:11.6f} │ {tempos[1]:11.6f} │ {tempos[2]:11.6f} │")
    
    print("   └─────────────────┴─────────────┴─────────────┴─────────────┘")
    print()
    
    print("3. ANÁLISE DETALHADA:")
    
    def contar_operacoes(algoritmo_nome, lista):
        """Conta operações para cada algoritmo"""
        n = len(lista)
        
        if algoritmo_nome == "Bubble Sort":
            # Pior caso: O(n²) comparações e trocas
            comparacoes_max = n * (n - 1) // 2
            # Melhor caso (já ordenado): O(n) comparações, 0 trocas
            comparacoes_min = n - 1
            return comparacoes_min, comparacoes_max, "O(n)", "O(n²)"
        
        elif algoritmo_nome == "Selection Sort":
            # Sempre O(n²) comparações, O(n) trocas
            comparacoes = n * (n - 1) // 2
            trocas = n - 1
            return comparacoes, comparacoes, "O(n²)", "O(n²)"
        
        elif algoritmo_nome == "Insertion Sort":
            # Melhor caso: O(n) comparações
            # Pior caso: O(n²) comparações
            comparacoes_min = n - 1
            comparacoes_max = n * (n - 1) // 2
            return comparacoes_min, comparacoes_max, "O(n)", "O(n²)"
    
    print("   Análise teórica de complexidade:")
    print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │   ALGORITMO     │ MELHOR CASO │ PIOR CASO   │ ESTABILID.  │ ADAPTATIVO  │")
    print("   ├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤")
    
    propriedades = [
        ("Bubble Sort", "O(n)", "O(n²)", "Estável", "Sim"),
        ("Selection Sort", "O(n²)", "O(n²)", "Instável", "Não"),
        ("Insertion Sort", "O(n)", "O(n²)", "Estável", "Sim")
    ]
    
    for nome, melhor, pior, estabilidade, adaptativo in propriedades:
        print(f"   │ {nome:15} │ {melhor:11} │ {pior:11} │ {estabilidade:11} │ {adaptativo:11} │")
    
    print("   └─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘")
    print()
    
    print("4. RECOMENDAÇÕES DE USO:")
    print()
    
    print("   BUBBLE SORT:")
    print("   ✅ Fins educacionais (fácil de entender)")
    print("   ✅ Detectar se lista já está ordenada")
    print("   ❌ Evitar em produção (muito lento)")
    print()
    
    print("   SELECTION SORT:")
    print("   ✅ Quando número de trocas deve ser minimizado")
    print("   ✅ Memória é extremamente limitada")
    print("   ❌ Quando estabilidade é importante")
    print("   ❌ Dados parcialmente ordenados")
    print()
    
    print("   INSERTION SORT:")
    print("   ✅ Listas pequenas (< 50 elementos)")
    print("   ✅ Dados quase ordenados")
    print("   ✅ Dados chegando em tempo real")
    print("   ✅ Como sub-rotina de algoritmos híbridos")
    print("   ✅ Quando estabilidade é necessária")
    print()
    
    print("5. DEMONSTRAÇÃO DE ESTABILIDADE:")
    
    # Lista com elementos iguais mas distinguíveis
    pessoas = [
        ("Ana", 25, "A"),
        ("Bruno", 30, "B"),
        ("Carlos", 25, "C"),
        ("Diana", 20, "D"),
        ("Eduardo", 25, "E")
    ]
    
    print(f"   Lista original: {[(p[0], p[1]) for p in pessoas]}")
    
    # Ordenação por idade mantendo estabilidade
    def ordenar_por_idade_estavel(lista):
        """Insertion sort ordenando por idade (estável)"""
        lista_copia = lista.copy()
        
        for i in range(1, len(lista_copia)):
            chave = lista_copia[i]
            j = i - 1
            
            while j >= 0 and lista_copia[j][1] > chave[1]:
                lista_copia[j + 1] = lista_copia[j]
                j -= 1
            
            lista_copia[j + 1] = chave
        
        return lista_copia
    
    def ordenar_por_idade_instavel(lista):
        """Selection sort ordenando por idade (instável)"""
        lista_copia = lista.copy()
        n = len(lista_copia)
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if lista_copia[j][1] < lista_copia[min_idx][1]:
                    min_idx = j
            lista_copia[i], lista_copia[min_idx] = lista_copia[min_idx], lista_copia[i]
        
        return lista_copia
    
    resultado_estavel = ordenar_por_idade_estavel(pessoas)
    resultado_instavel = ordenar_por_idade_instavel(pessoas)
    
    print(f"   Insertion Sort (estável): {[(p[0], p[1], p[2]) for p in resultado_estavel]}")
    print(f"   Selection Sort (instável): {[(p[0], p[1], p[2]) for p in resultado_instavel]}")
    print("   → Note que pessoas com 25 anos mantiveram ordem relativa no algoritmo estável")
    print()

if __name__ == "__main__":
    print("MÓDULO 3.4 - ALGORITMOS DE ORDENAÇÃO BÁSICOS")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceitos_fundamentais()
    print("\n" + "="*50 + "\n")
    
    bubble_sort_implementacao()
    print("\n" + "="*50 + "\n")
    
    selection_sort_implementacao()
    print("\n" + "="*50 + "\n")
    
    insertion_sort_implementacao()
    print("\n" + "="*50 + "\n")
    
    comparacao_algoritmos()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 3.4 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceitos fundamentais de ordenação")
    print("✅ Implementação de Bubble Sort com otimizações")
    print("✅ Implementação de Selection Sort")
    print("✅ Implementação de Insertion Sort")
    print("✅ Análise de complexidade O(n²)")
    print("✅ Conceitos de estabilidade e adaptabilidade")
    print("✅ Comparação de performance entre algoritmos")
    print("✅ Casos de uso apropriados para cada algoritmo")
    print("✅ Visualização passo a passo dos processos")
    print("\n➡️  Próximo: Módulo 3.5 - Algoritmos de Ordenação Avançados")