"""
Módulo: Conjuntos (Sets) e Operações
Tópico: Estruturas de Dados Nativas
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico a Intermediário

Objetivos de Aprendizado:
- Compreender conjuntos como coleções de elementos únicos
- Dominar criação e manipulação de sets
- Implementar operações matemáticas com conjuntos
- Trabalhar com set comprehensions
- Entender frozenset (conjuntos imutáveis)
- Aplicar conjuntos na resolução de problemas
- Analisar performance de operações com sets
- Resolver problemas de eliminação de duplicatas

Conceitos Abordados:
- Definição e características de conjuntos
- Criação de sets (set() e {})
- Operações básicas (add, remove, discard)
- Operações matemáticas (união, interseção, diferença)
- Set comprehensions
- frozenset - conjuntos imutáveis
- Métodos de comparação e teste
- Casos de uso práticos

Pré-requisitos:
- Módulos 2.1, 2.2 e 2.3 completos
- Conhecimento de iteração
- Compreensão de hashable objects

Complexidade Temporal:
- Busca: O(1) médio
- Inserção: O(1) médio
- Remoção: O(1) médio
- Operações de conjunto: O(min(len(s1), len(s2)))

Complexidade Espacial: O(n) onde n é o número de elementos únicos
"""

import time
import random

def conceito_conjuntos():
    """
    Introduz o conceito fundamental de conjuntos (sets).
    
    Analogia: Conjuntos são como coleções de objetos únicos,
    similar a uma caixa onde não pode haver itens duplicados.
    """
    print("=== CONCEITO DE CONJUNTOS (SETS) ===")
    print()
    
    print("1. O QUE SÃO CONJUNTOS?")
    print("   → Coleções não ordenadas de elementos únicos")
    print("   → Baseados na teoria matemática de conjuntos")
    print("   → Elementos devem ser hashable (imutáveis)")
    print("   → Não permitem duplicatas")
    print("   → Mutáveis - podem ser modificados")
    print("   → Otimizados para operações de pertencimento")
    print("   → Implementados como hash tables")
    print()
    
    print("2. ANALOGIAS DO COTIDIANO:")
    print("   🎯 Coleção de selos únicos")
    print("   👥 Lista de convidados (sem repetições)")
    print("   🏷️  Tags únicas de um post")
    print("   🎵 Playlist sem músicas repetidas")
    print("   📚 Conjunto de disciplinas cursadas")
    print("   🌟 Habilidades de um profissional")
    print("   🏆 Conquistas em um jogo")
    print()
    
    print("3. VISUALIZAÇÃO ASCII DE UM CONJUNTO:")
    exemplo_set = {1, 2, 3, 4, 5}
    print(f"   Conjunto: {exemplo_set}")
    print()
    print("   ┌─────────────────────────────┐")
    print("   │    CONJUNTO = {1,2,3,4,5}   │")
    print("   │                             │")
    print("   │    ┌───┐ ┌───┐ ┌───┐        │")
    print("   │    │ 1 │ │ 3 │ │ 5 │        │")
    print("   │    └───┘ └───┘ └───┘        │")
    print("   │         ┌───┐ ┌───┐         │")
    print("   │         │ 2 │ │ 4 │         │")
    print("   │         └───┘ └───┘         │")
    print("   │                             │")
    print("   │  • Sem ordem específica     │")
    print("   │  • Elementos únicos         │")
    print("   │  • Acesso rápido O(1)       │")
    print("   └─────────────────────────────┘")
    print()
    
    print("4. OPERAÇÕES MATEMÁTICAS VISUAIS:")
    print("   Conjunto A = {1, 2, 3, 4}")
    print("   Conjunto B = {3, 4, 5, 6}")
    print()
    print("   UNIÃO (A ∪ B):")
    print("   ┌─────────────────┐")
    print("   │  A     B        │")
    print("   │ ┌───┬─────┬───┐ │")
    print("   │ │1,2│3,4  │5,6│ │")
    print("   │ └───┴─────┴───┘ │")
    print("   │ Resultado: {1,2,3,4,5,6}")
    print("   └─────────────────┘")
    print()
    
    print("   INTERSEÇÃO (A ∩ B):")
    print("   ┌─────────────────┐")
    print("   │  A     B        │")
    print("   │ ┌───┬─────┬───┐ │")
    print("   │ │1,2│ 3,4 │5,6│ │")
    print("   │ └───┴─────┴───┘ │")
    print("   │ Resultado: {3,4}")
    print("   └─────────────────┘")
    print()
    
    print("5. DIFERENÇAS COM OUTRAS ESTRUTURAS:")
    print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │ CARACTERÍSTICA  │     SET     │    LISTA    │ DICIONÁRIO  │")
    print("   ├─────────────────┼─────────────┼─────────────┼─────────────┤")
    print("   │ Elementos       │   Únicos    │ Duplicatas  │ Chaves únic.│")
    print("   │ Ordem           │ Não ordenado│  Ordenada   │ Inserção*   │")
    print("   │ Indexação       │     Não     │     Sim     │ Por chave   │")
    print("   │ Mutabilidade    │   Mutável   │   Mutável   │   Mutável   │")
    print("   │ Busca           │    O(1)     │    O(n)     │    O(1)     │")
    print("   │ Operações Mat.  │     Sim     │     Não     │     Não     │")
    print("   │ Uso de memória  │    Médio    │   Baixo     │    Alto     │")
    print("   └─────────────────┴─────────────┴─────────────┴─────────────┘")
    print("   * Python ≥ 3.7")
    print()
    
    print("6. EXEMPLO PRÁTICO:")
    print("   # Removendo duplicatas de uma lista")
    lista_com_duplicatas = [1, 2, 2, 3, 3, 3, 4, 4, 5]
    print(f"   lista_original = {lista_com_duplicatas}")
    
    conjunto_unico = set(lista_com_duplicatas)
    lista_sem_duplicatas = list(conjunto_unico)
    
    print(f"   → Conjunto: {conjunto_unico}")
    print(f"   → Lista única: {sorted(lista_sem_duplicatas)}")
    print(f"   → Elementos removidos: {len(lista_com_duplicatas) - len(lista_sem_duplicatas)}")
    print()

def criacao_manipulacao_sets():
    """
    Explora diferentes formas de criar e manipular conjuntos.
    
    Analogia: Criar conjuntos é como organizar coleções,
    onde cada item só pode aparecer uma vez.
    """
    print("=== CRIAÇÃO E MANIPULAÇÃO DE SETS ===")
    print()
    
    print("1. CRIANDO CONJUNTOS VAZIOS:")
    print("   # CUIDADO: {} cria dicionário, não set!")
    print("   set_vazio = set()        # ✅ Correto")
    print("   dict_vazio = {}          # ❌ Isso é um dicionário!")
    print()
    
    set_vazio = set()
    dict_vazio = {}
    
    print(f"   → set_vazio: {set_vazio} (tipo: {type(set_vazio)})")
    print(f"   → dict_vazio: {dict_vazio} (tipo: {type(dict_vazio)})")
    print()
    
    print("2. CRIANDO CONJUNTOS COM ELEMENTOS:")
    print("   # Sintaxe literal")
    print("   numeros = {1, 2, 3, 4, 5}")
    print("   cores = {'vermelho', 'verde', 'azul'}")
    print()
    
    numeros = {1, 2, 3, 4, 5}
    cores = {'vermelho', 'verde', 'azul'}
    
    print(f"   → numeros: {numeros}")
    print(f"   → cores: {cores}")
    print()
    
    print("3. CRIANDO A PARTIR DE ITERÁVEIS:")
    print("   # De lista")
    print("   lista = [1, 2, 2, 3, 3, 3, 4]")
    print("   set_da_lista = set(lista)")
    lista = [1, 2, 2, 3, 3, 3, 4]
    set_da_lista = set(lista)
    print(f"   → {set_da_lista}")
    print()
    
    print("   # De string")
    print("   set_chars = set('python')")
    set_chars = set('python')
    print(f"   → {set_chars}")
    print()
    
    print("   # De range")
    print("   set_range = set(range(0, 10, 2))")
    set_range = set(range(0, 10, 2))
    print(f"   → {set_range}")
    print()
    
    print("4. ADICIONANDO ELEMENTOS:")
    frutas = {'maçã', 'banana'}
    print(f"   frutas = {frutas}")
    print()
    
    print("   # add() - adiciona um elemento")
    print("   frutas.add('laranja')")
    frutas.add('laranja')
    print(f"   → {frutas}")
    print()
    
    print("   # Tentando adicionar duplicata")
    print("   frutas.add('maçã')  # Não muda nada")
    frutas.add('maçã')
    print(f"   → {frutas}")
    print()
    
    print("   # update() - adiciona múltiplos elementos")
    print("   frutas.update(['uva', 'pêra', 'kiwi'])")
    frutas.update(['uva', 'pêra', 'kiwi'])
    print(f"   → {frutas}")
    print()
    
    print("   # update() com string")
    print("   letras = {'a', 'b'}")
    print("   letras.update('cde')")
    letras = {'a', 'b'}
    letras.update('cde')
    print(f"   → {letras}")
    print()
    
    print("5. REMOVENDO ELEMENTOS:")
    numeros_teste = {1, 2, 3, 4, 5}
    print(f"   numeros = {numeros_teste}")
    print()
    
    print("   # remove() - remove elemento (erro se não existir)")
    print("   numeros.remove(3)")
    numeros_teste.remove(3)
    print(f"   → {numeros_teste}")
    print()
    
    print("   # discard() - remove elemento (sem erro se não existir)")
    print("   numeros.discard(10)  # Não existe, mas não dá erro")
    numeros_teste.discard(10)
    print(f"   → {numeros_teste}")
    print()
    
    print("   # pop() - remove e retorna elemento aleatório")
    print("   elemento = numeros.pop()")
    elemento = numeros_teste.pop()
    print(f"   → Elemento removido: {elemento}")
    print(f"   → Conjunto após pop: {numeros_teste}")
    print()
    
    print("   # clear() - remove todos os elementos")
    numeros_temp = {7, 8, 9}
    print(f"   Antes do clear: {numeros_temp}")
    numeros_temp.clear()
    print(f"   → Após clear: {numeros_temp}")
    print()
    
    print("6. VERIFICAÇÃO DE PERTENCIMENTO:")
    animais = {'gato', 'cachorro', 'pássaro', 'peixe'}
    print(f"   animais = {animais}")
    print()
    
    print("   # Operador 'in'")
    print(f"   'gato' in animais: {'gato' in animais}")
    print(f"   'cobra' in animais: {'cobra' in animais}")
    print()
    
    print("   # Operador 'not in'")
    print(f"   'cobra' not in animais: {'cobra' not in animais}")
    print()
    
    print("7. OPERAÇÕES DE CÓPIA:")
    original = {1, 2, 3}
    print(f"   original = {original}")
    
    print("   # copy() - cópia superficial")
    copia = original.copy()
    print(f"   copia = original.copy(): {copia}")
    
    print("   # Modificando a cópia")
    copia.add(4)
    print(f"   → Original: {original}")
    print(f"   → Cópia: {copia}")
    print("   → Objetos independentes")
    print()

def operacoes_matematicas():
    """
    Explora operações matemáticas com conjuntos.
    
    Analogia: Operações com conjuntos são como operações
    com grupos de objetos na vida real.
    """
    print("=== OPERAÇÕES MATEMÁTICAS COM CONJUNTOS ===")
    print()
    
    # Conjuntos para demonstração
    A = {1, 2, 3, 4, 5}
    B = {4, 5, 6, 7, 8}
    C = {1, 2, 3}
    
    print(f"   Conjunto A = {A}")
    print(f"   Conjunto B = {B}")
    print(f"   Conjunto C = {C}")
    print()
    
    print("1. UNIÃO (∪) - TODOS OS ELEMENTOS:")
    print("   → Combina elementos de ambos os conjuntos")
    print("   → Remove duplicatas automaticamente")
    print()
    
    print("   # Operador |")
    print("   A | B")
    uniao_op = A | B
    print(f"   → {uniao_op}")
    print()
    
    print("   # Método union()")
    print("   A.union(B)")
    uniao_metodo = A.union(B)
    print(f"   → {uniao_metodo}")
    print()
    
    print("   # União de múltiplos conjuntos")
    print("   A.union(B, C)")
    uniao_multipla = A.union(B, C)
    print(f"   → {uniao_multipla}")
    print()
    
    print("2. INTERSEÇÃO (∩) - ELEMENTOS COMUNS:")
    print("   → Apenas elementos presentes em ambos")
    print()
    
    print("   # Operador &")
    print("   A & B")
    intersecao_op = A & B
    print(f"   → {intersecao_op}")
    print()
    
    print("   # Método intersection()")
    print("   A.intersection(B)")
    intersecao_metodo = A.intersection(B)
    print(f"   → {intersecao_metodo}")
    print()
    
    print("3. DIFERENÇA (-) - ELEMENTOS EXCLUSIVOS:")
    print("   → Elementos do primeiro que não estão no segundo")
    print()
    
    print("   # Operador -")
    print("   A - B")
    diferenca_ab = A - B
    print(f"   → {diferenca_ab}")
    print()
    
    print("   B - A")
    diferenca_ba = B - A
    print(f"   → {diferenca_ba}")
    print()
    
    print("   # Método difference()")
    print("   A.difference(B)")
    diferenca_metodo = A.difference(B)
    print(f"   → {diferenca_metodo}")
    print()
    
    print("4. DIFERENÇA SIMÉTRICA (△) - ELEMENTOS ÚNICOS:")
    print("   → Elementos que estão em um OU outro, mas não em ambos")
    print()
    
    print("   # Operador ^")
    print("   A ^ B")
    diff_simetrica_op = A ^ B
    print(f"   → {diff_simetrica_op}")
    print()
    
    print("   # Método symmetric_difference()")
    print("   A.symmetric_difference(B)")
    diff_simetrica_metodo = A.symmetric_difference(B)
    print(f"   → {diff_simetrica_metodo}")
    print()
    
    print("5. VISUALIZAÇÃO DAS OPERAÇÕES:")
    print("   A = {1, 2, 3, 4, 5}")
    print("   B = {4, 5, 6, 7, 8}")
    print()
    print("   ┌─────────────────────────────────────┐")
    print("   │        DIAGRAMA DE VENN             │")
    print("   │                                     │")
    print("   │    A          B                     │")
    print("   │  ┌─────┬─────┬─────┐                │")
    print("   │  │1,2,3│4,5  │6,7,8│                │")
    print("   │  └─────┴─────┴─────┘                │")
    print("   │                                     │")
    print("   │  União: {1,2,3,4,5,6,7,8}          │")
    print("   │  Interseção: {4,5}                  │")
    print("   │  A - B: {1,2,3}                     │")
    print("   │  B - A: {6,7,8}                     │")
    print("   │  Diferença Simétrica: {1,2,3,6,7,8}│")
    print("   └─────────────────────────────────────┘")
    print()
    
    print("6. OPERAÇÕES DE COMPARAÇÃO:")
    print("   # Subconjunto (⊆)")
    print(f"   C.issubset(A): {C.issubset(A)}")
    print(f"   C <= A: {C <= A}")
    print()
    
    print("   # Subconjunto próprio (⊂)")
    print(f"   C < A: {C < A}")
    print()
    
    print("   # Superconjunto (⊇)")
    print(f"   A.issuperset(C): {A.issuperset(C)}")
    print(f"   A >= C: {A >= C}")
    print()
    
    print("   # Superconjunto próprio (⊃)")
    print(f"   A > C: {A > C}")
    print()
    
    print("   # Conjuntos disjuntos (sem elementos comuns)")
    D = {10, 11, 12}
    print(f"   D = {D}")
    print(f"   A.isdisjoint(D): {A.isdisjoint(D)}")
    print()
    
    print("7. OPERAÇÕES IN-PLACE (MODIFICAM O CONJUNTO):")
    teste = {1, 2, 3}
    print(f"   teste = {teste}")
    print()
    
    print("   # |= (union update)")
    print("   teste |= {4, 5}")
    teste |= {4, 5}
    print(f"   → {teste}")
    print()
    
    print("   # &= (intersection update)")
    print("   teste &= {2, 3, 4}")
    teste &= {2, 3, 4}
    print(f"   → {teste}")
    print()
    
    print("   # -= (difference update)")
    print("   teste -= {4}")
    teste -= {4}
    print(f"   → {teste}")
    print()
    
    print("   # ^= (symmetric difference update)")
    print("   teste ^= {1, 5}")
    teste ^= {1, 5}
    print(f"   → {teste}")
    print()

def set_comprehensions():
    """
    Explora set comprehensions - forma concisa de criar conjuntos.
    
    Analogia: Set comprehensions são como filtros automáticos
    que criam coleções únicas seguindo regras específicas.
    """
    print("=== SET COMPREHENSIONS ===")
    print()
    
    print("1. SINTAXE BÁSICA:")
    print("   {expressão for item in iterável}")
    print("   {expressão for item in iterável if condição}")
    print()
    
    print("2. EXEMPLOS BÁSICOS:")
    print("   # Quadrados dos números")
    print("   quadrados = {x**2 for x in range(1, 6)}")
    quadrados = {x**2 for x in range(1, 6)}
    print(f"   → {quadrados}")
    print()
    
    print("   # Caracteres únicos de uma string")
    print("   chars = {char.upper() for char in 'python'}")
    chars = {char.upper() for char in 'python'}
    print(f"   → {chars}")
    print()
    
    print("3. COM CONDIÇÕES:")
    print("   # Apenas números pares")
    print("   pares = {x for x in range(20) if x % 2 == 0}")
    pares = {x for x in range(20) if x % 2 == 0}
    print(f"   → {pares}")
    print()
    
    print("   # Vogais de uma frase")
    print("   frase = 'Python é uma linguagem incrível'")
    print("   vogais = {char.lower() for char in frase if char.lower() in 'aeiou'}")
    frase = 'Python é uma linguagem incrível'
    vogais = {char.lower() for char in frase if char.lower() in 'aeiou'}
    print(f"   → {vogais}")
    print()
    
    print("4. PROCESSAMENTO DE LISTAS:")
    print("   # Removendo duplicatas e aplicando transformação")
    numeros_duplicados = [1, 2, 2, 3, 3, 4, 4, 5]
    print(f"   numeros = {numeros_duplicados}")
    print("   cubos_unicos = {x**3 for x in numeros}")
    cubos_unicos = {x**3 for x in numeros_duplicados}
    print(f"   → {cubos_unicos}")
    print()
    
    print("5. TRABALHANDO COM STRINGS:")
    palavras = ['python', 'java', 'javascript', 'python', 'go', 'java']
    print(f"   palavras = {palavras}")
    print()
    
    print("   # Primeiras letras únicas")
    print("   primeiras_letras = {palavra[0].upper() for palavra in palavras}")
    primeiras_letras = {palavra[0].upper() for palavra in palavras}
    print(f"   → {primeiras_letras}")
    print()
    
    print("   # Palavras com mais de 4 caracteres")
    print("   palavras_longas = {palavra for palavra in palavras if len(palavra) > 4}")
    palavras_longas = {palavra for palavra in palavras if len(palavra) > 4}
    print(f"   → {palavras_longas}")
    print()
    
    print("6. OPERAÇÕES MATEMÁTICAS:")
    print("   # Divisores de um número")
    print("   def divisores(n):")
    print("       return {i for i in range(1, n+1) if n % i == 0}")
    
    def divisores(n):
        return {i for i in range(1, n+1) if n % i == 0}
    
    print(f"   → divisores(12): {divisores(12)}")
    print(f"   → divisores(15): {divisores(15)}")
    print()
    
    print("   # Números primos até N")
    print("   def eh_primo(n):")
    print("       return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))")
    print("   primos = {n for n in range(2, 20) if eh_primo(n)}")
    
    def eh_primo(n):
        return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))
    
    primos = {n for n in range(2, 20) if eh_primo(n)}
    print(f"   → {primos}")
    print()
    
    print("7. PROCESSAMENTO DE DADOS:")
    vendas = [
        {'produto': 'notebook', 'categoria': 'eletrônicos'},
        {'produto': 'mouse', 'categoria': 'eletrônicos'},
        {'produto': 'livro', 'categoria': 'educação'},
        {'produto': 'teclado', 'categoria': 'eletrônicos'},
        {'produto': 'curso', 'categoria': 'educação'}
    ]
    
    print("   vendas = [")
    for venda in vendas[:2]:
        print(f"       {venda},")
    print("       ...")
    print("   ]")
    print()
    
    print("   # Categorias únicas")
    print("   categorias = {venda['categoria'] for venda in vendas}")
    categorias = {venda['categoria'] for venda in vendas}
    print(f"   → {categorias}")
    print()
    
    print("   # Produtos da categoria eletrônicos")
    print("   eletronicos = {v['produto'] for v in vendas if v['categoria'] == 'eletrônicos'}")
    eletronicos = {v['produto'] for v in vendas if v['categoria'] == 'eletrônicos'}
    print(f"   → {eletronicos}")
    print()
    
    print("8. COMPARAÇÃO COM MÉTODOS TRADICIONAIS:")
    print("   # Método tradicional")
    print("   resultado_tradicional = set()")
    print("   for x in range(10):")
    print("       if x % 2 == 0:")
    print("           resultado_tradicional.add(x**2)")
    
    resultado_tradicional = set()
    for x in range(10):
        if x % 2 == 0:
            resultado_tradicional.add(x**2)
    
    print("   # Com set comprehension")
    print("   resultado_comprehension = {x**2 for x in range(10) if x % 2 == 0}")
    resultado_comprehension = {x**2 for x in range(10) if x % 2 == 0}
    
    print(f"   → Tradicional: {resultado_tradicional}")
    print(f"   → Comprehension: {resultado_comprehension}")
    print(f"   → Iguais: {resultado_tradicional == resultado_comprehension}")
    print()

def frozenset_conjuntos_imutaveis():
    """
    Explora frozenset - conjuntos imutáveis.
    
    Analogia: frozenset é como uma coleção lacrada,
    onde não se pode adicionar ou remover itens.
    """
    print("=== FROZENSET - CONJUNTOS IMUTÁVEIS ===")
    print()
    
    print("1. O QUE É FROZENSET?")
    print("   → Versão imutável de set")
    print("   → Pode ser usado como chave de dicionário")
    print("   → Pode ser elemento de outro conjunto")
    print("   → Hashable (tem método __hash__)")
    print("   → Suporta todas as operações de consulta")
    print("   → NÃO suporta operações de modificação")
    print()
    
    print("2. CRIANDO FROZENSETS:")
    print("   # A partir de lista")
    print("   fs1 = frozenset([1, 2, 3, 4])")
    fs1 = frozenset([1, 2, 3, 4])
    print(f"   → {fs1}")
    print()
    
    print("   # A partir de string")
    print("   fs2 = frozenset('python')")
    fs2 = frozenset('python')
    print(f"   → {fs2}")
    print()
    
    print("   # Frozenset vazio")
    print("   fs_vazio = frozenset()")
    fs_vazio = frozenset()
    print(f"   → {fs_vazio}")
    print()
    
    print("3. DIFERENÇAS COM SET NORMAL:")
    set_normal = {1, 2, 3}
    fs_imutavel = frozenset([1, 2, 3])
    
    print(f"   set_normal = {set_normal}")
    print(f"   fs_imutavel = {fs_imutavel}")
    print()
    
    print("   # Operações permitidas em ambos:")
    print(f"   2 in set_normal: {2 in set_normal}")
    print(f"   2 in fs_imutavel: {2 in fs_imutavel}")
    print(f"   len(fs_imutavel): {len(fs_imutavel)}")
    print()
    
    print("   # Operações só no set normal:")
    print("   set_normal.add(4)  # ✅ Funciona")
    set_normal.add(4)
    print(f"   → {set_normal}")
    
    print("   # fs_imutavel.add(4)  # ❌ AttributeError")
    print("   → frozenset não tem método add()")
    print()
    
    print("4. FROZENSET COMO CHAVE DE DICIONÁRIO:")
    print("   # frozenset pode ser chave, set não pode")
    
    grupos = {
        frozenset(['ana', 'bruno']): 'Equipe A',
        frozenset(['carlos', 'diana']): 'Equipe B',
        frozenset(['eduardo']): 'Equipe C'
    }
    
    print("   grupos = {")
    for chave, valor in grupos.items():
        print(f"       {chave}: '{valor}',")
    print("   }")
    print()
    
    print("   # Acessando por chave frozenset")
    chave_busca = frozenset(['ana', 'bruno'])
    print(f"   grupos[frozenset(['ana', 'bruno'])]: {grupos[chave_busca]}")
    print()
    
    print("5. FROZENSET EM CONJUNTOS:")
    print("   # frozenset pode ser elemento de set")
    
    conjunto_de_conjuntos = {
        frozenset([1, 2]),
        frozenset([3, 4]),
        frozenset([5, 6])
    }
    
    print("   conjunto_de_conjuntos = {")
    for fs in conjunto_de_conjuntos:
        print(f"       {fs},")
    print("   }")
    print()
    
    print("   # Verificando pertencimento")
    print(f"   frozenset([1, 2]) in conjunto_de_conjuntos: {frozenset([1, 2]) in conjunto_de_conjuntos}")
    print()
    
    print("6. OPERAÇÕES MATEMÁTICAS COM FROZENSET:")
    fs_a = frozenset([1, 2, 3, 4])
    fs_b = frozenset([3, 4, 5, 6])
    
    print(f"   fs_a = {fs_a}")
    print(f"   fs_b = {fs_b}")
    print()
    
    print("   # Todas as operações matemáticas funcionam")
    print(f"   → União: {fs_a | fs_b}")
    print(f"   → Interseção: {fs_a & fs_b}")
    print(f"   → Diferença: {fs_a - fs_b}")
    print(f"   → Diferença simétrica: {fs_a ^ fs_b}")
    print()
    
    print("7. CASOS DE USO PRÁTICOS:")
    print("   # Cache de resultados com chaves complexas")
    
    cache_resultados = {}
    
    def calcular_estatisticas(dados):
        """Calcula estatísticas com cache baseado em frozenset"""
        chave = frozenset(dados)
        
        if chave in cache_resultados:
            print(f"   → Cache hit para {list(dados)[:3]}...")
            return cache_resultados[chave]
        
        # Simulando cálculo pesado
        resultado = {
            'soma': sum(dados),
            'media': sum(dados) / len(dados),
            'max': max(dados),
            'min': min(dados)
        }
        
        cache_resultados[chave] = resultado
        print(f"   → Calculado para {list(dados)[:3]}...")
        return resultado
    
    # Testando o cache
    dados1 = [1, 2, 3, 4, 5]
    dados2 = [5, 4, 3, 2, 1]  # Mesmos elementos, ordem diferente
    
    print("   # Primeira chamada")
    resultado1 = calcular_estatisticas(dados1)
    
    print("   # Segunda chamada com mesmos dados (ordem diferente)")
    resultado2 = calcular_estatisticas(dados2)
    
    print(f"   → Resultados iguais: {resultado1 == resultado2}")
    print(f"   → Entradas no cache: {len(cache_resultados)}")
    print()
    
    print("8. PERFORMANCE E HASHABILIDADE:")
    
    # Teste de hashabilidade
    print("   # Testando hashabilidade")
    try:
        hash_fs = hash(fs1)
        print(f"   → hash(frozenset): {hash_fs}")
    except TypeError as e:
        print(f"   → Erro: {e}")
    
    try:
        hash_set = hash(set_normal)
        print(f"   → hash(set): {hash_set}")
    except TypeError as e:
        print(f"   → Erro ao fazer hash de set: {e}")
    
    print()

def casos_uso_praticos():
    """
    Demonstra casos de uso práticos para conjuntos.
    """
    print("=== CASOS DE USO PRÁTICOS ===")
    print()
    
    print("Caso 1: Sistema de Permissões")
    
    def sistema_permissoes():
        """Sistema de controle de acesso baseado em conjuntos"""
        
        # Definindo permissões por papel
        permissoes = {
            'admin': {'criar', 'ler', 'atualizar', 'deletar', 'gerenciar_usuarios'},
            'editor': {'criar', 'ler', 'atualizar'},
            'viewer': {'ler'},
            'moderador': {'ler', 'atualizar', 'moderar_conteudo'}
        }
        
        # Usuários e seus papéis
        usuarios = {
            'alice': {'admin'},
            'bob': {'editor', 'moderador'},
            'charlie': {'viewer'},
            'diana': {'editor'}
        }
        
        def obter_permissoes_usuario(usuario):
            """Obtém todas as permissões de um usuário"""
            papeis = usuarios.get(usuario, set())
            permissoes_usuario = set()
            
            for papel in papeis:
                permissoes_usuario |= permissoes.get(papel, set())
            
            return permissoes_usuario
        
        def pode_executar(usuario, acao):
            """Verifica se usuário pode executar uma ação"""
            return acao in obter_permissoes_usuario(usuario)
        
        # Demonstração
        print("   SISTEMA DE PERMISSÕES:")
        for usuario in usuarios:
            perms = obter_permissoes_usuario(usuario)
            print(f"   → {usuario}: {perms}")
        
        print()
        print("   VERIFICAÇÕES:")
        print(f"   → Alice pode deletar: {pode_executar('alice', 'deletar')}")
        print(f"   → Bob pode moderar: {pode_executar('bob', 'moderar_conteudo')}")
        print(f"   → Charlie pode criar: {pode_executar('charlie', 'criar')}")
        print()
        
        return permissoes, usuarios
    
    sistema_permissoes()
    
    print("Caso 2: Análise de Dados de Vendas")
    
    def analise_vendas():
        """Análise de padrões de compra usando conjuntos"""
        
        # Dados de compras (cliente: produtos comprados)
        compras = {
            'cliente_1': {'notebook', 'mouse', 'teclado'},
            'cliente_2': {'smartphone', 'fone', 'carregador'},
            'cliente_3': {'notebook', 'mouse', 'monitor'},
            'cliente_4': {'tablet', 'caneta_digital', 'capa'},
            'cliente_5': {'notebook', 'teclado', 'monitor'},
            'cliente_6': {'smartphone', 'fone', 'powerbank'}
        }
        
        print("   ANÁLISE DE VENDAS:")
        print("   Produtos por cliente:")
        for cliente, produtos in list(compras.items())[:3]:
            print(f"   → {cliente}: {produtos}")
        print("   ...")
        print()
        
        # Todos os produtos vendidos
        todos_produtos = set()
        for produtos in compras.values():
            todos_produtos |= produtos
        
        print(f"   → Total de produtos únicos: {len(todos_produtos)}")
        print(f"   → Produtos: {todos_produtos}")
        print()
        
        # Produtos mais populares
        contador_produtos = {}
        for produtos in compras.values():
            for produto in produtos:
                contador_produtos[produto] = contador_produtos.get(produto, 0) + 1
        
        produtos_populares = sorted(contador_produtos.items(), 
                                  key=lambda x: x[1], reverse=True)[:3]
        
        print("   → Top 3 produtos mais vendidos:")
        for produto, qtd in produtos_populares:
            print(f"     {produto}: {qtd} vendas")
        print()
        
        # Clientes com compras similares
        print("   → Clientes com produtos em comum:")
        clientes = list(compras.keys())
        for i in range(len(clientes)):
            for j in range(i+1, len(clientes)):
                cliente1, cliente2 = clientes[i], clientes[j]
                produtos_comuns = compras[cliente1] & compras[cliente2]
                if produtos_comuns:
                    print(f"     {cliente1} e {cliente2}: {produtos_comuns}")
        print()
        
        return compras, todos_produtos
    
    analise_vendas()
    
    print("Caso 3: Validador de Dependências")
    
    def validador_dependencias():
        """Sistema para validar dependências de projetos"""
        
        # Dependências de diferentes projetos
        projetos = {
            'projeto_web': {'flask', 'requests', 'sqlalchemy', 'pytest'},
            'projeto_data': {'pandas', 'numpy', 'matplotlib', 'pytest'},
            'projeto_api': {'fastapi', 'requests', 'sqlalchemy', 'uvicorn'},
            'projeto_ml': {'scikit-learn', 'pandas', 'numpy', 'matplotlib'}
        }
        
        # Bibliotecas disponíveis no ambiente
        ambiente_dev = {'flask', 'requests', 'pandas', 'numpy', 'pytest'}
        ambiente_prod = {'flask', 'requests', 'sqlalchemy', 'fastapi', 'uvicorn'}
        
        def verificar_compatibilidade(projeto, ambiente):
            """Verifica se projeto pode rodar no ambiente"""
            deps_projeto = projetos[projeto]
            deps_faltando = deps_projeto - ambiente
            deps_disponiveis = deps_projeto & ambiente
            
            return {
                'compativel': len(deps_faltando) == 0,
                'faltando': deps_faltando,
                'disponiveis': deps_disponiveis,
                'cobertura': len(deps_disponiveis) / len(deps_projeto) * 100
            }
        
        print("   VALIDADOR DE DEPENDÊNCIAS:")
        print()
        
        for projeto in projetos:
            print(f"   {projeto.upper()}:")
            
            # Verificar em desenvolvimento
            resultado_dev = verificar_compatibilidade(projeto, ambiente_dev)
            print(f"   → Desenvolvimento: {'✅' if resultado_dev['compativel'] else '❌'} "
                  f"({resultado_dev['cobertura']:.0f}% cobertura)")
            if resultado_dev['faltando']:
                print(f"     Faltando: {resultado_dev['faltando']}")
            
            # Verificar em produção
            resultado_prod = verificar_compatibilidade(projeto, ambiente_prod)
            print(f"   → Produção: {'✅' if resultado_prod['compativel'] else '❌'} "
                  f"({resultado_prod['cobertura']:.0f}% cobertura)")
            if resultado_prod['faltando']:
                print(f"     Faltando: {resultado_prod['faltando']}")
            print()
        
        # Dependências comuns entre projetos
        print("   DEPENDÊNCIAS COMUNS:")
        deps_comuns = set.intersection(*projetos.values())
        print(f"   → Usadas por todos: {deps_comuns}")
        
        # Dependências únicas
        print("   → Dependências únicas por projeto:")
        for projeto, deps in projetos.items():
            outras_deps = set()
            for outro_proj, outras in projetos.items():
                if outro_proj != projeto:
                    outras_deps |= outras
            
            unicas = deps - outras_deps
            if unicas:
                print(f"     {projeto}: {unicas}")
        print()
        
        return projetos, ambiente_dev, ambiente_prod
    
    validador_dependencias()

if __name__ == "__main__":
    print("MÓDULO 2.4 - CONJUNTOS (SETS) E OPERAÇÕES")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceito_conjuntos()
    print("\n" + "="*50 + "\n")
    
    criacao_manipulacao_sets()
    print("\n" + "="*50 + "\n")
    
    operacoes_matematicas()
    print("\n" + "="*50 + "\n")
    
    set_comprehensions()
    print("\n" + "="*50 + "\n")
    
    frozenset_conjuntos_imutaveis()
    print("\n" + "="*50 + "\n")
    
    casos_uso_praticos()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 2.4 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceito e características de conjuntos")
    print("✅ Criação e manipulação de sets")
    print("✅ Operações matemáticas (união, interseção, diferença)")
    print("✅ Set comprehensions")
    print("✅ frozenset - conjuntos imutáveis")
    print("✅ Casos de uso práticos")
    print("\n➡️  Próximo: Módulo 2.5 - Strings e Manipulação de Texto")