"""
Utils - Utilitários para o Curso de Lógica de Programação

Este pacote contém utilitários e ferramentas auxiliares utilizadas
em todo o curso de Lógica de Programação e Estruturas de Dados.

Módulos disponíveis:
- helpers: Funções auxiliares comuns
- constants: Constantes globais do projeto
- decorators: Decoradores úteis
- validators: Validadores de dados
- performance: Ferramentas de análise de performance

Autor: Professor de Lógica de Programação
Data: 2024
"""

# Versão do pacote
__version__ = "1.0.0"

# Metadados
__author__ = "Professor de Lógica de Programação"
__email__ = "professor@logica.edu"
__description__ = "Utilitários para Curso de Lógica de Programação e Estruturas de Dados"

# Imports dos módulos principais
try:
    from . import helpers
    from . import constants
    from . import decorators
    from . import validators
    from . import performance
    
    # Imports específicos mais utilizados
    from .helpers import (
        formatar_tempo, formatar_memoria, formatar_numero,
        validar_lista, converter_para_numero, gerar_lista_aleatoria,
        calcular_percentual, limpar_string
    )
    
    from .constants import (
        TAMANHOS_TESTE, CORES, MENSAGENS_ERRO, CONFIGURACOES_PADRAO,
        obter_config_algoritmo, formatar_texto_colorido
    )
    
    from .decorators import (
        medir_tempo, cache_resultado, log_execucao, validar_tipos,
        benchmark, comparar_algoritmos
    )
    
    from .validators import (
        Validador, ValidadorEstruturaDados, ValidadorDadosEmpresariais,
        ValidadorNumerico, ValidadorString
    )
    
    from .performance import (
        AnalisadorComplexidade, ProfilerAvancado, MonitorRecursos,
        BenchmarkSuite
    )
    
    # Lista de módulos públicos
    __all__ = [
        # Módulos
        'helpers', 'constants', 'decorators', 'validators', 'performance',
        
        # Funções helpers
        'formatar_tempo', 'formatar_memoria', 'formatar_numero',
        'validar_lista', 'converter_para_numero', 'gerar_lista_aleatoria',
        'calcular_percentual', 'limpar_string',
        
        # Constants
        'TAMANHOS_TESTE', 'CORES', 'MENSAGENS_ERRO', 'CONFIGURACOES_PADRAO',
        'obter_config_algoritmo', 'formatar_texto_colorido',
        
        # Decorators
        'medir_tempo', 'cache_resultado', 'log_execucao', 'validar_tipos',
        'benchmark', 'comparar_algoritmos',
        
        # Validators
        'Validador', 'ValidadorEstruturaDados', 'ValidadorDadosEmpresariais',
        'ValidadorNumerico', 'ValidadorString',
        
        # Performance
        'AnalisadorComplexidade', 'ProfilerAvancado', 'MonitorRecursos',
        'BenchmarkSuite'
    ]
    
    print("📦 Pacote utils carregado com sucesso!")
    print(f"   Versão: {__version__}")
    print(f"   Módulos disponíveis: helpers, constants, decorators, validators, performance")
    print(f"   Funções importadas: {len(__all__)} itens disponíveis")
    
except ImportError as e:
    import logging
    import sys
    
    # Configurar logging para erros de importação
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)
    
    # Log detalhado do erro
    logger.warning(f"Erro ao importar módulo utils: {e}")
    logger.warning(f"Módulo problemático: {e.name if hasattr(e, 'name') else 'desconhecido'}")
    logger.warning("Alguns recursos podem não estar disponíveis")
    
    # Tentar importar módulos individualmente para identificar qual está falhando
    modulos_disponiveis = []
    modulos_com_erro = []
    
    for modulo in ['helpers', 'constants', 'decorators', 'validators', 'performance']:
        try:
            globals()[modulo] = __import__(f'utils.{modulo}', fromlist=[modulo])
            modulos_disponiveis.append(modulo)
        except ImportError as mod_error:
            modulos_com_erro.append((modulo, str(mod_error)))
            logger.error(f"Falha ao importar {modulo}: {mod_error}")
    
    # Informar usuário sobre status dos módulos
    if modulos_disponiveis:
        print(f"✅ Módulos utils disponíveis: {', '.join(modulos_disponiveis)}")
    
    if modulos_com_erro:
        print(f"❌ Módulos com erro: {', '.join([m[0] for m in modulos_com_erro])}")
        print("💡 Execute 'pip install -r requirements.txt' para resolver dependências")
    
    # Definir __all__ apenas com módulos disponíveis
    __all__ = modulos_disponiveis


def listar_funcionalidades():
    """
    Lista todas as funcionalidades disponíveis no pacote utils.
    """
    print("\n🛠️  FUNCIONALIDADES DO PACOTE UTILS:")
    print()
    
    print("📋 HELPERS (Funções Auxiliares):")
    print("   • Formatação de dados (tempo, memória, números)")
    print("   • Validação básica (listas, números, strings)")
    print("   • Conversão de tipos segura")
    print("   • Geração de dados de teste")
    print("   • Cálculos matemáticos auxiliares")
    print("   • Manipulação de strings")
    print("   • Utilitários de sistema")
    print()
    
    print("🎯 CONSTANTS (Constantes Globais):")
    print("   • Tamanhos de teste padronizados")
    print("   • Cores para terminal")
    print("   • Mensagens de erro padronizadas")
    print("   • Configurações padrão de algoritmos")
    print("   • Limites e thresholds")
    print("   • Templates e formatos")
    print()
    
    print("🎨 DECORATORS (Decoradores):")
    print("   • Medição de tempo de execução")
    print("   • Cache LRU e memoização")
    print("   • Logging automático")
    print("   • Validação de tipos e ranges")
    print("   • Retry automático")
    print("   • Benchmark e comparação")
    print()
    
    print("✅ VALIDATORS (Validadores):")
    print("   • Estruturas de dados (listas, árvores, grafos)")
    print("   • Algoritmos (ordenação, busca)")
    print("   • Dados empresariais (CPF, CNPJ, email)")
    print("   • Tipos numéricos (ranges, primos)")
    print("   • Strings (formatos, padrões)")
    print("   • Performance (complexidade, limites)")
    print()
    
    print("📊 PERFORMANCE (Análise de Performance):")
    print("   • Análise de complexidade temporal/espacial")
    print("   • Profiling detalhado de funções")
    print("   • Monitoramento de recursos do sistema")
    print("   • Benchmark comparativo")
    print("   • Relatórios de otimização")
    print("   • Gráficos de performance")
    print()
    
    print("💡 EXEMPLO DE USO:")
    print("   from utils import medir_tempo, Validador, AnalisadorComplexidade")
    print("   from utils.helpers import gerar_lista_aleatoria")
    print("   from utils.constants import TAMANHOS_TESTE")
    print()


def demonstrar_utils():
    """
    Demonstra o uso das principais funcionalidades do pacote utils.
    """
    print("\n🚀 DEMONSTRAÇÃO DO PACOTE UTILS:")
    print()
    
    try:
        # Demonstrar helpers
        print("1. HELPERS:")
        from .helpers import formatar_tempo, gerar_lista_aleatoria
        print(f"   Tempo formatado: {formatar_tempo(0.001234)}")
        lista = gerar_lista_aleatoria(5)
        print(f"   Lista aleatória: {lista}")
        print()
        
        # Demonstrar decorators
        print("2. DECORATORS:")
        from .decorators import medir_tempo
        
        @medir_tempo(exibir=True)
        def operacao_teste():
            return sum(range(1000))
        
        resultado = operacao_teste()
        print(f"   Resultado: {resultado}")
        print()
        
        # Demonstrar validators
        print("3. VALIDATORS:")
        from .validators import ValidadorNumerico, ValidadorString
        print(f"   17 é primo: {ValidadorNumerico.numero_primo(17)}")
        print(f"   'Python' apenas letras: {ValidadorString.apenas_letras('Python')}")
        print()
        
        print("✅ Demonstração concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")


# Executar demonstração se importado diretamente
if __name__ == "__main__":
    listar_funcionalidades()
    demonstrar_utils()