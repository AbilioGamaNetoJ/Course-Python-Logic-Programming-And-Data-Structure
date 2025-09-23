"""
Módulo: Estruturas de Repetição (Loops)
Tópico: Fundamentos de Lógica de Programação
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico

Objetivos de Aprendizado:
- Compreender o conceito de repetição em programação
- Dominar os loops for e while
- Usar range() eficientemente
- Controlar loops com break e continue
- Aplicar loops aninhados
- Evitar loops infinitos e otimizar performance

Conceitos Abordados:
- Loop for com range()
- Loop for com iteráveis (listas, strings)
- Loop while
- Comandos break e continue
- Loops aninhados (nested loops)
- Else em loops
- Compreensão de listas (list comprehension)
- Boas práticas e otimização

Pré-requisitos:
- Módulos anteriores: Tipos de Dados, Operadores, Estruturas Condicionais
- Conhecimento de listas básicas
- Compreensão de condições booleanas

Complexidade Temporal: O(n) para loops simples, O(n²) para loops aninhados
Complexidade Espacial: O(1) para loops simples, O(n) se criando estruturas
"""

def conceito_estruturas_repeticao():
    """
    Introduz o conceito fundamental de estruturas de repetição.
    
    Analogia: Loops são como uma playlist de música que toca repetidamente.
    Você define as regras (quantas vezes, até quando) e o programa
    executa as instruções automaticamente.
    """
    print("=== CONCEITO DE ESTRUTURAS DE REPETIÇÃO ===")
    print()
    
    print("1. O QUE SÃO ESTRUTURAS DE REPETIÇÃO?")
    print("   → Executam um bloco de código múltiplas vezes")
    print("   → Evitam repetição manual de código")
    print("   → Fundamentais para processar coleções de dados")
    print("   → Tornam programas mais eficientes e concisos")
    print()
    
    print("2. ANALOGIAS DO COTIDIANO:")
    print("   🔄 Lavar pratos: para cada prato na pia, lave e seque")
    print("   🔄 Contar ovelhas: enquanto não dormir, conte +1 ovelha")
    print("   🔄 Playlist: para cada música na lista, toque a música")
    print("   🔄 Exercício: repita 10 flexões")
    print()
    
    print("3. TIPOS PRINCIPAIS:")
    print("   ┌─────────────┬─────────────────────────────────────┐")
    print("   │    TIPO     │              QUANDO USAR            │")
    print("   ├─────────────┼─────────────────────────────────────┤")
    print("   │ for         │ Número conhecido de repetições      │")
    print("   │             │ Iterar sobre coleções (lista, etc.) │")
    print("   ├─────────────┼─────────────────────────────────────┤")
    print("   │ while       │ Repetir enquanto condição for True  │")
    print("   │             │ Número desconhecido de repetições   │")
    print("   └─────────────┴─────────────────────────────────────┘")
    print()
    
    print("4. EXEMPLO VISUAL - Sem loop vs Com loop:")
    print("   ❌ Sem loop (repetitivo):")
    print("   print('Olá!')")
    print("   print('Olá!')")
    print("   print('Olá!')")
    print("   print('Olá!')")
    print("   print('Olá!')")
    print()
    print("   ✅ Com loop (elegante):")
    print("   for i in range(5):")
    print("       print('Olá!')")
    print()
    print("   Resultado:")
    for i in range(5):
        print("   → Olá!")
    print()

def loop_for_basico():
    """
    Explora o loop for básico com range().
    
    Analogia: O for com range() é como contar nos dedos.
    Você sabe exatamente quantas vezes vai contar (0, 1, 2, 3, 4...)
    e para cada número, executa uma ação.
    """
    print("=== LOOP FOR BÁSICO ===")
    print()
    
    print("1. SINTAXE BÁSICA:")
    print("   for variavel in range(numero):")
    print("       # código a ser repetido")
    print()
    print("   → 'variavel' recebe cada valor da sequência")
    print("   → range(n) gera números de 0 até n-1")
    print("   → Indentação é obrigatória!")
    print()
    
    # Exemplo 1: Loop simples
    print("2. EXEMPLO 1: Loop simples")
    print("   for i in range(3):")
    print("       print(f'Repetição {i}')")
    print()
    print("   Resultado:")
    for i in range(3):
        print(f"   → Repetição {i}")
    print()
    
    # Exemplo 2: Usando a variável do loop
    print("3. EXEMPLO 2: Usando a variável do loop")
    print("   for numero in range(1, 6):")
    print("       quadrado = numero ** 2")
    print("       print(f'{numero}² = {quadrado}')")
    print()
    print("   Resultado:")
    for numero in range(1, 6):
        quadrado = numero ** 2
        print(f"   → {numero}² = {quadrado}")
    print()
    
    # Exemplo 3: Range com step
    print("4. EXEMPLO 3: Range com step (passo)")
    print("   for i in range(0, 10, 2):")
    print("       print(f'Número par: {i}')")
    print()
    print("   Resultado:")
    for i in range(0, 10, 2):
        print(f"   → Número par: {i}")
    print()
    
    # Exemplo 4: Range decrescente
    print("5. EXEMPLO 4: Contagem regressiva")
    print("   for i in range(5, 0, -1):")
    print("       print(f'Contagem: {i}')")
    print("   print('🚀 Decolagem!')")
    print()
    print("   Resultado:")
    for i in range(5, 0, -1):
        print(f"   → Contagem: {i}")
    print("   → 🚀 Decolagem!")
    print()
    
    # Exemplo 5: Acumulador
    print("6. EXEMPLO 5: Somando números (acumulador)")
    print("   soma = 0")
    print("   for i in range(1, 6):")
    print("       soma += i")
    print("       print(f'Somando {i}: total = {soma}')")
    print()
    print("   Resultado:")
    soma = 0
    for i in range(1, 6):
        soma += i
        print(f"   → Somando {i}: total = {soma}")
    print(f"   → Soma final: {soma}")
    print()

def loop_for_iteraveis():
    """
    Explora o loop for com iteráveis (listas, strings, etc.).
    
    Analogia: É como examinar cada item numa caixa de brinquedos.
    Você pega um brinquedo por vez, brinca com ele, depois pega o próximo.
    """
    print("=== LOOP FOR COM ITERÁVEIS ===")
    print()
    
    print("1. CONCEITO:")
    print("   → Iteráveis são objetos que podem ser percorridos")
    print("   → Listas, strings, tuplas, dicionários são iteráveis")
    print("   → Mais natural que usar índices")
    print()
    
    # Exemplo 1: Iterando sobre lista
    print("2. EXEMPLO 1: Iterando sobre lista")
    frutas = ['maçã', 'banana', 'laranja', 'uva']
    print(f"   frutas = {frutas}")
    print("   for fruta in frutas:")
    print("       print(f'Eu gosto de {fruta}')")
    print()
    print("   Resultado:")
    for fruta in frutas:
        print(f"   → Eu gosto de {fruta}")
    print()
    
    # Exemplo 2: Iterando sobre string
    print("3. EXEMPLO 2: Iterando sobre string")
    palavra = "Python"
    print(f"   palavra = '{palavra}'")
    print("   for letra in palavra:")
    print("       print(f'Letra: {letra}')")
    print()
    print("   Resultado:")
    for letra in palavra:
        print(f"   → Letra: {letra}")
    print()
    
    # Exemplo 3: Usando enumerate()
    print("4. EXEMPLO 3: Usando enumerate() para ter índice")
    cores = ['vermelho', 'verde', 'azul']
    print(f"   cores = {cores}")
    print("   for indice, cor in enumerate(cores):")
    print("       print(f'{indice}: {cor}')")
    print()
    print("   Resultado:")
    for indice, cor in enumerate(cores):
        print(f"   → {indice}: {cor}")
    print()
    
    # Exemplo 4: Processando lista de números
    print("5. EXEMPLO 4: Processando lista de números")
    notas = [8.5, 7.0, 9.2, 6.8, 8.0]
    print(f"   notas = {notas}")
    print("   soma_notas = 0")
    print("   for nota in notas:")
    print("       soma_notas += nota")
    print("   media = soma_notas / len(notas)")
    print()
    print("   Resultado:")
    soma_notas = 0
    for nota in notas:
        soma_notas += nota
    media = soma_notas / len(notas)
    print(f"   → Soma das notas: {soma_notas}")
    print(f"   → Média: {media:.2f}")
    print()
    
    # Exemplo 5: Filtrando elementos
    print("6. EXEMPLO 5: Filtrando elementos")
    numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"   numeros = {numeros}")
    print("   pares = []")
    print("   for numero in numeros:")
    print("       if numero % 2 == 0:")
    print("           pares.append(numero)")
    print()
    print("   Resultado:")
    pares = []
    for numero in numeros:
        if numero % 2 == 0:
            pares.append(numero)
    print(f"   → Números pares: {pares}")
    print()

def loop_while():
    """
    Explora o loop while - repetição baseada em condição.
    
    Analogia: While é como esperar o ônibus na parada.
    Você fica lá ENQUANTO o ônibus não chega.
    Quando ele chega (condição muda), você para de esperar.
    """
    print("=== LOOP WHILE ===")
    print()
    
    print("1. SINTAXE:")
    print("   while condição:")
    print("       # código a ser repetido")
    print("       # IMPORTANTE: modificar a condição!")
    print()
    print("   → Repete ENQUANTO a condição for True")
    print("   → Cuidado com loops infinitos!")
    print("   → Sempre modifique a variável da condição")
    print()
    
    # Exemplo 1: Contador simples
    print("2. EXEMPLO 1: Contador simples")
    print("   contador = 0")
    print("   while contador < 5:")
    print("       print(f'Contador: {contador}')")
    print("       contador += 1")
    print()
    print("   Resultado:")
    contador = 0
    while contador < 5:
        print(f"   → Contador: {contador}")
        contador += 1
    print()
    
    # Exemplo 2: Somando até limite
    print("3. EXEMPLO 2: Somando até atingir limite")
    print("   soma = 0")
    print("   numero = 1")
    print("   while soma < 50:")
    print("       soma += numero")
    print("       print(f'Somando {numero}: total = {soma}')")
    print("       numero += 1")
    print()
    print("   Resultado:")
    soma = 0
    numero = 1
    while soma < 50:
        soma += numero
        print(f"   → Somando {numero}: total = {soma}")
        numero += 1
        if numero > 10:  # Proteção contra loop infinito no exemplo
            break
    print()
    
    # Exemplo 3: Validação de entrada
    print("4. EXEMPLO 3: Simulação de validação de entrada")
    print("   # Simulando entrada do usuário")
    print("   entradas_simuladas = ['abc', '0', '-5', '10']")
    print("   indice = 0")
    print("   while True:")
    print("       entrada = entradas_simuladas[indice]")
    print("       numero = int(entrada) if entrada.isdigit() else -1")
    print("       if numero > 0:")
    print("           print(f'Número válido: {numero}')")
    print("           break")
    print("       print(f'Entrada inválida: {entrada}')")
    print("       indice += 1")
    print()
    print("   Resultado:")
    entradas_simuladas = ['abc', '0', '-5', '10']
    indice = 0
    while True:
        entrada = entradas_simuladas[indice]
        numero = int(entrada) if entrada.isdigit() else -1
        if numero > 0:
            print(f"   → Número válido: {numero}")
            break
        print(f"   → Entrada inválida: {entrada}")
        indice += 1
        if indice >= len(entradas_simuladas):  # Proteção
            break
    print()
    
    # Exemplo 4: Jogo de adivinhação
    print("5. EXEMPLO 4: Simulação de jogo de adivinhação")
    import random
    numero_secreto = random.randint(1, 10)
    tentativas = [7, 3, 5, numero_secreto]  # Simulando tentativas
    print(f"   numero_secreto = {numero_secreto} (gerado aleatoriamente)")
    print("   tentativas_simuladas = [7, 3, 5, numero_secreto]")
    print("   tentativa_atual = 0")
    print("   while True:")
    print("       palpite = tentativas_simuladas[tentativa_atual]")
    print("       if palpite == numero_secreto:")
    print("           print('Acertou!')")
    print("           break")
    print("       print(f'Errou! Tentativa: {palpite}')")
    print("       tentativa_atual += 1")
    print()
    print("   Resultado:")
    tentativa_atual = 0
    while True:
        palpite = tentativas[tentativa_atual]
        if palpite == numero_secreto:
            print("   → Acertou!")
            break
        print(f"   → Errou! Tentativa: {palpite}")
        tentativa_atual += 1
        if tentativa_atual >= len(tentativas):  # Proteção
            break
    print()

def break_continue():
    """
    Explora os comandos break e continue para controle de loops.
    
    Analogia: 
    - break é como sair da fila do banco quando percebe que esqueceu os documentos
    - continue é como pular uma música na playlist e ir para a próxima
    """
    print("=== COMANDOS BREAK E CONTINUE ===")
    print()
    
    print("1. CONCEITOS:")
    print("   break:")
    print("   → Interrompe completamente o loop")
    print("   → Sai do loop imediatamente")
    print("   → Execução continua após o loop")
    print()
    print("   continue:")
    print("   → Pula para a próxima iteração")
    print("   → Ignora o resto do código no loop atual")
    print("   → Loop continua normalmente")
    print()
    
    # Exemplo 1: break
    print("2. EXEMPLO 1: Usando break")
    print("   for i in range(10):")
    print("       if i == 5:")
    print("           print('Encontrei o 5! Parando...')")
    print("           break")
    print("       print(f'Número: {i}')")
    print("   print('Loop terminado')")
    print()
    print("   Resultado:")
    for i in range(10):
        if i == 5:
            print("   → Encontrei o 5! Parando...")
            break
        print(f"   → Número: {i}")
    print("   → Loop terminado")
    print()
    
    # Exemplo 2: continue
    print("3. EXEMPLO 2: Usando continue")
    print("   for i in range(10):")
    print("       if i % 2 == 0:")
    print("           continue  # pula números pares")
    print("       print(f'Número ímpar: {i}')")
    print()
    print("   Resultado:")
    for i in range(10):
        if i % 2 == 0:
            continue  # pula números pares
        print(f"   → Número ímpar: {i}")
    print()
    
    # Exemplo 3: break em while
    print("4. EXEMPLO 3: break em while (busca em lista)")
    nomes = ['Ana', 'Bruno', 'Carlos', 'Diana', 'Eduardo']
    nome_procurado = 'Carlos'
    print(f"   nomes = {nomes}")
    print(f"   nome_procurado = '{nome_procurado}'")
    print("   indice = 0")
    print("   while indice < len(nomes):")
    print("       if nomes[indice] == nome_procurado:")
    print("           print(f'Encontrado {nome_procurado} na posição {indice}')")
    print("           break")
    print("       indice += 1")
    print("   else:")
    print("       print(f'{nome_procurado} não encontrado')")
    print()
    print("   Resultado:")
    indice = 0
    while indice < len(nomes):
        if nomes[indice] == nome_procurado:
            print(f"   → Encontrado {nome_procurado} na posição {indice}")
            break
        indice += 1
    else:
        print(f"   → {nome_procurado} não encontrado")
    print()
    
    # Exemplo 4: continue com validação
    print("5. EXEMPLO 4: continue para validação")
    numeros = [1, -2, 3, 0, 5, -1, 7]
    print(f"   numeros = {numeros}")
    print("   print('Processando apenas números positivos:')")
    print("   for numero in numeros:")
    print("       if numero <= 0:")
    print("           continue  # pula números não positivos")
    print("       resultado = numero ** 2")
    print("       print(f'{numero}² = {resultado}')")
    print()
    print("   Resultado:")
    print("   → Processando apenas números positivos:")
    for numero in numeros:
        if numero <= 0:
            continue  # pula números não positivos
        resultado = numero ** 2
        print(f"   → {numero}² = {resultado}")
    print()

def loops_aninhados():
    """
    Explora loops aninhados (nested loops).
    
    Analogia: Loops aninhados são como examinar uma estante de livros.
    Para cada prateleira (loop externo), você examina cada livro (loop interno).
    """
    print("=== LOOPS ANINHADOS (NESTED LOOPS) ===")
    print()
    
    print("1. CONCEITO:")
    print("   → Loop dentro de outro loop")
    print("   → Loop externo controla as 'rodadas principais'")
    print("   → Loop interno executa completamente a cada rodada externa")
    print("   → Complexidade: O(n × m) onde n e m são os tamanhos dos loops")
    print()
    
    # Exemplo 1: Tabuada
    print("2. EXEMPLO 1: Tabuada completa")
    print("   for i in range(1, 4):  # números de 1 a 3")
    print("       print(f'Tabuada do {i}:')")
    print("       for j in range(1, 6):  # multiplicadores de 1 a 5")
    print("           resultado = i * j")
    print("           print(f'  {i} x {j} = {resultado}')")
    print("       print()  # linha em branco")
    print()
    print("   Resultado:")
    for i in range(1, 4):  # números de 1 a 3
        print(f"   → Tabuada do {i}:")
        for j in range(1, 6):  # multiplicadores de 1 a 5
            resultado = i * j
            print(f"     {i} x {j} = {resultado}")
        print()  # linha em branco
    
    # Exemplo 2: Matriz (grade)
    print("3. EXEMPLO 2: Criando uma matriz 3x3")
    print("   for linha in range(3):")
    print("       for coluna in range(3):")
    print("           print(f'({linha},{coluna})', end=' ')")
    print("       print()  # nova linha")
    print()
    print("   Resultado:")
    for linha in range(3):
        print("   → ", end="")
        for coluna in range(3):
            print(f"({linha},{coluna})", end=" ")
        print()  # nova linha
    print()
    
    # Exemplo 3: Padrão de estrelas
    print("4. EXEMPLO 3: Padrão de estrelas (triângulo)")
    print("   for i in range(1, 6):")
    print("       for j in range(i):")
    print("           print('*', end='')")
    print("       print()  # nova linha")
    print()
    print("   Resultado:")
    for i in range(1, 6):
        print("   → ", end="")
        for j in range(i):
            print("*", end="")
        print()  # nova linha
    print()
    
    # Exemplo 4: Busca em matriz
    print("5. EXEMPLO 4: Busca em matriz")
    matriz = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    valor_procurado = 5
    print(f"   matriz = {matriz}")
    print(f"   valor_procurado = {valor_procurado}")
    print("   encontrado = False")
    print("   for i in range(len(matriz)):")
    print("       for j in range(len(matriz[i])):")
    print("           if matriz[i][j] == valor_procurado:")
    print("               print(f'Encontrado {valor_procurado} na posição ({i},{j})')")
    print("               encontrado = True")
    print("               break")
    print("       if encontrado:")
    print("           break")
    print()
    print("   Resultado:")
    encontrado = False
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == valor_procurado:
                print(f"   → Encontrado {valor_procurado} na posição ({i},{j})")
                encontrado = True
                break
        if encontrado:
            break
    print()
    
    # Exemplo 5: Combinações
    print("6. EXEMPLO 5: Gerando combinações")
    cores = ['vermelho', 'verde', 'azul']
    tamanhos = ['P', 'M', 'G']
    print(f"   cores = {cores}")
    print(f"   tamanhos = {tamanhos}")
    print("   print('Combinações disponíveis:')")
    print("   for cor in cores:")
    print("       for tamanho in tamanhos:")
    print("           print(f'Camiseta {cor} tamanho {tamanho}')")
    print()
    print("   Resultado:")
    print("   → Combinações disponíveis:")
    for cor in cores:
        for tamanho in tamanhos:
            print(f"     Camiseta {cor} tamanho {tamanho}")
    print()

def else_em_loops():
    """
    Explora a cláusula else em loops - um recurso único do Python.
    
    Analogia: O else em loops é como um "plano B" que só executa
    se você completou toda a tarefa sem interrupções (sem break).
    """
    print("=== ELSE EM LOOPS ===")
    print()
    
    print("1. CONCEITO:")
    print("   → Cláusula else OPCIONAL em loops for e while")
    print("   → Executa APENAS se o loop completar normalmente")
    print("   → NÃO executa se o loop for interrompido por break")
    print("   → Útil para detectar se algo foi encontrado ou não")
    print()
    
    # Exemplo 1: Busca com else
    print("2. EXEMPLO 1: Busca com else")
    numeros = [2, 4, 6, 8, 10]
    procurado = 7
    print(f"   numeros = {numeros}")
    print(f"   procurado = {procurado}")
    print("   for numero in numeros:")
    print("       if numero == procurado:")
    print("           print(f'Encontrado: {procurado}')")
    print("           break")
    print("   else:")
    print("       print(f'{procurado} não foi encontrado')")
    print()
    print("   Resultado:")
    for numero in numeros:
        if numero == procurado:
            print(f"   → Encontrado: {procurado}")
            break
    else:
        print(f"   → {procurado} não foi encontrado")
    print()
    
    # Exemplo 2: Validação de senha
    print("3. EXEMPLO 2: Validação de senha")
    senha = "python123"
    senhas_proibidas = ["123456", "password", "admin"]
    print(f"   senha = '{senha}'")
    print(f"   senhas_proibidas = {senhas_proibidas}")
    print("   for senha_proibida in senhas_proibidas:")
    print("       if senha == senha_proibida:")
    print("           print('Senha muito comum! Escolha outra.')")
    print("           break")
    print("   else:")
    print("       print('Senha aceita!')")
    print()
    print("   Resultado:")
    for senha_proibida in senhas_proibidas:
        if senha == senha_proibida:
            print("   → Senha muito comum! Escolha outra.")
            break
    else:
        print("   → Senha aceita!")
    print()
    
    # Exemplo 3: While com else
    print("4. EXEMPLO 3: While com else")
    print("   contador = 0")
    print("   while contador < 3:")
    print("       print(f'Tentativa {contador + 1}')")
    print("       contador += 1")
    print("       # Simula uma condição que nunca acontece")
    print("       if False:  # nunca será True")
    print("           break")
    print("   else:")
    print("       print('Todas as tentativas foram concluídas')")
    print()
    print("   Resultado:")
    contador = 0
    while contador < 3:
        print(f"   → Tentativa {contador + 1}")
        contador += 1
        # Simula uma condição que nunca acontece
        if False:  # nunca será True
            break
    else:
        print("   → Todas as tentativas foram concluídas")
    print()

def list_comprehension():
    """
    Introduz list comprehension - uma forma pythônica de criar listas.
    
    Analogia: List comprehension é como uma máquina de produção em série.
    Você define o molde (expressão) e a matéria-prima (iterável),
    e ela produz uma lista automaticamente.
    """
    print("=== LIST COMPREHENSION ===")
    print()
    
    print("1. CONCEITO:")
    print("   → Forma concisa de criar listas")
    print("   → Substitui loops for simples")
    print("   → Mais eficiente e 'pythônica'")
    print("   → Sintaxe: [expressão for item in iterável if condição]")
    print()
    
    # Exemplo 1: Comparação loop vs comprehension
    print("2. EXEMPLO 1: Loop tradicional vs List Comprehension")
    print("   # Método tradicional:")
    print("   quadrados = []")
    print("   for i in range(5):")
    print("       quadrados.append(i ** 2)")
    print()
    print("   # List comprehension:")
    print("   quadrados = [i ** 2 for i in range(5)]")
    print()
    print("   Resultado:")
    
    # Método tradicional
    quadrados_tradicional = []
    for i in range(5):
        quadrados_tradicional.append(i ** 2)
    
    # List comprehension
    quadrados_comprehension = [i ** 2 for i in range(5)]
    
    print(f"   → Tradicional: {quadrados_tradicional}")
    print(f"   → Comprehension: {quadrados_comprehension}")
    print()
    
    # Exemplo 2: Com condição
    print("3. EXEMPLO 2: List comprehension com condição")
    numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"   numeros = {numeros}")
    print("   pares = [n for n in numeros if n % 2 == 0]")
    print()
    pares = [n for n in numeros if n % 2 == 0]
    print(f"   → Números pares: {pares}")
    print()
    
    # Exemplo 3: Transformação de strings
    print("4. EXEMPLO 3: Transformação de strings")
    palavras = ['python', 'java', 'javascript', 'go']
    print(f"   palavras = {palavras}")
    print("   maiusculas = [palavra.upper() for palavra in palavras]")
    print("   tamanhos = [len(palavra) for palavra in palavras]")
    print()
    maiusculas = [palavra.upper() for palavra in palavras]
    tamanhos = [len(palavra) for palavra in palavras]
    print(f"   → Maiúsculas: {maiusculas}")
    print(f"   → Tamanhos: {tamanhos}")
    print()
    
    # Exemplo 4: Comprehension aninhada
    print("5. EXEMPLO 4: List comprehension aninhada")
    print("   matriz = [[i*j for j in range(1, 4)] for i in range(1, 4)]")
    print()
    matriz = [[i*j for j in range(1, 4)] for i in range(1, 4)]
    print("   → Matriz gerada:")
    for linha in matriz:
        print(f"     {linha}")
    print()

def boas_praticas_loops():
    """
    Apresenta boas práticas para estruturas de repetição.
    """
    print("=== BOAS PRÁTICAS EM LOOPS ===")
    print()
    
    print("1. EVITE LOOPS INFINITOS:")
    print("   ❌ Perigoso:")
    print("   while True:")
    print("       print('Isso nunca para!')  # Loop infinito!")
    print()
    print("   ✅ Melhor:")
    print("   contador = 0")
    print("   while contador < 10:")
    print("       print(f'Iteração {contador}')")
    print("       contador += 1  # SEMPRE modifique a condição!")
    print()
    
    print("2. USE NOMES DESCRITIVOS:")
    print("   ❌ Ruim:")
    print("   for i in lista:")
    print("       for j in i:")
    print("           print(j)")
    print()
    print("   ✅ Melhor:")
    print("   for linha in matriz:")
    print("       for elemento in linha:")
    print("           print(elemento)")
    print()
    
    print("3. PREFIRA ITERAÇÃO DIRETA:")
    print("   ❌ Menos pythônico:")
    print("   for i in range(len(lista)):")
    print("       print(lista[i])")
    print()
    print("   ✅ Mais pythônico:")
    print("   for item in lista:")
    print("       print(item)")
    print()
    print("   ✅ Se precisar do índice:")
    print("   for i, item in enumerate(lista):")
    print("       print(f'{i}: {item}')")
    print()
    
    print("4. USE LIST COMPREHENSION QUANDO APROPRIADO:")
    print("   ✅ Para transformações simples:")
    print("   quadrados = [x**2 for x in numeros]")
    print()
    print("   ❌ Evite para lógica complexa:")
    print("   # Muito complexo para comprehension")
    print("   resultado = []")
    print("   for item in lista:")
    print("       if condicao_complexa(item):")
    print("           valor = transformacao_complexa(item)")
    print("           resultado.append(valor)")
    print()
    
    print("5. CUIDADO COM LOOPS ANINHADOS:")
    print("   → Complexidade cresce rapidamente: O(n²), O(n³)...")
    print("   → Considere algoritmos mais eficientes")
    print("   → Use break/continue para otimizar quando possível")
    print()

def exemplos_praticos():
    """
    Exemplos práticos integrando todos os conceitos de loops.
    """
    print("=== EXEMPLOS PRÁTICOS INTEGRADOS ===")
    print()
    
    # Exemplo 1: Análise de vendas
    print("Exemplo 1: Análise de Vendas Mensais")
    vendas_mensais = [15000, 18000, 12000, 22000, 19000, 25000, 
                     28000, 24000, 21000, 26000, 30000, 35000]
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
             'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    print("Relatório de Vendas 2024:")
    print("-" * 30)
    
    total_vendas = 0
    melhor_mes = ""
    maior_venda = 0
    meses_acima_media = []
    
    # Primeira passada: calcular total e encontrar melhor mês
    for i, venda in enumerate(vendas_mensais):
        total_vendas += venda
        if venda > maior_venda:
            maior_venda = venda
            melhor_mes = meses[i]
    
    media_mensal = total_vendas / len(vendas_mensais)
    
    # Segunda passada: identificar meses acima da média
    for i, venda in enumerate(vendas_mensais):
        if venda > media_mensal:
            meses_acima_media.append(meses[i])
    
    # Relatório detalhado
    for mes, venda in zip(meses, vendas_mensais):
        status = "📈" if venda > media_mensal else "📉"
        print(f"{mes}: R$ {venda:,} {status}")
    
    print("-" * 30)
    print(f"Total anual: R$ {total_vendas:,}")
    print(f"Média mensal: R$ {media_mensal:,.2f}")
    print(f"Melhor mês: {melhor_mes} (R$ {maior_venda:,})")
    print(f"Meses acima da média: {', '.join(meses_acima_media)}")
    print()
    
    # Exemplo 2: Validador de CPF
    print("Exemplo 2: Validador de CPF (algoritmo simplificado)")
    cpfs_teste = ["12345678901", "11111111111", "12345678900"]
    
    for cpf in cpfs_teste:
        print(f"Validando CPF: {cpf}")
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11 or not cpf.isdigit():
            print("→ ❌ CPF inválido: deve ter 11 dígitos numéricos")
            continue
        
        # Verifica se não são todos iguais
        if cpf == cpf[0] * 11:
            print("→ ❌ CPF inválido: todos os dígitos são iguais")
            continue
        
        # Cálculo simplificado do primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        
        primeiro_digito = 11 - (soma % 11)
        if primeiro_digito >= 10:
            primeiro_digito = 0
        
        if int(cpf[9]) == primeiro_digito:
            print("→ ✅ CPF válido (verificação simplificada)")
        else:
            print("→ ❌ CPF inválido: dígito verificador incorreto")
        print()
    
    # Exemplo 3: Jogo da Forca (simulado)
    print("Exemplo 3: Jogo da Forca (simulado)")
    palavra_secreta = "PYTHON"
    tentativas_simuladas = ['P', 'A', 'Y', 'T', 'H', 'O', 'N']
    letras_descobertas = set()
    tentativas_erradas = []
    max_erros = 6
    
    print(f"Palavra secreta: {'*' * len(palavra_secreta)}")
    print(f"Tentativas permitidas: {max_erros}")
    print()
    
    for tentativa in tentativas_simuladas:
        print(f"Tentativa: {tentativa}")
        
        if tentativa in palavra_secreta:
            letras_descobertas.add(tentativa)
            print("→ ✅ Letra correta!")
        else:
            tentativas_erradas.append(tentativa)
            print("→ ❌ Letra incorreta!")
        
        # Mostra o progresso
        palavra_mostrada = ""
        for letra in palavra_secreta:
            if letra in letras_descobertas:
                palavra_mostrada += letra
            else:
                palavra_mostrada += "_"
        
        print(f"Palavra: {palavra_mostrada}")
        print(f"Erros: {len(tentativas_erradas)}/{max_erros}")
        
        # Verifica condições de vitória/derrota
        if set(palavra_secreta) <= letras_descobertas:
            print("🎉 Parabéns! Você ganhou!")
            break
        elif len(tentativas_erradas) >= max_erros:
            print("💀 Game Over! Você perdeu!")
            break
        
        print("-" * 20)
    print()

def exercicios():
    """
    Exercícios progressivos para fixação das estruturas de repetição.
    """
    print("=== EXERCÍCIOS DE FIXAÇÃO ===")
    print()
    
    print("NÍVEL 1 - Básico (for e while simples):")
    print("1. Imprimir números de 1 a 10")
    print("2. Calcular a soma dos números de 1 a 100")
    print("3. Imprimir a tabuada do 7")
    print("4. Contar quantas vezes a letra 'a' aparece numa palavra")
    print("5. Encontrar o maior número numa lista")
    print()
    
    print("NÍVEL 2 - Intermediário (loops com condições):")
    print("6. Imprimir apenas números pares de 1 a 20")
    print("7. Calcular fatorial de um número")
    print("8. Verificar se um número é primo")
    print("9. Inverter uma string usando loop")
    print("10. Contar vogais e consoantes numa frase")
    print()
    
    print("NÍVEL 3 - Avançado (loops aninhados e complexos):")
    print("11. Criar um padrão de estrelas (pirâmide)")
    print("12. Multiplicar duas matrizes")
    print("13. Encontrar todos os números primos até N")
    print("14. Implementar busca sequencial em lista")
    print("15. Criar um menu interativo com while")
    print()
    
    print("NÍVEL 4 - List Comprehension:")
    print("16. Criar lista dos quadrados dos números pares de 1 a 20")
    print("17. Filtrar palavras com mais de 5 letras de uma lista")
    print("18. Criar matriz 3x3 com números sequenciais")
    print("19. Extrair apenas números positivos de uma lista mista")
    print("20. Converter lista de temperaturas Celsius para Fahrenheit")
    print()
    
    # Exemplo de solução
    print("EXEMPLO DE SOLUÇÃO - Exercício 2:")
    print("# Calcular a soma dos números de 1 a 100")
    print("soma = 0")
    print("for i in range(1, 101):")
    print("    soma += i")
    print("print(f'A soma é: {soma}')")
    print()
    print("# Ou usando a fórmula matemática:")
    print("n = 100")
    print("soma = n * (n + 1) // 2")
    print("print(f'A soma é: {soma}')")
    print()
    
    # Executando o exemplo
    print("RESULTADO:")
    soma = 0
    for i in range(1, 101):
        soma += i
    print(f"→ Método loop: {soma}")
    
    n = 100
    soma_formula = n * (n + 1) // 2
    print(f"→ Método fórmula: {soma_formula}")
    print()

def resumo_estruturas_repeticao():
    """
    Resumo visual de todas as estruturas de repetição.
    """
    print("=== RESUMO DAS ESTRUTURAS DE REPETIÇÃO ===")
    print()
    
    print("┌─────────────────┬─────────────────────────────────────────────────┐")
    print("│   ESTRUTURA     │                   QUANDO USAR                  │")
    print("├─────────────────┼─────────────────────────────────────────────────┤")
    print("│ for range()     │ Número conhecido de repetições                 │")
    print("│ for iterável    │ Percorrer listas, strings, etc.                │")
    print("│ while           │ Repetir enquanto condição for True             │")
    print("│ break           │ Sair do loop imediatamente                     │")
    print("│ continue        │ Pular para próxima iteração                    │")
    print("│ else em loop    │ Executar se loop completar sem break           │")
    print("│ List comprehension│ Criar listas de forma concisa                │")
    print("└─────────────────┴─────────────────────────────────────────────────┘")
    print()
    
    print("COMPLEXIDADE TEMPORAL:")
    print("• Loop simples: O(n)")
    print("• Loops aninhados: O(n²), O(n³), etc.")
    print("• List comprehension: O(n) - geralmente mais eficiente")
    print()
    
    print("BOAS PRÁTICAS:")
    print("✅ Use nomes descritivos para variáveis de loop")
    print("✅ Prefira iteração direta sobre índices")
    print("✅ Use enumerate() quando precisar de índices")
    print("✅ Evite loops aninhados desnecessários")
    print("✅ Use list comprehension para transformações simples")
    print("✅ Sempre modifique a condição em loops while")
    print("✅ Use break/continue para otimizar quando apropriado")
    print()
    
    print("PADRÕES COMUNS:")
    print("• Acumulador: soma += valor")
    print("• Contador: contador += 1")
    print("• Busca: if item == procurado: break")
    print("• Filtro: if condicao: lista.append(item)")
    print("• Transformação: nova_lista = [f(x) for x in lista]")
    print()

if __name__ == "__main__":
    # Demonstração completa do módulo
    print("🐍 CURSO DE PYTHON - MÓDULO 1.5: ESTRUTURAS DE REPETIÇÃO 🐍")
    print("=" * 70)
    print()
    
    # Execução sequencial de todos os conceitos
    conceito_estruturas_repeticao()
    print("-" * 50)
    
    loop_for_basico()
    print("-" * 50)
    
    loop_for_iteraveis()
    print("-" * 50)
    
    loop_while()
    print("-" * 50)
    
    break_continue()
    print("-" * 50)
    
    loops_aninhados()
    print("-" * 50)
    
    else_em_loops()
    print("-" * 50)
    
    list_comprehension()
    print("-" * 50)
    
    boas_praticas_loops()
    print("-" * 50)
    
    exemplos_praticos()
    print("-" * 50)
    
    resumo_estruturas_repeticao()
    print("-" * 50)
    
    exercicios()
    
    print("=" * 70)
    print("🎉 PARABÉNS! Você dominou as Estruturas de Repetição!")
    print("Próximo módulo: Funções e Modularização")
    print("=" * 70)