"""
Módulo: Dicionários e Mapeamentos
Tópico: Estruturas de Dados Nativas
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico a Intermediário

Objetivos de Aprendizado:
- Compreender dicionários como estruturas chave-valor
- Dominar criação, acesso e modificação de dicionários
- Implementar operações avançadas com dicionários
- Trabalhar com métodos de dicionários
- Aplicar dictionary comprehensions
- Entender OrderedDict, defaultdict e Counter
- Analisar performance de dicionários
- Resolver problemas práticos com mapeamentos

Conceitos Abordados:
- Definição e características de dicionários
- Criação e sintaxe de dicionários
- Acesso e modificação de elementos
- Métodos principais (keys, values, items, get, pop, etc.)
- Dictionary comprehensions
- Dicionários aninhados
- Variações especiais (OrderedDict, defaultdict, Counter)
- Operações de conjunto com dicionários
- Casos de uso práticos

Pré-requisitos:
- Módulos 2.1 e 2.2 completos
- Conhecimento de iteração
- Compreensão de hashable objects

Complexidade Temporal:
- Acesso: O(1) médio
- Inserção: O(1) médio
- Remoção: O(1) médio
- Busca: O(1) médio

Complexidade Espacial: O(n) onde n é o número de pares chave-valor
"""

import time
import sys
from collections import OrderedDict, defaultdict, Counter

def conceito_dicionarios():
    """
    Introduz o conceito fundamental de dicionários.
    
    Analogia: Dicionários são como catálogos telefônicos ou índices.
    Cada entrada tem uma chave única que mapeia para um valor específico,
    permitindo acesso rápido e direto aos dados.
    """
    print("=== CONCEITO DE DICIONÁRIOS ===")
    print()
    
    print("1. O QUE SÃO DICIONÁRIOS?")
    print("   → Estruturas de dados que mapeiam chaves para valores")
    print("   → Não ordenados (Python < 3.7) ou ordenados por inserção (Python ≥ 3.7)")
    print("   → Chaves devem ser únicas e hashable")
    print("   → Valores podem ser de qualquer tipo")
    print("   → Mutáveis - podem ser modificados")
    print("   → Acesso extremamente rápido O(1)")
    print("   → Implementados como hash tables")
    print()
    
    print("2. ANALOGIAS DO COTIDIANO:")
    print("   📞 Catálogo telefônico (nome → telefone)")
    print("   📚 Dicionário de idiomas (palavra → significado)")
    print("   🏪 Catálogo de produtos (código → produto)")
    print("   🎫 Sistema de reservas (assento → passageiro)")
    print("   🏥 Prontuário médico (CPF → dados do paciente)")
    print("   🎮 Placar de jogos (jogador → pontuação)")
    print("   🗂️  Arquivo de funcionários (ID → dados)")
    print()
    
    print("3. VISUALIZAÇÃO ASCII DE UM DICIONÁRIO:")
    exemplo_dict = {'nome': 'Ana', 'idade': 25, 'cidade': 'SP'}
    print("   Dicionário: {'nome': 'Ana', 'idade': 25, 'cidade': 'SP'}")
    print()
    print("   ┌─────────────┬─────────────┐")
    print("   │    CHAVE    │    VALOR    │")
    print("   ├─────────────┼─────────────┤")
    print("   │   'nome'    │    'Ana'    │ ← Par chave-valor")
    print("   │   'idade'   │     25      │ ← Par chave-valor")
    print("   │   'cidade'  │    'SP'     │ ← Par chave-valor")
    print("   └─────────────┴─────────────┘")
    print("        ↑             ↑")
    print("    Hashable      Qualquer tipo")
    print()
    
    print("4. ESTRUTURA INTERNA (HASH TABLE):")
    print("   Hash Function")
    print("        ↓")
    print("   ┌─────┬─────┬─────┬─────┬─────┐")
    print("   │  0  │  1  │  2  │  3  │  4  │ ← Buckets")
    print("   └─────┴─────┴─────┴─────┴─────┘")
    print("     ↓     ↓     ↓     ↓     ↓")
    print("   None  'nome' None 'idade' 'cidade'")
    print("         'Ana'        25     'SP'")
    print()
    print("   • Hash da chave determina posição")
    print("   • Colisões são tratadas internamente")
    print("   • Acesso direto = O(1)")
    print()
    
    print("5. DIFERENÇAS COM OUTRAS ESTRUTURAS:")
    print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │ CARACTERÍSTICA  │ DICIONÁRIO  │    LISTA    │    TUPLA    │")
    print("   ├─────────────────┼─────────────┼─────────────┼─────────────┤")
    print("   │ Acesso          │ Por chave   │ Por índice  │ Por índice  │")
    print("   │ Ordem           │ Inserção*   │   Posição   │   Posição   │")
    print("   │ Mutabilidade    │   Mutável   │   Mutável   │  Imutável   │")
    print("   │ Chaves/Índices  │  Hashable   │  Inteiros   │  Inteiros   │")
    print("   │ Duplicatas      │     Não     │     Sim     │     Sim     │")
    print("   │ Performance     │    O(1)     │    O(n)     │    O(n)     │")
    print("   │ Uso de memória  │    Alto     │   Médio     │   Baixo     │")
    print("   └─────────────────┴─────────────┴─────────────┴─────────────┘")
    print("   * Python ≥ 3.7")
    print()
    
    print("6. EXEMPLO PRÁTICO:")
    print("   # Criando um dicionário")
    print("   estudante = {")
    print("       'nome': 'Carlos',")
    print("       'idade': 22,")
    print("       'curso': 'Engenharia',")
    print("       'notas': [8.5, 9.0, 7.5]")
    print("   }")
    print()
    
    # Executando o exemplo
    estudante = {
        'nome': 'Carlos',
        'idade': 22,
        'curso': 'Engenharia',
        'notas': [8.5, 9.0, 7.5]
    }
    
    print("   RESULTADO:")
    print(f"   → Dicionário: {estudante}")
    print(f"   → Nome: {estudante['nome']}")
    print(f"   → Idade: {estudante['idade']}")
    print(f"   → Média: {sum(estudante['notas'])/len(estudante['notas']):.2f}")
    print(f"   → Tipo: {type(estudante)}")
    print(f"   → Tamanho: {len(estudante)} pares chave-valor")
    print()

def criacao_sintaxe_dicionarios():
    """
    Explora diferentes formas de criar dicionários.
    
    Analogia: Criar dicionários é como organizar diferentes tipos
    de catálogos, cada um com sua forma específica de estruturação.
    """
    print("=== CRIAÇÃO E SINTAXE DE DICIONÁRIOS ===")
    print()
    
    print("1. DICIONÁRIO VAZIO:")
    print("   dict_vazio1 = {}")
    print("   dict_vazio2 = dict()")
    print()
    
    dict_vazio1 = {}
    dict_vazio2 = dict()
    
    print(f"   → dict_vazio1: {dict_vazio1} (tipo: {type(dict_vazio1)})")
    print(f"   → dict_vazio2: {dict_vazio2} (tipo: {type(dict_vazio2)})")
    print()
    
    print("2. DICIONÁRIO COM VALORES INICIAIS:")
    print("   # Sintaxe literal (mais comum)")
    print("   pessoa = {")
    print("       'nome': 'Maria',")
    print("       'idade': 30,")
    print("       'profissao': 'Médica'")
    print("   }")
    print()
    
    pessoa = {
        'nome': 'Maria',
        'idade': 30,
        'profissao': 'Médica'
    }
    
    print(f"   → pessoa: {pessoa}")
    print()
    
    print("3. USANDO O CONSTRUTOR dict():")
    print("   # Com argumentos nomeados")
    print("   config = dict(host='localhost', porta=8080, debug=True)")
    print()
    print("   # Com lista de tuplas")
    print("   cores = dict([('vermelho', '#FF0000'), ('verde', '#00FF00')])")
    print()
    print("   # Com zip")
    print("   chaves = ['a', 'b', 'c']")
    print("   valores = [1, 2, 3]")
    print("   alfabeto = dict(zip(chaves, valores))")
    print()
    
    config = dict(host='localhost', porta=8080, debug=True)
    cores = dict([('vermelho', '#FF0000'), ('verde', '#00FF00')])
    chaves = ['a', 'b', 'c']
    valores = [1, 2, 3]
    alfabeto = dict(zip(chaves, valores))
    
    print("   RESULTADO:")
    print(f"   → config: {config}")
    print(f"   → cores: {cores}")
    print(f"   → alfabeto: {alfabeto}")
    print()
    
    print("4. DICTIONARY COMPREHENSION:")
    print("   # Quadrados dos números")
    print("   quadrados = {x: x**2 for x in range(1, 6)}")
    print()
    print("   # Com condição")
    print("   pares = {x: x**2 for x in range(10) if x % 2 == 0}")
    print()
    print("   # Transformando lista")
    print("   nomes = ['ana', 'bruno', 'carlos']")
    print("   maiusculas = {nome: nome.upper() for nome in nomes}")
    print()
    
    quadrados = {x: x**2 for x in range(1, 6)}
    pares = {x: x**2 for x in range(10) if x % 2 == 0}
    nomes = ['ana', 'bruno', 'carlos']
    maiusculas = {nome: nome.upper() for nome in nomes}
    
    print("   RESULTADO:")
    print(f"   → quadrados: {quadrados}")
    print(f"   → pares: {pares}")
    print(f"   → maiusculas: {maiusculas}")
    print()
    
    print("5. DICIONÁRIOS COM DIFERENTES TIPOS DE CHAVES:")
    print("   # Chaves de diferentes tipos (todas hashable)")
    print("   misto = {")
    print("       'string': 'valor1',")
    print("       42: 'valor2',")
    print("       (1, 2): 'valor3',")
    print("       True: 'valor4'")
    print("   }")
    print()
    
    misto = {
        'string': 'valor1',
        42: 'valor2',
        (1, 2): 'valor3',
        True: 'valor4'
    }
    
    print(f"   → misto: {misto}")
    print()
    
    print("   ⚠️  CUIDADO: True e 1 são considerados iguais!")
    print("   teste = {True: 'boolean', 1: 'inteiro'}")
    teste = {True: 'boolean', 1: 'inteiro'}
    print(f"   → teste: {teste}")
    print("   → Apenas uma entrada permanece (1 == True)")
    print()
    
    print("6. DICIONÁRIOS ANINHADOS:")
    print("   # Estrutura hierárquica")
    print("   empresa = {")
    print("       'nome': 'TechCorp',")
    print("       'funcionarios': {")
    print("           'dev': ['Ana', 'Bruno'],")
    print("           'design': ['Carlos', 'Diana']")
    print("       },")
    print("       'config': {")
    print("           'servidor': {'host': 'localhost', 'porta': 8080}")
    print("       }")
    print("   }")
    print()
    
    empresa = {
        'nome': 'TechCorp',
        'funcionarios': {
            'dev': ['Ana', 'Bruno'],
            'design': ['Carlos', 'Diana']
        },
        'config': {
            'servidor': {'host': 'localhost', 'porta': 8080}
        }
    }
    
    print(f"   → empresa['nome']: {empresa['nome']}")
    print(f"   → empresa['funcionarios']['dev']: {empresa['funcionarios']['dev']}")
    print(f"   → empresa['config']['servidor']['porta']: {empresa['config']['servidor']['porta']}")
    print()
    
    print("7. CHAVES INVÁLIDAS (NÃO HASHABLE):")
    print("   # Estas tentativas falharão:")
    print("   # dict_erro = {[1, 2]: 'lista'}     # ❌ TypeError")
    print("   # dict_erro = {{}: 'dict'}          # ❌ TypeError")
    print("   # dict_erro = {{'a': 1}: 'set'}     # ❌ TypeError")
    print()
    print("   ✅ Chaves válidas (hashable):")
    print("   • str, int, float, bool")
    print("   • tuple (se contém apenas hashable)")
    print("   • frozenset")
    print("   • None")
    print("   • Objetos customizados com __hash__()")
    print()

def acesso_modificacao():
    """
    Explora operações de acesso e modificação em dicionários.
    
    Analogia: Acessar dicionários é como consultar um catálogo.
    Você pode buscar, adicionar, modificar ou remover entradas.
    """
    print("=== ACESSO E MODIFICAÇÃO ===")
    print()
    
    print("1. ACESSO A VALORES:")
    dados = {'nome': 'João', 'idade': 28, 'cidade': 'Rio de Janeiro'}
    print(f"   Dicionário: {dados}")
    print()
    
    print("   # Acesso direto com []")
    print("   dados['nome']")
    print("   dados['idade']")
    print(f"   → Nome: {dados['nome']}")
    print(f"   → Idade: {dados['idade']}")
    print()
    
    print("   # Acesso seguro com get()")
    print("   dados.get('profissao')           # Retorna None")
    print("   dados.get('profissao', 'N/A')    # Retorna valor padrão")
    print(f"   → Profissão: {dados.get('profissao')}")
    print(f"   → Profissão (padrão): {dados.get('profissao', 'N/A')}")
    print()
    
    print("   # Diferença entre [] e get()")
    print("   # dados['inexistente']           # ❌ KeyError")
    print("   # dados.get('inexistente')       # ✅ None")
    print()
    
    print("2. MODIFICAÇÃO DE VALORES:")
    print("   # Alterando valor existente")
    print("   dados['idade'] = 29")
    dados['idade'] = 29
    print(f"   → Após alteração: {dados}")
    print()
    
    print("   # Adicionando nova chave-valor")
    print("   dados['profissao'] = 'Engenheiro'")
    dados['profissao'] = 'Engenheiro'
    print(f"   → Após adição: {dados}")
    print()
    
    print("3. REMOÇÃO DE ELEMENTOS:")
    print("   # Usando del")
    print("   del dados['cidade']")
    dados_copia = dados.copy()
    del dados_copia['cidade']
    print(f"   → Após del: {dados_copia}")
    print()
    
    print("   # Usando pop() - remove e retorna valor")
    print("   profissao = dados.pop('profissao')")
    profissao = dados.pop('profissao')
    print(f"   → Valor removido: {profissao}")
    print(f"   → Dicionário após pop: {dados}")
    print()
    
    print("   # pop() com valor padrão")
    print("   telefone = dados.pop('telefone', 'Não informado')")
    telefone = dados.pop('telefone', 'Não informado')
    print(f"   → Telefone: {telefone}")
    print()
    
    print("   # Usando popitem() - remove último item (Python ≥ 3.7)")
    dados['email'] = 'joao@email.com'
    dados['telefone'] = '11999999999'
    print(f"   → Antes do popitem: {dados}")
    chave, valor = dados.popitem()
    print(f"   → Item removido: {chave} = {valor}")
    print(f"   → Após popitem: {dados}")
    print()
    
    print("4. OPERAÇÕES DE ATUALIZAÇÃO:")
    dados1 = {'a': 1, 'b': 2}
    dados2 = {'b': 3, 'c': 4}
    
    print(f"   dados1: {dados1}")
    print(f"   dados2: {dados2}")
    print()
    
    print("   # update() - mescla dicionários")
    print("   dados1.update(dados2)")
    dados1.update(dados2)
    print(f"   → Após update: {dados1}")
    print("   → Chaves duplicadas são sobrescritas")
    print()
    
    print("   # update() com argumentos nomeados")
    dados1.update(d=5, e=6)
    print("   dados1.update(d=5, e=6)")
    print(f"   → Resultado: {dados1}")
    print()
    
    print("5. SETDEFAULT() - ADICIONA SE NÃO EXISTIR:")
    contador = {}
    palavras = ['python', 'java', 'python', 'c++', 'java', 'python']
    
    print(f"   Palavras: {palavras}")
    print("   # Contando com setdefault")
    print("   for palavra in palavras:")
    print("       contador.setdefault(palavra, 0)")
    print("       contador[palavra] += 1")
    print()
    
    for palavra in palavras:
        contador.setdefault(palavra, 0)
        contador[palavra] += 1
    
    print(f"   → Contador: {contador}")
    print()
    
    print("6. VERIFICAÇÃO DE EXISTÊNCIA:")
    dados_teste = {'nome': 'Ana', 'idade': 25}
    
    print(f"   Dicionário: {dados_teste}")
    print()
    print("   # Verificando chaves")
    print(f"   'nome' in dados_teste: {'nome' in dados_teste}")
    print(f"   'profissao' in dados_teste: {'profissao' in dados_teste}")
    print()
    print("   # Verificando valores")
    print(f"   'Ana' in dados_teste.values(): {'Ana' in dados_teste.values()}")
    print(f"   25 in dados_teste.values(): {25 in dados_teste.values()}")
    print()

def metodos_dicionarios():
    """
    Explora os métodos principais dos dicionários.
    
    Analogia: Métodos de dicionários são como ferramentas especializadas
    para diferentes tipos de consulta e manipulação de catálogos.
    """
    print("=== MÉTODOS DE DICIONÁRIOS ===")
    print()
    
    dados = {
        'nome': 'Maria',
        'idade': 32,
        'cidade': 'São Paulo',
        'profissao': 'Arquiteta'
    }
    
    print(f"   Dicionário base: {dados}")
    print()
    
    print("1. MÉTODOS DE VISUALIZAÇÃO:")
    print("   # keys() - retorna chaves")
    print("   dados.keys()")
    chaves = dados.keys()
    print(f"   → Chaves: {list(chaves)}")
    print(f"   → Tipo: {type(chaves)}")
    print()
    
    print("   # values() - retorna valores")
    print("   dados.values()")
    valores = dados.values()
    print(f"   → Valores: {list(valores)}")
    print(f"   → Tipo: {type(valores)}")
    print()
    
    print("   # items() - retorna pares chave-valor")
    print("   dados.items()")
    itens = dados.items()
    print(f"   → Itens: {list(itens)}")
    print(f"   → Tipo: {type(itens)}")
    print()
    
    print("2. ITERAÇÃO COM MÉTODOS:")
    print("   # Iterando sobre chaves")
    print("   for chave in dados.keys():")
    print("       print(f'{chave}: {dados[chave]}')")
    print()
    print("   RESULTADO:")
    for chave in dados.keys():
        print(f"   → {chave}: {dados[chave]}")
    print()
    
    print("   # Iterando sobre valores")
    print("   for valor in dados.values():")
    print("       print(f'Valor: {valor}')")
    print()
    print("   RESULTADO:")
    for valor in dados.values():
        print(f"   → Valor: {valor}")
    print()
    
    print("   # Iterando sobre itens (mais comum)")
    print("   for chave, valor in dados.items():")
    print("       print(f'{chave} = {valor}')")
    print()
    print("   RESULTADO:")
    for chave, valor in dados.items():
        print(f"   → {chave} = {valor}")
    print()
    
    print("3. MÉTODOS DE CÓPIA:")
    print("   # copy() - cópia superficial")
    print("   dados_copia = dados.copy()")
    dados_copia = dados.copy()
    print(f"   → Cópia: {dados_copia}")
    print(f"   → São objetos diferentes: {dados is not dados_copia}")
    print()
    
    print("   # Modificando a cópia")
    dados_copia['idade'] = 33
    print("   dados_copia['idade'] = 33")
    print(f"   → Original: {dados['idade']}")
    print(f"   → Cópia: {dados_copia['idade']}")
    print("   → Cópia superficial não afeta o original")
    print()
    
    print("4. MÉTODO CLEAR():")
    dados_temp = {'a': 1, 'b': 2, 'c': 3}
    print(f"   Antes do clear: {dados_temp}")
    dados_temp.clear()
    print("   dados_temp.clear()")
    print(f"   → Após clear: {dados_temp}")
    print()
    
    print("5. MÉTODOS DE BUSCA AVANÇADA:")
    estoque = {
        'notebook': 10,
        'mouse': 50,
        'teclado': 25,
        'monitor': 8
    }
    
    print(f"   Estoque: {estoque}")
    print()
    
    print("   # Encontrando produto com maior estoque")
    print("   produto_max = max(estoque, key=estoque.get)")
    produto_max = max(estoque, key=estoque.get)
    print(f"   → Produto com maior estoque: {produto_max} ({estoque[produto_max]} unidades)")
    print()
    
    print("   # Encontrando produto com menor estoque")
    print("   produto_min = min(estoque, key=estoque.get)")
    produto_min = min(estoque, key=estoque.get)
    print(f"   → Produto com menor estoque: {produto_min} ({estoque[produto_min]} unidades)")
    print()
    
    print("6. OPERAÇÕES DE CONJUNTO:")
    dict1 = {'a': 1, 'b': 2, 'c': 3}
    dict2 = {'b': 2, 'c': 4, 'd': 5}
    
    print(f"   dict1: {dict1}")
    print(f"   dict2: {dict2}")
    print()
    
    print("   # Chaves em comum")
    print("   dict1.keys() & dict2.keys()")
    chaves_comuns = dict1.keys() & dict2.keys()
    print(f"   → Chaves comuns: {chaves_comuns}")
    print()
    
    print("   # Chaves diferentes")
    print("   dict1.keys() - dict2.keys()")
    chaves_diff = dict1.keys() - dict2.keys()
    print(f"   → Chaves só em dict1: {chaves_diff}")
    print()
    
    print("   # Todas as chaves")
    print("   dict1.keys() | dict2.keys()")
    todas_chaves = dict1.keys() | dict2.keys()
    print(f"   → Todas as chaves: {todas_chaves}")
    print()

def dictionary_comprehensions():
    """
    Explora dictionary comprehensions - forma concisa de criar dicionários.
    
    Analogia: Dictionary comprehensions são como máquinas automáticas
    que criam catálogos seguindo regras específicas.
    """
    print("=== DICTIONARY COMPREHENSIONS ===")
    print()
    
    print("1. SINTAXE BÁSICA:")
    print("   {chave_expr: valor_expr for item in iterável}")
    print("   {chave_expr: valor_expr for item in iterável if condição}")
    print()
    
    print("2. EXEMPLOS BÁSICOS:")
    print("   # Quadrados dos números")
    print("   quadrados = {x: x**2 for x in range(1, 6)}")
    quadrados = {x: x**2 for x in range(1, 6)}
    print(f"   → {quadrados}")
    print()
    
    print("   # Comprimento de palavras")
    print("   palavras = ['python', 'java', 'javascript', 'go']")
    print("   tamanhos = {palavra: len(palavra) for palavra in palavras}")
    palavras = ['python', 'java', 'javascript', 'go']
    tamanhos = {palavra: len(palavra) for palavra in palavras}
    print(f"   → {tamanhos}")
    print()
    
    print("3. COM CONDIÇÕES:")
    print("   # Apenas números pares")
    print("   pares = {x: x**2 for x in range(10) if x % 2 == 0}")
    pares = {x: x**2 for x in range(10) if x % 2 == 0}
    print(f"   → {pares}")
    print()
    
    print("   # Palavras com mais de 4 letras")
    print("   palavras_longas = {p: len(p) for p in palavras if len(p) > 4}")
    palavras_longas = {p: len(p) for p in palavras if len(p) > 4}
    print(f"   → {palavras_longas}")
    print()
    
    print("4. TRANSFORMANDO ESTRUTURAS:")
    print("   # Lista de tuplas para dicionário")
    print("   dados = [('nome', 'Ana'), ('idade', 25), ('cidade', 'SP')]")
    print("   pessoa = {chave: valor for chave, valor in dados}")
    dados = [('nome', 'Ana'), ('idade', 25), ('cidade', 'SP')]
    pessoa = {chave: valor for chave, valor in dados}
    print(f"   → {pessoa}")
    print()
    
    print("   # Invertendo dicionário")
    print("   original = {'a': 1, 'b': 2, 'c': 3}")
    print("   invertido = {valor: chave for chave, valor in original.items()}")
    original = {'a': 1, 'b': 2, 'c': 3}
    invertido = {valor: chave for chave, valor in original.items()}
    print(f"   → Original: {original}")
    print(f"   → Invertido: {invertido}")
    print()
    
    print("5. PROCESSAMENTO DE TEXTO:")
    texto = "python é uma linguagem de programação"
    print(f"   Texto: '{texto}'")
    print()
    
    print("   # Contando caracteres")
    print("   contador_chars = {char: texto.count(char) for char in set(texto) if char != ' '}")
    contador_chars = {char: texto.count(char) for char in set(texto) if char != ' '}
    print(f"   → {contador_chars}")
    print()
    
    print("   # Contando palavras")
    print("   palavras_texto = texto.split()")
    print("   contador_palavras = {palavra: texto.split().count(palavra) for palavra in set(texto.split())}")
    palavras_texto = texto.split()
    contador_palavras = {palavra: texto.split().count(palavra) for palavra in set(texto.split())}
    print(f"   → {contador_palavras}")
    print()
    
    print("6. ANINHADAS E COMPLEXAS:")
    print("   # Tabela de multiplicação")
    print("   tabuada = {i: {j: i*j for j in range(1, 4)} for i in range(1, 4)}")
    tabuada = {i: {j: i*j for j in range(1, 4)} for i in range(1, 4)}
    print(f"   → {tabuada}")
    print()
    
    print("   # Processando dados de vendas")
    vendas = [
        {'produto': 'notebook', 'preco': 2500, 'qtd': 2},
        {'produto': 'mouse', 'preco': 50, 'qtd': 10},
        {'produto': 'teclado', 'preco': 150, 'qtd': 5}
    ]
    
    print("   vendas = [")
    for venda in vendas:
        print(f"       {venda},")
    print("   ]")
    print()
    
    print("   # Total por produto")
    print("   totais = {v['produto']: v['preco'] * v['qtd'] for v in vendas}")
    totais = {v['produto']: v['preco'] * v['qtd'] for v in vendas}
    print(f"   → {totais}")
    print()
    
    print("7. COMPARAÇÃO COM LOOP TRADICIONAL:")
    print("   # Forma tradicional")
    print("   resultado_loop = {}")
    print("   for x in range(1, 6):")
    print("       if x % 2 == 0:")
    print("           resultado_loop[x] = x**2")
    print()
    
    resultado_loop = {}
    for x in range(1, 6):
        if x % 2 == 0:
            resultado_loop[x] = x**2
    
    print("   # Com comprehension")
    print("   resultado_comp = {x: x**2 for x in range(1, 6) if x % 2 == 0}")
    resultado_comp = {x: x**2 for x in range(1, 6) if x % 2 == 0}
    
    print(f"   → Loop tradicional: {resultado_loop}")
    print(f"   → Comprehension: {resultado_comp}")
    print(f"   → Resultados iguais: {resultado_loop == resultado_comp}")
    print()

def dicionarios_especiais():
    """
    Explora variações especiais de dicionários do módulo collections.
    
    Analogia: Dicionários especiais são como catálogos especializados,
    cada um otimizado para um tipo específico de uso.
    """
    print("=== DICIONÁRIOS ESPECIAIS (collections) ===")
    print()
    
    print("1. OrderedDict - DICIONÁRIO ORDENADO:")
    print("   → Mantém ordem de inserção (Python < 3.7)")
    print("   → Métodos adicionais para reordenação")
    print("   → Útil quando ordem é crítica")
    print()
    
    print("   from collections import OrderedDict")
    print()
    print("   # Criando OrderedDict")
    print("   od = OrderedDict([('primeiro', 1), ('segundo', 2), ('terceiro', 3)])")
    od = OrderedDict([('primeiro', 1), ('segundo', 2), ('terceiro', 3)])
    print(f"   → {od}")
    print()
    
    print("   # move_to_end() - move item para o final")
    print("   od.move_to_end('primeiro')")
    od.move_to_end('primeiro')
    print(f"   → Após mover: {od}")
    print()
    
    print("   # move_to_end(last=False) - move para o início")
    print("   od.move_to_end('terceiro', last=False)")
    od.move_to_end('terceiro', last=False)
    print(f"   → Após mover para início: {od}")
    print()
    
    print("2. defaultdict - DICIONÁRIO COM VALOR PADRÃO:")
    print("   → Cria valores automaticamente para chaves inexistentes")
    print("   → Evita KeyError")
    print("   → Útil para agrupamentos e contadores")
    print()
    
    print("   from collections import defaultdict")
    print()
    print("   # defaultdict com lista")
    print("   grupos = defaultdict(list)")
    grupos = defaultdict(list)
    
    pessoas = [
        ('Ana', 'TI'),
        ('Bruno', 'RH'),
        ('Carlos', 'TI'),
        ('Diana', 'Vendas'),
        ('Eduardo', 'TI')
    ]
    
    print("   pessoas = [('Ana', 'TI'), ('Bruno', 'RH'), ...]")
    print("   for nome, depto in pessoas:")
    print("       grupos[depto].append(nome)")
    print()
    
    for nome, depto in pessoas:
        grupos[depto].append(nome)
    
    print(f"   → Grupos: {dict(grupos)}")
    print()
    
    print("   # defaultdict com int (contador)")
    print("   contador = defaultdict(int)")
    contador = defaultdict(int)
    
    texto = "python é uma linguagem python"
    print(f"   Texto: '{texto}'")
    print("   for palavra in texto.split():")
    print("       contador[palavra] += 1")
    print()
    
    for palavra in texto.split():
        contador[palavra] += 1
    
    print(f"   → Contador: {dict(contador)}")
    print()
    
    print("3. Counter - CONTADOR ESPECIALIZADO:")
    print("   → Subclasse de dict para contar objetos hashable")
    print("   → Métodos especializados para contagem")
    print("   → Muito útil para análise de frequência")
    print()
    
    print("   from collections import Counter")
    print()
    print("   # Contando elementos de uma lista")
    print("   frutas = ['maçã', 'banana', 'maçã', 'laranja', 'banana', 'maçã']")
    frutas = ['maçã', 'banana', 'maçã', 'laranja', 'banana', 'maçã']
    print("   contador_frutas = Counter(frutas)")
    contador_frutas = Counter(frutas)
    print(f"   → {contador_frutas}")
    print()
    
    print("   # Contando caracteres")
    print("   contador_chars = Counter('abracadabra')")
    contador_chars = Counter('abracadabra')
    print(f"   → {contador_chars}")
    print()
    
    print("   # Métodos especiais do Counter")
    print("   # most_common() - elementos mais comuns")
    print("   contador_frutas.most_common(2)")
    mais_comuns = contador_frutas.most_common(2)
    print(f"   → 2 mais comuns: {mais_comuns}")
    print()
    
    print("   # elements() - todos os elementos")
    print("   list(contador_chars.elements())")
    elementos = list(contador_chars.elements())
    print(f"   → Elementos: {elementos}")
    print()
    
    print("   # Operações matemáticas com Counters")
    c1 = Counter(['a', 'b', 'c', 'a'])
    c2 = Counter(['a', 'b', 'b', 'd'])
    
    print(f"   c1 = {c1}")
    print(f"   c2 = {c2}")
    print()
    print(f"   → c1 + c2: {c1 + c2}")  # Soma
    print(f"   → c1 - c2: {c1 - c2}")  # Subtração
    print(f"   → c1 & c2: {c1 & c2}")  # Interseção
    print(f"   → c1 | c2: {c1 | c2}")  # União
    print()
    
    print("4. COMPARAÇÃO DE PERFORMANCE:")
    
    # Teste de performance para contagem
    import time
    
    dados_teste = ['a', 'b', 'c'] * 10000
    
    # Método tradicional
    start = time.time()
    contador_tradicional = {}
    for item in dados_teste:
        contador_tradicional[item] = contador_tradicional.get(item, 0) + 1
    tempo_tradicional = time.time() - start
    
    # defaultdict
    start = time.time()
    contador_default = defaultdict(int)
    for item in dados_teste:
        contador_default[item] += 1
    tempo_default = time.time() - start
    
    # Counter
    start = time.time()
    contador_counter = Counter(dados_teste)
    tempo_counter = time.time() - start
    
    print(f"   Contando 30.000 elementos:")
    print(f"   → Método tradicional: {tempo_tradicional:.4f}s")
    print(f"   → defaultdict: {tempo_default:.4f}s")
    print(f"   → Counter: {tempo_counter:.4f}s")
    print()
    
    print("5. QUANDO USAR CADA TIPO:")
    print("   ┌─────────────────┬─────────────────────────────────────┐")
    print("   │      TIPO       │            QUANDO USAR              │")
    print("   ├─────────────────┼─────────────────────────────────────┤")
    print("   │ dict            │ Uso geral, performance crítica      │")
    print("   │ OrderedDict     │ Ordem de inserção é importante      │")
    print("   │ defaultdict     │ Evitar KeyError, agrupamentos       │")
    print("   │ Counter         │ Contagem de elementos, frequência   │")
    print("   └─────────────────┴─────────────────────────────────────┘")
    print()

def casos_uso_dicionarios():
    """
    Demonstra casos de uso práticos para dicionários.
    """
    print("=== CASOS DE USO PRÁTICOS ===")
    print()
    
    print("Caso 1: Sistema de Cache Inteligente")
    
    def sistema_cache_inteligente():
        """Cache com TTL (Time To Live) e estatísticas"""
        import time
        
        class CacheInteligente:
            def __init__(self, ttl_padrao=300):  # 5 minutos
                self.cache = {}
                self.ttl_padrao = ttl_padrao
                self.stats = {'hits': 0, 'misses': 0, 'expirados': 0}
            
            def get(self, chave):
                if chave in self.cache:
                    valor, timestamp, ttl = self.cache[chave]
                    if time.time() - timestamp < ttl:
                        self.stats['hits'] += 1
                        return valor
                    else:
                        del self.cache[chave]
                        self.stats['expirados'] += 1
                
                self.stats['misses'] += 1
                return None
            
            def set(self, chave, valor, ttl=None):
                ttl = ttl or self.ttl_padrao
                self.cache[chave] = (valor, time.time(), ttl)
            
            def get_stats(self):
                total = sum(self.stats.values())
                if total == 0:
                    return self.stats
                
                return {
                    **self.stats,
                    'hit_rate': self.stats['hits'] / total * 100
                }
        
        # Demonstração
        cache = CacheInteligente(ttl_padrao=2)  # 2 segundos para demo
        
        print("   # Usando o cache")
        cache.set('usuario_123', {'nome': 'Ana', 'email': 'ana@email.com'})
        cache.set('config_app', {'debug': True, 'version': '1.0'})
        
        print("   # Acessos")
        print(f"   → usuario_123: {cache.get('usuario_123')}")
        print(f"   → config_app: {cache.get('config_app')}")
        print(f"   → inexistente: {cache.get('inexistente')}")
        
        print(f"   → Estatísticas: {cache.get_stats()}")
        print()
        
        return cache
    
    sistema_cache_inteligente()
    
    print("Caso 2: Analisador de Logs")
    
    def analisador_logs():
        """Analisa logs de servidor web"""
        from collections import defaultdict, Counter
        
        # Simulando logs de servidor
        logs = [
            "192.168.1.1 GET /home 200",
            "192.168.1.2 GET /about 200", 
            "192.168.1.1 POST /login 401",
            "192.168.1.3 GET /home 200",
            "192.168.1.2 GET /products 404",
            "192.168.1.1 GET /home 200",
            "192.168.1.4 POST /contact 500",
            "192.168.1.1 GET /admin 403"
        ]
        
        # Estruturas para análise
        ips = Counter()
        endpoints = Counter()
        status_codes = Counter()
        ip_endpoints = defaultdict(set)
        
        print("   Analisando logs de servidor:")
        for log in logs[:3]:  # Mostra apenas primeiros 3
            print(f"   → {log}")
        print(f"   ... e mais {len(logs) - 3} entradas")
        print()
        
        # Processando logs
        for log in logs:
            partes = log.split()
            ip = partes[0]
            metodo = partes[1]
            endpoint = partes[2]
            status = partes[3]
            
            ips[ip] += 1
            endpoints[endpoint] += 1
            status_codes[status] += 1
            ip_endpoints[ip].add(endpoint)
        
        print("   ANÁLISE DOS LOGS:")
        print(f"   → IPs mais ativos: {ips.most_common(2)}")
        print(f"   → Endpoints mais acessados: {endpoints.most_common(2)}")
        print(f"   → Status codes: {dict(status_codes)}")
        print()
        
        print("   → Endpoints únicos por IP:")
        for ip, endpoints_visitados in ip_endpoints.items():
            print(f"     {ip}: {len(endpoints_visitados)} endpoints únicos")
        print()
        
        return {'ips': ips, 'endpoints': endpoints, 'status_codes': status_codes}
    
    analisador_logs()
    
    print("Caso 3: Sistema de Configuração Hierárquica")
    
    def sistema_configuracao():
        """Sistema de configuração com herança e override"""
        
        # Configurações base
        config_base = {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'timeout': 30
            },
            'cache': {
                'host': 'localhost',
                'port': 6379,
                'ttl': 3600
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(levelname)s - %(message)s'
            }
        }
        
        # Configurações por ambiente
        config_desenvolvimento = {
            'database': {
                'host': 'dev-db.local',
                'debug': True
            },
            'logging': {
                'level': 'DEBUG'
            }
        }
        
        config_producao = {
            'database': {
                'host': 'prod-db.empresa.com',
                'port': 5433,
                'ssl': True
            },
            'cache': {
                'host': 'cache-cluster.empresa.com',
                'ttl': 7200
            }
        }
        
        def mesclar_config(base, override):
            """Mescla configurações recursivamente"""
            resultado = base.copy()
            
            for chave, valor in override.items():
                if chave in resultado and isinstance(resultado[chave], dict) and isinstance(valor, dict):
                    resultado[chave] = mesclar_config(resultado[chave], valor)
                else:
                    resultado[chave] = valor
            
            return resultado
        
        # Gerando configurações finais
        config_dev = mesclar_config(config_base, config_desenvolvimento)
        config_prod = mesclar_config(config_base, config_producao)
        
        print("   CONFIGURAÇÕES POR AMBIENTE:")
        print()
        print("   Desenvolvimento - Database:")
        for chave, valor in config_dev['database'].items():
            print(f"   → {chave}: {valor}")
        print()
        
        print("   Produção - Database:")
        for chave, valor in config_prod['database'].items():
            print(f"   → {chave}: {valor}")
        print()
        
        return {'dev': config_dev, 'prod': config_prod}
    
    sistema_configuracao()

if __name__ == "__main__":
    print("MÓDULO 2.3 - DICIONÁRIOS E MAPEAMENTOS")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceito_dicionarios()
    print("\n" + "="*50 + "\n")
    
    criacao_sintaxe_dicionarios()
    print("\n" + "="*50 + "\n")
    
    acesso_modificacao()
    print("\n" + "="*50 + "\n")
    
    metodos_dicionarios()
    print("\n" + "="*50 + "\n")
    
    dictionary_comprehensions()
    print("\n" + "="*50 + "\n")
    
    dicionarios_especiais()
    print("\n" + "="*50 + "\n")
    
    casos_uso_dicionarios()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 2.3 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceito e características de dicionários")
    print("✅ Criação e sintaxe de dicionários")
    print("✅ Acesso e modificação de elementos")
    print("✅ Métodos principais de dicionários")
    print("✅ Dictionary comprehensions")
    print("✅ Dicionários especiais (OrderedDict, defaultdict, Counter)")
    print("✅ Casos de uso práticos")
    print("\n➡️  Próximo: Módulo 2.4 - Conjuntos (Sets) e Operações")