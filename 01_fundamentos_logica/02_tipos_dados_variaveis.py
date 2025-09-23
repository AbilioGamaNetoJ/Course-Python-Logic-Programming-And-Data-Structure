"""
Módulo: Tipos de Dados e Variáveis
Tópico: Fundamentos de Lógica de Programação
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico

Objetivos de Aprendizado:
- Compreender o conceito de variáveis como "caixas" de dados
- Conhecer os tipos de dados fundamentais do Python
- Entender tipagem dinâmica e como Python gerencia tipos
- Aprender conversões entre tipos (casting)
- Dominar operações básicas com cada tipo de dado

Conceitos Abordados:
- Variáveis e atribuição
- Tipos primitivos: int, float, str, bool
- Tipagem dinâmica
- Conversão de tipos (casting)
- Operações com strings
- Valores especiais: None, True, False

Pré-requisitos:
- Módulo anterior: Introdução ao Python
- Conceitos básicos de print() e variáveis
"""

def conceito_variaveis():
    """
    Explica o conceito fundamental de variáveis em programação.
    
    Analogia: Variáveis são como caixas etiquetadas onde guardamos coisas.
    Cada caixa tem um nome (rótulo) e pode conter diferentes tipos de objetos.
    Podemos trocar o conteúdo da caixa, mas o nome permanece o mesmo.
    
    Returns:
        None: Função demonstrativa
    """
    print("=== CONCEITO DE VARIÁVEIS ===")
    print()
    
    # Passo 1: Analogia das caixas
    print("1. VARIÁVEIS SÃO COMO CAIXAS ETIQUETADAS:")
    print("   📦 Caixa 'nome' → contém 'João'")
    print("   📦 Caixa 'idade' → contém 25")
    print("   📦 Caixa 'altura' → contém 1.75")
    print()
    
    # Demonstração prática
    nome = 'João'
    idade = 25
    altura = 1.75
    
    print("   Em Python:")
    print(f"   nome = '{nome}'     # Caixa 'nome' recebe texto")
    print(f"   idade = {idade}        # Caixa 'idade' recebe número inteiro")
    print(f"   altura = {altura}     # Caixa 'altura' recebe número decimal")
    print()
    
    # Passo 2: Reatribuição (trocar conteúdo da caixa)
    print("2. PODEMOS TROCAR O CONTEÚDO DAS CAIXAS:")
    print(f"   Antes: nome = '{nome}'")
    nome = 'Maria'
    print(f"   Depois: nome = '{nome}'")
    print("   → A mesma caixa 'nome' agora contém outro valor!")
    print()
    
    # Passo 3: Regras para nomes de variáveis
    print("3. REGRAS PARA NOMES DE VARIÁVEIS:")
    print("   ✅ Podem conter letras, números e underscore (_)")
    print("   ✅ Devem começar com letra ou underscore")
    print("   ✅ São case-sensitive (nome ≠ Nome)")
    print("   ❌ Não podem ser palavras reservadas (if, for, while...)")
    print()
    
    # Exemplos de nomes válidos e inválidos
    print("   Exemplos válidos:")
    nome_completo = "João Silva"
    idade2 = 30
    _privado = "secreto"
    print(f"   nome_completo = '{nome_completo}'")
    print(f"   idade2 = {idade2}")
    print(f"   _privado = '{_privado}'")
    print()
    
    print("   Exemplos inválidos:")
    print("   ❌ 2nome = 'João'      # Não pode começar com número")
    print("   ❌ nome-completo = ... # Hífen não é permitido")
    print("   ❌ if = 10            # 'if' é palavra reservada")
    print()

def tipos_numericos():
    """
    Explora os tipos numéricos do Python: int e float.
    
    Analogia: int são números inteiros como contar objetos (1, 2, 3...).
    float são números com vírgula como medir altura (1.75m, 2.30m...).
    """
    print("=== TIPOS NUMÉRICOS ===")
    print()
    
    # Passo 1: Números inteiros (int)
    print("1. NÚMEROS INTEIROS (int):")
    print("   → Números sem vírgula: ..., -2, -1, 0, 1, 2, ...")
    print("   → Usados para contar, indexar, loops")
    print()
    
    # Exemplos práticos de int
    quantidade_alunos = 30
    temperatura = -5
    ano_nascimento = 1990
    
    print("   Exemplos:")
    print(f"   quantidade_alunos = {quantidade_alunos}")
    print(f"   temperatura = {temperatura}")
    print(f"   ano_nascimento = {ano_nascimento}")
    print(f"   type(quantidade_alunos) = {type(quantidade_alunos)}")
    print()
    
    # Passo 2: Números decimais (float)
    print("2. NÚMEROS DECIMAIS (float):")
    print("   → Números com vírgula (ponto em Python): 1.5, 3.14, -2.7")
    print("   → Usados para medidas, cálculos precisos, percentuais")
    print()
    
    # Exemplos práticos de float
    altura = 1.75
    peso = 70.5
    pi = 3.14159
    preco = 29.99
    
    print("   Exemplos:")
    print(f"   altura = {altura}")
    print(f"   peso = {peso}")
    print(f"   pi = {pi}")
    print(f"   preco = {preco}")
    print(f"   type(altura) = {type(altura)}")
    print()
    
    # Passo 3: Operações matemáticas
    print("3. OPERAÇÕES MATEMÁTICAS:")
    a = 10
    b = 3
    
    print(f"   a = {a}, b = {b}")
    print(f"   a + b = {a + b}    # Soma")
    print(f"   a - b = {a - b}    # Subtração")
    print(f"   a * b = {a * b}   # Multiplicação")
    print(f"   a / b = {a / b:.2f}  # Divisão (sempre retorna float)")
    print(f"   a // b = {a // b}   # Divisão inteira")
    print(f"   a % b = {a % b}    # Resto da divisão (módulo)")
    print(f"   a ** b = {a ** b}  # Potenciação")
    print()

def tipo_string():
    """
    Explora o tipo string (texto) em Python.
    
    Analogia: Strings são como frases ou palavras escritas.
    Podem ser curtas como "Oi" ou longas como um parágrafo inteiro.
    """
    print("=== TIPO STRING (TEXTO) ===")
    print()
    
    # Passo 1: Criando strings
    print("1. CRIANDO STRINGS:")
    print("   → Texto entre aspas simples: 'Olá'")
    print("   → Texto entre aspas duplas: \"Mundo\"")
    print("   → Texto multilinha: '''...''' ou \"\"\"...\"\"\"")
    print()
    
    # Exemplos de criação
    nome = 'Python'
    linguagem = "Programação"
    descricao = """Python é uma linguagem
    de programação poderosa
    e fácil de aprender"""
    
    print("   Exemplos:")
    print(f"   nome = '{nome}'")
    print(f"   linguagem = \"{linguagem}\"")
    print(f"   descricao = '''{descricao}'''")
    print(f"   type(nome) = {type(nome)}")
    print()
    
    # Passo 2: Operações com strings
    print("2. OPERAÇÕES COM STRINGS:")
    primeiro_nome = "João"
    sobrenome = "Silva"
    
    print(f"   primeiro_nome = '{primeiro_nome}'")
    print(f"   sobrenome = '{sobrenome}'")
    print()
    
    # Concatenação (juntar strings)
    nome_completo = primeiro_nome + " " + sobrenome
    print(f"   Concatenação: '{primeiro_nome}' + ' ' + '{sobrenome}' = '{nome_completo}'")
    
    # Repetição
    risada = "ha" * 5
    print(f"   Repetição: 'ha' * 5 = '{risada}'")
    
    # Tamanho
    print(f"   Tamanho: len('{nome_completo}') = {len(nome_completo)} caracteres")
    print()
    
    # Passo 3: Formatação de strings
    print("3. FORMATAÇÃO DE STRINGS:")
    nome = "Ana"
    idade = 25
    
    # Método f-string (mais moderno)
    mensagem1 = f"Meu nome é {nome} e tenho {idade} anos"
    print(f"   f-string: f\"Meu nome é {{nome}} e tenho {{idade}} anos\"")
    print(f"   Resultado: '{mensagem1}'")
    
    # Método .format()
    mensagem2 = "Meu nome é {} e tenho {} anos".format(nome, idade)
    print(f"   .format(): \"Meu nome é {{}} e tenho {{}} anos\".format(nome, idade)")
    print(f"   Resultado: '{mensagem2}'")
    print()
    
    # Passo 4: Métodos úteis de string
    print("4. MÉTODOS ÚTEIS DE STRING:")
    texto = "  Python é Incrível!  "
    print(f"   texto = '{texto}'")
    print(f"   texto.upper() = '{texto.upper()}'      # Maiúsculas")
    print(f"   texto.lower() = '{texto.lower()}'      # Minúsculas")
    print(f"   texto.strip() = '{texto.strip()}'    # Remove espaços das bordas")
    print(f"   texto.replace('Python', 'Java') = '{texto.replace('Python', 'Java')}'")
    print()

def tipo_boolean():
    """
    Explora o tipo boolean (verdadeiro/falso) em Python.
    
    Analogia: Boolean é como um interruptor de luz - só pode estar
    ligado (True) ou desligado (False). Não há meio termo.
    """
    print("=== TIPO BOOLEAN (VERDADEIRO/FALSO) ===")
    print()
    
    # Passo 1: Valores boolean
    print("1. VALORES BOOLEAN:")
    print("   → Apenas dois valores possíveis: True e False")
    print("   → Sempre com primeira letra maiúscula")
    print("   → Resultado de comparações e operações lógicas")
    print()
    
    # Exemplos básicos
    verdadeiro = True
    falso = False
    
    print("   Exemplos:")
    print(f"   verdadeiro = {verdadeiro}")
    print(f"   falso = {falso}")
    print(f"   type(verdadeiro) = {type(verdadeiro)}")
    print()
    
    # Passo 2: Comparações que geram boolean
    print("2. COMPARAÇÕES (GERAM BOOLEAN):")
    a = 10
    b = 5
    
    print(f"   a = {a}, b = {b}")
    print(f"   a > b = {a > b}     # Maior que")
    print(f"   a < b = {a < b}     # Menor que")
    print(f"   a >= b = {a >= b}    # Maior ou igual")
    print(f"   a <= b = {a <= b}    # Menor ou igual")
    print(f"   a == b = {a == b}    # Igual (atenção: dois sinais =)")
    print(f"   a != b = {a != b}    # Diferente")
    print()
    
    # Passo 3: Operadores lógicos
    print("3. OPERADORES LÓGICOS:")
    tem_chuva = True
    tem_guarda_chuva = False
    
    print(f"   tem_chuva = {tem_chuva}")
    print(f"   tem_guarda_chuva = {tem_guarda_chuva}")
    print()
    
    print(f"   tem_chuva and tem_guarda_chuva = {tem_chuva and tem_guarda_chuva}")
    print("   → 'and' só é True se AMBOS forem True")
    
    print(f"   tem_chuva or tem_guarda_chuva = {tem_chuva or tem_guarda_chuva}")
    print("   → 'or' é True se PELO MENOS UM for True")
    
    print(f"   not tem_chuva = {not tem_chuva}")
    print("   → 'not' inverte o valor (True vira False e vice-versa)")
    print()
    
    # Passo 4: Valores que Python considera False
    print("4. VALORES 'FALSY' (Python considera False):")
    valores_falsy = [False, 0, 0.0, "", [], {}, None]
    
    for valor in valores_falsy:
        print(f"   bool({repr(valor)}) = {bool(valor)}")
    
    print()
    print("   → Qualquer outro valor é considerado True!")
    print(f"   bool(1) = {bool(1)}")
    print(f"   bool('texto') = {bool('texto')}")
    print(f"   bool([1, 2, 3]) = {bool([1, 2, 3])}")
    print()

def conversao_tipos():
    """
    Demonstra como converter entre diferentes tipos de dados.
    
    Analogia: Conversão é como traduzir entre idiomas diferentes.
    Às vezes a tradução é perfeita, às vezes perdemos informação,
    e às vezes é impossível traduzir.
    """
    print("=== CONVERSÃO ENTRE TIPOS (CASTING) ===")
    print()
    
    # Passo 1: Conversões numéricas
    print("1. CONVERSÕES NUMÉRICAS:")
    
    # int para float
    numero_int = 42
    numero_float = float(numero_int)
    print(f"   int → float: float({numero_int}) = {numero_float}")
    
    # float para int (perde a parte decimal)
    numero_float = 3.14
    numero_int = int(numero_float)
    print(f"   float → int: int({numero_float}) = {numero_int} (perde decimais!)")
    
    # string para número
    texto_numero = "123"
    numero = int(texto_numero)
    print(f"   string → int: int('{texto_numero}') = {numero}")
    
    texto_decimal = "45.67"
    decimal = float(texto_decimal)
    print(f"   string → float: float('{texto_decimal}') = {decimal}")
    print()
    
    # Passo 2: Conversões para string
    print("2. CONVERSÕES PARA STRING:")
    idade = 25
    altura = 1.75
    ativo = True
    
    print(f"   int → string: str({idade}) = '{str(idade)}'")
    print(f"   float → string: str({altura}) = '{str(altura)}'")
    print(f"   bool → string: str({ativo}) = '{str(ativo)}'")
    print()
    
    # Passo 3: Conversões para boolean
    print("3. CONVERSÕES PARA BOOLEAN:")
    valores = [0, 1, -1, "", "texto", [], [1, 2], None]
    
    for valor in valores:
        resultado = bool(valor)
        print(f"   bool({repr(valor)}) = {resultado}")
    print()
    
    # Passo 4: Cuidados com conversões
    print("4. CUIDADOS COM CONVERSÕES:")
    print("   ⚠️  Nem toda conversão é possível:")
    print("   int('abc') → ERRO! Não é um número válido")
    print("   float('3.14.15') → ERRO! Formato inválido")
    print()
    
    # Exemplo de tratamento de erro
    print("   💡 Sempre verifique se a conversão é possível:")
    texto = "123"
    if texto.isdigit():
        numero = int(texto)
        print(f"   '{texto}' é um número válido: {numero}")
    else:
        print(f"   '{texto}' não é um número válido")
    print()

def tipo_none():
    """
    Explica o tipo especial None em Python.
    
    Analogia: None é como uma caixa vazia com uma etiqueta dizendo "vazio".
    É diferente de não ter caixa - a caixa existe, mas não tem nada dentro.
    """
    print("=== TIPO ESPECIAL: NONE ===")
    print()
    
    print("1. O QUE É NONE:")
    print("   → Representa 'nada' ou 'ausência de valor'")
    print("   → Diferente de 0, False ou string vazia")
    print("   → Usado quando uma variável existe mas não tem valor definido")
    print()
    
    # Exemplos de uso
    resultado = None
    nome_usuario = None
    
    print("   Exemplos:")
    print(f"   resultado = {resultado}")
    print(f"   nome_usuario = {nome_usuario}")
    print(f"   type(resultado) = {type(resultado)}")
    print()
    
    # Verificando se é None
    print("2. VERIFICANDO SE É NONE:")
    print(f"   resultado is None = {resultado is None}")
    print(f"   resultado == None = {resultado == None}")
    print("   → Use 'is None' ao invés de '== None' (boa prática)")
    print()
    
    # None em funções
    print("3. NONE EM FUNÇÕES:")
    print("   → Funções que não retornam nada, retornam None")
    
    def funcao_sem_return():
        print("   Esta função não tem return")
    
    retorno = funcao_sem_return()
    print(f"   retorno = {retorno}")
    print()

def exemplos_praticos():
    """
    Demonstrações práticas integrando todos os tipos de dados.
    """
    print("=== EXEMPLOS PRÁTICOS ===")
    print()
    
    # Exemplo 1: Cadastro de pessoa
    print("Exemplo 1: Cadastro de Pessoa")
    nome = "Ana Silva"
    idade = 28
    altura = 1.65
    tem_carteira = True
    salario = None  # Ainda não informado
    
    print(f"Nome: {nome} (tipo: {type(nome).__name__})")
    print(f"Idade: {idade} anos (tipo: {type(idade).__name__})")
    print(f"Altura: {altura}m (tipo: {type(altura).__name__})")
    print(f"Tem carteira: {tem_carteira} (tipo: {type(tem_carteira).__name__})")
    print(f"Salário: {salario} (tipo: {type(salario).__name__})")
    print()
    
    # Exemplo 2: Calculadora de IMC
    print("Exemplo 2: Calculadora de IMC")
    peso = 70.5
    altura = 1.75
    imc = peso / (altura ** 2)
    
    print(f"Peso: {peso}kg")
    print(f"Altura: {altura}m")
    print(f"IMC: {imc:.2f}")
    
    # Classificação usando boolean
    sobrepeso = imc > 25
    print(f"Está com sobrepeso? {sobrepeso}")
    print()
    
    # Exemplo 3: Processamento de dados
    print("Exemplo 3: Processamento de Entrada do Usuário")
    entrada_idade = "25"  # Simulando input do usuário
    entrada_altura = "1.75"
    
    # Conversões necessárias
    idade_numerica = int(entrada_idade)
    altura_numerica = float(entrada_altura)
    
    print(f"Entrada original: '{entrada_idade}' e '{entrada_altura}'")
    print(f"Após conversão: {idade_numerica} e {altura_numerica}")
    
    # Validação
    idade_valida = 0 <= idade_numerica <= 120
    altura_valida = 0.5 <= altura_numerica <= 3.0
    
    print(f"Idade válida? {idade_valida}")
    print(f"Altura válida? {altura_valida}")
    print()

def exercicios():
    """
    Exercícios para fixação do conteúdo sobre tipos de dados.
    
    Nível 1: Exercícios básicos com tipos individuais
    Nível 2: Exercícios intermediários combinando tipos
    Nível 3: Exercícios avançados com conversões e validações
    """
    print("=== EXERCÍCIOS DE FIXAÇÃO ===")
    print()
    
    print("NÍVEL 1 - Básico:")
    print("1. Crie variáveis para armazenar: nome, idade, altura e se é estudante")
    print("2. Faça operações matemáticas com dois números inteiros")
    print("3. Crie uma string com seu nome completo e exiba seu tamanho")
    print("4. Compare dois números e exiba se o primeiro é maior que o segundo")
    print("5. Use operadores lógicos para combinar duas condições")
    print()
    
    print("NÍVEL 2 - Intermediário:")
    print("6. Converta uma string numérica para int e faça cálculos")
    print("7. Crie uma mensagem formatada usando f-strings")
    print("8. Verifique se uma variável é None e trate adequadamente")
    print("9. Calcule a média de três notas (use float)")
    print("10. Determine se um ano é bissexto (use operadores lógicos)")
    print()
    
    print("NÍVEL 3 - Avançado:")
    print("11. Crie um validador de idade (string → int com verificação)")
    print("12. Faça um conversor de temperatura com validação de entrada")
    print("13. Implemente um sistema de login simples (nome e senha)")
    print("14. Crie um calculador de desconto com diferentes tipos de dados")
    print("15. Desenvolva um analisador de texto (tamanho, maiúsculas, etc.)")
    print()
    
    # Exemplo de solução
    print("EXEMPLO DE SOLUÇÃO - Exercício 1:")
    print("# Criando variáveis com diferentes tipos")
    print("nome = 'João Silva'")
    print("idade = 25")
    print("altura = 1.80")
    print("eh_estudante = True")
    print()
    print("# Exibindo informações")
    print("print(f'Nome: {nome}')")
    print("print(f'Idade: {idade} anos')")
    print("print(f'Altura: {altura}m')")
    print("print(f'É estudante: {eh_estudante}')")
    print()
    
    # Executando o exemplo
    nome = 'João Silva'
    idade = 25
    altura = 1.80
    eh_estudante = True
    
    print("RESULTADO:")
    print(f'Nome: {nome}')
    print(f'Idade: {idade} anos')
    print(f'Altura: {altura}m')
    print(f'É estudante: {eh_estudante}')
    print()

def resumo_tipos():
    """
    Resumo visual de todos os tipos de dados aprendidos.
    """
    print("=== RESUMO DOS TIPOS DE DADOS ===")
    print()
    
    print("┌─────────────┬─────────────────┬─────────────────────┬─────────────────┐")
    print("│    TIPO     │    EXEMPLO      │      DESCRIÇÃO      │   CONVERSÃO     │")
    print("├─────────────┼─────────────────┼─────────────────────┼─────────────────┤")
    print("│ int         │ 42, -10, 0      │ Números inteiros    │ int(valor)      │")
    print("│ float       │ 3.14, -2.5      │ Números decimais    │ float(valor)    │")
    print("│ str         │ 'texto', \"abc\"   │ Texto/caracteres    │ str(valor)      │")
    print("│ bool        │ True, False     │ Verdadeiro/Falso    │ bool(valor)     │")
    print("│ NoneType    │ None            │ Ausência de valor   │ Não aplicável   │")
    print("└─────────────┴─────────────────┴─────────────────────┴─────────────────┘")
    print()
    
    print("DICAS IMPORTANTES:")
    print("✅ Use type(variavel) para descobrir o tipo")
    print("✅ Python é dinamicamente tipado (tipo pode mudar)")
    print("✅ Sempre valide conversões para evitar erros")
    print("✅ Use nomes descritivos para suas variáveis")
    print("✅ None é diferente de 0, False ou string vazia")
    print()

if __name__ == "__main__":
    # Demonstração completa do módulo
    print("🐍 CURSO DE PYTHON - MÓDULO 1.2: TIPOS DE DADOS E VARIÁVEIS 🐍")
    print("=" * 70)
    print()
    
    # Execução sequencial de todos os conceitos
    conceito_variaveis()
    print("-" * 50)
    
    tipos_numericos()
    print("-" * 50)
    
    tipo_string()
    print("-" * 50)
    
    tipo_boolean()
    print("-" * 50)
    
    conversao_tipos()
    print("-" * 50)
    
    tipo_none()
    print("-" * 50)
    
    exemplos_praticos()
    print("-" * 50)
    
    resumo_tipos()
    print("-" * 50)
    
    exercicios()
    
    print("=" * 70)
    print("🎉 PARABÉNS! Você dominou os Tipos de Dados e Variáveis!")
    print("Próximo módulo: Operadores e Expressões")
    print("=" * 70)