"""
Validators - Validadores de Dados Específicos

Este módulo contém validadores especializados para diferentes tipos de dados
e estruturas utilizadas no curso de Lógica de Programação e Estruturas de Dados.

Tipos de validadores:
1. Estruturas de dados (listas, árvores, grafos)
2. Algoritmos (ordenação, busca)
3. Dados empresariais (CPF, CNPJ, email, telefone)
4. Tipos numéricos (inteiros, floats, ranges)
5. Strings (formatos, padrões)
6. Performance (complexidade, limites)

Autor: Professor de Lógica de Programação
Data: 2024
"""

import re
import math
from typing import Any, List, Dict, Set, Tuple, Optional, Union, Callable
from collections import defaultdict
from datetime import datetime, date
import json


# ============================================================================
# VALIDADORES DE ESTRUTURAS DE DADOS
# ============================================================================

class ValidadorEstruturaDados:
    """Validadores para estruturas de dados."""
    
    @staticmethod
    def lista_valida(lista: Any, tipo_elemento: type = None, 
                    tamanho_min: int = 0, tamanho_max: int = None) -> bool:
        """
        Valida se uma lista atende aos critérios especificados.
        
        Args:
            lista: Objeto a ser validado
            tipo_elemento: Tipo esperado dos elementos
            tamanho_min: Tamanho mínimo da lista
            tamanho_max: Tamanho máximo da lista
            
        Returns:
            True se válida, False caso contrário
        """
        if not isinstance(lista, list):
            return False
        
        # Validar tamanho
        if len(lista) < tamanho_min:
            return False
        
        if tamanho_max is not None and len(lista) > tamanho_max:
            return False
        
        # Validar tipo dos elementos
        if tipo_elemento is not None:
            for elemento in lista:
                if not isinstance(elemento, tipo_elemento):
                    return False
        
        return True
    
    @staticmethod
    def lista_ordenada(lista: List[Any], crescente: bool = True) -> bool:
        """
        Verifica se uma lista está ordenada.
        
        Args:
            lista: Lista a ser verificada
            crescente: Se deve estar em ordem crescente
            
        Returns:
            True se ordenada, False caso contrário
        """
        if not isinstance(lista, list) or len(lista) <= 1:
            return True
        
        for i in range(1, len(lista)):
            if crescente:
                if lista[i] < lista[i-1]:
                    return False
            else:
                if lista[i] > lista[i-1]:
                    return False
        
        return True
    
    @staticmethod
    def arvore_binaria_valida(no: Any) -> bool:
        """
        Valida se uma estrutura representa uma árvore binária válida.
        
        Args:
            no: Nó raiz da árvore
            
        Returns:
            True se válida, False caso contrário
        """
        if no is None:
            return True
        
        # Verificar se tem atributos necessários
        if not hasattr(no, 'valor'):
            return False
        
        # Verificar filhos
        esquerda_valida = True
        direita_valida = True
        
        if hasattr(no, 'esquerda') and no.esquerda is not None:
            esquerda_valida = ValidadorEstruturaDados.arvore_binaria_valida(no.esquerda)
        
        if hasattr(no, 'direita') and no.direita is not None:
            direita_valida = ValidadorEstruturaDados.arvore_binaria_valida(no.direita)
        
        return esquerda_valida and direita_valida
    
    @staticmethod
    def bst_valida(no: Any, min_val: float = float('-inf'), 
                  max_val: float = float('inf')) -> bool:
        """
        Valida se uma árvore é uma BST válida.
        
        Args:
            no: Nó raiz da árvore
            min_val: Valor mínimo permitido
            max_val: Valor máximo permitido
            
        Returns:
            True se BST válida, False caso contrário
        """
        if no is None:
            return True
        
        if not hasattr(no, 'valor'):
            return False
        
        # Verificar se valor está no range válido
        if no.valor <= min_val or no.valor >= max_val:
            return False
        
        # Verificar recursivamente
        esquerda_valida = True
        direita_valida = True
        
        if hasattr(no, 'esquerda') and no.esquerda is not None:
            esquerda_valida = ValidadorEstruturaDados.bst_valida(
                no.esquerda, min_val, no.valor
            )
        
        if hasattr(no, 'direita') and no.direita is not None:
            direita_valida = ValidadorEstruturaDados.bst_valida(
                no.direita, no.valor, max_val
            )
        
        return esquerda_valida and direita_valida
    
    @staticmethod
    def grafo_valido(grafo: Dict[Any, List[Any]]) -> bool:
        """
        Valida se um dicionário representa um grafo válido.
        
        Args:
            grafo: Dicionário representando o grafo
            
        Returns:
            True se válido, False caso contrário
        """
        if not isinstance(grafo, dict):
            return False
        
        # Verificar se todos os valores são listas
        for vertice, adjacentes in grafo.items():
            if not isinstance(adjacentes, list):
                return False
            
            # Verificar se todos os adjacentes existem como vértices
            for adj in adjacentes:
                if adj not in grafo:
                    return False
        
        return True


# ============================================================================
# VALIDADORES DE ALGORITMOS
# ============================================================================

class ValidadorAlgoritmo:
    """Validadores para algoritmos."""
    
    @staticmethod
    def algoritmo_ordenacao_valido(func: Callable, teste_casos: int = 10) -> bool:
        """
        Testa se um algoritmo de ordenação funciona corretamente.
        
        Args:
            func: Função de ordenação a ser testada
            teste_casos: Número de casos de teste
            
        Returns:
            True se válido, False caso contrário
        """
        import random
        
        try:
            for _ in range(teste_casos):
                # Gerar lista aleatória
                tamanho = random.randint(0, 100)
                lista = [random.randint(-1000, 1000) for _ in range(tamanho)]
                lista_original = lista.copy()
                
                # Aplicar algoritmo
                resultado = func(lista)
                
                # Verificar se está ordenada
                if not ValidadorEstruturaDados.lista_ordenada(resultado):
                    return False
                
                # Verificar se tem os mesmos elementos
                if sorted(lista_original) != sorted(resultado):
                    return False
            
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def algoritmo_busca_valido(func: Callable, teste_casos: int = 10) -> bool:
        """
        Testa se um algoritmo de busca funciona corretamente.
        
        Args:
            func: Função de busca a ser testada
            teste_casos: Número de casos de teste
            
        Returns:
            True se válido, False caso contrário
        """
        import random
        
        try:
            for _ in range(teste_casos):
                # Gerar lista ordenada
                tamanho = random.randint(1, 100)
                lista = sorted([random.randint(-1000, 1000) for _ in range(tamanho)])
                
                # Testar elemento presente
                elemento = random.choice(lista)
                resultado = func(lista, elemento)
                
                if resultado == -1 or lista[resultado] != elemento:
                    return False
                
                # Testar elemento ausente
                elemento_ausente = max(lista) + 1
                resultado = func(lista, elemento_ausente)
                
                if resultado != -1:
                    return False
            
            return True
            
        except Exception:
            return False


# ============================================================================
# VALIDADORES DE DADOS EMPRESARIAIS
# ============================================================================

class ValidadorDadosEmpresariais:
    """Validadores para dados empresariais."""
    
    @staticmethod
    def cpf_valido(cpf: str) -> bool:
        """
        Valida CPF brasileiro.
        
        Args:
            cpf: String do CPF
            
        Returns:
            True se válido, False caso contrário
        """
        # Remover caracteres não numéricos
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        # Verificar se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verificar se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Calcular primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        if int(cpf[9]) != digito1:
            return False
        
        # Calcular segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        return int(cpf[10]) == digito2
    
    @staticmethod
    def cnpj_valido(cnpj: str) -> bool:
        """
        Valida CNPJ brasileiro.
        
        Args:
            cnpj: String do CNPJ
            
        Returns:
            True se válido, False caso contrário
        """
        # Remover caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        # Verificar se tem 14 dígitos
        if len(cnpj) != 14:
            return False
        
        # Verificar se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return False
        
        # Calcular primeiro dígito verificador
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        if int(cnpj[12]) != digito1:
            return False
        
        # Calcular segundo dígito verificador
        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        return int(cnpj[13]) == digito2
    
    @staticmethod
    def email_valido(email: str) -> bool:
        """
        Valida formato de email.
        
        Args:
            email: String do email
            
        Returns:
            True se válido, False caso contrário
        """
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email))
    
    @staticmethod
    def telefone_valido(telefone: str) -> bool:
        """
        Valida formato de telefone brasileiro.
        
        Args:
            telefone: String do telefone
            
        Returns:
            True se válido, False caso contrário
        """
        # Remover caracteres não numéricos
        telefone = re.sub(r'[^0-9]', '', telefone)
        
        # Verificar formatos válidos
        # Celular: 11 dígitos (com 9)
        # Fixo: 10 dígitos
        if len(telefone) == 11:
            # Celular: deve começar com DDD válido e ter 9 como terceiro dígito
            return telefone[0:2] in ['11', '12', '13', '14', '15', '16', '17', '18', '19',
                                   '21', '22', '24', '27', '28', '31', '32', '33', '34',
                                   '35', '37', '38', '41', '42', '43', '44', '45', '46',
                                   '47', '48', '49', '51', '53', '54', '55', '61', '62',
                                   '63', '64', '65', '66', '67', '68', '69', '71', '73',
                                   '74', '75', '77', '79', '81', '82', '83', '84', '85',
                                   '86', '87', '88', '89', '91', '92', '93', '94', '95',
                                   '96', '97', '98', '99'] and telefone[2] == '9'
        elif len(telefone) == 10:
            # Fixo: deve começar com DDD válido
            return telefone[0:2] in ['11', '12', '13', '14', '15', '16', '17', '18', '19',
                                   '21', '22', '24', '27', '28', '31', '32', '33', '34',
                                   '35', '37', '38', '41', '42', '43', '44', '45', '46',
                                   '47', '48', '49', '51', '53', '54', '55', '61', '62',
                                   '63', '64', '65', '66', '67', '68', '69', '71', '73',
                                   '74', '75', '77', '79', '81', '82', '83', '84', '85',
                                   '86', '87', '88', '89', '91', '92', '93', '94', '95',
                                   '96', '97', '98', '99']
        
        return False
    
    @staticmethod
    def cep_valido(cep: str) -> bool:
        """
        Valida formato de CEP brasileiro.
        
        Args:
            cep: String do CEP
            
        Returns:
            True se válido, False caso contrário
        """
        # Remover caracteres não numéricos
        cep = re.sub(r'[^0-9]', '', cep)
        
        # Verificar se tem 8 dígitos
        return len(cep) == 8 and cep.isdigit()


# ============================================================================
# VALIDADORES NUMÉRICOS
# ============================================================================

class ValidadorNumerico:
    """Validadores para dados numéricos."""
    
    @staticmethod
    def inteiro_positivo(valor: Any) -> bool:
        """Valida se é inteiro positivo."""
        return isinstance(valor, int) and valor > 0
    
    @staticmethod
    def inteiro_nao_negativo(valor: Any) -> bool:
        """Valida se é inteiro não negativo."""
        return isinstance(valor, int) and valor >= 0
    
    @staticmethod
    def numero_no_range(valor: Any, minimo: float, maximo: float) -> bool:
        """Valida se número está no range especificado."""
        return isinstance(valor, (int, float)) and minimo <= valor <= maximo
    
    @staticmethod
    def percentual_valido(valor: Any) -> bool:
        """Valida se é um percentual válido (0-100)."""
        return isinstance(valor, (int, float)) and 0 <= valor <= 100
    
    @staticmethod
    def numero_primo(n: int) -> bool:
        """Verifica se um número é primo."""
        if not isinstance(n, int) or n < 2:
            return False
        
        if n == 2:
            return True
        
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        
        return True
    
    @staticmethod
    def potencia_de_dois(n: int) -> bool:
        """Verifica se um número é potência de 2."""
        return isinstance(n, int) and n > 0 and (n & (n - 1)) == 0


# ============================================================================
# VALIDADORES DE STRING
# ============================================================================

class ValidadorString:
    """Validadores para strings."""
    
    @staticmethod
    def string_nao_vazia(texto: Any) -> bool:
        """Valida se string não está vazia."""
        return isinstance(texto, str) and len(texto.strip()) > 0
    
    @staticmethod
    def apenas_letras(texto: str) -> bool:
        """Valida se contém apenas letras."""
        return isinstance(texto, str) and texto.isalpha()
    
    @staticmethod
    def apenas_numeros(texto: str) -> bool:
        """Valida se contém apenas números."""
        return isinstance(texto, str) and texto.isdigit()
    
    @staticmethod
    def alfanumerico(texto: str) -> bool:
        """Valida se é alfanumérico."""
        return isinstance(texto, str) and texto.isalnum()
    
    @staticmethod
    def tamanho_valido(texto: str, min_len: int = 0, max_len: int = None) -> bool:
        """Valida tamanho da string."""
        if not isinstance(texto, str):
            return False
        
        if len(texto) < min_len:
            return False
        
        if max_len is not None and len(texto) > max_len:
            return False
        
        return True
    
    @staticmethod
    def formato_data(texto: str, formato: str = '%d/%m/%Y') -> bool:
        """Valida formato de data."""
        try:
            datetime.strptime(texto, formato)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def json_valido(texto: str) -> bool:
        """Valida se string é JSON válido."""
        try:
            json.loads(texto)
            return True
        except (json.JSONDecodeError, TypeError):
            return False


# ============================================================================
# VALIDADORES DE PERFORMANCE
# ============================================================================

class ValidadorPerformance:
    """Validadores para análise de performance."""
    
    @staticmethod
    def complexidade_aceitavel(func: Callable, tamanho_entrada: int, 
                             tempo_limite: float = 1.0) -> bool:
        """
        Verifica se função executa dentro do tempo limite.
        
        Args:
            func: Função a ser testada
            tamanho_entrada: Tamanho da entrada de teste
            tempo_limite: Tempo limite em segundos
            
        Returns:
            True se dentro do limite, False caso contrário
        """
        import time
        import random
        
        try:
            # Gerar entrada de teste
            entrada = [random.randint(1, 1000) for _ in range(tamanho_entrada)]
            
            # Medir tempo
            inicio = time.perf_counter()
            func(entrada)
            fim = time.perf_counter()
            
            return (fim - inicio) <= tempo_limite
            
        except Exception:
            return False
    
    @staticmethod
    def uso_memoria_aceitavel(func: Callable, limite_mb: float = 100.0) -> bool:
        """
        Verifica se função usa memória dentro do limite.
        
        Args:
            func: Função a ser testada
            limite_mb: Limite de memória em MB
            
        Returns:
            True se dentro do limite, False caso contrário
        """
        import sys
        import gc
        
        try:
            # Limpar garbage collector
            gc.collect()
            
            # Medir memória inicial
            memoria_inicial = sys.getsizeof(gc.get_objects())
            
            # Executar função
            resultado = func()
            
            # Medir memória final
            memoria_final = sys.getsizeof(gc.get_objects())
            memoria_final += sys.getsizeof(resultado) if resultado else 0
            
            # Calcular diferença em MB
            diferenca_mb = (memoria_final - memoria_inicial) / (1024 * 1024)
            
            return diferenca_mb <= limite_mb
            
        except Exception:
            return False


# ============================================================================
# CLASSE PRINCIPAL DE VALIDAÇÃO
# ============================================================================

class Validador:
    """Classe principal que agrupa todos os validadores."""
    
    def __init__(self):
        self.estrutura = ValidadorEstruturaDados()
        self.algoritmo = ValidadorAlgoritmo()
        self.empresarial = ValidadorDadosEmpresariais()
        self.numerico = ValidadorNumerico()
        self.string = ValidadorString()
        self.performance = ValidadorPerformance()
        
        # Histórico de validações
        self.historico = []
    
    def validar(self, dados: Any, regras: List[Callable]) -> Dict[str, Any]:
        """
        Executa múltiplas validações em dados.
        
        Args:
            dados: Dados a serem validados
            regras: Lista de funções de validação
            
        Returns:
            Dicionário com resultados das validações
        """
        resultados = {
            'valido': True,
            'erros': [],
            'detalhes': {}
        }
        
        for regra in regras:
            try:
                nome_regra = regra.__name__
                resultado = regra(dados)
                
                resultados['detalhes'][nome_regra] = resultado
                
                if not resultado:
                    resultados['valido'] = False
                    resultados['erros'].append(f"Falha na validação: {nome_regra}")
                    
            except Exception as e:
                resultados['valido'] = False
                resultados['erros'].append(f"Erro na validação {regra.__name__}: {str(e)}")
        
        # Adicionar ao histórico
        self.historico.append({
            'timestamp': datetime.now(),
            'dados_tipo': type(dados).__name__,
            'regras_aplicadas': len(regras),
            'resultado': resultados['valido']
        })
        
        return resultados
    
    def obter_historico(self) -> List[Dict]:
        """Retorna histórico de validações."""
        return self.historico.copy()
    
    def limpar_historico(self):
        """Limpa histórico de validações."""
        self.historico.clear()


# ============================================================================
# FUNÇÕES DE TESTE E DEMONSTRAÇÃO
# ============================================================================

def testar_validadores():
    """
    Testa todos os validadores do módulo.
    """
    print("=== TESTE DOS VALIDADORES ===")
    print()
    
    validador = Validador()
    
    # Teste de estruturas de dados
    print("1. ESTRUTURAS DE DADOS:")
    lista_teste = [1, 2, 3, 4, 5]
    print(f"   Lista [1,2,3,4,5] ordenada: {ValidadorEstruturaDados.lista_ordenada(lista_teste)}")
    print(f"   Lista válida (int): {ValidadorEstruturaDados.lista_valida(lista_teste, int)}")
    print()
    
    # Teste de dados empresariais
    print("2. DADOS EMPRESARIAIS:")
    print(f"   CPF 123.456.789-09: {ValidadorDadosEmpresariais.cpf_valido('123.456.789-09')}")
    print(f"   Email test@email.com: {ValidadorDadosEmpresariais.email_valido('test@email.com')}")
    print(f"   CEP 01234-567: {ValidadorDadosEmpresariais.cep_valido('01234-567')}")
    print()
    
    # Teste de validadores numéricos
    print("3. VALIDADORES NUMÉRICOS:")
    print(f"   17 é primo: {ValidadorNumerico.numero_primo(17)}")
    print(f"   16 é potência de 2: {ValidadorNumerico.potencia_de_dois(16)}")
    print(f"   85 é percentual válido: {ValidadorNumerico.percentual_valido(85)}")
    print()
    
    # Teste de strings
    print("4. VALIDADORES DE STRING:")
    print(f"   'Python' apenas letras: {ValidadorString.apenas_letras('Python')}")
    print(f"   '12345' apenas números: {ValidadorString.apenas_numeros('12345')}")
    print(f"   '25/12/2024' formato data: {ValidadorString.formato_data('25/12/2024')}")
    print()
    
    # Teste de validação múltipla
    print("5. VALIDAÇÃO MÚLTIPLA:")
    dados_teste = "Python123"
    regras = [
        ValidadorString.string_nao_vazia,
        ValidadorString.alfanumerico,
        lambda x: ValidadorString.tamanho_valido(x, 5, 15)
    ]
    
    resultado = validador.validar(dados_teste, regras)
    print(f"   Dados: '{dados_teste}'")
    print(f"   Válido: {resultado['valido']}")
    print(f"   Detalhes: {resultado['detalhes']}")
    
    print("\n=== TESTE CONCLUÍDO ===")


if __name__ == "__main__":
    testar_validadores()