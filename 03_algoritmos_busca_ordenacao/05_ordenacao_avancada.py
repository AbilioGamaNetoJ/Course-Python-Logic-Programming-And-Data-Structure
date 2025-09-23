"""
Módulo: Algoritmos de Ordenação Avançados
Tópico: Algoritmos de Busca e Ordenação - Merge Sort, Quick Sort e Heap Sort
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário a Avançado

Objetivos de Aprendizado:
- Compreender algoritmos divide-and-conquer
- Implementar Merge Sort (O(n log n))
- Implementar Quick Sort com otimizações
- Implementar Heap Sort
- Analisar complexidade logarítmica
- Comparar com algoritmos básicos
- Aplicar estratégias de otimização
- Escolher algoritmo apropriado por cenário

Conceitos Abordados:
- Paradigma divide-and-conquer
- Merge Sort (ordenação por intercalação)
- Quick Sort (ordenação rápida)
- Heap Sort (ordenação por heap)
- Complexidade O(n log n)
- Análise de casos (melhor, médio, pior)
- Estabilidade vs Performance
- Otimizações práticas

Pré-requisitos:
- Módulos 3.1 a 3.4 completos
- Compreensão de recursão
- Conhecimento de árvores binárias (para Heap Sort)
- Análise de complexidade

Complexidade:
- Merge Sort: O(n log n) sempre, O(n) espaço
- Quick Sort: O(n log n) médio, O(n²) pior caso, O(log n) espaço
- Heap Sort: O(n log n) sempre, O(1) espaço
"""

import time
import random
import math
from typing import List, Tuple, Callable

def conceitos_divide_conquista():
    """
    Introduz o paradigma divide-and-conquer.
    """
    print("=== PARADIGMA DIVIDE-AND-CONQUER ===")
    print()
    
    print("1. DEFINIÇÃO:")
    print("   Divide-and-Conquer (Dividir para Conquistar) é uma estratégia")
    print("   algorítmica que resolve problemas complexos dividindo-os em")
    print("   subproblemas menores, resolvendo-os recursivamente e combinando")
    print("   as soluções para obter a solução final.")
    print()
    
    print("2. ESTRUTURA GERAL:")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │                PROBLEMA ORIGINAL                        │")
    print("   └─────────────────┬───────────────────────────────────────┘")
    print("                     │ DIVIDIR")
    print("   ┌─────────────────▼───────────────────────────────────────┐")
    print("   │         SUBPROBLEMA 1    │    SUBPROBLEMA 2             │")
    print("   └─────────────────┬────────┴────────┬───────────────────────┘")
    print("                     │ CONQUISTAR      │ CONQUISTAR")
    print("   ┌─────────────────▼─────────────────▼───────────────────────┐")
    print("   │         SOLUÇÃO 1        │        SOLUÇÃO 2              │")
    print("   └─────────────────┬────────┴────────┬───────────────────────┘")
    print("                     │ COMBINAR        │")
    print("   ┌─────────────────▼───────────────────────────────────────────┐")
    print("   │                 SOLUÇÃO FINAL                              │")
    print("   └─────────────────────────────────────────────────────────────┘")
    print()
    
    print("3. TRÊS PASSOS FUNDAMENTAIS:")
    print()
    
    print("   DIVIDIR:")
    print("   → Quebrar o problema em subproblemas menores")
    print("   → Geralmente dividir pela metade")
    print("   → Continuar até chegar ao caso base")
    print()
    
    print("   CONQUISTAR:")
    print("   → Resolver subproblemas recursivamente")
    print("   → Caso base: problema pequeno o suficiente para resolver diretamente")
    print("   → Aplicar a mesma estratégia nos subproblemas")
    print()
    
    print("   COMBINAR:")
    print("   → Unir soluções dos subproblemas")
    print("   → Construir solução do problema original")
    print("   → Esta etapa varia conforme o algoritmo")
    print()
    
    print("4. VANTAGENS DO DIVIDE-AND-CONQUER:")
    print("   ✅ Reduz complexidade de O(n²) para O(n log n)")
    print("   ✅ Naturalmente paralelo")
    print("   ✅ Elegante e fácil de entender")
    print("   ✅ Aproveita cache do processador")
    print("   ✅ Funciona bem com recursão")
    print()
    
    print("5. ANÁLISE DE COMPLEXIDADE:")
    print("   Para algoritmos divide-and-conquer típicos:")
    print("   T(n) = 2T(n/2) + O(n)")
    print("   → Pelo Teorema Mestre: T(n) = O(n log n)")
    print()
    
    print("   Intuição:")
    print("   → log n níveis de recursão")
    print("   → O(n) trabalho por nível")
    print("   → Total: O(n log n)")
    print()
    
    print("6. APLICAÇÕES EM ORDENAÇÃO:")
    print("   → Merge Sort: Sempre O(n log n)")
    print("   → Quick Sort: O(n log n) em média")
    print("   → Heap Sort: O(n log n) sempre")
    print()

def merge_sort_implementacao():
    """
    Implementa e analisa o algoritmo Merge Sort.
    """
    print("=== MERGE SORT (ORDENAÇÃO POR INTERCALAÇÃO) ===")
    print()
    
    print("1. CONCEITO:")
    print("   O Merge Sort divide a lista pela metade recursivamente")
    print("   até chegar a listas de um elemento, depois intercala")
    print("   (merge) essas listas mantendo a ordem, construindo")
    print("   gradualmente a lista ordenada final.")
    print()
    
    print("2. ALGORITMO:")
    print("   1. DIVIDIR: Dividir lista pela metade")
    print("   2. CONQUISTAR: Ordenar recursivamente cada metade")
    print("   3. COMBINAR: Intercalar as duas metades ordenadas")
    print()
    
    print("3. IMPLEMENTAÇÃO BÁSICA:")
    
    def merge_sort_basico(lista):
        """
        Implementação básica do Merge Sort.
        
        Args:
            lista: Lista a ser ordenada
            
        Returns:
            List: Lista ordenada
        """
        # Caso base: lista com 0 ou 1 elemento já está ordenada
        if len(lista) <= 1:
            return lista
        
        # Dividir: encontrar o meio
        meio = len(lista) // 2
        esquerda = lista[:meio]
        direita = lista[meio:]
        
        # Conquistar: ordenar recursivamente cada metade
        esquerda_ordenada = merge_sort_basico(esquerda)
        direita_ordenada = merge_sort_basico(direita)
        
        # Combinar: intercalar as duas metades ordenadas
        return intercalar(esquerda_ordenada, direita_ordenada)
    
    def intercalar(esquerda, direita):
        """
        Intercala duas listas ordenadas em uma lista ordenada.
        
        Args:
            esquerda: Lista ordenada
            direita: Lista ordenada
            
        Returns:
            List: Lista intercalada e ordenada
        """
        resultado = []
        i = j = 0
        
        # Comparar elementos e adicionar o menor
        while i < len(esquerda) and j < len(direita):
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1
        
        # Adicionar elementos restantes
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        
        return resultado
    
    # Demonstração básica
    numeros = [38, 27, 43, 3, 9, 82, 10]
    print(f"   Lista original: {numeros}")
    
    resultado = merge_sort_basico(numeros)
    print(f"   Lista ordenada: {resultado}")
    print()
    
    print("4. VISUALIZAÇÃO PASSO A PASSO:")
    
    def merge_sort_visualizado(lista, nivel=0):
        """
        Merge Sort com visualização do processo.
        """
        indent = "   " + "  " * nivel
        
        print(f"{indent}Dividir: {lista}")
        
        # Caso base
        if len(lista) <= 1:
            print(f"{indent}Caso base: {lista}")
            return lista
        
        # Dividir
        meio = len(lista) // 2
        esquerda = lista[:meio]
        direita = lista[meio:]
        
        print(f"{indent}├─ Esquerda: {esquerda}")
        print(f"{indent}└─ Direita: {direita}")
        
        # Conquistar
        esquerda_ordenada = merge_sort_visualizado(esquerda, nivel + 1)
        direita_ordenada = merge_sort_visualizado(direita, nivel + 1)
        
        # Combinar
        resultado = intercalar_visualizado(esquerda_ordenada, direita_ordenada, nivel)
        
        print(f"{indent}Resultado: {resultado}")
        return resultado
    
    def intercalar_visualizado(esquerda, direita, nivel):
        """Intercalação com visualização"""
        indent = "   " + "  " * nivel
        print(f"{indent}Intercalar: {esquerda} + {direita}")
        
        resultado = []
        i = j = 0
        
        while i < len(esquerda) and j < len(direita):
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                print(f"{indent}→ Adicionar {esquerda[i]} da esquerda")
                i += 1
            else:
                resultado.append(direita[j])
                print(f"{indent}→ Adicionar {direita[j]} da direita")
                j += 1
        
        # Adicionar restantes
        if i < len(esquerda):
            resultado.extend(esquerda[i:])
            print(f"{indent}→ Adicionar restante da esquerda: {esquerda[i:]}")
        
        if j < len(direita):
            resultado.extend(direita[j:])
            print(f"{indent}→ Adicionar restante da direita: {direita[j:]}")
        
        return resultado
    
    # Exemplo visual com lista menor
    print("   Exemplo visual:")
    numeros_pequenos = [4, 2, 7, 1]
    merge_sort_visualizado(numeros_pequenos)
    print()
    
    print("5. ANÁLISE DE COMPLEXIDADE:")
    
    def merge_sort_com_contador(lista, contador=None):
        """Merge Sort que conta operações"""
        if contador is None:
            contador = {'comparacoes': 0, 'movimentos': 0, 'niveis': 0}
        
        if len(lista) <= 1:
            return lista, contador
        
        contador['niveis'] += 1
        meio = len(lista) // 2
        
        esquerda, contador = merge_sort_com_contador(lista[:meio], contador)
        direita, contador = merge_sort_com_contador(lista[meio:], contador)
        
        return intercalar_com_contador(esquerda, direita, contador), contador
    
    def intercalar_com_contador(esquerda, direita, contador):
        """Intercalação que conta operações"""
        resultado = []
        i = j = 0
        
        while i < len(esquerda) and j < len(direita):
            contador['comparacoes'] += 1
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                contador['movimentos'] += 1
                i += 1
            else:
                resultado.append(direita[j])
                contador['movimentos'] += 1
                j += 1
        
        # Movimentos dos elementos restantes
        contador['movimentos'] += len(esquerda) - i + len(direita) - j
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        
        return resultado
    
    # Teste com diferentes tamanhos
    tamanhos = [8, 16, 32, 64]
    
    print("   Análise empírica de complexidade:")
    print("   ┌──────────┬─────────────┬─────────────┬─────────────┐")
    print("   │ TAMANHO  │ COMPARAÇÕES │ MOVIMENTOS  │   NÍVEIS    │")
    print("   ├──────────┼─────────────┼─────────────┼─────────────┤")
    
    for n in tamanhos:
        lista_teste = [random.randint(1, 100) for _ in range(n)]
        _, stats = merge_sort_com_contador(lista_teste)
        
        print(f"   │ {n:8} │ {stats['comparacoes']:11} │ {stats['movimentos']:11} │ {stats['niveis']:11} │")
    
    print("   └──────────┴─────────────┴─────────────┴─────────────┘")
    print()
    
    print("   Observações:")
    print("   → Níveis ≈ log₂(n) como esperado")
    print("   → Comparações ≈ n log n")
    print("   → Movimentos ≈ n log n")
    print("   → Performance consistente (não-adaptativo)")
    print()
    
    print("6. CARACTERÍSTICAS DO MERGE SORT:")
    print("   ✅ Sempre O(n log n) - performance garantida")
    print("   ✅ Estável (mantém ordem de elementos iguais)")
    print("   ✅ Previsível (não depende dos dados)")
    print("   ✅ Paralelizável")
    print("   ❌ Usa O(n) espaço extra")
    print("   ❌ Não é in-place")
    print("   ❌ Overhead de recursão")
    print()

def quick_sort_implementacao():
    """
    Implementa e analisa o algoritmo Quick Sort.
    """
    print("=== QUICK SORT (ORDENAÇÃO RÁPIDA) ===")
    print()
    
    print("1. CONCEITO:")
    print("   O Quick Sort escolhe um elemento como 'pivô' e particiona")
    print("   a lista de forma que elementos menores ficam à esquerda")
    print("   e maiores à direita do pivô. Depois aplica o mesmo processo")
    print("   recursivamente nas duas partições.")
    print()
    
    print("2. ALGORITMO:")
    print("   1. ESCOLHER: Selecionar um pivô")
    print("   2. PARTICIONAR: Reorganizar lista em torno do pivô")
    print("   3. RECURSÃO: Aplicar Quick Sort nas duas partições")
    print()
    
    print("3. IMPLEMENTAÇÃO BÁSICA:")
    
    def quick_sort_basico(lista):
        """
        Implementação básica do Quick Sort.
        
        Args:
            lista: Lista a ser ordenada
            
        Returns:
            List: Lista ordenada
        """
        # Caso base
        if len(lista) <= 1:
            return lista
        
        # Escolher pivô (último elemento)
        pivo = lista[-1]
        
        # Particionar
        menores = [x for x in lista[:-1] if x <= pivo]
        maiores = [x for x in lista[:-1] if x > pivo]
        
        # Recursão e combinação
        return quick_sort_basico(menores) + [pivo] + quick_sort_basico(maiores)
    
    # Demonstração básica
    numeros = [3, 6, 8, 10, 1, 2, 1]
    print(f"   Lista original: {numeros}")
    
    resultado = quick_sort_basico(numeros)
    print(f"   Lista ordenada: {resultado}")
    print()
    
    print("4. IMPLEMENTAÇÃO IN-PLACE (OTIMIZADA):")
    
    def quick_sort_inplace(lista, inicio=0, fim=None):
        """
        Quick Sort in-place (mais eficiente em memória).
        """
        if fim is None:
            fim = len(lista) - 1
        
        if inicio < fim:
            # Particionar e obter posição do pivô
            pos_pivo = particionar(lista, inicio, fim)
            
            # Recursão nas duas partições
            quick_sort_inplace(lista, inicio, pos_pivo - 1)
            quick_sort_inplace(lista, pos_pivo + 1, fim)
    
    def particionar(lista, inicio, fim):
        """
        Particiona a lista em torno do pivô (último elemento).
        
        Returns:
            int: Posição final do pivô
        """
        pivo = lista[fim]
        i = inicio - 1  # Índice do menor elemento
        
        for j in range(inicio, fim):
            # Se elemento atual é menor ou igual ao pivô
            if lista[j] <= pivo:
                i += 1
                lista[i], lista[j] = lista[j], lista[i]
        
        # Colocar pivô na posição correta
        lista[i + 1], lista[fim] = lista[fim], lista[i + 1]
        return i + 1
    
    print("5. VISUALIZAÇÃO DO PARTICIONAMENTO:")
    
    def particionar_visualizado(lista, inicio, fim):
        """Particionamento com visualização"""
        print(f"   Particionar: {lista[inicio:fim+1]} (pivô = {lista[fim]})")
        
        pivo = lista[fim]
        i = inicio - 1
        
        for j in range(inicio, fim):
            print(f"   → Comparar {lista[j]} com pivô {pivo}: ", end="")
            
            if lista[j] <= pivo:
                i += 1
                if i != j:
                    lista[i], lista[j] = lista[j], lista[i]
                    print(f"trocar → {lista}")
                else:
                    print(f"manter → {lista}")
            else:
                print(f"maior → {lista}")
        
        # Colocar pivô na posição final
        lista[i + 1], lista[fim] = lista[fim], lista[i + 1]
        print(f"   Pivô {pivo} na posição {i + 1}: {lista}")
        
        return i + 1
    
    def quick_sort_visualizado(lista, inicio=0, fim=None, nivel=0):
        """Quick Sort com visualização"""
        if fim is None:
            fim = len(lista) - 1
        
        indent = "   " + "  " * nivel
        
        if inicio < fim:
            print(f"{indent}Quick Sort: {lista[inicio:fim+1]}")
            
            pos_pivo = particionar_visualizado(lista, inicio, fim)
            
            print(f"{indent}├─ Esquerda: {lista[inicio:pos_pivo]}")
            print(f"{indent}└─ Direita: {lista[pos_pivo+1:fim+1]}")
            
            quick_sort_visualizado(lista, inicio, pos_pivo - 1, nivel + 1)
            quick_sort_visualizado(lista, pos_pivo + 1, fim, nivel + 1)
    
    # Exemplo visual
    print("   Exemplo visual:")
    numeros_exemplo = [4, 2, 7, 1, 8, 3]
    lista_copia = numeros_exemplo.copy()
    quick_sort_visualizado(lista_copia)
    print(f"   Resultado final: {lista_copia}")
    print()
    
    print("6. ESTRATÉGIAS DE ESCOLHA DO PIVÔ:")
    
    def quick_sort_pivo_aleatorio(lista, inicio=0, fim=None):
        """Quick Sort com pivô aleatório"""
        if fim is None:
            fim = len(lista) - 1
        
        if inicio < fim:
            # Escolher pivô aleatório e trocar com o último
            pivo_idx = random.randint(inicio, fim)
            lista[pivo_idx], lista[fim] = lista[fim], lista[pivo_idx]
            
            pos_pivo = particionar(lista, inicio, fim)
            quick_sort_pivo_aleatorio(lista, inicio, pos_pivo - 1)
            quick_sort_pivo_aleatorio(lista, pos_pivo + 1, fim)
    
    def quick_sort_mediana_de_tres(lista, inicio=0, fim=None):
        """Quick Sort com mediana de três como pivô"""
        if fim is None:
            fim = len(lista) - 1
        
        if inicio < fim:
            # Mediana de três: início, meio, fim
            meio = (inicio + fim) // 2
            
            # Ordenar os três elementos
            if lista[inicio] > lista[meio]:
                lista[inicio], lista[meio] = lista[meio], lista[inicio]
            if lista[meio] > lista[fim]:
                lista[meio], lista[fim] = lista[fim], lista[meio]
            if lista[inicio] > lista[meio]:
                lista[inicio], lista[meio] = lista[meio], lista[inicio]
            
            # Colocar mediana no final (como pivô)
            lista[meio], lista[fim] = lista[fim], lista[meio]
            
            pos_pivo = particionar(lista, inicio, fim)
            quick_sort_mediana_de_tres(lista, inicio, pos_pivo - 1)
            quick_sort_mediana_de_tres(lista, pos_pivo + 1, fim)
    
    print("   Comparação de estratégias de pivô:")
    
    # Teste com lista que causa pior caso para pivô fixo
    lista_pior_caso = list(range(1, 11))  # Lista já ordenada
    
    estrategias = [
        ("Último elemento", lambda l: quick_sort_inplace(l.copy())),
        ("Aleatório", lambda l: quick_sort_pivo_aleatorio(l.copy())),
        ("Mediana de 3", lambda l: quick_sort_mediana_de_tres(l.copy()))
    ]
    
    print("   ┌─────────────────┬─────────────┬─────────────┐")
    print("   │   ESTRATÉGIA    │    TEMPO    │ OBSERVAÇÃO  │")
    print("   ├─────────────────┼─────────────┼─────────────┤")
    
    for nome, funcao in estrategias:
        start = time.perf_counter()
        try:
            funcao(lista_pior_caso)
            tempo = time.perf_counter() - start
            obs = "OK"
        except RecursionError:
            tempo = float('inf')
            obs = "Stack overflow"
        
        print(f"   │ {nome:15} │ {tempo:11.6f} │ {obs:11} │")
    
    print("   └─────────────────┴─────────────┴─────────────┘")
    print()
    
    print("7. ANÁLISE DE COMPLEXIDADE:")
    print("   MELHOR CASO: O(n log n)")
    print("   → Pivô sempre divide lista pela metade")
    print("   → log n níveis, O(n) trabalho por nível")
    print()
    
    print("   CASO MÉDIO: O(n log n)")
    print("   → Pivô divide lista em proporções razoáveis")
    print("   → Análise probabilística mostra O(n log n)")
    print()
    
    print("   PIOR CASO: O(n²)")
    print("   → Pivô sempre é o menor ou maior elemento")
    print("   → Acontece com listas já ordenadas (pivô fixo)")
    print("   → n níveis, O(n) trabalho por nível")
    print()
    
    print("8. CARACTERÍSTICAS DO QUICK SORT:")
    print("   ✅ Muito rápido na prática (O(n log n) médio)")
    print("   ✅ In-place (O(log n) espaço para recursão)")
    print("   ✅ Cache-friendly")
    print("   ✅ Paralelizável")
    print("   ❌ Instável")
    print("   ❌ Pior caso O(n²)")
    print("   ❌ Performance depende da escolha do pivô")
    print()

def heap_sort_implementacao():
    """
    Implementa e analisa o algoritmo Heap Sort.
    """
    print("=== HEAP SORT (ORDENAÇÃO POR HEAP) ===")
    print()
    
    print("1. CONCEITO:")
    print("   O Heap Sort usa uma estrutura de dados chamada heap")
    print("   (árvore binária completa com propriedade de heap)")
    print("   para ordenar elementos. Constrói um max-heap e")
    print("   repetidamente extrai o máximo.")
    print()
    
    print("2. PROPRIEDADE DE HEAP:")
    print("   MAX-HEAP: Pai ≥ Filhos")
    print("   MIN-HEAP: Pai ≤ Filhos")
    print()
    
    print("   Representação em array:")
    print("   Para elemento no índice i:")
    print("   → Pai: (i-1)//2")
    print("   → Filho esquerdo: 2*i + 1")
    print("   → Filho direito: 2*i + 2")
    print()
    
    print("3. ALGORITMO:")
    print("   1. CONSTRUIR: Transformar array em max-heap")
    print("   2. EXTRAIR: Repetidamente extrair máximo")
    print("   3. REORGANIZAR: Manter propriedade de heap")
    print()
    
    print("4. IMPLEMENTAÇÃO:")
    
    def heap_sort(lista):
        """
        Implementação do Heap Sort.
        
        Args:
            lista: Lista a ser ordenada
            
        Returns:
            List: Lista ordenada
        """
        lista_copia = lista.copy()
        n = len(lista_copia)
        
        # Construir max-heap
        for i in range(n // 2 - 1, -1, -1):
            heapify(lista_copia, n, i)
        
        # Extrair elementos um por um
        for i in range(n - 1, 0, -1):
            # Mover raiz atual para o final
            lista_copia[0], lista_copia[i] = lista_copia[i], lista_copia[0]
            
            # Chamar heapify na heap reduzida
            heapify(lista_copia, i, 0)
        
        return lista_copia
    
    def heapify(lista, n, i):
        """
        Mantém propriedade de max-heap para subárvore com raiz em i.
        
        Args:
            lista: Array representando heap
            n: Tamanho da heap
            i: Índice da raiz da subárvore
        """
        maior = i  # Inicializar maior como raiz
        esquerdo = 2 * i + 1  # Filho esquerdo
        direito = 2 * i + 2   # Filho direito
        
        # Se filho esquerdo é maior que raiz
        if esquerdo < n and lista[esquerdo] > lista[maior]:
            maior = esquerdo
        
        # Se filho direito é maior que o maior até agora
        if direito < n and lista[direito] > lista[maior]:
            maior = direito
        
        # Se maior não é raiz
        if maior != i:
            lista[i], lista[maior] = lista[maior], lista[i]
            
            # Recursivamente heapify a subárvore afetada
            heapify(lista, n, maior)
    
    # Demonstração básica
    numeros = [12, 11, 13, 5, 6, 7]
    print(f"   Lista original: {numeros}")
    
    resultado = heap_sort(numeros)
    print(f"   Lista ordenada: {resultado}")
    print()
    
    print("5. VISUALIZAÇÃO DA CONSTRUÇÃO DO HEAP:")
    
    def visualizar_heap(lista, titulo="Heap"):
        """Visualiza heap como árvore"""
        print(f"   {titulo}: {lista}")
        
        if not lista:
            return
        
        # Calcular altura da árvore
        altura = int(math.log2(len(lista))) + 1
        
        # Imprimir árvore nível por nível
        for nivel in range(altura):
            inicio = 2 ** nivel - 1
            fim = min(2 ** (nivel + 1) - 1, len(lista))
            
            if inicio >= len(lista):
                break
            
            # Espaçamento para centralizar
            espacos = " " * (4 * (altura - nivel - 1))
            
            print("   " + espacos, end="")
            for i in range(inicio, fim):
                if i < len(lista):
                    print(f"{lista[i]:2}", end="  ")
            print()
        print()
    
    def heap_sort_visualizado(lista):
        """Heap Sort com visualização"""
        lista_copia = lista.copy()
        n = len(lista_copia)
        
        print("   Construindo max-heap:")
        
        # Construir heap
        for i in range(n // 2 - 1, -1, -1):
            print(f"   Heapify a partir do índice {i}:")
            heapify_visualizado(lista_copia, n, i)
            visualizar_heap(lista_copia, f"Após heapify({i})")
        
        print("   Extraindo elementos:")
        
        # Extrair elementos
        for i in range(n - 1, 0, -1):
            print(f"   Extrair máximo {lista_copia[0]}:")
            
            # Trocar raiz com último elemento
            lista_copia[0], lista_copia[i] = lista_copia[i], lista_copia[0]
            print(f"   Após troca: {lista_copia}")
            
            # Heapify heap reduzida
            heapify_visualizado(lista_copia, i, 0)
            
            # Mostrar estado atual
            heap_parte = lista_copia[:i]
            ordenada_parte = lista_copia[i:]
            print(f"   Heap: {heap_parte} | Ordenado: {ordenada_parte}")
            print("   " + "─" * 40)
        
        return lista_copia
    
    def heapify_visualizado(lista, n, i):
        """Heapify com visualização"""
        maior = i
        esquerdo = 2 * i + 1
        direito = 2 * i + 2
        
        # Encontrar o maior
        if esquerdo < n and lista[esquerdo] > lista[maior]:
            maior = esquerdo
        
        if direito < n and lista[direito] > lista[maior]:
            maior = direito
        
        # Se precisa trocar
        if maior != i:
            print(f"   → Trocar {lista[i]} (índice {i}) com {lista[maior]} (índice {maior})")
            lista[i], lista[maior] = lista[maior], lista[i]
            
            # Continuar heapify
            heapify_visualizado(lista, n, maior)
    
    # Exemplo visual
    print("   Exemplo visual:")
    numeros_exemplo = [4, 10, 3, 5, 1]
    heap_sort_visualizado(numeros_exemplo)
    print()
    
    print("6. ANÁLISE DE COMPLEXIDADE:")
    print("   CONSTRUÇÃO DO HEAP: O(n)")
    print("   → Embora heapify seja O(log n), análise amortizada mostra O(n)")
    print()
    
    print("   EXTRAÇÃO DE ELEMENTOS: O(n log n)")
    print("   → n extrações, cada uma O(log n) para heapify")
    print()
    
    print("   TOTAL: O(n log n)")
    print("   → Sempre O(n log n), independente dos dados")
    print()
    
    print("7. CARACTERÍSTICAS DO HEAP SORT:")
    print("   ✅ Sempre O(n log n) - performance garantida")
    print("   ✅ In-place (O(1) espaço extra)")
    print("   ✅ Não usa recursão (iterativo)")
    print("   ✅ Bom para sistemas com restrições de memória")
    print("   ❌ Instável")
    print("   ❌ Não é cache-friendly")
    print("   ❌ Constante maior que Quick Sort")
    print()

def comparacao_algoritmos_avancados():
    """
    Compara os algoritmos avançados de ordenação.
    """
    print("=== COMPARAÇÃO DOS ALGORITMOS AVANÇADOS ===")
    print()
    
    print("1. IMPLEMENTAÇÕES PARA BENCHMARK:")
    
    # Implementações otimizadas para comparação
    def merge_sort_otimizado(lista):
        """Merge Sort otimizado"""
        if len(lista) <= 1:
            return lista
        
        meio = len(lista) // 2
        esquerda = merge_sort_otimizado(lista[:meio])
        direita = merge_sort_otimizado(lista[meio:])
        
        # Intercalação otimizada
        resultado = []
        i = j = 0
        
        while i < len(esquerda) and j < len(direita):
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1
        
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        
        return resultado
    
    def quick_sort_otimizado(lista):
        """Quick Sort com mediana de três e cutoff para insertion sort"""
        def quick_sort_rec(arr, inicio, fim):
            if fim - inicio < 10:  # Cutoff para insertion sort
                insertion_sort_range(arr, inicio, fim)
                return
            
            if inicio < fim:
                # Mediana de três
                meio = (inicio + fim) // 2
                if arr[inicio] > arr[meio]:
                    arr[inicio], arr[meio] = arr[meio], arr[inicio]
                if arr[meio] > arr[fim]:
                    arr[meio], arr[fim] = arr[fim], arr[meio]
                if arr[inicio] > arr[meio]:
                    arr[inicio], arr[meio] = arr[meio], arr[inicio]
                
                arr[meio], arr[fim] = arr[fim], arr[meio]
                
                pos_pivo = particionar_otimizado(arr, inicio, fim)
                quick_sort_rec(arr, inicio, pos_pivo - 1)
                quick_sort_rec(arr, pos_pivo + 1, fim)
        
        def particionar_otimizado(arr, inicio, fim):
            pivo = arr[fim]
            i = inicio - 1
            
            for j in range(inicio, fim):
                if arr[j] <= pivo:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            
            arr[i + 1], arr[fim] = arr[fim], arr[i + 1]
            return i + 1
        
        def insertion_sort_range(arr, inicio, fim):
            for i in range(inicio + 1, fim + 1):
                chave = arr[i]
                j = i - 1
                while j >= inicio and arr[j] > chave:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = chave
        
        lista_copia = lista.copy()
        quick_sort_rec(lista_copia, 0, len(lista_copia) - 1)
        return lista_copia
    
    def heap_sort_otimizado(lista):
        """Heap Sort otimizado"""
        def heapify_iterativo(arr, n, i):
            while True:
                maior = i
                esquerdo = 2 * i + 1
                direito = 2 * i + 2
                
                if esquerdo < n and arr[esquerdo] > arr[maior]:
                    maior = esquerdo
                
                if direito < n and arr[direito] > arr[maior]:
                    maior = direito
                
                if maior == i:
                    break
                
                arr[i], arr[maior] = arr[maior], arr[i]
                i = maior
        
        lista_copia = lista.copy()
        n = len(lista_copia)
        
        # Construir heap
        for i in range(n // 2 - 1, -1, -1):
            heapify_iterativo(lista_copia, n, i)
        
        # Extrair elementos
        for i in range(n - 1, 0, -1):
            lista_copia[0], lista_copia[i] = lista_copia[i], lista_copia[0]
            heapify_iterativo(lista_copia, i, 0)
        
        return lista_copia
    
    print("2. BENCHMARK DE PERFORMANCE:")
    
    algoritmos = [
        ("Merge Sort", merge_sort_otimizado),
        ("Quick Sort", quick_sort_otimizado),
        ("Heap Sort", heap_sort_otimizado)
    ]
    
    # Diferentes cenários de teste
    cenarios = {
        "Aleatório (1K)": [random.randint(1, 1000) for _ in range(1000)],
        "Ordenado (1K)": list(range(1000)),
        "Reverso (1K)": list(range(999, -1, -1)),
        "Quase Ord. (1K)": list(range(1000)) + [random.randint(1, 1000) for _ in range(50)],
        "Duplicatas (1K)": [random.randint(1, 100) for _ in range(1000)]
    }
    
    print("   Tempos de execução (em segundos):")
    print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │    CENÁRIO      │ MERGE SORT  │ QUICK SORT  │ HEAP SORT   │")
    print("   ├─────────────────┼─────────────┼─────────────┼─────────────┤")
    
    for nome_cenario, lista_teste in cenarios.items():
        tempos = []
        
        for nome_algo, algoritmo in algoritmos:
            # Medir tempo médio de 3 execuções
            tempos_exec = []
            for _ in range(3):
                start = time.perf_counter()
                algoritmo(lista_teste.copy())
                tempo = time.perf_counter() - start
                tempos_exec.append(tempo)
            
            tempo_medio = sum(tempos_exec) / len(tempos_exec)
            tempos.append(tempo_medio)
        
        print(f"   │ {nome_cenario:15} │ {tempos[0]:11.6f} │ {tempos[1]:11.6f} │ {tempos[2]:11.6f} │")
    
    print("   └─────────────────┴─────────────┴─────────────┴─────────────┘")
    print()
    
    print("3. ANÁLISE COMPARATIVA:")
    
    print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │   ALGORITMO     │ COMPLEXID.  │   ESPAÇO    │ ESTABILID.  │ OBSERVAÇÕES │")
    print("   ├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤")
    print("   │ Merge Sort      │ O(n log n)  │    O(n)     │   Estável   │ Previsível  │")
    print("   │ Quick Sort      │ O(n log n)* │  O(log n)   │  Instável   │ Rápido      │")
    print("   │ Heap Sort       │ O(n log n)  │    O(1)     │  Instável   │ Consistente │")
    print("   └─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘")
    print("   * Caso médio; pior caso O(n²)")
    print()
    
    print("4. GUIA DE ESCOLHA:")
    print()
    
    print("   MERGE SORT - Use quando:")
    print("   ✅ Estabilidade é crucial")
    print("   ✅ Performance previsível é necessária")
    print("   ✅ Dados são muito grandes (external sorting)")
    print("   ✅ Paralelização é possível")
    print("   ❌ Memória é limitada")
    print()
    
    print("   QUICK SORT - Use quando:")
    print("   ✅ Performance máxima é prioridade")
    print("   ✅ Memória é limitada")
    print("   ✅ Dados são aleatórios")
    print("   ✅ Cache performance importa")
    print("   ❌ Estabilidade é necessária")
    print("   ❌ Pior caso O(n²) é inaceitável")
    print()
    
    print("   HEAP SORT - Use quando:")
    print("   ✅ Memória é muito limitada")
    print("   ✅ Performance garantida é necessária")
    print("   ✅ Não pode usar recursão")
    print("   ✅ Implementação simples é preferida")
    print("   ❌ Cache performance é crítica")
    print("   ❌ Estabilidade é necessária")
    print()
    
    print("5. ALGORITMOS HÍBRIDOS:")
    print("   Na prática, muitas implementações usam combinações:")
    print("   → Introsort: Quick Sort + Heap Sort (C++ std::sort)")
    print("   → Timsort: Merge Sort + Insertion Sort (Python sorted())")
    print("   → Quick Sort + Insertion Sort para arrays pequenos")
    print()

if __name__ == "__main__":
    print("MÓDULO 3.5 - ALGORITMOS DE ORDENAÇÃO AVANÇADOS")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceitos_divide_conquista()
    print("\n" + "="*50 + "\n")
    
    merge_sort_implementacao()
    print("\n" + "="*50 + "\n")
    
    quick_sort_implementacao()
    print("\n" + "="*50 + "\n")
    
    heap_sort_implementacao()
    print("\n" + "="*50 + "\n")
    
    comparacao_algoritmos_avancados()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 3.5 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Paradigma divide-and-conquer")
    print("✅ Merge Sort - O(n log n) estável")
    print("✅ Quick Sort - O(n log n) médio, in-place")
    print("✅ Heap Sort - O(n log n) garantido, O(1) espaço")
    print("✅ Análise de complexidade logarítmica")
    print("✅ Estratégias de otimização")
    print("✅ Comparação de performance prática")
    print("✅ Guia de escolha por cenário")
    print("✅ Conceitos de algoritmos híbridos")
    print("\n➡️  Próximo: Módulo 3.6 - Análise Comparativa e Otimizações")