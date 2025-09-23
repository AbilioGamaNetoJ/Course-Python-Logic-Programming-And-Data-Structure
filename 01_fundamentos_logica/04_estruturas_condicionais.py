"""
Módulo: Estruturas Condicionais
Tópico: Fundamentos de Lógica de Programação
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico

Objetivos de Aprendizado:
- Compreender o conceito de tomada de decisão em programação
- Dominar as estruturas if, elif e else
- Construir condições complexas usando operadores lógicos
- Aplicar estruturas condicionais em problemas reais
- Evitar armadilhas comuns e escrever código limpo

Conceitos Abordados:
- Estrutura if simples
- Estrutura if-else
- Estrutura if-elif-else
- Condições aninhadas (nested if)
- Operador ternário (conditional expression)
- Valores truthy e falsy
- Boas práticas em estruturas condicionais

Pré-requisitos:
- Módulos anteriores: Tipos de Dados, Operadores
- Conhecimento de operadores de comparação e lógicos
- Compreensão de valores booleanos

Complexidade Temporal: O(1) - Avaliação de condições é constante
Complexidade Espacial: O(1) - Não usa espaço adicional significativo
"""

def conceito_estruturas_condicionais():
    """
    Introduz o conceito fundamental de estruturas condicionais.
    
    Analogia: Estruturas condicionais são como semáforos no trânsito.
    Dependendo da cor (condição), tomamos uma ação diferente:
    - Verde: seguir em frente
    - Amarelo: reduzir velocidade
    - Vermelho: parar
    
    Returns:
        None: Função demonstrativa
    """
    print("=== CONCEITO DE ESTRUTURAS CONDICIONAIS ===")
    print()
    
    print("1. O QUE SÃO ESTRUTURAS CONDICIONAIS?")
    print("   → Permitem que o programa tome decisões")
    print("   → Executam diferentes códigos baseados em condições")
    print("   → São fundamentais para criar programas inteligentes")
    print()
    
    print("2. ANALOGIA DO SEMÁFORO:")
    print("   🚦 Semáforo Verde  → if temperatura > 25: usar_shorts()")
    print("   🚦 Semáforo Amarelo → elif temperatura > 15: usar_casaco_leve()")
    print("   🚦 Semáforo Vermelho → else: usar_casaco_pesado()")
    print()
    
    print("3. FLUXO DE DECISÃO:")
    print("   ┌─────────────┐")
    print("   │  Condição?  │")
    print("   └──────┬──────┘")
    print("          │")
    print("     ┌────▼────┐")
    print("     │ True?   │")
    print("   ┌─▼─┐     ┌─▼─┐")
    print("   │Sim│     │Não│")
    print("   └─┬─┘     └─┬─┘")
    print("     │         │")
    print("   ┌─▼─┐     ┌─▼─┐")
    print("   │Ação│     │Outra│")
    print("   │ A  │     │Ação│")
    print("   └───┘     └───┘")
    print()
    
    # Exemplo prático simples
    print("4. EXEMPLO PRÁTICO:")
    idade = 18
    print(f"   idade = {idade}")
    print("   if idade >= 18:")
    print("       print('Pode votar!')")
    print("   else:")
    print("       print('Não pode votar ainda')")
    print()
    print("   Resultado:")
    
    if idade >= 18:
        print("   → Pode votar!")
    else:
        print("   → Não pode votar ainda")
    print()

def estrutura_if_simples():
    """
    Explora a estrutura if simples - a base de todas as condicionais.
    
    Analogia: O if é como uma porta que só se abre se você tiver a chave certa.
    Se a condição for verdadeira (você tem a chave), a porta abre e o código executa.
    """
    print("=== ESTRUTURA IF SIMPLES ===")
    print()
    
    print("1. SINTAXE BÁSICA:")
    print("   if condição:")
    print("       # código a ser executado se condição for True")
    print("       ação()")
    print()
    print("   ⚠️  ATENÇÃO: Os dois pontos (:) são obrigatórios!")
    print("   ⚠️  INDENTAÇÃO (espaços) é obrigatória em Python!")
    print()
    
    # Exemplos práticos
    print("2. EXEMPLOS PRÁTICOS:")
    
    # Exemplo 1: Verificação de idade
    print("   Exemplo 1: Verificação de maioridade")
    idade = 20
    print(f"   idade = {idade}")
    print("   if idade >= 18:")
    print("       print('É maior de idade')")
    print()
    print("   Resultado:")
    if idade >= 18:
        print("   → É maior de idade")
    print()
    
    # Exemplo 2: Verificação de nota
    print("   Exemplo 2: Verificação de aprovação")
    nota = 8.5
    print(f"   nota = {nota}")
    print("   if nota >= 7.0:")
    print("       print('Aprovado!')")
    print("       print('Parabéns!')")
    print()
    print("   Resultado:")
    if nota >= 7.0:
        print("   → Aprovado!")
        print("   → Parabéns!")
    print()
    
    # Exemplo 3: Verificação de string
    print("   Exemplo 3: Verificação de senha")
    senha = "123456"
    print(f"   senha = '{senha}'")
    print("   if len(senha) >= 6:")
    print("       print('Senha tem tamanho adequado')")
    print()
    print("   Resultado:")
    if len(senha) >= 6:
        print("   → Senha tem tamanho adequado")
    print()
    
    # Exemplo 4: Múltiplas condições
    print("   Exemplo 4: Múltiplas verificações independentes")
    temperatura = 30
    chuva = False
    
    print(f"   temperatura = {temperatura}")
    print(f"   chuva = {chuva}")
    print()
    print("   if temperatura > 25:")
    print("       print('Está calor!')")
    print("   if not chuva:")
    print("       print('Não está chovendo')")
    print("   if temperatura > 25 and not chuva:")
    print("       print('Perfeito para praia!')")
    print()
    print("   Resultado:")
    
    if temperatura > 25:
        print("   → Está calor!")
    if not chuva:
        print("   → Não está chovendo")
    if temperatura > 25 and not chuva:
        print("   → Perfeito para praia!")
    print()

def estrutura_if_else():
    """
    Explora a estrutura if-else - decisões binárias.
    
    Analogia: If-else é como uma bifurcação na estrada.
    Você sempre vai por um caminho OU outro, nunca pelos dois.
    """
    print("=== ESTRUTURA IF-ELSE ===")
    print()
    
    print("1. SINTAXE:")
    print("   if condição:")
    print("       # código se condição for True")
    print("   else:")
    print("       # código se condição for False")
    print()
    print("   → SEMPRE executa um dos dois blocos")
    print("   → Nunca executa ambos")
    print("   → Nunca deixa de executar pelo menos um")
    print()
    
    # Exemplos práticos
    print("2. EXEMPLOS PRÁTICOS:")
    
    # Exemplo 1: Par ou ímpar
    print("   Exemplo 1: Verificar se número é par ou ímpar")
    numero = 7
    print(f"   numero = {numero}")
    print("   if numero % 2 == 0:")
    print("       print(f'{numero} é par')")
    print("   else:")
    print("       print(f'{numero} é ímpar')")
    print()
    print("   Resultado:")
    if numero % 2 == 0:
        print(f"   → {numero} é par")
    else:
        print(f"   → {numero} é ímpar")
    print()
    
    # Exemplo 2: Maior ou menor de idade
    print("   Exemplo 2: Classificação por idade")
    idade = 16
    print(f"   idade = {idade}")
    print("   if idade >= 18:")
    print("       print('Maior de idade')")
    print("       status = 'adulto'")
    print("   else:")
    print("       print('Menor de idade')")
    print("       status = 'menor'")
    print()
    print("   Resultado:")
    if idade >= 18:
        print("   → Maior de idade")
        status = 'adulto'
    else:
        print("   → Menor de idade")
        status = 'menor'
    print(f"   → Status: {status}")
    print()
    
    # Exemplo 3: Validação de login
    print("   Exemplo 3: Sistema de login")
    usuario_correto = "admin"
    senha_correta = "123456"
    usuario = "admin"
    senha = "123456"
    
    print(f"   usuario = '{usuario}'")
    print(f"   senha = '{senha}'")
    print("   if usuario == usuario_correto and senha == senha_correta:")
    print("       print('Login realizado com sucesso!')")
    print("   else:")
    print("       print('Usuário ou senha incorretos')")
    print()
    print("   Resultado:")
    if usuario == usuario_correto and senha == senha_correta:
        print("   → Login realizado com sucesso!")
    else:
        print("   → Usuário ou senha incorretos")
    print()
    
    # Exemplo 4: Cálculo de desconto
    print("   Exemplo 4: Sistema de desconto")
    valor_compra = 150.0
    limite_desconto = 100.0
    
    print(f"   valor_compra = R$ {valor_compra}")
    print(f"   limite_desconto = R$ {limite_desconto}")
    print("   if valor_compra >= limite_desconto:")
    print("       desconto = valor_compra * 0.1")
    print("       print(f'Desconto de 10%: R$ {desconto:.2f}')")
    print("   else:")
    print("       desconto = 0")
    print("       print('Sem desconto')")
    print()
    print("   Resultado:")
    if valor_compra >= limite_desconto:
        desconto = valor_compra * 0.1
        print(f"   → Desconto de 10%: R$ {desconto:.2f}")
    else:
        desconto = 0
        print("   → Sem desconto")
    
    valor_final = valor_compra - desconto
    print(f"   → Valor final: R$ {valor_final:.2f}")
    print()

def estrutura_if_elif_else():
    """
    Explora a estrutura if-elif-else - múltiplas condições.
    
    Analogia: If-elif-else é como um menu de restaurante.
    Você escolhe UMA opção entre várias disponíveis.
    O garçom verifica sua escolha na ordem até encontrar uma válida.
    """
    print("=== ESTRUTURA IF-ELIF-ELSE ===")
    print()
    
    print("1. SINTAXE:")
    print("   if condição1:")
    print("       # código se condição1 for True")
    print("   elif condição2:")
    print("       # código se condição2 for True")
    print("   elif condição3:")
    print("       # código se condição3 for True")
    print("   else:")
    print("       # código se nenhuma condição for True")
    print()
    print("   → Avalia condições na ORDEM")
    print("   → Para na PRIMEIRA condição verdadeira")
    print("   → 'else' é opcional (captura todos os outros casos)")
    print()
    
    # Exemplo 1: Classificação de notas
    print("2. EXEMPLO 1: Sistema de notas")
    nota = 8.5
    print(f"   nota = {nota}")
    print("   if nota >= 9.0:")
    print("       conceito = 'A'")
    print("   elif nota >= 8.0:")
    print("       conceito = 'B'")
    print("   elif nota >= 7.0:")
    print("       conceito = 'C'")
    print("   elif nota >= 6.0:")
    print("       conceito = 'D'")
    print("   else:")
    print("       conceito = 'F'")
    print()
    print("   Resultado:")
    
    if nota >= 9.0:
        conceito = 'A'
    elif nota >= 8.0:
        conceito = 'B'
    elif nota >= 7.0:
        conceito = 'C'
    elif nota >= 6.0:
        conceito = 'D'
    else:
        conceito = 'F'
    
    print(f"   → Conceito: {conceito}")
    print()
    
    # Exemplo 2: Classificação de IMC
    print("3. EXEMPLO 2: Calculadora de IMC")
    peso = 70
    altura = 1.75
    imc = peso / (altura ** 2)
    
    print(f"   peso = {peso} kg")
    print(f"   altura = {altura} m")
    print(f"   imc = {imc:.2f}")
    print()
    print("   if imc < 18.5:")
    print("       classificacao = 'Abaixo do peso'")
    print("   elif imc < 25:")
    print("       classificacao = 'Peso normal'")
    print("   elif imc < 30:")
    print("       classificacao = 'Sobrepeso'")
    print("   elif imc < 35:")
    print("       classificacao = 'Obesidade grau I'")
    print("   else:")
    print("       classificacao = 'Obesidade grau II ou III'")
    print()
    print("   Resultado:")
    
    if imc < 18.5:
        classificacao = 'Abaixo do peso'
    elif imc < 25:
        classificacao = 'Peso normal'
    elif imc < 30:
        classificacao = 'Sobrepeso'
    elif imc < 35:
        classificacao = 'Obesidade grau I'
    else:
        classificacao = 'Obesidade grau II ou III'
    
    print(f"   → Classificação: {classificacao}")
    print()
    
    # Exemplo 3: Sistema de faixas etárias
    print("4. EXEMPLO 3: Classificação por faixa etária")
    idade = 25
    print(f"   idade = {idade}")
    print("   if idade < 13:")
    print("       categoria = 'Criança'")
    print("       atividade = 'Brincar e estudar'")
    print("   elif idade < 18:")
    print("       categoria = 'Adolescente'")
    print("       atividade = 'Estudar e descobrir vocação'")
    print("   elif idade < 60:")
    print("       categoria = 'Adulto'")
    print("       atividade = 'Trabalhar e construir carreira'")
    print("   else:")
    print("       categoria = 'Idoso'")
    print("       atividade = 'Aproveitar a aposentadoria'")
    print()
    print("   Resultado:")
    
    if idade < 13:
        categoria = 'Criança'
        atividade = 'Brincar e estudar'
    elif idade < 18:
        categoria = 'Adolescente'
        atividade = 'Estudar e descobrir vocação'
    elif idade < 60:
        categoria = 'Adulto'
        atividade = 'Trabalhar e construir carreira'
    else:
        categoria = 'Idoso'
        atividade = 'Aproveitar a aposentadoria'
    
    print(f"   → Categoria: {categoria}")
    print(f"   → Atividade: {atividade}")
    print()

def condicoes_aninhadas():
    """
    Explora estruturas condicionais aninhadas (nested if).
    
    Analogia: Condições aninhadas são como caixas dentro de caixas.
    Primeiro você abre a caixa maior, depois verifica se há
    caixas menores dentro, e assim por diante.
    """
    print("=== CONDIÇÕES ANINHADAS (NESTED IF) ===")
    print()
    
    print("1. CONCEITO:")
    print("   → Estruturas condicionais dentro de outras")
    print("   → Permitem verificações mais específicas")
    print("   → Cuidado com a complexidade e indentação!")
    print()
    
    print("2. SINTAXE:")
    print("   if condição_externa:")
    print("       if condição_interna:")
    print("           # código para ambas verdadeiras")
    print("       else:")
    print("           # código para externa True, interna False")
    print("   else:")
    print("       # código para externa False")
    print()
    
    # Exemplo 1: Sistema de acesso
    print("3. EXEMPLO 1: Sistema de acesso com múltiplas verificações")
    usuario = "admin"
    senha = "123456"
    tem_permissao = True
    
    print(f"   usuario = '{usuario}'")
    print(f"   senha = '{senha}'")
    print(f"   tem_permissao = {tem_permissao}")
    print()
    print("   if usuario == 'admin':")
    print("       if senha == '123456':")
    print("           if tem_permissao:")
    print("               print('Acesso total liberado!')")
    print("           else:")
    print("               print('Login correto, mas sem permissão')")
    print("       else:")
    print("           print('Usuário correto, senha incorreta')")
    print("   else:")
    print("       print('Usuário não encontrado')")
    print()
    print("   Resultado:")
    
    if usuario == 'admin':
        if senha == '123456':
            if tem_permissao:
                print("   → Acesso total liberado!")
            else:
                print("   → Login correto, mas sem permissão")
        else:
            print("   → Usuário correto, senha incorreta")
    else:
        print("   → Usuário não encontrado")
    print()
    
    # Exemplo 2: Sistema de desconto complexo
    print("4. EXEMPLO 2: Sistema de desconto com múltiplos critérios")
    valor_compra = 500.0
    eh_cliente_vip = True
    primeira_compra = False
    
    print(f"   valor_compra = R$ {valor_compra}")
    print(f"   eh_cliente_vip = {eh_cliente_vip}")
    print(f"   primeira_compra = {primeira_compra}")
    print()
    
    desconto = 0
    
    if valor_compra >= 100:
        print("   → Compra qualifica para desconto")
        if eh_cliente_vip:
            print("   → Cliente VIP detectado")
            if valor_compra >= 500:
                desconto = 0.20  # 20% para VIP com compra alta
                print("   → Desconto VIP Premium: 20%")
            else:
                desconto = 0.15  # 15% para VIP com compra normal
                print("   → Desconto VIP: 15%")
        else:
            print("   → Cliente regular")
            if primeira_compra:
                desconto = 0.10  # 10% para primeira compra
                print("   → Desconto primeira compra: 10%")
            else:
                desconto = 0.05  # 5% desconto padrão
                print("   → Desconto padrão: 5%")
    else:
        print("   → Compra não qualifica para desconto")
        desconto = 0
    
    valor_desconto = valor_compra * desconto
    valor_final = valor_compra - valor_desconto
    
    print(f"   → Desconto aplicado: {desconto * 100}%")
    print(f"   → Valor do desconto: R$ {valor_desconto:.2f}")
    print(f"   → Valor final: R$ {valor_final:.2f}")
    print()
    
    # Exemplo melhorado (menos aninhamento)
    print("5. VERSÃO MELHORADA (menos aninhamento):")
    print("   # Mesmo resultado, código mais limpo")
    print("   desconto = 0")
    print("   if valor_compra < 100:")
    print("       desconto = 0")
    print("   elif eh_cliente_vip and valor_compra >= 500:")
    print("       desconto = 0.20")
    print("   elif eh_cliente_vip:")
    print("       desconto = 0.15")
    print("   elif primeira_compra:")
    print("       desconto = 0.10")
    print("   else:")
    print("       desconto = 0.05")
    print()
    print("   💡 Prefira estruturas menos aninhadas quando possível!")
    print()

def operador_ternario():
    """
    Explora o operador ternário (conditional expression).
    
    Analogia: O operador ternário é como uma pergunta rápida:
    "Você quer café ou chá?" - uma resposta direta baseada numa condição.
    """
    print("=== OPERADOR TERNÁRIO ===")
    print()
    
    print("1. SINTAXE:")
    print("   valor_se_true if condição else valor_se_false")
    print()
    print("   → Versão compacta do if-else")
    print("   → Útil para atribuições simples")
    print("   → Não abuse! Pode prejudicar a legibilidade")
    print()
    
    # Comparação if-else vs ternário
    print("2. COMPARAÇÃO: IF-ELSE vs TERNÁRIO")
    idade = 20
    
    print(f"   idade = {idade}")
    print()
    print("   Versão tradicional (if-else):")
    print("   if idade >= 18:")
    print("       status = 'Adulto'")
    print("   else:")
    print("       status = 'Menor'")
    print()
    print("   Versão ternária:")
    print("   status = 'Adulto' if idade >= 18 else 'Menor'")
    print()
    
    # Executando ambas
    if idade >= 18:
        status_tradicional = 'Adulto'
    else:
        status_tradicional = 'Menor'
    
    status_ternario = 'Adulto' if idade >= 18 else 'Menor'
    
    print("   Resultado:")
    print(f"   → Tradicional: {status_tradicional}")
    print(f"   → Ternário: {status_ternario}")
    print()
    
    # Exemplos práticos
    print("3. EXEMPLOS PRÁTICOS:")
    
    # Exemplo 1: Determinar maior número
    a, b = 15, 23
    print(f"   a = {a}, b = {b}")
    maior = a if a > b else b
    print(f"   maior = a if a > b else b  →  {maior}")
    print()
    
    # Exemplo 2: Mensagem personalizada
    nome = "Ana"
    print(f"   nome = '{nome}'")
    saudacao = f"Olá, {nome}!" if nome else "Olá, visitante!"
    print(f"   saudacao = f'Olá, {{nome}}!' if nome else 'Olá, visitante!'")
    print(f"   → {saudacao}")
    print()
    
    # Exemplo 3: Formatação de preço
    preco = 29.99
    print(f"   preco = {preco}")
    preco_formatado = f"R$ {preco:.2f}" if preco > 0 else "Gratuito"
    print(f"   preco_formatado = f'R$ {{preco:.2f}}' if preco > 0 else 'Gratuito'")
    print(f"   → {preco_formatado}")
    print()
    
    # Exemplo 4: Ternário aninhado (cuidado!)
    print("4. TERNÁRIO ANINHADO (use com moderação):")
    nota = 8.5
    print(f"   nota = {nota}")
    resultado = "Excelente" if nota >= 9 else "Bom" if nota >= 7 else "Regular"
    print("   resultado = 'Excelente' if nota >= 9 else 'Bom' if nota >= 7 else 'Regular'")
    print(f"   → {resultado}")
    print()
    print("   ⚠️  Ternários aninhados podem ser confusos!")
    print("   💡 Prefira if-elif-else para múltiplas condições")
    print()

def valores_truthy_falsy():
    """
    Explora valores truthy e falsy em Python.
    
    Analogia: Em Python, alguns valores são considerados "vazios" ou "falsos"
    mesmo não sendo explicitamente False. É como uma caixa vazia -
    tecnicamente existe, mas não tem conteúdo útil.
    """
    print("=== VALORES TRUTHY E FALSY ===")
    print()
    
    print("1. CONCEITO:")
    print("   → Python avalia qualquer valor como True ou False")
    print("   → Valores 'falsy' são considerados False em condições")
    print("   → Todos os outros valores são 'truthy' (considerados True)")
    print()
    
    # Valores falsy
    print("2. VALORES FALSY (considerados False):")
    valores_falsy = [
        (False, "False"),
        (None, "None"),
        (0, "0 (zero)"),
        (0.0, "0.0 (zero float)"),
        ("", "'' (string vazia)"),
        ([], "[] (lista vazia)"),
        ({}, "{} (dicionário vazio)"),
        (set(), "set() (conjunto vazio)")
    ]
    
    for valor, descricao in valores_falsy:
        resultado = bool(valor)
        print(f"   bool({descricao:20}) = {resultado}")
    print()
    
    # Valores truthy
    print("3. VALORES TRUTHY (considerados True):")
    valores_truthy = [
        (True, "True"),
        (1, "1 (qualquer número != 0)"),
        (-1, "-1 (números negativos)"),
        ("texto", "'texto' (string não vazia)"),
        ([1, 2], "[1, 2] (lista com elementos)"),
        ({"a": 1}, "{'a': 1} (dict com elementos)")
    ]
    
    for valor, descricao in valores_truthy:
        resultado = bool(valor)
        print(f"   bool({descricao:25}) = {resultado}")
    print()
    
    # Exemplos práticos
    print("4. EXEMPLOS PRÁTICOS:")
    
    # Exemplo 1: Verificação de string
    nome = ""
    print(f"   nome = '{nome}'")
    print("   if nome:")
    print("       print(f'Olá, {nome}!')")
    print("   else:")
    print("       print('Nome não informado')")
    print()
    print("   Resultado:")
    if nome:
        print(f"   → Olá, {nome}!")
    else:
        print("   → Nome não informado")
    print()
    
    # Exemplo 2: Verificação de lista
    itens = []
    print(f"   itens = {itens}")
    print("   if itens:")
    print("       print(f'Temos {len(itens)} itens')")
    print("   else:")
    print("       print('Lista vazia')")
    print()
    print("   Resultado:")
    if itens:
        print(f"   → Temos {len(itens)} itens")
    else:
        print("   → Lista vazia")
    print()
    
    # Exemplo 3: Verificação de número
    saldo = 0
    print(f"   saldo = {saldo}")
    print("   if saldo:")
    print("       print(f'Saldo disponível: R$ {saldo}')")
    print("   else:")
    print("       print('Conta sem saldo')")
    print()
    print("   Resultado:")
    if saldo:
        print(f"   → Saldo disponível: R$ {saldo}")
    else:
        print("   → Conta sem saldo")
    print()
    
    # Exemplo 4: Verificação de None
    resultado_busca = None
    print(f"   resultado_busca = {resultado_busca}")
    print("   if resultado_busca:")
    print("       print(f'Encontrado: {resultado_busca}')")
    print("   else:")
    print("       print('Nada encontrado')")
    print()
    print("   Resultado:")
    if resultado_busca:
        print(f"   → Encontrado: {resultado_busca}")
    else:
        print("   → Nada encontrado")
    print()

def boas_praticas():
    """
    Apresenta boas práticas para estruturas condicionais.
    """
    print("=== BOAS PRÁTICAS ===")
    print()
    
    print("1. EVITE ANINHAMENTO EXCESSIVO:")
    print("   ❌ Ruim (muito aninhado):")
    print("   if condicao1:")
    print("       if condicao2:")
    print("           if condicao3:")
    print("               if condicao4:")
    print("                   fazer_algo()")
    print()
    print("   ✅ Melhor (early return/continue):")
    print("   if not condicao1:")
    print("       return")
    print("   if not condicao2:")
    print("       return")
    print("   if not condicao3:")
    print("       return")
    print("   if condicao4:")
    print("       fazer_algo()")
    print()
    
    print("2. USE NOMES DESCRITIVOS:")
    print("   ❌ Ruim:")
    print("   if x > 18 and y == True and z != None:")
    print()
    print("   ✅ Melhor:")
    print("   if idade > 18 and tem_permissao and documento is not None:")
    print()
    
    print("3. EXTRAIA CONDIÇÕES COMPLEXAS:")
    print("   ❌ Ruim:")
    print("   if (idade >= 18 and tem_carteira and not tem_multas) or eh_instrutor:")
    print()
    print("   ✅ Melhor:")
    print("   pode_dirigir = idade >= 18 and tem_carteira and not tem_multas")
    print("   if pode_dirigir or eh_instrutor:")
    print()
    
    print("4. USE COMPARAÇÕES EXPLÍCITAS QUANDO NECESSÁRIO:")
    print("   ❌ Pode ser ambíguo:")
    print("   if lista:  # lista vazia ou None?")
    print()
    print("   ✅ Mais claro:")
    print("   if lista is not None and len(lista) > 0:")
    print("   # ou")
    print("   if lista:  # quando você quer verificar se não está vazia")
    print()
    
    print("5. ORDENE CONDIÇÕES POR PROBABILIDADE:")
    print("   ✅ Condições mais prováveis primeiro:")
    print("   if idade < 60:        # mais comum")
    print("       categoria = 'adulto'")
    print("   elif idade < 18:      # menos comum")
    print("       categoria = 'menor'")
    print("   else:                 # menos comum")
    print("       categoria = 'idoso'")
    print()

def exemplos_praticos():
    """
    Exemplos práticos integrando todos os conceitos de estruturas condicionais.
    """
    print("=== EXEMPLOS PRÁTICOS INTEGRADOS ===")
    print()
    
    # Exemplo 1: Sistema de aprovação escolar
    print("Exemplo 1: Sistema de Aprovação Escolar")
    nome = "João Silva"
    nota1 = 8.5
    nota2 = 7.0
    nota3 = 9.0
    frequencia = 85  # porcentagem
    
    print(f"Aluno: {nome}")
    print(f"Notas: {nota1}, {nota2}, {nota3}")
    print(f"Frequência: {frequencia}%")
    print()
    
    # Cálculo da média
    media = (nota1 + nota2 + nota3) / 3
    print(f"Média: {media:.2f}")
    
    # Verificação de aprovação
    if frequencia < 75:
        situacao = "Reprovado por falta"
        print("→ Reprovado por frequência insuficiente")
    elif media >= 7.0:
        situacao = "Aprovado"
        print("→ Aprovado por média")
    elif media >= 5.0:
        situacao = "Recuperação"
        print("→ Recuperação (média entre 5.0 e 6.9)")
    else:
        situacao = "Reprovado por nota"
        print("→ Reprovado por média insuficiente")
    
    print(f"Situação final: {situacao}")
    print()
    
    # Exemplo 2: Calculadora de imposto de renda
    print("Exemplo 2: Calculadora de Imposto de Renda")
    salario_mensal = 5000.0
    salario_anual = salario_mensal * 12
    
    print(f"Salário mensal: R$ {salario_mensal:.2f}")
    print(f"Salário anual: R$ {salario_anual:.2f}")
    print()
    
    # Cálculo do imposto por faixas
    if salario_anual <= 22847.76:
        aliquota = 0.0
        parcela_deduzir = 0.0
        faixa = "Isento"
    elif salario_anual <= 33919.80:
        aliquota = 0.075
        parcela_deduzir = 1713.58
        faixa = "7,5%"
    elif salario_anual <= 45012.60:
        aliquota = 0.15
        parcela_deduzir = 4257.57
        faixa = "15%"
    elif salario_anual <= 55976.16:
        aliquota = 0.225
        parcela_deduzir = 7633.51
        faixa = "22,5%"
    else:
        aliquota = 0.275
        parcela_deduzir = 10432.32
        faixa = "27,5%"
    
    imposto_anual = (salario_anual * aliquota) - parcela_deduzir
    imposto_mensal = imposto_anual / 12
    salario_liquido = salario_mensal - imposto_mensal
    
    print(f"Faixa de tributação: {faixa}")
    print(f"Imposto anual: R$ {imposto_anual:.2f}")
    print(f"Imposto mensal: R$ {imposto_mensal:.2f}")
    print(f"Salário líquido: R$ {salario_liquido:.2f}")
    print()
    
    # Exemplo 3: Sistema de recomendação de atividade
    print("Exemplo 3: Sistema de Recomendação de Atividade")
    temperatura = 28
    chuva = False
    vento_forte = False
    fim_de_semana = True
    
    print(f"Temperatura: {temperatura}°C")
    print(f"Chuva: {chuva}")
    print(f"Vento forte: {vento_forte}")
    print(f"Fim de semana: {fim_de_semana}")
    print()
    
    # Lógica de recomendação
    if chuva:
        atividade = "Ficar em casa, ler um livro ou assistir filme"
    elif temperatura > 30 and not vento_forte:
        atividade = "Ir à praia ou piscina"
    elif temperatura > 25 and not chuva:
        if fim_de_semana:
            atividade = "Fazer um piquenique ou churrasco"
        else:
            atividade = "Caminhada no parque"
    elif temperatura > 15:
        atividade = "Visitar um museu ou shopping"
    else:
        atividade = "Ficar em casa com chocolate quente"
    
    print(f"Atividade recomendada: {atividade}")
    print()

def exercicios():
    """
    Exercícios progressivos para fixação das estruturas condicionais.
    """
    print("=== EXERCÍCIOS DE FIXAÇÃO ===")
    print()
    
    print("NÍVEL 1 - Básico:")
    print("1. Verificar se um número é positivo, negativo ou zero")
    print("2. Determinar se uma pessoa pode votar (idade >= 16)")
    print("3. Calcular desconto: 10% se compra >= R$ 100")
    print("4. Verificar se um ano é bissexto")
    print("5. Classificar temperatura: frio (<15), agradável (15-25), quente (>25)")
    print()
    
    print("NÍVEL 2 - Intermediário:")
    print("6. Sistema de notas: A (>=9), B (>=8), C (>=7), D (>=6), F (<6)")
    print("7. Calculadora de IMC com classificação completa")
    print("8. Validador de triângulo (três lados formam triângulo válido)")
    print("9. Sistema de login com 3 tentativas")
    print("10. Calculadora de tarifa de táxi (bandeirada + km rodado)")
    print()
    
    print("NÍVEL 3 - Avançado:")
    print("11. Sistema de aprovação: média >= 7 E frequência >= 75%")
    print("12. Calculadora de imposto progressivo")
    print("13. Sistema de recomendação baseado em múltiplos critérios")
    print("14. Validador de senha com múltiplos critérios")
    print("15. Sistema de pontuação de jogo com bônus e penalidades")
    print()
    
    # Exemplo de solução
    print("EXEMPLO DE SOLUÇÃO - Exercício 1:")
    print("# Verificar se número é positivo, negativo ou zero")
    print("numero = float(input('Digite um número: '))")
    print("if numero > 0:")
    print("    print('Número positivo')")
    print("elif numero < 0:")
    print("    print('Número negativo')")
    print("else:")
    print("    print('Número é zero')")
    print()
    
    # Executando o exemplo
    numero = -5.5
    print("RESULTADO (com numero = -5.5):")
    if numero > 0:
        print("→ Número positivo")
    elif numero < 0:
        print("→ Número negativo")
    else:
        print("→ Número é zero")
    print()

def resumo_estruturas_condicionais():
    """
    Resumo visual de todas as estruturas condicionais.
    """
    print("=== RESUMO DAS ESTRUTURAS CONDICIONAIS ===")
    print()
    
    print("┌─────────────────┬─────────────────────────────────────────────────┐")
    print("│   ESTRUTURA     │                   QUANDO USAR                  │")
    print("├─────────────────┼─────────────────────────────────────────────────┤")
    print("│ if              │ Uma única verificação                          │")
    print("│ if-else         │ Duas alternativas mutuamente exclusivas        │")
    print("│ if-elif-else    │ Múltiplas alternativas mutuamente exclusivas   │")
    print("│ if aninhado     │ Verificações dependentes (use com moderação)   │")
    print("│ Operador ternário│ Atribuição simples baseada em condição        │")
    print("└─────────────────┴─────────────────────────────────────────────────┘")
    print()
    
    print("VALORES FALSY (considerados False):")
    print("False, None, 0, 0.0, '', [], {}, set()")
    print()
    
    print("BOAS PRÁTICAS:")
    print("✅ Use nomes descritivos para variáveis e condições")
    print("✅ Evite aninhamento excessivo")
    print("✅ Extraia condições complexas para variáveis")
    print("✅ Ordene condições por probabilidade")
    print("✅ Use operador ternário apenas para casos simples")
    print("✅ Prefira comparações explícitas quando há ambiguidade")
    print()
    
    print("FLUXOGRAMA MENTAL:")
    print("1. Uma condição? → if")
    print("2. Duas alternativas? → if-else")
    print("3. Múltiplas alternativas? → if-elif-else")
    print("4. Condições dependentes? → if aninhado (com cuidado)")
    print("5. Atribuição simples? → operador ternário")
    print()

if __name__ == "__main__":
    # Demonstração completa do módulo
    print("🐍 CURSO DE PYTHON - MÓDULO 1.4: ESTRUTURAS CONDICIONAIS 🐍")
    print("=" * 70)
    print()
    
    # Execução sequencial de todos os conceitos
    conceito_estruturas_condicionais()
    print("-" * 50)
    
    estrutura_if_simples()
    print("-" * 50)
    
    estrutura_if_else()
    print("-" * 50)
    
    estrutura_if_elif_else()
    print("-" * 50)
    
    condicoes_aninhadas()
    print("-" * 50)
    
    operador_ternario()
    print("-" * 50)
    
    valores_truthy_falsy()
    print("-" * 50)
    
    boas_praticas()
    print("-" * 50)
    
    exemplos_praticos()
    print("-" * 50)
    
    resumo_estruturas_condicionais()
    print("-" * 50)
    
    exercicios()
    
    print("=" * 70)
    print("🎉 PARABÉNS! Você dominou as Estruturas Condicionais!")
    print("Próximo módulo: Estruturas de Repetição")
    print("=" * 70)