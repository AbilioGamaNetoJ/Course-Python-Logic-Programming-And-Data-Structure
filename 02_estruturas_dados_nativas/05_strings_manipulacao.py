"""
Módulo: Strings e Manipulação de Texto
Tópico: Estruturas de Dados Nativas
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico a Intermediário

Objetivos de Aprendizado:
- Compreender strings como sequências imutáveis de caracteres
- Dominar métodos de manipulação de strings
- Implementar formatação avançada de strings
- Trabalhar com expressões regulares básicas
- Aplicar técnicas de processamento de texto
- Entender encoding e unicode
- Resolver problemas práticos com strings
- Analisar performance de operações com strings

Conceitos Abordados:
- Definição e características de strings
- Criação e sintaxe de strings
- Indexação e slicing
- Métodos de strings (busca, modificação, validação)
- Formatação (%, .format(), f-strings)
- Expressões regulares (re)
- Encoding e Unicode
- Processamento de texto

Pré-requisitos:
- Módulos 2.1 a 2.4 completos
- Conhecimento de iteração
- Compreensão de sequências

Complexidade Temporal:
- Acesso por índice: O(1)
- Busca: O(n)
- Concatenação: O(n)
- Slicing: O(k) onde k é o tamanho do slice

Complexidade Espacial: O(n) onde n é o comprimento da string
"""

import re
import time
import unicodedata

def conceito_strings():
    """
    Introduz o conceito fundamental de strings.
    
    Analogia: Strings são como sequências de caracteres em uma linha,
    similar a palavras escritas em papel onde cada letra tem uma posição fixa.
    """
    print("=== CONCEITO DE STRINGS ===")
    print()
    
    print("1. O QUE SÃO STRINGS?")
    print("   → Sequências imutáveis de caracteres Unicode")
    print("   → Ordenadas e indexáveis")
    print("   → Suportam slicing e iteração")
    print("   → Imutáveis - operações criam novas strings")
    print("   → Hashable - podem ser chaves de dicionário")
    print("   → Implementadas como arrays de caracteres")
    print()
    
    print("2. ANALOGIAS DO COTIDIANO:")
    print("   📝 Texto escrito em papel")
    print("   🔤 Sequência de letras em um livro")
    print("   📱 Mensagem de texto no celular")
    print("   🏷️  Etiqueta com nome")
    print("   📋 Linha de código no editor")
    print("   🎵 Letra de música")
    print("   📧 Endereço de email")
    print()
    
    print("3. VISUALIZAÇÃO ASCII DE UMA STRING:")
    exemplo_str = "Python"
    print(f"   String: '{exemplo_str}'")
    print()
    print("   ┌─────┬─────┬─────┬─────┬─────┬─────┐")
    print("   │  P  │  y  │  t  │  h  │  o  │  n  │")
    print("   └─────┴─────┴─────┴─────┴─────┴─────┘")
    print("     0     1     2     3     4     5    ← Índices positivos")
    print("    -6    -5    -4    -3    -2    -1    ← Índices negativos")
    print()
    
    print("4. CARACTERÍSTICAS IMPORTANTES:")
    print("   ┌─────────────────┬─────────────────────────────────────┐")
    print("   │ CARACTERÍSTICA  │              DESCRIÇÃO              │")
    print("   ├─────────────────┼─────────────────────────────────────┤")
    print("   │ Imutabilidade   │ Não podem ser modificadas in-place  │")
    print("   │ Indexação       │ Acesso por índice [0], [-1]         │")
    print("   │ Slicing         │ Fatias [início:fim:passo]           │")
    print("   │ Iteração        │ for char in string                  │")
    print("   │ Concatenação    │ + e += criam novas strings          │")
    print("   │ Comparação      │ Lexicográfica (ordem alfabética)    │")
    print("   │ Unicode         │ Suporte completo a caracteres UTF-8 │")
    print("   └─────────────────┴─────────────────────────────────────┘")
    print()
    
    print("5. EXEMPLO DE IMUTABILIDADE:")
    texto = "Python"
    print(f"   texto = '{texto}'")
    print(f"   id(texto) = {id(texto)}")
    print()
    
    print("   # Tentativa de 'modificação'")
    print("   texto += ' é incrível'")
    texto += " é incrível"
    print(f"   → Novo texto: '{texto}'")
    print(f"   → Novo id: {id(texto)}")
    print("   → Nova string foi criada!")
    print()
    
    print("6. TIPOS DE STRINGS:")
    print("   # String normal")
    print("   normal = 'Texto normal'")
    normal = 'Texto normal'
    
    print("   # Raw string (r-string)")
    print("   raw = r'C:\\Users\\nome\\arquivo.txt'")
    raw = r'C:\Users\nome\arquivo.txt'
    
    print("   # Byte string")
    print("   byte_str = b'Texto em bytes'")
    byte_str = b'Texto em bytes'
    
    print("   # Unicode string (padrão no Python 3)")
    print("   unicode_str = 'Olá, mundo! 🌍'")
    unicode_str = 'Olá, mundo! 🌍'
    
    print()
    print("   RESULTADO:")
    print(f"   → Normal: {normal} (tipo: {type(normal)})")
    print(f"   → Raw: {raw} (tipo: {type(raw)})")
    print(f"   → Bytes: {byte_str} (tipo: {type(byte_str)})")
    print(f"   → Unicode: {unicode_str} (tipo: {type(unicode_str)})")
    print()
    
    print("7. OPERAÇÕES BÁSICAS:")
    s1 = "Hello"
    s2 = "World"
    
    print(f"   s1 = '{s1}'")
    print(f"   s2 = '{s2}'")
    print()
    
    print("   # Concatenação")
    print(f"   s1 + ' ' + s2 = '{s1 + ' ' + s2}'")
    
    print("   # Repetição")
    print(f"   s1 * 3 = '{s1 * 3}'")
    
    print("   # Comprimento")
    print(f"   len(s1) = {len(s1)}")
    
    print("   # Pertencimento")
    print(f"   'ell' in s1 = {'ell' in s1}")
    
    print("   # Comparação")
    print(f"   s1 < s2 = {s1 < s2} (ordem lexicográfica)")
    print()

def criacao_indexacao():
    """
    Explora criação de strings e operações de indexação.
    
    Analogia: Indexação é como numerar as posições em uma fila,
    onde cada pessoa (caractere) tem um número específico.
    """
    print("=== CRIAÇÃO E INDEXAÇÃO DE STRINGS ===")
    print()
    
    print("1. FORMAS DE CRIAR STRINGS:")
    print("   # Aspas simples")
    print("   texto1 = 'Python é incrível'")
    texto1 = 'Python é incrível'
    
    print("   # Aspas duplas")
    print("   texto2 = \"Python é incrível\"")
    texto2 = "Python é incrível"
    
    print("   # Aspas triplas (multilinhas)")
    print("   texto3 = '''")
    print("   Texto com")
    print("   múltiplas linhas")
    print("   '''")
    texto3 = '''Texto com
múltiplas linhas'''
    
    print("   # Construtor str()")
    print("   texto4 = str(12345)")
    texto4 = str(12345)
    
    print()
    print("   RESULTADO:")
    print(f"   → texto1: '{texto1}'")
    print(f"   → texto2: '{texto2}'")
    print(f"   → texto3: '{repr(texto3)}'")
    print(f"   → texto4: '{texto4}' (tipo: {type(texto4)})")
    print()
    
    print("2. CARACTERES ESPECIAIS:")
    print("   # Escape sequences")
    especiais = "Linha 1\\nLinha 2\\tTabulação\\\"Aspas\\\\"
    print(f"   especiais = 'Linha 1\\\\nLinha 2\\\\tTabulação\\\\\"Aspas\\\\\\\\'")
    print("   RESULTADO:")
    print(f"   → {repr(especiais)}")
    print("   → Interpretado:")
    print(especiais)
    print()
    
    print("3. INDEXAÇÃO BÁSICA:")
    palavra = "Python"
    print(f"   palavra = '{palavra}'")
    print()
    
    print("   # Índices positivos")
    for i in range(len(palavra)):
        print(f"   palavra[{i}] = '{palavra[i]}'")
    print()
    
    print("   # Índices negativos")
    for i in range(-len(palavra), 0):
        print(f"   palavra[{i}] = '{palavra[i]}'")
    print()
    
    print("4. SLICING (FATIAMENTO):")
    texto = "Programação Python"
    print(f"   texto = '{texto}'")
    print()
    
    print("   # Sintaxe: [início:fim:passo]")
    print(f"   texto[0:11] = '{texto[0:11]}'")
    print(f"   texto[12:] = '{texto[12:]}'")
    print(f"   texto[:11] = '{texto[:11]}'")
    print(f"   texto[::2] = '{texto[::2]}'")
    print(f"   texto[::-1] = '{texto[::-1]}'")
    print()
    
    print("5. SLICING AVANÇADO:")
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(f"   alfabeto = '{alfabeto}'")
    print()
    
    print("   # Exemplos práticos")
    print(f"   → Primeiras 5 letras: '{alfabeto[:5]}'")
    print(f"   → Últimas 5 letras: '{alfabeto[-5:]}'")
    print(f"   → Do meio (10-15): '{alfabeto[10:15]}'")
    print(f"   → Letras pares: '{alfabeto[::2]}'")
    print(f"   → Letras ímpares: '{alfabeto[1::2]}'")
    print(f"   → Reverso: '{alfabeto[::-1]}'")
    print(f"   → Cada 3ª letra: '{alfabeto[::3]}'")
    print()
    
    print("6. ITERAÇÃO SOBRE STRINGS:")
    nome = "Ana"
    print(f"   nome = '{nome}'")
    print()
    
    print("   # Iteração simples")
    print("   for char in nome:")
    print("       print(f'Caractere: {char}')")
    print("   RESULTADO:")
    for char in nome:
        print(f"   → Caractere: {char}")
    print()
    
    print("   # Iteração com índice")
    print("   for i, char in enumerate(nome):")
    print("       print(f'Posição {i}: {char}')")
    print("   RESULTADO:")
    for i, char in enumerate(nome):
        print(f"   → Posição {i}: {char}")
    print()
    
    print("7. VERIFICAÇÃO DE LIMITES:")
    teste = "Teste"
    print(f"   teste = '{teste}' (comprimento: {len(teste)})")
    print()
    
    print("   # Índices válidos")
    print(f"   teste[0] = '{teste[0]}'  # ✅ Válido")
    print(f"   teste[-1] = '{teste[-1]}'  # ✅ Válido")
    
    print("   # Índices inválidos causariam IndexError")
    print("   # teste[10]  # ❌ IndexError")
    print("   # teste[-10] # ❌ IndexError")
    print()
    
    print("   # Slicing é mais tolerante")
    print(f"   teste[10:20] = '{teste[10:20]}'  # ✅ Retorna string vazia")
    print(f"   teste[-10:2] = '{teste[-10:2]}'  # ✅ Ajusta automaticamente")
    print()

def metodos_strings():
    """
    Explora os métodos principais para manipulação de strings.
    
    Analogia: Métodos de strings são como ferramentas especializadas
    para diferentes tipos de edição e análise de texto.
    """
    print("=== MÉTODOS DE STRINGS ===")
    print()
    
    texto_exemplo = "  Python é uma Linguagem Incrível  "
    print(f"   texto = '{texto_exemplo}'")
    print()
    
    print("1. MÉTODOS DE LIMPEZA:")
    print("   # strip() - remove espaços das extremidades")
    print(f"   texto.strip() = '{texto_exemplo.strip()}'")
    
    print("   # lstrip() - remove espaços da esquerda")
    print(f"   texto.lstrip() = '{texto_exemplo.lstrip()}'")
    
    print("   # rstrip() - remove espaços da direita")
    print(f"   texto.rstrip() = '{texto_exemplo.rstrip()}'")
    print()
    
    print("2. MÉTODOS DE TRANSFORMAÇÃO:")
    palavra = "Python Programming"
    print(f"   palavra = '{palavra}'")
    print()
    
    print(f"   → lower(): '{palavra.lower()}'")
    print(f"   → upper(): '{palavra.upper()}'")
    print(f"   → title(): '{palavra.title()}'")
    print(f"   → capitalize(): '{palavra.capitalize()}'")
    print(f"   → swapcase(): '{palavra.swapcase()}'")
    print()
    
    print("3. MÉTODOS DE BUSCA:")
    frase = "Python é uma linguagem Python"
    print(f"   frase = '{frase}'")
    print()
    
    print(f"   → find('Python'): {frase.find('Python')}")
    print(f"   → find('Java'): {frase.find('Java')}")
    print(f"   → rfind('Python'): {frase.rfind('Python')}")
    print(f"   → index('uma'): {frase.index('uma')}")
    print(f"   → count('Python'): {frase.count('Python')}")
    print()
    
    print("4. MÉTODOS DE VERIFICAÇÃO:")
    exemplos = ['Python123', 'python', 'PYTHON', '12345', 'Hello World']
    
    print("   Testando diferentes strings:")
    for exemplo in exemplos:
        print(f"   '{exemplo}':")
        print(f"     → isalpha(): {exemplo.isalpha()}")
        print(f"     → isdigit(): {exemplo.isdigit()}")
        print(f"     → isalnum(): {exemplo.isalnum()}")
        print(f"     → islower(): {exemplo.islower()}")
        print(f"     → isupper(): {exemplo.isupper()}")
        print(f"     → isspace(): {exemplo.isspace()}")
        print()
    
    print("5. MÉTODOS DE DIVISÃO E JUNÇÃO:")
    texto_csv = "nome,idade,cidade,profissao"
    print(f"   texto_csv = '{texto_csv}'")
    
    print("   # split() - divide string")
    campos = texto_csv.split(',')
    print(f"   → split(','): {campos}")
    
    print("   # join() - junta lista em string")
    print("   ' | '.join(campos)")
    resultado_join = ' | '.join(campos)
    print(f"   → Resultado: '{resultado_join}'")
    print()
    
    print("   # splitlines() - divide por linhas")
    texto_linhas = "Linha 1\nLinha 2\nLinha 3"
    print(f"   texto_linhas = {repr(texto_linhas)}")
    linhas = texto_linhas.splitlines()
    print(f"   → splitlines(): {linhas}")
    print()
    
    print("6. MÉTODOS DE SUBSTITUIÇÃO:")
    texto_original = "Java é bom, mas Python é melhor que Java"
    print(f"   texto = '{texto_original}'")
    print()
    
    print("   # replace() - substitui todas as ocorrências")
    print("   texto.replace('Java', 'JavaScript')")
    substituido = texto_original.replace('Java', 'JavaScript')
    print(f"   → '{substituido}'")
    
    print("   # replace() com limite")
    print("   texto.replace('Java', 'C++', 1)")
    substituido_limitado = texto_original.replace('Java', 'C++', 1)
    print(f"   → '{substituido_limitado}'")
    print()
    
    print("7. MÉTODOS DE ALINHAMENTO:")
    nome = "Python"
    print(f"   nome = '{nome}'")
    print()
    
    print(f"   → center(20): '{nome.center(20)}'")
    print(f"   → center(20, '*'): '{nome.center(20, '*')}'")
    print(f"   → ljust(15): '{nome.ljust(15)}'")
    print(f"   → rjust(15): '{nome.rjust(15)}'")
    print(f"   → zfill(10): '{nome.zfill(10)}'")
    print()
    
    print("8. MÉTODOS AVANÇADOS:")
    
    print("   # startswith() e endswith()")
    arquivo = "documento.pdf"
    print(f"   arquivo = '{arquivo}'")
    print(f"   → startswith('doc'): {arquivo.startswith('doc')}")
    print(f"   → endswith('.pdf'): {arquivo.endswith('.pdf')}")
    print()
    
    print("   # partition() - divide em 3 partes")
    email = "usuario@dominio.com"
    print(f"   email = '{email}'")
    partes = email.partition('@')
    print(f"   → partition('@'): {partes}")
    print()
    
    print("   # expandtabs() - expande tabs")
    texto_tab = "Nome:\tIdade:\tCidade:"
    print(f"   texto_tab = {repr(texto_tab)}")
    print(f"   → expandtabs(4): '{texto_tab.expandtabs(4)}'")
    print()

def formatacao_strings():
    """
    Explora técnicas de formatação de strings.
    
    Analogia: Formatação é como usar moldes ou templates
    para criar textos padronizados com dados variáveis.
    """
    print("=== FORMATAÇÃO DE STRINGS ===")
    print()
    
    nome = "Ana"
    idade = 25
    salario = 5500.75
    
    print(f"   Dados: nome='{nome}', idade={idade}, salario={salario}")
    print()
    
    print("1. FORMATAÇÃO COM % (ESTILO ANTIGO):")
    print("   # Especificadores básicos")
    print("   'Nome: %s, Idade: %d' % (nome, idade)")
    resultado_percent = 'Nome: %s, Idade: %d' % (nome, idade)
    print(f"   → '{resultado_percent}'")
    
    print("   # Com formatação numérica")
    print("   'Salário: R$ %.2f' % salario")
    resultado_salario = 'Salário: R$ %.2f' % salario
    print(f"   → '{resultado_salario}'")
    print()
    
    print("2. MÉTODO .format():")
    print("   # Posicional")
    print("   'Nome: {}, Idade: {}'.format(nome, idade)")
    resultado_format1 = 'Nome: {}, Idade: {}'.format(nome, idade)
    print(f"   → '{resultado_format1}'")
    
    print("   # Com índices")
    print("   '{1} tem {0} anos'.format(idade, nome)")
    resultado_format2 = '{1} tem {0} anos'.format(idade, nome)
    print(f"   → '{resultado_format2}'")
    
    print("   # Com nomes")
    print("   '{nome} ganha R$ {salario:.2f}'.format(nome=nome, salario=salario)")
    resultado_format3 = '{nome} ganha R$ {salario:.2f}'.format(nome=nome, salario=salario)
    print(f"   → '{resultado_format3}'")
    print()
    
    print("3. F-STRINGS (PYTHON 3.6+) - RECOMENDADO:")
    print("   # Sintaxe simples")
    print("   f'Nome: {nome}, Idade: {idade}'")
    resultado_f1 = f'Nome: {nome}, Idade: {idade}'
    print(f"   → '{resultado_f1}'")
    
    print("   # Com expressões")
    print("   f'{nome} nasceu em {2024 - idade}'")
    resultado_f2 = f'{nome} nasceu em {2024 - idade}'
    print(f"   → '{resultado_f2}'")
    
    print("   # Com formatação")
    print("   f'Salário: R$ {salario:,.2f}'")
    resultado_f3 = f'Salário: R$ {salario:,.2f}'
    print(f"   → '{resultado_f3}'")
    print()
    
    print("4. FORMATAÇÃO NUMÉRICA AVANÇADA:")
    numero = 1234567.89
    print(f"   numero = {numero}")
    print()
    
    print("   # Diferentes formatos")
    print(f"   → Padrão: {numero}")
    print(f"   → 2 decimais: {numero:.2f}")
    print(f"   → Separador de milhares: {numero:,.2f}")
    print(f"   → Notação científica: {numero:.2e}")
    print(f"   → Percentual: {0.1234:.2%}")
    print(f"   → Preenchimento: {numero:015.2f}")
    print()
    
    print("5. FORMATAÇÃO DE DATAS:")
    from datetime import datetime
    
    agora = datetime.now()
    print(f"   agora = {agora}")
    print()
    
    print("   # Diferentes formatos de data")
    print(f"   → ISO: {agora:%Y-%m-%d}")
    print(f"   → Brasileiro: {agora:%d/%m/%Y}")
    print(f"   → Completo: {agora:%A, %d de %B de %Y}")
    print(f"   → Hora: {agora:%H:%M:%S}")
    print()
    
    print("6. ALINHAMENTO E PREENCHIMENTO:")
    texto = "Python"
    print(f"   texto = '{texto}'")
    print()
    
    print("   # Alinhamento com f-strings")
    print(f"   → Esquerda (20): '{texto:<20}'")
    print(f"   → Centro (20): '{texto:^20}'")
    print(f"   → Direita (20): '{texto:>20}'")
    print(f"   → Preenchido: '{texto:*^20}'")
    print()
    
    print("7. FORMATAÇÃO CONDICIONAL:")
    usuarios = [
        {'nome': 'Ana', 'ativo': True, 'pontos': 1250},
        {'nome': 'Bruno', 'ativo': False, 'pontos': 890},
        {'nome': 'Carlos', 'ativo': True, 'pontos': 2100}
    ]
    
    print("   # Formatação baseada em condições")
    for usuario in usuarios:
        status = "🟢 ATIVO" if usuario['ativo'] else "🔴 INATIVO"
        nivel = "⭐ VIP" if usuario['pontos'] > 1000 else "👤 NORMAL"
        
        print(f"   → {usuario['nome']:.<15} {status} {nivel} ({usuario['pontos']} pts)")
    print()
    
    print("8. TEMPLATE STRINGS (MÓDULO string):")
    from string import Template
    
    template = Template("Olá $nome, você tem $idade anos e mora em $cidade")
    print("   template = Template('Olá $nome, você tem $idade anos e mora em $cidade')")
    
    dados = {'nome': 'Maria', 'idade': 30, 'cidade': 'São Paulo'}
    resultado_template = template.substitute(dados)
    print(f"   → {resultado_template}")
    
    # Safe substitute
    dados_incompletos = {'nome': 'João', 'idade': 25}
    resultado_safe = template.safe_substitute(dados_incompletos)
    print(f"   → Safe substitute: {resultado_safe}")
    print()

def expressoes_regulares():
    """
    Introduz expressões regulares para processamento avançado de texto.
    
    Analogia: Regex é como um detector de padrões muito sofisticado,
    capaz de encontrar e extrair informações específicas em textos.
    """
    print("=== EXPRESSÕES REGULARES (REGEX) ===")
    print()
    
    print("1. CONCEITOS BÁSICOS:")
    print("   → Padrões para busca e manipulação de texto")
    print("   → Linguagem específica para descrição de padrões")
    print("   → Muito poderosas, mas podem ser complexas")
    print("   → Módulo 're' do Python")
    print()
    
    print("2. METACARACTERES BÁSICOS:")
    print("   ┌─────────┬─────────────────────────────────────┐")
    print("   │ SÍMBOLO │              SIGNIFICADO            │")
    print("   ├─────────┼─────────────────────────────────────┤")
    print("   │    .    │ Qualquer caractere (exceto \\n)      │")
    print("   │    ^    │ Início da string                    │")
    print("   │    $    │ Final da string                     │")
    print("   │    *    │ 0 ou mais repetições                │")
    print("   │    +    │ 1 ou mais repetições                │")
    print("   │    ?    │ 0 ou 1 repetição                    │")
    print("   │   \\d    │ Dígito [0-9]                        │")
    print("   │   \\w    │ Caractere de palavra [a-zA-Z0-9_]   │")
    print("   │   \\s    │ Espaço em branco                    │")
    print("   └─────────┴─────────────────────────────────────┘")
    print()
    
    print("3. BUSCA SIMPLES:")
    texto = "Python é uma linguagem de programação Python"
    print(f"   texto = '{texto}'")
    print()
    
    print("   # re.search() - primeira ocorrência")
    match = re.search(r'Python', texto)
    if match:
        print(f"   → Encontrado: '{match.group()}' na posição {match.start()}")
    
    print("   # re.findall() - todas as ocorrências")
    todas = re.findall(r'Python', texto)
    print(f"   → Todas: {todas}")
    
    print("   # re.finditer() - com posições")
    print("   → Posições:")
    for match in re.finditer(r'Python', texto):
        print(f"     '{match.group()}' em {match.start()}-{match.end()}")
    print()
    
    print("4. PADRÕES COM METACARACTERES:")
    
    # Validação de email simples
    emails = ['user@domain.com', 'invalid.email', 'test@test.org', 'bad@']
    padrao_email = r'\w+@\w+\.\w+'
    
    print(f"   Padrão email: {padrao_email}")
    print("   Testando emails:")
    for email in emails:
        if re.match(padrao_email, email):
            print(f"   → '{email}': ✅ Válido")
        else:
            print(f"   → '{email}': ❌ Inválido")
    print()
    
    print("5. GRUPOS E CAPTURA:")
    texto_data = "Hoje é 15/03/2024 e ontem foi 14/03/2024"
    padrao_data = r'(\d{2})/(\d{2})/(\d{4})'
    
    print(f"   texto = '{texto_data}'")
    print(f"   padrão = '{padrao_data}'")
    print()
    
    print("   # Extraindo datas com grupos")
    for match in re.finditer(padrao_data, texto_data):
        dia, mes, ano = match.groups()
        print(f"   → Data: {match.group()} - Dia: {dia}, Mês: {mes}, Ano: {ano}")
    print()
    
    print("6. SUBSTITUIÇÃO COM REGEX:")
    texto_telefone = "Contatos: (11) 99999-9999 e (21) 88888-8888"
    print(f"   texto = '{texto_telefone}'")
    
    # Mascarar telefones
    padrao_tel = r'\((\d{2})\) (\d{5})-(\d{4})'
    substituicao = r'(\1) *****-\3'
    
    texto_mascarado = re.sub(padrao_tel, substituicao, texto_telefone)
    print(f"   → Mascarado: '{texto_mascarado}'")
    print()
    
    print("7. VALIDAÇÕES PRÁTICAS:")
    
    def validar_cpf(cpf):
        """Valida formato de CPF"""
        padrao = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
        return bool(re.match(padrao, cpf))
    
    def validar_telefone(telefone):
        """Valida formato de telefone brasileiro"""
        padrao = r'^\(\d{2}\) \d{4,5}-\d{4}$'
        return bool(re.match(padrao, telefone))
    
    def extrair_urls(texto):
        """Extrai URLs de um texto"""
        padrao = r'https?://[^\s]+'
        return re.findall(padrao, texto)
    
    # Testando validações
    cpfs = ['123.456.789-00', '12345678900', '123.456.789-0']
    telefones = ['(11) 99999-9999', '11999999999', '(11) 9999-9999']
    
    print("   Validando CPFs:")
    for cpf in cpfs:
        resultado = "✅" if validar_cpf(cpf) else "❌"
        print(f"   → '{cpf}': {resultado}")
    
    print("\n   Validando telefones:")
    for tel in telefones:
        resultado = "✅" if validar_telefone(tel) else "❌"
        print(f"   → '{tel}': {resultado}")
    
    print("\n   Extraindo URLs:")
    texto_urls = "Visite https://python.org e http://github.com para mais info"
    urls = extrair_urls(texto_urls)
    print(f"   → URLs encontradas: {urls}")
    print()

def processamento_texto():
    """
    Demonstra técnicas avançadas de processamento de texto.
    """
    print("=== PROCESSAMENTO AVANÇADO DE TEXTO ===")
    print()
    
    print("Caso 1: Analisador de Texto")
    
    def analisar_texto(texto):
        """Análise completa de um texto"""
        
        # Estatísticas básicas
        stats = {
            'caracteres': len(texto),
            'caracteres_sem_espacos': len(texto.replace(' ', '')),
            'palavras': len(texto.split()),
            'linhas': len(texto.splitlines()),
            'paragrafos': len([p for p in texto.split('\n\n') if p.strip()])
        }
        
        # Análise de palavras
        palavras = re.findall(r'\b\w+\b', texto.lower())
        from collections import Counter
        contador_palavras = Counter(palavras)
        
        # Análise de caracteres
        chars = [c for c in texto.lower() if c.isalpha()]
        contador_chars = Counter(chars)
        
        return {
            'estatisticas': stats,
            'palavras_mais_comuns': contador_palavras.most_common(5),
            'chars_mais_comuns': contador_chars.most_common(5),
            'palavra_mais_longa': max(palavras, key=len) if palavras else '',
            'media_palavras_por_linha': stats['palavras'] / max(stats['linhas'], 1)
        }
    
    # Texto de exemplo
    texto_exemplo = """
    Python é uma linguagem de programação de alto nível.
    É conhecida por sua sintaxe clara e legível.
    
    Python é amplamente usada em ciência de dados,
    desenvolvimento web e automação.
    """
    
    print("   ANÁLISE DE TEXTO:")
    print(f"   Texto: {repr(texto_exemplo[:50])}...")
    
    analise = analisar_texto(texto_exemplo)
    
    print("\n   ESTATÍSTICAS:")
    for chave, valor in analise['estatisticas'].items():
        print(f"   → {chave.replace('_', ' ').title()}: {valor}")
    
    print(f"\n   → Palavras mais comuns: {analise['palavras_mais_comuns']}")
    print(f"   → Palavra mais longa: '{analise['palavra_mais_longa']}'")
    print(f"   → Média palavras/linha: {analise['media_palavras_por_linha']:.1f}")
    print()
    
    print("Caso 2: Limpeza e Normalização")
    
    def limpar_texto(texto):
        """Limpa e normaliza texto para processamento"""
        
        # Remove caracteres especiais, mantém apenas letras, números e espaços
        texto_limpo = re.sub(r'[^\w\s]', '', texto)
        
        # Normaliza espaços
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo)
        
        # Remove espaços das extremidades
        texto_limpo = texto_limpo.strip()
        
        # Converte para minúsculas
        texto_limpo = texto_limpo.lower()
        
        return texto_limpo
    
    texto_sujo = "  Olá!!! Como você está??? Tudo bem... 😊  "
    print(f"   Texto original: '{texto_sujo}'")
    texto_limpo = limpar_texto(texto_sujo)
    print(f"   → Texto limpo: '{texto_limpo}'")
    print()
    
    print("Caso 3: Extrator de Informações")
    
    def extrair_informacoes(texto):
        """Extrai diferentes tipos de informação de um texto"""
        
        # Padrões para diferentes tipos de dados
        padroes = {
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'telefones': r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}',
            'cpfs': r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}',
            'ceps': r'\d{5}-?\d{3}',
            'urls': r'https?://[^\s]+',
            'datas': r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            'valores': r'R\$\s?\d+(?:,\d{2})?'
        }
        
        resultados = {}
        for tipo, padrao in padroes.items():
            matches = re.findall(padrao, texto)
            if matches:
                resultados[tipo] = matches
        
        return resultados
    
    texto_info = """
    Contato: João Silva
    Email: joao@empresa.com
    Telefone: (11) 99999-9999
    CPF: 123.456.789-00
    Endereço: Rua das Flores, 123 - CEP: 01234-567
    Site: https://empresa.com
    Nascimento: 15/03/1990
    Salário: R$ 5.500,00
    """
    
    print("   EXTRAÇÃO DE INFORMAÇÕES:")
    print("   Texto com dados pessoais...")
    
    informacoes = extrair_informacoes(texto_info)
    for tipo, dados in informacoes.items():
        print(f"   → {tipo.title()}: {dados}")
    print()

if __name__ == "__main__":
    print("MÓDULO 2.5 - STRINGS E MANIPULAÇÃO DE TEXTO")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceito_strings()
    print("\n" + "="*50 + "\n")
    
    criacao_indexacao()
    print("\n" + "="*50 + "\n")
    
    metodos_strings()
    print("\n" + "="*50 + "\n")
    
    formatacao_strings()
    print("\n" + "="*50 + "\n")
    
    expressoes_regulares()
    print("\n" + "="*50 + "\n")
    
    processamento_texto()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 2.5 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceito e características de strings")
    print("✅ Criação e indexação de strings")
    print("✅ Métodos de manipulação de strings")
    print("✅ Formatação avançada (%, .format(), f-strings)")
    print("✅ Expressões regulares básicas")
    print("✅ Processamento avançado de texto")
    print("\n➡️  Próximo: Módulo 2.6 - Compreensão de Listas e Geradores")