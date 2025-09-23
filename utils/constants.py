"""
Constants - Constantes Globais do Projeto

Este módulo centraliza todas as constantes utilizadas no curso de
Lógica de Programação e Estruturas de Dados, organizadas por categorias
para facilitar manutenção e reutilização.

Categorias de constantes:
1. Tamanhos de teste para algoritmos
2. Cores para terminal
3. Mensagens de erro padronizadas
4. Configurações padrão
5. Limites e thresholds
6. Formatos e templates
7. Códigos de status

Autor: Professor de Lógica de Programação
Data: 2024
"""

from typing import Dict, List, Tuple, Any
from enum import Enum


# ============================================================================
# TAMANHOS DE TESTE PARA ALGORITMOS
# ============================================================================

# Tamanhos pequenos para testes rápidos
TAMANHOS_PEQUENOS = [10, 50, 100, 500]

# Tamanhos médios para análise de performance
TAMANHOS_MEDIOS = [1000, 5000, 10000, 50000]

# Tamanhos grandes para benchmarks
TAMANHOS_GRANDES = [100000, 500000, 1000000]

# Conjunto completo de tamanhos de teste
TAMANHOS_TESTE = TAMANHOS_PEQUENOS + TAMANHOS_MEDIOS + TAMANHOS_GRANDES

# Tamanhos específicos para diferentes tipos de estruturas
TAMANHOS_ARVORES = [100, 500, 1000, 5000, 10000]
TAMANHOS_GRAFOS = [50, 100, 500, 1000, 2000]
TAMANHOS_STRINGS = [100, 1000, 10000, 100000]


# ============================================================================
# CORES PARA TERMINAL (ANSI ESCAPE CODES)
# ============================================================================

class Cores:
    """Códigos de cores ANSI para terminal."""
    
    # Cores básicas
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Cores de texto
    PRETO = '\033[30m'
    VERMELHO = '\033[31m'
    VERDE = '\033[32m'
    AMARELO = '\033[33m'
    AZUL = '\033[34m'
    MAGENTA = '\033[35m'
    CIANO = '\033[36m'
    BRANCO = '\033[37m'
    
    # Cores de fundo
    FUNDO_PRETO = '\033[40m'
    FUNDO_VERMELHO = '\033[41m'
    FUNDO_VERDE = '\033[42m'
    FUNDO_AMARELO = '\033[43m'
    FUNDO_AZUL = '\033[44m'
    FUNDO_MAGENTA = '\033[45m'
    FUNDO_CIANO = '\033[46m'
    FUNDO_BRANCO = '\033[47m'
    
    # Cores especiais para diferentes tipos de output
    SUCESSO = VERDE
    ERRO = VERMELHO
    AVISO = AMARELO
    INFO = AZUL
    DEBUG = MAGENTA
    TITULO = BOLD + AZUL
    SUBTITULO = BOLD + CIANO


# Dicionário de cores para fácil acesso
CORES_TERMINAL = {
    'reset': Cores.RESET,
    'bold': Cores.BOLD,
    'sucesso': Cores.SUCESSO,
    'erro': Cores.ERRO,
    'aviso': Cores.AVISO,
    'info': Cores.INFO,
    'titulo': Cores.TITULO,
    'subtitulo': Cores.SUBTITULO
}


# ============================================================================
# MENSAGENS DE ERRO PADRONIZADAS
# ============================================================================

MENSAGENS_ERRO = {
    # Erros de validação
    'lista_vazia': "Lista não pode estar vazia",
    'lista_invalida': "Objeto fornecido não é uma lista válida",
    'indice_invalido': "Índice fora dos limites da lista",
    'tipo_invalido': "Tipo de dado inválido para esta operação",
    'valor_negativo': "Valor não pode ser negativo",
    'valor_zero': "Valor não pode ser zero",
    'divisao_zero': "Divisão por zero não é permitida",
    
    # Erros de estruturas de dados
    'pilha_vazia': "Operação inválida: pilha está vazia",
    'fila_vazia': "Operação inválida: fila está vazia",
    'arvore_vazia': "Operação inválida: árvore está vazia",
    'no_nao_encontrado': "Nó não encontrado na estrutura",
    'chave_duplicada': "Chave já existe na estrutura",
    'chave_nao_encontrada': "Chave não encontrada na estrutura",
    
    # Erros de algoritmos
    'algoritmo_nao_convergiu': "Algoritmo não convergiu no número máximo de iterações",
    'dados_insuficientes': "Dados insuficientes para executar o algoritmo",
    'parametros_invalidos': "Parâmetros fornecidos são inválidos",
    'memoria_insuficiente': "Memória insuficiente para executar a operação",
    
    # Erros de arquivo/sistema
    'arquivo_nao_encontrado': "Arquivo não encontrado",
    'permissao_negada': "Permissão negada para acessar o recurso",
    'espaco_insuficiente': "Espaço em disco insuficiente",
    'timeout': "Operação excedeu o tempo limite"
}


# ============================================================================
# CONFIGURAÇÕES PADRÃO
# ============================================================================

CONFIGURACOES_DEFAULT = {
    # Configurações de performance
    'max_iteracoes': 10000,
    'timeout_segundos': 30,
    'memoria_max_mb': 512,
    'threads_max': 4,
    
    # Configurações de exibição
    'precisao_decimal': 3,
    'largura_terminal': 80,
    'max_items_exibir': 20,
    'truncar_strings': True,
    'tamanho_max_string': 50,
    
    # Configurações de teste
    'seed_random': 42,
    'repeticoes_benchmark': 5,
    'aquecimento_iteracoes': 3,
    'coleta_garbage': True,
    
    # Configurações de logging
    'nivel_log': 'INFO',
    'formato_timestamp': '%Y-%m-%d %H:%M:%S',
    'arquivo_log': 'curso_python.log',
    'rotacao_log': True,
    'tamanho_max_log_mb': 10
}


# ============================================================================
# LIMITES E THRESHOLDS
# ============================================================================

# Limites de complexidade
LIMITE_COMPLEXIDADE_O1 = 1
LIMITE_COMPLEXIDADE_OLOG_N = 100000
LIMITE_COMPLEXIDADE_ON = 50000
LIMITE_COMPLEXIDADE_ON2 = 5000
LIMITE_COMPLEXIDADE_ON3 = 500

# Thresholds para escolha de algoritmos
THRESHOLD_INSERTION_SORT = 10  # Usar insertion sort para listas pequenas
THRESHOLD_QUICKSORT_PIVOT = 3  # Mediana de 3 para quicksort
THRESHOLD_MERGE_SORT_MEMORIA = 1000000  # Limite de memória para merge sort

# Limites de estruturas de dados
MAX_PROFUNDIDADE_RECURSAO = 1000
MAX_TAMANHO_CACHE = 1000
MAX_ELEMENTOS_HASH_TABLE = 1000000
MAX_NOS_ARVORE = 100000

# Thresholds de performance
TEMPO_LIMITE_OPERACAO_MS = 1000
MEMORIA_LIMITE_OPERACAO_MB = 100
CPU_LIMITE_PERCENTUAL = 80


# ============================================================================
# FORMATOS E TEMPLATES
# ============================================================================

# Formatos de saída
FORMATO_TEMPO = "{:.3f}s"
FORMATO_MEMORIA = "{:.1f}MB"
FORMATO_PERCENTUAL = "{:.1f}%"
FORMATO_NUMERO_GRANDE = "{:,}"

# Templates de relatório
TEMPLATE_CABECALHO = """
{'=' * 60}
{titulo.center(60)}
{'=' * 60}
"""

TEMPLATE_SECAO = """
{'-' * 40}
{titulo}
{'-' * 40}
"""

TEMPLATE_RESULTADO_BENCHMARK = """
Algoritmo: {nome}
Tamanho: {tamanho:,} elementos
Tempo: {tempo}
Memória: {memoria}
Comparações: {comparacoes:,}
Trocas: {trocas:,}
"""

TEMPLATE_ANALISE_COMPLEXIDADE = """
Análise de Complexidade:
- Melhor caso: O({melhor})
- Caso médio: O({medio})
- Pior caso: O({pior})
- Complexidade espacial: O({espaco})
"""


# ============================================================================
# CÓDIGOS DE STATUS E ESTADOS
# ============================================================================

class StatusExecucao(Enum):
    """Estados possíveis de execução."""
    PENDENTE = "pendente"
    EXECUTANDO = "executando"
    CONCLUIDO = "concluido"
    ERRO = "erro"
    CANCELADO = "cancelado"
    TIMEOUT = "timeout"


class TipoComplexidade(Enum):
    """Tipos de complexidade algorítmica."""
    O1 = "O(1)"
    OLOG_N = "O(log n)"
    ON = "O(n)"
    ON_LOG_N = "O(n log n)"
    ON2 = "O(n²)"
    ON3 = "O(n³)"
    O2N = "O(2^n)"
    ON_FACTORIAL = "O(n!)"


class TipoEstrutura(Enum):
    """Tipos de estruturas de dados."""
    LISTA = "lista"
    PILHA = "pilha"
    FILA = "fila"
    DEQUE = "deque"
    ARVORE = "arvore"
    GRAFO = "grafo"
    HASH_TABLE = "hash_table"
    HEAP = "heap"


class TipoAlgoritmo(Enum):
    """Tipos de algoritmos."""
    ORDENACAO = "ordenacao"
    BUSCA = "busca"
    GRAFO = "grafo"
    DINAMICA = "programacao_dinamica"
    GULOSO = "guloso"
    DIVIDIR_CONQUISTAR = "dividir_conquistar"
    BACKTRACKING = "backtracking"


# ============================================================================
# CONFIGURAÇÕES ESPECÍFICAS POR MÓDULO
# ============================================================================

# Configurações para algoritmos de ordenação
CONFIG_ORDENACAO = {
    'bubble_sort': {'max_elementos': 1000, 'otimizado': True},
    'insertion_sort': {'max_elementos': 5000, 'busca_binaria': False},
    'selection_sort': {'max_elementos': 1000, 'min_max': False},
    'merge_sort': {'max_elementos': 1000000, 'in_place': False},
    'quick_sort': {'max_elementos': 1000000, 'pivot': 'mediana_3'},
    'heap_sort': {'max_elementos': 1000000, 'max_heap': True},
    'radix_sort': {'max_elementos': 1000000, 'base': 10}
}

# Configurações para algoritmos de busca
CONFIG_BUSCA = {
    'linear': {'max_elementos': 100000, 'early_stop': True},
    'binaria': {'max_elementos': 10000000, 'recursiva': False},
    'interpolacao': {'max_elementos': 1000000, 'distribuicao_uniforme': True},
    'exponencial': {'max_elementos': 1000000, 'base': 2},
    'ternaria': {'max_elementos': 1000000, 'recursiva': True}
}

# Configurações para estruturas de dados
CONFIG_ESTRUTURAS = {
    'lista_ligada': {'cache_tamanho': True, 'dupla_ligacao': False},
    'arvore_binaria': {'balanceamento': 'avl', 'max_profundidade': 50},
    'hash_table': {'fator_carga': 0.75, 'redimensionamento': True},
    'heap': {'tipo': 'max', 'array_based': True},
    'grafo': {'representacao': 'lista_adjacencia', 'direcionado': False}
}


# ============================================================================
# MENSAGENS DE AJUDA E DOCUMENTAÇÃO
# ============================================================================

MENSAGENS_AJUDA = {
    'uso_geral': """
    Este é um curso interativo de Lógica de Programação e Estruturas de Dados.
    
    Comandos disponíveis:
    - help: Exibe esta mensagem
    - list: Lista todos os módulos disponíveis
    - run <modulo>: Executa um módulo específico
    - test <modulo>: Executa testes de um módulo
    - benchmark <algoritmo>: Executa benchmark de um algoritmo
    """,
    
    'modulos_disponiveis': """
    Módulos do curso:
    1. Fundamentos de Lógica
    2. Estruturas de Dados Nativas
    3. Algoritmos de Busca e Ordenação
    4. Estruturas de Dados Lineares
    5. Estruturas de Dados Não-Lineares
    6. Análise de Complexidade
    7. Algoritmos Avançados
    8. Projetos Práticos
    """,
    
    'dicas_performance': """
    Dicas para melhor performance:
    - Use estruturas de dados apropriadas para cada caso
    - Considere a complexidade temporal e espacial
    - Implemente algoritmos iterativos quando possível
    - Use cache para operações custosas
    - Monitore o uso de memória
    """
}


# ============================================================================
# DADOS DE EXEMPLO PARA TESTES
# ============================================================================

# Listas de exemplo para diferentes cenários
LISTAS_EXEMPLO = {
    'pequena': [3, 1, 4, 1, 5, 9, 2, 6],
    'ordenada': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'reversa': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    'duplicatas': [1, 3, 2, 3, 4, 2, 5, 1, 3],
    'unico_elemento': [42],
    'vazia': []
}

# Strings de exemplo para algoritmos de string
STRINGS_EXEMPLO = {
    'palindromo': "arara",
    'texto_simples': "hello world",
    'texto_complexo': "The quick brown fox jumps over the lazy dog",
    'numeros': "123456789",
    'especiais': "!@#$%^&*()",
    'mista': "Abc123!@#"
}

# Grafos de exemplo
GRAFOS_EXEMPLO = {
    'simples': {
        'vertices': ['A', 'B', 'C', 'D'],
        'arestas': [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')]
    },
    'completo_4': {
        'vertices': ['A', 'B', 'C', 'D'],
        'arestas': [('A', 'B'), ('A', 'C'), ('A', 'D'), 
                   ('B', 'C'), ('B', 'D'), ('C', 'D')]
    },
    'arvore': {
        'vertices': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'arestas': [('A', 'B'), ('A', 'C'), ('B', 'D'), 
                   ('B', 'E'), ('C', 'F'), ('C', 'G')]
    }
}


# ============================================================================
# FUNÇÕES AUXILIARES PARA CONSTANTES
# ============================================================================

def obter_config_algoritmo(nome_algoritmo: str) -> Dict[str, Any]:
    """
    Obtém configuração específica de um algoritmo.
    
    Args:
        nome_algoritmo: Nome do algoritmo
        
    Returns:
        Dicionário com configurações
    """
    configs = {**CONFIG_ORDENACAO, **CONFIG_BUSCA}
    return configs.get(nome_algoritmo, {})


def obter_limite_complexidade(complexidade: TipoComplexidade) -> int:
    """
    Obtém limite recomendado para um tipo de complexidade.
    
    Args:
        complexidade: Tipo de complexidade
        
    Returns:
        Limite recomendado de elementos
    """
    limites = {
        TipoComplexidade.O1: LIMITE_COMPLEXIDADE_O1,
        TipoComplexidade.OLOG_N: LIMITE_COMPLEXIDADE_OLOG_N,
        TipoComplexidade.ON: LIMITE_COMPLEXIDADE_ON,
        TipoComplexidade.ON2: LIMITE_COMPLEXIDADE_ON2,
        TipoComplexidade.ON3: LIMITE_COMPLEXIDADE_ON3
    }
    return limites.get(complexidade, 1000)


def formatar_com_cor(texto: str, cor: str) -> str:
    """
    Formata texto com cor ANSI.
    
    Args:
        texto: Texto a ser formatado
        cor: Nome da cor
        
    Returns:
        Texto formatado com cor
    """
    cor_code = CORES_TERMINAL.get(cor, '')
    reset_code = CORES_TERMINAL.get('reset', '')
    return f"{cor_code}{texto}{reset_code}"


def obter_exemplo_dados(tipo: str, nome: str = None) -> Any:
    """
    Obtém dados de exemplo para testes.
    
    Args:
        tipo: Tipo de dados ('lista', 'string', 'grafo')
        nome: Nome específico do exemplo
        
    Returns:
        Dados de exemplo
    """
    exemplos = {
        'lista': LISTAS_EXEMPLO,
        'string': STRINGS_EXEMPLO,
        'grafo': GRAFOS_EXEMPLO
    }
    
    if tipo not in exemplos:
        return None
    
    if nome:
        return exemplos[tipo].get(nome)
    else:
        return exemplos[tipo]


# ============================================================================
# VALIDAÇÃO DE CONSTANTES
# ============================================================================

def validar_constantes():
    """
    Valida se todas as constantes estão definidas corretamente.
    
    Returns:
        True se todas as constantes são válidas
    """
    try:
        # Verificar se tamanhos de teste são válidos
        assert all(isinstance(t, int) and t > 0 for t in TAMANHOS_TESTE)
        
        # Verificar se configurações têm valores válidos
        assert CONFIGURACOES_DEFAULT['max_iteracoes'] > 0
        assert CONFIGURACOES_DEFAULT['timeout_segundos'] > 0
        assert CONFIGURACOES_DEFAULT['precisao_decimal'] >= 0
        
        # Verificar se limites são consistentes
        assert LIMITE_COMPLEXIDADE_ON2 < LIMITE_COMPLEXIDADE_ON
        assert THRESHOLD_INSERTION_SORT > 0
        
        return True
        
    except (AssertionError, KeyError, TypeError):
        return False


if __name__ == "__main__":
    # Teste das constantes
    print("=== TESTE DAS CONSTANTES ===")
    print()
    
    print("1. TAMANHOS DE TESTE:")
    print(f"   Pequenos: {TAMANHOS_PEQUENOS}")
    print(f"   Médios: {TAMANHOS_MEDIOS}")
    print(f"   Grandes: {TAMANHOS_GRANDES}")
    
    print("\n2. CONFIGURAÇÕES:")
    for chave, valor in list(CONFIGURACOES_DEFAULT.items())[:5]:
        print(f"   {chave}: {valor}")
    
    print("\n3. CORES:")
    print(f"   {formatar_com_cor('SUCESSO', 'sucesso')}")
    print(f"   {formatar_com_cor('ERRO', 'erro')}")
    print(f"   {formatar_com_cor('AVISO', 'aviso')}")
    
    print("\n4. EXEMPLOS:")
    print(f"   Lista pequena: {obter_exemplo_dados('lista', 'pequena')}")
    print(f"   String palindromo: {obter_exemplo_dados('string', 'palindromo')}")
    
    print(f"\n5. VALIDAÇÃO: {'✓ PASSOU' if validar_constantes() else '✗ FALHOU'}")
    
    print("\n=== TESTE CONCLUÍDO ===")