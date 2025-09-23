"""
Módulo: Algoritmos Especializados
Tópico: Algoritmos de Busca e Ordenação - Casos Especiais e Aplicações Avançadas
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Avançado

Objetivos de Aprendizado:
- Implementar algoritmos para casos específicos
- Compreender algoritmos de ordenação não-comparativa
- Aplicar algoritmos em problemas reais
- Otimizar para tipos de dados específicos
- Implementar algoritmos de busca avançados
- Desenvolver soluções para big data
- Compreender algoritmos paralelos
- Aplicar técnicas de aproximação

Conceitos Abordados:
- Counting Sort, Radix Sort, Bucket Sort
- Algoritmos de busca em strings
- Busca aproximada e fuzzy matching
- Algoritmos para dados externos
- Ordenação estável vs instável
- Algoritmos probabilísticos
- Técnicas de paralelização
- Otimizações específicas por domínio

Pré-requisitos:
- Módulos 3.1 a 3.6 completos
- Compreensão sólida de complexidade
- Conhecimento de estruturas de dados básicas
- Familiaridade com conceitos de sistemas

Complexidade:
- Algoritmos lineares O(n) para casos específicos
- Algoritmos sub-lineares para busca
- Análise de trade-offs espaço-tempo
- Complexidade em cenários paralelos
"""

import random
import string
import math
import heapq
from collections import defaultdict, Counter
from typing import List, Tuple, Optional, Callable, Iterator
import time
import bisect

def algoritmos_ordenacao_nao_comparativa():
    """
    Implementa algoritmos de ordenação que não usam comparações.
    """
    print("=== ALGORITMOS DE ORDENAÇÃO NÃO-COMPARATIVA ===")
    print()
    
    print("1. COUNTING SORT - O(n + k):")
    print("   → Eficiente quando k (range) é pequeno")
    print("   → Estável por natureza")
    print("   → Usa espaço extra O(k)")
    print()
    
    def counting_sort_basico(lista, max_val=None):
        """
        Counting Sort básico para números inteiros positivos.
        """
        if not lista:
            return lista
        
        if max_val is None:
            max_val = max(lista)
        
        # Array de contagem
        count = [0] * (max_val + 1)
        
        # Contar ocorrências
        for num in lista:
            count[num] += 1
        
        # Reconstruir array ordenado
        resultado = []
        for valor, freq in enumerate(count):
            resultado.extend([valor] * freq)
        
        return resultado
    
    def counting_sort_estavel(lista, max_val=None):
        """
        Counting Sort estável que preserva ordem relativa.
        """
        if not lista:
            return lista
        
        if max_val is None:
            max_val = max(lista)
        
        # Array de contagem
        count = [0] * (max_val + 1)
        
        # Contar ocorrências
        for num in lista:
            count[num] += 1
        
        # Transformar em posições cumulativas
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        
        # Construir resultado da direita para esquerda (estabilidade)
        resultado = [0] * len(lista)
        for i in range(len(lista) - 1, -1, -1):
            valor = lista[i]
            count[valor] -= 1
            resultado[count[valor]] = valor
        
        return resultado
    
    # Demonstração
    dados_teste = [4, 2, 2, 8, 3, 3, 1, 7, 4, 2]
    print(f"   Dados originais: {dados_teste}")
    print(f"   Counting básico: {counting_sort_basico(dados_teste)}")
    print(f"   Counting estável: {counting_sort_estavel(dados_teste)}")
    print()
    
    print("2. RADIX SORT - O(d × (n + k)):")
    print("   → d = número de dígitos")
    print("   → k = base (10 para decimal)")
    print("   → Eficiente para números com poucos dígitos")
    print()
    
    def radix_sort_lsd(lista):
        """
        Radix Sort LSD (Least Significant Digit) para inteiros.
        """
        if not lista:
            return lista
        
        # Encontrar número máximo para determinar dígitos
        max_num = max(lista)
        num_digitos = len(str(max_num))
        
        # Copiar lista
        resultado = lista.copy()
        
        # Processar cada dígito
        for digito in range(num_digitos):
            # Counting sort por dígito atual
            buckets = [[] for _ in range(10)]
            
            for num in resultado:
                digito_atual = (num // (10 ** digito)) % 10
                buckets[digito_atual].append(num)
            
            # Reconstruir lista
            resultado = []
            for bucket in buckets:
                resultado.extend(bucket)
        
        return resultado
    
    def radix_sort_msd(lista, digito=None):
        """
        Radix Sort MSD (Most Significant Digit) - recursivo.
        """
        if not lista or len(lista) <= 1:
            return lista
        
        if digito is None:
            max_num = max(lista)
            digito = len(str(max_num)) - 1
        
        if digito < 0:
            return lista
        
        # Separar em buckets por dígito mais significativo
        buckets = [[] for _ in range(10)]
        
        for num in lista:
            digito_atual = (num // (10 ** digito)) % 10
            buckets[digito_atual].append(num)
        
        # Recursivamente ordenar cada bucket
        resultado = []
        for bucket in buckets:
            if bucket:
                resultado.extend(radix_sort_msd(bucket, digito - 1))
        
        return resultado
    
    # Demonstração
    dados_radix = [170, 45, 75, 90, 2, 802, 24, 66]
    print(f"   Dados originais: {dados_radix}")
    print(f"   Radix LSD:       {radix_sort_lsd(dados_radix)}")
    print(f"   Radix MSD:       {radix_sort_msd(dados_radix)}")
    print()
    
    print("3. BUCKET SORT - O(n + k) médio:")
    print("   → Distribui elementos em buckets")
    print("   → Ordena cada bucket individualmente")
    print("   → Eficiente para distribuição uniforme")
    print()
    
    def bucket_sort(lista, num_buckets=None):
        """
        Bucket Sort para números em ponto flutuante [0, 1).
        """
        if not lista:
            return lista
        
        if num_buckets is None:
            num_buckets = len(lista)
        
        # Criar buckets
        buckets = [[] for _ in range(num_buckets)]
        
        # Distribuir elementos nos buckets
        for num in lista:
            bucket_index = min(int(num * num_buckets), num_buckets - 1)
            buckets[bucket_index].append(num)
        
        # Ordenar cada bucket e concatenar
        resultado = []
        for bucket in buckets:
            if bucket:
                bucket.sort()  # Pode usar qualquer algoritmo
                resultado.extend(bucket)
        
        return resultado
    
    def bucket_sort_inteiros(lista, bucket_size=5):
        """
        Bucket Sort adaptado para inteiros.
        """
        if not lista:
            return lista
        
        min_val, max_val = min(lista), max(lista)
        bucket_range = (max_val - min_val) // bucket_size + 1
        
        # Criar buckets
        buckets = [[] for _ in range(bucket_range)]
        
        # Distribuir elementos
        for num in lista:
            bucket_index = (num - min_val) // bucket_size
            buckets[bucket_index].append(num)
        
        # Ordenar e concatenar
        resultado = []
        for bucket in buckets:
            if bucket:
                bucket.sort()
                resultado.extend(bucket)
        
        return resultado
    
    # Demonstração
    dados_float = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    dados_int = [29, 25, 3, 49, 9, 37, 21, 43]
    
    print(f"   Float [0,1):     {[f'{x:.2f}' for x in dados_float]}")
    print(f"   Bucket sorted:   {[f'{x:.2f}' for x in bucket_sort(dados_float)]}")
    print(f"   Inteiros:        {dados_int}")
    print(f"   Bucket sorted:   {bucket_sort_inteiros(dados_int)}")
    print()

def algoritmos_busca_avancados():
    """
    Implementa algoritmos de busca especializados.
    """
    print("=== ALGORITMOS DE BUSCA AVANÇADOS ===")
    print()
    
    print("1. BUSCA INTERPOLADA - O(log log n) médio:")
    print("   → Melhora busca binária para dados uniformemente distribuídos")
    print("   → Estima posição baseada no valor")
    print("   → Pode degradar para O(n) no pior caso")
    print()
    
    def busca_interpolada(lista, item):
        """
        Busca interpolada para listas ordenadas com distribuição uniforme.
        """
        esquerda, direita = 0, len(lista) - 1
        
        while esquerda <= direita and item >= lista[esquerda] and item <= lista[direita]:
            # Se só há um elemento
            if esquerda == direita:
                return esquerda if lista[esquerda] == item else -1
            
            # Calcular posição interpolada
            pos = esquerda + int(
                ((item - lista[esquerda]) / (lista[direita] - lista[esquerda])) 
                * (direita - esquerda)
            )
            
            # Garantir que pos está no range válido
            pos = max(esquerda, min(pos, direita))
            
            if lista[pos] == item:
                return pos
            elif lista[pos] < item:
                esquerda = pos + 1
            else:
                direita = pos - 1
        
        return -1
    
    def comparar_busca_interpolada_binaria():
        """Compara performance entre busca interpolada e binária"""
        # Gerar dados uniformemente distribuídos
        dados = list(range(1, 10001, 2))  # 1, 3, 5, ..., 9999
        item_busca = 5001
        
        # Contar comparações
        class ContadorComparacoes:
            def __init__(self):
                self.count = 0
            
            def compare(self, a, b, op):
                self.count += 1
                if op == '==':
                    return a == b
                elif op == '<':
                    return a < b
                elif op == '<=':
                    return a <= b
                elif op == '>':
                    return a > b
                elif op == '>=':
                    return a >= b
        
        def busca_binaria_com_contador(lista, item, contador):
            esquerda, direita = 0, len(lista) - 1
            
            while esquerda <= direita:
                meio = (esquerda + direita) // 2
                
                if contador.compare(lista[meio], item, '=='):
                    return meio
                elif contador.compare(lista[meio], item, '<'):
                    esquerda = meio + 1
                else:
                    direita = meio - 1
            
            return -1
        
        def busca_interpolada_com_contador(lista, item, contador):
            esquerda, direita = 0, len(lista) - 1
            
            while (esquerda <= direita and 
                   contador.compare(item, lista[esquerda], '>=') and 
                   contador.compare(item, lista[direita], '<=')):
                
                if contador.compare(esquerda, direita, '=='):
                    return esquerda if contador.compare(lista[esquerda], item, '==') else -1
                
                pos = esquerda + int(
                    ((item - lista[esquerda]) / (lista[direita] - lista[esquerda])) 
                    * (direita - esquerda)
                )
                pos = max(esquerda, min(pos, direita))
                
                if contador.compare(lista[pos], item, '=='):
                    return pos
                elif contador.compare(lista[pos], item, '<'):
                    esquerda = pos + 1
                else:
                    direita = pos - 1
            
            return -1
        
        # Testar busca binária
        contador_bin = ContadorComparacoes()
        pos_bin = busca_binaria_com_contador(dados, item_busca, contador_bin)
        
        # Testar busca interpolada
        contador_int = ContadorComparacoes()
        pos_int = busca_interpolada_com_contador(dados, item_busca, contador_int)
        
        print(f"   Buscando {item_busca} em lista de {len(dados)} elementos:")
        print(f"   → Busca binária:     {contador_bin.count} comparações")
        print(f"   → Busca interpolada: {contador_int.count} comparações")
        print(f"   → Melhoria:          {contador_bin.count / contador_int.count:.1f}x")
        print()
    
    comparar_busca_interpolada_binaria()
    
    print("2. BUSCA EXPONENCIAL - O(log n):")
    print("   → Útil quando não sabemos o tamanho da lista")
    print("   → Encontra range e depois usa busca binária")
    print("   → Eficiente para listas muito grandes")
    print()
    
    def busca_exponencial(lista, item):
        """
        Busca exponencial para listas ordenadas de tamanho desconhecido.
        """
        if not lista:
            return -1
        
        if lista[0] == item:
            return 0
        
        # Encontrar range onde o elemento pode estar
        i = 1
        while i < len(lista) and lista[i] <= item:
            i *= 2
        
        # Busca binária no range encontrado
        esquerda = i // 2
        direita = min(i, len(lista) - 1)
        
        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            
            if lista[meio] == item:
                return meio
            elif lista[meio] < item:
                esquerda = meio + 1
            else:
                direita = meio - 1
        
        return -1
    
    # Demonstração
    dados_grandes = list(range(0, 100000, 7))  # 0, 7, 14, ..., 99995
    item_teste = 49007
    
    pos = busca_exponencial(dados_grandes, item_teste)
    print(f"   Buscando {item_teste} em lista de {len(dados_grandes)} elementos")
    print(f"   → Posição encontrada: {pos}")
    print(f"   → Valor na posição:   {dados_grandes[pos] if pos != -1 else 'Não encontrado'}")
    print()
    
    print("3. BUSCA TERNÁRIA - O(log₃ n):")
    print("   → Divide em 3 partes ao invés de 2")
    print("   → Teoricamente menos comparações")
    print("   → Na prática, pode ser mais lenta devido ao overhead")
    print()
    
    def busca_ternaria(lista, item):
        """
        Busca ternária - divide lista em 3 partes.
        """
        esquerda, direita = 0, len(lista) - 1
        
        while esquerda <= direita:
            # Dois pontos de divisão
            meio1 = esquerda + (direita - esquerda) // 3
            meio2 = direita - (direita - esquerda) // 3
            
            if lista[meio1] == item:
                return meio1
            elif lista[meio2] == item:
                return meio2
            elif item < lista[meio1]:
                direita = meio1 - 1
            elif item > lista[meio2]:
                esquerda = meio2 + 1
            else:
                esquerda = meio1 + 1
                direita = meio2 - 1
        
        return -1
    
    # Comparar busca binária vs ternária
    def comparar_busca_binaria_ternaria():
        dados = list(range(1000))
        item = 567
        
        # Contar comparações
        class Contador:
            def __init__(self):
                self.count = 0
        
        def busca_binaria_contador(lista, item, contador):
            esquerda, direita = 0, len(lista) - 1
            
            while esquerda <= direita:
                contador.count += 1
                meio = (esquerda + direita) // 2
                
                if lista[meio] == item:
                    return meio
                elif lista[meio] < item:
                    esquerda = meio + 1
                else:
                    direita = meio - 1
            
            return -1
        
        def busca_ternaria_contador(lista, item, contador):
            esquerda, direita = 0, len(lista) - 1
            
            while esquerda <= direita:
                contador.count += 2  # Duas comparações por iteração
                meio1 = esquerda + (direita - esquerda) // 3
                meio2 = direita - (direita - esquerda) // 3
                
                if lista[meio1] == item:
                    return meio1
                elif lista[meio2] == item:
                    return meio2
                elif item < lista[meio1]:
                    direita = meio1 - 1
                elif item > lista[meio2]:
                    esquerda = meio2 + 1
                else:
                    esquerda = meio1 + 1
                    direita = meio2 - 1
            
            return -1
        
        contador_bin = Contador()
        contador_ter = Contador()
        
        pos_bin = busca_binaria_contador(dados, item, contador_bin)
        pos_ter = busca_ternaria_contador(dados, item, contador_ter)
        
        print(f"   Comparação de comparações:")
        print(f"   → Busca binária:  {contador_bin.count} comparações")
        print(f"   → Busca ternária: {contador_ter.count} comparações")
        print(f"   → Diferença:      {contador_ter.count - contador_bin.count}")
        print()
    
    comparar_busca_binaria_ternaria()

def algoritmos_busca_strings():
    """
    Implementa algoritmos especializados para busca em strings.
    """
    print("=== ALGORITMOS DE BUSCA EM STRINGS ===")
    print()
    
    print("1. ALGORITMO KMP (Knuth-Morris-Pratt) - O(n + m):")
    print("   → Evita re-comparações desnecessárias")
    print("   → Usa tabela de falhas (failure function)")
    print("   → Ótimo para padrões com repetições")
    print()
    
    def kmp_search(texto, padrao):
        """
        Busca KMP para encontrar todas as ocorrências de um padrão.
        """
        def construir_tabela_falhas(padrao):
            """Constrói tabela de falhas para KMP"""
            tabela = [0] * len(padrao)
            j = 0
            
            for i in range(1, len(padrao)):
                while j > 0 and padrao[i] != padrao[j]:
                    j = tabela[j - 1]
                
                if padrao[i] == padrao[j]:
                    j += 1
                
                tabela[i] = j
            
            return tabela
        
        if not padrao:
            return []
        
        tabela_falhas = construir_tabela_falhas(padrao)
        ocorrencias = []
        j = 0  # índice para padrão
        
        for i in range(len(texto)):  # índice para texto
            while j > 0 and texto[i] != padrao[j]:
                j = tabela_falhas[j - 1]
            
            if texto[i] == padrao[j]:
                j += 1
            
            if j == len(padrao):
                ocorrencias.append(i - j + 1)
                j = tabela_falhas[j - 1]
        
        return ocorrencias
    
    # Demonstração
    texto_exemplo = "ABABDABACDABABCABCABCABCABC"
    padrao_exemplo = "ABABCABC"
    
    ocorrencias = kmp_search(texto_exemplo, padrao_exemplo)
    print(f"   Texto:  {texto_exemplo}")
    print(f"   Padrão: {padrao_exemplo}")
    print(f"   Ocorrências nas posições: {ocorrencias}")
    
    # Mostrar onde estão as ocorrências
    for pos in ocorrencias:
        print(f"   Posição {pos:2d}: {texto_exemplo[pos:pos+len(padrao_exemplo)]}")
    print()
    
    print("2. ALGORITMO BOYER-MOORE - O(n/m) melhor caso:")
    print("   → Busca da direita para esquerda no padrão")
    print("   → Usa heurística do caractere ruim")
    print("   → Muito eficiente para textos longos")
    print()
    
    def boyer_moore_search(texto, padrao):
        """
        Implementação simplificada do Boyer-Moore.
        """
        def construir_tabela_caractere_ruim(padrao):
            """Constrói tabela de caracteres ruins"""
            tabela = {}
            for i in range(len(padrao)):
                tabela[padrao[i]] = i
            return tabela
        
        if not padrao:
            return []
        
        tabela_ruim = construir_tabela_caractere_ruim(padrao)
        ocorrencias = []
        i = 0  # posição no texto
        
        while i <= len(texto) - len(padrao):
            j = len(padrao) - 1  # começar do final do padrão
            
            # Comparar da direita para esquerda
            while j >= 0 and padrao[j] == texto[i + j]:
                j -= 1
            
            if j < 0:  # padrão encontrado
                ocorrencias.append(i)
                i += 1
            else:
                # Calcular deslocamento baseado no caractere ruim
                char_ruim = texto[i + j]
                if char_ruim in tabela_ruim:
                    deslocamento = max(1, j - tabela_ruim[char_ruim])
                else:
                    deslocamento = j + 1
                i += deslocamento
        
        return ocorrencias
    
    # Demonstração
    ocorrencias_bm = boyer_moore_search(texto_exemplo, padrao_exemplo)
    print(f"   Boyer-Moore encontrou: {ocorrencias_bm}")
    print()
    
    print("3. ALGORITMO RABIN-KARP - O(n + m) médio:")
    print("   → Usa hashing para comparação rápida")
    print("   → Rolling hash para eficiência")
    print("   → Bom para múltiplos padrões")
    print()
    
    def rabin_karp_search(texto, padrao, base=256, primo=101):
        """
        Busca Rabin-Karp usando rolling hash.
        """
        if not padrao or len(padrao) > len(texto):
            return []
        
        m, n = len(padrao), len(texto)
        ocorrencias = []
        
        # Calcular hash do padrão
        hash_padrao = 0
        hash_texto = 0
        h = 1
        
        # Valor de h = base^(m-1) % primo
        for i in range(m - 1):
            h = (h * base) % primo
        
        # Calcular hash inicial do padrão e primeira janela do texto
        for i in range(m):
            hash_padrao = (base * hash_padrao + ord(padrao[i])) % primo
            hash_texto = (base * hash_texto + ord(texto[i])) % primo
        
        # Deslizar janela sobre o texto
        for i in range(n - m + 1):
            # Se hashes coincidem, verificar caractere por caractere
            if hash_padrao == hash_texto:
                if texto[i:i + m] == padrao:
                    ocorrencias.append(i)
            
            # Calcular hash da próxima janela (rolling hash)
            if i < n - m:
                hash_texto = (base * (hash_texto - ord(texto[i]) * h) + ord(texto[i + m])) % primo
                
                # Garantir que hash seja positivo
                if hash_texto < 0:
                    hash_texto += primo
        
        return ocorrencias
    
    # Demonstração
    ocorrencias_rk = rabin_karp_search(texto_exemplo, padrao_exemplo)
    print(f"   Rabin-Karp encontrou: {ocorrencias_rk}")
    print()
    
    print("4. COMPARAÇÃO DE PERFORMANCE:")
    
    def comparar_algoritmos_string():
        """Compara performance dos algoritmos de busca em string"""
        import time
        
        # Gerar texto grande
        texto_grande = "ABCD" * 10000 + "ABABCABC" + "EFGH" * 10000
        padrao_busca = "ABABCABC"
        
        algoritmos = [
            ("Busca Ingênua", lambda t, p: busca_ingenua_string(t, p)),
            ("KMP", kmp_search),
            ("Boyer-Moore", boyer_moore_search),
            ("Rabin-Karp", rabin_karp_search)
        ]
        
        def busca_ingenua_string(texto, padrao):
            """Busca ingênua para comparação"""
            ocorrencias = []
            for i in range(len(texto) - len(padrao) + 1):
                if texto[i:i + len(padrao)] == padrao:
                    ocorrencias.append(i)
            return ocorrencias
        
        print("   Performance em texto de ~240KB:")
        print("   ┌─────────────────┬─────────────┬─────────────┐")
        print("   │   ALGORITMO     │    TEMPO    │  SPEEDUP    │")
        print("   ├─────────────────┼─────────────┼─────────────┤")
        
        tempos = {}
        for nome, algoritmo in algoritmos:
            start = time.perf_counter()
            resultado = algoritmo(texto_grande, padrao_busca)
            end = time.perf_counter()
            
            tempo = end - start
            tempos[nome] = tempo
            
            print(f"   │ {nome:15} │ {tempo*1000:9.3f} ms │", end="")
            if nome == "Busca Ingênua":
                print(f" {'1.00x':9} │")
            else:
                speedup = tempos["Busca Ingênua"] / tempo
                print(f" {speedup:9.2f}x │")
        
        print("   └─────────────────┴─────────────┴─────────────┘")
        print()
    
    comparar_algoritmos_string()

def algoritmos_aproximados():
    """
    Implementa algoritmos de busca aproximada e fuzzy matching.
    """
    print("=== ALGORITMOS DE BUSCA APROXIMADA ===")
    print()
    
    print("1. DISTÂNCIA DE LEVENSHTEIN:")
    print("   → Mede diferença entre duas strings")
    print("   → Número mínimo de edições (inserção, remoção, substituição)")
    print("   → Base para fuzzy matching")
    print()
    
    def distancia_levenshtein(s1, s2):
        """
        Calcula distância de Levenshtein entre duas strings.
        """
        m, n = len(s1), len(s2)
        
        # Criar matriz DP
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Inicializar primeira linha e coluna
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Preencher matriz
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # remoção
                        dp[i][j - 1],      # inserção
                        dp[i - 1][j - 1]   # substituição
                    )
        
        return dp[m][n]
    
    def distancia_levenshtein_otimizada(s1, s2):
        """
        Versão otimizada em espaço O(min(m,n)).
        """
        # Garantir que s1 seja a string menor
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        
        m, n = len(s1), len(s2)
        
        # Usar apenas duas linhas
        prev = list(range(m + 1))
        curr = [0] * (m + 1)
        
        for j in range(1, n + 1):
            curr[0] = j
            
            for i in range(1, m + 1):
                if s1[i - 1] == s2[j - 1]:
                    curr[i] = prev[i - 1]
                else:
                    curr[i] = 1 + min(prev[i], curr[i - 1], prev[i - 1])
            
            prev, curr = curr, prev
        
        return prev[m]
    
    # Demonstração
    exemplos = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("python", "java"),
        ("algoritmo", "logaritmo")
    ]
    
    print("   Exemplos de distância de Levenshtein:")
    for s1, s2 in exemplos:
        dist = distancia_levenshtein(s1, s2)
        print(f"   → '{s1}' ↔ '{s2}': {dist}")
    print()
    
    print("2. BUSCA FUZZY:")
    print("   → Encontra strings similares dentro de um threshold")
    print("   → Útil para correção ortográfica e busca tolerante a erros")
    print()
    
    def busca_fuzzy(texto, padrao, max_distancia=2):
        """
        Busca fuzzy usando distância de Levenshtein.
        """
        palavras = texto.split()
        matches = []
        
        for i, palavra in enumerate(palavras):
            distancia = distancia_levenshtein_otimizada(palavra.lower(), padrao.lower())
            if distancia <= max_distancia:
                matches.append({
                    'palavra': palavra,
                    'posicao': i,
                    'distancia': distancia,
                    'similaridade': 1 - distancia / max(len(palavra), len(padrao))
                })
        
        # Ordenar por similaridade
        matches.sort(key=lambda x: x['distancia'])
        return matches
    
    # Demonstração
    texto_busca = """
    Python é uma linguagem de programação poderosa e versátil.
    Muitos programadores escolhem Pyton para desenvolvimento web.
    A sintaxe do Python é clara e legível.
    Pythn é usado em ciência de dados e inteligência artificial.
    """
    
    padrao_fuzzy = "Python"
    matches = busca_fuzzy(texto_busca, padrao_fuzzy, max_distancia=2)
    
    print(f"   Buscando '{padrao_fuzzy}' com tolerância de 2 erros:")
    for match in matches:
        print(f"   → '{match['palavra']}' (distância: {match['distancia']}, "
              f"similaridade: {match['similaridade']:.2f})")
    print()
    
    print("3. ALGORITMO DE WAGNER-FISCHER ESTENDIDO:")
    print("   → Permite diferentes custos para operações")
    print("   → Mais flexível que Levenshtein básico")
    print()
    
    def distancia_wagner_fischer(s1, s2, custo_ins=1, custo_del=1, custo_sub=1):
        """
        Algoritmo Wagner-Fischer com custos personalizados.
        """
        m, n = len(s1), len(s2)
        
        # Matriz DP
        dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]
        
        # Inicialização
        dp[0][0] = 0
        for i in range(1, m + 1):
            dp[i][0] = dp[i - 1][0] + custo_del
        for j in range(1, n + 1):
            dp[0][j] = dp[0][j - 1] + custo_ins
        
        # Preenchimento
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(
                        dp[i - 1][j] + custo_del,      # deleção
                        dp[i][j - 1] + custo_ins,      # inserção
                        dp[i - 1][j - 1] + custo_sub   # substituição
                    )
        
        return dp[m][n]
    
    # Demonstração com custos diferentes
    s1, s2 = "algorithm", "logarithm"
    
    dist_normal = distancia_wagner_fischer(s1, s2)
    dist_sub_cara = distancia_wagner_fischer(s1, s2, custo_sub=2)
    dist_ins_cara = distancia_wagner_fischer(s1, s2, custo_ins=2)
    
    print(f"   Comparando '{s1}' e '{s2}':")
    print(f"   → Custos iguais (1,1,1):     {dist_normal}")
    print(f"   → Substituição cara (1,1,2): {dist_sub_cara}")
    print(f"   → Inserção cara (2,1,1):     {dist_ins_cara}")
    print()

if __name__ == "__main__":
    print("MÓDULO 3.7 - ALGORITMOS ESPECIALIZADOS")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    algoritmos_ordenacao_nao_comparativa()
    print("\n" + "="*50 + "\n")
    
    algoritmos_busca_avancados()
    print("\n" + "="*50 + "\n")
    
    algoritmos_busca_strings()
    print("\n" + "="*50 + "\n")
    
    algoritmos_aproximados()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 3.7 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Counting Sort, Radix Sort, Bucket Sort")
    print("✅ Busca interpolada e exponencial")
    print("✅ Algoritmos KMP, Boyer-Moore, Rabin-Karp")
    print("✅ Distância de Levenshtein e busca fuzzy")
    print("✅ Algoritmos não-comparativos O(n)")
    print("✅ Busca em strings com padrões complexos")
    print("✅ Algoritmos aproximados e tolerantes a erros")
    print("✅ Otimizações específicas por domínio")
    print("✅ Análise comparativa de performance")
    print("\n➡️  Próximo: Módulo 3.8 - Algoritmos Paralelos e Distribuídos")