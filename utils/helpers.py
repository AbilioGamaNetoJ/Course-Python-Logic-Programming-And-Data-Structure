"""
Helpers - Funções Auxiliares Comuns

Este módulo contém funções auxiliares que são utilizadas em múltiplos
módulos do curso, centralizando funcionalidades comuns como formatação,
validação, conversão e geração de dados de teste.

Categorias de funções:
1. Formatação de dados
2. Validação básica
3. Conversão de tipos
4. Geração de dados de teste
5. Cálculos matemáticos auxiliares
6. Manipulação de strings
7. Utilitários de sistema

Autor: Professor de Lógica de Programação
Data: 2024
"""

import time
import random
import string
import sys
import os
from typing import Any, List, Dict, Union, Optional, Tuple
from decimal import Decimal
import math


# ============================================================================
# FORMATAÇÃO DE DADOS
# ============================================================================

def formatar_tempo(segundos: float, precisao: int = 3) -> str:
    """
    Formata tempo em segundos para formato legível.
    
    Args:
        segundos: Tempo em segundos
        precisao: Número de casas decimais
        
    Returns:
        String formatada (ex: "1.234s", "2.5ms", "123μs")
    """
    if segundos >= 1:
        return f"{segundos:.{precisao}f}s"
    elif segundos >= 0.001:
        return f"{segundos * 1000:.{precisao}f}ms"
    elif segundos >= 0.000001:
        return f"{segundos * 1000000:.{precisao}f}μs"
    else:
        return f"{segundos * 1000000000:.{precisao}f}ns"


def formatar_memoria(bytes_: int) -> str:
    """
    Formata tamanho em bytes para formato legível.
    
    Args:
        bytes_: Tamanho em bytes
        
    Returns:
        String formatada (ex: "1.2KB", "3.4MB", "5.6GB")
    """
    if bytes_ < 1024:
        return f"{bytes_}B"
    elif bytes_ < 1024**2:
        return f"{bytes_ / 1024:.1f}KB"
    elif bytes_ < 1024**3:
        return f"{bytes_ / (1024**2):.1f}MB"
    else:
        return f"{bytes_ / (1024**3):.1f}GB"


def formatar_numero(numero: Union[int, float], separador: str = ".") -> str:
    """
    Formata número com separadores de milhares.
    
    Args:
        numero: Número a ser formatado
        separador: Separador de milhares
        
    Returns:
        String formatada (ex: "1.234.567")
    """
    if isinstance(numero, float):
        partes = f"{numero:.2f}".split(".")
        inteira = partes[0]
        decimal = partes[1] if len(partes) > 1 else "00"
    else:
        inteira = str(numero)
        decimal = None
    
    # Adicionar separadores de milhares
    if len(inteira) > 3:
        grupos = []
        for i in range(len(inteira), 0, -3):
            inicio = max(0, i - 3)
            grupos.append(inteira[inicio:i])
        inteira = separador.join(reversed(grupos))
    
    return f"{inteira},{decimal}" if decimal else inteira


def formatar_percentual(valor: float, total: float, precisao: int = 1) -> str:
    """
    Calcula e formata percentual.
    
    Args:
        valor: Valor atual
        total: Valor total
        precisao: Casas decimais
        
    Returns:
        String formatada (ex: "75.5%")
    """
    if total == 0:
        return "0.0%"
    
    percentual = (valor / total) * 100
    return f"{percentual:.{precisao}f}%"


def formatar_lista_legivel(lista: List[Any], max_items: int = 10) -> str:
    """
    Formata lista para exibição legível.
    
    Args:
        lista: Lista a ser formatada
        max_items: Máximo de itens a exibir
        
    Returns:
        String formatada
    """
    if not lista:
        return "[]"
    
    if len(lista) <= max_items:
        return str(lista)
    
    inicio = lista[:max_items//2]
    fim = lista[-max_items//2:]
    meio = f"... ({len(lista) - max_items} itens) ..."
    
    return f"[{', '.join(map(str, inicio))}, {meio}, {', '.join(map(str, fim))}]"


# ============================================================================
# VALIDAÇÃO BÁSICA
# ============================================================================

def validar_lista(obj: Any) -> bool:
    """
    Valida se objeto é uma lista válida.
    
    Args:
        obj: Objeto a ser validado
        
    Returns:
        True se for lista válida
    """
    return isinstance(obj, (list, tuple)) and len(obj) > 0


def validar_numero(obj: Any) -> bool:
    """
    Valida se objeto é um número válido.
    
    Args:
        obj: Objeto a ser validado
        
    Returns:
        True se for número válido
    """
    return isinstance(obj, (int, float)) and not math.isnan(obj) and math.isfinite(obj)


def validar_string_nao_vazia(obj: Any) -> bool:
    """
    Valida se objeto é string não vazia.
    
    Args:
        obj: Objeto a ser validado
        
    Returns:
        True se for string não vazia
    """
    return isinstance(obj, str) and len(obj.strip()) > 0


def validar_range_numerico(valor: Union[int, float], minimo: Union[int, float], 
                          maximo: Union[int, float]) -> bool:
    """
    Valida se valor está dentro do range especificado.
    
    Args:
        valor: Valor a ser validado
        minimo: Valor mínimo (inclusivo)
        maximo: Valor máximo (inclusivo)
        
    Returns:
        True se estiver no range
    """
    return validar_numero(valor) and minimo <= valor <= maximo


# ============================================================================
# CONVERSÃO DE TIPOS
# ============================================================================

def converter_para_lista(obj: Any) -> List[Any]:
    """
    Converte objeto para lista.
    
    Args:
        obj: Objeto a ser convertido
        
    Returns:
        Lista convertida
    """
    if isinstance(obj, list):
        return obj
    elif isinstance(obj, (tuple, set)):
        return list(obj)
    elif isinstance(obj, str):
        return list(obj)
    elif hasattr(obj, '__iter__'):
        return list(obj)
    else:
        return [obj]


def converter_para_numero(obj: Any, tipo: type = float) -> Union[int, float, None]:
    """
    Converte objeto para número.
    
    Args:
        obj: Objeto a ser convertido
        tipo: Tipo de número (int ou float)
        
    Returns:
        Número convertido ou None se inválido
    """
    try:
        if isinstance(obj, str):
            obj = obj.strip().replace(',', '.')
        return tipo(obj)
    except (ValueError, TypeError):
        return None


def converter_para_string_segura(obj: Any) -> str:
    """
    Converte objeto para string de forma segura.
    
    Args:
        obj: Objeto a ser convertido
        
    Returns:
        String convertida
    """
    try:
        return str(obj)
    except Exception:
        return f"<{type(obj).__name__} object>"


# ============================================================================
# GERAÇÃO DE DADOS DE TESTE
# ============================================================================

def gerar_lista_aleatoria(tamanho: int, minimo: int = 1, maximo: int = 1000) -> List[int]:
    """
    Gera lista de números aleatórios.
    
    Args:
        tamanho: Tamanho da lista
        minimo: Valor mínimo
        maximo: Valor máximo
        
    Returns:
        Lista de números aleatórios
    """
    return [random.randint(minimo, maximo) for _ in range(tamanho)]


def gerar_lista_ordenada(tamanho: int, crescente: bool = True) -> List[int]:
    """
    Gera lista ordenada.
    
    Args:
        tamanho: Tamanho da lista
        crescente: Se True, ordem crescente; se False, decrescente
        
    Returns:
        Lista ordenada
    """
    lista = list(range(1, tamanho + 1))
    return lista if crescente else lista[::-1]


def gerar_lista_com_duplicatas(tamanho: int, num_valores_unicos: int = None) -> List[int]:
    """
    Gera lista com valores duplicados.
    
    Args:
        tamanho: Tamanho da lista
        num_valores_unicos: Número de valores únicos (padrão: tamanho//3)
        
    Returns:
        Lista com duplicatas
    """
    if num_valores_unicos is None:
        num_valores_unicos = max(1, tamanho // 3)
    
    valores = list(range(1, num_valores_unicos + 1))
    return [random.choice(valores) for _ in range(tamanho)]


def gerar_string_aleatoria(tamanho: int, incluir_espacos: bool = False) -> str:
    """
    Gera string aleatória.
    
    Args:
        tamanho: Tamanho da string
        incluir_espacos: Se incluir espaços
        
    Returns:
        String aleatória
    """
    caracteres = string.ascii_letters + string.digits
    if incluir_espacos:
        caracteres += " "
    
    return ''.join(random.choice(caracteres) for _ in range(tamanho))


def gerar_dados_teste(tipo: str, tamanho: int, **kwargs) -> Any:
    """
    Gera dados de teste baseado no tipo especificado.
    
    Args:
        tipo: Tipo de dados ('lista', 'ordenada', 'duplicatas', 'string')
        tamanho: Tamanho dos dados
        **kwargs: Argumentos adicionais específicos do tipo
        
    Returns:
        Dados de teste gerados
    """
    if tipo == 'lista':
        return gerar_lista_aleatoria(tamanho, **kwargs)
    elif tipo == 'ordenada':
        return gerar_lista_ordenada(tamanho, **kwargs)
    elif tipo == 'duplicatas':
        return gerar_lista_com_duplicatas(tamanho, **kwargs)
    elif tipo == 'string':
        return gerar_string_aleatoria(tamanho, **kwargs)
    else:
        raise ValueError(f"Tipo de dados não suportado: {tipo}")


# ============================================================================
# CÁLCULOS MATEMÁTICOS AUXILIARES
# ============================================================================

def calcular_percentual(parte: Union[int, float], total: Union[int, float]) -> float:
    """
    Calcula percentual de forma segura.
    
    Args:
        parte: Valor da parte
        total: Valor total
        
    Returns:
        Percentual (0.0 a 100.0)
    """
    if total == 0:
        return 0.0
    return (parte / total) * 100


def calcular_media(valores: List[Union[int, float]]) -> float:
    """
    Calcula média de lista de valores.
    
    Args:
        valores: Lista de valores numéricos
        
    Returns:
        Média dos valores
    """
    if not valores:
        return 0.0
    return sum(valores) / len(valores)


def calcular_mediana(valores: List[Union[int, float]]) -> float:
    """
    Calcula mediana de lista de valores.
    
    Args:
        valores: Lista de valores numéricos
        
    Returns:
        Mediana dos valores
    """
    if not valores:
        return 0.0
    
    valores_ordenados = sorted(valores)
    n = len(valores_ordenados)
    
    if n % 2 == 0:
        return (valores_ordenados[n//2 - 1] + valores_ordenados[n//2]) / 2
    else:
        return valores_ordenados[n//2]


def calcular_desvio_padrao(valores: List[Union[int, float]]) -> float:
    """
    Calcula desvio padrão de lista de valores.
    
    Args:
        valores: Lista de valores numéricos
        
    Returns:
        Desvio padrão dos valores
    """
    if len(valores) < 2:
        return 0.0
    
    media = calcular_media(valores)
    variancia = sum((x - media) ** 2 for x in valores) / (len(valores) - 1)
    return math.sqrt(variancia)


# ============================================================================
# MANIPULAÇÃO DE STRINGS
# ============================================================================

def limpar_string(texto: str) -> str:
    """
    Remove espaços extras e caracteres especiais de string.
    
    Args:
        texto: String a ser limpa
        
    Returns:
        String limpa
    """
    return ' '.join(texto.strip().split())


def truncar_string(texto: str, tamanho_max: int, sufixo: str = "...") -> str:
    """
    Trunca string se exceder tamanho máximo.
    
    Args:
        texto: String a ser truncada
        tamanho_max: Tamanho máximo
        sufixo: Sufixo para indicar truncamento
        
    Returns:
        String truncada
    """
    if len(texto) <= tamanho_max:
        return texto
    
    return texto[:tamanho_max - len(sufixo)] + sufixo


def extrair_numeros(texto: str) -> List[float]:
    """
    Extrai todos os números de uma string.
    
    Args:
        texto: String contendo números
        
    Returns:
        Lista de números encontrados
    """
    import re
    
    padrao = r'-?\d+\.?\d*'
    matches = re.findall(padrao, texto)
    
    numeros = []
    for match in matches:
        try:
            if '.' in match:
                numeros.append(float(match))
            else:
                numeros.append(int(match))
        except ValueError:
            continue
    
    return numeros


# ============================================================================
# UTILITÁRIOS DE SISTEMA
# ============================================================================

def obter_tamanho_objeto(obj: Any) -> int:
    """
    Obtém tamanho aproximado de objeto em bytes.
    
    Args:
        obj: Objeto a ser medido
        
    Returns:
        Tamanho em bytes
    """
    return sys.getsizeof(obj)


def criar_diretorio_se_nao_existe(caminho: str) -> bool:
    """
    Cria diretório se não existir.
    
    Args:
        caminho: Caminho do diretório
        
    Returns:
        True se criado ou já existia
    """
    try:
        os.makedirs(caminho, exist_ok=True)
        return True
    except Exception:
        return False


def obter_timestamp() -> str:
    """
    Obtém timestamp atual formatado.
    
    Returns:
        Timestamp no formato YYYY-MM-DD HH:MM:SS
    """
    return time.strftime("%Y-%m-%d %H:%M:%S")


def pausar_execucao(segundos: float = 1.0):
    """
    Pausa execução por tempo especificado.
    
    Args:
        segundos: Tempo de pausa em segundos
    """
    time.sleep(segundos)


# ============================================================================
# UTILITÁRIOS DE DEBUG
# ============================================================================

def imprimir_separador(titulo: str = "", largura: int = 60, char: str = "="):
    """
    Imprime separador visual com título opcional.
    
    Args:
        titulo: Título do separador
        largura: Largura do separador
        char: Caractere usado no separador
    """
    if titulo:
        print(f"\n{char * largura}")
        print(f"{titulo.center(largura)}")
        print(f"{char * largura}")
    else:
        print(f"{char * largura}")


def imprimir_info_objeto(obj: Any, nome: str = "objeto"):
    """
    Imprime informações detalhadas sobre um objeto.
    
    Args:
        obj: Objeto a ser analisado
        nome: Nome do objeto para exibição
    """
    print(f"\n=== INFORMAÇÕES DO {nome.upper()} ===")
    print(f"Tipo: {type(obj).__name__}")
    print(f"Valor: {obj}")
    print(f"Tamanho: {len(obj) if hasattr(obj, '__len__') else 'N/A'}")
    print(f"Tamanho em bytes: {obter_tamanho_objeto(obj)}")
    print(f"ID: {id(obj)}")
    
    if hasattr(obj, '__dict__'):
        print(f"Atributos: {list(obj.__dict__.keys())}")


# ============================================================================
# FUNÇÕES DE TESTE E DEMONSTRAÇÃO
# ============================================================================

def testar_helpers():
    """
    Testa todas as funções do módulo helpers.
    """
    print("=== TESTE DO MÓDULO HELPERS ===")
    print()
    
    # Teste de formatação
    print("1. FORMATAÇÃO:")
    print(f"   Tempo: {formatar_tempo(0.001234)}")
    print(f"   Memória: {formatar_memoria(1536000)}")
    print(f"   Número: {formatar_numero(1234567.89)}")
    print(f"   Percentual: {formatar_percentual(75, 100)}")
    
    # Teste de validação
    print("\n2. VALIDAÇÃO:")
    print(f"   Lista válida: {validar_lista([1, 2, 3])}")
    print(f"   Número válido: {validar_numero(42.5)}")
    print(f"   String válida: {validar_string_nao_vazia('teste')}")
    
    # Teste de conversão
    print("\n3. CONVERSÃO:")
    print(f"   Para lista: {converter_para_lista((1, 2, 3))}")
    print(f"   Para número: {converter_para_numero('42.5')}")
    
    # Teste de geração de dados
    print("\n4. GERAÇÃO DE DADOS:")
    print(f"   Lista aleatória: {formatar_lista_legivel(gerar_lista_aleatoria(5))}")
    print(f"   Lista ordenada: {gerar_lista_ordenada(5)}")
    print(f"   String aleatória: {gerar_string_aleatoria(10)}")
    
    # Teste de cálculos
    valores = [1, 2, 3, 4, 5]
    print("\n5. CÁLCULOS:")
    print(f"   Valores: {valores}")
    print(f"   Média: {calcular_media(valores):.2f}")
    print(f"   Mediana: {calcular_mediana(valores):.2f}")
    print(f"   Desvio padrão: {calcular_desvio_padrao(valores):.2f}")
    
    print("\n=== TESTE CONCLUÍDO ===")


if __name__ == "__main__":
    testar_helpers()