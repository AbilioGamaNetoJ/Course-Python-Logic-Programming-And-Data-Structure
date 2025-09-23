"""
Performance - Ferramentas de Análise de Performance

Este módulo contém ferramentas avançadas para análise de performance,
profiling, benchmarking e otimização de algoritmos e estruturas de dados
utilizadas no curso de Lógica de Programação e Estruturas de Dados.

Funcionalidades:
1. Análise de complexidade temporal e espacial
2. Profiling detalhado de funções
3. Benchmarking comparativo de algoritmos
4. Monitoramento de recursos do sistema
5. Análise de gargalos de performance
6. Relatórios de otimização

Autor: Professor de Lógica de Programação
Data: 2024
"""

# Imports com tratamento de dependências opcionais
import time
import gc
import sys
import threading
import functools
import tracemalloc
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime
import json
import csv
from pathlib import Path

# Imports opcionais com tratamento de erro
try:
    import psutil
    PSUTIL_DISPONIVEL = True
except ImportError:
    PSUTIL_DISPONIVEL = False
    print("⚠️  psutil não disponível - monitoramento de recursos limitado")

try:
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_DISPONIVEL = True
except ImportError:
    MATPLOTLIB_DISPONIVEL = False
    print("⚠️  matplotlib/numpy não disponível - gráficos desabilitados")


# ============================================================================
# CLASSES DE DADOS PARA MÉTRICAS
# ============================================================================

@dataclass
class MetricaTempo:
    """Métrica de tempo de execução."""
    nome: str
    tempo_execucao: float
    timestamp: datetime
    parametros: Dict[str, Any]
    sucesso: bool
    memoria_usada: Optional[int] = None


@dataclass
class MetricaComplexidade:
    """Métrica de análise de complexidade."""
    algoritmo: str
    tamanho_entrada: int
    tempo_execucao: float
    memoria_usada: int
    operacoes_realizadas: int
    complexidade_teorica: str


@dataclass
class RelatorioPerformance:
    """Relatório completo de performance."""
    nome_teste: str
    timestamp: datetime
    metricas_tempo: List[MetricaTempo]
    metricas_complexidade: List[MetricaComplexidade]
    recursos_sistema: Dict[str, Any]
    recomendacoes: List[str]


# ============================================================================
# ANALISADOR DE COMPLEXIDADE
# ============================================================================

class AnalisadorComplexidade:
    """Analisa complexidade temporal e espacial de algoritmos."""
    
    def __init__(self):
        self.historico = []
        self.tamanhos_teste = [10, 50, 100, 500, 1000, 5000]
    
    def analisar_complexidade_temporal(self, func: Callable, 
                                     gerador_entrada: Callable,
                                     nome: str = None) -> Dict[str, Any]:
        """
        Analisa complexidade temporal de uma função.
        
        Args:
            func: Função a ser analisada
            gerador_entrada: Função que gera entrada de teste dado o tamanho
            nome: Nome do algoritmo
            
        Returns:
            Dicionário com análise de complexidade
        """
        nome = nome or func.__name__
        resultados = []
        
        print(f"🔍 Analisando complexidade temporal de {nome}...")
        
        for tamanho in self.tamanhos_teste:
            # Gerar entrada
            entrada = gerador_entrada(tamanho)
            
            # Múltiplas execuções para média
            tempos = []
            for _ in range(3):
                gc.collect()
                
                inicio = time.perf_counter()
                try:
                    func(entrada)
                    sucesso = True
                except Exception as e:
                    print(f"   ❌ Erro com tamanho {tamanho}: {e}")
                    sucesso = False
                    break
                fim = time.perf_counter()
                
                tempos.append(fim - inicio)
            
            if sucesso and tempos:
                tempo_medio = sum(tempos) / len(tempos)
                resultados.append({
                    'tamanho': tamanho,
                    'tempo': tempo_medio,
                    'tempo_por_elemento': tempo_medio / tamanho if tamanho > 0 else 0
                })
                
                print(f"   📊 n={tamanho:5d}: {tempo_medio:.6f}s ({tempo_medio/tamanho*1000000:.2f}μs/elem)")
        
        # Analisar padrão de crescimento
        complexidade_estimada = self._estimar_complexidade(resultados)
        
        analise = {
            'nome': nome,
            'resultados': resultados,
            'complexidade_estimada': complexidade_estimada,
            'timestamp': datetime.now()
        }
        
        self.historico.append(analise)
        return analise
    
    def _estimar_complexidade(self, resultados: List[Dict]) -> str:
        """Estima complexidade baseada nos resultados."""
        if len(resultados) < 3:
            return "Dados insuficientes"
        
        # Calcular razões de crescimento
        razoes = []
        for i in range(1, len(resultados)):
            if resultados[i-1]['tempo'] > 0:
                razao_tempo = resultados[i]['tempo'] / resultados[i-1]['tempo']
                razao_tamanho = resultados[i]['tamanho'] / resultados[i-1]['tamanho']
                razoes.append(razao_tempo / razao_tamanho)
        
        if not razoes:
            return "Indeterminada"
        
        razao_media = sum(razoes) / len(razoes)
        
        # Classificar complexidade
        if razao_media < 1.2:
            return "O(1) - Constante"
        elif razao_media < 2.0:
            return "O(log n) - Logarítmica"
        elif razao_media < 3.0:
            return "O(n) - Linear"
        elif razao_media < 5.0:
            return "O(n log n) - Linearítmica"
        elif razao_media < 10.0:
            return "O(n²) - Quadrática"
        else:
            return "O(n³) ou superior - Cúbica+"
    
    def comparar_algoritmos(self, algoritmos: Dict[str, Callable],
                          gerador_entrada: Callable) -> Dict[str, Any]:
        """
        Compara complexidade de múltiplos algoritmos.
        
        Args:
            algoritmos: Dicionário nome -> função
            gerador_entrada: Função geradora de entrada
            
        Returns:
            Comparação detalhada
        """
        print("🏁 Comparando algoritmos...")
        
        analises = {}
        for nome, func in algoritmos.items():
            analises[nome] = self.analisar_complexidade_temporal(func, gerador_entrada, nome)
        
        # Criar comparação
        comparacao = {
            'timestamp': datetime.now(),
            'algoritmos': analises,
            'ranking': self._criar_ranking(analises),
            'recomendacoes': self._gerar_recomendacoes(analises)
        }
        
        self._exibir_comparacao(comparacao)
        return comparacao
    
    def _criar_ranking(self, analises: Dict) -> List[Dict]:
        """Cria ranking de performance."""
        ranking = []
        
        for nome, analise in analises.items():
            if analise['resultados']:
                # Usar tempo do maior tamanho testado
                tempo_final = analise['resultados'][-1]['tempo']
                ranking.append({
                    'nome': nome,
                    'tempo': tempo_final,
                    'complexidade': analise['complexidade_estimada']
                })
        
        return sorted(ranking, key=lambda x: x['tempo'])
    
    def _gerar_recomendacoes(self, analises: Dict) -> List[str]:
        """Gera recomendações baseadas na análise."""
        recomendacoes = []
        
        # Encontrar melhor algoritmo
        ranking = self._criar_ranking(analises)
        if ranking:
            melhor = ranking[0]
            recomendacoes.append(f"Para melhor performance, use: {melhor['nome']}")
            
            if len(ranking) > 1:
                pior = ranking[-1]
                diferenca = pior['tempo'] / melhor['tempo']
                recomendacoes.append(
                    f"{melhor['nome']} é {diferenca:.1f}x mais rápido que {pior['nome']}"
                )
        
        # Recomendações por complexidade
        for nome, analise in analises.items():
            complexidade = analise['complexidade_estimada']
            if "Quadrática" in complexidade or "Cúbica" in complexidade:
                recomendacoes.append(
                    f"⚠️  {nome} tem alta complexidade - considere otimização para grandes entradas"
                )
        
        return recomendacoes
    
    def _exibir_comparacao(self, comparacao: Dict):
        """Exibe comparação formatada."""
        print("\n📈 RANKING DE PERFORMANCE:")
        for i, item in enumerate(comparacao['ranking'], 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
            print(f"   {emoji} {item['nome']}: {item['tempo']:.6f}s ({item['complexidade']})")
        
        print("\n💡 RECOMENDAÇÕES:")
        for rec in comparacao['recomendacoes']:
            print(f"   • {rec}")


# ============================================================================
# PROFILER AVANÇADO
# ============================================================================

class ProfilerAvancado:
    """Profiler avançado para análise detalhada de performance."""
    
    def __init__(self):
        self.sessoes = {}
        self.ativo = False
        self.dados_profiling = defaultdict(list)
    
    def iniciar_sessao(self, nome: str):
        """Inicia sessão de profiling."""
        self.sessoes[nome] = {
            'inicio': time.perf_counter(),
            'memoria_inicial': self._obter_memoria_processo(),
            'chamadas': [],
            'ativo': True
        }
        
        # Iniciar trace de memória
        if not tracemalloc.is_tracing():
            tracemalloc.start()
        
        print(f"🔍 Iniciando profiling: {nome}")
    
    def finalizar_sessao(self, nome: str) -> Dict[str, Any]:
        """Finaliza sessão de profiling."""
        if nome not in self.sessoes:
            raise ValueError(f"Sessão '{nome}' não encontrada")
        
        sessao = self.sessoes[nome]
        if not sessao['ativo']:
            raise ValueError(f"Sessão '{nome}' já foi finalizada")
        
        # Calcular métricas finais
        tempo_total = time.perf_counter() - sessao['inicio']
        memoria_final = self._obter_memoria_processo()
        memoria_usada = memoria_final - sessao['memoria_inicial']
        
        # Obter snapshot de memória
        snapshot = None
        if tracemalloc.is_tracing():
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')[:10]
        else:
            top_stats = []
        
        # Finalizar sessão
        sessao['ativo'] = False
        sessao['tempo_total'] = tempo_total
        sessao['memoria_usada'] = memoria_usada
        sessao['snapshot_memoria'] = top_stats
        
        print(f"✅ Profiling finalizado: {nome}")
        print(f"   Tempo total: {tempo_total:.6f}s")
        print(f"   Memória usada: {memoria_usada:+.2f} MB")
        
        return sessao
    
    def profile_funcao(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Faz profiling de uma função específica."""
        nome = f"{func.__name__}_{int(time.time())}"
        
        self.iniciar_sessao(nome)
        
        try:
            resultado = func(*args, **kwargs)
            sucesso = True
        except Exception as e:
            resultado = e
            sucesso = False
        
        sessao = self.finalizar_sessao(nome)
        sessao['resultado'] = resultado
        sessao['sucesso'] = sucesso
        
        return sessao
    
    def _obter_memoria_processo(self) -> float:
        """Obtém uso de memória do processo atual."""
        try:
            if PSUTIL_DISPONIVEL:
                processo = psutil.Process()
                return processo.memory_info().rss / 1024 / 1024  # MB
            else:
                # Fallback usando tracemalloc se psutil não estiver disponível
                if tracemalloc.is_tracing():
                    current, peak = tracemalloc.get_traced_memory()
                    return current / 1024 / 1024  # MB
                return 0.0
        except Exception:
            return 0.0
    
    def gerar_relatorio_detalhado(self, nome_sessao: str) -> str:
        """Gera relatório detalhado de uma sessão."""
        if nome_sessao not in self.sessoes:
            return "Sessão não encontrada"
        
        sessao = self.sessoes[nome_sessao]
        
        relatorio = f"""
=== RELATÓRIO DE PROFILING: {nome_sessao} ===

⏱️  TEMPO DE EXECUÇÃO:
   • Tempo total: {sessao.get('tempo_total', 0):.6f}s
   • Status: {'✅ Sucesso' if sessao.get('sucesso', False) else '❌ Erro'}

💾 USO DE MEMÓRIA:
   • Memória inicial: {sessao['memoria_inicial']:.2f} MB
   • Memória usada: {sessao.get('memoria_usada', 0):+.2f} MB

🔥 TOP CONSUMIDORES DE MEMÓRIA:
"""
        
        # Adicionar top stats de memória
        for i, stat in enumerate(sessao.get('snapshot_memoria', [])[:5], 1):
            relatorio += f"   {i}. {stat.traceback.format()[-1].strip()}: {stat.size / 1024:.1f} KB\n"
        
        return relatorio


# ============================================================================
# MONITOR DE RECURSOS
# ============================================================================

class MonitorRecursos:
    """Monitor de recursos do sistema durante execução."""
    
    def __init__(self, intervalo: float = 0.1):
        self.intervalo = intervalo
        self.monitorando = False
        self.dados = {
            'cpu': [],
            'memoria': [],
            'timestamps': []
        }
        self.thread_monitor = None
    
    def iniciar_monitoramento(self):
        """Inicia monitoramento de recursos."""
        if self.monitorando:
            return
        
        self.monitorando = True
        self.dados = {'cpu': [], 'memoria': [], 'timestamps': []}
        
        self.thread_monitor = threading.Thread(target=self._monitorar_recursos)
        self.thread_monitor.daemon = True
        self.thread_monitor.start()
        
        print("📊 Monitoramento de recursos iniciado")
    
    def parar_monitoramento(self) -> Dict[str, Any]:
        """Para monitoramento e retorna dados coletados."""
        if not self.monitorando:
            return self.dados
        
        self.monitorando = False
        
        if self.thread_monitor:
            self.thread_monitor.join(timeout=1.0)
        
        print("⏹️  Monitoramento de recursos parado")
        
        # Calcular estatísticas
        if self.dados['cpu']:
            estatisticas = {
                'cpu_media': sum(self.dados['cpu']) / len(self.dados['cpu']),
                'cpu_max': max(self.dados['cpu']),
                'memoria_media': sum(self.dados['memoria']) / len(self.dados['memoria']),
                'memoria_max': max(self.dados['memoria']),
                'duracao': len(self.dados['timestamps']) * self.intervalo
            }
            
            print(f"   CPU média: {estatisticas['cpu_media']:.1f}%")
            print(f"   CPU máxima: {estatisticas['cpu_max']:.1f}%")
            print(f"   Memória média: {estatisticas['memoria_media']:.1f} MB")
            print(f"   Memória máxima: {estatisticas['memoria_max']:.1f} MB")
            
            self.dados['estatisticas'] = estatisticas
        
        return self.dados
    
    def _monitorar_recursos(self):
        """Thread de monitoramento de recursos."""
        if PSUTIL_DISPONIVEL:
            processo = psutil.Process()
        
        while self.monitorando:
            try:
                # Coletar métricas
                if PSUTIL_DISPONIVEL:
                    cpu_percent = processo.cpu_percent()
                    memoria_mb = processo.memory_info().rss / 1024 / 1024
                else:
                    # Fallback básico sem psutil
                    cpu_percent = 0.0
                    memoria_mb = 0.0
                    
                timestamp = time.time()
                
                # Armazenar dados
                self.dados['cpu'].append(cpu_percent)
                self.dados['memoria'].append(memoria_mb)
                self.dados['timestamps'].append(timestamp)
                
                time.sleep(self.intervalo)
                
            except Exception as e:
                print(f"Erro no monitoramento: {e}")
                break
    
    def gerar_grafico_recursos(self, salvar_arquivo: str = None):
        """Gera gráfico dos recursos monitorados."""
        if not self.dados['timestamps']:
            print("Nenhum dado para gerar gráfico")
            return
        
        if not MATPLOTLIB_DISPONIVEL:
            print("⚠️  matplotlib não disponível - não é possível gerar gráficos")
            print("Para habilitar gráficos, instale: pip install matplotlib numpy")
            return
        
        try:
            # Criar subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            # Converter timestamps para tempo relativo
            tempo_inicial = self.dados['timestamps'][0]
            tempos = [(t - tempo_inicial) for t in self.dados['timestamps']]
            
            # Gráfico de CPU
            ax1.plot(tempos, self.dados['cpu'], 'b-', linewidth=2)
            ax1.set_ylabel('CPU (%)')
            ax1.set_title('Uso de Recursos do Sistema')
            ax1.grid(True, alpha=0.3)
            
            # Gráfico de Memória
            ax2.plot(tempos, self.dados['memoria'], 'r-', linewidth=2)
            ax2.set_xlabel('Tempo (s)')
            ax2.set_ylabel('Memória (MB)')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if salvar_arquivo:
                plt.savefig(salvar_arquivo, dpi=300, bbox_inches='tight')
                print(f"Gráfico salvo em: {salvar_arquivo}")
            else:
                plt.show()
                
        except Exception as e:
            print(f"Erro ao gerar gráfico: {e}")


# ============================================================================
# BENCHMARK SUITE
# ============================================================================

class BenchmarkSuite:
    """Suite completa de benchmarking."""
    
    def __init__(self):
        self.resultados = []
        self.configuracao = {
            'repeticoes': 5,
            'aquecimento': 2,
            'timeout': 30.0
        }
    
    def configurar(self, **kwargs):
        """Configura parâmetros do benchmark."""
        self.configuracao.update(kwargs)
    
    def benchmark_funcao(self, func: Callable, nome: str = None,
                        *args, **kwargs) -> Dict[str, Any]:
        """Executa benchmark de uma função."""
        nome = nome or func.__name__
        
        print(f"🏃 Executando benchmark: {nome}")
        
        # Aquecimento
        for _ in range(self.configuracao['aquecimento']):
            try:
                func(*args, **kwargs)
            except:
                pass
        
        # Coleta de métricas
        tempos = []
        memorias = []
        sucessos = 0
        
        for i in range(self.configuracao['repeticoes']):
            gc.collect()
            
            # Medir memória inicial
            memoria_inicial = self._obter_memoria()
            
            # Executar com timeout
            inicio = time.perf_counter()
            try:
                resultado = self._executar_com_timeout(
                    func, self.configuracao['timeout'], *args, **kwargs
                )
                sucesso = True
                sucessos += 1
            except Exception as e:
                resultado = e
                sucesso = False
            
            fim = time.perf_counter()
            
            # Medir memória final
            memoria_final = self._obter_memoria()
            
            tempo_execucao = fim - inicio
            memoria_usada = memoria_final - memoria_inicial
            
            tempos.append(tempo_execucao)
            memorias.append(memoria_usada)
            
            print(f"   Execução {i+1}: {tempo_execucao:.6f}s")
        
        # Calcular estatísticas
        if tempos:
            estatisticas = {
                'nome': nome,
                'tempo_medio': sum(tempos) / len(tempos),
                'tempo_min': min(tempos),
                'tempo_max': max(tempos),
                'tempo_desvio': self._calcular_desvio(tempos),
                'memoria_media': sum(memorias) / len(memorias),
                'memoria_max': max(memorias),
                'taxa_sucesso': sucessos / self.configuracao['repeticoes'],
                'timestamp': datetime.now()
            }
            
            self.resultados.append(estatisticas)
            self._exibir_resultado(estatisticas)
            
            return estatisticas
        
        return None
    
    def benchmark_comparativo(self, funcoes: Dict[str, Callable],
                            *args, **kwargs) -> Dict[str, Any]:
        """Executa benchmark comparativo de múltiplas funções."""
        print("🏁 Iniciando benchmark comparativo...")
        
        resultados_comparacao = {}
        
        for nome, func in funcoes.items():
            resultado = self.benchmark_funcao(func, nome, *args, **kwargs)
            if resultado:
                resultados_comparacao[nome] = resultado
        
        # Criar ranking
        ranking = sorted(
            resultados_comparacao.values(),
            key=lambda x: x['tempo_medio']
        )
        
        # Exibir comparação
        print("\n🏆 RANKING DE PERFORMANCE:")
        for i, resultado in enumerate(ranking, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
            print(f"   {emoji} {resultado['nome']}: {resultado['tempo_medio']:.6f}s")
        
        # Calcular speedup
        if len(ranking) > 1:
            print("\n⚡ SPEEDUP:")
            baseline = ranking[0]['tempo_medio']
            for resultado in ranking[1:]:
                speedup = resultado['tempo_medio'] / baseline
                print(f"   {resultado['nome']}: {speedup:.2f}x mais lento")
        
        return {
            'resultados': resultados_comparacao,
            'ranking': ranking,
            'timestamp': datetime.now()
        }
    
    def _executar_com_timeout(self, func: Callable, timeout: float,
                            *args, **kwargs):
        """Executa função com timeout."""
        import signal
        
        def handler(signum, frame):
            raise TimeoutError("Execução excedeu timeout")
        
        # Configurar timeout (apenas Unix)
        if hasattr(signal, 'SIGALRM'):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(int(timeout))
        
        try:
            resultado = func(*args, **kwargs)
        finally:
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
        
        return resultado
    
    def _obter_memoria(self) -> float:
        """Obtém uso atual de memória em MB."""
        try:
            processo = psutil.Process()
            return processo.memory_info().rss / 1024 / 1024
        except:
            return 0.0
    
    def _calcular_desvio(self, valores: List[float]) -> float:
        """Calcula desvio padrão."""
        if len(valores) <= 1:
            return 0.0
        
        media = sum(valores) / len(valores)
        variancia = sum((x - media) ** 2 for x in valores) / len(valores)
        return variancia ** 0.5
    
    def _exibir_resultado(self, resultado: Dict):
        """Exibe resultado formatado."""
        print(f"   ✅ Tempo médio: {resultado['tempo_medio']:.6f}s")
        print(f"   📊 Desvio: ±{resultado['tempo_desvio']:.6f}s")
        print(f"   💾 Memória: {resultado['memoria_media']:+.2f} MB")
        print(f"   ✔️  Taxa sucesso: {resultado['taxa_sucesso']:.1%}")
    
    def salvar_resultados(self, arquivo: str):
        """Salva resultados em arquivo."""
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, indent=2, default=str)
            print(f"Resultados salvos em: {arquivo}")
        except Exception as e:
            print(f"Erro ao salvar resultados: {e}")
    
    def gerar_relatorio_html(self, arquivo: str = "relatorio_performance.html"):
        """Gera relatório HTML dos resultados."""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Relatório de Performance</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .metric { background-color: #e8f4fd; }
    </style>
</head>
<body>
    <h1>📊 Relatório de Performance</h1>
    <p>Gerado em: {timestamp}</p>
    
    <h2>Resultados dos Benchmarks</h2>
    <table>
        <tr>
            <th>Função</th>
            <th>Tempo Médio (s)</th>
            <th>Tempo Min (s)</th>
            <th>Tempo Max (s)</th>
            <th>Desvio (s)</th>
            <th>Memória (MB)</th>
            <th>Taxa Sucesso</th>
        </tr>
""".format(timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        
        for resultado in self.resultados:
            html += f"""
        <tr>
            <td>{resultado['nome']}</td>
            <td class="metric">{resultado['tempo_medio']:.6f}</td>
            <td>{resultado['tempo_min']:.6f}</td>
            <td>{resultado['tempo_max']:.6f}</td>
            <td>{resultado['tempo_desvio']:.6f}</td>
            <td>{resultado['memoria_media']:+.2f}</td>
            <td>{resultado['taxa_sucesso']:.1%}</td>
        </tr>
"""
        
        html += """
    </table>
</body>
</html>
"""
        
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Relatório HTML gerado: {arquivo}")
        except Exception as e:
            print(f"Erro ao gerar relatório HTML: {e}")


# ============================================================================
# FUNÇÕES DE TESTE E DEMONSTRAÇÃO
# ============================================================================

def testar_performance_tools():
    """
    Testa todas as ferramentas de performance.
    """
    print("=== TESTE DAS FERRAMENTAS DE PERFORMANCE ===")
    print()
    
    # Funções de teste
    def bubble_sort(lista):
        n = len(lista)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista[j] > lista[j + 1]:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
        return lista
    
    def quick_sort(lista):
        if len(lista) <= 1:
            return lista
        pivot = lista[len(lista) // 2]
        esquerda = [x for x in lista if x < pivot]
        meio = [x for x in lista if x == pivot]
        direita = [x for x in lista if x > pivot]
        return quick_sort(esquerda) + meio + quick_sort(direita)
    
    def gerar_lista_aleatoria(tamanho):
        import random
        return [random.randint(1, 1000) for _ in range(tamanho)]
    
    # Teste 1: Análise de Complexidade
    print("1. ANÁLISE DE COMPLEXIDADE:")
    analisador = AnalisadorComplexidade()
    analisador.analisar_complexidade_temporal(bubble_sort, gerar_lista_aleatoria, "Bubble Sort")
    print()
    
    # Teste 2: Comparação de Algoritmos
    print("2. COMPARAÇÃO DE ALGORITMOS:")
    algoritmos = {
        'Bubble Sort': bubble_sort,
        'Quick Sort': quick_sort,
        'Python sorted': lambda x: sorted(x)
    }
    analisador.comparar_algoritmos(algoritmos, gerar_lista_aleatoria)
    print()
    
    # Teste 3: Profiler Avançado
    print("3. PROFILER AVANÇADO:")
    profiler = ProfilerAvancado()
    
    def operacao_complexa():
        # Simular operação que usa memória
        dados = [i ** 2 for i in range(10000)]
        return sum(dados)
    
    sessao = profiler.profile_funcao(operacao_complexa)
    print(profiler.gerar_relatorio_detalhado(f"operacao_complexa_{int(time.time())}"))
    
    # Teste 4: Benchmark Suite
    print("4. BENCHMARK SUITE:")
    suite = BenchmarkSuite()
    suite.configurar(repeticoes=3, aquecimento=1)
    
    # Benchmark de função simples
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    suite.benchmark_funcao(fibonacci, "Fibonacci Recursivo", 20)
    
    print("\n=== TESTE CONCLUÍDO ===")


if __name__ == "__main__":
    testar_performance_tools()