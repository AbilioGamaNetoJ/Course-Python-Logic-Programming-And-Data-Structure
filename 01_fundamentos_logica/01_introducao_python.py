"""
Módulo: Introdução ao Python
Tópico: Fundamentos de Lógica de Programação
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico

Objetivos de Aprendizado:
- Compreender o que é Python e suas características
- Entender como o interpretador Python funciona
- Conhecer a sintaxe básica e filosofia da linguagem
- Executar seus primeiros programas Python
- Compreender conceitos de entrada e saída de dados

Conceitos Abordados:
- História e filosofia do Python
- Interpretador vs Compilador
- Sintaxe básica e indentação
- Comentários e documentação
- Função print() e input()
- Execução de programas Python

Pré-requisitos:
- Conhecimento básico de computação
- Python instalado no sistema
"""

def introducao_python():
    """
    Introdução ao Python: A linguagem que fala como você pensa.
    
    Python é uma linguagem de programação criada por Guido van Rossum em 1991.
    Seu nome vem do grupo de comédia britânico "Monty Python".
    
    Analogia: Se linguagens de programação fossem idiomas humanos, Python seria
    como o português - claro, direto e fácil de entender.
    
    Características principais:
    - Sintaxe simples e legível
    - Interpretada (não precisa compilar)
    - Multiplataforma (Windows, Mac, Linux)
    - Orientada a objetos
    - Grande comunidade e bibliotecas
    
    Returns:
        None: Esta função demonstra conceitos, não retorna valores
    """
    print("=== BEM-VINDO AO PYTHON ===")
    print()
    
    # Passo 1: Demonstrando a simplicidade do Python
    print("1. Python é simples - veja como imprimir texto:")
    print("   print('Olá, mundo!')")
    print("   Resultado:", end=" ")
    print('Olá, mundo!')
    print()
    
    # Passo 2: Mostrando a filosofia Python (Zen of Python)
    print("2. A filosofia do Python (algumas regras do 'Zen of Python'):")
    print("   - Bonito é melhor que feio")
    print("   - Explícito é melhor que implícito") 
    print("   - Simples é melhor que complexo")
    print("   - Legibilidade conta")
    print()
    
    # Passo 3: Demonstrando como Python interpreta código
    print("3. Python é interpretado - executa linha por linha:")
    print("   Linha 1: nome = 'Python'")
    nome = 'Python'
    print("   Linha 2: print(f'Eu estou aprendendo {nome}!')")
    print(f'   Resultado: Eu estou aprendendo {nome}!')
    print()

def como_python_funciona():
    """
    Explica como o interpretador Python funciona internamente.
    
    Analogia: O interpretador Python é como um tradutor simultâneo.
    Ele lê seu código em português (Python) e traduz para linguagem
    de máquina que o computador entende, linha por linha.
    """
    print("=== COMO O PYTHON FUNCIONA ===")
    print()
    
    # Demonstração do processo de interpretação
    print("Processo de execução do Python:")
    print("1. Você escreve código Python (.py)")
    print("2. Interpretador lê linha por linha")
    print("3. Converte para bytecode (código intermediário)")
    print("4. Máquina virtual Python executa o bytecode")
    print("5. Resultado aparece na tela")
    print()
    
    # Exemplo prático
    print("Exemplo prático - vamos ver o Python 'pensando':")
    codigo = "2 + 3 * 4"
    print(f"Código: {codigo}")
    print("Python pensa: 'Primeiro 3 * 4 = 12, depois 2 + 12 = 14'")
    resultado = 2 + 3 * 4
    print(f"Resultado: {resultado}")
    print()

def sintaxe_basica():
    """
    Demonstra os elementos fundamentais da sintaxe Python.
    
    A sintaxe é como a gramática de uma linguagem - são as regras
    que devemos seguir para que o Python nos entenda corretamente.
    """
    print("=== SINTAXE BÁSICA DO PYTHON ===")
    print()
    
    # Passo 1: Indentação (muito importante em Python!)
    print("1. INDENTAÇÃO - A alma do Python:")
    print("   Python usa espaços para organizar o código")
    print("   Exemplo de código bem indentado:")
    print()
    print("   if True:")
    print("       print('Este código está indentado')")
    print("       print('Todas estas linhas estão no mesmo nível')")
    print("   print('Esta linha voltou ao nível original')")
    print()
    
    # Demonstração prática da indentação
    if True:
        print("   → Este código está indentado corretamente!")
        print("   → Python entende que estas linhas estão juntas")
    print("   → Esta linha voltou ao nível original")
    print()
    
    # Passo 2: Comentários
    print("2. COMENTÁRIOS - Suas anotações no código:")
    print("   # Isto é um comentário de linha")
    print('   """')
    print("   Isto é um comentário")
    print("   de múltiplas linhas")
    print('   """')
    print()
    
    # Passo 3: Sensibilidade a maiúsculas/minúsculas
    print("3. CASE SENSITIVE - Python diferencia maiúsculas de minúsculas:")
    nome = "Python"
    Nome = "Java"
    print(f"   nome = '{nome}'")
    print(f"   Nome = '{Nome}'")
    print("   → 'nome' e 'Nome' são variáveis diferentes!")
    print()

def entrada_saida_dados():
    """
    Demonstra como receber dados do usuário e exibir resultados.
    
    Analogia: input() é como fazer uma pergunta e esperar a resposta.
    print() é como falar algo em voz alta para todos ouvirem.
    """
    print("=== ENTRADA E SAÍDA DE DADOS ===")
    print()
    
    # Passo 1: Função print() - nossa forma de "falar"
    print("1. PRINT() - Como o Python 'fala' conosco:")
    print("   print('Texto simples')")
    print("   print(f'Texto com variável: {42}')")
    print("   print('Múltiplos', 'valores', 'separados')")
    print()
    
    # Demonstração de diferentes usos do print
    numero = 42
    print("   Exemplos práticos:")
    print('   → Texto simples')
    print(f'   → Texto com variável: {numero}')
    print('   → Múltiplos', 'valores', 'separados')
    print()
    
    # Passo 2: Função input() - nossa forma de "escutar"
    print("2. INPUT() - Como o Python 'escuta' você:")
    print("   nome = input('Digite seu nome: ')")
    print("   print(f'Olá, {nome}!')")
    print()
    print("   IMPORTANTE: input() sempre retorna texto (string)")
    print("   Para números, precisamos converter:")
    print("   idade = int(input('Digite sua idade: '))")
    print()

def exemplos_praticos():
    """
    Demonstrações práticas dos conceitos aprendidos.
    
    Aqui aplicamos tudo que aprendemos em situações reais,
    como se fossem pequenos programas úteis.
    """
    print("=== EXEMPLOS PRÁTICOS ===")
    print()
    
    # Exemplo 1: Programa simples de saudação
    print("Exemplo 1: Programa de Saudação")
    print("Código:")
    print("   nome = 'Estudante'")
    print("   print(f'Bem-vindo ao curso de Python, {nome}!')")
    print("Resultado:")
    nome = 'Estudante'
    print(f"   Bem-vindo ao curso de Python, {nome}!")
    print()
    
    # Exemplo 2: Calculadora simples
    print("Exemplo 2: Calculadora Básica")
    print("Código:")
    print("   a = 10")
    print("   b = 5")
    print("   soma = a + b")
    print("   print(f'{a} + {b} = {soma}')")
    print("Resultado:")
    a = 10
    b = 5
    soma = a + b
    print(f"   {a} + {b} = {soma}")
    print()
    
    # Exemplo 3: Programa com múltiplas operações
    print("Exemplo 3: Informações do Sistema")
    import sys
    print("Código:")
    print("   import sys")
    print("   print(f'Versão do Python: {sys.version}')")
    print("   print(f'Plataforma: {sys.platform}')")
    print("Resultado:")
    print(f"   Versão do Python: {sys.version.split()[0]}")
    print(f"   Plataforma: {sys.platform}")
    print()

def exercicios():
    """
    Exercícios para fixação do conteúdo.
    
    Nível 1: Exercícios básicos para praticar sintaxe
    Nível 2: Exercícios intermediários combinando conceitos  
    Nível 3: Exercícios avançados aplicando conhecimento
    """
    print("=== EXERCÍCIOS DE FIXAÇÃO ===")
    print()
    
    print("NÍVEL 1 - Básico:")
    print("1. Crie um programa que imprima 'Meu primeiro programa Python!'")
    print("2. Faça um programa que imprima seu nome e idade")
    print("3. Crie variáveis para armazenar seu nome, idade e cidade")
    print("4. Use print() para exibir essas informações formatadas")
    print()
    
    print("NÍVEL 2 - Intermediário:")
    print("5. Crie um programa que calcule e exiba a área de um retângulo")
    print("6. Faça um programa que converta temperatura de Celsius para Fahrenheit")
    print("7. Crie um programa que calcule quantos dias você já viveu")
    print("8. Faça um programa que exiba informações sobre Python usando comentários")
    print()
    
    print("NÍVEL 3 - Avançado:")
    print("9. Crie um programa interativo que peça nome, idade e hobby do usuário")
    print("10. Faça uma calculadora que realize as 4 operações básicas")
    print("11. Crie um programa que simule um diálogo entre você e o computador")
    print("12. Desenvolva um programa que demonstre todos os conceitos aprendidos")
    print()
    
    # Exemplo de solução para exercício nível 1
    print("EXEMPLO DE SOLUÇÃO - Exercício 1:")
    print("print('Meu primeiro programa Python!')")
    print("Resultado:")
    print("Meu primeiro programa Python!")
    print()

def dicas_boas_praticas():
    """
    Dicas importantes para escrever código Python de qualidade.
    
    Estas práticas vão te ajudar desde o início a desenvolver
    um estilo de programação limpo e profissional.
    """
    print("=== DICAS E BOAS PRÁTICAS ===")
    print()
    
    print("1. NOMES DESCRITIVOS:")
    print("   ❌ Ruim: a = 10")
    print("   ✅ Bom:  idade = 10")
    print()
    
    print("2. COMENTÁRIOS ÚTEIS:")
    print("   ❌ Ruim: x = x + 1  # adiciona 1 a x")
    print("   ✅ Bom:  contador = contador + 1  # próximo item da lista")
    print()
    
    print("3. INDENTAÇÃO CONSISTENTE:")
    print("   ✅ Use sempre 4 espaços para indentar")
    print("   ✅ Seja consistente em todo o código")
    print()
    
    print("4. LINHAS NÃO MUITO LONGAS:")
    print("   ✅ Mantenha linhas com até 79 caracteres")
    print("   ✅ Quebre linhas longas de forma elegante")
    print()
    
    print("5. TESTE SEU CÓDIGO:")
    print("   ✅ Execute frequentemente para verificar erros")
    print("   ✅ Teste com diferentes valores")
    print()

if __name__ == "__main__":
    # Demonstração completa do módulo
    print("🐍 CURSO DE PYTHON - MÓDULO 1: INTRODUÇÃO AO PYTHON 🐍")
    print("=" * 60)
    print()
    
    # Execução sequencial de todos os conceitos
    introducao_python()
    print("-" * 40)
    
    como_python_funciona()
    print("-" * 40)
    
    sintaxe_basica()
    print("-" * 40)
    
    entrada_saida_dados()
    print("-" * 40)
    
    exemplos_praticos()
    print("-" * 40)
    
    dicas_boas_praticas()
    print("-" * 40)
    
    exercicios()
    
    print("=" * 60)
    print("🎉 PARABÉNS! Você completou a Introdução ao Python!")
    print("Próximo módulo: Tipos de Dados e Variáveis")
    print("=" * 60)