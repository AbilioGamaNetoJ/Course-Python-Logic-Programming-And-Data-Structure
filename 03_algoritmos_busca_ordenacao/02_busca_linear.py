"""
Módulo: Algoritmos de Busca Linear
Tópico: Algoritmos de Busca e Ordenação - Busca Sequencial
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Básico a Intermediário

Objetivos de Aprendizado:
- Compreender o conceito de busca linear
- Implementar diferentes variações de busca linear
- Analisar complexidade temporal e espacial
- Identificar casos de uso apropriados
- Comparar performance com outros algoritmos
- Otimizar implementações básicas
- Aplicar busca linear em problemas reais
- Desenvolver intuição sobre eficiência

Conceitos Abordados:
- Busca sequencial básica
- Busca com sentinela
- Busca de múltiplas ocorrências
- Busca em estruturas aninhadas
- Busca com critérios personalizados
- Otimizações práticas
- Análise de casos extremos
- Comparação de implementações

Pré-requisitos:
- Módulo 3.1 completo
- Conhecimento de listas e loops
- Compreensão de complexidade O(n)
- Familiaridade com funções

Complexidade:
- Temporal: O(n) - linear
- Espacial: O(1) - constante
- Melhor caso: O(1) - elemento no início
- Pior caso: O(n) - elemento no final ou inexistente
"""

import time
import random
from typing import List, Any, Optional, Tuple, Callable
import sys

def conceito_busca_linear():
    """
    Introduz o conceito fundamental de busca linear.
    
    Analogia: Busca linear é como procurar uma palavra específica
    em um dicionário lendo página por página desde o início.
    """
    print("=== CONCEITO DE BUSCA LINEAR ===")
    print()
    
    print("1. DEFINIÇÃO:")
    print("   A busca linear (ou sequencial) é o algoritmo mais simples")
    print("   para encontrar um elemento em uma coleção de dados.")
    print("   Examina cada elemento sequencialmente até encontrar o item")
    print("   procurado ou percorrer toda a estrutura.")
    print()
    
    print("2. CARACTERÍSTICAS:")
    print("   ✅ Simplicidade: Fácil de entender e implementar")
    print("   ✅ Versatilidade: Funciona em qualquer estrutura sequencial")
    print("   ✅ Sem pré-requisitos: Não precisa de dados ordenados")
    print("   ❌ Eficiência: O(n) - pode ser lento para grandes datasets")
    print("   ❌ Escalabilidade: Performance degrada linearmente")
    print()
    
    print("3. ALGORITMO BÁSICO:")
    print("   1. Começar no primeiro elemento")
    print("   2. Comparar elemento atual com o valor procurado")
    print("   3. Se encontrou, retornar posição/elemento")
    print("   4. Se não encontrou, ir para próximo elemento")
    print("   5. Repetir até encontrar ou chegar ao final")
    print("   6. Se chegou ao final, elemento não existe")
    print()
    
    print("4. IMPLEMENTAÇÃO BÁSICA:")
    
    def busca_linear_basica(lista, item):
        """
        Implementação mais simples de busca linear.
        
        Args:
            lista: Lista onde buscar
            item: Item a ser encontrado
            
        Returns:
            int: Índice do item ou -1 se não encontrado
        """
        for i in range(len(lista)):
            if lista[i] == item:
                return i
        return -1
    
    # Demonstração prática
    numeros = [3, 7, 1, 9, 4, 6, 2, 8, 5]
    item_procurado = 6
    
    print(f"   Lista: {numeros}")
    print(f"   Procurando: {item_procurado}")
    
    # Simulando passo a passo
    print("\n   Execução passo a passo:")
    for i, numero in enumerate(numeros):
        print(f"   → Posição {i}: {numero}", end="")
        if numero == item_procurado:
            print(" ✓ ENCONTRADO!")
            break
        else:
            print(" ✗ Continuar...")
    
    resultado = busca_linear_basica(numeros, item_procurado)
    print(f"\n   Resultado: Índice {resultado}")
    print()
    
    print("5. ANÁLISE DE COMPLEXIDADE:")
    
    # Contando operações
    def busca_linear_com_contador(lista, item):
        """Versão que conta operações realizadas"""
        comparacoes = 0
        
        for i in range(len(lista)):
            comparacoes += 1
            if lista[i] == item:
                return i, comparacoes
        
        return -1, comparacoes
    
    # Testando diferentes cenários
    cenarios = [
        ("Melhor caso (início)", numeros, numeros[0]),
        ("Caso médio (meio)", numeros, numeros[len(numeros)//2]),
        ("Pior caso (final)", numeros, numeros[-1]),
        ("Não encontrado", numeros, 99)
    ]
    
    print("   Análise de casos:")
    print("   ┌─────────────────────┬─────────────┬─────────────────┐")
    print("   │       CASO          │ COMPARAÇÕES │   COMPLEXIDADE  │")
    print("   ├─────────────────────┼─────────────┼─────────────────┤")
    
    for nome, lista_teste, item_teste in cenarios:
        pos, comp = busca_linear_com_contador(lista_teste, item_teste)
        complexidade = "O(1)" if comp == 1 else f"O({comp})" if comp < len(lista_teste) else "O(n)"
        print(f"   │ {nome:19} │ {comp:11} │ {complexidade:15} │")
    
    print("   └─────────────────────┴─────────────┴─────────────────┘")
    print()
    
    print("6. VISUALIZAÇÃO DO PROCESSO:")
    
    def visualizar_busca(lista, item):
        """Cria visualização ASCII da busca"""
        print(f"   Buscando {item} em {lista}")
        print("   " + "─" * (len(lista) * 4 + 1))
        
        for i, elemento in enumerate(lista):
            # Mostra estado atual
            linha = "   │"
            for j, num in enumerate(lista):
                if j == i:
                    linha += f" {num}*│"  # Elemento atual
                else:
                    linha += f" {num} │"
            print(linha)
            
            if elemento == item:
                print("   " + "─" * (len(lista) * 4 + 1))
                print(f"   ✓ ENCONTRADO na posição {i}!")
                return i
            
            print("   " + "─" * (len(lista) * 4 + 1))
        
        print("   ✗ NÃO ENCONTRADO")
        return -1
    
    print("   Exemplo visual:")
    lista_visual = [2, 5, 1, 8, 3]
    visualizar_busca(lista_visual, 8)
    print()

def implementacoes_avancadas():
    """
    Apresenta implementações mais sofisticadas de busca linear.
    """
    print("=== IMPLEMENTAÇÕES AVANÇADAS ===")
    print()
    
    print("1. BUSCA COM SENTINELA:")
    print("   Otimização que adiciona o elemento procurado no final")
    print("   da lista para eliminar verificação de limites.")
    print()
    
    def busca_linear_sentinela(lista, item):
        """
        Busca linear com sentinela - otimização clássica.
        
        A sentinela elimina a necessidade de verificar se chegamos
        ao final da lista a cada iteração.
        """
        if not lista:
            return -1
        
        # Salva o último elemento
        ultimo = lista[-1]
        
        # Coloca o item procurado como sentinela
        lista[-1] = item
        
        i = 0
        # Loop sem verificação de limites
        while lista[i] != item:
            i += 1
        
        # Restaura o último elemento
        lista[-1] = ultimo
        
        # Verifica se encontrou antes da sentinela ou se o último era o item
        if i < len(lista) - 1 or ultimo == item:
            return i
        else:
            return -1
    
    # Comparando performance
    lista_teste = list(range(10000))
    item_teste = 7500
    
    # Busca normal
    start = time.perf_counter()
    for _ in range(1000):
        resultado_normal = lista_teste.index(item_teste) if item_teste in lista_teste else -1
    tempo_normal = time.perf_counter() - start
    
    # Busca com sentinela
    start = time.perf_counter()
    for _ in range(1000):
        lista_copia = lista_teste.copy()
        resultado_sentinela = busca_linear_sentinela(lista_copia, item_teste)
    tempo_sentinela = time.perf_counter() - start
    
    print(f"   Teste com lista de 10.000 elementos (1000 execuções):")
    print(f"   → Busca normal: {tempo_normal:.6f}s")
    print(f"   → Busca sentinela: {tempo_sentinela:.6f}s")
    print(f"   → Diferença: {((tempo_normal - tempo_sentinela) / tempo_normal * 100):.1f}%")
    print()
    
    print("2. BUSCA DE MÚLTIPLAS OCORRÊNCIAS:")
    print("   Encontra todas as posições onde o elemento aparece.")
    print()
    
    def busca_todas_ocorrencias(lista, item):
        """
        Encontra todas as posições de um item na lista.
        
        Returns:
            List[int]: Lista com todos os índices onde o item aparece
        """
        posicoes = []
        
        for i, elemento in enumerate(lista):
            if elemento == item:
                posicoes.append(i)
        
        return posicoes
    
    def busca_primeira_ultima(lista, item):
        """
        Encontra primeira e última ocorrência de um item.
        
        Returns:
            Tuple[int, int]: (primeira_posição, última_posição) ou (-1, -1)
        """
        primeira = -1
        ultima = -1
        
        for i, elemento in enumerate(lista):
            if elemento == item:
                if primeira == -1:
                    primeira = i
                ultima = i
        
        return primeira, ultima
    
    # Demonstração
    lista_com_duplicatas = [1, 3, 7, 3, 9, 3, 2, 3, 5]
    item_duplicado = 3
    
    todas_pos = busca_todas_ocorrencias(lista_com_duplicatas, item_duplicado)
    primeira, ultima = busca_primeira_ultima(lista_com_duplicatas, item_duplicado)
    
    print(f"   Lista: {lista_com_duplicatas}")
    print(f"   Procurando: {item_duplicado}")
    print(f"   → Todas as posições: {todas_pos}")
    print(f"   → Primeira ocorrência: {primeira}")
    print(f"   → Última ocorrência: {ultima}")
    print()
    
    print("3. BUSCA COM CRITÉRIO PERSONALIZADO:")
    print("   Usa função personalizada para definir critério de busca.")
    print()
    
    def busca_com_criterio(lista, criterio_func):
        """
        Busca usando função de critério personalizada.
        
        Args:
            lista: Lista onde buscar
            criterio_func: Função que retorna True para elemento desejado
            
        Returns:
            int: Índice do primeiro elemento que satisfaz o critério
        """
        for i, elemento in enumerate(lista):
            if criterio_func(elemento):
                return i
        return -1
    
    def busca_todos_criterio(lista, criterio_func):
        """Encontra todos os elementos que satisfazem o critério"""
        resultados = []
        
        for i, elemento in enumerate(lista):
            if criterio_func(elemento):
                resultados.append((i, elemento))
        
        return resultados
    
    # Exemplos de uso
    numeros = [12, 7, 23, 4, 18, 9, 31, 6, 25]
    
    # Buscar primeiro número par
    primeiro_par = busca_com_criterio(numeros, lambda x: x % 2 == 0)
    
    # Buscar todos os números maiores que 15
    maiores_15 = busca_todos_criterio(numeros, lambda x: x > 15)
    
    # Buscar primeiro número de dois dígitos
    dois_digitos = busca_com_criterio(numeros, lambda x: x >= 10)
    
    print(f"   Lista: {numeros}")
    print(f"   → Primeiro par: índice {primeiro_par} (valor: {numeros[primeiro_par] if primeiro_par != -1 else 'N/A'})")
    print(f"   → Maiores que 15: {maiores_15}")
    print(f"   → Primeiro ≥ 10: índice {dois_digitos} (valor: {numeros[dois_digitos]})")
    print()
    
    print("4. BUSCA EM ESTRUTURAS ANINHADAS:")
    print("   Busca em listas de listas, dicionários, objetos, etc.")
    print()
    
    def busca_em_matriz(matriz, item):
        """
        Busca linear em matriz 2D.
        
        Returns:
            Tuple[int, int]: (linha, coluna) ou (-1, -1) se não encontrado
        """
        for i, linha in enumerate(matriz):
            for j, elemento in enumerate(linha):
                if elemento == item:
                    return i, j
        return -1, -1
    
    def busca_em_dicionarios(lista_dicts, chave, valor):
        """
        Busca em lista de dicionários por chave-valor.
        
        Returns:
            int: Índice do dicionário que contém chave=valor
        """
        for i, dicionario in enumerate(lista_dicts):
            if chave in dicionario and dicionario[chave] == valor:
                return i
        return -1
    
    # Exemplos
    matriz = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    pessoas = [
        {"nome": "Ana", "idade": 25, "cidade": "São Paulo"},
        {"nome": "Bruno", "idade": 30, "cidade": "Rio de Janeiro"},
        {"nome": "Carlos", "idade": 25, "cidade": "Belo Horizonte"}
    ]
    
    pos_matriz = busca_em_matriz(matriz, 5)
    pos_pessoa = busca_em_dicionarios(pessoas, "idade", 25)
    
    print(f"   Matriz 3x3: {matriz}")
    print(f"   → Buscar 5: posição {pos_matriz}")
    print()
    print(f"   Lista de pessoas: {len(pessoas)} registros")
    print(f"   → Primeira pessoa com 25 anos: índice {pos_pessoa}")
    if pos_pessoa != -1:
        print(f"     Nome: {pessoas[pos_pessoa]['nome']}")
    print()

def otimizacoes_praticas():
    """
    Demonstra otimizações práticas para busca linear.
    """
    print("=== OTIMIZAÇÕES PRÁTICAS ===")
    print()
    
    print("1. BUSCA COM PARADA ANTECIPADA:")
    print("   Para listas ordenadas, pode parar quando elemento atual > procurado.")
    print()
    
    def busca_linear_ordenada(lista_ordenada, item):
        """
        Busca linear otimizada para listas ordenadas.
        Pode parar antecipadamente se elemento atual > procurado.
        """
        comparacoes = 0
        
        for i, elemento in enumerate(lista_ordenada):
            comparacoes += 1
            if elemento == item:
                return i, comparacoes
            elif elemento > item:
                # Parada antecipada - elemento não existe
                break
        
        return -1, comparacoes
    
    # Comparação
    lista_ordenada = list(range(0, 1000, 2))  # [0, 2, 4, 6, ..., 998]
    item_inexistente = 501  # Número ímpar que não existe
    
    # Busca normal
    pos_normal, comp_normal = busca_linear_com_contador(lista_ordenada, item_inexistente)
    
    # Busca otimizada
    pos_otimizada, comp_otimizada = busca_linear_ordenada(lista_ordenada, item_inexistente)
    
    print(f"   Lista ordenada de 500 elementos pares")
    print(f"   Procurando: {item_inexistente} (não existe)")
    print(f"   → Busca normal: {comp_normal} comparações")
    print(f"   → Busca otimizada: {comp_otimizada} comparações")
    print(f"   → Economia: {comp_normal - comp_otimizada} comparações ({((comp_normal - comp_otimizada) / comp_normal * 100):.1f}%)")
    print()
    
    print("2. BUSCA COM CACHE/MEMOIZAÇÃO:")
    print("   Armazena resultados de buscas anteriores.")
    print()
    
    class BuscaComCache:
        """
        Implementa busca linear com cache de resultados.
        Útil quando fazemos muitas buscas na mesma lista.
        """
        
        def __init__(self, lista):
            self.lista = lista
            self.cache = {}  # item -> posição
            self.cache_construido = False
        
        def construir_cache(self):
            """Constrói cache completo da lista"""
            self.cache.clear()
            for i, item in enumerate(self.lista):
                if item not in self.cache:
                    self.cache[item] = i
            self.cache_construido = True
        
        def buscar(self, item):
            """Busca com cache"""
            if not self.cache_construido:
                self.construir_cache()
            
            return self.cache.get(item, -1)
        
        def buscar_sem_cache(self, item):
            """Busca tradicional para comparação"""
            for i, elemento in enumerate(self.lista):
                if elemento == item:
                    return i
            return -1
    
    # Teste de performance
    lista_grande = [random.randint(1, 1000) for _ in range(5000)]
    buscador = BuscaComCache(lista_grande)
    
    # Itens para buscar (alguns repetidos)
    itens_busca = [random.choice(lista_grande) for _ in range(100)]
    
    # Busca sem cache
    start = time.perf_counter()
    resultados_sem_cache = [buscador.buscar_sem_cache(item) for item in itens_busca]
    tempo_sem_cache = time.perf_counter() - start
    
    # Busca com cache
    start = time.perf_counter()
    resultados_com_cache = [buscador.buscar(item) for item in itens_busca]
    tempo_com_cache = time.perf_counter() - start
    
    print(f"   Lista de 5.000 elementos, 100 buscas:")
    print(f"   → Sem cache: {tempo_sem_cache:.6f}s")
    print(f"   → Com cache: {tempo_com_cache:.6f}s")
    print(f"   → Speedup: {tempo_sem_cache / tempo_com_cache:.1f}x mais rápido")
    print()
    
    print("3. BUSCA PARALELA (CONCEITUAL):")
    print("   Divide a lista em partes e busca simultaneamente.")
    print()
    
    def busca_linear_dividida(lista, item, num_partes=4):
        """
        Simula busca paralela dividindo a lista em partes.
        (Implementação sequencial para demonstração)
        """
        tamanho_parte = len(lista) // num_partes
        resultados = []
        
        for i in range(num_partes):
            inicio = i * tamanho_parte
            fim = inicio + tamanho_parte if i < num_partes - 1 else len(lista)
            
            # Busca na parte atual
            for j in range(inicio, fim):
                if lista[j] == item:
                    resultados.append(j)
                    break
        
        return resultados[0] if resultados else -1
    
    # Demonstração conceitual
    lista_demo = list(range(100))
    item_demo = 75
    
    resultado_dividida = busca_linear_dividida(lista_demo, item_demo)
    print(f"   Lista de 100 elementos dividida em 4 partes")
    print(f"   Procurando: {item_demo}")
    print(f"   → Resultado: índice {resultado_dividida}")
    print("   → Em implementação real paralela, cada parte seria")
    print("     processada por thread/processo diferente")
    print()
    
    print("4. BUSCA COM HEURÍSTICAS:")
    print("   Usa conhecimento do domínio para otimizar.")
    print()
    
    def busca_com_heuristica_frequencia(lista, item, historico_buscas=None):
        """
        Busca que considera frequência de buscas anteriores.
        Elementos mais buscados são verificados primeiro.
        """
        if historico_buscas is None:
            historico_buscas = {}
        
        # Atualiza histórico
        historico_buscas[item] = historico_buscas.get(item, 0) + 1
        
        # Cria lista de índices ordenada por frequência de busca
        indices_por_frequencia = []
        for i, elemento in enumerate(lista):
            frequencia = historico_buscas.get(elemento, 0)
            indices_por_frequencia.append((i, elemento, frequencia))
        
        # Ordena por frequência (mais frequentes primeiro)
        indices_por_frequencia.sort(key=lambda x: x[2], reverse=True)
        
        # Busca na ordem de frequência
        for i, elemento, freq in indices_por_frequencia:
            if elemento == item:
                return i
        
        return -1
    
    # Simulação
    lista_freq = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    historico = {'c': 10, 'a': 5, 'e': 3}  # 'c' é mais buscado
    
    resultado_heuristica = busca_com_heuristica_frequencia(lista_freq, 'c', historico)
    print(f"   Lista: {lista_freq}")
    print(f"   Histórico de buscas: {historico}")
    print(f"   → Buscar 'c': encontrado no índice {resultado_heuristica}")
    print("   → Heurística: elementos mais buscados são verificados primeiro")
    print()

def casos_uso_praticos():
    """
    Apresenta casos de uso práticos da busca linear.
    """
    print("=== CASOS DE USO PRÁTICOS ===")
    print()
    
    print("1. VALIDAÇÃO DE DADOS:")
    print("   Verificar se valores estão em listas de valores válidos.")
    print()
    
    def validar_entrada(valor, valores_validos):
        """Valida se entrada está na lista de valores permitidos"""
        return valor in valores_validos
    
    def validar_multiplos_campos(dados, validadores):
        """Valida múltiplos campos usando busca linear"""
        erros = []
        
        for campo, valor in dados.items():
            if campo in validadores:
                valores_validos = validadores[campo]
                if not validar_entrada(valor, valores_validos):
                    erros.append(f"Campo '{campo}': valor '{valor}' inválido")
        
        return erros
    
    # Exemplo prático
    dados_usuario = {
        "pais": "Brasil",
        "estado": "SP",
        "categoria": "Premium"
    }
    
    validadores = {
        "pais": ["Brasil", "Argentina", "Chile", "Uruguai"],
        "estado": ["SP", "RJ", "MG", "RS", "PR"],
        "categoria": ["Básico", "Premium", "Enterprise"]
    }
    
    erros = validar_multiplos_campos(dados_usuario, validadores)
    
    print(f"   Dados: {dados_usuario}")
    print(f"   Validação: {'✓ Todos os campos válidos' if not erros else '✗ Erros encontrados'}")
    if erros:
        for erro in erros:
            print(f"   → {erro}")
    print()
    
    print("2. BUSCA EM LOGS E REGISTROS:")
    print("   Encontrar eventos específicos em logs de sistema.")
    print()
    
    def buscar_eventos_log(logs, tipo_evento=None, usuario=None, periodo=None):
        """
        Busca eventos específicos em logs usando critérios múltiplos.
        """
        eventos_encontrados = []
        
        for i, log in enumerate(logs):
            # Verifica todos os critérios
            if tipo_evento and log.get('tipo') != tipo_evento:
                continue
            if usuario and log.get('usuario') != usuario:
                continue
            if periodo:
                inicio, fim = periodo
                if not (inicio <= log.get('timestamp', 0) <= fim):
                    continue
            
            eventos_encontrados.append((i, log))
        
        return eventos_encontrados
    
    # Simulação de logs
    logs_sistema = [
        {"timestamp": 1000, "tipo": "login", "usuario": "ana", "ip": "192.168.1.10"},
        {"timestamp": 1005, "tipo": "acesso", "usuario": "ana", "recurso": "dashboard"},
        {"timestamp": 1010, "tipo": "erro", "usuario": "bruno", "mensagem": "Falha na conexão"},
        {"timestamp": 1015, "tipo": "login", "usuario": "carlos", "ip": "192.168.1.20"},
        {"timestamp": 1020, "tipo": "logout", "usuario": "ana", "duracao": 20}
    ]
    
    # Buscas específicas
    logins = buscar_eventos_log(logs_sistema, tipo_evento="login")
    eventos_ana = buscar_eventos_log(logs_sistema, usuario="ana")
    eventos_periodo = buscar_eventos_log(logs_sistema, periodo=(1005, 1015))
    
    print(f"   Total de logs: {len(logs_sistema)}")
    print(f"   → Eventos de login: {len(logins)}")
    print(f"   → Eventos da Ana: {len(eventos_ana)}")
    print(f"   → Eventos no período 1005-1015: {len(eventos_periodo)}")
    print()
    
    print("3. BUSCA EM INVENTÁRIO/CATÁLOGO:")
    print("   Encontrar produtos por diferentes critérios.")
    print()
    
    class BuscadorProdutos:
        """Sistema de busca para catálogo de produtos"""
        
        def __init__(self, produtos):
            self.produtos = produtos
        
        def buscar_por_nome(self, nome):
            """Busca produtos por nome (busca parcial)"""
            resultados = []
            nome_lower = nome.lower()
            
            for i, produto in enumerate(self.produtos):
                if nome_lower in produto['nome'].lower():
                    resultados.append((i, produto))
            
            return resultados
        
        def buscar_por_faixa_preco(self, preco_min, preco_max):
            """Busca produtos por faixa de preço"""
            resultados = []
            
            for i, produto in enumerate(self.produtos):
                preco = produto['preco']
                if preco_min <= preco <= preco_max:
                    resultados.append((i, produto))
            
            return resultados
        
        def buscar_por_categoria_e_disponibilidade(self, categoria, disponivel=True):
            """Busca produtos por categoria e disponibilidade"""
            resultados = []
            
            for i, produto in enumerate(self.produtos):
                if (produto['categoria'] == categoria and 
                    produto['disponivel'] == disponivel):
                    resultados.append((i, produto))
            
            return resultados
    
    # Catálogo de exemplo
    produtos = [
        {"nome": "Notebook Dell", "preco": 2500, "categoria": "Eletrônicos", "disponivel": True},
        {"nome": "Mouse Logitech", "preco": 50, "categoria": "Eletrônicos", "disponivel": True},
        {"nome": "Cadeira Gamer", "preco": 800, "categoria": "Móveis", "disponivel": False},
        {"nome": "Monitor Samsung", "preco": 600, "categoria": "Eletrônicos", "disponivel": True},
        {"nome": "Mesa de Escritório", "preco": 400, "categoria": "Móveis", "disponivel": True}
    ]
    
    buscador = BuscadorProdutos(produtos)
    
    # Diferentes tipos de busca
    por_nome = buscador.buscar_por_nome("Dell")
    por_preco = buscador.buscar_por_faixa_preco(100, 1000)
    por_categoria = buscador.buscar_por_categoria_e_disponibilidade("Eletrônicos")
    
    print(f"   Catálogo com {len(produtos)} produtos")
    print(f"   → Produtos com 'Dell': {len(por_nome)}")
    print(f"   → Produtos entre R$ 100-1000: {len(por_preco)}")
    print(f"   → Eletrônicos disponíveis: {len(por_categoria)}")
    print()
    
    print("4. QUANDO USAR BUSCA LINEAR:")
    print()
    
    casos_apropriados = [
        "✅ Listas pequenas (< 100 elementos)",
        "✅ Dados não ordenados",
        "✅ Busca única ou poucas buscas",
        "✅ Estruturas que não suportam indexação",
        "✅ Quando simplicidade é prioridade",
        "✅ Busca com critérios complexos",
        "✅ Primeira implementação (prototipagem)"
    ]
    
    casos_inadequados = [
        "❌ Listas muito grandes (> 10.000 elementos)",
        "❌ Muitas buscas repetitivas",
        "❌ Dados já ordenados (use busca binária)",
        "❌ Performance crítica",
        "❌ Quando há alternativas mais eficientes disponíveis"
    ]
    
    print("   CASOS APROPRIADOS:")
    for caso in casos_apropriados:
        print(f"   {caso}")
    
    print("\n   CASOS INADEQUADOS:")
    for caso in casos_inadequados:
        print(f"   {caso}")
    print()

if __name__ == "__main__":
    print("MÓDULO 3.2 - ALGORITMOS DE BUSCA LINEAR")
    print("=" * 50)
    print()
    
    # Executando todas as seções
    conceito_busca_linear()
    print("\n" + "="*50 + "\n")
    
    implementacoes_avancadas()
    print("\n" + "="*50 + "\n")
    
    otimizacoes_praticas()
    print("\n" + "="*50 + "\n")
    
    casos_uso_praticos()
    print("\n" + "="*50 + "\n")
    
    print("🎓 MÓDULO 3.2 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Conceito e implementação de busca linear")
    print("✅ Análise de complexidade O(n)")
    print("✅ Implementações avançadas (sentinela, múltiplas ocorrências)")
    print("✅ Busca com critérios personalizados")
    print("✅ Otimizações práticas (cache, parada antecipada)")
    print("✅ Casos de uso reais e apropriados")
    print("✅ Comparação de performance entre variações")
    print("\n➡️  Próximo: Módulo 3.3 - Algoritmos de Busca Binária")