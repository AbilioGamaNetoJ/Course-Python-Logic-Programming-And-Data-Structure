# 📦 Pacote Utils - Utilitários do Curso

Este pacote contém utilitários e ferramentas auxiliares utilizadas em todo o **Curso de Lógica de Programação e Estruturas de Dados** em Python.

## 🎯 Objetivo

Centralizar funcionalidades comuns, evitar duplicação de código e fornecer ferramentas padronizadas para:
- Formatação e validação de dados
- Análise de performance e complexidade
- Decoradores para otimização
- Constantes globais do projeto
- Validadores especializados

## 📋 Estrutura do Pacote

```
utils/
├── __init__.py          # Configuração do pacote e imports
├── helpers.py           # Funções auxiliares comuns
├── constants.py         # Constantes globais do projeto
├── decorators.py        # Decoradores úteis
├── validators.py        # Validadores de dados
├── performance.py       # Ferramentas de análise de performance
└── README.md           # Esta documentação
```

## 🛠️ Módulos Disponíveis

### 📋 helpers.py - Funções Auxiliares
Funções utilitárias para uso geral:

**Formatação de Dados:**
- `formatar_tempo(segundos)` - Formata tempo em formato legível
- `formatar_memoria(bytes)` - Formata tamanho de memória
- `formatar_numero(numero)` - Formata números com separadores
- `formatar_percentual(valor)` - Formata percentuais

**Validação Básica:**
- `validar_lista(lista)` - Valida se é uma lista válida
- `validar_numero(numero)` - Valida números
- `validar_string_nao_vazia(string)` - Valida strings

**Geração de Dados de Teste:**
- `gerar_lista_aleatoria(tamanho)` - Gera listas aleatórias
- `gerar_lista_ordenada(tamanho)` - Gera listas ordenadas
- `gerar_string_aleatoria(tamanho)` - Gera strings aleatórias

### 🎯 constants.py - Constantes Globais
Constantes padronizadas para todo o projeto:

**Tamanhos de Teste:**
```python
TAMANHOS_TESTE = {
    'pequeno': 100,
    'medio': 1000,
    'grande': 10000,
    'muito_grande': 100000
}
```

**Cores para Terminal:**
```python
CORES = {
    'vermelho': '\033[91m',
    'verde': '\033[92m',
    'amarelo': '\033[93m',
    'azul': '\033[94m',
    'reset': '\033[0m'
}
```

**Configurações de Algoritmos:**
- Limites de complexidade
- Thresholds de performance
- Mensagens de erro padronizadas

### 🎨 decorators.py - Decoradores
Decoradores para análise e otimização:

**Performance:**
- `@medir_tempo` - Mede tempo de execução
- `@contar_operacoes` - Conta operações realizadas
- `@profile_memoria` - Analisa uso de memória

**Cache:**
- `@cache_resultado` - Cache LRU para resultados
- `@memoize` - Memoização de funções

**Logging:**
- `@log_execucao` - Log automático de execução
- `@log_erros` - Log de erros e exceções

**Benchmark:**
- `@benchmark` - Benchmark automático
- `@comparar_algoritmos` - Comparação de algoritmos

### ✅ validators.py - Validadores
Validadores especializados para diferentes tipos de dados:

**Estruturas de Dados:**
- `ValidadorEstruturaDados` - Valida listas, árvores, grafos
- Validação de ordenação, balanceamento, conectividade

**Dados Empresariais:**
- `ValidadorDadosEmpresariais` - CPF, CNPJ, email, telefone
- Validação de CEP, datas, formatos específicos

**Tipos Numéricos:**
- `ValidadorNumerico` - Ranges, primos, potências
- Validação de tipos numéricos específicos

**Strings:**
- `ValidadorString` - Formatos, padrões, tamanhos
- Validação de JSON, datas, alfanuméricos

### 📊 performance.py - Análise de Performance
Ferramentas avançadas para análise de performance:

**Análise de Complexidade:**
- `AnalisadorComplexidade` - Análise temporal e espacial
- Comparação de algoritmos
- Geração de gráficos de complexidade

**Profiling Avançado:**
- `ProfilerAvancado` - Profiling detalhado de funções
- Análise de uso de memória
- Relatórios de otimização

**Monitoramento:**
- `MonitorRecursos` - Monitoramento de CPU e memória
- Geração de gráficos em tempo real
- Alertas de uso excessivo

**Benchmark:**
- `BenchmarkSuite` - Suite completa de benchmarks
- Comparação de múltiplos algoritmos
- Relatórios HTML detalhados

## 🚀 Como Usar

### Importação Básica
```python
# Importar módulos específicos
from utils import helpers, constants, decorators

# Importar funções específicas
from utils.helpers import formatar_tempo, gerar_lista_aleatoria
from utils.constants import TAMANHOS_TESTE, CORES
from utils.decorators import medir_tempo, benchmark
```

### Exemplo Prático
```python
from utils import medir_tempo, gerar_lista_aleatoria, TAMANHOS_TESTE

@medir_tempo(exibir=True)
def algoritmo_teste(lista):
    return sorted(lista)

# Gerar dados de teste
tamanho = TAMANHOS_TESTE['medio']
dados = gerar_lista_aleatoria(tamanho)

# Executar com medição automática
resultado = algoritmo_teste(dados)
```

### Análise de Performance
```python
from utils.performance import AnalisadorComplexidade, BenchmarkSuite

# Analisar complexidade
analisador = AnalisadorComplexidade()
complexidade = analisador.analisar_funcao(minha_funcao, dados_teste)

# Benchmark comparativo
benchmark = BenchmarkSuite()
benchmark.adicionar_algoritmo("Bubble Sort", bubble_sort)
benchmark.adicionar_algoritmo("Quick Sort", quick_sort)
relatorio = benchmark.executar_benchmark(dados_teste)
```

### Validação de Dados
```python
from utils.validators import Validador, ValidadorNumerico

# Validação geral
validador = Validador()
resultado = validador.validar_multiplos([
    (lista_dados, 'lista_valida'),
    (numero, 'numero_positivo'),
    (email, 'email_valido')
])

# Validação específica
if ValidadorNumerico.numero_primo(17):
    print("17 é primo!")
```

## 📈 Benefícios

### ✅ Padronização
- Funções consistentes em todo o projeto
- Mensagens de erro padronizadas
- Formatos de saída uniformes

### ⚡ Performance
- Decoradores para análise automática
- Cache inteligente de resultados
- Profiling detalhado

### 🔍 Debugging
- Logging automático
- Validação rigorosa de dados
- Relatórios de erro detalhados

### 📊 Análise
- Métricas de complexidade
- Comparação de algoritmos
- Gráficos de performance

## 🎓 Integração com o Curso

Este pacote utils é utilizado em todos os módulos do curso:

- **Módulo 1-3**: Helpers para formatação e validação básica
- **Módulo 4-5**: Validadores de estruturas de dados
- **Módulo 6-7**: Decoradores de performance e análise
- **Módulo 8**: Ferramentas completas de benchmark e profiling

## 💡 Exemplos de Uso por Módulo

### Estruturas de Dados
```python
from utils.validators import ValidadorEstruturaDados
from utils.decorators import medir_tempo

@medir_tempo()
def inserir_arvore_avl(arvore, valor):
    # Implementação...
    pass

# Validar estrutura após operação
if ValidadorEstruturaDados.arvore_balanceada(arvore):
    print("Árvore mantém balanceamento!")
```

### Algoritmos de Ordenação
```python
from utils.performance import BenchmarkSuite
from utils.helpers import gerar_lista_aleatoria

# Comparar algoritmos de ordenação
benchmark = BenchmarkSuite()
dados = gerar_lista_aleatoria(1000)

benchmark.comparar_algoritmos({
    'Bubble Sort': bubble_sort,
    'Quick Sort': quick_sort,
    'Merge Sort': merge_sort
}, dados)
```

### Projetos Práticos
```python
from utils import *

# Sistema completo com todas as ferramentas
class SistemaGestao:
    @log_execucao
    @medir_tempo
    def processar_pedido(self, pedido):
        # Validar dados
        if not Validador.validar_pedido(pedido):
            raise ValueError("Pedido inválido")
        
        # Processar...
        return resultado
```

## 🔧 Manutenção e Extensão

Para adicionar novas funcionalidades:

1. **Helpers**: Adicione funções utilitárias em `helpers.py`
2. **Constants**: Defina novas constantes em `constants.py`
3. **Decorators**: Implemente novos decoradores em `decorators.py`
4. **Validators**: Crie validadores específicos em `validators.py`
5. **Performance**: Adicione ferramentas de análise em `performance.py`

Lembre-se de:
- Atualizar `__init__.py` com novos imports
- Adicionar testes para novas funcionalidades
- Documentar adequadamente o código
- Manter compatibilidade com versões anteriores

---

**Versão:** 1.0.0  
**Autor:** Professor de Lógica de Programação  
**Data:** 2024

Este pacote é parte integrante do **Curso de Lógica de Programação e Estruturas de Dados** e foi desenvolvido para maximizar o aprendizado através de ferramentas práticas e padronizadas.