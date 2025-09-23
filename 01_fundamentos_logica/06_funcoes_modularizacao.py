"""
Módulo: Funções e Modularização
Tópico: Fundamentos de Lógica de Programação
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico

Objetivos de Aprendizado:
- Compreender o conceito de funções e sua importância
- Criar funções com parâmetros e valores de retorno
- Dominar escopo de variáveis (local vs global)
- Aplicar diferentes tipos de argumentos (posicionais, nomeados, *args, **kwargs)
- Implementar funções lambda e recursão básica
- Organizar código em módulos reutilizáveis

Conceitos Abordados:
- Definição e chamada de funções
- Parâmetros e argumentos
- Valores de retorno
- Escopo de variáveis (local, global, nonlocal)
- Argumentos padrão
- *args e **kwargs
- Funções lambda
- Recursão básica
- Docstrings e documentação
- Modularização e importação

Pré-requisitos:
- Todos os módulos anteriores do curso
- Conhecimento sólido de estruturas condicionais e loops
- Compreensão de tipos de dados e operadores

Complexidade Temporal: Varia conforme implementação (O(1) a O(n!))
Complexidade Espacial: O(1) para funções simples, O(n) para recursão
"""

def conceito_funcoes():
    """
    Introduz o conceito fundamental de funções.
    
    Analogia: Funções são como máquinas especializadas numa fábrica.
    Você coloca matéria-prima (parâmetros), a máquina processa,
    e você recebe o produto final (retorno).
    """
    print("=== CONCEITO DE FUNÇÕES ===")
    print()
    
    print("1. O QUE SÃO FUNÇÕES?")
    print("   → Blocos de código reutilizáveis")
    print("   → Executam uma tarefa específica")
    print("   → Podem receber dados (parâmetros)")
    print("   → Podem retornar resultados")
    print("   → Fundamentais para organização e reutilização")
    print()
    
    print("2. ANALOGIAS DO COTIDIANO:")
    print("   🏭 Máquina de café: água + pó → café")
    print("   🧮 Calculadora: números + operação → resultado")
    print("   🍳 Receita: ingredientes + instruções → prato")
    print("   📞 Telefone: número → conexão")
    print()
    
    print("3. VANTAGENS DAS FUNÇÕES:")
    print("   ✅ Reutilização de código")
    print("   ✅ Organização e legibilidade")
    print("   ✅ Facilita manutenção")
    print("   ✅ Reduz duplicação")
    print("   ✅ Permite testes isolados")
    print("   ✅ Divide problemas complexos")
    print()
    
    print("4. ANATOMIA DE UMA FUNÇÃO:")
    print("   def nome_da_funcao(parametros):")
    print("       '''Docstring explicativa'''")
    print("       # corpo da função")
    print("       return resultado  # opcional")
    print()
    print("   → def: palavra-chave para definir")
    print("   → nome_da_funcao: identificador único")
    print("   → parametros: dados de entrada (opcional)")
    print("   → docstring: documentação (boa prática)")
    print("   → return: valor de saída (opcional)")
    print()
    
    # Exemplo prático simples
    print("5. EXEMPLO PRÁTICO:")
    print("   def saudacao(nome):")
    print("       '''Função que cria uma saudação personalizada'''")
    print("       return f'Olá, {nome}! Bem-vindo ao Python!'")
    print()
    print("   # Chamando a função")
    print("   mensagem = saudacao('Ana')")
    print("   print(mensagem)")
    print()
    print("   Resultado:")
    
    def saudacao(nome):
        """Função que cria uma saudação personalizada"""
        return f"Olá, {nome}! Bem-vindo ao Python!"
    
    mensagem = saudacao('Ana')
    print(f"   → {mensagem}")
    print()

def definindo_funcoes():
    """
    Explora como definir e chamar funções básicas.
    
    Analogia: Definir uma função é como escrever uma receita.
    Chamar a função é como seguir a receita para fazer o prato.
    """
    print("=== DEFININDO E CHAMANDO FUNÇÕES ===")
    print()
    
    print("1. FUNÇÃO SEM PARÂMETROS E SEM RETORNO:")
    print("   def mostrar_menu():")
    print("       print('=== MENU PRINCIPAL ===')")
    print("       print('1. Opção A')")
    print("       print('2. Opção B')")
    print("       print('3. Sair')")
    print()
    print("   # Chamando a função")
    print("   mostrar_menu()")
    print()
    print("   Resultado:")
    
    def mostrar_menu():
        print("   === MENU PRINCIPAL ===")
        print("   1. Opção A")
        print("   2. Opção B")
        print("   3. Sair")
    
    mostrar_menu()
    print()
    
    print("2. FUNÇÃO COM PARÂMETROS:")
    print("   def calcular_area_retangulo(largura, altura):")
    print("       area = largura * altura")
    print("       print(f'Área: {largura} x {altura} = {area}')")
    print()
    print("   # Chamando com argumentos")
    print("   calcular_area_retangulo(5, 3)")
    print("   calcular_area_retangulo(10, 7)")
    print()
    print("   Resultado:")
    
    def calcular_area_retangulo(largura, altura):
        area = largura * altura
        print(f"   → Área: {largura} x {altura} = {area}")
    
    calcular_area_retangulo(5, 3)
    calcular_area_retangulo(10, 7)
    print()
    
    print("3. FUNÇÃO COM RETORNO:")
    print("   def somar(a, b):")
    print("       resultado = a + b")
    print("       return resultado")
    print()
    print("   # Usando o valor retornado")
    print("   soma1 = somar(10, 5)")
    print("   soma2 = somar(3, 7)")
    print("   total = somar(soma1, soma2)")
    print("   print(f'Total: {total}')")
    print()
    print("   Resultado:")
    
    def somar(a, b):
        resultado = a + b
        return resultado
    
    soma1 = somar(10, 5)
    soma2 = somar(3, 7)
    total = somar(soma1, soma2)
    print(f"   → soma1 = {soma1}")
    print(f"   → soma2 = {soma2}")
    print(f"   → Total: {total}")
    print()
    
    print("4. FUNÇÃO COM MÚLTIPLOS RETORNOS:")
    print("   def dividir_com_resto(dividendo, divisor):")
    print("       quociente = dividendo // divisor")
    print("       resto = dividendo % divisor")
    print("       return quociente, resto")
    print()
    print("   # Recebendo múltiplos valores")
    print("   q, r = dividir_com_resto(17, 5)")
    print("   print(f'17 ÷ 5 = {q} resto {r}')")
    print()
    print("   Resultado:")
    
    def dividir_com_resto(dividendo, divisor):
        quociente = dividendo // divisor
        resto = dividendo % divisor
        return quociente, resto
    
    q, r = dividir_com_resto(17, 5)
    print(f"   → 17 ÷ 5 = {q} resto {r}")
    print()

def parametros_argumentos():
    """
    Explora diferentes tipos de parâmetros e argumentos.
    
    Analogia: Parâmetros são como campos num formulário.
    Alguns são obrigatórios, outros opcionais com valores padrão.
    """
    print("=== PARÂMETROS E ARGUMENTOS ===")
    print()
    
    print("1. ARGUMENTOS POSICIONAIS:")
    print("   def apresentar_pessoa(nome, idade, cidade):")
    print("       print(f'{nome}, {idade} anos, mora em {cidade}')")
    print()
    print("   # Ordem importa!")
    print("   apresentar_pessoa('João', 25, 'São Paulo')")
    print("   apresentar_pessoa('Maria', 30, 'Rio de Janeiro')")
    print()
    print("   Resultado:")
    
    def apresentar_pessoa(nome, idade, cidade):
        print(f"   → {nome}, {idade} anos, mora em {cidade}")
    
    apresentar_pessoa('João', 25, 'São Paulo')
    apresentar_pessoa('Maria', 30, 'Rio de Janeiro')
    print()
    
    print("2. ARGUMENTOS NOMEADOS (KEYWORD):")
    print("   # Mesma função, mas chamada com nomes")
    print("   apresentar_pessoa(cidade='Brasília', nome='Pedro', idade=28)")
    print("   apresentar_pessoa(nome='Ana', idade=22, cidade='Salvador')")
    print()
    print("   Resultado:")
    apresentar_pessoa(cidade='Brasília', nome='Pedro', idade=28)
    apresentar_pessoa(nome='Ana', idade=22, cidade='Salvador')
    print()
    
    print("3. PARÂMETROS COM VALORES PADRÃO:")
    print("   def criar_usuario(nome, idade, ativo=True, admin=False):")
    print("       status = 'Ativo' if ativo else 'Inativo'")
    print("       tipo = 'Admin' if admin else 'Usuário'")
    print("       print(f'{nome} ({idade} anos) - {status} - {tipo}')")
    print()
    print("   # Usando valores padrão")
    print("   criar_usuario('Carlos', 35)")
    print("   criar_usuario('Lucia', 28, admin=True)")
    print("   criar_usuario('Roberto', 45, ativo=False)")
    print()
    print("   Resultado:")
    
    def criar_usuario(nome, idade, ativo=True, admin=False):
        status = 'Ativo' if ativo else 'Inativo'
        tipo = 'Admin' if admin else 'Usuário'
        print(f"   → {nome} ({idade} anos) - {status} - {tipo}")
    
    criar_usuario('Carlos', 35)
    criar_usuario('Lucia', 28, admin=True)
    criar_usuario('Roberto', 45, ativo=False)
    print()
    
    print("4. MISTURANDO TIPOS DE ARGUMENTOS:")
    print("   def fazer_pedido(item, quantidade=1, urgente=False, desconto=0):")
    print("       preco_base = 10.0")
    print("       subtotal = preco_base * quantidade")
    print("       total = subtotal * (1 - desconto)")
    print("       prioridade = 'URGENTE' if urgente else 'Normal'")
    print("       print(f'{item} x{quantidade} = R${total:.2f} [{prioridade}]')")
    print()
    print("   fazer_pedido('Pizza')")
    print("   fazer_pedido('Hambúrguer', 2)")
    print("   fazer_pedido('Sanduíche', quantidade=3, urgente=True)")
    print("   fazer_pedido('Salada', 1, desconto=0.1)")
    print()
    print("   Resultado:")
    
    def fazer_pedido(item, quantidade=1, urgente=False, desconto=0):
        preco_base = 10.0
        subtotal = preco_base * quantidade
        total = subtotal * (1 - desconto)
        prioridade = 'URGENTE' if urgente else 'Normal'
        print(f"   → {item} x{quantidade} = R${total:.2f} [{prioridade}]")
    
    fazer_pedido('Pizza')
    fazer_pedido('Hambúrguer', 2)
    fazer_pedido('Sanduíche', quantidade=3, urgente=True)
    fazer_pedido('Salada', 1, desconto=0.1)
    print()

def args_kwargs():
    """
    Explora *args e **kwargs para argumentos variáveis.
    
    Analogia: *args é como uma mochila que pode carregar qualquer quantidade
    de itens. **kwargs é como um dicionário de configurações personalizadas.
    """
    print("=== *ARGS E **KWARGS ===")
    print()
    
    print("1. *ARGS - ARGUMENTOS POSICIONAIS VARIÁVEIS:")
    print("   def somar_todos(*numeros):")
    print("       total = 0")
    print("       for numero in numeros:")
    print("           total += numero")
    print("       return total")
    print()
    print("   # Pode receber qualquer quantidade de argumentos")
    print("   print(somar_todos(1, 2, 3))")
    print("   print(somar_todos(10, 20, 30, 40, 50))")
    print("   print(somar_todos(5))")
    print("   print(somar_todos())  # sem argumentos")
    print()
    print("   Resultado:")
    
    def somar_todos(*numeros):
        total = 0
        for numero in numeros:
            total += numero
        return total
    
    print(f"   → somar_todos(1, 2, 3) = {somar_todos(1, 2, 3)}")
    print(f"   → somar_todos(10, 20, 30, 40, 50) = {somar_todos(10, 20, 30, 40, 50)}")
    print(f"   → somar_todos(5) = {somar_todos(5)}")
    print(f"   → somar_todos() = {somar_todos()}")
    print()
    
    print("2. **KWARGS - ARGUMENTOS NOMEADOS VARIÁVEIS:")
    print("   def criar_perfil(nome, **informacoes):")
    print("       print(f'Perfil de {nome}:')")
    print("       for chave, valor in informacoes.items():")
    print("           print(f'  {chave}: {valor}')")
    print()
    print("   criar_perfil('João', idade=30, cidade='SP', profissao='Dev')")
    print("   criar_perfil('Maria', idade=25, hobby='Leitura')")
    print()
    print("   Resultado:")
    
    def criar_perfil(nome, **informacoes):
        print(f"   → Perfil de {nome}:")
        for chave, valor in informacoes.items():
            print(f"     {chave}: {valor}")
    
    criar_perfil('João', idade=30, cidade='SP', profissao='Dev')
    print()
    criar_perfil('Maria', idade=25, hobby='Leitura')
    print()
    
    print("3. COMBINANDO TUDO:")
    print("   def funcao_completa(obrigatorio, padrao='valor', *args, **kwargs):")
    print("       print(f'Obrigatório: {obrigatorio}')")
    print("       print(f'Padrão: {padrao}')")
    print("       print(f'Args extras: {args}')")
    print("       print(f'Kwargs: {kwargs}')")
    print()
    print("   funcao_completa('A', 'B', 'C', 'D', nome='João', idade=30)")
    print()
    print("   Resultado:")
    
    def funcao_completa(obrigatorio, padrao='valor', *args, **kwargs):
        print(f"   → Obrigatório: {obrigatorio}")
        print(f"   → Padrão: {padrao}")
        print(f"   → Args extras: {args}")
        print(f"   → Kwargs: {kwargs}")
    
    funcao_completa('A', 'B', 'C', 'D', nome='João', idade=30)
    print()
    
    print("4. EXEMPLO PRÁTICO - LOGGER FLEXÍVEL:")
    print("   def log(nivel, mensagem, *detalhes, **contexto):")
    print("       print(f'[{nivel}] {mensagem}')")
    print("       if detalhes:")
    print("           print(f'Detalhes: {detalhes}')")
    print("       if contexto:")
    print("           print(f'Contexto: {contexto}')")
    print()
    print("   log('INFO', 'Sistema iniciado')")
    print("   log('ERROR', 'Falha na conexão', 'timeout', 'retry=3', host='localhost')")
    print()
    print("   Resultado:")
    
    def log(nivel, mensagem, *detalhes, **contexto):
        print(f"   → [{nivel}] {mensagem}")
        if detalhes:
            print(f"     Detalhes: {detalhes}")
        if contexto:
            print(f"     Contexto: {contexto}")
    
    log('INFO', 'Sistema iniciado')
    print()
    log('ERROR', 'Falha na conexão', 'timeout', 'retry=3', host='localhost')
    print()

def escopo_variaveis():
    """
    Explora escopo de variáveis (local, global, nonlocal).
    
    Analogia: Escopo é como os cômodos de uma casa.
    Variáveis locais ficam no quarto (privadas),
    variáveis globais ficam na sala (acessíveis a todos).
    """
    print("=== ESCOPO DE VARIÁVEIS ===")
    print()
    
    print("1. ESCOPO LOCAL vs GLOBAL:")
    print("   # Variável global")
    print("   contador_global = 0")
    print()
    print("   def incrementar():")
    print("       # Variável local")
    print("       contador_local = 10")
    print("       print(f'Local: {contador_local}')")
    print("       print(f'Global (leitura): {contador_global}')")
    print()
    print("   incrementar()")
    print("   print(f'Global fora da função: {contador_global}')")
    print("   # print(contador_local)  # ERRO! Não existe fora da função")
    print()
    print("   Resultado:")
    
    # Variável global
    contador_global = 0
    
    def incrementar():
        # Variável local
        contador_local = 10
        print(f"   → Local: {contador_local}")
        print(f"   → Global (leitura): {contador_global}")
    
    incrementar()
    print(f"   → Global fora da função: {contador_global}")
    print()
    
    print("2. MODIFICANDO VARIÁVEL GLOBAL:")
    print("   saldo = 1000")
    print()
    print("   def sacar(valor):")
    print("       global saldo")
    print("       if saldo >= valor:")
    print("           saldo -= valor")
    print("           print(f'Saque de R${valor}. Saldo: R${saldo}')")
    print("       else:")
    print("           print('Saldo insuficiente')")
    print()
    print("   print(f'Saldo inicial: R${saldo}')")
    print("   sacar(200)")
    print("   sacar(500)")
    print("   sacar(400)  # Deve dar erro")
    print()
    print("   Resultado:")
    
    saldo = 1000
    
    def sacar(valor):
        global saldo
        if saldo >= valor:
            saldo -= valor
            print(f"   → Saque de R${valor}. Saldo: R${saldo}")
        else:
            print("   → Saldo insuficiente")
    
    print(f"   → Saldo inicial: R${saldo}")
    sacar(200)
    sacar(500)
    sacar(400)  # Deve dar erro
    print()
    
    print("3. ESCOPO NONLOCAL (FUNÇÕES ANINHADAS):")
    print("   def contador_avancado():")
    print("       count = 0")
    print("       def incrementar():")
    print("           nonlocal count")
    print("           count += 1")
    print("           return count")
    print("       def decrementar():")
    print("           nonlocal count")
    print("           count -= 1")
    print("           return count")
    print("       return incrementar, decrementar")
    print()
    print("   inc, dec = contador_avancado()")
    print("   print(f'Inc: {inc()}')")
    print("   print(f'Inc: {inc()}')")
    print("   print(f'Dec: {dec()}')")
    print()
    print("   Resultado:")
    
    def contador_avancado():
        count = 0
        def incrementar():
            nonlocal count
            count += 1
            return count
        def decrementar():
            nonlocal count
            count -= 1
            return count
        return incrementar, decrementar
    
    inc, dec = contador_avancado()
    print(f"   → Inc: {inc()}")
    print(f"   → Inc: {inc()}")
    print(f"   → Dec: {dec()}")
    print()
    
    print("4. BOAS PRÁTICAS DE ESCOPO:")
    print("   ✅ Prefira variáveis locais")
    print("   ✅ Use global apenas quando necessário")
    print("   ✅ Passe dados via parâmetros")
    print("   ✅ Retorne resultados em vez de modificar globais")
    print("   ❌ Evite muitas variáveis globais")
    print()

def funcoes_lambda():
    """
    Explora funções lambda (anônimas).
    
    Analogia: Funções lambda são como calculadoras de bolso.
    Pequenas, específicas, usadas rapidamente e descartadas.
    """
    print("=== FUNÇÕES LAMBDA ===")
    print()
    
    print("1. CONCEITO:")
    print("   → Funções anônimas (sem nome)")
    print("   → Sintaxe compacta: lambda argumentos: expressão")
    print("   → Úteis para operações simples e rápidas")
    print("   → Comumente usadas com map(), filter(), sorted()")
    print()
    
    print("2. COMPARAÇÃO: FUNÇÃO NORMAL vs LAMBDA:")
    print("   # Função normal")
    print("   def quadrado(x):")
    print("       return x ** 2")
    print()
    print("   # Função lambda equivalente")
    print("   quadrado_lambda = lambda x: x ** 2")
    print()
    print("   print(quadrado(5))")
    print("   print(quadrado_lambda(5))")
    print()
    print("   Resultado:")
    
    def quadrado(x):
        return x ** 2
    
    quadrado_lambda = lambda x: x ** 2
    
    print(f"   → quadrado(5) = {quadrado(5)}")
    print(f"   → quadrado_lambda(5) = {quadrado_lambda(5)}")
    print()
    
    print("3. LAMBDA COM MAP():")
    print("   numeros = [1, 2, 3, 4, 5]")
    print("   quadrados = list(map(lambda x: x ** 2, numeros))")
    print("   print(f'Números: {numeros}')")
    print("   print(f'Quadrados: {quadrados}')")
    print()
    print("   Resultado:")
    
    numeros = [1, 2, 3, 4, 5]
    quadrados = list(map(lambda x: x ** 2, numeros))
    print(f"   → Números: {numeros}")
    print(f"   → Quadrados: {quadrados}")
    print()
    
    print("4. LAMBDA COM FILTER():")
    print("   numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]")
    print("   pares = list(filter(lambda x: x % 2 == 0, numeros))")
    print("   print(f'Números: {numeros}')")
    print("   print(f'Pares: {pares}')")
    print()
    print("   Resultado:")
    
    numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pares = list(filter(lambda x: x % 2 == 0, numeros))
    print(f"   → Números: {numeros}")
    print(f"   → Pares: {pares}")
    print()
    
    print("5. LAMBDA COM SORTED():")
    print("   pessoas = [('Ana', 25), ('Bruno', 30), ('Carlos', 20)]")
    print("   # Ordenar por idade")
    print("   por_idade = sorted(pessoas, key=lambda pessoa: pessoa[1])")
    print("   print(f'Original: {pessoas}')")
    print("   print(f'Por idade: {por_idade}')")
    print()
    print("   Resultado:")
    
    pessoas = [('Ana', 25), ('Bruno', 30), ('Carlos', 20)]
    por_idade = sorted(pessoas, key=lambda pessoa: pessoa[1])
    print(f"   → Original: {pessoas}")
    print(f"   → Por idade: {por_idade}")
    print()
    
    print("6. LAMBDAS MAIS COMPLEXAS:")
    print("   # Lambda com múltiplos argumentos")
    print("   somar = lambda a, b: a + b")
    print("   print(f'somar(3, 5) = {somar(3, 5)}')")
    print()
    print("   # Lambda com condição")
    print("   maior = lambda a, b: a if a > b else b")
    print("   print(f'maior(10, 7) = {maior(10, 7)}')")
    print()
    print("   Resultado:")
    
    somar = lambda a, b: a + b
    print(f"   → somar(3, 5) = {somar(3, 5)}")
    
    maior = lambda a, b: a if a > b else b
    print(f"   → maior(10, 7) = {maior(10, 7)}")
    print()

def recursao_basica():
    """
    Introduz o conceito de recursão.
    
    Analogia: Recursão é como bonecas russas (matrioskas).
    Cada boneca contém uma versão menor de si mesma,
    até chegar na menor que não pode ser aberta.
    """
    print("=== RECURSÃO BÁSICA ===")
    print()
    
    print("1. CONCEITO:")
    print("   → Função que chama a si mesma")
    print("   → Deve ter uma condição de parada (caso base)")
    print("   → Útil para problemas que podem ser divididos")
    print("   → Cuidado com stack overflow!")
    print()
    
    print("2. EXEMPLO CLÁSSICO - FATORIAL:")
    print("   def fatorial(n):")
    print("       # Caso base")
    print("       if n <= 1:")
    print("           return 1")
    print("       # Caso recursivo")
    print("       return n * fatorial(n - 1)")
    print()
    print("   print(f'5! = {fatorial(5)}')")
    print("   print(f'0! = {fatorial(0)}')")
    print()
    print("   Resultado:")
    
    def fatorial(n):
        # Caso base
        if n <= 1:
            return 1
        # Caso recursivo
        return n * fatorial(n - 1)
    
    print(f"   → 5! = {fatorial(5)}")
    print(f"   → 0! = {fatorial(0)}")
    print()
    
    print("3. VISUALIZANDO A RECURSÃO:")
    print("   fatorial(5)")
    print("   ├─ 5 * fatorial(4)")
    print("   │  ├─ 4 * fatorial(3)")
    print("   │  │  ├─ 3 * fatorial(2)")
    print("   │  │  │  ├─ 2 * fatorial(1)")
    print("   │  │  │  │  └─ 1 (caso base)")
    print("   │  │  │  └─ 2 * 1 = 2")
    print("   │  │  └─ 3 * 2 = 6")
    print("   │  └─ 4 * 6 = 24")
    print("   └─ 5 * 24 = 120")
    print()
    
    print("4. FIBONACCI RECURSIVO:")
    print("   def fibonacci(n):")
    print("       if n <= 1:")
    print("           return n")
    print("       return fibonacci(n-1) + fibonacci(n-2)")
    print()
    print("   # Primeiros números de Fibonacci")
    print("   for i in range(8):")
    print("       print(f'fib({i}) = {fibonacci(i)}')")
    print()
    print("   Resultado:")
    
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    for i in range(8):
        print(f"   → fib({i}) = {fibonacci(i)}")
    print()
    
    print("5. CONTAGEM REGRESSIVA:")
    print("   def contagem_regressiva(n):")
    print("       if n <= 0:")
    print("           print('🚀 Decolagem!')")
    print("           return")
    print("       print(f'Contagem: {n}')")
    print("       contagem_regressiva(n - 1)")
    print()
    print("   contagem_regressiva(5)")
    print()
    print("   Resultado:")
    
    def contagem_regressiva(n):
        if n <= 0:
            print("   → 🚀 Decolagem!")
            return
        print(f"   → Contagem: {n}")
        contagem_regressiva(n - 1)
    
    contagem_regressiva(5)
    print()
    
    print("6. CUIDADOS COM RECURSÃO:")
    print("   ⚠️  Sempre defina um caso base")
    print("   ⚠️  Certifique-se de que converge para o caso base")
    print("   ⚠️  Cuidado com a profundidade (stack overflow)")
    print("   ⚠️  Recursão pode ser ineficiente (ex: Fibonacci)")
    print("   💡 Considere iteração para casos simples")
    print()

def docstrings_documentacao():
    """
    Explora docstrings e documentação de funções.
    
    Analogia: Docstrings são como manuais de instruções.
    Explicam o que a função faz, como usar e o que esperar.
    """
    print("=== DOCSTRINGS E DOCUMENTAÇÃO ===")
    print()
    
    print("1. IMPORTÂNCIA DA DOCUMENTAÇÃO:")
    print("   → Explica o propósito da função")
    print("   → Descreve parâmetros e retorno")
    print("   → Facilita manutenção e colaboração")
    print("   → Permite geração automática de documentação")
    print()
    
    print("2. TIPOS DE DOCSTRINGS:")
    print("   # Docstring simples")
    print("   def somar(a, b):")
    print("       '''Soma dois números e retorna o resultado.'''")
    print("       return a + b")
    print()
    print("   # Docstring detalhada")
    print("   def calcular_imc(peso, altura):")
    print("       '''")
    print("       Calcula o Índice de Massa Corporal (IMC).")
    print("       ")
    print("       Args:")
    print("           peso (float): Peso em quilogramas")
    print("           altura (float): Altura em metros")
    print("       ")
    print("       Returns:")
    print("           float: Valor do IMC calculado")
    print("       ")
    print("       Raises:")
    print("           ValueError: Se altura for zero ou negativa")
    print("       '''")
    print("       if altura <= 0:")
    print("           raise ValueError('Altura deve ser positiva')")
    print("       return peso / (altura ** 2)")
    print()
    
    # Exemplo prático
    def calcular_imc(peso, altura):
        """
        Calcula o Índice de Massa Corporal (IMC).
        
        Args:
            peso (float): Peso em quilogramas
            altura (float): Altura em metros
        
        Returns:
            float: Valor do IMC calculado
        
        Raises:
            ValueError: Se altura for zero ou negativa
        """
        if altura <= 0:
            raise ValueError('Altura deve ser positiva')
        return peso / (altura ** 2)
    
    print("3. ACESSANDO DOCSTRINGS:")
    print("   print(calcular_imc.__doc__)")
    print("   help(calcular_imc)")
    print()
    print("   Resultado:")
    print("   →", calcular_imc.__doc__.strip().split('\n')[0])
    print()
    
    print("4. EXEMPLO COMPLETO COM DOCUMENTAÇÃO:")
    print("   def validar_cpf(cpf):")
    print("       '''")
    print("       Valida um número de CPF brasileiro.")
    print("       ")
    print("       Args:")
    print("           cpf (str): CPF no formato 'XXX.XXX.XXX-XX' ou 'XXXXXXXXXXX'")
    print("       ")
    print("       Returns:")
    print("           bool: True se CPF é válido, False caso contrário")
    print("       ")
    print("       Example:")
    print("           >>> validar_cpf('123.456.789-09')")
    print("           False")
    print("           >>> validar_cpf('000.000.000-00')")
    print("           False")
    print("       '''")
    print("       # Implementação simplificada")
    print("       cpf_numeros = ''.join(filter(str.isdigit, cpf))")
    print("       return len(cpf_numeros) == 11 and cpf_numeros != cpf_numeros[0] * 11")
    print()
    
    def validar_cpf(cpf):
        """
        Valida um número de CPF brasileiro.
        
        Args:
            cpf (str): CPF no formato 'XXX.XXX.XXX-XX' ou 'XXXXXXXXXXX'
        
        Returns:
            bool: True se CPF é válido, False caso contrário
        
        Example:
            >>> validar_cpf('123.456.789-09')
            False
            >>> validar_cpf('000.000.000-00')
            False
        """
        # Implementação simplificada
        cpf_numeros = ''.join(filter(str.isdigit, cpf))
        return len(cpf_numeros) == 11 and cpf_numeros != cpf_numeros[0] * 11
    
    print("   Testando:")
    print(f"   → validar_cpf('123.456.789-09'): {validar_cpf('123.456.789-09')}")
    print(f"   → validar_cpf('000.000.000-00'): {validar_cpf('000.000.000-00')}")
    print(f"   → validar_cpf('123.456.789-10'): {validar_cpf('123.456.789-10')}")
    print()

def modularizacao():
    """
    Explora conceitos de modularização e organização de código.
    
    Analogia: Modularização é como organizar uma biblioteca.
    Livros do mesmo assunto ficam na mesma estante (módulo),
    facilitando encontrar e usar o que precisa.
    """
    print("=== MODULARIZAÇÃO ===")
    print()
    
    print("1. CONCEITO DE MÓDULOS:")
    print("   → Arquivos .py contendo funções relacionadas")
    print("   → Organizam código por funcionalidade")
    print("   → Facilitam reutilização e manutenção")
    print("   → Evitam poluição do namespace global")
    print()
    
    print("2. ESTRUTURA DE UM PROJETO:")
    print("   meu_projeto/")
    print("   ├── main.py")
    print("   ├── matematica.py")
    print("   ├── utils.py")
    print("   └── validadores.py")
    print()
    
    print("3. EXEMPLO DE MÓDULO - matematica.py:")
    print("   '''Módulo com funções matemáticas básicas'''")
    print("   ")
    print("   def somar(a, b):")
    print("       '''Soma dois números'''")
    print("       return a + b")
    print("   ")
    print("   def multiplicar(a, b):")
    print("       '''Multiplica dois números'''")
    print("       return a * b")
    print("   ")
    print("   def fatorial(n):")
    print("       '''Calcula fatorial de n'''")
    print("       if n <= 1:")
    print("           return 1")
    print("       return n * fatorial(n - 1)")
    print()
    
    print("4. FORMAS DE IMPORTAR:")
    print("   # Importar módulo completo")
    print("   import matematica")
    print("   resultado = matematica.somar(5, 3)")
    print()
    print("   # Importar funções específicas")
    print("   from matematica import somar, multiplicar")
    print("   resultado = somar(5, 3)")
    print()
    print("   # Importar com alias")
    print("   import matematica as mat")
    print("   resultado = mat.somar(5, 3)")
    print()
    print("   # Importar tudo (não recomendado)")
    print("   from matematica import *")
    print("   resultado = somar(5, 3)")
    print()
    
    print("5. EXEMPLO PRÁTICO - SIMULAÇÃO:")
    print("   # Simulando funções de um módulo")
    print("   def somar_modulo(a, b):")
    print("       return a + b")
    print("   ")
    print("   def multiplicar_modulo(a, b):")
    print("       return a * b")
    print("   ")
    print("   # Usando as funções")
    print("   print(f'Soma: {somar_modulo(10, 5)}')")
    print("   print(f'Multiplicação: {multiplicar_modulo(4, 7)}')")
    print()
    print("   Resultado:")
    
    def somar_modulo(a, b):
        return a + b
    
    def multiplicar_modulo(a, b):
        return a * b
    
    print(f"   → Soma: {somar_modulo(10, 5)}")
    print(f"   → Multiplicação: {multiplicar_modulo(4, 7)}")
    print()
    
    print("6. BOAS PRÁTICAS DE MODULARIZAÇÃO:")
    print("   ✅ Um módulo = uma responsabilidade")
    print("   ✅ Nomes descritivos para módulos")
    print("   ✅ Docstrings no início dos módulos")
    print("   ✅ Funções relacionadas no mesmo módulo")
    print("   ✅ Use __init__.py para pacotes")
    print("   ❌ Evite import * (poluição do namespace)")
    print("   ❌ Evite dependências circulares")
    print()

def exemplos_praticos():
    """
    Exemplos práticos integrando todos os conceitos de funções.
    """
    print("=== EXEMPLOS PRÁTICOS INTEGRADOS ===")
    print()
    
    # Exemplo 1: Sistema de calculadora
    print("Exemplo 1: Sistema de Calculadora Modular")
    
    def somar(a, b):
        """Soma dois números"""
        return a + b
    
    def subtrair(a, b):
        """Subtrai dois números"""
        return a - b
    
    def multiplicar(a, b):
        """Multiplica dois números"""
        return a * b
    
    def dividir(a, b):
        """Divide dois números"""
        if b == 0:
            return "Erro: Divisão por zero!"
        return a / b
    
    def calcular(operacao, a, b):
        """
        Executa operação matemática baseada no nome.
        
        Args:
            operacao (str): Nome da operação ('somar', 'subtrair', etc.)
            a (float): Primeiro número
            b (float): Segundo número
        
        Returns:
            float or str: Resultado da operação ou mensagem de erro
        """
        operacoes = {
            'somar': somar,
            'subtrair': subtrair,
            'multiplicar': multiplicar,
            'dividir': dividir
        }
        
        if operacao in operacoes:
            return operacoes[operacao](a, b)
        else:
            return "Operação não encontrada!"
    
    print("Testando calculadora:")
    testes = [
        ('somar', 10, 5),
        ('subtrair', 10, 3),
        ('multiplicar', 4, 7),
        ('dividir', 15, 3),
        ('dividir', 10, 0),
        ('potencia', 2, 3)
    ]
    
    for op, a, b in testes:
        resultado = calcular(op, a, b)
        print(f"   → {op}({a}, {b}) = {resultado}")
    print()
    
    # Exemplo 2: Sistema de validação
    print("Exemplo 2: Sistema de Validação de Dados")
    
    def validar_email(email):
        """Valida formato básico de email"""
        return '@' in email and '.' in email.split('@')[-1]
    
    def validar_senha(senha, min_length=8):
        """
        Valida força da senha.
        
        Args:
            senha (str): Senha a ser validada
            min_length (int): Comprimento mínimo
        
        Returns:
            tuple: (bool, list) - (é_válida, lista_de_problemas)
        """
        problemas = []
        
        if len(senha) < min_length:
            problemas.append(f"Deve ter pelo menos {min_length} caracteres")
        
        if not any(c.isupper() for c in senha):
            problemas.append("Deve ter pelo menos uma letra maiúscula")
        
        if not any(c.islower() for c in senha):
            problemas.append("Deve ter pelo menos uma letra minúscula")
        
        if not any(c.isdigit() for c in senha):
            problemas.append("Deve ter pelo menos um número")
        
        return len(problemas) == 0, problemas
    
    def validar_usuario(nome, email, senha):
        """
        Valida dados completos do usuário.
        
        Returns:
            dict: Resultado da validação com detalhes
        """
        resultado = {
            'valido': True,
            'erros': []
        }
        
        # Validar nome
        if not nome or len(nome.strip()) < 2:
            resultado['erros'].append("Nome deve ter pelo menos 2 caracteres")
            resultado['valido'] = False
        
        # Validar email
        if not validar_email(email):
            resultado['erros'].append("Email inválido")
            resultado['valido'] = False
        
        # Validar senha
        senha_valida, problemas_senha = validar_senha(senha)
        if not senha_valida:
            resultado['erros'].extend(problemas_senha)
            resultado['valido'] = False
        
        return resultado
    
    print("Testando validação:")
    usuarios_teste = [
        ("João Silva", "joao@email.com", "MinhaSenh@123"),
        ("A", "email_invalido", "123"),
        ("Maria", "maria@teste.com", "SenhaForte1")
    ]
    
    for nome, email, senha in usuarios_teste:
        resultado = validar_usuario(nome, email, senha)
        print(f"   → {nome}: {'✅ Válido' if resultado['valido'] else '❌ Inválido'}")
        if not resultado['valido']:
            for erro in resultado['erros']:
                print(f"     - {erro}")
        print()
    
    # Exemplo 3: Sistema de relatórios com funções de alta ordem
    print("Exemplo 3: Sistema de Relatórios")
    
    vendas = [
        {'produto': 'Notebook', 'valor': 2500, 'categoria': 'Eletrônicos'},
        {'produto': 'Mouse', 'valor': 50, 'categoria': 'Eletrônicos'},
        {'produto': 'Livro', 'valor': 30, 'categoria': 'Educação'},
        {'produto': 'Cadeira', 'valor': 200, 'categoria': 'Móveis'},
        {'produto': 'Monitor', 'valor': 800, 'categoria': 'Eletrônicos'}
    ]
    
    def filtrar_por_categoria(vendas, categoria):
        """Filtra vendas por categoria"""
        return list(filter(lambda v: v['categoria'] == categoria, vendas))
    
    def calcular_total(vendas):
        """Calcula total das vendas"""
        return sum(map(lambda v: v['valor'], vendas))
    
    def gerar_relatorio(vendas, titulo="Relatório de Vendas"):
        """
        Gera relatório formatado das vendas.
        
        Args:
            vendas (list): Lista de vendas
            titulo (str): Título do relatório
        
        Returns:
            str: Relatório formatado
        """
        if not vendas:
            return f"{titulo}: Nenhuma venda encontrada"
        
        total = calcular_total(vendas)
        media = total / len(vendas)
        
        relatorio = [f"{titulo}:"]
        relatorio.append("-" * len(titulo))
        
        for venda in vendas:
            relatorio.append(f"• {venda['produto']}: R$ {venda['valor']}")
        
        relatorio.append("-" * len(titulo))
        relatorio.append(f"Total: R$ {total}")
        relatorio.append(f"Média: R$ {media:.2f}")
        relatorio.append(f"Quantidade: {len(vendas)} itens")
        
        return "\n".join(relatorio)
    
    print("Relatório Geral:")
    print(gerar_relatorio(vendas))
    print()
    
    print("Relatório por Categoria:")
    eletronicos = filtrar_por_categoria(vendas, 'Eletrônicos')
    print(gerar_relatorio(eletronicos, "Eletrônicos"))
    print()

def exercicios():
    """
    Exercícios progressivos para fixação de funções.
    """
    print("=== EXERCÍCIOS DE FIXAÇÃO ===")
    print()
    
    print("NÍVEL 1 - Funções Básicas:")
    print("1. Criar função que converte Celsius para Fahrenheit")
    print("2. Função que calcula área de um círculo")
    print("3. Função que verifica se número é par ou ímpar")
    print("4. Função que encontra o maior de três números")
    print("5. Função que conta vogais em uma string")
    print()
    
    print("NÍVEL 2 - Parâmetros e Retorno:")
    print("6. Função com parâmetros padrão para calcular juros")
    print("7. Função que retorna múltiplos valores (min, max, média)")
    print("8. Função que valida CPF (algoritmo completo)")
    print("9. Função recursiva para calcular potência")
    print("10. Função que usa *args para somar números variáveis")
    print()
    
    print("NÍVEL 3 - Funções Avançadas:")
    print("11. Função que usa **kwargs para criar perfil de usuário")
    print("12. Função decoradora simples (conceito avançado)")
    print("13. Função que retorna outra função (closure)")
    print("14. Sistema de cache usando funções")
    print("15. Função que processa lista com função callback")
    print()
    
    print("NÍVEL 4 - Modularização:")
    print("16. Criar módulo de utilidades matemáticas")
    print("17. Módulo de validação de dados")
    print("18. Sistema de logging modular")
    print("19. Calculadora científica modular")
    print("20. Sistema de relatórios com múltiplos módulos")
    print()
    
    # Exemplo de solução
    print("EXEMPLO DE SOLUÇÃO - Exercício 1:")
    print("def celsius_para_fahrenheit(celsius):")
    print("    '''Converte temperatura de Celsius para Fahrenheit'''")
    print("    fahrenheit = (celsius * 9/5) + 32")
    print("    return fahrenheit")
    print()
    print("# Testando")
    print("print(f'0°C = {celsius_para_fahrenheit(0)}°F')")
    print("print(f'100°C = {celsius_para_fahrenheit(100)}°F')")
    print()
    
    # Executando o exemplo
    def celsius_para_fahrenheit(celsius):
        """Converte temperatura de Celsius para Fahrenheit"""
        fahrenheit = (celsius * 9/5) + 32
        return fahrenheit
    
    print("RESULTADO:")
    print(f"   → 0°C = {celsius_para_fahrenheit(0)}°F")
    print(f"   → 100°C = {celsius_para_fahrenheit(100)}°F")
    print()

def resumo_funcoes():
    """
    Resumo visual de todos os conceitos de funções.
    """
    print("=== RESUMO DE FUNÇÕES ===")
    print()
    
    print("┌─────────────────┬─────────────────────────────────────────────────┐")
    print("│   CONCEITO      │                   DESCRIÇÃO                    │")
    print("├─────────────────┼─────────────────────────────────────────────────┤")
    print("│ def função()    │ Define uma função                               │")
    print("│ return valor    │ Retorna um valor da função                     │")
    print("│ Parâmetros      │ Dados de entrada da função                     │")
    print("│ Argumentos      │ Valores passados para os parâmetros            │")
    print("│ *args           │ Argumentos posicionais variáveis               │")
    print("│ **kwargs        │ Argumentos nomeados variáveis                  │")
    print("│ lambda          │ Função anônima de uma linha                    │")
    print("│ Recursão        │ Função que chama a si mesma                    │")
    print("│ Escopo          │ Visibilidade de variáveis                      │")
    print("│ Docstring       │ Documentação da função                         │")
    print("│ Módulos         │ Arquivos com funções relacionadas              │")
    print("└─────────────────┴─────────────────────────────────────────────────┘")
    print()
    
    print("TIPOS DE ARGUMENTOS:")
    print("• Posicionais: func(a, b)")
    print("• Nomeados: func(nome='João', idade=30)")
    print("• Padrão: func(nome, ativo=True)")
    print("• Variáveis: func(*args, **kwargs)")
    print()
    
    print("ESCOPO DE VARIÁVEIS:")
    print("• Local: Dentro da função")
    print("• Global: Fora de todas as funções")
    print("• Nonlocal: Em funções aninhadas")
    print()
    
    print("BOAS PRÁTICAS:")
    print("✅ Use nomes descritivos para funções")
    print("✅ Funções devem fazer uma coisa bem feita")
    print("✅ Prefira parâmetros a variáveis globais")
    print("✅ Documente suas funções")
    print("✅ Use type hints quando possível")
    print("✅ Mantenha funções pequenas (< 20 linhas)")
    print("✅ Evite muitos parâmetros (< 5)")
    print("✅ Use return explícito")
    print()
    
    print("QUANDO USAR CADA TIPO:")
    print("• Função normal: Tarefas gerais")
    print("• Lambda: Operações simples e rápidas")
    print("• Recursão: Problemas que se dividem")
    print("• *args: Número variável de argumentos")
    print("• **kwargs: Configurações flexíveis")
    print()

if __name__ == "__main__":
    # Demonstração completa do módulo
    print("🐍 CURSO DE PYTHON - MÓDULO 1.6: FUNÇÕES E MODULARIZAÇÃO 🐍")
    print("=" * 70)
    print()
    
    # Execução sequencial de todos os conceitos
    conceito_funcoes()
    print("-" * 50)
    
    definindo_funcoes()
    print("-" * 50)
    
    parametros_argumentos()
    print("-" * 50)
    
    args_kwargs()
    print("-" * 50)
    
    escopo_variaveis()
    print("-" * 50)
    
    funcoes_lambda()
    print("-" * 50)
    
    recursao_basica()
    print("-" * 50)
    
    docstrings_documentacao()
    print("-" * 50)
    
    modularizacao()
    print("-" * 50)
    
    exemplos_praticos()
    print("-" * 50)
    
    resumo_funcoes()
    print("-" * 50)
    
    exercicios()
    
    print("=" * 70)
    print("🎉 PARABÉNS! Você dominou Funções e Modularização!")
    print("Próximo módulo: Estruturas de Dados Nativas")
    print("=" * 70)