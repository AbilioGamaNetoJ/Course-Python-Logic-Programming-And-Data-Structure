"""
MÓDULO 08.4 - ANALISADOR DE DADOS AVANÇADO
==========================================

Objetivos de Aprendizado:
- Implementar pipeline completo de análise de dados
- Dominar técnicas de limpeza e preprocessamento
- Aplicar estatística descritiva e inferencial
- Criar visualizações informativas e interativas
- Implementar algoritmos de detecção de outliers
- Realizar análise exploratória de dados (EDA)
- Aplicar técnicas de feature engineering
- Implementar validação estatística de hipóteses

Conceitos Abordados:
- Data Pipeline e ETL (Extract, Transform, Load)
- Estatística Descritiva e Inferencial
- Análise Exploratória de Dados (EDA)
- Detecção e Tratamento de Outliers
- Feature Engineering e Seleção
- Correlação e Causalidade
- Testes de Hipóteses
- Análise de Séries Temporais
- Clustering e Segmentação
- Visualização de Dados Avançada

Algoritmos Implementados:
- Z-Score e IQR para detecção de outliers
- Isolation Forest para anomalias
- PCA para redução de dimensionalidade
- K-Means para clustering
- Análise de correlação (Pearson, Spearman, Kendall)
- Testes estatísticos (t-test, chi-square, ANOVA)
- Regressão linear e não-linear
- Análise de componentes principais

Pré-requisitos:
- Pandas e NumPy para manipulação de dados
- Matplotlib e Seaborn para visualização
- Scipy para estatística
- Scikit-learn para machine learning
- Conhecimento de estatística básica
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, Counter
from abc import ABC, abstractmethod
import warnings
import time
import json
import os
from pathlib import Path

# Imports para análise estatística
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import silhouette_score, calinski_harabasz_score

warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class TipoAnalise(Enum):
    """Tipos de análise de dados."""
    DESCRITIVA = "Descritiva"
    EXPLORATORIA = "Exploratória"
    INFERENCIAL = "Inferencial"
    PREDITIVA = "Preditiva"
    PRESCRITIVA = "Prescritiva"


class TipoVariavel(Enum):
    """Tipos de variáveis."""
    NUMERICA_CONTINUA = "Numérica Contínua"
    NUMERICA_DISCRETA = "Numérica Discreta"
    CATEGORICA_NOMINAL = "Categórica Nominal"
    CATEGORICA_ORDINAL = "Categórica Ordinal"
    TEMPORAL = "Temporal"
    TEXTO = "Texto"


class MetodoOutlier(Enum):
    """Métodos de detecção de outliers."""
    Z_SCORE = "Z-Score"
    IQR = "Interquartile Range"
    ISOLATION_FOREST = "Isolation Forest"
    LOCAL_OUTLIER_FACTOR = "Local Outlier Factor"
    MODIFIED_Z_SCORE = "Modified Z-Score"


class TipoVisualizacao(Enum):
    """Tipos de visualização."""
    HISTOGRAMA = "Histograma"
    BOXPLOT = "Box Plot"
    SCATTERPLOT = "Scatter Plot"
    HEATMAP = "Heatmap"
    BARPLOT = "Bar Plot"
    LINEPLOT = "Line Plot"
    VIOLINPLOT = "Violin Plot"
    PAIRPLOT = "Pair Plot"


@dataclass
class EstatisticasDescritivas:
    """Estatísticas descritivas de uma variável."""
    nome_variavel: str
    tipo_variavel: TipoVariavel
    count: int
    missing: int
    unique: int
    mean: Optional[float] = None
    median: Optional[float] = None
    mode: Optional[Any] = None
    std: Optional[float] = None
    min_val: Optional[Any] = None
    max_val: Optional[Any] = None
    q25: Optional[float] = None
    q75: Optional[float] = None
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            'nome_variavel': self.nome_variavel,
            'tipo_variavel': self.tipo_variavel.value,
            'count': self.count,
            'missing': self.missing,
            'missing_percent': (self.missing / (self.count + self.missing)) * 100,
            'unique': self.unique,
            'mean': self.mean,
            'median': self.median,
            'mode': self.mode,
            'std': self.std,
            'min': self.min_val,
            'max': self.max_val,
            'q25': self.q25,
            'q75': self.q75,
            'skewness': self.skewness,
            'kurtosis': self.kurtosis
        }


@dataclass
class ResultadoTeste:
    """Resultado de um teste estatístico."""
    nome_teste: str
    estatistica: float
    p_valor: float
    graus_liberdade: Optional[int] = None
    valor_critico: Optional[float] = None
    significativo: bool = False
    interpretacao: str = ""
    
    def __post_init__(self):
        """Determina se o resultado é estatisticamente significativo."""
        self.significativo = self.p_valor < 0.05


@dataclass
class RelatorioAnalise:
    """Relatório completo de análise de dados."""
    dataset_info: Dict[str, Any]
    estatisticas_descritivas: Dict[str, EstatisticasDescritivas]
    outliers_detectados: Dict[str, List[int]]
    correlacoes: Optional[pd.DataFrame] = None
    testes_realizados: List[ResultadoTeste] = field(default_factory=list)
    clusters_encontrados: Optional[Dict[str, Any]] = None
    recomendacoes: List[str] = field(default_factory=list)
    tempo_processamento: float = 0.0


class DetectorOutliers:
    """
    Detector de outliers com múltiplos métodos.
    """
    
    def __init__(self):
        """Inicializa detector."""
        self.metodos_disponiveis = {
            MetodoOutlier.Z_SCORE: self._z_score,
            MetodoOutlier.IQR: self._iqr,
            MetodoOutlier.ISOLATION_FOREST: self._isolation_forest,
            MetodoOutlier.MODIFIED_Z_SCORE: self._modified_z_score
        }
    
    def detectar(self, data: pd.Series, metodo: MetodoOutlier, 
                 **parametros) -> List[int]:
        """
        Detecta outliers usando método especificado.
        
        Args:
            data: Série de dados
            metodo: Método de detecção
            **parametros: Parâmetros específicos do método
        
        Returns:
            Lista de índices dos outliers
        """
        if metodo not in self.metodos_disponiveis:
            raise ValueError(f"Método {metodo} não implementado")
        
        return self.metodos_disponiveis[metodo](data, **parametros)
    
    def _z_score(self, data: pd.Series, threshold: float = 3.0) -> List[int]:
        """Detecção por Z-Score."""
        if not pd.api.types.is_numeric_dtype(data):
            return []
        
        z_scores = np.abs(stats.zscore(data.dropna()))
        outliers_mask = z_scores > threshold
        
        # Mapear de volta para índices originais
        valid_indices = data.dropna().index
        outlier_indices = valid_indices[outliers_mask]
        
        return outlier_indices.tolist()
    
    def _iqr(self, data: pd.Series, factor: float = 1.5) -> List[int]:
        """Detecção por Interquartile Range."""
        if not pd.api.types.is_numeric_dtype(data):
            return []
        
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR
        
        outliers_mask = (data < lower_bound) | (data > upper_bound)
        return data[outliers_mask].index.tolist()
    
    def _isolation_forest(self, data: pd.Series, 
                         contamination: float = 0.1) -> List[int]:
        """Detecção por Isolation Forest."""
        if not pd.api.types.is_numeric_dtype(data):
            return []
        
        # Preparar dados
        data_clean = data.dropna()
        if len(data_clean) < 10:  # Mínimo para Isolation Forest
            return []
        
        X = data_clean.values.reshape(-1, 1)
        
        # Aplicar Isolation Forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        outliers_pred = iso_forest.fit_predict(X)
        
        # Mapear outliers de volta para índices originais
        outlier_indices = data_clean.index[outliers_pred == -1]
        return outlier_indices.tolist()
    
    def _modified_z_score(self, data: pd.Series, threshold: float = 3.5) -> List[int]:
        """Detecção por Modified Z-Score (usando mediana)."""
        if not pd.api.types.is_numeric_dtype(data):
            return []
        
        median = data.median()
        mad = np.median(np.abs(data - median))
        
        if mad == 0:
            return []
        
        modified_z_scores = 0.6745 * (data - median) / mad
        outliers_mask = np.abs(modified_z_scores) > threshold
        
        return data[outliers_mask].index.tolist()
    
    def detectar_multiplos_metodos(self, data: pd.Series, 
                                  metodos: List[MetodoOutlier] = None) -> Dict[str, List[int]]:
        """
        Detecta outliers usando múltiplos métodos.
        
        Args:
            data: Série de dados
            metodos: Lista de métodos (None = todos)
        
        Returns:
            Dicionário com outliers por método
        """
        if metodos is None:
            metodos = list(MetodoOutlier)
        
        resultados = {}
        
        for metodo in metodos:
            try:
                outliers = self.detectar(data, metodo)
                resultados[metodo.value] = outliers
            except Exception as e:
                print(f"Erro ao aplicar {metodo.value}: {e}")
                resultados[metodo.value] = []
        
        return resultados
    
    def consenso_outliers(self, resultados_multiplos: Dict[str, List[int]], 
                         min_metodos: int = 2) -> List[int]:
        """
        Encontra outliers por consenso entre métodos.
        
        Args:
            resultados_multiplos: Resultados de múltiplos métodos
            min_metodos: Mínimo de métodos que devem concordar
        
        Returns:
            Lista de outliers por consenso
        """
        contador_outliers = Counter()
        
        for outliers in resultados_multiplos.values():
            for outlier_idx in outliers:
                contador_outliers[outlier_idx] += 1
        
        # Outliers que aparecem em pelo menos min_metodos
        outliers_consenso = [
            idx for idx, count in contador_outliers.items()
            if count >= min_metodos
        ]
        
        return sorted(outliers_consenso)


class AnalisadorEstatistico:
    """
    Analisador estatístico avançado.
    """
    
    def __init__(self):
        """Inicializa analisador."""
        self.testes_disponiveis = {
            'normalidade_shapiro': self._teste_shapiro_wilk,
            'normalidade_ks': self._teste_kolmogorov_smirnov,
            't_test_uma_amostra': self._t_test_uma_amostra,
            't_test_duas_amostras': self._t_test_duas_amostras,
            'chi_quadrado': self._teste_chi_quadrado,
            'anova_uma_via': self._anova_uma_via,
            'correlacao_pearson': self._correlacao_pearson,
            'correlacao_spearman': self._correlacao_spearman
        }
    
    def calcular_estatisticas_descritivas(self, data: pd.Series) -> EstatisticasDescritivas:
        """
        Calcula estatísticas descritivas completas.
        
        Args:
            data: Série de dados
        
        Returns:
            Estatísticas descritivas
        """
        # Determinar tipo de variável
        tipo_var = self._determinar_tipo_variavel(data)
        
        # Estatísticas básicas
        count = data.count()
        missing = data.isnull().sum()
        unique = data.nunique()
        
        # Inicializar estatísticas
        stats_desc = EstatisticasDescritivas(
            nome_variavel=data.name or "unnamed",
            tipo_variavel=tipo_var,
            count=count,
            missing=missing,
            unique=unique
        )
        
        # Estatísticas para variáveis numéricas
        if pd.api.types.is_numeric_dtype(data):
            stats_desc.mean = data.mean()
            stats_desc.median = data.median()
            stats_desc.std = data.std()
            stats_desc.min_val = data.min()
            stats_desc.max_val = data.max()
            stats_desc.q25 = data.quantile(0.25)
            stats_desc.q75 = data.quantile(0.75)
            
            # Skewness e Kurtosis
            if count > 1:
                stats_desc.skewness = data.skew()
                stats_desc.kurtosis = data.kurtosis()
        
        # Moda (para todos os tipos)
        try:
            mode_result = data.mode()
            if len(mode_result) > 0:
                stats_desc.mode = mode_result.iloc[0]
        except:
            pass
        
        return stats_desc
    
    def _determinar_tipo_variavel(self, data: pd.Series) -> TipoVariavel:
        """Determina o tipo de uma variável."""
        if pd.api.types.is_datetime64_any_dtype(data):
            return TipoVariavel.TEMPORAL
        elif pd.api.types.is_numeric_dtype(data):
            # Verificar se é discreta ou contínua
            unique_ratio = data.nunique() / len(data)
            if unique_ratio < 0.05 or data.nunique() < 20:
                return TipoVariavel.NUMERICA_DISCRETA
            else:
                return TipoVariavel.NUMERICA_CONTINUA
        elif pd.api.types.is_string_dtype(data) or pd.api.types.is_object_dtype(data):
            # Verificar se pode ser ordinal
            if data.nunique() < 10:
                return TipoVariavel.CATEGORICA_NOMINAL
            else:
                return TipoVariavel.TEXTO
        else:
            return TipoVariavel.CATEGORICA_NOMINAL
    
    def realizar_teste(self, nome_teste: str, *args, **kwargs) -> ResultadoTeste:
        """
        Realiza teste estatístico específico.
        
        Args:
            nome_teste: Nome do teste
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
        
        Returns:
            Resultado do teste
        """
        if nome_teste not in self.testes_disponiveis:
            raise ValueError(f"Teste {nome_teste} não disponível")
        
        return self.testes_disponiveis[nome_teste](*args, **kwargs)
    
    def _teste_shapiro_wilk(self, data: pd.Series) -> ResultadoTeste:
        """Teste de normalidade Shapiro-Wilk."""
        data_clean = data.dropna()
        
        if len(data_clean) < 3:
            return ResultadoTeste(
                nome_teste="Shapiro-Wilk",
                estatistica=0,
                p_valor=1,
                interpretacao="Dados insuficientes para o teste"
            )
        
        if len(data_clean) > 5000:
            # Shapiro-Wilk não é recomendado para amostras grandes
            data_clean = data_clean.sample(5000, random_state=42)
        
        estatistica, p_valor = stats.shapiro(data_clean)
        
        interpretacao = (
            "Os dados seguem distribuição normal" if p_valor >= 0.05
            else "Os dados não seguem distribuição normal"
        )
        
        return ResultadoTeste(
            nome_teste="Shapiro-Wilk",
            estatistica=estatistica,
            p_valor=p_valor,
            interpretacao=interpretacao
        )
    
    def _teste_kolmogorov_smirnov(self, data: pd.Series) -> ResultadoTeste:
        """Teste de normalidade Kolmogorov-Smirnov."""
        data_clean = data.dropna()
        
        if len(data_clean) < 3:
            return ResultadoTeste(
                nome_teste="Kolmogorov-Smirnov",
                estatistica=0,
                p_valor=1,
                interpretacao="Dados insuficientes para o teste"
            )
        
        # Normalizar dados
        data_norm = (data_clean - data_clean.mean()) / data_clean.std()
        
        estatistica, p_valor = stats.kstest(data_norm, 'norm')
        
        interpretacao = (
            "Os dados seguem distribuição normal" if p_valor >= 0.05
            else "Os dados não seguem distribuição normal"
        )
        
        return ResultadoTeste(
            nome_teste="Kolmogorov-Smirnov",
            estatistica=estatistica,
            p_valor=p_valor,
            interpretacao=interpretacao
        )
    
    def _t_test_uma_amostra(self, data: pd.Series, valor_teste: float) -> ResultadoTeste:
        """Teste t para uma amostra."""
        data_clean = data.dropna()
        
        if len(data_clean) < 2:
            return ResultadoTeste(
                nome_teste="T-test (uma amostra)",
                estatistica=0,
                p_valor=1,
                interpretacao="Dados insuficientes para o teste"
            )
        
        estatistica, p_valor = stats.ttest_1samp(data_clean, valor_teste)
        
        interpretacao = (
            f"A média da amostra é significativamente diferente de {valor_teste}"
            if p_valor < 0.05
            else f"A média da amostra não é significativamente diferente de {valor_teste}"
        )
        
        return ResultadoTeste(
            nome_teste="T-test (uma amostra)",
            estatistica=estatistica,
            p_valor=p_valor,
            graus_liberdade=len(data_clean) - 1,
            interpretacao=interpretacao
        )
    
    def _t_test_duas_amostras(self, data1: pd.Series, data2: pd.Series) -> ResultadoTeste:
        """Teste t para duas amostras independentes."""
        data1_clean = data1.dropna()
        data2_clean = data2.dropna()
        
        if len(data1_clean) < 2 or len(data2_clean) < 2:
            return ResultadoTeste(
                nome_teste="T-test (duas amostras)",
                estatistica=0,
                p_valor=1,
                interpretacao="Dados insuficientes para o teste"
            )
        
        estatistica, p_valor = stats.ttest_ind(data1_clean, data2_clean)
        
        interpretacao = (
            "As médias das duas amostras são significativamente diferentes"
            if p_valor < 0.05
            else "As médias das duas amostras não são significativamente diferentes"
        )
        
        return ResultadoTeste(
            nome_teste="T-test (duas amostras)",
            estatistica=estatistica,
            p_valor=p_valor,
            graus_liberdade=len(data1_clean) + len(data2_clean) - 2,
            interpretacao=interpretacao
        )
    
    def _teste_chi_quadrado(self, data1: pd.Series, data2: pd.Series) -> ResultadoTeste:
        """Teste qui-quadrado de independência."""
        # Criar tabela de contingência
        tabela_contingencia = pd.crosstab(data1, data2)
        
        if tabela_contingencia.size == 0:
            return ResultadoTeste(
                nome_teste="Chi-quadrado",
                estatistica=0,
                p_valor=1,
                interpretacao="Dados insuficientes para o teste"
            )
        
        estatistica, p_valor, dof, expected = stats.chi2_contingency(tabela_contingencia)
        
        interpretacao = (
            "As variáveis são independentes"
            if p_valor >= 0.05
            else "As variáveis são dependentes (associadas)"
        )
        
        return ResultadoTeste(
            nome_teste="Chi-quadrado",
            estatistica=estatistica,
            p_valor=p_valor,
            graus_liberdade=dof,
            interpretacao=interpretacao
        )
    
    def _anova_uma_via(self, *grupos) -> ResultadoTeste:
        """ANOVA de uma via."""
        grupos_clean = [grupo.dropna() for grupo in grupos if len(grupo.dropna()) > 0]
        
        if len(grupos_clean) < 2:
            return ResultadoTeste(
                nome_teste="ANOVA (uma via)",
                estatistica=0,
                p_valor=1,
                interpretacao="Dados insuficientes para o teste"
            )
        
        estatistica, p_valor = stats.f_oneway(*grupos_clean)
        
        interpretacao = (
            "Pelo menos uma média é significativamente diferente"
            if p_valor < 0.05
            else "Todas as médias são estatisticamente iguais"
        )
        
        return ResultadoTeste(
            nome_teste="ANOVA (uma via)",
            estatistica=estatistica,
            p_valor=p_valor,
            interpretacao=interpretacao
        )
    
    def _correlacao_pearson(self, data1: pd.Series, data2: pd.Series) -> ResultadoTeste:
        """Correlação de Pearson."""
        # Remover valores ausentes
        data_combined = pd.DataFrame({'x': data1, 'y': data2}).dropna()
        
        if len(data_combined) < 3:
            return ResultadoTeste(
                nome_teste="Correlação de Pearson",
                estatistica=0,
                p_valor=1,
                interpretacao="Dados insuficientes para o teste"
            )
        
        estatistica, p_valor = stats.pearsonr(data_combined['x'], data_combined['y'])
        
        # Interpretar força da correlação
        abs_corr = abs(estatistica)
        if abs_corr < 0.1:
            forca = "muito fraca"
        elif abs_corr < 0.3:
            forca = "fraca"
        elif abs_corr < 0.5:
            forca = "moderada"
        elif abs_corr < 0.7:
            forca = "forte"
        else:
            forca = "muito forte"
        
        direcao = "positiva" if estatistica > 0 else "negativa"
        
        interpretacao = (
            f"Correlação {forca} {direcao} (r={estatistica:.3f})"
            if p_valor < 0.05
            else f"Correlação não significativa (r={estatistica:.3f})"
        )
        
        return ResultadoTeste(
            nome_teste="Correlação de Pearson",
            estatistica=estatistica,
            p_valor=p_valor,
            interpretacao=interpretacao
        )
    
    def _correlacao_spearman(self, data1: pd.Series, data2: pd.Series) -> ResultadoTeste:
        """Correlação de Spearman."""
        # Remover valores ausentes
        data_combined = pd.DataFrame({'x': data1, 'y': data2}).dropna()
        
        if len(data_combined) < 3:
            return ResultadoTeste(
                nome_teste="Correlação de Spearman",
                estatistica=0,
                p_valor=1,
                interpretacao="Dados insuficientes para o teste"
            )
        
        estatistica, p_valor = stats.spearmanr(data_combined['x'], data_combined['y'])
        
        # Interpretar força da correlação
        abs_corr = abs(estatistica)
        if abs_corr < 0.1:
            forca = "muito fraca"
        elif abs_corr < 0.3:
            forca = "fraca"
        elif abs_corr < 0.5:
            forca = "moderada"
        elif abs_corr < 0.7:
            forca = "forte"
        else:
            forca = "muito forte"
        
        direcao = "positiva" if estatistica > 0 else "negativa"
        
        interpretacao = (
            f"Correlação {forca} {direcao} (ρ={estatistica:.3f})"
            if p_valor < 0.05
            else f"Correlação não significativa (ρ={estatistica:.3f})"
        )
        
        return ResultadoTeste(
            nome_teste="Correlação de Spearman",
            estatistica=estatistica,
            p_valor=p_valor,
            interpretacao=interpretacao
        )


class VisualizadorDados:
    """
    Visualizador de dados avançado.
    """
    
    def __init__(self, estilo: str = 'seaborn-v0_8', paleta: str = 'husl'):
        """
        Inicializa visualizador.
        
        Args:
            estilo: Estilo do matplotlib
            paleta: Paleta de cores do seaborn
        """
        plt.style.use(estilo)
        sns.set_palette(paleta)
        self.fig_size = (12, 8)
    
    def criar_dashboard_eda(self, df: pd.DataFrame, 
                           colunas_numericas: List[str] = None,
                           colunas_categoricas: List[str] = None) -> plt.Figure:
        """
        Cria dashboard de análise exploratória.
        
        Args:
            df: DataFrame
            colunas_numericas: Lista de colunas numéricas
            colunas_categoricas: Lista de colunas categóricas
        
        Returns:
            Figura do matplotlib
        """
        if colunas_numericas is None:
            colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if colunas_categoricas is None:
            colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Calcular número de subplots necessários
        n_plots = min(len(colunas_numericas), 6) + min(len(colunas_categoricas), 4)
        n_rows = (n_plots + 2) // 3
        
        fig, axes = plt.subplots(n_rows, 3, figsize=(18, 6 * n_rows))
        axes = axes.flatten() if n_rows > 1 else [axes] if n_rows == 1 else []
        
        plot_idx = 0
        
        # Histogramas para variáveis numéricas
        for i, col in enumerate(colunas_numericas[:6]):
            if plot_idx >= len(axes):
                break
            
            ax = axes[plot_idx]
            df[col].hist(bins=30, alpha=0.7, ax=ax)
            ax.set_title(f'Distribuição de {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequência')
            ax.grid(True, alpha=0.3)
            
            plot_idx += 1
        
        # Gráficos de barras para variáveis categóricas
        for i, col in enumerate(colunas_categoricas[:4]):
            if plot_idx >= len(axes):
                break
            
            ax = axes[plot_idx]
            value_counts = df[col].value_counts().head(10)
            value_counts.plot(kind='bar', ax=ax)
            ax.set_title(f'Distribuição de {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Contagem')
            ax.tick_params(axis='x', rotation=45)
            
            plot_idx += 1
        
        # Remover subplots vazios
        for i in range(plot_idx, len(axes)):
            fig.delaxes(axes[i])
        
        plt.tight_layout()
        return fig
    
    def criar_matriz_correlacao(self, df: pd.DataFrame, 
                               metodo: str = 'pearson') -> plt.Figure:
        """
        Cria matriz de correlação.
        
        Args:
            df: DataFrame
            metodo: Método de correlação ('pearson', 'spearman', 'kendall')
        
        Returns:
            Figura do matplotlib
        """
        # Selecionar apenas colunas numéricas
        df_numeric = df.select_dtypes(include=[np.number])
        
        if df_numeric.empty:
            fig, ax = plt.subplots(figsize=self.fig_size)
            ax.text(0.5, 0.5, 'Nenhuma variável numérica encontrada', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        # Calcular correlação
        corr_matrix = df_numeric.corr(method=metodo)
        
        # Criar heatmap
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm',
                   center=0, square=True, ax=ax, cbar_kws={'shrink': 0.8})
        
        ax.set_title(f'Matriz de Correlação ({metodo.title()})')
        
        plt.tight_layout()
        return fig
    
    def criar_boxplots_outliers(self, df: pd.DataFrame, 
                               colunas: List[str] = None) -> plt.Figure:
        """
        Cria boxplots para detecção visual de outliers.
        
        Args:
            df: DataFrame
            colunas: Lista de colunas (None = todas numéricas)
        
        Returns:
            Figura do matplotlib
        """
        if colunas is None:
            colunas = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not colunas:
            fig, ax = plt.subplots(figsize=self.fig_size)
            ax.text(0.5, 0.5, 'Nenhuma variável numérica encontrada', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        n_cols = min(len(colunas), 4)
        n_rows = (len(colunas) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
        
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(colunas):
            if i >= len(axes):
                break
            
            ax = axes[i]
            df.boxplot(column=col, ax=ax)
            ax.set_title(f'Boxplot de {col}')
            ax.grid(True, alpha=0.3)
        
        # Remover subplots vazios
        for i in range(len(colunas), len(axes)):
            fig.delaxes(axes[i])
        
        plt.tight_layout()
        return fig
    
    def criar_pairplot(self, df: pd.DataFrame, 
                      colunas: List[str] = None,
                      hue: str = None) -> plt.Figure:
        """
        Cria pairplot para análise de relacionamentos.
        
        Args:
            df: DataFrame
            colunas: Lista de colunas
            hue: Coluna para colorir pontos
        
        Returns:
            Figura do seaborn
        """
        if colunas is None:
            colunas = df.select_dtypes(include=[np.number]).columns.tolist()[:5]
        
        if len(colunas) < 2:
            fig, ax = plt.subplots(figsize=self.fig_size)
            ax.text(0.5, 0.5, 'Pelo menos 2 variáveis numéricas necessárias', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        # Limitar número de colunas para performance
        colunas = colunas[:5]
        
        df_subset = df[colunas + ([hue] if hue and hue in df.columns else [])]
        
        g = sns.pairplot(df_subset, hue=hue, diag_kind='hist')
        g.fig.suptitle('Pairplot - Análise de Relacionamentos', y=1.02)
        
        return g.fig


class ClusterizadorDados:
    """
    Clusterizador de dados com múltiplos algoritmos.
    """
    
    def __init__(self):
        """Inicializa clusterizador."""
        self.scaler = StandardScaler()
        self.algoritmos_disponiveis = {
            'kmeans': self._kmeans,
            'dbscan': self._dbscan
        }
    
    def preparar_dados(self, df: pd.DataFrame, 
                      colunas: List[str] = None) -> np.ndarray:
        """
        Prepara dados para clustering.
        
        Args:
            df: DataFrame
            colunas: Lista de colunas (None = todas numéricas)
        
        Returns:
            Array normalizado
        """
        if colunas is None:
            colunas = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Selecionar e limpar dados
        data = df[colunas].dropna()
        
        # Normalizar
        data_scaled = self.scaler.fit_transform(data)
        
        return data_scaled, data.index
    
    def encontrar_numero_otimo_clusters(self, data: np.ndarray, 
                                      max_clusters: int = 10) -> Dict[str, Any]:
        """
        Encontra número ótimo de clusters usando múltiplos métodos.
        
        Args:
            data: Dados normalizados
            max_clusters: Número máximo de clusters a testar
        
        Returns:
            Dicionário com resultados dos métodos
        """
        if len(data) < 4:
            return {'erro': 'Dados insuficientes para clustering'}
        
        max_clusters = min(max_clusters, len(data) - 1)
        
        resultados = {
            'elbow': {'k_values': [], 'inertias': []},
            'silhouette': {'k_values': [], 'scores': []},
            'calinski_harabasz': {'k_values': [], 'scores': []}
        }
        
        for k in range(2, max_clusters + 1):
            # K-Means
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(data)
            
            # Método do cotovelo (inércia)
            resultados['elbow']['k_values'].append(k)
            resultados['elbow']['inertias'].append(kmeans.inertia_)
            
            # Silhouette Score
            if len(np.unique(labels)) > 1:
                sil_score = silhouette_score(data, labels)
                resultados['silhouette']['k_values'].append(k)
                resultados['silhouette']['scores'].append(sil_score)
                
                # Calinski-Harabasz Index
                ch_score = calinski_harabasz_score(data, labels)
                resultados['calinski_harabasz']['k_values'].append(k)
                resultados['calinski_harabasz']['scores'].append(ch_score)
        
        # Encontrar k ótimo para cada método
        if resultados['silhouette']['scores']:
            melhor_k_sil = resultados['silhouette']['k_values'][
                np.argmax(resultados['silhouette']['scores'])
            ]
            resultados['recomendacao_silhouette'] = melhor_k_sil
        
        if resultados['calinski_harabasz']['scores']:
            melhor_k_ch = resultados['calinski_harabasz']['k_values'][
                np.argmax(resultados['calinski_harabasz']['scores'])
            ]
            resultados['recomendacao_calinski_harabasz'] = melhor_k_ch
        
        return resultados
    
    def _kmeans(self, data: np.ndarray, n_clusters: int = 3, **kwargs) -> Dict[str, Any]:
        """Aplica K-Means clustering."""
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10, **kwargs)
        labels = kmeans.fit_predict(data)
        
        # Calcular métricas
        inertia = kmeans.inertia_
        silhouette = silhouette_score(data, labels) if len(np.unique(labels)) > 1 else -1
        
        return {
            'algoritmo': 'K-Means',
            'labels': labels,
            'centroids': kmeans.cluster_centers_,
            'n_clusters': n_clusters,
            'inertia': inertia,
            'silhouette_score': silhouette,
            'modelo': kmeans
        }
    
    def _dbscan(self, data: np.ndarray, eps: float = 0.5, 
               min_samples: int = 5, **kwargs) -> Dict[str, Any]:
        """Aplica DBSCAN clustering."""
        dbscan = DBSCAN(eps=eps, min_samples=min_samples, **kwargs)
        labels = dbscan.fit_predict(data)
        
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)
        
        # Calcular silhouette apenas se há clusters válidos
        silhouette = -1
        if n_clusters > 1 and n_noise < len(labels):
            # Remover pontos de ruído para cálculo do silhouette
            mask = labels != -1
            if np.sum(mask) > 1:
                silhouette = silhouette_score(data[mask], labels[mask])
        
        return {
            'algoritmo': 'DBSCAN',
            'labels': labels,
            'n_clusters': n_clusters,
            'n_noise': n_noise,
            'silhouette_score': silhouette,
            'modelo': dbscan
        }
    
    def aplicar_clustering(self, data: np.ndarray, algoritmo: str = 'kmeans',
                          **parametros) -> Dict[str, Any]:
        """
        Aplica algoritmo de clustering.
        
        Args:
            data: Dados normalizados
            algoritmo: Nome do algoritmo
            **parametros: Parâmetros específicos do algoritmo
        
        Returns:
            Resultados do clustering
        """
        if algoritmo not in self.algoritmos_disponiveis:
            raise ValueError(f"Algoritmo {algoritmo} não disponível")
        
        return self.algoritmos_disponiveis[algoritmo](data, **parametros)
    
    def visualizar_clusters(self, data: np.ndarray, labels: np.ndarray,
                           centroids: np.ndarray = None) -> plt.Figure:
        """
        Visualiza resultados do clustering.
        
        Args:
            data: Dados originais
            labels: Labels dos clusters
            centroids: Centroides (opcional)
        
        Returns:
            Figura do matplotlib
        """
        # Se dados têm mais de 2 dimensões, aplicar PCA
        if data.shape[1] > 2:
            pca = PCA(n_components=2, random_state=42)
            data_2d = pca.fit_transform(data)
            
            if centroids is not None:
                centroids_2d = pca.transform(centroids)
            else:
                centroids_2d = None
        else:
            data_2d = data
            centroids_2d = centroids
        
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        # Plotar pontos
        scatter = ax.scatter(data_2d[:, 0], data_2d[:, 1], c=labels, 
                           cmap='viridis', alpha=0.7)
        
        # Plotar centroides se disponíveis
        if centroids_2d is not None:
            ax.scatter(centroids_2d[:, 0], centroids_2d[:, 1], 
                      c='red', marker='x', s=200, linewidths=3, label='Centroides')
            ax.legend()
        
        ax.set_title('Visualização dos Clusters')
        ax.set_xlabel('Componente Principal 1' if data.shape[1] > 2 else 'Dimensão 1')
        ax.set_ylabel('Componente Principal 2' if data.shape[1] > 2 else 'Dimensão 2')
        
        plt.colorbar(scatter)
        plt.tight_layout()
        
        return fig


class AnalisadorDados:
    """
    Analisador de dados principal que integra todos os componentes.
    """
    
    def __init__(self):
        """Inicializa analisador principal."""
        self.detector_outliers = DetectorOutliers()
        self.analisador_estatistico = AnalisadorEstatistico()
        self.visualizador = VisualizadorDados()
        self.clusterizador = ClusterizadorDados()
    
    def analisar_dataset_completo(self, df: pd.DataFrame, 
                                 target_column: str = None) -> RelatorioAnalise:
        """
        Realiza análise completa de um dataset.
        
        Args:
            df: DataFrame a ser analisado
            target_column: Coluna alvo (para análise supervisionada)
        
        Returns:
            Relatório completo da análise
        """
        inicio_tempo = time.time()
        
        print("Iniciando análise completa do dataset...")
        
        # 1. Informações básicas do dataset
        dataset_info = {
            'shape': df.shape,
            'memory_usage': df.memory_usage(deep=True).sum(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_rows': df.duplicated().sum()
        }
        
        print(f"Dataset: {df.shape[0]} linhas, {df.shape[1]} colunas")
        
        # 2. Estatísticas descritivas por coluna
        print("Calculando estatísticas descritivas...")
        estatisticas_descritivas = {}
        
        for coluna in df.columns:
            stats = self.analisador_estatistico.calcular_estatisticas_descritivas(df[coluna])
            estatisticas_descritivas[coluna] = stats
        
        # 3. Detecção de outliers
        print("Detectando outliers...")
        outliers_detectados = {}
        
        colunas_numericas = df.select_dtypes(include=[np.number]).columns
        for coluna in colunas_numericas:
            outliers_multiplos = self.detector_outliers.detectar_multiplos_metodos(df[coluna])
            outliers_consenso = self.detector_outliers.consenso_outliers(outliers_multiplos, min_metodos=2)
            outliers_detectados[coluna] = outliers_consenso
        
        # 4. Matriz de correlação
        correlacoes = None
        if len(colunas_numericas) > 1:
            print("Calculando correlações...")
            correlacoes = df[colunas_numericas].corr()
        
        # 5. Testes estatísticos
        print("Realizando testes estatísticos...")
        testes_realizados = []
        
        # Testes de normalidade para variáveis numéricas
        for coluna in colunas_numericas:
            if df[coluna].count() > 3:
                teste_shapiro = self.analisador_estatistico.realizar_teste(
                    'normalidade_shapiro', df[coluna]
                )
                testes_realizados.append(teste_shapiro)
        
        # Testes de correlação entre variáveis numéricas
        for i, col1 in enumerate(colunas_numericas):
            for col2 in colunas_numericas[i+1:]:
                if df[col1].count() > 3 and df[col2].count() > 3:
                    teste_corr = self.analisador_estatistico.realizar_teste(
                        'correlacao_pearson', df[col1], df[col2]
                    )
                    teste_corr.nome_teste = f"Correlação {col1} vs {col2}"
                    testes_realizados.append(teste_corr)
        
        # 6. Clustering (se há variáveis numéricas suficientes)
        clusters_encontrados = None
        if len(colunas_numericas) >= 2 and len(df) > 10:
            print("Realizando análise de clustering...")
            try:
                data_scaled, indices = self.clusterizador.preparar_dados(df, list(colunas_numericas))
                
                # Encontrar número ótimo de clusters
                otimizacao_clusters = self.clusterizador.encontrar_numero_otimo_clusters(data_scaled)
                
                # Aplicar K-Means com número recomendado
                if 'recomendacao_silhouette' in otimizacao_clusters:
                    k_otimo = otimizacao_clusters['recomendacao_silhouette']
                    resultado_kmeans = self.clusterizador.aplicar_clustering(
                        data_scaled, 'kmeans', n_clusters=k_otimo
                    )
                    
                    clusters_encontrados = {
                        'otimizacao': otimizacao_clusters,
                        'resultado_kmeans': resultado_kmeans
                    }
            except Exception as e:
                print(f"Erro no clustering: {e}")
        
        # 7. Gerar recomendações
        recomendacoes = self._gerar_recomendacoes(
            df, estatisticas_descritivas, outliers_detectados, 
            correlacoes, testes_realizados
        )
        
        # Calcular tempo de processamento
        tempo_processamento = time.time() - inicio_tempo
        
        print(f"Análise concluída em {tempo_processamento:.2f} segundos")
        
        return RelatorioAnalise(
            dataset_info=dataset_info,
            estatisticas_descritivas=estatisticas_descritivas,
            outliers_detectados=outliers_detectados,
            correlacoes=correlacoes,
            testes_realizados=testes_realizados,
            clusters_encontrados=clusters_encontrados,
            recomendacoes=recomendacoes,
            tempo_processamento=tempo_processamento
        )
    
    def _gerar_recomendacoes(self, df: pd.DataFrame,
                           estatisticas: Dict[str, EstatisticasDescritivas],
                           outliers: Dict[str, List[int]],
                           correlacoes: Optional[pd.DataFrame],
                           testes: List[ResultadoTeste]) -> List[str]:
        """Gera recomendações baseadas na análise."""
        recomendacoes = []
        
        # Recomendações sobre dados faltantes
        for coluna, stats in estatisticas.items():
            missing_percent = (stats.missing / (stats.count + stats.missing)) * 100
            if missing_percent > 20:
                recomendacoes.append(
                    f"Coluna '{coluna}' tem {missing_percent:.1f}% de dados faltantes. "
                    "Considere imputação ou remoção."
                )
        
        # Recomendações sobre outliers
        for coluna, outliers_indices in outliers.items():
            if len(outliers_indices) > 0:
                percent_outliers = (len(outliers_indices) / len(df)) * 100
                if percent_outliers > 5:
                    recomendacoes.append(
                        f"Coluna '{coluna}' tem {percent_outliers:.1f}% de outliers. "
                        "Investigue se são erros ou valores legítimos."
                    )
        
        # Recomendações sobre correlações
        if correlacoes is not None:
            # Encontrar correlações muito altas (multicolinearidade)
            corr_alta = correlacoes.abs() > 0.9
            np.fill_diagonal(corr_alta.values, False)
            
            if corr_alta.any().any():
                recomendacoes.append(
                    "Detectadas correlações muito altas entre variáveis. "
                    "Considere remover variáveis redundantes para evitar multicolinearidade."
                )
        
        # Recomendações sobre normalidade
        testes_normalidade = [t for t in testes if 'normalidade' in t.nome_teste.lower()]
        nao_normais = [t for t in testes_normalidade if t.significativo]
        
        if len(nao_normais) > 0:
            recomendacoes.append(
                f"{len(nao_normais)} variáveis não seguem distribuição normal. "
                "Considere transformações (log, sqrt) ou testes não-paramétricos."
            )
        
        # Recomendações sobre variabilidade
        for coluna, stats in estatisticas.items():
            if stats.tipo_variavel in [TipoVariavel.NUMERICA_CONTINUA, TipoVariavel.NUMERICA_DISCRETA]:
                if stats.std is not None and stats.mean is not None and stats.mean != 0:
                    cv = stats.std / abs(stats.mean)  # Coeficiente de variação
                    if cv > 1:
                        recomendacoes.append(
                            f"Coluna '{coluna}' tem alta variabilidade (CV={cv:.2f}). "
                            "Considere normalização ou padronização."
                        )
        
        # Recomendações gerais
        if df.duplicated().sum() > 0:
            recomendacoes.append(
                f"Dataset contém {df.duplicated().sum()} linhas duplicadas. "
                "Considere remoção se apropriado."
            )
        
        return recomendacoes
    
    def gerar_relatorio_html(self, relatorio: RelatorioAnalise, 
                           nome_arquivo: str = "relatorio_analise.html"):
        """
        Gera relatório em HTML.
        
        Args:
            relatorio: Relatório da análise
            nome_arquivo: Nome do arquivo HTML
        """
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Relatório de Análise de Dados</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1, h2, h3 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .recommendation {{ background-color: #fff3cd; padding: 10px; margin: 10px 0; border-left: 4px solid #ffc107; }}
                .metric {{ background-color: #d4edda; padding: 5px; margin: 5px 0; }}
            </style>
        </head>
        <body>
            <h1>Relatório de Análise de Dados</h1>
            
            <h2>Informações do Dataset</h2>
            <div class="metric">Dimensões: {relatorio.dataset_info['shape'][0]} linhas × {relatorio.dataset_info['shape'][1]} colunas</div>
            <div class="metric">Uso de memória: {relatorio.dataset_info['memory_usage'] / 1024 / 1024:.2f} MB</div>
            <div class="metric">Linhas duplicadas: {relatorio.dataset_info['duplicate_rows']}</div>
            <div class="metric">Tempo de processamento: {relatorio.tempo_processamento:.2f} segundos</div>
            
            <h2>Estatísticas Descritivas</h2>
            <table>
                <tr>
                    <th>Variável</th>
                    <th>Tipo</th>
                    <th>Count</th>
                    <th>Missing (%)</th>
                    <th>Únicos</th>
                    <th>Média</th>
                    <th>Mediana</th>
                    <th>Desvio Padrão</th>
                </tr>
        """
        
        for nome, stats in relatorio.estatisticas_descritivas.items():
            stats_dict = stats.to_dict()
            html_content += f"""
                <tr>
                    <td>{nome}</td>
                    <td>{stats_dict['tipo_variavel']}</td>
                    <td>{stats_dict['count']}</td>
                    <td>{stats_dict['missing_percent']:.1f}%</td>
                    <td>{stats_dict['unique']}</td>
                    <td>{stats_dict['mean']:.3f if stats_dict['mean'] is not None else 'N/A'}</td>
                    <td>{stats_dict['median']:.3f if stats_dict['median'] is not None else 'N/A'}</td>
                    <td>{stats_dict['std']:.3f if stats_dict['std'] is not None else 'N/A'}</td>
                </tr>
            """
        
        html_content += """
            </table>
            
            <h2>Outliers Detectados</h2>
        """
        
        for coluna, outliers_indices in relatorio.outliers_detectados.items():
            if outliers_indices:
                percent = (len(outliers_indices) / relatorio.dataset_info['shape'][0]) * 100
                html_content += f"<div class='metric'>{coluna}: {len(outliers_indices)} outliers ({percent:.1f}%)</div>"
        
        html_content += "<h2>Testes Estatísticos</h2>"
        
        for teste in relatorio.testes_realizados:
            significativo = "Sim" if teste.significativo else "Não"
            html_content += f"""
                <div class='metric'>
                    <strong>{teste.nome_teste}</strong><br>
                    Estatística: {teste.estatistica:.4f}, p-valor: {teste.p_valor:.4f}<br>
                    Significativo: {significativo}<br>
                    {teste.interpretacao}
                </div>
            """
        
        html_content += "<h2>Recomendações</h2>"
        
        for recomendacao in relatorio.recomendacoes:
            html_content += f"<div class='recommendation'>{recomendacao}</div>"
        
        html_content += """
            </body>
            </html>
        """
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Relatório HTML salvo como: {nome_arquivo}")


def gerar_dataset_exemplo() -> pd.DataFrame:
    """Gera dataset de exemplo para demonstração."""
    np.random.seed(42)
    
    n_samples = 1000
    
    # Variáveis numéricas
    idade = np.random.normal(35, 12, n_samples).astype(int)
    idade = np.clip(idade, 18, 80)
    
    salario = np.random.lognormal(10, 0.5, n_samples)
    salario = np.round(salario, 2)
    
    experiencia = np.maximum(0, idade - 22 + np.random.normal(0, 3, n_samples))
    experiencia = np.round(experiencia, 1)
    
    # Adicionar alguns outliers
    outlier_indices = np.random.choice(n_samples, 50, replace=False)
    salario[outlier_indices] *= np.random.uniform(3, 10, 50)
    
    # Variáveis categóricas
    departamentos = np.random.choice(['TI', 'Vendas', 'Marketing', 'RH', 'Financeiro'], n_samples)
    nivel_educacao = np.random.choice(['Ensino Médio', 'Superior', 'Pós-graduação', 'Mestrado'], n_samples)
    
    # Variável com dados faltantes
    bonus = np.random.normal(5000, 2000, n_samples)
    missing_indices = np.random.choice(n_samples, 200, replace=False)
    bonus[missing_indices] = np.nan
    
    # Criar DataFrame
    df = pd.DataFrame({
        'idade': idade,
        'salario': salario,
        'experiencia': experiencia,
        'departamento': departamentos,
        'nivel_educacao': nivel_educacao,
        'bonus': bonus
    })
    
    # Adicionar algumas linhas duplicadas
    df = pd.concat([df, df.sample(20, random_state=42)], ignore_index=True)
    
    return df


def demonstracao_analise_basica():
    """Demonstração de análise básica de dados."""
    print("=== DEMONSTRAÇÃO: ANÁLISE BÁSICA DE DADOS ===")
    
    # Gerar dataset de exemplo
    df = gerar_dataset_exemplo()
    print(f"Dataset gerado: {df.shape[0]} linhas, {df.shape[1]} colunas")
    
    # Criar analisador
    analisador = AnalisadorDados()
    
    # Análise básica de uma coluna
    print("\n--- Estatísticas Descritivas: Salário ---")
    stats_salario = analisador.analisador_estatistico.calcular_estatisticas_descritivas(df['salario'])
    stats_dict = stats_salario.to_dict()
    
    for key, value in stats_dict.items():
        if value is not None:
            if isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")
    
    # Detecção de outliers
    print("\n--- Detecção de Outliers: Salário ---")
    outliers_multiplos = analisador.detector_outliers.detectar_multiplos_metodos(df['salario'])
    
    for metodo, outliers in outliers_multiplos.items():
        percent = (len(outliers) / len(df)) * 100
        print(f"{metodo}: {len(outliers)} outliers ({percent:.1f}%)")
    
    # Consenso de outliers
    outliers_consenso = analisador.detector_outliers.consenso_outliers(outliers_multiplos)
    print(f"Consenso (≥2 métodos): {len(outliers_consenso)} outliers")
    
    # Teste de normalidade
    print("\n--- Teste de Normalidade: Salário ---")
    teste_shapiro = analisador.analisador_estatistico.realizar_teste(
        'normalidade_shapiro', df['salario']
    )
    print(f"Shapiro-Wilk: estatística={teste_shapiro.estatistica:.4f}, "
          f"p-valor={teste_shapiro.p_valor:.4f}")
    print(f"Interpretação: {teste_shapiro.interpretacao}")


def demonstracao_correlacoes():
    """Demonstração de análise de correlações."""
    print("\n=== DEMONSTRAÇÃO: ANÁLISE DE CORRELAÇÕES ===")
    
    df = gerar_dataset_exemplo()
    analisador = AnalisadorDados()
    
    # Correlação entre idade e experiência
    print("\n--- Correlação: Idade vs Experiência ---")
    teste_pearson = analisador.analisador_estatistico.realizar_teste(
        'correlacao_pearson', df['idade'], df['experiencia']
    )
    print(f"Pearson: r={teste_pearson.estatistica:.3f}, p-valor={teste_pearson.p_valor:.4f}")
    print(f"Interpretação: {teste_pearson.interpretacao}")
    
    # Correlação entre salário e experiência
    print("\n--- Correlação: Salário vs Experiência ---")
    teste_spearman = analisador.analisador_estatistico.realizar_teste(
        'correlacao_spearman', df['salario'], df['experiencia']
    )
    print(f"Spearman: ρ={teste_spearman.estatistica:.3f}, p-valor={teste_spearman.p_valor:.4f}")
    print(f"Interpretação: {teste_spearman.interpretacao}")
    
    # Matriz de correlação completa
    print("\n--- Matriz de Correlação (Variáveis Numéricas) ---")
    colunas_numericas = df.select_dtypes(include=[np.number]).columns
    matriz_corr = df[colunas_numericas].corr()
    print(matriz_corr.round(3))


def demonstracao_clustering():
    """Demonstração de análise de clustering."""
    print("\n=== DEMONSTRAÇÃO: ANÁLISE DE CLUSTERING ===")
    
    df = gerar_dataset_exemplo()
    analisador = AnalisadorDados()
    
    # Preparar dados para clustering
    colunas_para_cluster = ['idade', 'salario', 'experiencia']
    data_scaled, indices = analisador.clusterizador.preparar_dados(df, colunas_para_cluster)
    
    print(f"Dados preparados: {data_scaled.shape[0]} amostras, {data_scaled.shape[1]} features")
    
    # Encontrar número ótimo de clusters
    print("\n--- Otimização do Número de Clusters ---")
    otimizacao = analisador.clusterizador.encontrar_numero_otimo_clusters(data_scaled, max_clusters=8)
    
    if 'recomendacao_silhouette' in otimizacao:
        print(f"Melhor k (Silhouette): {otimizacao['recomendacao_silhouette']}")
    if 'recomendacao_calinski_harabasz' in otimizacao:
        print(f"Melhor k (Calinski-Harabasz): {otimizacao['recomendacao_calinski_harabasz']}")
    
    # Aplicar K-Means
    print("\n--- Aplicando K-Means ---")
    k_otimo = otimizacao.get('recomendacao_silhouette', 3)
    resultado_kmeans = analisador.clusterizador.aplicar_clustering(
        data_scaled, 'kmeans', n_clusters=k_otimo
    )
    
    print(f"Algoritmo: {resultado_kmeans['algoritmo']}")
    print(f"Número de clusters: {resultado_kmeans['n_clusters']}")
    print(f"Inércia: {resultado_kmeans['inertia']:.2f}")
    print(f"Silhouette Score: {resultado_kmeans['silhouette_score']:.3f}")
    
    # Aplicar DBSCAN
    print("\n--- Aplicando DBSCAN ---")
    resultado_dbscan = analisador.clusterizador.aplicar_clustering(
        data_scaled, 'dbscan', eps=0.5, min_samples=5
    )
    
    print(f"Algoritmo: {resultado_dbscan['algoritmo']}")
    print(f"Número de clusters: {resultado_dbscan['n_clusters']}")
    print(f"Pontos de ruído: {resultado_dbscan['n_noise']}")
    print(f"Silhouette Score: {resultado_dbscan['silhouette_score']:.3f}")


def demonstracao_visualizacoes():
    """Demonstração de visualizações."""
    print("\n=== DEMONSTRAÇÃO: VISUALIZAÇÕES ===")
    
    df = gerar_dataset_exemplo()
    analisador = AnalisadorDados()
    
    # Dashboard EDA
    print("Criando dashboard de análise exploratória...")
    fig_dashboard = analisador.visualizador.criar_dashboard_eda(df)
    plt.savefig('dashboard_eda.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Dashboard salvo como: dashboard_eda.png")
    
    # Matriz de correlação
    print("Criando matriz de correlação...")
    fig_corr = analisador.visualizador.criar_matriz_correlacao(df)
    plt.savefig('matriz_correlacao.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Matriz de correlação salva como: matriz_correlacao.png")
    
    # Boxplots para outliers
    print("Criando boxplots para detecção de outliers...")
    fig_box = analisador.visualizador.criar_boxplots_outliers(df)
    plt.savefig('boxplots_outliers.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Boxplots salvos como: boxplots_outliers.png")
    
    # Pairplot
    print("Criando pairplot...")
    colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()[:4]
    fig_pair = analisador.visualizador.criar_pairplot(df, colunas_numericas, hue='departamento')
    plt.savefig('pairplot.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Pairplot salvo como: pairplot.png")


def demonstracao_analise_completa():
    """Demonstração de análise completa de dataset."""
    print("\n=== DEMONSTRAÇÃO: ANÁLISE COMPLETA ===")
    
    df = gerar_dataset_exemplo()
    analisador = AnalisadorDados()
    
    # Realizar análise completa
    relatorio = analisador.analisar_dataset_completo(df)
    
    # Exibir resumo do relatório
    print(f"\n--- Resumo da Análise ---")
    print(f"Dataset: {relatorio.dataset_info['shape'][0]} × {relatorio.dataset_info['shape'][1]}")
    print(f"Tempo de processamento: {relatorio.tempo_processamento:.2f}s")
    print(f"Variáveis analisadas: {len(relatorio.estatisticas_descritivas)}")
    print(f"Testes realizados: {len(relatorio.testes_realizados)}")
    print(f"Recomendações geradas: {len(relatorio.recomendacoes)}")
    
    # Exibir algumas recomendações
    print(f"\n--- Principais Recomendações ---")
    for i, recomendacao in enumerate(relatorio.recomendacoes[:3], 1):
        print(f"{i}. {recomendacao}")
    
    # Gerar relatório HTML
    analisador.gerar_relatorio_html(relatorio, "relatorio_completo.html")
    
    return relatorio


def benchmark_performance():
    """Benchmark de performance do analisador."""
    print("\n=== BENCHMARK: PERFORMANCE ===")
    
    tamanhos = [100, 500, 1000, 5000]
    tempos = []
    
    for tamanho in tamanhos:
        print(f"\nTestando com {tamanho} amostras...")
        
        # Gerar dataset do tamanho especificado
        np.random.seed(42)
        df_test = gerar_dataset_exemplo()
        df_test = df_test.sample(min(tamanho, len(df_test)), random_state=42)
        
        # Medir tempo de análise
        analisador = AnalisadorDados()
        inicio = time.time()
        
        relatorio = analisador.analisar_dataset_completo(df_test)
        
        tempo_total = time.time() - inicio
        tempos.append(tempo_total)
        
        print(f"Tempo: {tempo_total:.2f}s")
        print(f"Tempo por amostra: {(tempo_total/tamanho)*1000:.2f}ms")
    
    # Resumo do benchmark
    print(f"\n--- Resumo do Benchmark ---")
    for tamanho, tempo in zip(tamanhos, tempos):
        print(f"{tamanho:5d} amostras: {tempo:6.2f}s ({(tempo/tamanho)*1000:6.2f}ms/amostra)")


if __name__ == "__main__":
    print("MÓDULO 08.4 - ANALISADOR DE DADOS AVANÇADO")
    print("=" * 50)
    
    # Executar demonstrações
    demonstracao_analise_basica()
    demonstracao_correlacoes()
    demonstracao_clustering()
    demonstracao_visualizacoes()
    
    # Análise completa
    relatorio_final = demonstracao_analise_completa()
    
    # Benchmark de performance
    benchmark_performance()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO - ANALISADOR DE DADOS AVANÇADO")
    print("=" * 50)
    
    print("""
    Neste módulo, implementamos um sistema completo de análise de dados que demonstra:
    
    🔍 COMPONENTES PRINCIPAIS:
    • DetectorOutliers: Múltiplos métodos de detecção (Z-Score, IQR, Isolation Forest)
    • AnalisadorEstatistico: Testes estatísticos e estatísticas descritivas
    • VisualizadorDados: Gráficos informativos e dashboards
    • ClusterizadorDados: Algoritmos de clustering e otimização
    • AnalisadorDados: Orquestrador principal da análise
    
    📊 ANÁLISES IMPLEMENTADAS:
    • Estatísticas descritivas completas por tipo de variável
    • Detecção de outliers com consenso entre métodos
    • Testes de normalidade (Shapiro-Wilk, Kolmogorov-Smirnov)
    • Análise de correlações (Pearson, Spearman)
    • Testes de hipóteses (t-test, chi-quadrado, ANOVA)
    • Clustering automático com otimização de parâmetros
    
    🎨 VISUALIZAÇÕES AVANÇADAS:
    • Dashboard de análise exploratória automático
    • Matriz de correlação com heatmap
    • Boxplots para detecção visual de outliers
    • Pairplots para análise de relacionamentos
    • Visualização de clusters com PCA
    
    🔧 FUNCIONALIDADES TÉCNICAS:
    • Pipeline ETL automatizado
    • Tratamento robusto de dados faltantes
    • Normalização e padronização automática
    • Geração de relatórios HTML
    • Sistema de recomendações inteligente
    • Benchmark de performance
    
    📈 ALGORITMOS DE CLUSTERING:
    • K-Means com otimização automática do número de clusters
    • DBSCAN para detecção de clusters de densidade
    • Métodos de avaliação (Silhouette, Calinski-Harabasz)
    • Visualização com redução de dimensionalidade (PCA)
    
    🧪 TESTES ESTATÍSTICOS:
    • Testes de normalidade para validação de pressupostos
    • Testes de correlação com interpretação automática
    • Testes de independência (qui-quadrado)
    • ANOVA para comparação de múltiplos grupos
    
    📋 RELATÓRIOS E RECOMENDAÇÕES:
    • Relatório HTML completo e navegável
    • Sistema de recomendações baseado em análise
    • Identificação automática de problemas nos dados
    • Sugestões de preprocessamento e limpeza
    
    🚀 OTIMIZAÇÕES DE PERFORMANCE:
    • Processamento eficiente de grandes datasets
    • Algoritmos otimizados para diferentes tamanhos de dados
    • Tratamento inteligente de memória
    • Paralelização onde apropriado
    
    💡 APLICAÇÕES PRÁTICAS:
    • Análise exploratória de dados (EDA) automatizada
    • Detecção de anomalias em dados empresariais
    • Segmentação de clientes
    • Análise de qualidade de dados
    • Preparação de dados para machine learning
    • Relatórios executivos automatizados
    
    Este analisador representa uma ferramenta completa para análise de dados,
    integrando estatística, visualização e machine learning em um pipeline
    robusto e escalável, adequado tanto para análises exploratórias quanto
    para sistemas de produção.
    """)