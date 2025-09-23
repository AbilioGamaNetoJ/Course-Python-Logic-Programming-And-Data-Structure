"""
Módulo: Operadores e Expressões
Tópico: Fundamentos de Lógica de Programação
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico

Objetivos de Aprendizado:
- Dominar todos os tipos de operadores em Python
- Compreender precedência e associatividade de operadores
- Construir expressões complexas de forma legível
- Aplicar operadores em situações práticas do cotidiano
- Evitar armadilhas comuns com operadores

Conceitos Abordados:
- Operadores aritméticos (+, -, *, /, //, %, **)
- Operadores de comparação (==, !=, <, >, <=, >=)
- Operadores lógicos (and, or, not)
- Operadores de atribuição (=, +=, -=, *=, etc.)
- Operadores de identidade (is, is not)
- Operadores de associação (in, not in)
- Precedência e parênteses
- Expressões booleanas complexas

Pré-requisitos:
- Módulos anteriores: Introdução ao Python, Tipos de Dados
- Conhecimento de variáveis e tipos básicos
"""

def operadores_aritmeticos():
    """
    Explora todos os operadores aritméticos do Python.
    
    Analogia: Operadores aritméticos são como as operações básicas
    da calculadora, mas com alguns extras que facilitam cálculos
    específicos de programação.
    
    Returns:
        None: Função demonstrativa
    """
    print("=== OPERADORES ARITMÉTICOS ===")
    print()
    
    # Valores para demonstração
    a = 17
    b = 5
    
    print(f"Usando a = {a} e b = {b}:")
    print()
    
    # Operações básicas
    print("1. OPERAÇÕES BÁSICAS:")
    print(f"   a + b = {a} + {b} = {a + b}    # Adição")
    print(f"   a - b = {a} - {b} = {a - b}   # Subtração")
    print(f"   a * b = {a} * {b} = {a * b}   # Multiplicação")
    print(f"   a / b = {a} / {b} = {a / b:.2f}  # Divisão (sempre float)")
    print()
    
    # Operações especiais
    print("2. OPERAÇÕES ESPECIAIS:")
    print(f"   a // b = {a} // {b} = {a // b}   # Divisão inteira (piso)")
    print(f"   a % b = {a} % {b} = {a % b}    # Módulo (resto da divisão)")
    print(f"   a ** b = {a} ** {b} = {a ** b}  # Potenciação")
    print()
    
    # Explicação detalhada do módulo
    print("3. ENTENDENDO O MÓDULO (%):")
    print("   O módulo retorna o RESTO da divisão inteira")
    print(f"   {a} ÷ {b} = {a // b} com resto {a % b}")
    print("   Visualização:")
    print(f"   {a} = {b} × {a // b} + {a % b}")
    print(f"   {a} = {b} × {a // b} + {a % b} = {b * (a // b) + (a % b)}")
    print()
    
    # Casos práticos do módulo
    print("4. USOS PRÁTICOS DO MÓDULO:")
    
    # Verificar se é par ou ímpar
    numero = 8
    eh_par = numero % 2 == 0
    print(f"   {numero} é par? {numero} % 2 = {numero % 2} → {eh_par}")
    
    # Verificar múltiplos
    numero = 15
    multiplo_de_3 = numero % 3 == 0
    multiplo_de_5 = numero % 5 == 0
    print(f"   {numero} é múltiplo de 3? {numero} % 3 = {numero % 3} → {multiplo_de_3}")
    print(f"   {numero} é múltiplo de 5? {numero} % 5 = {numero % 5} → {multiplo_de_5}")
    
    # Circular em lista (índice circular)
    tamanho_lista = 7
    indice = 10
    indice_circular = indice % tamanho_lista
    print(f"   Índice circular: posição {indice} em lista de {tamanho_lista} → posição {indice_circular}")
    print()
    
    # Operações com diferentes tipos
    print("5. OPERAÇÕES COM DIFERENTES TIPOS:")
    inteiro = 10
    decimal = 3.5
    
    print(f"   int + float: {inteiro} + {decimal} = {inteiro + decimal} (resultado: float)")
    print(f"   int * float: {inteiro} * {decimal} = {inteiro * decimal} (resultado: float)")
    
    # String com operadores
    texto = "Python"
    print(f"   string * int: '{texto}' * 3 = '{texto * 3}'")
    print(f"   string + string: '{texto}' + ' é legal' = '{texto + ' é legal'}'")
    print()

def operadores_comparacao():
    """
    Explora operadores de comparação e suas nuances.
    
    Analogia: Operadores de comparação são como juízes que decidem
    se uma afirmação é verdadeira ou falsa, sempre retornando
    um veredicto claro: True ou False.
    """
    print("=== OPERADORES DE COMPARAÇÃO ===")
    print()
    
    # Valores para demonstração
    x = 10
    y = 20
    z = 10
    
    print(f"Usando x = {x}, y = {y}, z = {z}:")
    print()
    
    # Comparações básicas
    print("1. COMPARAÇÕES BÁSICAS:")
    print(f"   x == z  →  {x} == {z}  →  {x == z}   # Igual")
    print(f"   x != y  →  {x} != {y}  →  {x != y}   # Diferente")
    print(f"   x < y   →  {x} < {y}   →  {x < y}    # Menor que")
    print(f"   x > y   →  {x} > {y}   →  {x > y}   # Maior que")
    print(f"   x <= z  →  {x} <= {z}  →  {x <= z}   # Menor ou igual")
    print(f"   y >= x  →  {y} >= {x}  →  {y >= x}   # Maior ou igual")
    print()
    
    # Comparações com strings
    print("2. COMPARAÇÕES COM STRINGS:")
    nome1 = "Ana"
    nome2 = "Bruno"
    nome3 = "Ana"
    
    print(f"   '{nome1}' == '{nome3}' → {nome1 == nome3}   # Igualdade exata")
    print(f"   '{nome1}' < '{nome2}' → {nome1 < nome2}    # Ordem alfabética")
    print(f"   '{nome1}'.lower() == 'ana' → {nome1.lower() == 'ana'}  # Comparação case-insensitive")
    print()
    
    # Comparações com diferentes tipos
    print("3. CUIDADOS COM TIPOS DIFERENTES:")
    numero_int = 5
    numero_float = 5.0
    numero_str = "5"
    
    print(f"   {numero_int} == {numero_float} → {numero_int == numero_float}     # int vs float: OK")
    print(f"   {numero_int} == '{numero_str}' → {numero_int == numero_str}    # int vs string: False")
    print(f"   {numero_int} == int('{numero_str}') → {numero_int == int(numero_str)}  # Após conversão: True")
    print()
    
    # Comparações encadeadas
    print("4. COMPARAÇÕES ENCADEADAS:")
    idade = 25
    print(f"   idade = {idade}")
    print(f"   18 <= idade <= 65 → 18 <= {idade} <= 65 → {18 <= idade <= 65}")
    print("   Equivale a: (18 <= idade) and (idade <= 65)")
    print(f"   Resultado: ({18 <= idade}) and ({idade <= 65}) = {(18 <= idade) and (idade <= 65)}")
    print()
    
    # Comparação de listas e estruturas
    print("5. COMPARAÇÃO DE ESTRUTURAS:")
    lista1 = [1, 2, 3]
    lista2 = [1, 2, 3]
    lista3 = [1, 2, 4]
    
    print(f"   {lista1} == {lista2} → {lista1 == lista2}   # Mesmo conteúdo")
    print(f"   {lista1} == {lista3} → {lista1 == lista3}   # Conteúdo diferente")
    print(f"   {lista1} < {lista3} → {lista1 < lista3}    # Comparação lexicográfica")
    print()

def operadores_logicos():
    """
    Explora operadores lógicos e tabelas verdade.
    
    Analogia: Operadores lógicos são como conectores em frases:
    - 'and' é como "e" (ambas condições devem ser verdadeiras)
    - 'or' é como "ou" (pelo menos uma deve ser verdadeira)
    - 'not' é como "não" (inverte a condição)
    """
    print("=== OPERADORES LÓGICOS ===")
    print()
    
    # Variáveis para demonstração
    tem_chuva = True
    tem_guarda_chuva = False
    tem_carro = True
    tem_dinheiro = True
    
    print("Situação:")
    print(f"   tem_chuva = {tem_chuva}")
    print(f"   tem_guarda_chuva = {tem_guarda_chuva}")
    print(f"   tem_carro = {tem_carro}")
    print(f"   tem_dinheiro = {tem_dinheiro}")
    print()
    
    # Operador AND
    print("1. OPERADOR AND (E):")
    print("   Só é True quando AMBAS as condições são True")
    
    pode_sair_a_pe = not tem_chuva and tem_guarda_chuva
    print(f"   Pode sair a pé? (not tem_chuva) and tem_guarda_chuva")
    print(f"   ({not tem_chuva}) and ({tem_guarda_chuva}) = {pode_sair_a_pe}")
    
    pode_viajar = tem_carro and tem_dinheiro
    print(f"   Pode viajar? tem_carro and tem_dinheiro")
    print(f"   ({tem_carro}) and ({tem_dinheiro}) = {pode_viajar}")
    print()
    
    # Operador OR
    print("2. OPERADOR OR (OU):")
    print("   É True quando PELO MENOS UMA condição é True")
    
    tem_transporte = tem_carro or tem_dinheiro  # dinheiro para táxi/ônibus
    print(f"   Tem transporte? tem_carro or tem_dinheiro")
    print(f"   ({tem_carro}) or ({tem_dinheiro}) = {tem_transporte}")
    
    vai_se_molhar = tem_chuva or not tem_guarda_chuva
    print(f"   Vai se molhar? tem_chuva or (not tem_guarda_chuva)")
    print(f"   ({tem_chuva}) or ({not tem_guarda_chuva}) = {vai_se_molhar}")
    print()
    
    # Operador NOT
    print("3. OPERADOR NOT (NÃO):")
    print("   Inverte o valor: True vira False, False vira True")
    
    nao_tem_chuva = not tem_chuva
    print(f"   not tem_chuva = not {tem_chuva} = {nao_tem_chuva}")
    
    nao_pode_viajar = not pode_viajar
    print(f"   not pode_viajar = not {pode_viajar} = {nao_pode_viajar}")
    print()
    
    # Tabela verdade
    print("4. TABELA VERDADE:")
    print("   ┌───────┬───────┬─────────┬────────┐")
    print("   │   A   │   B   │ A and B │ A or B │")
    print("   ├───────┼───────┼─────────┼────────┤")
    
    valores = [(True, True), (True, False), (False, True), (False, False)]
    for a, b in valores:
        and_result = a and b
        or_result = a or b
        print(f"   │ {str(a):5} │ {str(b):5} │ {str(and_result):7} │ {str(or_result):6} │")
    
    print("   └───────┴───────┴─────────┴────────┘")
    print()
    
    # Expressões complexas
    print("5. EXPRESSÕES LÓGICAS COMPLEXAS:")
    idade = 25
    tem_carteira = True
    tem_experiencia = False
    
    print(f"   idade = {idade}")
    print(f"   tem_carteira = {tem_carteira}")
    print(f"   tem_experiencia = {tem_experiencia}")
    print()
    
    # Pode dirigir?
    pode_dirigir = idade >= 18 and tem_carteira
    print(f"   Pode dirigir? (idade >= 18) and tem_carteira")
    print(f"   ({idade >= 18}) and ({tem_carteira}) = {pode_dirigir}")
    
    # Pode trabalhar como motorista?
    pode_ser_motorista = pode_dirigir and (idade >= 21 or tem_experiencia)
    print(f"   Pode ser motorista? pode_dirigir and (idade >= 21 or tem_experiencia)")
    print(f"   {pode_dirigir} and (({idade >= 21}) or ({tem_experiencia})) = {pode_ser_motorista}")
    print()

def operadores_atribuicao():
    """
    Explora operadores de atribuição e suas variações.
    
    Analogia: Operadores de atribuição são como atalhos para
    operações comuns. Em vez de escrever "x = x + 5", podemos
    escrever "x += 5" - mais rápido e claro.
    """
    print("=== OPERADORES DE ATRIBUIÇÃO ===")
    print()
    
    # Atribuição simples
    print("1. ATRIBUIÇÃO SIMPLES:")
    x = 10
    print(f"   x = 10  →  x = {x}")
    print()
    
    # Atribuições compostas
    print("2. ATRIBUIÇÕES COMPOSTAS:")
    
    # Adição
    print(f"   x += 5   (equivale a: x = x + 5)")
    print(f"   Antes: x = {x}")
    x += 5
    print(f"   Depois: x = {x}")
    print()
    
    # Subtração
    print(f"   x -= 3   (equivale a: x = x - 3)")
    print(f"   Antes: x = {x}")
    x -= 3
    print(f"   Depois: x = {x}")
    print()
    
    # Multiplicação
    print(f"   x *= 2   (equivale a: x = x * 2)")
    print(f"   Antes: x = {x}")
    x *= 2
    print(f"   Depois: x = {x}")
    print()
    
    # Divisão
    print(f"   x /= 4   (equivale a: x = x / 4)")
    print(f"   Antes: x = {x}")
    x /= 4
    print(f"   Depois: x = {x}")
    print()
    
    # Outros operadores
    y = 17
    print(f"   y = {y}")
    
    print(f"   y //= 5  (divisão inteira: y = y // 5)")
    print(f"   Antes: y = {y}")
    y //= 5
    print(f"   Depois: y = {y}")
    
    print(f"   y %= 2   (módulo: y = y % 2)")
    print(f"   Antes: y = {y}")
    y %= 2
    print(f"   Depois: y = {y}")
    
    z = 2
    print(f"   z = {z}")
    print(f"   z **= 3  (potência: z = z ** 3)")
    print(f"   Antes: z = {z}")
    z **= 3
    print(f"   Depois: z = {z}")
    print()
    
    # Com strings
    print("3. ATRIBUIÇÃO COM STRINGS:")
    mensagem = "Olá"
    print(f"   mensagem = '{mensagem}'")
    
    mensagem += " mundo!"
    print(f"   mensagem += ' mundo!'  →  mensagem = '{mensagem}'")
    
    palavra = "Ha"
    print(f"   palavra = '{palavra}'")
    palavra *= 3
    print(f"   palavra *= 3  →  palavra = '{palavra}'")
    print()
    
    # Atribuição múltipla
    print("4. ATRIBUIÇÃO MÚLTIPLA:")
    a, b, c = 1, 2, 3
    print(f"   a, b, c = 1, 2, 3  →  a={a}, b={b}, c={c}")
    
    # Troca de valores
    print(f"   Antes da troca: a={a}, b={b}")
    a, b = b, a
    print(f"   a, b = b, a  →  Depois: a={a}, b={b}")
    print()

def operadores_identidade_associacao():
    """
    Explora operadores de identidade (is) e associação (in).
    
    Analogia: 
    - 'is' verifica se duas variáveis apontam para o MESMO objeto na memória
    - 'in' verifica se um item está DENTRO de uma coleção
    """
    print("=== OPERADORES DE IDENTIDADE E ASSOCIAÇÃO ===")
    print()
    
    # Operadores de identidade
    print("1. OPERADORES DE IDENTIDADE (is, is not):")
    print("   'is' verifica se duas variáveis referenciam o MESMO objeto")
    print()
    
    # Exemplo com números pequenos (cache do Python)
    a = 5
    b = 5
    print(f"   a = {a}, b = {b}")
    print(f"   a == b  →  {a == b}   # Mesmo valor")
    print(f"   a is b  →  {a is b}    # Mesmo objeto (Python cacheia números pequenos)")
    print(f"   id(a) = {id(a)}, id(b) = {id(b)}")
    print()
    
    # Exemplo com listas
    lista1 = [1, 2, 3]
    lista2 = [1, 2, 3]
    lista3 = lista1
    
    print(f"   lista1 = {lista1}")
    print(f"   lista2 = {lista2}")
    print(f"   lista3 = lista1  # lista3 aponta para o mesmo objeto que lista1")
    print()
    
    print(f"   lista1 == lista2  →  {lista1 == lista2}   # Mesmo conteúdo")
    print(f"   lista1 is lista2  →  {lista1 is lista2}   # Objetos diferentes")
    print(f"   lista1 is lista3  →  {lista1 is lista3}   # Mesmo objeto")
    print()
    
    # Exemplo com None
    valor = None
    print(f"   valor = {valor}")
    print(f"   valor is None     →  {valor is None}")
    print(f"   valor is not None →  {valor is not None}")
    print("   💡 Use sempre 'is None' ao invés de '== None'")
    print()
    
    # Operadores de associação
    print("2. OPERADORES DE ASSOCIAÇÃO (in, not in):")
    print("   'in' verifica se um elemento está presente em uma sequência")
    print()
    
    # Com strings
    frase = "Python é incrível"
    print(f"   frase = '{frase}'")
    print(f"   'Python' in frase     →  {'Python' in frase}")
    print(f"   'Java' in frase       →  {'Java' in frase}")
    print(f"   'python' in frase     →  {'python' in frase}  # Case sensitive!")
    print(f"   'python' in frase.lower()  →  {'python' in frase.lower()}")
    print()
    
    # Com listas
    numeros = [1, 2, 3, 4, 5]
    print(f"   numeros = {numeros}")
    print(f"   3 in numeros      →  {3 in numeros}")
    print(f"   6 in numeros      →  {6 in numeros}")
    print(f"   6 not in numeros  →  {6 not in numeros}")
    print()
    
    # Com dicionários (verifica chaves)
    pessoa = {'nome': 'Ana', 'idade': 25, 'cidade': 'São Paulo'}
    print(f"   pessoa = {pessoa}")
    print(f"   'nome' in pessoa     →  {'nome' in pessoa}")
    print(f"   'Ana' in pessoa      →  {'Ana' in pessoa}   # Verifica chaves, não valores")
    print(f"   'Ana' in pessoa.values()  →  {'Ana' in pessoa.values()}  # Para verificar valores")
    print()

def precedencia_operadores():
    """
    Explica a precedência (ordem de execução) dos operadores.
    
    Analogia: Como na matemática, existe uma ordem para resolver
    operações. Multiplicação antes de soma, parênteses primeiro, etc.
    """
    print("=== PRECEDÊNCIA DE OPERADORES ===")
    print()
    
    print("1. ORDEM DE PRECEDÊNCIA (do maior para o menor):")
    print("   1. ()           # Parênteses")
    print("   2. **           # Potenciação")
    print("   3. *, /, //, %  # Multiplicação, divisão, divisão inteira, módulo")
    print("   4. +, -         # Adição, subtração")
    print("   5. <, <=, >, >=, ==, != # Comparações")
    print("   6. not          # Negação lógica")
    print("   7. and          # E lógico")
    print("   8. or           # Ou lógico")
    print()
    
    # Exemplos práticos
    print("2. EXEMPLOS PRÁTICOS:")
    
    # Exemplo 1: Aritmética
    resultado1 = 2 + 3 * 4
    print(f"   2 + 3 * 4 = {resultado1}")
    print("   Ordem: primeiro 3 * 4 = 12, depois 2 + 12 = 14")
    
    resultado2 = (2 + 3) * 4
    print(f"   (2 + 3) * 4 = {resultado2}")
    print("   Ordem: primeiro (2 + 3) = 5, depois 5 * 4 = 20")
    print()
    
    # Exemplo 2: Potenciação
    resultado3 = 2 ** 3 ** 2
    print(f"   2 ** 3 ** 2 = {resultado3}")
    print("   Potenciação é associativa à direita: 2 ** (3 ** 2) = 2 ** 9 = 512")
    
    resultado4 = (2 ** 3) ** 2
    print(f"   (2 ** 3) ** 2 = {resultado4}")
    print("   Com parênteses: (2 ** 3) ** 2 = 8 ** 2 = 64")
    print()
    
    # Exemplo 3: Lógica e comparação
    x = 5
    y = 10
    z = 15
    
    print(f"   x = {x}, y = {y}, z = {z}")
    
    resultado5 = x < y and y < z
    print(f"   x < y and y < z = {x} < {y} and {y} < {z} = {resultado5}")
    print("   Ordem: primeiro as comparações, depois o 'and'")
    
    resultado6 = not x > y or z > y
    print(f"   not x > y or z > y = not {x} > {y} or {z} > {y} = {resultado6}")
    print("   Ordem: comparações → not → or")
    print("   Passo a passo: not False or True = True or True = True")
    print()
    
    # Exemplo 4: Expressão complexa
    print("3. EXPRESSÃO COMPLEXA:")
    a = 2
    b = 3
    c = 4
    
    expressao = a + b * c ** 2 > 20 and not a == b
    print(f"   a = {a}, b = {b}, c = {c}")
    print(f"   a + b * c ** 2 > 20 and not a == b")
    print("   Passo a passo:")
    print(f"   1. c ** 2 = {c} ** 2 = {c ** 2}")
    print(f"   2. b * (c ** 2) = {b} * {c ** 2} = {b * c ** 2}")
    print(f"   3. a + (b * c ** 2) = {a} + {b * c ** 2} = {a + b * c ** 2}")
    print(f"   4. (a + b * c ** 2) > 20 = {a + b * c ** 2} > 20 = {a + b * c ** 2 > 20}")
    print(f"   5. a == b = {a} == {b} = {a == b}")
    print(f"   6. not (a == b) = not {a == b} = {not a == b}")
    print(f"   7. {a + b * c ** 2 > 20} and {not a == b} = {expressao}")
    print()
    
    print("4. DICAS PARA BOA PRÁTICA:")
    print("   ✅ Use parênteses para deixar a intenção clara")
    print("   ✅ Quebre expressões complexas em partes menores")
    print("   ✅ Prefira legibilidade à economia de caracteres")
    print()
    
    # Exemplo de refatoração
    print("   Exemplo de refatoração:")
    print("   ❌ Difícil de ler:")
    print("   if idade >= 18 and tem_carteira and not tem_multas or eh_instrutor:")
    print()
    print("   ✅ Mais claro:")
    print("   pode_dirigir = idade >= 18 and tem_carteira and not tem_multas")
    print("   if pode_dirigir or eh_instrutor:")
    print()

def exemplos_praticos():
    """
    Exemplos práticos integrando todos os operadores.
    """
    print("=== EXEMPLOS PRÁTICOS INTEGRADOS ===")
    print()
    
    # Exemplo 1: Sistema de desconto
    print("Exemplo 1: Sistema de Desconto em Loja")
    preco_original = 100.0
    quantidade = 3
    eh_cliente_vip = True
    tem_cupom = False
    
    print(f"Preço original: R$ {preco_original}")
    print(f"Quantidade: {quantidade}")
    print(f"Cliente VIP: {eh_cliente_vip}")
    print(f"Tem cupom: {tem_cupom}")
    print()
    
    # Cálculo do subtotal
    subtotal = preco_original * quantidade
    print(f"Subtotal: R$ {subtotal}")
    
    # Desconto por quantidade
    desconto_quantidade = 0.1 if quantidade >= 3 else 0
    print(f"Desconto por quantidade (≥3): {desconto_quantidade * 100}%")
    
    # Desconto VIP
    desconto_vip = 0.15 if eh_cliente_vip else 0
    print(f"Desconto VIP: {desconto_vip * 100}%")
    
    # Desconto cupom
    desconto_cupom = 0.05 if tem_cupom else 0
    print(f"Desconto cupom: {desconto_cupom * 100}%")
    
    # Desconto total (não pode passar de 25%)
    desconto_total = min(desconto_quantidade + desconto_vip + desconto_cupom, 0.25)
    print(f"Desconto total (máx 25%): {desconto_total * 100}%")
    
    # Valor final
    valor_desconto = subtotal * desconto_total
    valor_final = subtotal - valor_desconto
    
    print(f"Valor do desconto: R$ {valor_desconto:.2f}")
    print(f"Valor final: R$ {valor_final:.2f}")
    print()
    
    # Exemplo 2: Validador de senha
    print("Exemplo 2: Validador de Senha")
    senha = "MinhaSenh@123"
    
    print(f"Senha: '{senha}'")
    print("Critérios de validação:")
    
    # Verificações individuais
    tem_minimo_8_chars = len(senha) >= 8
    tem_maiuscula = any(c.isupper() for c in senha)
    tem_minuscula = any(c.islower() for c in senha)
    tem_numero = any(c.isdigit() for c in senha)
    tem_especial = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in senha)
    
    print(f"✓ Mínimo 8 caracteres: {tem_minimo_8_chars}")
    print(f"✓ Tem maiúscula: {tem_maiuscula}")
    print(f"✓ Tem minúscula: {tem_minuscula}")
    print(f"✓ Tem número: {tem_numero}")
    print(f"✓ Tem caractere especial: {tem_especial}")
    
    # Validação final
    senha_valida = (tem_minimo_8_chars and tem_maiuscula and 
                   tem_minuscula and tem_numero and tem_especial)
    
    print(f"Senha válida: {senha_valida}")
    print()
    
    # Exemplo 3: Calculadora de IMC com classificação
    print("Exemplo 3: Calculadora de IMC")
    peso = 70.5
    altura = 1.75
    
    print(f"Peso: {peso} kg")
    print(f"Altura: {altura} m")
    
    # Cálculo do IMC
    imc = peso / (altura ** 2)
    print(f"IMC: {imc:.2f}")
    
    # Classificação usando operadores de comparação
    if imc < 18.5:
        classificacao = "Abaixo do peso"
    elif 18.5 <= imc < 25:
        classificacao = "Peso normal"
    elif 25 <= imc < 30:
        classificacao = "Sobrepeso"
    else:
        classificacao = "Obesidade"
    
    print(f"Classificação: {classificacao}")
    
    # Recomendações usando operadores lógicos
    precisa_ganhar_peso = imc < 18.5
    precisa_perder_peso = imc >= 25
    peso_ideal = not (precisa_ganhar_peso or precisa_perder_peso)
    
    print(f"Precisa ganhar peso: {precisa_ganhar_peso}")
    print(f"Precisa perder peso: {precisa_perder_peso}")
    print(f"Peso ideal: {peso_ideal}")
    print()

def exercicios():
    """
    Exercícios progressivos para fixação dos operadores.
    """
    print("=== EXERCÍCIOS DE FIXAÇÃO ===")
    print()
    
    print("NÍVEL 1 - Operadores Básicos:")
    print("1. Calcule a área de um retângulo (largura * altura)")
    print("2. Verifique se um número é par usando o operador módulo")
    print("3. Compare duas idades e determine qual é maior")
    print("4. Concatene nome e sobrenome com um espaço")
    print("5. Calcule o quadrado de um número usando **")
    print()
    
    print("NÍVEL 2 - Operadores Lógicos:")
    print("6. Determine se uma pessoa pode votar (idade >= 16)")
    print("7. Verifique se um ano é bissexto (divisível por 4 e não por 100, ou por 400)")
    print("8. Crie um sistema de login (usuário E senha corretos)")
    print("9. Determine se um triângulo é válido (soma de dois lados > terceiro lado)")
    print("10. Verifique se um número está em um intervalo (10 <= x <= 50)")
    print()
    
    print("NÍVEL 3 - Expressões Complexas:")
    print("11. Sistema de aprovação: média >= 7 E frequência >= 75%")
    print("12. Calculadora de frete: peso, distância e urgência")
    print("13. Validador de email: tem @ E tem . E não começa com número")
    print("14. Sistema de pontuação de jogo com bônus e penalidades")
    print("15. Calculadora de imposto progressivo com faixas")
    print()
    
    # Exemplo de solução
    print("EXEMPLO DE SOLUÇÃO - Exercício 2:")
    print("# Verificar se um número é par")
    print("numero = 42")
    print("eh_par = numero % 2 == 0")
    print("print(f'{numero} é par: {eh_par}')")
    print()
    
    # Executando o exemplo
    numero = 42
    eh_par = numero % 2 == 0
    print("RESULTADO:")
    print(f"{numero} é par: {eh_par}")
    print(f"Explicação: {numero} % 2 = {numero % 2}, e {numero % 2} == 0 é {eh_par}")
    print()

def resumo_operadores():
    """
    Resumo visual de todos os operadores aprendidos.
    """
    print("=== RESUMO DOS OPERADORES ===")
    print()
    
    print("┌─────────────────┬─────────────────┬─────────────────────────────────┐")
    print("│      TIPO       │   OPERADORES    │           DESCRIÇÃO             │")
    print("├─────────────────┼─────────────────┼─────────────────────────────────┤")
    print("│ Aritméticos     │ +, -, *, /      │ Operações matemáticas básicas   │")
    print("│                 │ //, %, **       │ Div. inteira, módulo, potência  │")
    print("├─────────────────┼─────────────────┼─────────────────────────────────┤")
    print("│ Comparação      │ ==, !=          │ Igual, diferente                │")
    print("│                 │ <, >, <=, >=    │ Menor, maior, menor/maior igual │")
    print("├─────────────────┼─────────────────┼─────────────────────────────────┤")
    print("│ Lógicos         │ and, or, not    │ E, ou, não lógicos              │")
    print("├─────────────────┼─────────────────┼─────────────────────────────────┤")
    print("│ Atribuição      │ =               │ Atribuição simples              │")
    print("│                 │ +=, -=, *=, /=  │ Atribuições compostas           │")
    print("├─────────────────┼─────────────────┼─────────────────────────────────┤")
    print("│ Identidade      │ is, is not      │ Mesmo objeto na memória         │")
    print("├─────────────────┼─────────────────┼─────────────────────────────────┤")
    print("│ Associação      │ in, not in      │ Pertence à sequência            │")
    print("└─────────────────┴─────────────────┴─────────────────────────────────┘")
    print()
    
    print("PRECEDÊNCIA (ordem de execução):")
    print("1. ()  →  2. **  →  3. *, /, //, %  →  4. +, -")
    print("5. <, <=, >, >=, ==, !=  →  6. not  →  7. and  →  8. or")
    print()
    
    print("DICAS IMPORTANTES:")
    print("✅ Use parênteses para clareza")
    print("✅ Quebre expressões complexas")
    print("✅ Teste sempre suas expressões lógicas")
    print("✅ Cuidado com tipos diferentes em comparações")
    print("✅ Use 'is None' ao invés de '== None'")
    print()

if __name__ == "__main__":
    # Demonstração completa do módulo
    print("🐍 CURSO DE PYTHON - MÓDULO 1.3: OPERADORES E EXPRESSÕES 🐍")
    print("=" * 70)
    print()
    
    # Execução sequencial de todos os conceitos
    operadores_aritmeticos()
    print("-" * 50)
    
    operadores_comparacao()
    print("-" * 50)
    
    operadores_logicos()
    print("-" * 50)
    
    operadores_atribuicao()
    print("-" * 50)
    
    operadores_identidade_associacao()
    print("-" * 50)
    
    precedencia_operadores()
    print("-" * 50)
    
    exemplos_praticos()
    print("-" * 50)
    
    resumo_operadores()
    print("-" * 50)
    
    exercicios()
    
    print("=" * 70)
    print("🎉 PARABÉNS! Você dominou os Operadores e Expressões!")
    print("Próximo módulo: Estruturas Condicionais")
    print("=" * 70)