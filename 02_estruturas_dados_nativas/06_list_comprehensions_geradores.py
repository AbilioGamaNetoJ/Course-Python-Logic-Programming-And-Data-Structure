"""
Módulo: List Comprehensions e Geradores
Tópico: Estruturas de Dados Nativas - Conceitos Avançados
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário a Avançado

Objetivos de Aprendizado:
- Dominar list comprehensions para criação eficiente de listas
- Compreender dict e set comprehensions
- Entender o conceito de geradores (generators)
- Implementar generator expressions
- Comparar performance entre diferentes abordagens
- Aplicar lazy evaluation e economia de memória
- Resolver problemas complexos com comprehensions
- Entender quando usar cada técnica

Conceitos Abordados:
- List comprehensions básicas e avançadas
- Dict comprehensions
- Set comprehensions
- Generator expressions
- Função yield e geradores
- Lazy evaluation
- Memory efficiency
- Performance comparison

Pré-requisitos:
- Módulos 2.1 a 2.5 completos
- Conhecimento de loops e condicionais
- Compreensão de funções

Complexidade Temporal:
- List comprehension: O(n)
- Generator: O(1) para criação, O(n) para iteração completa
- Dict/Set comprehension: O(n)

Complexidade Espacial:
- List comprehension: O(n)
- Generator: O(1)
- Dict/Set comprehension: O(n)
"""

import time
import sys
from memory_profiler import profile
import itertools

def conceito_comprehensions():
    """
    Introduz o conceito de comprehensions em Python.
    
    Analogia: Comprehensions são como fórmulas matemáticas que descrevem
    como criar uma coleção baseada em regras específicas.
    """
    print("=== CONCEITO DE COMPREHENSIONS ===")
    print()
    
    print("1. O QUE SÃO COMPREHENSIONS?")
    print("   → Sintaxe concisa para criar coleções")
    print("   → Baseadas em notação matemática de conjuntos")
    print("   → Mais legíveis que loops tradicionais")
    print("   → Geralmente mais eficientes")
    print("   → Expressam intenção de forma clara")
    print()
    
    print("2. ANALOGIA MATEMÁTICA:")
    print("   Em matemática: {x² | x ∈ ℕ, x < 5}")
    print("   Em Python: [x**2 for x in range(5)]")
    print()
    print("   Lê-se: 'x ao quadrado para cada x em range(5)'")
    print()
    
    print("3. COMPARAÇÃO: LOOP vs COMPREHENSION")
    print()
    
    print("   # Método tradicional (loop)")
    print("   quadrados_loop = []")
    print("   for x in range(5):")
    print("       quadrados_loop.append(x**2)")
    
    quadrados_loop = []
    for x in range(5):
        quadrados_loop.append(x**2)
    
    print(f"   → Resultado: {quadrados_loop}")
    print()
    
    print("   # Método moderno (comprehension)")
    print("   quadrados_comp = [x**2 for x in range(5)]")
    quadrados_comp = [x**2 for x in range(5)]
    print(f"   → Resultado: {quadrados_comp}")
    print()
    
    print("4. VANTAGENS DAS COMPREHENSIONS:")
    print("   ✅ Código mais conciso e legível")
    print("   ✅ Menos propenso a erros")
    print("   ✅ Melhor performance")
    print("   ✅ Expressão clara da intenção")
    print("   ✅ Funcional vs imperativo")
    print()
    
    print("5. ESTRUTURA BÁSICA:")
    print("   [EXPRESSÃO for ITEM in ITERÁVEL]")
    print("   [EXPRESSÃO for ITEM in ITERÁVEL if CONDIÇÃO]")
    print()
    
    print("   Componentes:")
    print("   ┌─────────────┬─────────────────────────────────────┐")
    print("   │ COMPONENTE  │              DESCRIÇÃO              │")
    print("   ├─────────────┼─────────────────────────────────────┤")
    print("   │ EXPRESSÃO   │ O que será incluído na lista        │")
    print("   │ ITEM        │ Variável de iteração                │")
    print("   │ ITERÁVEL    │ Sequência a ser percorrida          │")
    print("   │ CONDIÇÃO    │ Filtro opcional (if)                │")
    print("   └─────────────┴─────────────────────────────────────┘")
    print()
    
    print("6. TIPOS DE COMPREHENSIONS:")
    print("   → List comprehension: [expr for item in iterable]")
    print("   → Dict comprehension: {key: value for item in iterable}")
    print("   → Set comprehension: {expr for item in iterable}")
    print("   → Generator expression: (expr for item in iterable)")
    print()
    
    print("7. EXEMPLO PRÁTICO - PROCESSAMENTO DE DADOS:")
    vendas = [100, 250, 180, 320, 90, 400, 150]
    print(f"   vendas = {vendas}")
    print()
    
    print("   # Vendas com desconto de 10%")
    vendas_desconto = [venda * 0.9 for venda in vendas]
    print(f"   → Com desconto: {vendas_desconto}")
    
    print("   # Apenas vendas acima de 200")
    vendas_altas = [venda for venda in vendas if venda > 200]
    print(f"   → Vendas altas: {vendas_altas}")
    
    print("   # Vendas categorizadas")
    categorias = ['Alta' if v > 200 else 'Baixa' for v in vendas]
    print(f"   → Categorias: {categorias}")
    print()

def list_comprehensions_basicas():
    """
    Explora list comprehensions básicas e suas variações.
    """
    print("=== LIST COMPREHENSIONS BÁSICAS ===")
    print()
    
    print("1. SINTAXE FUNDAMENTAL:")
    print("   [expressão for item in iterável]")
    print()
    
    print("   # Exemplo 1: Números ao quadrado")
    print("   quadrados = [x**2 for x in range(1, 6)]")
    quadrados = [x**2 for x in range(1, 6)]
    print(f"   → {quadrados}")
    print()
    
    print("   # Exemplo 2: Strings em maiúsculas")
    nomes = ['ana', 'bruno', 'carlos', 'diana']
    print(f"   nomes = {nomes}")
    print("   nomes_upper = [nome.upper() for nome in nomes]")
    nomes_upper = [nome.upper() for nome in nomes]
    print(f"   → {nomes_upper}")
    print()
    
    print("2. COMPREHENSIONS COM CONDIÇÕES:")
    print("   [expressão for item in iterável if condição]")
    print()
    
    numeros = list(range(1, 11))
    print(f"   numeros = {numeros}")
    
    print("   # Apenas números pares")
    print("   pares = [x for x in numeros if x % 2 == 0]")
    pares = [x for x in numeros if x % 2 == 0]
    print(f"   → {pares}")
    
    print("   # Quadrados dos ímpares")
    print("   quadrados_impares = [x**2 for x in numeros if x % 2 == 1]")
    quadrados_impares = [x**2 for x in numeros if x % 2 == 1]
    print(f"   → {quadrados_impares}")
    print()
    
    print("3. EXPRESSÕES CONDICIONAIS (TERNÁRIO):")
    print("   [expr_if if condição else expr_else for item in iterável]")
    print()
    
    print("   # Classificação par/ímpar")
    print("   classificacao = ['Par' if x % 2 == 0 else 'Ímpar' for x in range(1, 6)]")
    classificacao = ['Par' if x % 2 == 0 else 'Ímpar' for x in range(1, 6)]
    print(f"   → {classificacao}")
    
    print("   # Valores absolutos com sinal")
    valores = [-3, -1, 0, 2, 5]
    print(f"   valores = {valores}")
    print("   abs_com_sinal = [abs(x) if x < 0 else x for x in valores]")
    abs_com_sinal = [abs(x) if x < 0 else x for x in valores]
    print(f"   → {abs_com_sinal}")
    print()
    
    print("4. TRABALHANDO COM STRINGS:")
    frase = "Python é uma linguagem incrível"
    print(f"   frase = '{frase}'")
    
    print("   # Comprimento de cada palavra")
    print("   comprimentos = [len(palavra) for palavra in frase.split()]")
    comprimentos = [len(palavra) for palavra in frase.split()]
    print(f"   → {comprimentos}")
    
    print("   # Palavras com mais de 4 letras")
    print("   palavras_longas = [p for p in frase.split() if len(p) > 4]")
    palavras_longas = [p for p in frase.split() if len(p) > 4]
    print(f"   → {palavras_longas}")
    
    print("   # Primeira letra de cada palavra")
    print("   iniciais = [palavra[0].upper() for palavra in frase.split()]")
    iniciais = [palavra[0].upper() for palavra in frase.split()]
    print(f"   → {iniciais}")
    print()
    
    print("5. TRABALHANDO COM LISTAS ANINHADAS:")
    matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(f"   matriz = {matriz}")
    
    print("   # Achatar matriz (flatten)")
    print("   plana = [item for linha in matriz for item in linha]")
    plana = [item for linha in matriz for item in linha]
    print(f"   → {plana}")
    
    print("   # Elementos pares da matriz")
    print("   pares_matriz = [item for linha in matriz for item in linha if item % 2 == 0]")
    pares_matriz = [item for linha in matriz for item in linha if item % 2 == 0]
    print(f"   → {pares_matriz}")
    print()
    
    print("6. CASOS PRÁTICOS:")
    
    # Processamento de dados de vendas
    vendas_mes = [
        {'produto': 'Notebook', 'quantidade': 5, 'preco': 2500},
        {'produto': 'Mouse', 'quantidade': 20, 'preco': 50},
        {'produto': 'Teclado', 'quantidade': 15, 'preco': 150},
        {'produto': 'Monitor', 'quantidade': 8, 'preco': 800}
    ]
    
    print("   # Dados de vendas:")
    for venda in vendas_mes:
        print(f"   → {venda}")
    print()
    
    print("   # Total por produto")
    print("   totais = [v['quantidade'] * v['preco'] for v in vendas_mes]")
    totais = [v['quantidade'] * v['preco'] for v in vendas_mes]
    print(f"   → {totais}")
    
    print("   # Produtos caros (preço > 100)")
    print("   caros = [v['produto'] for v in vendas_mes if v['preco'] > 100]")
    caros = [v['produto'] for v in vendas_mes if v['preco'] > 100]
    print(f"   → {caros}")
    
    print("   # Relatório formatado")
    print("   relatorio = [f\"{v['produto']}: R$ {v['quantidade'] * v['preco']:,.2f}\" for v in vendas_mes]")
    relatorio = [f"{v['produto']}: R$ {v['quantidade'] * v['preco']:,.2f}" for v in vendas_mes]
    for item in relatorio:
        print(f"   → {item}")
    print()

def comprehensions_avancadas():
    """
    Explora dict e set comprehensions e casos avançados.
    """
    print("=== COMPREHENSIONS AVANÇADAS ===")
    print()
    
    print("1. DICT COMPREHENSIONS:")
    print("   {chave: valor for item in iterável}")
    print()
    
    print("   # Exemplo 1: Quadrados como dicionário")
    print("   quadrados_dict = {x: x**2 for x in range(1, 6)}")
    quadrados_dict = {x: x**2 for x in range(1, 6)}
    print(f"   → {quadrados_dict}")
    
    print("   # Exemplo 2: Invertendo dicionário")
    original = {'a': 1, 'b': 2, 'c': 3}
    print(f"   original = {original}")
    print("   invertido = {v: k for k, v in original.items()}")
    invertido = {v: k for k, v in original.items()}
    print(f"   → {invertido}")
    print()
    
    print("2. SET COMPREHENSIONS:")
    print("   {expressão for item in iterável}")
    print()
    
    print("   # Exemplo 1: Quadrados únicos")
    numeros = [1, -1, 2, -2, 3, -3]
    print(f"   numeros = {numeros}")
    print("   quadrados_set = {x**2 for x in numeros}")
    quadrados_set = {x**2 for x in numeros}
    print(f"   → {quadrados_set}")
    
    print("   # Exemplo 2: Primeiras letras únicas")
    palavras = ['python', 'java', 'javascript', 'php', 'perl']
    print(f"   palavras = {palavras}")
    print("   iniciais_set = {palavra[0].upper() for palavra in palavras}")
    iniciais_set = {palavra[0].upper() for palavra in palavras}
    print(f"   → {iniciais_set}")
    print()
    
    print("3. COMPREHENSIONS ANINHADAS:")
    print("   # Matriz transposta")
    matriz = [[1, 2, 3], [4, 5, 6]]
    print(f"   matriz = {matriz}")
    print("   transposta = [[linha[i] for linha in matriz] for i in range(len(matriz[0]))]")
    transposta = [[linha[i] for linha in matriz] for i in range(len(matriz[0]))]
    print(f"   → {transposta}")
    print()
    
    print("   # Tabela de multiplicação")
    print("   tabuada = [[i * j for j in range(1, 4)] for i in range(1, 4)]")
    tabuada = [[i * j for j in range(1, 4)] for i in range(1, 4)]
    print("   → Resultado:")
    for linha in tabuada:
        print(f"     {linha}")
    print()
    
    print("4. CASOS PRÁTICOS AVANÇADOS:")
    
    # Análise de texto
    texto = "Python é uma linguagem de programação Python"
    print(f"   texto = '{texto}'")
    
    print("   # Contagem de caracteres")
    print("   char_count = {char: texto.lower().count(char) for char in set(texto.lower()) if char.isalpha()}")
    char_count = {char: texto.lower().count(char) for char in set(texto.lower()) if char.isalpha()}
    print(f"   → {dict(sorted(char_count.items()))}")
    
    print("   # Índices de palavras")
    palavras = texto.split()
    print("   indices_palavras = {palavra: i for i, palavra in enumerate(palavras)}")
    indices_palavras = {palavra: i for i, palavra in enumerate(palavras)}
    print(f"   → {indices_palavras}")
    print()
    
    # Processamento de dados de funcionários
    funcionarios = [
        {'nome': 'Ana', 'departamento': 'TI', 'salario': 5000},
        {'nome': 'Bruno', 'departamento': 'RH', 'salario': 4500},
        {'nome': 'Carlos', 'departamento': 'TI', 'salario': 5500},
        {'nome': 'Diana', 'departamento': 'Vendas', 'salario': 4000}
    ]
    
    print("   # Dados de funcionários:")
    for func in funcionarios:
        print(f"   → {func}")
    print()
    
    print("   # Salários por departamento")
    print("   salarios_depto = {f['departamento']: f['salario'] for f in funcionarios}")
    salarios_depto = {f['departamento']: f['salario'] for f in funcionarios}
    print(f"   → {salarios_depto}")
    
    print("   # Funcionários de TI")
    print("   ti_funcionarios = {f['nome']: f['salario'] for f in funcionarios if f['departamento'] == 'TI'}")
    ti_funcionarios = {f['nome']: f['salario'] for f in funcionarios if f['departamento'] == 'TI'}
    print(f"   → {ti_funcionarios}")
    
    print("   # Departamentos únicos")
    print("   departamentos = {f['departamento'] for f in funcionarios}")
    departamentos = {f['departamento'] for f in funcionarios}
    print(f"   → {departamentos}")
    print()

def conceito_geradores():
    """
    Introduz o conceito de geradores e lazy evaluation.
    
    Analogia: Geradores são como fábricas que produzem itens sob demanda,
    em vez de produzir tudo de uma vez e armazenar.
    """
    print("=== CONCEITO DE GERADORES ===")
    print()
    
    print("1. O QUE SÃO GERADORES?")
    print("   → Objetos que produzem itens sob demanda (lazy evaluation)")
    print("   → Não armazenam todos os valores na memória")
    print("   → Usam a palavra-chave 'yield'")
    print("   → Implementam o protocolo de iteração")
    print("   → Muito eficientes em memória")
    print("   → Ideais para sequências grandes ou infinitas")
    print()
    
    print("2. ANALOGIA DO COTIDIANO:")
    print("   🏭 Lista: Fábrica que produz todos os produtos e os armazena")
    print("   ⚡ Gerador: Linha de produção que faz um item por vez")
    print()
    print("   📚 Lista: Biblioteca com todos os livros impressos")
    print("   📖 Gerador: Impressora que imprime páginas conforme necessário")
    print()
    
    print("3. COMPARAÇÃO: LISTA vs GERADOR")
    print()
    
    print("   # Lista (eager evaluation)")
    print("   lista_quadrados = [x**2 for x in range(5)]")
    lista_quadrados = [x**2 for x in range(5)]
    print(f"   → Tipo: {type(lista_quadrados)}")
    print(f"   → Valores: {lista_quadrados}")
    print(f"   → Tamanho na memória: {sys.getsizeof(lista_quadrados)} bytes")
    print()
    
    print("   # Gerador (lazy evaluation)")
    print("   gen_quadrados = (x**2 for x in range(5))")
    gen_quadrados = (x**2 for x in range(5))
    print(f"   → Tipo: {type(gen_quadrados)}")
    print(f"   → Objeto: {gen_quadrados}")
    print(f"   → Tamanho na memória: {sys.getsizeof(gen_quadrados)} bytes")
    print()
    
    print("   # Consumindo o gerador")
    print("   for valor in gen_quadrados:")
    print("       print(valor)")
    print("   → Resultado:")
    gen_quadrados = (x**2 for x in range(5))  # Recriando pois foi consumido
    for valor in gen_quadrados:
        print(f"     {valor}")
    print()
    
    print("4. FUNÇÃO GERADORA COM YIELD:")
    
    def contador_simples(limite):
        """Gerador simples que conta até um limite"""
        print(f"   Iniciando contador até {limite}")
        for i in range(limite):
            print(f"   Produzindo: {i}")
            yield i
        print(f"   Contador finalizado")
    
    print("   def contador_simples(limite):")
    print("       for i in range(limite):")
    print("           yield i")
    print()
    
    print("   # Criando o gerador")
    print("   contador = contador_simples(3)")
    contador = contador_simples(3)
    print(f"   → Tipo: {type(contador)}")
    print()
    
    print("   # Consumindo um por vez")
    print("   next(contador) →", next(contador))
    print("   next(contador) →", next(contador))
    print("   next(contador) →", next(contador))
    
    try:
        print("   next(contador) →", next(contador))
    except StopIteration:
        print("   → StopIteration: Gerador esgotado")
    print()
    
    print("5. VANTAGENS DOS GERADORES:")
    print("   ✅ Economia de memória")
    print("   ✅ Lazy evaluation")
    print("   ✅ Podem representar sequências infinitas")
    print("   ✅ Composição eficiente")
    print("   ✅ Melhor para processamento de grandes datasets")
    print()
    
    print("6. EXEMPLO PRÁTICO - FIBONACCI:")
    
    def fibonacci_gerador():
        """Gerador infinito da sequência de Fibonacci"""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    print("   def fibonacci_gerador():")
    print("       a, b = 0, 1")
    print("       while True:")
    print("           yield a")
    print("           a, b = b, a + b")
    print()
    
    print("   # Primeiros 10 números de Fibonacci")
    fib = fibonacci_gerador()
    primeiros_10 = [next(fib) for _ in range(10)]
    print(f"   → {primeiros_10}")
    print()
    
    print("7. GENERATOR EXPRESSIONS:")
    print("   (expressão for item in iterável)")
    print()
    
    print("   # Soma de quadrados (memory efficient)")
    print("   soma = sum(x**2 for x in range(1000000))")
    # Simulando para números menores para demonstração
    soma = sum(x**2 for x in range(10))
    print(f"   → Soma dos quadrados de 0-9: {soma}")
    
    print("   # Filtro com gerador")
    print("   pares_grandes = (x for x in range(100) if x % 2 == 0 and x > 50)")
    pares_grandes = (x for x in range(100) if x % 2 == 0 and x > 50)
    print(f"   → Primeiros 5: {list(itertools.islice(pares_grandes, 5))}")
    print()

def geradores_avancados():
    """
    Explora técnicas avançadas com geradores.
    """
    print("=== GERADORES AVANÇADOS ===")
    print()
    
    print("1. GERADOR COM ESTADO:")
    
    def contador_com_estado(inicio=0, passo=1):
        """Gerador que mantém estado interno"""
        atual = inicio
        while True:
            yield atual
            atual += passo
    
    print("   def contador_com_estado(inicio=0, passo=1):")
    print("       atual = inicio")
    print("       while True:")
    print("           yield atual")
    print("           atual += passo")
    print()
    
    print("   # Contador de 5 em 5")
    contador5 = contador_com_estado(0, 5)
    print("   primeiros_5 = [next(contador5) for _ in range(5)]")
    primeiros_5 = [next(contador5) for _ in range(5)]
    print(f"   → {primeiros_5}")
    print()
    
    print("2. GERADOR DE PROCESSAMENTO DE ARQUIVO:")
    
    def processar_linhas(texto):
        """Simula processamento de arquivo linha por linha"""
        linhas = texto.strip().split('\n')
        for numero_linha, linha in enumerate(linhas, 1):
            # Processamento da linha
            linha_processada = {
                'numero': numero_linha,
                'conteudo': linha.strip(),
                'palavras': len(linha.split()),
                'caracteres': len(linha)
            }
            yield linha_processada
    
    texto_exemplo = """
    Python é uma linguagem incrível
    Geradores são muito úteis
    Eles economizam memória
    """
    
    print("   # Processando texto linha por linha")
    print("   for info_linha in processar_linhas(texto):")
    print("       print(info_linha)")
    print()
    print("   → Resultado:")
    for info_linha in processar_linhas(texto_exemplo):
        print(f"     Linha {info_linha['numero']}: {info_linha['palavras']} palavras, {info_linha['caracteres']} chars")
    print()
    
    print("3. PIPELINE DE GERADORES:")
    
    def numeros_fonte(limite):
        """Gerador fonte de números"""
        for i in range(limite):
            yield i
    
    def filtrar_pares(numeros):
        """Filtra apenas números pares"""
        for num in numeros:
            if num % 2 == 0:
                yield num
    
    def elevar_ao_quadrado(numeros):
        """Eleva números ao quadrado"""
        for num in numeros:
            yield num ** 2
    
    print("   # Pipeline: números → pares → quadrados")
    print("   fonte = numeros_fonte(10)")
    print("   pares = filtrar_pares(fonte)")
    print("   quadrados = elevar_ao_quadrado(pares)")
    
    fonte = numeros_fonte(10)
    pares = filtrar_pares(fonte)
    quadrados = elevar_ao_quadrado(pares)
    
    resultado_pipeline = list(quadrados)
    print(f"   → {resultado_pipeline}")
    print()
    
    print("4. GERADOR COM SEND() E CLOSE():")
    
    def acumulador():
        """Gerador que acumula valores enviados"""
        total = 0
        while True:
            valor = yield total
            if valor is not None:
                total += valor
    
    print("   def acumulador():")
    print("       total = 0")
    print("       while True:")
    print("           valor = yield total")
    print("           if valor is not None:")
    print("               total += valor")
    print()
    
    print("   # Usando send() para enviar valores")
    acc = acumulador()
    next(acc)  # Inicializa o gerador
    
    print("   acc = acumulador()")
    print("   next(acc)  # Inicializa")
    print(f"   acc.send(10) → {acc.send(10)}")
    print(f"   acc.send(20) → {acc.send(20)}")
    print(f"   acc.send(5) → {acc.send(5)}")
    print()
    
    print("5. GERADOR INFINITO COM ITERTOOLS:")
    
    print("   # Ciclo infinito")
    print("   import itertools")
    print("   cores = itertools.cycle(['vermelho', 'verde', 'azul'])")
    cores = itertools.cycle(['vermelho', 'verde', 'azul'])
    primeiras_cores = [next(cores) for _ in range(8)]
    print(f"   → Primeiras 8: {primeiras_cores}")
    
    print("   # Contagem infinita")
    print("   contador_inf = itertools.count(1, 2)  # Ímpares")
    contador_inf = itertools.count(1, 2)
    primeiros_impares = [next(contador_inf) for _ in range(5)]
    print(f"   → Primeiros 5 ímpares: {primeiros_impares}")
    print()
    
    print("6. PERFORMANCE E MEMÓRIA:")
    
    def comparar_performance():
        """Compara performance entre lista e gerador"""
        n = 100000
        
        # Lista
        start_time = time.time()
        lista = [x**2 for x in range(n)]
        tempo_lista = time.time() - start_time
        memoria_lista = sys.getsizeof(lista)
        
        # Gerador
        start_time = time.time()
        gerador = (x**2 for x in range(n))
        tempo_gerador = time.time() - start_time
        memoria_gerador = sys.getsizeof(gerador)
        
        return {
            'lista': {'tempo': tempo_lista, 'memoria': memoria_lista},
            'gerador': {'tempo': tempo_gerador, 'memoria': memoria_gerador}
        }
    
    print("   # Comparação de performance (n=100,000)")
    stats = comparar_performance()
    
    print(f"   Lista:")
    print(f"   → Tempo: {stats['lista']['tempo']:.6f}s")
    print(f"   → Memória: {stats['lista']['memoria']:,} bytes")
    
    print(f"   Gerador:")
    print(f"   → Tempo: {stats['gerador']['tempo']:.6f}s")
    print(f"   → Memória: {stats['gerador']['memoria']:,} bytes")
    
    economia_memoria = (1 - stats['gerador']['memoria'] / stats['lista']['memoria']) * 100
    print(f"   → Economia de memória: {economia_memoria:.1f}%")
    print()

def casos_praticos_avancados():
    """
    Demonstra casos práticos avançados usando comprehensions e geradores.
    """
    print("=== CASOS PRÁTICOS AVANÇADOS ===")
    print()
    
    print("Caso 1: Processador de Log")
    
    def processar_logs(logs):
        """Processa logs de servidor web"""
        for linha in logs:
            if 'ERROR' in linha:
                partes = linha.split(' - ')
                if len(partes) >= 3:
                    timestamp = partes[0]
                    nivel = partes[1]
                    mensagem = partes[2]
                    yield {
                        'timestamp': timestamp,
                        'nivel': nivel,
                        'mensagem': mensagem,
                        'critico': 'CRITICAL' in mensagem
                    }
    
    logs_exemplo = [
        "2024-01-15 10:30:00 - ERROR - Database connection failed",
        "2024-01-15 10:30:05 - INFO - User login successful",
        "2024-01-15 10:30:10 - ERROR - CRITICAL: System out of memory",
        "2024-01-15 10:30:15 - WARNING - High CPU usage detected"
    ]
    
    print("   # Processando logs de erro")
    erros = list(processar_logs(logs_exemplo))
    for erro in erros:
        status = "🔴 CRÍTICO" if erro['critico'] else "⚠️  ERRO"
        print(f"   → {status}: {erro['mensagem']}")
    print()
    
    print("Caso 2: Analisador de Vendas")
    
    vendas_dados = [
        {'data': '2024-01-01', 'produto': 'Notebook', 'valor': 2500, 'vendedor': 'Ana'},
        {'data': '2024-01-01', 'produto': 'Mouse', 'valor': 50, 'vendedor': 'Bruno'},
        {'data': '2024-01-02', 'produto': 'Notebook', 'valor': 2500, 'vendedor': 'Ana'},
        {'data': '2024-01-02', 'produto': 'Teclado', 'valor': 150, 'vendedor': 'Carlos'},
        {'data': '2024-01-03', 'produto': 'Monitor', 'valor': 800, 'vendedor': 'Ana'}
    ]
    
    print("   # Análises com comprehensions")
    
    # Total por vendedor
    vendedores = {venda['vendedor'] for venda in vendas_dados}
    total_por_vendedor = {
        vendedor: sum(v['valor'] for v in vendas_dados if v['vendedor'] == vendedor)
        for vendedor in vendedores
    }
    print("   → Total por vendedor:")
    for vendedor, total in total_por_vendedor.items():
        print(f"     {vendedor}: R$ {total:,.2f}")
    
    # Produtos únicos por dia
    produtos_por_dia = {
        venda['data']: {v['produto'] for v in vendas_dados if v['data'] == venda['data']}
        for venda in vendas_dados
    }
    print("\n   → Produtos únicos por dia:")
    for data, produtos in produtos_por_dia.items():
        print(f"     {data}: {', '.join(produtos)}")
    
    # Vendas acima de R$ 1000
    vendas_altas = [
        f"{v['produto']} - R$ {v['valor']:,.2f} ({v['vendedor']})"
        for v in vendas_dados if v['valor'] > 1000
    ]
    print("\n   → Vendas acima de R$ 1.000:")
    for venda in vendas_altas:
        print(f"     {venda}")
    print()
    
    print("Caso 3: Gerador de Relatórios")
    
    def gerar_relatorio_mensal(vendas):
        """Gera relatório mensal de vendas"""
        # Agrupa por mês
        from collections import defaultdict
        vendas_mes = defaultdict(list)
        
        for venda in vendas:
            mes = venda['data'][:7]  # YYYY-MM
            vendas_mes[mes].append(venda)
        
        # Gera relatório para cada mês
        for mes, vendas_do_mes in vendas_mes.items():
            total_mes = sum(v['valor'] for v in vendas_do_mes)
            qtd_vendas = len(vendas_do_mes)
            ticket_medio = total_mes / qtd_vendas if qtd_vendas > 0 else 0
            
            yield {
                'mes': mes,
                'total': total_mes,
                'quantidade': qtd_vendas,
                'ticket_medio': ticket_medio,
                'top_produto': max(vendas_do_mes, key=lambda x: x['valor'])['produto']
            }
    
    print("   # Relatório mensal")
    for relatorio in gerar_relatorio_mensal(vendas_dados):
        print(f"   → Mês {relatorio['mes']}:")
        print(f"     Total: R$ {relatorio['total']:,.2f}")
        print(f"     Vendas: {relatorio['quantidade']}")
        print(f"     Ticket médio: R$ {relatorio['ticket_medio']:.2f}")
        print(f"     Top produto: {relatorio['top_produto']}")
        print()
    
    print("Caso 4: Pipeline de Transformação de Dados")
    
    def extrair_numeros(texto):
        """Extrai números de um texto"""
        import re
        for numero in re.findall(r'\d+', texto):
            yield int(numero)
    
    def filtrar_pares(numeros):
        """Filtra apenas números pares"""
        for num in numeros:
            if num % 2 == 0:
                yield num
    
    def transformar_quadrados(numeros):
        """Transforma em quadrados"""
        for num in numeros:
            yield num ** 2
    
    def limitar_resultado(numeros, limite):
        """Limita quantidade de resultados"""
        count = 0
        for num in numeros:
            if count >= limite:
                break
            yield num
            count += 1
    
    texto_numeros = "Temos 12 produtos, 7 vendedores, 25 clientes e 8 fornecedores"
    print(f"   Texto: '{texto_numeros}'")
    
    # Pipeline completo
    pipeline = limitar_resultado(
        transformar_quadrados(
            filtrar_pares(
                extrair_numeros(texto_numeros)
            )
        ), 3
    )
    
    resultado_final = list(pipeline)
    print(f"   → Pipeline (números → pares → quadrados → limite 3): {resultado_final}")
    print()

if __name__ == "__main__":
    print("MÓDULO 2.6 - LIST COMPREHENSIONS E GERADORES")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceito_comprehensions()
    print("\n" + "="*50 + "\n")
    
    list_comprehensions_basicas()
    print("\n" + "="*50 + "\n")
    
    comprehensions_avancadas()
    print("\n" + "="*50 + "\n")
    
    conceito_geradores()
    print("\n" + "="*50 + "\n")
    
    geradores_avancados()
    print("\n" + "="*50 + "\n")
    
    casos_praticos_avancados()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 2.6 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ List comprehensions básicas e avançadas")
    print("✅ Dict e set comprehensions")
    print("✅ Conceito de geradores e lazy evaluation")
    print("✅ Generator expressions")
    print("✅ Funções geradoras com yield")
    print("✅ Pipeline de geradores")
    print("✅ Comparação de performance e memória")
    print("✅ Casos práticos avançados")
    print("\n➡️  Próximo: Módulo 2.7 - Análise de Performance")