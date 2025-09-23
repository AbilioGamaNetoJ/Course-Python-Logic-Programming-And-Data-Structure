"""
Módulo: Tuplas e Imutabilidade
Tópico: Estruturas de Dados Nativas
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico a Intermediário

Objetivos de Aprendizado:
- Compreender tuplas como estruturas imutáveis
- Dominar criação, acesso e operações com tuplas
- Entender quando usar tuplas vs listas
- Implementar unpacking e packing de tuplas
- Trabalhar com tuplas nomeadas (namedtuple)
- Analisar performance de tuplas vs listas
- Aplicar tuplas em casos práticos

Conceitos Abordados:
- Definição e características de tuplas
- Criação e sintaxe de tuplas
- Imutabilidade e suas implicações
- Indexação e fatiamento
- Métodos disponíveis (count, index)
- Unpacking e packing
- Tuplas aninhadas
- Named tuples
- Comparação com listas
- Casos de uso práticos

Pré-requisitos:
- Módulo 2.1 completo (Listas)
- Conhecimento de indexação
- Compreensão de mutabilidade vs imutabilidade

Complexidade Temporal:
- Acesso: O(1)
- Busca: O(n)
- Criação: O(n)

Complexidade Espacial: O(n) onde n é o número de elementos
"""

import time
import sys
from collections import namedtuple

def conceito_tuplas():
    """
    Introduz o conceito fundamental de tuplas.
    
    Analogia: Tuplas são como cápsulas do tempo seladas.
    Uma vez criadas, não podem ser modificadas, garantindo
    que os dados permaneçam íntegros e seguros.
    """
    print("=== CONCEITO DE TUPLAS ===")
    print()
    
    print("1. O QUE SÃO TUPLAS?")
    print("   → Estruturas de dados ordenadas e IMUTÁVEIS")
    print("   → Podem conter elementos de diferentes tipos")
    print("   → Indexadas a partir de 0 (como listas)")
    print("   → Tamanho fixo após criação")
    print("   → Mais eficientes em memória que listas")
    print("   → Podem ser usadas como chaves de dicionário")
    print()
    
    print("2. ANALOGIAS DO COTIDIANO:")
    print("   🏛️  Documento histórico selado")
    print("   📦 Pacote lacrado nos correios")
    print("   🧬 DNA - sequência imutável")
    print("   📍 Coordenadas geográficas (lat, lon)")
    print("   🎫 Bilhete de cinema (data, hora, assento)")
    print("   📋 Registro oficial (CPF, nome, data nascimento)")
    print()
    
    print("3. VISUALIZAÇÃO ASCII DE UMA TUPLA:")
    tupla_exemplo = ('A', 'B', 'C', 'D', 'E')
    print("   Tupla: ('A', 'B', 'C', 'D', 'E')")
    print()
    print("   ┌───┬───┬───┬───┬───┐")
    print("   │ A │ B │ C │ D │ E │  🔒 IMUTÁVEL")
    print("   └───┴───┴───┴───┴───┘")
    print("     0   1   2   3   4   ← Índices")
    print("    -5  -4  -3  -2  -1   ← Índices negativos")
    print()
    
    print("4. DIFERENÇAS PRINCIPAIS COM LISTAS:")
    print("   ┌─────────────────┬─────────────┬─────────────┐")
    print("   │   CARACTERÍSTICA│    TUPLA    │    LISTA    │")
    print("   ├─────────────────┼─────────────┼─────────────┤")
    print("   │ Mutabilidade    │  Imutável   │   Mutável   │")
    print("   │ Sintaxe         │    ( )      │    [ ]      │")
    print("   │ Performance     │ Mais rápida│ Mais lenta  │")
    print("   │ Uso de memória  │   Menor     │   Maior     │")
    print("   │ Métodos         │   Poucos    │   Muitos    │")
    print("   │ Chave dict      │     Sim     │     Não     │")
    print("   │ Hashable        │     Sim     │     Não     │")
    print("   └─────────────────┴─────────────┴─────────────┘")
    print()
    
    print("5. EXEMPLO PRÁTICO:")
    print("   # Criando uma tupla")
    print("   coordenadas = (40.7128, -74.0060)  # NYC")
    print("   print(f'Tupla: {coordenadas}')")
    print("   print(f'Latitude: {coordenadas[0]}')")
    print("   print(f'Longitude: {coordenadas[1]}')")
    print("   print(f'Tamanho: {len(coordenadas)}')")
    print()
    
    # Executando o exemplo
    coordenadas = (40.7128, -74.0060)
    print("   RESULTADO:")
    print(f"   → Tupla: {coordenadas}")
    print(f"   → Latitude: {coordenadas[0]}")
    print(f"   → Longitude: {coordenadas[1]}")
    print(f"   → Tamanho: {len(coordenadas)}")
    print()
    
    print("6. TENTATIVA DE MODIFICAÇÃO (ERRO):")
    print("   # coordenadas[0] = 41.0  # ❌ TypeError!")
    print("   # Tuplas são imutáveis - não podem ser modificadas")
    print()

def criacao_sintaxe():
    """
    Explora diferentes formas de criar tuplas e suas sintaxes.
    
    Analogia: Criar tuplas é como embalar produtos em diferentes
    tipos de embalagens seladas, cada uma com suas regras específicas.
    """
    print("=== CRIAÇÃO E SINTAXE DE TUPLAS ===")
    print()
    
    print("1. TUPLA VAZIA:")
    print("   tupla_vazia1 = ()")
    print("   tupla_vazia2 = tuple()")
    print()
    tupla_vazia1 = ()
    tupla_vazia2 = tuple()
    print(f"   → tupla_vazia1: {tupla_vazia1} (tipo: {type(tupla_vazia1)})")
    print(f"   → tupla_vazia2: {tupla_vazia2} (tipo: {type(tupla_vazia2)})")
    print()
    
    print("2. TUPLA COM UM ELEMENTO (CUIDADO COM A VÍRGULA!):")
    print("   # ERRADO - Não é tupla, são apenas parênteses")
    print("   nao_tupla = (42)")
    print("   print(type(nao_tupla))  # <class 'int'>")
    print()
    print("   # CORRETO - Vírgula torna elemento em tupla")
    print("   tupla_um = (42,)")
    print("   tupla_um_alt = 42,")
    print("   print(type(tupla_um))   # <class 'tuple'>")
    print()
    
    nao_tupla = (42)
    tupla_um = (42,)
    tupla_um_alt = 42,
    
    print("   RESULTADO:")
    print(f"   → nao_tupla: {nao_tupla} (tipo: {type(nao_tupla)})")
    print(f"   → tupla_um: {tupla_um} (tipo: {type(tupla_um)})")
    print(f"   → tupla_um_alt: {tupla_um_alt} (tipo: {type(tupla_um_alt)})")
    print()
    
    print("3. TUPLAS COM MÚLTIPLOS ELEMENTOS:")
    print("   numeros = (1, 2, 3, 4, 5)")
    print("   cores = ('vermelho', 'azul', 'verde')")
    print("   mista = (1, 'texto', 3.14, True, None)")
    print("   sem_parenteses = 1, 2, 3, 4, 5  # Também é tupla!")
    print()
    
    numeros = (1, 2, 3, 4, 5)
    cores = ('vermelho', 'azul', 'verde')
    mista = (1, 'texto', 3.14, True, None)
    sem_parenteses = 1, 2, 3, 4, 5
    
    print("   RESULTADO:")
    print(f"   → numeros: {numeros}")
    print(f"   → cores: {cores}")
    print(f"   → mista: {mista}")
    print(f"   → sem_parenteses: {sem_parenteses}")
    print()
    
    print("4. CRIAÇÃO A PARTIR DE OUTROS ITERÁVEIS:")
    print("   # A partir de lista")
    print("   lista = [1, 2, 3, 4]")
    print("   tupla_da_lista = tuple(lista)")
    print()
    print("   # A partir de string")
    print("   tupla_string = tuple('Python')")
    print()
    print("   # A partir de range")
    print("   tupla_range = tuple(range(5))")
    print()
    
    lista = [1, 2, 3, 4]
    tupla_da_lista = tuple(lista)
    tupla_string = tuple('Python')
    tupla_range = tuple(range(5))
    
    print("   RESULTADO:")
    print(f"   → tupla_da_lista: {tupla_da_lista}")
    print(f"   → tupla_string: {tupla_string}")
    print(f"   → tupla_range: {tupla_range}")
    print()
    
    print("5. TUPLAS ANINHADAS:")
    print("   # Tupla de tuplas")
    print("   matriz_tupla = ((1, 2, 3), (4, 5, 6), (7, 8, 9))")
    print("   coordenadas_3d = ((0, 0, 0), (1, 1, 1), (2, 2, 2))")
    print()
    print("   # Tupla mista com diferentes tipos")
    print("   pessoa = ('João', 30, (1.75, 70), ('Python', 'Java'))")
    print()
    
    matriz_tupla = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    coordenadas_3d = ((0, 0, 0), (1, 1, 1), (2, 2, 2))
    pessoa = ('João', 30, (1.75, 70), ('Python', 'Java'))
    
    print("   RESULTADO:")
    print(f"   → matriz_tupla: {matriz_tupla}")
    print(f"   → coordenadas_3d: {coordenadas_3d}")
    print(f"   → pessoa: {pessoa}")
    print()
    
    print("6. BOAS PRÁTICAS DE SINTAXE:")
    print("   ✅ Use parênteses para clareza")
    print("   ✅ Sempre use vírgula para tuplas de um elemento")
    print("   ✅ Use quebras de linha para tuplas longas")
    print("   ✅ Agrupe elementos relacionados logicamente")
    print()
    
    print("   Exemplo de tupla bem formatada:")
    print("   endereco = (")
    print("       'Rua das Flores, 123',")
    print("       'São Paulo',")
    print("       'SP',")
    print("       '01234-567'")
    print("   )")
    print()
    
    endereco = (
        'Rua das Flores, 123',
        'São Paulo',
        'SP',
        '01234-567'
    )
    print(f"   → endereco: {endereco}")
    print()

def imutabilidade_detalhada():
    """
    Explora o conceito de imutabilidade em profundidade.
    
    Analogia: Imutabilidade é como um contrato assinado.
    Uma vez estabelecido, não pode ser alterado, apenas
    um novo contrato pode ser criado.
    """
    print("=== IMUTABILIDADE DETALHADA ===")
    print()
    
    print("1. O QUE SIGNIFICA IMUTÁVEL?")
    print("   → Não pode ser modificada após criação")
    print("   → Operações criam novas tuplas")
    print("   → Referência pode mudar, objeto não")
    print("   → Garante integridade dos dados")
    print("   → Permite uso como chave de dicionário")
    print("   → Thread-safe por natureza")
    print()
    
    print("2. DEMONSTRAÇÃO DE IMUTABILIDADE:")
    original = (1, 2, 3)
    print(f"   Tupla original: {original}")
    print(f"   ID da tupla: {id(original)}")
    print()
    
    print("   # Tentativas de modificação (todas falharão):")
    print("   # original[0] = 10        # ❌ TypeError")
    print("   # original.append(4)      # ❌ AttributeError")
    print("   # original.remove(1)      # ❌ AttributeError")
    print("   # del original[0]         # ❌ TypeError")
    print()
    
    print("3. OPERAÇÕES QUE CRIAM NOVAS TUPLAS:")
    print("   # Concatenação")
    print("   nova_tupla = original + (4, 5)")
    nova_tupla = original + (4, 5)
    print(f"   → Nova tupla: {nova_tupla}")
    print(f"   → ID nova tupla: {id(nova_tupla)}")
    print(f"   → Original inalterada: {original}")
    print()
    
    print("   # Repetição")
    print("   repetida = original * 2")
    repetida = original * 2
    print(f"   → Repetida: {repetida}")
    print()
    
    print("   # Fatiamento")
    print("   fatia = original[1:]")
    fatia = original[1:]
    print(f"   → Fatia: {fatia}")
    print(f"   → ID fatia: {id(fatia)}")
    print()
    
    print("4. CUIDADO COM OBJETOS MUTÁVEIS DENTRO DE TUPLAS:")
    print("   # Tupla contendo lista (objeto mutável)")
    print("   tupla_com_lista = (1, [2, 3, 4], 5)")
    tupla_com_lista = (1, [2, 3, 4], 5)
    print(f"   → Tupla original: {tupla_com_lista}")
    print(f"   → ID da tupla: {id(tupla_com_lista)}")
    print()
    
    print("   # A tupla é imutável, mas a lista dentro dela não!")
    print("   tupla_com_lista[1].append(6)")
    tupla_com_lista[1].append(6)
    print(f"   → Após modificar lista: {tupla_com_lista}")
    print(f"   → ID da tupla (mesmo): {id(tupla_com_lista)}")
    print("   ⚠️  A tupla não mudou, mas seu conteúdo sim!")
    print()
    
    print("5. COMPARAÇÃO DE IDENTIDADE:")
    tupla1 = (1, 2, 3)
    tupla2 = (1, 2, 3)
    tupla3 = tupla1
    
    print(f"   tupla1: {tupla1} (ID: {id(tupla1)})")
    print(f"   tupla2: {tupla2} (ID: {id(tupla2)})")
    print(f"   tupla3: {tupla3} (ID: {id(tupla3)})")
    print()
    
    print(f"   → tupla1 == tupla2: {tupla1 == tupla2} (valores iguais)")
    print(f"   → tupla1 is tupla2: {tupla1 is tupla2} (objetos diferentes)")
    print(f"   → tupla1 is tupla3: {tupla1 is tupla3} (mesmo objeto)")
    print()
    
    print("6. VANTAGENS DA IMUTABILIDADE:")
    print("   ✅ Segurança: Dados não podem ser alterados acidentalmente")
    print("   ✅ Performance: Otimizações internas do Python")
    print("   ✅ Hashable: Pode ser chave de dicionário ou elemento de set")
    print("   ✅ Thread-safe: Múltiplas threads podem acessar sem problemas")
    print("   ✅ Debugging: Menos bugs relacionados a modificações inesperadas")
    print("   ✅ Funcional: Adequada para programação funcional")
    print()
    
    print("7. QUANDO A IMUTABILIDADE É ÚTIL:")
    print("   📍 Coordenadas geográficas")
    print("   📅 Datas e horários")
    print("   🔑 Chaves de configuração")
    print("   📊 Dados de entrada de funções")
    print("   🏷️  Identificadores únicos")
    print("   📋 Registros de log")
    print("   🎯 Constantes do sistema")
    print()

def operacoes_basicas_tuplas():
    """
    Explora operações básicas disponíveis para tuplas.
    
    Analogia: Operações com tuplas são como consultas a um arquivo.
    Você pode ler, pesquisar e extrair informações, mas não modificar.
    """
    print("=== OPERAÇÕES BÁSICAS COM TUPLAS ===")
    print()
    
    print("1. ACESSO POR ÍNDICE:")
    frutas = ('maçã', 'banana', 'laranja', 'uva', 'manga')
    print(f"   Tupla: {frutas}")
    print()
    
    print("   # Acesso positivo")
    print("   frutas[0]   # Primeira fruta")
    print("   frutas[2]   # Terceira fruta")
    print("   frutas[-1]  # Última fruta")
    print("   frutas[-2]  # Penúltima fruta")
    print()
    
    print("   RESULTADO:")
    print(f"   → frutas[0] = '{frutas[0]}'")
    print(f"   → frutas[2] = '{frutas[2]}'")
    print(f"   → frutas[-1] = '{frutas[-1]}'")
    print(f"   → frutas[-2] = '{frutas[-2]}'")
    print()
    
    print("2. FATIAMENTO (SLICING):")
    numeros = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    print(f"   Tupla: {numeros}")
    print()
    
    print("   # Fatiamento básico")
    print("   numeros[2:6]    # Do índice 2 ao 5")
    print("   numeros[:4]     # Do início ao índice 3")
    print("   numeros[6:]     # Do índice 6 ao final")
    print("   numeros[::2]    # Todos, pulando de 2 em 2")
    print("   numeros[::-1]   # Todos em ordem reversa")
    print()
    
    print("   RESULTADO:")
    print(f"   → numeros[2:6] = {numeros[2:6]}")
    print(f"   → numeros[:4] = {numeros[:4]}")
    print(f"   → numeros[6:] = {numeros[6:]}")
    print(f"   → numeros[::2] = {numeros[::2]}")
    print(f"   → numeros[::-1] = {numeros[::-1]}")
    print()
    
    print("3. MÉTODOS DISPONÍVEIS (APENAS 2!):")
    elementos = (1, 2, 3, 2, 4, 2, 5)
    print(f"   Tupla: {elementos}")
    print()
    
    print("   # count() - Conta ocorrências")
    print("   elementos.count(2)")
    count_2 = elementos.count(2)
    print(f"   → Quantidade de 2: {count_2}")
    print()
    
    print("   # index() - Encontra primeira ocorrência")
    print("   elementos.index(2)")
    index_2 = elementos.index(2)
    print(f"   → Primeiro índice de 2: {index_2}")
    print()
    
    print("   # index() com início e fim")
    print("   elementos.index(2, 2)  # Buscar a partir do índice 2")
    index_2_from_2 = elementos.index(2, 2)
    print(f"   → Próximo índice de 2: {index_2_from_2}")
    print()
    
    print("4. OPERADORES:")
    tupla1 = (1, 2, 3)
    tupla2 = (4, 5, 6)
    
    print(f"   tupla1: {tupla1}")
    print(f"   tupla2: {tupla2}")
    print()
    
    print("   # Concatenação (+)")
    print("   tupla1 + tupla2")
    concatenada = tupla1 + tupla2
    print(f"   → Resultado: {concatenada}")
    print()
    
    print("   # Repetição (*)")
    print("   tupla1 * 3")
    repetida = tupla1 * 3
    print(f"   → Resultado: {repetida}")
    print()
    
    print("   # Pertencimento (in)")
    print("   2 in tupla1")
    print("   7 in tupla1")
    print(f"   → 2 está em tupla1: {2 in tupla1}")
    print(f"   → 7 está em tupla1: {7 in tupla1}")
    print()
    
    print("5. FUNÇÕES BUILT-IN:")
    valores = (10, 5, 8, 3, 12, 7, 15)
    print(f"   Tupla: {valores}")
    print()
    
    print("   # Funções básicas")
    print(f"   → len(valores): {len(valores)}")
    print(f"   → min(valores): {min(valores)}")
    print(f"   → max(valores): {max(valores)}")
    print(f"   → sum(valores): {sum(valores)}")
    print(f"   → sorted(valores): {sorted(valores)}")  # Retorna lista!
    print()
    
    print("6. COMPARAÇÃO DE TUPLAS:")
    tupla_a = (1, 2, 3)
    tupla_b = (1, 2, 4)
    tupla_c = (1, 2, 3)
    
    print(f"   tupla_a: {tupla_a}")
    print(f"   tupla_b: {tupla_b}")
    print(f"   tupla_c: {tupla_c}")
    print()
    
    print("   # Comparações lexicográficas")
    print(f"   → tupla_a == tupla_c: {tupla_a == tupla_c}")
    print(f"   → tupla_a < tupla_b: {tupla_a < tupla_b}")
    print(f"   → tupla_a > tupla_b: {tupla_a > tupla_b}")
    print()
    
    print("7. ITERAÇÃO:")
    cores = ('vermelho', 'verde', 'azul')
    print(f"   Tupla: {cores}")
    print()
    
    print("   # Iteração simples")
    print("   for cor in cores:")
    print("       print(f'Cor: {cor}')")
    print()
    print("   RESULTADO:")
    for cor in cores:
        print(f"   → Cor: {cor}")
    print()
    
    print("   # Iteração com índice")
    print("   for i, cor in enumerate(cores):")
    print("       print(f'{i}: {cor}')")
    print()
    print("   RESULTADO:")
    for i, cor in enumerate(cores):
        print(f"   → {i}: {cor}")
    print()

def unpacking_packing():
    """
    Explora unpacking e packing de tuplas - recursos poderosos do Python.
    
    Analogia: Unpacking é como desembalar uma caixa de presentes,
    onde cada item vai para uma variável específica.
    Packing é o processo inverso - embalar itens numa caixa.
    """
    print("=== UNPACKING E PACKING DE TUPLAS ===")
    print()
    
    print("1. UNPACKING BÁSICO:")
    coordenadas = (10, 20)
    print(f"   Tupla: {coordenadas}")
    print()
    
    print("   # Unpacking simples")
    print("   x, y = coordenadas")
    x, y = coordenadas
    print(f"   → x = {x}")
    print(f"   → y = {y}")
    print()
    
    print("   # Unpacking com múltiplos valores")
    pessoa = ('Ana', 25, 'Engenheira', 'São Paulo')
    print(f"   Tupla: {pessoa}")
    print("   nome, idade, profissao, cidade = pessoa")
    nome, idade, profissao, cidade = pessoa
    print(f"   → nome = '{nome}'")
    print(f"   → idade = {idade}")
    print(f"   → profissao = '{profissao}'")
    print(f"   → cidade = '{cidade}'")
    print()
    
    print("2. UNPACKING COM ASTERISCO (*):")
    numeros = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    print(f"   Tupla: {numeros}")
    print()
    
    print("   # Primeiro, último e o resto")
    print("   primeiro, *meio, ultimo = numeros")
    primeiro, *meio, ultimo = numeros
    print(f"   → primeiro = {primeiro}")
    print(f"   → meio = {meio}")  # Lista!
    print(f"   → ultimo = {ultimo}")
    print()
    
    print("   # Primeiros dois e o resto")
    print("   a, b, *resto = numeros")
    a, b, *resto = numeros
    print(f"   → a = {a}")
    print(f"   → b = {b}")
    print(f"   → resto = {resto}")
    print()
    
    print("   # O resto no meio")
    print("   inicio, *meio, fim1, fim2 = numeros")
    inicio, *meio, fim1, fim2 = numeros
    print(f"   → inicio = {inicio}")
    print(f"   → meio = {meio}")
    print(f"   → fim1 = {fim1}")
    print(f"   → fim2 = {fim2}")
    print()
    
    print("3. PACKING (CRIAÇÃO AUTOMÁTICA):")
    print("   # Packing automático")
    print("   dados = 'João', 30, 'Programador'")
    dados = 'João', 30, 'Programador'
    print(f"   → dados = {dados} (tipo: {type(dados)})")
    print()
    
    print("   # Packing em função")
    def criar_pessoa(nome, idade, profissao):
        return nome, idade, profissao  # Retorna tupla automaticamente
    
    print("   def criar_pessoa(nome, idade, profissao):")
    print("       return nome, idade, profissao")
    print()
    print("   resultado = criar_pessoa('Maria', 28, 'Designer')")
    resultado = criar_pessoa('Maria', 28, 'Designer')
    print(f"   → resultado = {resultado}")
    print()
    
    print("4. TROCA DE VARIÁVEIS:")
    print("   # Forma tradicional (outras linguagens)")
    print("   # temp = a")
    print("   # a = b")
    print("   # b = temp")
    print()
    print("   # Forma pythônica com tuplas")
    a, b = 10, 20
    print(f"   Antes: a = {a}, b = {b}")
    print("   a, b = b, a")
    a, b = b, a
    print(f"   Depois: a = {a}, b = {b}")
    print()
    
    print("5. UNPACKING EM LOOPS:")
    pontos = [(0, 0), (1, 2), (3, 4), (5, 6)]
    print(f"   Lista de tuplas: {pontos}")
    print()
    
    print("   # Unpacking em for loop")
    print("   for x, y in pontos:")
    print("       print(f'Ponto: ({x}, {y})')")
    print()
    print("   RESULTADO:")
    for x, y in pontos:
        print(f"   → Ponto: ({x}, {y})")
    print()
    
    print("6. UNPACKING EM FUNÇÕES:")
    def calcular_distancia(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    
    print("   def calcular_distancia(p1, p2):")
    print("       x1, y1 = p1")
    print("       x2, y2 = p2")
    print("       return ((x2 - x1)**2 + (y2 - y1)**2)**0.5")
    print()
    
    ponto1 = (0, 0)
    ponto2 = (3, 4)
    distancia = calcular_distancia(ponto1, ponto2)
    print(f"   Distância entre {ponto1} e {ponto2}: {distancia}")
    print()
    
    print("7. UNPACKING COM ARGUMENTOS DE FUNÇÃO:")
    def somar_tres(a, b, c):
        return a + b + c
    
    valores = (10, 20, 30)
    print(f"   Tupla: {valores}")
    print("   def somar_tres(a, b, c):")
    print("       return a + b + c")
    print()
    print("   # Unpacking com *")
    print("   resultado = somar_tres(*valores)")
    resultado = somar_tres(*valores)
    print(f"   → Resultado: {resultado}")
    print()
    
    print("8. CASOS PRÁTICOS:")
    print("   # Retorno múltiplo de função")
    def estatisticas(numeros):
        return min(numeros), max(numeros), sum(numeros)/len(numeros)
    
    dados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    minimo, maximo, media = estatisticas(dados)
    
    print("   def estatisticas(numeros):")
    print("       return min(numeros), max(numeros), sum(numeros)/len(numeros)")
    print()
    print(f"   minimo, maximo, media = estatisticas({dados[:5]}...)")
    print(f"   → Mínimo: {minimo}")
    print(f"   → Máximo: {maximo}")
    print(f"   → Média: {media:.2f}")
    print()

def namedtuples():
    """
    Explora namedtuples - tuplas com campos nomeados.
    
    Analogia: NamedTuple é como um formulário com campos específicos.
    Você pode acessar os dados tanto por posição quanto por nome do campo.
    """
    print("=== NAMEDTUPLES ===")
    print()
    
    print("1. O QUE SÃO NAMEDTUPLES?")
    print("   → Subclasse de tupla com campos nomeados")
    print("   → Mantém todas as características de tuplas")
    print("   → Adiciona acesso por nome de atributo")
    print("   → Mais legível que tuplas normais")
    print("   → Ainda imutável e hashable")
    print("   → Definida na biblioteca collections")
    print()
    
    print("2. CRIANDO UMA NAMEDTUPLE:")
    print("   from collections import namedtuple")
    print()
    print("   # Definindo a estrutura")
    print("   Pessoa = namedtuple('Pessoa', ['nome', 'idade', 'cidade'])")
    print("   # ou")
    print("   Pessoa = namedtuple('Pessoa', 'nome idade cidade')")
    print()
    
    # Criando namedtuple
    Pessoa = namedtuple('Pessoa', ['nome', 'idade', 'cidade'])
    
    print("   # Criando instâncias")
    print("   p1 = Pessoa('Ana', 25, 'São Paulo')")
    print("   p2 = Pessoa(nome='Bruno', idade=30, cidade='Rio de Janeiro')")
    
    p1 = Pessoa('Ana', 25, 'São Paulo')
    p2 = Pessoa(nome='Bruno', idade=30, cidade='Rio de Janeiro')
    
    print(f"   → p1: {p1}")
    print(f"   → p2: {p2}")
    print()
    
    print("3. ACESSANDO DADOS:")
    print("   # Por índice (como tupla normal)")
    print(f"   p1[0] = '{p1[0]}'")
    print(f"   p1[1] = {p1[1]}")
    print()
    
    print("   # Por nome (vantagem da namedtuple)")
    print(f"   p1.nome = '{p1.nome}'")
    print(f"   p1.idade = {p1.idade}")
    print(f"   p1.cidade = '{p1.cidade}'")
    print()
    
    print("4. MÉTODOS ESPECIAIS:")
    print("   # _asdict() - Converte para dicionário")
    print("   p1_dict = p1._asdict()")
    p1_dict = p1._asdict()
    print(f"   → {p1_dict}")
    print()
    
    print("   # _replace() - Cria nova instância com alterações")
    print("   p1_nova_idade = p1._replace(idade=26)")
    p1_nova_idade = p1._replace(idade=26)
    print(f"   → Original: {p1}")
    print(f"   → Modificada: {p1_nova_idade}")
    print()
    
    print("   # _fields - Lista os campos")
    print(f"   Pessoa._fields = {Pessoa._fields}")
    print()
    
    print("5. EXEMPLO PRÁTICO - COORDENADAS:")
    Ponto = namedtuple('Ponto', ['x', 'y'])
    
    print("   Ponto = namedtuple('Ponto', ['x', 'y'])")
    print()
    
    # Criando pontos
    origem = Ponto(0, 0)
    destino = Ponto(3, 4)
    
    print(f"   origem = Ponto(0, 0) → {origem}")
    print(f"   destino = Ponto(3, 4) → {destino}")
    print()
    
    # Calculando distância
    def distancia(p1, p2):
        return ((p2.x - p1.x)**2 + (p2.y - p1.y)**2)**0.5
    
    print("   def distancia(p1, p2):")
    print("       return ((p2.x - p1.x)**2 + (p2.y - p1.y)**2)**0.5")
    print()
    
    dist = distancia(origem, destino)
    print(f"   Distância: {dist}")
    print()
    
    print("6. EXEMPLO PRÁTICO - REGISTRO DE FUNCIONÁRIO:")
    Funcionario = namedtuple('Funcionario', [
        'id', 'nome', 'departamento', 'salario', 'data_admissao'
    ])
    
    print("   Funcionario = namedtuple('Funcionario', [")
    print("       'id', 'nome', 'departamento', 'salario', 'data_admissao'")
    print("   ])")
    print()
    
    # Criando funcionários
    func1 = Funcionario(1, 'Maria Silva', 'TI', 8000, '2023-01-15')
    func2 = Funcionario(2, 'João Santos', 'RH', 6500, '2023-03-20')
    
    funcionarios = [func1, func2]
    
    print("   Funcionários cadastrados:")
    for func in funcionarios:
        print(f"   → {func.nome} ({func.departamento}) - R$ {func.salario}")
    print()
    
    print("7. VANTAGENS DAS NAMEDTUPLES:")
    print("   ✅ Mais legível que tuplas normais")
    print("   ✅ Mantém performance de tuplas")
    print("   ✅ Imutável (segurança)")
    print("   ✅ Pode ser usada como chave de dicionário")
    print("   ✅ Suporte a unpacking")
    print("   ✅ Menos memória que classes")
    print("   ✅ Compatível com código que espera tuplas")
    print()
    
    print("8. QUANDO USAR NAMEDTUPLES:")
    print("   📊 Dados estruturados simples")
    print("   📍 Coordenadas e pontos")
    print("   📋 Registros de banco de dados")
    print("   🔧 Configurações")
    print("   📈 Dados científicos")
    print("   🎯 Retorno de múltiplos valores de funções")
    print("   📝 Estruturas de dados temporárias")
    print()

def performance_comparacao():
    """
    Compara performance entre tuplas, listas e namedtuples.
    
    Analogia: Performance é como eficiência de diferentes veículos.
    Cada um tem suas vantagens dependendo da situação.
    """
    print("=== ANÁLISE DE PERFORMANCE ===")
    print()
    
    print("1. COMPARAÇÃO DE MEMÓRIA:")
    
    # Criando estruturas de teste
    lista_teste = [1, 2, 3, 4, 5] * 1000
    tupla_teste = tuple(lista_teste)
    
    # Medindo tamanho
    tamanho_lista = sys.getsizeof(lista_teste)
    tamanho_tupla = sys.getsizeof(tupla_teste)
    
    print(f"   Lista com 5000 elementos: {tamanho_lista:,} bytes")
    print(f"   Tupla com 5000 elementos: {tamanho_tupla:,} bytes")
    print(f"   → Tupla usa {((tamanho_lista - tamanho_tupla) / tamanho_lista * 100):.1f}% menos memória")
    print()
    
    print("2. TESTE DE CRIAÇÃO:")
    import time
    
    def teste_criacao_lista():
        return [1, 2, 3, 4, 5] * 1000
    
    def teste_criacao_tupla():
        return (1, 2, 3, 4, 5) * 1000
    
    # Testando criação de lista
    start = time.time()
    for _ in range(10000):
        lista = teste_criacao_lista()
    tempo_lista = time.time() - start
    
    # Testando criação de tupla
    start = time.time()
    for _ in range(10000):
        tupla = teste_criacao_tupla()
    tempo_tupla = time.time() - start
    
    print(f"   Criação de 10.000 listas: {tempo_lista:.4f}s")
    print(f"   Criação de 10.000 tuplas: {tempo_tupla:.4f}s")
    print(f"   → Tupla é {tempo_lista/tempo_tupla:.1f}x mais rápida na criação")
    print()
    
    print("3. TESTE DE ACESSO:")
    lista_acesso = list(range(1000))
    tupla_acesso = tuple(range(1000))
    
    # Testando acesso em lista
    start = time.time()
    for _ in range(100000):
        _ = lista_acesso[500]
    tempo_acesso_lista = time.time() - start
    
    # Testando acesso em tupla
    start = time.time()
    for _ in range(100000):
        _ = tupla_acesso[500]
    tempo_acesso_tupla = time.time() - start
    
    print(f"   Acesso 100.000x em lista: {tempo_acesso_lista:.4f}s")
    print(f"   Acesso 100.000x em tupla: {tempo_acesso_tupla:.4f}s")
    print(f"   → Tupla é {tempo_acesso_lista/tempo_acesso_tupla:.1f}x mais rápida no acesso")
    print()
    
    print("4. TESTE DE ITERAÇÃO:")
    # Testando iteração em lista
    start = time.time()
    for _ in range(1000):
        for item in lista_acesso:
            pass
    tempo_iter_lista = time.time() - start
    
    # Testando iteração em tupla
    start = time.time()
    for _ in range(1000):
        for item in tupla_acesso:
            pass
    tempo_iter_tupla = time.time() - start
    
    print(f"   Iteração 1.000x em lista: {tempo_iter_lista:.4f}s")
    print(f"   Iteração 1.000x em tupla: {tempo_iter_tupla:.4f}s")
    print(f"   → Tupla é {tempo_iter_lista/tempo_iter_tupla:.1f}x mais rápida na iteração")
    print()
    
    print("5. COMPARAÇÃO COM NAMEDTUPLE:")
    Ponto = namedtuple('Ponto', ['x', 'y'])
    
    # Testando criação de namedtuple
    start = time.time()
    for _ in range(10000):
        ponto = Ponto(1, 2)
    tempo_namedtuple = time.time() - start
    
    # Testando criação de tupla normal
    start = time.time()
    for _ in range(10000):
        ponto = (1, 2)
    tempo_tupla_normal = time.time() - start
    
    print(f"   Criação 10.000 namedtuples: {tempo_namedtuple:.4f}s")
    print(f"   Criação 10.000 tuplas normais: {tempo_tupla_normal:.4f}s")
    print(f"   → Tupla normal é {tempo_namedtuple/tempo_tupla_normal:.1f}x mais rápida")
    print()
    
    print("6. RESUMO DE PERFORMANCE:")
    print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │   OPERAÇÃO      │    LISTA    │    TUPLA    │ NAMEDTUPLE  │")
    print("   ├─────────────────┼─────────────┼─────────────┼─────────────┤")
    print("   │ Uso de memória  │    Alto     │    Baixo    │    Médio    │")
    print("   │ Criação         │   Lenta     │   Rápida    │    Média    │")
    print("   │ Acesso          │   Rápido    │ Mais rápido│    Rápido   │")
    print("   │ Iteração        │   Rápida    │ Mais rápida│    Rápida   │")
    print("   │ Modificação     │     Sim     │     Não     │     Não     │")
    print("   │ Legibilidade    │    Boa      │   Limitada  │   Excelente │")
    print("   └─────────────────┴─────────────┴─────────────┴─────────────┘")
    print()
    
    print("7. RECOMENDAÇÕES DE USO:")
    print("   🚀 Use TUPLAS quando:")
    print("      • Performance é crítica")
    print("      • Dados não mudam")
    print("      • Precisa de chave de dicionário")
    print("      • Estrutura simples")
    print()
    print("   📝 Use LISTAS quando:")
    print("      • Precisa modificar dados")
    print("      • Tamanho varia frequentemente")
    print("      • Muitas operações de inserção/remoção")
    print()
    print("   🏷️  Use NAMEDTUPLES quando:")
    print("      • Precisa de legibilidade")
    print("      • Estrutura de dados bem definida")
    print("      • Acesso por nome é importante")
    print("      • Dados não mudam")
    print()

def casos_uso_praticos():
    """
    Demonstra casos de uso práticos para tuplas.
    """
    print("=== CASOS DE USO PRÁTICOS ===")
    print()
    
    print("Caso 1: Sistema de Coordenadas Geográficas")
    
    def sistema_coordenadas():
        """Sistema para gerenciar coordenadas geográficas"""
        
        # Definindo pontos de interesse
        pontos_interesse = {
            'Cristo Redentor': (-22.9519, -43.2105),
            'Torre Eiffel': (48.8584, 2.2945),
            'Times Square': (40.7580, -73.9855),
            'Big Ben': (51.4994, -0.1245)
        }
        
        print("   Pontos de interesse (nome: (latitude, longitude)):")
        for nome, (lat, lon) in pontos_interesse.items():
            print(f"   → {nome}: ({lat}, {lon})")
        print()
        
        # Função para calcular distância
        def calcular_distancia_geo(coord1, coord2):
            """Calcula distância aproximada entre coordenadas"""
            lat1, lon1 = coord1
            lat2, lon2 = coord2
            
            # Fórmula simplificada (não considera curvatura da Terra)
            diff_lat = lat2 - lat1
            diff_lon = lon2 - lon1
            return (diff_lat**2 + diff_lon**2)**0.5
        
        # Calculando distâncias
        cristo = pontos_interesse['Cristo Redentor']
        torre_eiffel = pontos_interesse['Torre Eiffel']
        
        distancia = calcular_distancia_geo(cristo, torre_eiffel)
        print(f"   Distância Cristo Redentor ↔ Torre Eiffel: {distancia:.2f} unidades")
        print()
        
        return pontos_interesse
    
    sistema_coordenadas()
    
    print("Caso 2: Configurações de Sistema")
    
    def configuracoes_sistema():
        """Sistema de configurações usando tuplas como chaves"""
        
        # Configurações por ambiente e módulo
        configuracoes = {
            ('desenvolvimento', 'database'): {
                'host': 'localhost',
                'porta': 5432,
                'debug': True
            },
            ('producao', 'database'): {
                'host': 'db.empresa.com',
                'porta': 5432,
                'debug': False
            },
            ('desenvolvimento', 'cache'): {
                'host': 'localhost',
                'porta': 6379,
                'ttl': 300
            },
            ('producao', 'cache'): {
                'host': 'cache.empresa.com',
                'porta': 6379,
                'ttl': 3600
            }
        }
        
        print("   Configurações por (ambiente, módulo):")
        for (ambiente, modulo), config in configuracoes.items():
            print(f"   → {ambiente.title()} - {modulo.title()}:")
            for chave, valor in config.items():
                print(f"     • {chave}: {valor}")
        print()
        
        # Função para obter configuração
        def obter_config(ambiente, modulo):
            return configuracoes.get((ambiente, modulo), {})
        
        # Exemplo de uso
        config_dev_db = obter_config('desenvolvimento', 'database')
        print(f"   Config Dev Database: {config_dev_db}")
        print()
        
        return configuracoes
    
    configuracoes_sistema()
    
    print("Caso 3: Processamento de Dados CSV")
    
    def processar_dados_csv():
        """Simula processamento de dados CSV com tuplas"""
        
        # Dados simulados de vendas (data, produto, quantidade, valor)
        vendas_dados = [
            ('2024-01-15', 'Notebook', 2, 2500.00),
            ('2024-01-16', 'Mouse', 10, 25.00),
            ('2024-01-16', 'Teclado', 5, 80.00),
            ('2024-01-17', 'Monitor', 3, 450.00),
            ('2024-01-17', 'Notebook', 1, 2500.00),
            ('2024-01-18', 'Mouse', 15, 25.00)
        ]
        
        print("   Dados de vendas (data, produto, qtd, valor):")
        for venda in vendas_dados[:3]:  # Mostra apenas primeiras 3
            data, produto, qtd, valor = venda
            print(f"   → {data}: {produto} - {qtd}x R$ {valor:.2f}")
        print(f"   ... e mais {len(vendas_dados) - 3} registros")
        print()
        
        # Análises usando unpacking
        total_vendas = sum(qtd * valor for _, _, qtd, valor in vendas_dados)
        print(f"   Total de vendas: R$ {total_vendas:,.2f}")
        
        # Vendas por produto
        vendas_por_produto = {}
        for _, produto, qtd, valor in vendas_dados:
            if produto not in vendas_por_produto:
                vendas_por_produto[produto] = 0
            vendas_por_produto[produto] += qtd * valor
        
        print("   Vendas por produto:")
        for produto, total in sorted(vendas_por_produto.items(), 
                                   key=lambda x: x[1], reverse=True):
            print(f"   → {produto}: R$ {total:,.2f}")
        print()
        
        return vendas_dados
    
    processar_dados_csv()
    
    print("Caso 4: Cache com Chaves Compostas")
    
    def sistema_cache():
        """Sistema de cache usando tuplas como chaves compostas"""
        
        cache = {}
        
        def cache_resultado(usuario_id, operacao, parametros):
            """Cacheia resultado de operação"""
            chave = (usuario_id, operacao, tuple(sorted(parametros.items())))
            
            if chave in cache:
                print(f"   ✅ Cache HIT para {operacao} do usuário {usuario_id}")
                return cache[chave]
            
            # Simula processamento
            if operacao == 'relatorio_vendas':
                resultado = f"Relatório de vendas para {parametros}"
            elif operacao == 'dashboard':
                resultado = f"Dashboard para {parametros}"
            else:
                resultado = f"Resultado de {operacao}"
            
            cache[chave] = resultado
            print(f"   💾 Cache MISS - Armazenando {operacao} do usuário {usuario_id}")
            return resultado
        
        # Simulando uso do cache
        print("   Sistema de Cache com Chaves Compostas:")
        
        # Primeira chamada - cache miss
        resultado1 = cache_resultado(123, 'relatorio_vendas', 
                                   {'periodo': '2024-01', 'regiao': 'SP'})
        
        # Segunda chamada - cache hit
        resultado2 = cache_resultado(123, 'relatorio_vendas', 
                                   {'periodo': '2024-01', 'regiao': 'SP'})
        
        # Terceira chamada - cache miss (usuário diferente)
        resultado3 = cache_resultado(456, 'relatorio_vendas', 
                                   {'periodo': '2024-01', 'regiao': 'SP'})
        
        print(f"   Total de entradas no cache: {len(cache)}")
        print()
        
        return cache
    
    sistema_cache()

def exercicios_tuplas():
    """
    Exercícios progressivos para fixação de tuplas.
    """
    print("=== EXERCÍCIOS DE FIXAÇÃO - TUPLAS ===")
    print()
    
    print("NÍVEL 1 - Conceitos Básicos:")
    print("1. Criar tupla com dados pessoais (nome, idade, cidade)")
    print("2. Acessar elementos por índice positivo e negativo")
    print("3. Usar fatiamento para extrair partes da tupla")
    print("4. Contar ocorrências de um elemento")
    print("5. Encontrar índice de um elemento específico")
    print()
    
    print("NÍVEL 2 - Unpacking e Packing:")
    print("6. Fazer unpacking de tupla com coordenadas (x, y, z)")
    print("7. Trocar valores de três variáveis usando tuplas")
    print("8. Usar unpacking com asterisco (*) para separar elementos")
    print("9. Criar função que retorna múltiplos valores como tupla")
    print("10. Fazer unpacking em loop com lista de tuplas")
    print()
    
    print("NÍVEL 3 - NamedTuples:")
    print("11. Criar namedtuple para representar um livro")
    print("12. Converter namedtuple para dicionário")
    print("13. Usar _replace() para 'modificar' namedtuple")
    print("14. Criar lista de namedtuples e ordenar por campo")
    print("15. Implementar função que aceita namedtuple como parâmetro")
    print()
    
    print("NÍVEL 4 - Aplicações Práticas:")
    print("16. Sistema de coordenadas com operações matemáticas")
    print("17. Cache usando tuplas como chaves compostas")
    print("18. Processador de dados CSV retornando tuplas")
    print("19. Sistema de configurações por ambiente")
    print("20. Comparador de performance tupla vs lista")
    print()
    
    # Exemplo de solução
    print("EXEMPLO DE SOLUÇÃO - Exercício 9:")
    print("def estatisticas_lista(numeros):")
    print("    if not numeros:")
    print("        return None, None, None")
    print("    minimo = min(numeros)")
    print("    maximo = max(numeros)")
    print("    media = sum(numeros) / len(numeros)")
    print("    return minimo, maximo, media")
    print()
    
    # Executando o exemplo
    def estatisticas_lista(numeros):
        if not numeros:
            return None, None, None
        minimo = min(numeros)
        maximo = max(numeros)
        media = sum(numeros) / len(numeros)
        return minimo, maximo, media
    
    teste_numeros = [1, 5, 3, 9, 2, 7, 4, 8, 6]
    min_val, max_val, media_val = estatisticas_lista(teste_numeros)
    
    print(f"Lista: {teste_numeros}")
    print(f"Resultado: min={min_val}, max={max_val}, média={media_val:.2f}")
    print()

def resumo_tuplas():
    """
    Resumo visual de todos os conceitos de tuplas.
    """
    print("=== RESUMO DE TUPLAS ===")
    print()
    
    print("┌─────────────────────┬─────────────┬─────────────────────────────┐")
    print("│    CARACTERÍSTICA   │    TUPLA    │         DESCRIÇÃO           │")
    print("├─────────────────────┼─────────────┼─────────────────────────────┤")
    print("│ Mutabilidade        │  Imutável   │ Não pode ser modificada     │")
    print("│ Sintaxe             │    ( )      │ Parênteses (vírgula p/ 1)   │")
    print("│ Indexação           │     Sim     │ Acesso por índice [i]       │")
    print("│ Fatiamento          │     Sim     │ Slicing [início:fim:passo]  │")
    print("│ Métodos             │ count/index │ Apenas 2 métodos            │")
    print("│ Hashable            │     Sim     │ Pode ser chave de dict      │")
    print("│ Performance         │    Alta     │ Mais rápida que lista       │")
    print("│ Memória             │   Eficiente │ Menos memória que lista     │")
    print("│ Unpacking           │     Sim     │ a, b = tupla               │")
    print("│ Iteração            │     Sim     │ for item in tupla          │")
    print("└─────────────────────┴─────────────┴─────────────────────────────┘")
    print()
    
    print("OPERAÇÕES PRINCIPAIS:")
    print("• Criação: tupla = (1, 2, 3) ou tupla = 1, 2, 3")
    print("• Acesso: tupla[índice]")
    print("• Fatiamento: tupla[início:fim:passo]")
    print("• Unpacking: a, b, c = tupla")
    print("• Concatenação: tupla1 + tupla2")
    print("• Repetição: tupla * n")
    print("• Pertencimento: item in tupla")
    print("• Tamanho: len(tupla)")
    print("• Conversão: tuple(iterável)")
    print()
    
    print("NAMEDTUPLES:")
    print("• from collections import namedtuple")
    print("• Pessoa = namedtuple('Pessoa', ['nome', 'idade'])")
    print("• p = Pessoa('Ana', 25)")
    print("• Acesso: p.nome ou p[0]")
    print("• Métodos: _asdict(), _replace(), _fields")
    print()
    
    print("CASOS DE USO IDEAIS:")
    print("🎯 Coordenadas geográficas")
    print("🎯 Dados de configuração")
    print("🎯 Registros de banco de dados")
    print("🎯 Chaves compostas de dicionários")
    print("🎯 Retorno múltiplo de funções")
    print("🎯 Estruturas de dados temporárias")
    print("🎯 Dados que não devem ser modificados")
    print()
    
    print("PRÓXIMO MÓDULO: 2.3 - Dicionários e Mapeamentos")
    print("=" * 50)

if __name__ == "__main__":
    print("MÓDULO 2.2 - TUPLAS E IMUTABILIDADE")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceito_tuplas()
    print("\n" + "="*50 + "\n")
    
    criacao_sintaxe()
    print("\n" + "="*50 + "\n")
    
    imutabilidade_detalhada()
    print("\n" + "="*50 + "\n")
    
    operacoes_basicas_tuplas()
    print("\n" + "="*50 + "\n")
    
    unpacking_packing()
    print("\n" + "="*50 + "\n")
    
    namedtuples()
    print("\n" + "="*50 + "\n")
    
    performance_comparacao()
    print("\n" + "="*50 + "\n")
    
    casos_uso_praticos()
    print("\n" + "="*50 + "\n")
    
    exercicios_tuplas()
    print("\n" + "="*50 + "\n")
    
    resumo_tuplas()
    
    print("\n🎓 MÓDULO 2.2 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceito e características de tuplas")
    print("✅ Criação e sintaxe de tuplas")
    print("✅ Imutabilidade e suas implicações")
    print("✅ Operações básicas (acesso, fatiamento, métodos)")
    print("✅ Unpacking e packing de tuplas")
    print("✅ NamedTuples e suas vantagens")
    print("✅ Análise de performance vs listas")
    print("✅ Casos de uso práticos")
    print("✅ Exercícios de fixação")
    print("\n➡️  Próximo: Módulo 2.3 - Dicionários e Mapeamentos")