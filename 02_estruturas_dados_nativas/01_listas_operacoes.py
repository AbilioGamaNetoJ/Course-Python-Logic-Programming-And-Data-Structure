"""
Módulo: Listas e Operações
Tópico: Estruturas de Dados Nativas
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico a Intermediário

Objetivos de Aprendizado:
- Compreender listas como estruturas de dados dinâmicas
- Dominar operações básicas e avançadas com listas
- Analisar performance de diferentes operações
- Implementar algoritmos de manipulação de listas
- Visualizar estruturas de dados em ASCII
- Comparar eficiência de métodos alternativos

Conceitos Abordados:
- Criação e inicialização de listas
- Indexação e fatiamento (slicing)
- Métodos de inserção, remoção e busca
- List comprehensions
- Listas aninhadas (matrizes)
- Operações de ordenação e reversão
- Análise de performance O(1), O(n), O(n log n)
- Visualização ASCII de estruturas

Pré-requisitos:
- Módulo 01 completo (especialmente funções e loops)
- Conhecimento de tipos de dados básicos
- Compreensão de indexação

Complexidade Temporal: 
- Acesso: O(1)
- Busca: O(n)
- Inserção: O(1) no final, O(n) no meio
- Remoção: O(1) no final, O(n) no meio

Complexidade Espacial: O(n) onde n é o número de elementos
"""

import time
import random

def conceito_listas():
    """
    Introduz o conceito fundamental de listas.
    
    Analogia: Listas são como prateleiras numeradas numa biblioteca.
    Cada livro (elemento) tem uma posição específica (índice),
    e você pode adicionar, remover ou reorganizar os livros.
    """
    print("=== CONCEITO DE LISTAS ===")
    print()
    
    print("1. O QUE SÃO LISTAS?")
    print("   → Estruturas de dados ordenadas e mutáveis")
    print("   → Podem conter elementos de diferentes tipos")
    print("   → Indexadas a partir de 0")
    print("   → Tamanho dinâmico (cresce/diminui conforme necessário)")
    print("   → Uma das estruturas mais versáteis do Python")
    print()
    
    print("2. ANALOGIAS DO COTIDIANO:")
    print("   📚 Prateleira de livros numerada")
    print("   🚂 Vagões de trem em sequência")
    print("   📝 Lista de compras ordenada")
    print("   🎵 Playlist de músicas")
    print("   🏠 Casas numeradas numa rua")
    print()
    
    print("3. VISUALIZAÇÃO ASCII DE UMA LISTA:")
    lista_exemplo = ['A', 'B', 'C', 'D', 'E']
    print("   Lista: ['A', 'B', 'C', 'D', 'E']")
    print()
    print("   ┌───┬───┬───┬───┬───┐")
    print("   │ A │ B │ C │ D │ E │")
    print("   └───┴───┴───┴───┴───┘")
    print("     0   1   2   3   4   ← Índices")
    print("    -5  -4  -3  -2  -1   ← Índices negativos")
    print()
    
    print("4. CARACTERÍSTICAS IMPORTANTES:")
    print("   ✅ Ordenada: Mantém a ordem de inserção")
    print("   ✅ Mutável: Pode ser modificada após criação")
    print("   ✅ Permite duplicatas: Mesmo elemento pode aparecer várias vezes")
    print("   ✅ Heterogênea: Pode misturar tipos de dados")
    print("   ✅ Indexável: Acesso direto por posição")
    print()
    
    print("5. EXEMPLO PRÁTICO:")
    print("   # Criando uma lista")
    print("   frutas = ['maçã', 'banana', 'laranja']")
    print("   print(f'Lista: {frutas}')")
    print("   print(f'Primeiro item: {frutas[0]}')")
    print("   print(f'Último item: {frutas[-1]}')")
    print("   print(f'Tamanho: {len(frutas)}')")
    print()
    
    # Executando o exemplo
    frutas = ['maçã', 'banana', 'laranja']
    print("   RESULTADO:")
    print(f"   → Lista: {frutas}")
    print(f"   → Primeiro item: {frutas[0]}")
    print(f"   → Último item: {frutas[-1]}")
    print(f"   → Tamanho: {len(frutas)}")
    print()

def criacao_inicializacao():
    """
    Explora diferentes formas de criar e inicializar listas.
    
    Analogia: Criar listas é como preparar diferentes tipos de recipientes.
    Alguns vazios, outros com conteúdo inicial, alguns com padrões específicos.
    """
    print("=== CRIAÇÃO E INICIALIZAÇÃO DE LISTAS ===")
    print()
    
    print("1. LISTA VAZIA:")
    print("   lista_vazia1 = []")
    print("   lista_vazia2 = list()")
    print()
    lista_vazia1 = []
    lista_vazia2 = list()
    print(f"   → lista_vazia1: {lista_vazia1}")
    print(f"   → lista_vazia2: {lista_vazia2}")
    print()
    
    print("2. LISTA COM ELEMENTOS INICIAIS:")
    print("   numeros = [1, 2, 3, 4, 5]")
    print("   cores = ['vermelho', 'azul', 'verde']")
    print("   mista = [1, 'texto', 3.14, True, None]")
    print()
    numeros = [1, 2, 3, 4, 5]
    cores = ['vermelho', 'azul', 'verde']
    mista = [1, 'texto', 3.14, True, None]
    print(f"   → numeros: {numeros}")
    print(f"   → cores: {cores}")
    print(f"   → mista: {mista}")
    print()
    
    print("3. LISTA COM REPETIÇÃO:")
    print("   zeros = [0] * 5")
    print("   asteriscos = ['*'] * 10")
    print("   # CUIDADO com objetos mutáveis!")
    print("   listas_vazias = [[] for _ in range(3)]  # ✅ Correto")
    print("   # listas_problema = [[]] * 3  # ❌ Todas referenciam a mesma lista")
    print()
    zeros = [0] * 5
    asteriscos = ['*'] * 10
    listas_vazias = [[] for _ in range(3)]
    print(f"   → zeros: {zeros}")
    print(f"   → asteriscos: {asteriscos}")
    print(f"   → listas_vazias: {listas_vazias}")
    print()
    
    print("4. LISTA A PARTIR DE RANGE:")
    print("   sequencia = list(range(10))")
    print("   pares = list(range(0, 20, 2))")
    print("   decrescente = list(range(10, 0, -1))")
    print()
    sequencia = list(range(10))
    pares = list(range(0, 20, 2))
    decrescente = list(range(10, 0, -1))
    print(f"   → sequencia: {sequencia}")
    print(f"   → pares: {pares}")
    print(f"   → decrescente: {decrescente}")
    print()
    
    print("5. LISTA A PARTIR DE STRING:")
    print("   letras = list('Python')")
    print("   palavras = 'Python é incrível'.split()")
    print("   caracteres = list('ABCDE')")
    print()
    letras = list('Python')
    palavras = 'Python é incrível'.split()
    caracteres = list('ABCDE')
    print(f"   → letras: {letras}")
    print(f"   → palavras: {palavras}")
    print(f"   → caracteres: {caracteres}")
    print()
    
    print("6. LIST COMPREHENSION (CRIAÇÃO AVANÇADA):")
    print("   quadrados = [x**2 for x in range(1, 6)]")
    print("   pares_ate_20 = [x for x in range(21) if x % 2 == 0]")
    print("   maiusculas = [letra.upper() for letra in 'python']")
    print()
    quadrados = [x**2 for x in range(1, 6)]
    pares_ate_20 = [x for x in range(21) if x % 2 == 0]
    maiusculas = [letra.upper() for letra in 'python']
    print(f"   → quadrados: {quadrados}")
    print(f"   → pares_ate_20: {pares_ate_20}")
    print(f"   → maiusculas: {maiusculas}")
    print()

def indexacao_fatiamento():
    """
    Explora indexação e fatiamento (slicing) de listas.
    
    Analogia: Indexação é como endereços de casas numa rua.
    Fatiamento é como selecionar um quarteirão inteiro.
    """
    print("=== INDEXAÇÃO E FATIAMENTO ===")
    print()
    
    # Lista de exemplo
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    print(f"Lista exemplo: {alfabeto}")
    print()
    
    print("1. INDEXAÇÃO BÁSICA:")
    print("   alfabeto[0]   # Primeiro elemento")
    print("   alfabeto[4]   # Quinto elemento")
    print("   alfabeto[-1]  # Último elemento")
    print("   alfabeto[-3]  # Terceiro elemento do final")
    print()
    print("   RESULTADO:")
    print(f"   → alfabeto[0] = '{alfabeto[0]}'")
    print(f"   → alfabeto[4] = '{alfabeto[4]}'")
    print(f"   → alfabeto[-1] = '{alfabeto[-1]}'")
    print(f"   → alfabeto[-3] = '{alfabeto[-3]}'")
    print()
    
    print("2. VISUALIZAÇÃO DE ÍNDICES:")
    print("   Lista:", end="  ")
    for i, letra in enumerate(alfabeto):
        print(f"{letra:>3}", end="")
    print()
    print("   Índice:", end=" ")
    for i in range(len(alfabeto)):
        print(f"{i:>3}", end="")
    print()
    print("   Negativo:", end="")
    for i in range(len(alfabeto)):
        print(f"{i-len(alfabeto):>3}", end="")
    print()
    print()
    
    print("3. FATIAMENTO BÁSICO [início:fim]:")
    print("   alfabeto[1:4]    # Elementos 1, 2, 3 (4 não incluído)")
    print("   alfabeto[0:3]    # Primeiros 3 elementos")
    print("   alfabeto[5:8]    # Elementos do meio")
    print("   alfabeto[7:]     # Do índice 7 até o final")
    print("   alfabeto[:5]     # Do início até o índice 4")
    print()
    print("   RESULTADO:")
    print(f"   → alfabeto[1:4] = {alfabeto[1:4]}")
    print(f"   → alfabeto[0:3] = {alfabeto[0:3]}")
    print(f"   → alfabeto[5:8] = {alfabeto[5:8]}")
    print(f"   → alfabeto[7:] = {alfabeto[7:]}")
    print(f"   → alfabeto[:5] = {alfabeto[:5]}")
    print()
    
    print("4. FATIAMENTO COM PASSO [início:fim:passo]:")
    print("   alfabeto[::2]    # Todos os elementos, pulando de 2 em 2")
    print("   alfabeto[1::2]   # A partir do índice 1, pulando de 2 em 2")
    print("   alfabeto[::-1]   # Todos os elementos em ordem reversa")
    print("   alfabeto[2:8:2]  # Do índice 2 ao 7, pulando de 2 em 2")
    print()
    print("   RESULTADO:")
    print(f"   → alfabeto[::2] = {alfabeto[::2]}")
    print(f"   → alfabeto[1::2] = {alfabeto[1::2]}")
    print(f"   → alfabeto[::-1] = {alfabeto[::-1]}")
    print(f"   → alfabeto[2:8:2] = {alfabeto[2:8:2]}")
    print()
    
    print("5. FATIAMENTO COM ÍNDICES NEGATIVOS:")
    print("   alfabeto[-5:]    # Últimos 5 elementos")
    print("   alfabeto[:-3]    # Todos exceto os últimos 3")
    print("   alfabeto[-8:-2]  # Do 8º do final até o 3º do final")
    print("   alfabeto[-1::-1] # Do último para o primeiro")
    print()
    print("   RESULTADO:")
    print(f"   → alfabeto[-5:] = {alfabeto[-5:]}")
    print(f"   → alfabeto[:-3] = {alfabeto[:-3]}")
    print(f"   → alfabeto[-8:-2] = {alfabeto[-8:-2]}")
    print(f"   → alfabeto[-1::-1] = {alfabeto[-1::-1]}")
    print()
    
    print("6. CASOS ESPECIAIS E DICAS:")
    print("   alfabeto[:]      # Cópia completa da lista")
    print("   alfabeto[100:]   # Índice além do limite (retorna lista vazia)")
    print("   alfabeto[-100:]  # Índice negativo além do limite (retorna lista completa)")
    print()
    print("   RESULTADO:")
    print(f"   → alfabeto[:] = {alfabeto[:]}")
    print(f"   → alfabeto[100:] = {alfabeto[100:]}")
    print(f"   → alfabeto[-100:] = {alfabeto[-100:]}")
    print()

def operacoes_basicas():
    """
    Explora operações básicas de manipulação de listas.
    
    Analogia: Operações básicas são como ações numa biblioteca:
    adicionar livros, remover, procurar, reorganizar.
    """
    print("=== OPERAÇÕES BÁSICAS COM LISTAS ===")
    print()
    
    print("1. ADICIONANDO ELEMENTOS:")
    lista = ['A', 'B', 'C']
    print(f"   Lista inicial: {lista}")
    print()
    
    print("   # append() - Adiciona no final (O(1))")
    print("   lista.append('D')")
    lista.append('D')
    print(f"   → Após append: {lista}")
    print()
    
    print("   # insert() - Adiciona em posição específica (O(n))")
    print("   lista.insert(1, 'X')")
    lista.insert(1, 'X')
    print(f"   → Após insert: {lista}")
    print()
    
    print("   # extend() - Adiciona múltiplos elementos (O(k))")
    print("   lista.extend(['Y', 'Z'])")
    lista.extend(['Y', 'Z'])
    print(f"   → Após extend: {lista}")
    print()
    
    print("2. REMOVENDO ELEMENTOS:")
    print(f"   Lista atual: {lista}")
    print()
    
    print("   # remove() - Remove primeira ocorrência (O(n))")
    print("   lista.remove('X')")
    lista.remove('X')
    print(f"   → Após remove: {lista}")
    print()
    
    print("   # pop() - Remove e retorna elemento (O(1) no final, O(n) no meio)")
    print("   elemento = lista.pop()")
    elemento = lista.pop()
    print(f"   → Elemento removido: '{elemento}'")
    print(f"   → Lista após pop: {lista}")
    print()
    
    print("   # pop(índice) - Remove elemento específico")
    print("   elemento = lista.pop(1)")
    elemento = lista.pop(1)
    print(f"   → Elemento removido: '{elemento}'")
    print(f"   → Lista após pop(1): {lista}")
    print()
    
    print("   # del - Remove por índice ou fatia")
    print("   del lista[0]")
    del lista[0]
    print(f"   → Após del lista[0]: {lista}")
    print()
    
    print("   # clear() - Remove todos os elementos (O(n))")
    lista_temp = lista.copy()
    print("   lista_temp.clear()")
    lista_temp.clear()
    print(f"   → Após clear: {lista_temp}")
    print()
    
    print("3. BUSCANDO ELEMENTOS:")
    numeros = [10, 20, 30, 20, 40, 20, 50]
    print(f"   Lista: {numeros}")
    print()
    
    print("   # index() - Encontra índice da primeira ocorrência (O(n))")
    print("   indice = numeros.index(20)")
    indice = numeros.index(20)
    print(f"   → Índice de 20: {indice}")
    print()
    
    print("   # count() - Conta ocorrências (O(n))")
    print("   quantidade = numeros.count(20)")
    quantidade = numeros.count(20)
    print(f"   → Quantidade de 20: {quantidade}")
    print()
    
    print("   # in - Verifica se elemento existe (O(n))")
    print("   existe_30 = 30 in numeros")
    print("   existe_100 = 100 in numeros")
    existe_30 = 30 in numeros
    existe_100 = 100 in numeros
    print(f"   → 30 está na lista: {existe_30}")
    print(f"   → 100 está na lista: {existe_100}")
    print()
    
    print("4. OUTRAS OPERAÇÕES ÚTEIS:")
    lista_exemplo = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"   Lista: {lista_exemplo}")
    print()
    
    print("   # len() - Tamanho da lista (O(1))")
    print(f"   → Tamanho: {len(lista_exemplo)}")
    print()
    
    print("   # min() e max() - Menor e maior elemento (O(n))")
    print(f"   → Menor: {min(lista_exemplo)}")
    print(f"   → Maior: {max(lista_exemplo)}")
    print()
    
    print("   # sum() - Soma dos elementos (O(n))")
    print(f"   → Soma: {sum(lista_exemplo)}")
    print()
    
    print("   # sorted() - Retorna lista ordenada (O(n log n))")
    print(f"   → Ordenada: {sorted(lista_exemplo)}")
    print(f"   → Original: {lista_exemplo}")  # Não modifica a original
    print()
    
    print("   # reverse() - Inverte a lista in-place (O(n))")
    lista_exemplo.reverse()
    print(f"   → Após reverse: {lista_exemplo}")
    print()
    
    print("   # sort() - Ordena a lista in-place (O(n log n))")
    lista_exemplo.sort()
    print(f"   → Após sort: {lista_exemplo}")
    print()

def list_comprehensions():
    """
    Explora list comprehensions - forma pythônica de criar listas.
    
    Analogia: List comprehensions são como filtros e transformadores numa fábrica.
    Você pega matéria-prima, aplica regras e produz uma nova lista.
    """
    print("=== LIST COMPREHENSIONS ===")
    print()
    
    print("1. SINTAXE BÁSICA:")
    print("   [expressão for item in iterável]")
    print("   [expressão for item in iterável if condição]")
    print()
    
    print("2. EXEMPLO SIMPLES - QUADRADOS:")
    print("   # Forma tradicional")
    print("   quadrados_tradicional = []")
    print("   for x in range(1, 6):")
    print("       quadrados_tradicional.append(x**2)")
    print()
    print("   # List comprehension")
    print("   quadrados_lc = [x**2 for x in range(1, 6)]")
    print()
    
    quadrados_tradicional = []
    for x in range(1, 6):
        quadrados_tradicional.append(x**2)
    
    quadrados_lc = [x**2 for x in range(1, 6)]
    
    print("   RESULTADO:")
    print(f"   → Tradicional: {quadrados_tradicional}")
    print(f"   → List comprehension: {quadrados_lc}")
    print()
    
    print("3. COM CONDIÇÕES (FILTROS):")
    print("   # Números pares de 0 a 20")
    print("   pares = [x for x in range(21) if x % 2 == 0]")
    pares = [x for x in range(21) if x % 2 == 0]
    print(f"   → Pares: {pares}")
    print()
    
    print("   # Palavras com mais de 4 letras")
    print("   palavras = ['Python', 'é', 'uma', 'linguagem', 'incrível']")
    print("   palavras_longas = [p for p in palavras if len(p) > 4]")
    palavras = ['Python', 'é', 'uma', 'linguagem', 'incrível']
    palavras_longas = [p for p in palavras if len(p) > 4]
    print(f"   → Palavras longas: {palavras_longas}")
    print()
    
    print("4. TRANSFORMAÇÕES:")
    print("   # Converter para maiúsculas")
    print("   nomes = ['ana', 'bruno', 'carlos']")
    print("   nomes_maiusc = [nome.upper() for nome in nomes]")
    nomes = ['ana', 'bruno', 'carlos']
    nomes_maiusc = [nome.upper() for nome in nomes]
    print(f"   → Maiúsculas: {nomes_maiusc}")
    print()
    
    print("   # Calcular comprimentos")
    print("   comprimentos = [len(nome) for nome in nomes]")
    comprimentos = [len(nome) for nome in nomes]
    print(f"   → Comprimentos: {comprimentos}")
    print()
    
    print("5. LIST COMPREHENSIONS ANINHADAS:")
    print("   # Matriz 3x3")
    print("   matriz = [[i*3 + j for j in range(3)] for i in range(3)]")
    matriz = [[i*3 + j for j in range(3)] for i in range(3)]
    print("   → Matriz:")
    for linha in matriz:
        print(f"     {linha}")
    print()
    
    print("   # Achatar uma matriz")
    print("   matriz_exemplo = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]")
    print("   achatada = [item for linha in matriz_exemplo for item in linha]")
    matriz_exemplo = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    achatada = [item for linha in matriz_exemplo for item in linha]
    print(f"   → Achatada: {achatada}")
    print()
    
    print("6. CONDIÇÕES COMPLEXAS:")
    print("   # Números que são pares E maiores que 10")
    print("   numeros = range(1, 21)")
    print("   pares_grandes = [x for x in numeros if x % 2 == 0 and x > 10]")
    numeros = range(1, 21)
    pares_grandes = [x for x in numeros if x % 2 == 0 and x > 10]
    print(f"   → Pares > 10: {pares_grandes}")
    print()
    
    print("   # Expressão condicional (if-else)")
    print("   numeros = [1, 2, 3, 4, 5]")
    print("   par_impar = ['par' if x % 2 == 0 else 'ímpar' for x in numeros]")
    numeros = [1, 2, 3, 4, 5]
    par_impar = ['par' if x % 2 == 0 else 'ímpar' for x in numeros]
    print(f"   → Classificação: {par_impar}")
    print()
    
    print("7. PERFORMANCE - COMPARAÇÃO:")
    print("   # Testando performance com 100.000 elementos")
    
    def teste_tradicional():
        resultado = []
        for x in range(100000):
            if x % 2 == 0:
                resultado.append(x**2)
        return resultado
    
    def teste_list_comprehension():
        return [x**2 for x in range(100000) if x % 2 == 0]
    
    # Medindo tempo
    start = time.time()
    lista1 = teste_tradicional()
    tempo1 = time.time() - start
    
    start = time.time()
    lista2 = teste_list_comprehension()
    tempo2 = time.time() - start
    
    print(f"   → Método tradicional: {tempo1:.4f}s")
    print(f"   → List comprehension: {tempo2:.4f}s")
    print(f"   → List comprehension é {tempo1/tempo2:.1f}x mais rápida!")
    print()

def listas_aninhadas():
    """
    Explora listas aninhadas (matrizes) e suas operações.
    
    Analogia: Listas aninhadas são como prédios de apartamentos.
    Cada andar (lista externa) tem vários apartamentos (elementos internos).
    """
    print("=== LISTAS ANINHADAS (MATRIZES) ===")
    print()
    
    print("1. CRIANDO MATRIZES:")
    print("   # Matriz 2x3")
    print("   matriz = [[1, 2, 3], [4, 5, 6]]")
    matriz = [[1, 2, 3], [4, 5, 6]]
    print(f"   → Matriz: {matriz}")
    print()
    
    print("   # Visualização ASCII:")
    print("   ┌─────┬─────┬─────┐")
    for i, linha in enumerate(matriz):
        print("   │", end="")
        for elemento in linha:
            print(f" {elemento:^3} │", end="")
        print()
        if i < len(matriz) - 1:
            print("   ├─────┼─────┼─────┤")
    print("   └─────┴─────┴─────┘")
    print()
    
    print("2. ACESSANDO ELEMENTOS:")
    print("   matriz[0][1]  # Linha 0, Coluna 1")
    print("   matriz[1][2]  # Linha 1, Coluna 2")
    print()
    print("   RESULTADO:")
    print(f"   → matriz[0][1] = {matriz[0][1]}")
    print(f"   → matriz[1][2] = {matriz[1][2]}")
    print()
    
    print("3. CRIANDO MATRIZ COM LIST COMPREHENSION:")
    print("   # Matriz 4x4 com números sequenciais")
    print("   matriz_4x4 = [[i*4 + j + 1 for j in range(4)] for i in range(4)]")
    matriz_4x4 = [[i*4 + j + 1 for j in range(4)] for i in range(4)]
    print("   → Matriz 4x4:")
    for linha in matriz_4x4:
        print(f"     {linha}")
    print()
    
    print("4. OPERAÇÕES COM MATRIZES:")
    print("   # Soma de todos os elementos")
    print("   soma_total = sum(sum(linha) for linha in matriz_4x4)")
    soma_total = sum(sum(linha) for linha in matriz_4x4)
    print(f"   → Soma total: {soma_total}")
    print()
    
    print("   # Encontrar elemento máximo")
    print("   maximo = max(max(linha) for linha in matriz_4x4)")
    maximo = max(max(linha) for linha in matriz_4x4)
    print(f"   → Elemento máximo: {maximo}")
    print()
    
    print("   # Transpor matriz (trocar linhas por colunas)")
    print("   matriz_original = [[1, 2, 3], [4, 5, 6]]")
    print("   transposta = [[linha[i] for linha in matriz_original] for i in range(3)]")
    matriz_original = [[1, 2, 3], [4, 5, 6]]
    transposta = [[linha[i] for linha in matriz_original] for i in range(3)]
    print(f"   → Original: {matriz_original}")
    print(f"   → Transposta: {transposta}")
    print()
    
    print("5. MATRIZ COMO TABULEIRO DE JOGO:")
    print("   # Tabuleiro de jogo da velha")
    tabuleiro = [['X', 'O', 'X'], 
                 ['O', 'X', 'O'], 
                 ['X', 'O', 'X']]
    
    print("   Tabuleiro do Jogo da Velha:")
    print("   ┌───┬───┬───┐")
    for i, linha in enumerate(tabuleiro):
        print("   │", end="")
        for elemento in linha:
            print(f" {elemento} │", end="")
        print()
        if i < len(tabuleiro) - 1:
            print("   ├───┼───┼───┤")
    print("   └───┴───┴───┘")
    print()
    
    print("6. CUIDADOS COM REFERÊNCIAS:")
    print("   # ERRADO - Todas as listas referenciam o mesmo objeto")
    print("   matriz_problema = [[0] * 3] * 3")
    matriz_problema = [[0] * 3] * 3
    print(f"   → Antes: {matriz_problema}")
    matriz_problema[0][0] = 1
    print(f"   → Após matriz_problema[0][0] = 1: {matriz_problema}")
    print("   ⚠️  Todas as linhas foram modificadas!")
    print()
    
    print("   # CORRETO - Cada linha é uma lista independente")
    print("   matriz_correta = [[0] * 3 for _ in range(3)]")
    matriz_correta = [[0] * 3 for _ in range(3)]
    print(f"   → Antes: {matriz_correta}")
    matriz_correta[0][0] = 1
    print(f"   → Após matriz_correta[0][0] = 1: {matriz_correta}")
    print("   ✅ Apenas a linha desejada foi modificada!")
    print()

def analise_performance():
    """
    Analisa a performance de diferentes operações com listas.
    
    Analogia: Performance é como eficiência numa fábrica.
    Algumas operações são rápidas (O(1)), outras demoram mais (O(n)).
    """
    print("=== ANÁLISE DE PERFORMANCE ===")
    print()
    
    print("1. COMPLEXIDADE DAS OPERAÇÕES:")
    print("   ┌─────────────────────┬─────────────┬─────────────────────┐")
    print("   │      OPERAÇÃO       │ COMPLEXIDADE│     DESCRIÇÃO       │")
    print("   ├─────────────────────┼─────────────┼─────────────────────┤")
    print("   │ lista[i]            │    O(1)     │ Acesso por índice   │")
    print("   │ lista.append(x)     │    O(1)     │ Adicionar no final  │")
    print("   │ lista.pop()         │    O(1)     │ Remover do final    │")
    print("   │ lista.insert(i, x)  │    O(n)     │ Inserir no meio     │")
    print("   │ lista.remove(x)     │    O(n)     │ Remover por valor   │")
    print("   │ x in lista          │    O(n)     │ Buscar elemento     │")
    print("   │ lista.sort()        │  O(n log n) │ Ordenar lista       │")
    print("   │ len(lista)          │    O(1)     │ Tamanho da lista    │")
    print("   └─────────────────────┴─────────────┴─────────────────────┘")
    print()
    
    print("2. TESTE PRÁTICO - DIFERENTES TAMANHOS:")
    tamanhos = [1000, 10000, 100000]
    
    for tamanho in tamanhos:
        print(f"   Testando com {tamanho:,} elementos:")
        
        # Criar lista
        lista = list(range(tamanho))
        
        # Teste 1: Acesso por índice (O(1))
        start = time.time()
        for _ in range(1000):
            _ = lista[tamanho // 2]  # Acesso ao meio
        tempo_acesso = time.time() - start
        
        # Teste 2: Busca linear (O(n))
        start = time.time()
        _ = tamanho - 1 in lista  # Buscar último elemento
        tempo_busca = time.time() - start
        
        # Teste 3: Inserção no início (O(n))
        start = time.time()
        lista_temp = lista.copy()
        lista_temp.insert(0, -1)
        tempo_insercao = time.time() - start
        
        print(f"     → Acesso (O(1)): {tempo_acesso:.6f}s")
        print(f"     → Busca (O(n)): {tempo_busca:.6f}s")
        print(f"     → Inserção início (O(n)): {tempo_insercao:.6f}s")
        print()
    
    print("3. COMPARAÇÃO: APPEND vs INSERT:")
    print("   Testando 10.000 operações...")
    
    # Teste append (O(1))
    lista_append = []
    start = time.time()
    for i in range(10000):
        lista_append.append(i)
    tempo_append = time.time() - start
    
    # Teste insert no início (O(n))
    lista_insert = []
    start = time.time()
    for i in range(1000):  # Menos operações pois é muito lento
        lista_insert.insert(0, i)
    tempo_insert = time.time() - start
    
    print(f"   → append() 10.000x: {tempo_append:.6f}s")
    print(f"   → insert(0) 1.000x: {tempo_insert:.6f}s")
    print(f"   → insert é ~{(tempo_insert/1000)/(tempo_append/10000):.0f}x mais lento por operação")
    print()
    
    print("4. OTIMIZAÇÕES PRÁTICAS:")
    print("   ✅ Use append() em vez de insert(0) quando possível")
    print("   ✅ Use list comprehensions para criar listas")
    print("   ✅ Use sets para buscas frequentes (O(1) vs O(n))")
    print("   ✅ Pre-aloque listas quando souber o tamanho")
    print("   ✅ Use deque para inserções/remoções no início")
    print()
    
    print("5. EXEMPLO DE OTIMIZAÇÃO:")
    print("   # LENTO - Construir string com concatenação")
    print("   resultado = ''")
    print("   for i in range(1000):")
    print("       resultado += str(i)")
    print()
    print("   # RÁPIDO - Usar lista e join")
    print("   partes = []")
    print("   for i in range(1000):")
    print("       partes.append(str(i))")
    print("   resultado = ''.join(partes)")
    print()
    
    # Demonstração prática
    # Método lento
    start = time.time()
    resultado_lento = ''
    for i in range(1000):
        resultado_lento += str(i)
    tempo_lento = time.time() - start
    
    # Método rápido
    start = time.time()
    partes = []
    for i in range(1000):
        partes.append(str(i))
    resultado_rapido = ''.join(partes)
    tempo_rapido = time.time() - start
    
    print(f"   → Concatenação: {tempo_lento:.6f}s")
    print(f"   → Lista + join: {tempo_rapido:.6f}s")
    print(f"   → Melhoria: {tempo_lento/tempo_rapido:.1f}x mais rápido!")
    print()

def visualizacao_ascii():
    """
    Demonstra visualizações ASCII para listas e operações.
    
    Analogia: Visualizações são como diagramas que tornam
    conceitos abstratos mais concretos e fáceis de entender.
    """
    print("=== VISUALIZAÇÕES ASCII ===")
    print()
    
    print("1. ESTRUTURA DE UMA LISTA:")
    lista = [10, 20, 30, 40, 50]
    
    # Visualização horizontal
    print("   Visualização Horizontal:")
    print("   ┌────┬────┬────┬────┬────┐")
    print("   │", end="")
    for elemento in lista:
        print(f"{elemento:^4}│", end="")
    print()
    print("   └────┴────┴────┴────┴────┘")
    print("     0    1    2    3    4   ← Índices")
    print()
    
    # Visualização vertical
    print("   Visualização Vertical:")
    print("   Índice │ Valor")
    print("   ───────┼──────")
    for i, valor in enumerate(lista):
        print(f"     {i}    │  {valor}")
    print()
    
    print("2. OPERAÇÃO DE INSERÇÃO:")
    lista_demo = [1, 2, 4, 5]
    print(f"   Lista original: {lista_demo}")
    print("   Inserindo 3 na posição 2:")
    print()
    print("   Antes:")
    print("   ┌───┬───┬───┬───┐")
    print("   │ 1 │ 2 │ 4 │ 5 │")
    print("   └───┴───┴───┴───┘")
    print("     0   1   2   3")
    print()
    print("   Depois de insert(2, 3):")
    print("   ┌───┬───┬───┬───┬───┐")
    print("   │ 1 │ 2 │ 3 │ 4 │ 5 │")
    print("   └───┴───┴───┴───┴───┘")
    print("     0   1   2   3   4")
    print()
    
    print("3. OPERAÇÃO DE REMOÇÃO:")
    print("   Removendo elemento na posição 1:")
    print()
    print("   Antes:")
    print("   ┌───┬───┬───┬───┬───┐")
    print("   │ 1 │ 2 │ 3 │ 4 │ 5 │")
    print("   └───┴───┴───┴───┴───┘")
    print("     0   1   2   3   4")
    print("           ↑")
    print("        remove")
    print()
    print("   Depois de pop(1):")
    print("   ┌───┬───┬───┬───┐")
    print("   │ 1 │ 3 │ 4 │ 5 │")
    print("   └───┴───┴───┴───┘")
    print("     0   1   2   3")
    print()
    
    print("4. FATIAMENTO VISUAL:")
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    print(f"   Lista: {alfabeto}")
    print("   Fatiamento: alfabeto[1:5]")
    print()
    print("   ┌───┬───┬───┬───┬───┬───┬───┐")
    print("   │ A │ B │ C │ D │ E │ F │ G │")
    print("   └───┴───┴───┴───┴───┴───┴───┘")
    print("     0   1   2   3   4   5   6")
    print("         ↑───────────↑")
    print("       início      fim")
    print("      (incluído) (excluído)")
    print()
    print(f"   Resultado: {alfabeto[1:5]}")
    print()
    
    print("5. CRESCIMENTO DINÂMICO:")
    print("   Demonstrando como listas crescem:")
    print()
    
    etapas = [
        ([], "Lista vazia"),
        ([1], "Após append(1)"),
        ([1, 2], "Após append(2)"),
        ([1, 2, 3], "Após append(3)"),
        ([1, 2, 3, 4], "Após append(4)")
    ]
    
    for lista_etapa, descricao in etapas:
        print(f"   {descricao}:")
        if not lista_etapa:
            print("   ┌─────┐")
            print("   │vazia│")
            print("   └─────┘")
        else:
            print("   ┌" + "───┬" * (len(lista_etapa) - 1) + "───┐")
            print("   │", end="")
            for elemento in lista_etapa:
                print(f" {elemento} │", end="")
            print()
            print("   └" + "───┴" * (len(lista_etapa) - 1) + "───┘")
        print()
    
    print("6. COMPARAÇÃO DE ALGORITMOS:")
    print("   Busca Linear vs Busca em Lista Ordenada:")
    print()
    
    lista_busca = [2, 5, 8, 12, 16, 23, 38, 45, 67, 78]
    target = 23
    
    print(f"   Lista: {lista_busca}")
    print(f"   Procurando: {target}")
    print()
    
    print("   Busca Linear (O(n)):")
    print("   ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐")
    print("   │ 2│ 5│ 8│12│16│23│38│45│67│78│")
    print("   └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘")
    print("    ↑  ↑  ↑  ↑  ↑  ✓")
    print("    1  2  3  4  5  6 ← Passos até encontrar")
    print()

def exemplos_praticos():
    """
    Exemplos práticos integrando todos os conceitos de listas.
    """
    print("=== EXEMPLOS PRÁTICOS INTEGRADOS ===")
    print()
    
    # Exemplo 1: Sistema de notas
    print("Exemplo 1: Sistema de Gerenciamento de Notas")
    
    def gerenciar_notas():
        """Sistema completo de gerenciamento de notas"""
        notas = []
        
        # Simulando entrada de notas
        notas_entrada = [8.5, 7.2, 9.1, 6.8, 8.9, 7.5, 9.3, 8.1]
        notas.extend(notas_entrada)
        
        print(f"   Notas inseridas: {notas}")
        
        # Estatísticas
        media = sum(notas) / len(notas)
        maior_nota = max(notas)
        menor_nota = min(notas)
        notas_ordenadas = sorted(notas, reverse=True)
        
        print(f"   → Média: {media:.2f}")
        print(f"   → Maior nota: {maior_nota}")
        print(f"   → Menor nota: {menor_nota}")
        print(f"   → Notas ordenadas: {notas_ordenadas}")
        
        # Classificação
        aprovados = [nota for nota in notas if nota >= 7.0]
        reprovados = [nota for nota in notas if nota < 7.0]
        
        print(f"   → Aprovados ({len(aprovados)}): {aprovados}")
        print(f"   → Reprovados ({len(reprovados)}): {reprovados}")
        
        return notas
    
    gerenciar_notas()
    print()
    
    # Exemplo 2: Lista de compras inteligente
    print("Exemplo 2: Lista de Compras Inteligente")
    
    def lista_compras_inteligente():
        """Sistema de lista de compras com categorização"""
        
        # Produtos com categorias
        produtos = [
            ("Maçã", "Frutas", 3.50),
            ("Leite", "Laticínios", 4.20),
            ("Pão", "Padaria", 2.80),
            ("Banana", "Frutas", 2.90),
            ("Queijo", "Laticínios", 8.50),
            ("Ovos", "Proteínas", 6.00)
        ]
        
        print("   Produtos disponíveis:")
        for i, (nome, categoria, preco) in enumerate(produtos):
            print(f"   {i+1}. {nome} ({categoria}) - R$ {preco:.2f}")
        print()
        
        # Simulando carrinho de compras
        carrinho = [produtos[0], produtos[2], produtos[4], produtos[5]]
        
        print("   Carrinho de compras:")
        total = 0
        categorias = {}
        
        for nome, categoria, preco in carrinho:
            print(f"   • {nome} - R$ {preco:.2f}")
            total += preco
            
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append((nome, preco))
        
        print(f"\n   Total: R$ {total:.2f}")
        
        print("\n   Por categoria:")
        for categoria, itens in categorias.items():
            subtotal = sum(preco for _, preco in itens)
            print(f"   {categoria}: R$ {subtotal:.2f}")
            for nome, preco in itens:
                print(f"     - {nome}: R$ {preco:.2f}")
        
        return carrinho
    
    lista_compras_inteligente()
    print()
    
    # Exemplo 3: Análise de dados simples
    print("Exemplo 3: Análise de Dados de Vendas")
    
    def analisar_vendas():
        """Análise simples de dados de vendas"""
        
        # Dados de vendas (dia, valor)
        vendas_mes = [
            120, 150, 200, 180, 220, 190, 250,  # Semana 1
            280, 300, 320, 290, 350, 380, 400,  # Semana 2
            420, 380, 360, 340, 380, 400, 450,  # Semana 3
            480, 500, 520, 490, 550, 580, 600   # Semana 4
        ]
        
        print(f"   Vendas do mês ({len(vendas_mes)} dias): {vendas_mes[:7]}... (primeiros 7 dias)")
        
        # Análises básicas
        total_vendas = sum(vendas_mes)
        media_diaria = total_vendas / len(vendas_mes)
        melhor_dia = max(vendas_mes)
        pior_dia = min(vendas_mes)
        
        print(f"   → Total do mês: R$ {total_vendas:,.2f}")
        print(f"   → Média diária: R$ {media_diaria:.2f}")
        print(f"   → Melhor dia: R$ {melhor_dia:.2f}")
        print(f"   → Pior dia: R$ {pior_dia:.2f}")
        
        # Análise por semana
        semanas = [vendas_mes[i:i+7] for i in range(0, len(vendas_mes), 7)]
        
        print("\n   Análise por semana:")
        for i, semana in enumerate(semanas, 1):
            total_semana = sum(semana)
            media_semana = total_semana / len(semana)
            print(f"   Semana {i}: Total R$ {total_semana:,.2f}, Média R$ {media_semana:.2f}")
        
        # Dias acima da média
        dias_acima_media = [venda for venda in vendas_mes if venda > media_diaria]
        percentual_acima = (len(dias_acima_media) / len(vendas_mes)) * 100
        
        print(f"\n   → Dias acima da média: {len(dias_acima_media)} ({percentual_acima:.1f}%)")
        
        # Tendência (crescimento simples)
        primeira_semana = sum(semanas[0])
        ultima_semana = sum(semanas[-1])
        crescimento = ((ultima_semana - primeira_semana) / primeira_semana) * 100
        
        print(f"   → Crescimento 1ª para última semana: {crescimento:.1f}%")
        
        return vendas_mes
    
    analisar_vendas()
    print()

def exercicios():
    """
    Exercícios progressivos para fixação de listas.
    """
    print("=== EXERCÍCIOS DE FIXAÇÃO ===")
    print()
    
    print("NÍVEL 1 - Operações Básicas:")
    print("1. Criar lista com números de 1 a 10")
    print("2. Adicionar elemento no final e no início")
    print("3. Remover elemento por valor e por índice")
    print("4. Encontrar posição de um elemento")
    print("5. Contar quantas vezes um elemento aparece")
    print()
    
    print("NÍVEL 2 - Manipulação:")
    print("6. Inverter uma lista sem usar reverse()")
    print("7. Encontrar o segundo maior elemento")
    print("8. Remover duplicatas mantendo ordem")
    print("9. Intercalar duas listas ordenadas")
    print("10. Dividir lista em sublistas de tamanho n")
    print()
    
    print("NÍVEL 3 - List Comprehensions:")
    print("11. Criar lista de quadrados dos números pares")
    print("12. Filtrar palavras que começam com vogal")
    print("13. Converter lista de strings para maiúsculas")
    print("14. Criar matriz identidade 5x5")
    print("15. Achatar lista de listas aninhadas")
    print()
    
    print("NÍVEL 4 - Algoritmos:")
    print("16. Implementar busca binária em lista ordenada")
    print("17. Encontrar subsequência crescente mais longa")
    print("18. Rotacionar lista n posições à direita")
    print("19. Encontrar par de elementos com soma específica")
    print("20. Implementar merge de duas listas ordenadas")
    print()
    
    # Exemplo de solução
    print("EXEMPLO DE SOLUÇÃO - Exercício 7:")
    print("def segundo_maior(lista):")
    print("    if len(lista) < 2:")
    print("        return None")
    print("    lista_ordenada = sorted(set(lista), reverse=True)")
    print("    return lista_ordenada[1] if len(lista_ordenada) > 1 else None")
    print()
    
    # Executando o exemplo
    def segundo_maior(lista):
        if len(lista) < 2:
            return None
        lista_ordenada = sorted(set(lista), reverse=True)
        return lista_ordenada[1] if len(lista_ordenada) > 1 else None
    
    teste_lista = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    resultado = segundo_maior(teste_lista)
    print(f"Lista: {teste_lista}")
    print(f"Segundo maior: {resultado}")
    print()

def resumo_listas():
    """
    Resumo visual de todos os conceitos de listas.
    """
    print("=== RESUMO DE LISTAS ===")
    print()
    
    print("┌─────────────────────┬─────────────┬─────────────────────────────┐")
    print("│      OPERAÇÃO       │ COMPLEXIDADE│         DESCRIÇÃO           │")
    print("├─────────────────────┼─────────────┼─────────────────────────────┤")
    print("│ Criação []          │    O(1)     │ Lista vazia                 │")
    print("│ Acesso lista[i]     │    O(1)     │ Por índice                  │")
    print("│ Busca (in)          │    O(n)     │ Procurar elemento           │")
    print("│ Append              │    O(1)     │ Adicionar no final          │")
    print("│ Insert              │    O(n)     │ Inserir em posição          │")
    print("│ Remove              │    O(n)     │ Remover por valor           │")
    print("│ Pop                 │    O(1)     │ Remover do final            │")
    print("│ Sort                │  O(n log n) │ Ordenar in-place            │")
    print("│ Slicing             │    O(k)     │ Fatiar lista                │")
    print("│ List Comprehension  │    O(n)     │ Criar lista com filtro      │")
    print("└─────────────────────┴─────────────┴─────────────────────────────┘")
    print()
    
    print("MÉTODOS PRINCIPAIS:")
    print("• append(x): Adiciona elemento no final")
    print("• insert(i, x): Insere elemento na posição i")
    print("• remove(x): Remove primeira ocorrência de x")
    print("• pop(i): Remove e retorna elemento na posição i")
    print("• index(x): Retorna índice da primeira ocorrência")
    print("• count(x): Conta ocorrências de x")
    print("• sort(): Ordena lista in-place")
    print("• reverse(): Inverte lista in-place")
    print("• extend(lista): Adiciona elementos de outra lista")
    print("• clear(): Remove todos os elementos")
    print()
    
    print("BOAS PRÁTICAS:")
    print("✅ Use list comprehensions para criar listas")
    print("✅ Prefira append() a insert(0)")
    print("✅ Use enumerate() para índice + valor")
    print("✅ Cuidado com referências em listas aninhadas")
    print("✅ Use sets para buscas frequentes")
    print("✅ Pre-aloque quando souber o tamanho")
    print("✅ Use slicing para cópias")
    print("✅ Considere deque para inserções no início")
    print()
    
    print("PADRÕES COMUNS:")
    print("• Filtrar: [x for x in lista if condição]")
    print("• Transformar: [função(x) for x in lista]")
    print("• Achatar: [item for sublista in lista for item in sublista]")
    print("• Enumerar: [(i, x) for i, x in enumerate(lista)]")
    print("• Reverter: lista[::-1]")
    print("• Copiar: lista[:] ou lista.copy()")
    print()

if __name__ == "__main__":
    # Demonstração completa do módulo
    print("🐍 CURSO DE PYTHON - MÓDULO 2.1: LISTAS E OPERAÇÕES 🐍")
    print("=" * 70)
    print()
    
    # Execução sequencial de todos os conceitos
    conceito_listas()
    print("-" * 50)
    
    criacao_inicializacao()
    print("-" * 50)
    
    indexacao_fatiamento()
    print("-" * 50)
    
    operacoes_basicas()
    print("-" * 50)
    
    list_comprehensions()
    print("-" * 50)
    
    listas_aninhadas()
    print("-" * 50)
    
    analise_performance()
    print("-" * 50)
    
    visualizacao_ascii()
    print("-" * 50)
    
    exemplos_praticos()
    print("-" * 50)
    
    resumo_listas()
    print("-" * 50)
    
    exercicios()
    
    print()
    print("🎯 CONCLUSÃO DO MÓDULO 2.1")
    print("Você aprendeu sobre:")
    print("• Conceitos fundamentais de listas")
    print("• Criação e inicialização")
    print("• Indexação e fatiamento")
    print("• Operações básicas (CRUD)")
    print("• List comprehensions")
    print("• Listas aninhadas (matrizes)")
    print("• Análise de performance")
    print("• Visualizações ASCII")
    print("• Exemplos práticos integrados")
    print()
    print("📚 Próximo módulo: 2.2 - Tuplas e Imutabilidade")
    print("=" * 70)