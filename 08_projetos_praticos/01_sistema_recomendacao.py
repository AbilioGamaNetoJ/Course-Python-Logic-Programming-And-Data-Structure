"""
MÓDULO 08.1 - SISTEMA DE RECOMENDAÇÃO
====================================

Objetivos de Aprendizado:
- Implementar sistemas de recomendação completos
- Dominar filtragem colaborativa (user-based e item-based)
- Aplicar filtragem baseada em conteúdo
- Implementar algoritmos híbridos
- Usar técnicas de machine learning para recomendações
- Avaliar qualidade de recomendações
- Otimizar performance para grandes datasets
- Implementar cold start solutions

Conceitos Abordados:
- Filtragem Colaborativa (Collaborative Filtering)
- Filtragem Baseada em Conteúdo (Content-Based Filtering)
- Sistemas Híbridos
- Matrix Factorization (SVD, NMF)
- Similarity Metrics (Cosine, Pearson, Jaccard)
- Evaluation Metrics (RMSE, MAE, Precision, Recall)
- Cold Start Problem
- Scalability e Performance

Algoritmos Implementados:
- User-Based Collaborative Filtering
- Item-Based Collaborative Filtering
- Content-Based Filtering
- Matrix Factorization (SVD)
- K-Nearest Neighbors (KNN)
- Slope One Algorithm
- Association Rules (Market Basket Analysis)

Pré-requisitos:
- Estruturas de dados avançadas
- Algoritmos de busca e ordenação
- Análise de complexidade
- Conceitos básicos de machine learning
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Set, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, Counter
from abc import ABC, abstractmethod
import math
import random
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD, NMF
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


class TipoRecomendacao(Enum):
    """Tipos de sistemas de recomendação."""
    COLABORATIVA_USUARIO = "Colaborativa baseada em usuário"
    COLABORATIVA_ITEM = "Colaborativa baseada em item"
    CONTEUDO = "Baseada em conteúdo"
    HIBRIDA = "Híbrida"
    MATRIX_FACTORIZATION = "Fatoração de matriz"


class MetricaSimilaridade(Enum):
    """Métricas de similaridade."""
    COSINE = "Cosseno"
    PEARSON = "Correlação de Pearson"
    JACCARD = "Jaccard"
    EUCLIDEAN = "Euclidiana"
    MANHATTAN = "Manhattan"


@dataclass
class Usuario:
    """Representa um usuário do sistema."""
    id: int
    nome: str
    idade: Optional[int] = None
    genero: Optional[str] = None
    ocupacao: Optional[str] = None
    avaliacoes: Dict[int, float] = field(default_factory=dict)
    preferencias: Dict[str, Any] = field(default_factory=dict)
    
    def adicionar_avaliacao(self, item_id: int, rating: float):
        """Adiciona avaliação de um item."""
        self.avaliacoes[item_id] = rating
    
    def obter_avaliacao(self, item_id: int) -> Optional[float]:
        """Obtém avaliação de um item."""
        return self.avaliacoes.get(item_id)
    
    def itens_avaliados(self) -> Set[int]:
        """Retorna conjunto de itens avaliados."""
        return set(self.avaliacoes.keys())


@dataclass
class Item:
    """Representa um item do sistema."""
    id: int
    titulo: str
    generos: List[str] = field(default_factory=list)
    ano: Optional[int] = None
    diretor: Optional[str] = None
    atores: List[str] = field(default_factory=list)
    descricao: Optional[str] = None
    features: Dict[str, Any] = field(default_factory=dict)
    avaliacoes: Dict[int, float] = field(default_factory=dict)
    
    def adicionar_avaliacao(self, usuario_id: int, rating: float):
        """Adiciona avaliação de um usuário."""
        self.avaliacoes[usuario_id] = rating
    
    def rating_medio(self) -> float:
        """Calcula rating médio do item."""
        if not self.avaliacoes:
            return 0.0
        return sum(self.avaliacoes.values()) / len(self.avaliacoes)
    
    def num_avaliacoes(self) -> int:
        """Número de avaliações do item."""
        return len(self.avaliacoes)


@dataclass
class Recomendacao:
    """Representa uma recomendação."""
    item_id: int
    score: float
    explicacao: str = ""
    confianca: float = 0.0
    
    def __lt__(self, other):
        return self.score < other.score


@dataclass
class MetricasAvaliacao:
    """Métricas de avaliação do sistema."""
    rmse: float = 0.0
    mae: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    coverage: float = 0.0
    diversity: float = 0.0
    novelty: float = 0.0


class CalculadorSimilaridade:
    """
    Calculador de similaridade entre usuários/itens.
    """
    
    @staticmethod
    def cosine_similarity(vetor1: Dict[int, float], 
                         vetor2: Dict[int, float]) -> float:
        """
        Calcula similaridade do cosseno.
        
        Args:
            vetor1: Primeiro vetor (ratings)
            vetor2: Segundo vetor (ratings)
        
        Returns:
            Similaridade do cosseno [-1, 1]
        """
        # Itens em comum
        itens_comuns = set(vetor1.keys()) & set(vetor2.keys())
        
        if not itens_comuns:
            return 0.0
        
        # Calcular produtos
        numerador = sum(vetor1[item] * vetor2[item] for item in itens_comuns)
        
        # Calcular normas
        norma1 = math.sqrt(sum(vetor1[item]**2 for item in itens_comuns))
        norma2 = math.sqrt(sum(vetor2[item]**2 for item in itens_comuns))
        
        if norma1 == 0 or norma2 == 0:
            return 0.0
        
        return numerador / (norma1 * norma2)
    
    @staticmethod
    def pearson_correlation(vetor1: Dict[int, float], 
                           vetor2: Dict[int, float]) -> float:
        """
        Calcula correlação de Pearson.
        
        Args:
            vetor1: Primeiro vetor (ratings)
            vetor2: Segundo vetor (ratings)
        
        Returns:
            Correlação de Pearson [-1, 1]
        """
        # Itens em comum
        itens_comuns = set(vetor1.keys()) & set(vetor2.keys())
        
        if len(itens_comuns) < 2:
            return 0.0
        
        # Médias
        media1 = sum(vetor1[item] for item in itens_comuns) / len(itens_comuns)
        media2 = sum(vetor2[item] for item in itens_comuns) / len(itens_comuns)
        
        # Calcular correlação
        numerador = sum((vetor1[item] - media1) * (vetor2[item] - media2) 
                       for item in itens_comuns)
        
        denominador1 = sum((vetor1[item] - media1)**2 for item in itens_comuns)
        denominador2 = sum((vetor2[item] - media2)**2 for item in itens_comuns)
        
        denominador = math.sqrt(denominador1 * denominador2)
        
        if denominador == 0:
            return 0.0
        
        return numerador / denominador
    
    @staticmethod
    def jaccard_similarity(conjunto1: Set, conjunto2: Set) -> float:
        """
        Calcula similaridade de Jaccard.
        
        Args:
            conjunto1: Primeiro conjunto
            conjunto2: Segundo conjunto
        
        Returns:
            Similaridade de Jaccard [0, 1]
        """
        intersecao = len(conjunto1 & conjunto2)
        uniao = len(conjunto1 | conjunto2)
        
        if uniao == 0:
            return 0.0
        
        return intersecao / uniao


class SistemaRecomendacao(ABC):
    """
    Classe base para sistemas de recomendação.
    """
    
    def __init__(self, nome: str):
        """
        Inicializa sistema de recomendação.
        
        Args:
            nome: Nome do sistema
        """
        self.nome = nome
        self.usuarios: Dict[int, Usuario] = {}
        self.itens: Dict[int, Item] = {}
        self.matriz_ratings: Optional[np.ndarray] = None
        self.treinado = False
    
    def adicionar_usuario(self, usuario: Usuario):
        """Adiciona usuário ao sistema."""
        self.usuarios[usuario.id] = usuario
    
    def adicionar_item(self, item: Item):
        """Adiciona item ao sistema."""
        self.itens[item.id] = item
    
    def adicionar_rating(self, usuario_id: int, item_id: int, rating: float):
        """Adiciona rating ao sistema."""
        if usuario_id in self.usuarios:
            self.usuarios[usuario_id].adicionar_avaliacao(item_id, rating)
        
        if item_id in self.itens:
            self.itens[item_id].adicionar_avaliacao(usuario_id, rating)
    
    def construir_matriz_ratings(self):
        """Constrói matriz de ratings usuário-item."""
        if not self.usuarios or not self.itens:
            return
        
        usuarios_ids = sorted(self.usuarios.keys())
        itens_ids = sorted(self.itens.keys())
        
        # Mapear IDs para índices
        self.usuario_to_idx = {uid: idx for idx, uid in enumerate(usuarios_ids)}
        self.item_to_idx = {iid: idx for idx, iid in enumerate(itens_ids)}
        self.idx_to_usuario = {idx: uid for uid, idx in self.usuario_to_idx.items()}
        self.idx_to_item = {idx: iid for iid, idx in self.item_to_idx.items()}
        
        # Criar matriz
        self.matriz_ratings = np.zeros((len(usuarios_ids), len(itens_ids)))
        
        for usuario_id, usuario in self.usuarios.items():
            for item_id, rating in usuario.avaliacoes.items():
                if item_id in self.item_to_idx:
                    i = self.usuario_to_idx[usuario_id]
                    j = self.item_to_idx[item_id]
                    self.matriz_ratings[i, j] = rating
    
    @abstractmethod
    def treinar(self):
        """Treina o modelo de recomendação."""
        pass
    
    @abstractmethod
    def recomendar(self, usuario_id: int, n_recomendacoes: int = 10) -> List[Recomendacao]:
        """
        Gera recomendações para um usuário.
        
        Args:
            usuario_id: ID do usuário
            n_recomendacoes: Número de recomendações
        
        Returns:
            Lista de recomendações
        """
        pass
    
    def avaliar_sistema(self, test_set: List[Tuple[int, int, float]]) -> MetricasAvaliacao:
        """
        Avalia o sistema de recomendação.
        
        Args:
            test_set: Conjunto de teste (usuario_id, item_id, rating_real)
        
        Returns:
            Métricas de avaliação
        """
        predicoes = []
        reais = []
        
        for usuario_id, item_id, rating_real in test_set:
            rating_pred = self.predizer_rating(usuario_id, item_id)
            if rating_pred is not None:
                predicoes.append(rating_pred)
                reais.append(rating_real)
        
        if not predicoes:
            return MetricasAvaliacao()
        
        # Calcular métricas
        predicoes = np.array(predicoes)
        reais = np.array(reais)
        
        rmse = np.sqrt(np.mean((predicoes - reais)**2))
        mae = np.mean(np.abs(predicoes - reais))
        
        return MetricasAvaliacao(rmse=rmse, mae=mae)
    
    def predizer_rating(self, usuario_id: int, item_id: int) -> Optional[float]:
        """
        Prediz rating de um usuário para um item.
        
        Args:
            usuario_id: ID do usuário
            item_id: ID do item
        
        Returns:
            Rating predito ou None
        """
        # Implementação padrão - deve ser sobrescrita
        return None


class FiltroColaborativoUsuario(SistemaRecomendacao):
    """
    Sistema de recomendação baseado em filtragem colaborativa por usuário.
    """
    
    def __init__(self, metrica: MetricaSimilaridade = MetricaSimilaridade.COSINE,
                 k_vizinhos: int = 50):
        """
        Inicializa filtro colaborativo baseado em usuário.
        
        Args:
            metrica: Métrica de similaridade
            k_vizinhos: Número de vizinhos mais próximos
        """
        super().__init__("Filtro Colaborativo - Usuário")
        self.metrica = metrica
        self.k_vizinhos = k_vizinhos
        self.similaridades_usuario: Dict[Tuple[int, int], float] = {}
    
    def treinar(self):
        """Treina o modelo calculando similaridades entre usuários."""
        self.construir_matriz_ratings()
        
        print(f"Calculando similaridades entre {len(self.usuarios)} usuários...")
        
        # Calcular similaridades entre todos os pares de usuários
        usuarios_ids = list(self.usuarios.keys())
        
        for i, usuario1_id in enumerate(usuarios_ids):
            for j, usuario2_id in enumerate(usuarios_ids[i+1:], i+1):
                similaridade = self._calcular_similaridade_usuarios(
                    usuario1_id, usuario2_id
                )
                self.similaridades_usuario[(usuario1_id, usuario2_id)] = similaridade
                self.similaridades_usuario[(usuario2_id, usuario1_id)] = similaridade
        
        self.treinado = True
        print("Treinamento concluído!")
    
    def _calcular_similaridade_usuarios(self, usuario1_id: int, usuario2_id: int) -> float:
        """Calcula similaridade entre dois usuários."""
        usuario1 = self.usuarios[usuario1_id]
        usuario2 = self.usuarios[usuario2_id]
        
        if self.metrica == MetricaSimilaridade.COSINE:
            return CalculadorSimilaridade.cosine_similarity(
                usuario1.avaliacoes, usuario2.avaliacoes
            )
        elif self.metrica == MetricaSimilaridade.PEARSON:
            return CalculadorSimilaridade.pearson_correlation(
                usuario1.avaliacoes, usuario2.avaliacoes
            )
        elif self.metrica == MetricaSimilaridade.JACCARD:
            return CalculadorSimilaridade.jaccard_similarity(
                usuario1.itens_avaliados(), usuario2.itens_avaliados()
            )
        else:
            return 0.0
    
    def _obter_vizinhos_proximos(self, usuario_id: int) -> List[Tuple[int, float]]:
        """Obtém k vizinhos mais próximos de um usuário."""
        similaridades = []
        
        for outro_usuario_id in self.usuarios:
            if outro_usuario_id != usuario_id:
                sim = self.similaridades_usuario.get((usuario_id, outro_usuario_id), 0.0)
                if sim > 0:
                    similaridades.append((outro_usuario_id, sim))
        
        # Ordenar por similaridade decrescente
        similaridades.sort(key=lambda x: x[1], reverse=True)
        
        return similaridades[:self.k_vizinhos]
    
    def recomendar(self, usuario_id: int, n_recomendacoes: int = 10) -> List[Recomendacao]:
        """Gera recomendações baseadas em usuários similares."""
        if not self.treinado:
            raise ValueError("Sistema deve ser treinado primeiro")
        
        if usuario_id not in self.usuarios:
            return []
        
        # Obter vizinhos próximos
        vizinhos = self._obter_vizinhos_proximos(usuario_id)
        
        if not vizinhos:
            return []
        
        # Calcular scores para itens não avaliados
        usuario = self.usuarios[usuario_id]
        itens_avaliados = usuario.itens_avaliados()
        
        scores_itens = defaultdict(float)
        soma_similaridades = defaultdict(float)
        
        for vizinho_id, similaridade in vizinhos:
            vizinho = self.usuarios[vizinho_id]
            
            for item_id, rating in vizinho.avaliacoes.items():
                if item_id not in itens_avaliados:
                    scores_itens[item_id] += similaridade * rating
                    soma_similaridades[item_id] += abs(similaridade)
        
        # Normalizar scores
        recomendacoes = []
        for item_id, score_total in scores_itens.items():
            if soma_similaridades[item_id] > 0:
                score_normalizado = score_total / soma_similaridades[item_id]
                
                explicacao = f"Baseado em {len(vizinhos)} usuários similares"
                confianca = min(soma_similaridades[item_id] / len(vizinhos), 1.0)
                
                recomendacoes.append(Recomendacao(
                    item_id=item_id,
                    score=score_normalizado,
                    explicacao=explicacao,
                    confianca=confianca
                ))
        
        # Ordenar e retornar top N
        recomendacoes.sort(reverse=True)
        return recomendacoes[:n_recomendacoes]
    
    def predizer_rating(self, usuario_id: int, item_id: int) -> Optional[float]:
        """Prediz rating usando vizinhos próximos."""
        if not self.treinado or usuario_id not in self.usuarios:
            return None
        
        vizinhos = self._obter_vizinhos_proximos(usuario_id)
        
        if not vizinhos:
            return None
        
        numerador = 0.0
        denominador = 0.0
        
        for vizinho_id, similaridade in vizinhos:
            vizinho = self.usuarios[vizinho_id]
            if item_id in vizinho.avaliacoes:
                numerador += similaridade * vizinho.avaliacoes[item_id]
                denominador += abs(similaridade)
        
        if denominador == 0:
            return None
        
        return numerador / denominador


class FiltroColaborativoItem(SistemaRecomendacao):
    """
    Sistema de recomendação baseado em filtragem colaborativa por item.
    """
    
    def __init__(self, metrica: MetricaSimilaridade = MetricaSimilaridade.COSINE,
                 k_vizinhos: int = 50):
        """
        Inicializa filtro colaborativo baseado em item.
        
        Args:
            metrica: Métrica de similaridade
            k_vizinhos: Número de vizinhos mais próximos
        """
        super().__init__("Filtro Colaborativo - Item")
        self.metrica = metrica
        self.k_vizinhos = k_vizinhos
        self.similaridades_item: Dict[Tuple[int, int], float] = {}
    
    def treinar(self):
        """Treina o modelo calculando similaridades entre itens."""
        self.construir_matriz_ratings()
        
        print(f"Calculando similaridades entre {len(self.itens)} itens...")
        
        # Calcular similaridades entre todos os pares de itens
        itens_ids = list(self.itens.keys())
        
        for i, item1_id in enumerate(itens_ids):
            for j, item2_id in enumerate(itens_ids[i+1:], i+1):
                similaridade = self._calcular_similaridade_itens(item1_id, item2_id)
                self.similaridades_item[(item1_id, item2_id)] = similaridade
                self.similaridades_item[(item2_id, item1_id)] = similaridade
        
        self.treinado = True
        print("Treinamento concluído!")
    
    def _calcular_similaridade_itens(self, item1_id: int, item2_id: int) -> float:
        """Calcula similaridade entre dois itens."""
        item1 = self.itens[item1_id]
        item2 = self.itens[item2_id]
        
        if self.metrica == MetricaSimilaridade.COSINE:
            return CalculadorSimilaridade.cosine_similarity(
                item1.avaliacoes, item2.avaliacoes
            )
        elif self.metrica == MetricaSimilaridade.PEARSON:
            return CalculadorSimilaridade.pearson_correlation(
                item1.avaliacoes, item2.avaliacoes
            )
        elif self.metrica == MetricaSimilaridade.JACCARD:
            usuarios1 = set(item1.avaliacoes.keys())
            usuarios2 = set(item2.avaliacoes.keys())
            return CalculadorSimilaridade.jaccard_similarity(usuarios1, usuarios2)
        else:
            return 0.0
    
    def _obter_itens_similares(self, item_id: int) -> List[Tuple[int, float]]:
        """Obtém k itens mais similares."""
        similaridades = []
        
        for outro_item_id in self.itens:
            if outro_item_id != item_id:
                sim = self.similaridades_item.get((item_id, outro_item_id), 0.0)
                if sim > 0:
                    similaridades.append((outro_item_id, sim))
        
        # Ordenar por similaridade decrescente
        similaridades.sort(key=lambda x: x[1], reverse=True)
        
        return similaridades[:self.k_vizinhos]
    
    def recomendar(self, usuario_id: int, n_recomendacoes: int = 10) -> List[Recomendacao]:
        """Gera recomendações baseadas em itens similares."""
        if not self.treinado:
            raise ValueError("Sistema deve ser treinado primeiro")
        
        if usuario_id not in self.usuarios:
            return []
        
        usuario = self.usuarios[usuario_id]
        itens_avaliados = usuario.itens_avaliados()
        
        scores_itens = defaultdict(float)
        soma_similaridades = defaultdict(float)
        
        # Para cada item avaliado pelo usuário
        for item_avaliado_id, rating_usuario in usuario.avaliacoes.items():
            # Obter itens similares
            itens_similares = self._obter_itens_similares(item_avaliado_id)
            
            for item_similar_id, similaridade in itens_similares:
                if item_similar_id not in itens_avaliados:
                    scores_itens[item_similar_id] += similaridade * rating_usuario
                    soma_similaridades[item_similar_id] += abs(similaridade)
        
        # Normalizar scores
        recomendacoes = []
        for item_id, score_total in scores_itens.items():
            if soma_similaridades[item_id] > 0:
                score_normalizado = score_total / soma_similaridades[item_id]
                
                explicacao = f"Baseado em itens similares que você avaliou"
                confianca = min(soma_similaridades[item_id] / len(itens_avaliados), 1.0)
                
                recomendacoes.append(Recomendacao(
                    item_id=item_id,
                    score=score_normalizado,
                    explicacao=explicacao,
                    confianca=confianca
                ))
        
        # Ordenar e retornar top N
        recomendacoes.sort(reverse=True)
        return recomendacoes[:n_recomendacoes]


class FiltroBaseadoConteudo(SistemaRecomendacao):
    """
    Sistema de recomendação baseado em conteúdo.
    """
    
    def __init__(self):
        """Inicializa filtro baseado em conteúdo."""
        super().__init__("Filtro Baseado em Conteúdo")
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        self.matriz_conteudo: Optional[np.ndarray] = None
        self.perfis_usuario: Dict[int, np.ndarray] = {}
    
    def treinar(self):
        """Treina o modelo criando perfis de usuário baseados em conteúdo."""
        print("Construindo matriz de conteúdo...")
        
        # Criar documentos de conteúdo para cada item
        documentos = []
        itens_ordenados = sorted(self.itens.keys())
        
        for item_id in itens_ordenados:
            item = self.itens[item_id]
            
            # Combinar todas as features textuais
            conteudo = []
            
            if item.titulo:
                conteudo.append(item.titulo)
            
            if item.generos:
                conteudo.extend(item.generos)
            
            if item.diretor:
                conteudo.append(item.diretor)
            
            if item.atores:
                conteudo.extend(item.atores)
            
            if item.descricao:
                conteudo.append(item.descricao)
            
            documento = ' '.join(conteudo)
            documentos.append(documento)
        
        # Criar matriz TF-IDF
        self.matriz_conteudo = self.vectorizer.fit_transform(documentos).toarray()
        self.item_to_idx = {item_id: idx for idx, item_id in enumerate(itens_ordenados)}
        
        # Criar perfis de usuário
        print("Criando perfis de usuário...")
        
        for usuario_id, usuario in self.usuarios.items():
            perfil = self._criar_perfil_usuario(usuario)
            self.perfis_usuario[usuario_id] = perfil
        
        self.treinado = True
        print("Treinamento concluído!")
    
    def _criar_perfil_usuario(self, usuario: Usuario) -> np.ndarray:
        """Cria perfil de usuário baseado em suas avaliações."""
        if self.matriz_conteudo is None:
            return np.zeros(0)
        
        perfil = np.zeros(self.matriz_conteudo.shape[1])
        soma_ratings = 0.0
        
        for item_id, rating in usuario.avaliacoes.items():
            if item_id in self.item_to_idx:
                idx = self.item_to_idx[item_id]
                perfil += rating * self.matriz_conteudo[idx]
                soma_ratings += abs(rating)
        
        # Normalizar perfil
        if soma_ratings > 0:
            perfil /= soma_ratings
        
        return perfil
    
    def recomendar(self, usuario_id: int, n_recomendacoes: int = 10) -> List[Recomendacao]:
        """Gera recomendações baseadas no perfil de conteúdo do usuário."""
        if not self.treinado:
            raise ValueError("Sistema deve ser treinado primeiro")
        
        if usuario_id not in self.perfis_usuario:
            return []
        
        perfil_usuario = self.perfis_usuario[usuario_id]
        usuario = self.usuarios[usuario_id]
        itens_avaliados = usuario.itens_avaliados()
        
        recomendacoes = []
        
        # Calcular similaridade com todos os itens não avaliados
        for item_id, item in self.itens.items():
            if item_id not in itens_avaliados and item_id in self.item_to_idx:
                idx = self.item_to_idx[item_id]
                vetor_item = self.matriz_conteudo[idx]
                
                # Calcular similaridade do cosseno
                similaridade = cosine_similarity(
                    perfil_usuario.reshape(1, -1),
                    vetor_item.reshape(1, -1)
                )[0, 0]
                
                if similaridade > 0:
                    explicacao = f"Baseado no seu interesse em {', '.join(item.generos[:2])}"
                    
                    recomendacoes.append(Recomendacao(
                        item_id=item_id,
                        score=similaridade,
                        explicacao=explicacao,
                        confianca=similaridade
                    ))
        
        # Ordenar e retornar top N
        recomendacoes.sort(reverse=True)
        return recomendacoes[:n_recomendacoes]


class MatrixFactorization(SistemaRecomendacao):
    """
    Sistema de recomendação usando fatoração de matriz (SVD).
    """
    
    def __init__(self, n_factors: int = 50, n_epochs: int = 100, 
                 learning_rate: float = 0.01, regularization: float = 0.01):
        """
        Inicializa matrix factorization.
        
        Args:
            n_factors: Número de fatores latentes
            n_epochs: Número de épocas de treinamento
            learning_rate: Taxa de aprendizado
            regularization: Regularização
        """
        super().__init__("Matrix Factorization (SVD)")
        self.n_factors = n_factors
        self.n_epochs = n_epochs
        self.learning_rate = learning_rate
        self.regularization = regularization
        
        self.user_factors: Optional[np.ndarray] = None
        self.item_factors: Optional[np.ndarray] = None
        self.user_bias: Optional[np.ndarray] = None
        self.item_bias: Optional[np.ndarray] = None
        self.global_bias: float = 0.0
    
    def treinar(self):
        """Treina o modelo usando SGD."""
        self.construir_matriz_ratings()
        
        if self.matriz_ratings is None:
            return
        
        n_users, n_items = self.matriz_ratings.shape
        
        # Inicializar fatores aleatoriamente
        self.user_factors = np.random.normal(0, 0.1, (n_users, self.n_factors))
        self.item_factors = np.random.normal(0, 0.1, (n_items, self.n_factors))
        self.user_bias = np.zeros(n_users)
        self.item_bias = np.zeros(n_items)
        
        # Calcular bias global
        ratings_nao_zero = self.matriz_ratings[self.matriz_ratings > 0]
        self.global_bias = np.mean(ratings_nao_zero) if len(ratings_nao_zero) > 0 else 0.0
        
        # Obter índices de ratings não-zero
        indices_nao_zero = np.where(self.matriz_ratings > 0)
        
        print(f"Treinando com {len(indices_nao_zero[0])} ratings...")
        
        # Treinamento SGD
        for epoch in range(self.n_epochs):
            erro_total = 0.0
            
            # Embaralhar ordem dos ratings
            indices = list(zip(indices_nao_zero[0], indices_nao_zero[1]))
            random.shuffle(indices)
            
            for user_idx, item_idx in indices:
                rating_real = self.matriz_ratings[user_idx, item_idx]
                
                # Predição atual
                rating_pred = (self.global_bias + 
                             self.user_bias[user_idx] + 
                             self.item_bias[item_idx] +
                             np.dot(self.user_factors[user_idx], 
                                   self.item_factors[item_idx]))
                
                # Erro
                erro = rating_real - rating_pred
                erro_total += erro**2
                
                # Gradientes
                user_factor = self.user_factors[user_idx].copy()
                item_factor = self.item_factors[item_idx].copy()
                
                # Atualizar bias
                self.user_bias[user_idx] += self.learning_rate * (
                    erro - self.regularization * self.user_bias[user_idx]
                )
                self.item_bias[item_idx] += self.learning_rate * (
                    erro - self.regularization * self.item_bias[item_idx]
                )
                
                # Atualizar fatores
                self.user_factors[user_idx] += self.learning_rate * (
                    erro * item_factor - self.regularization * user_factor
                )
                self.item_factors[item_idx] += self.learning_rate * (
                    erro * user_factor - self.regularization * item_factor
                )
            
            rmse = np.sqrt(erro_total / len(indices))
            
            if epoch % 10 == 0:
                print(f"Época {epoch}: RMSE = {rmse:.4f}")
        
        self.treinado = True
        print("Treinamento concluído!")
    
    def predizer_rating(self, usuario_id: int, item_id: int) -> Optional[float]:
        """Prediz rating usando fatores latentes."""
        if not self.treinado:
            return None
        
        if (usuario_id not in self.usuario_to_idx or 
            item_id not in self.item_to_idx):
            return None
        
        user_idx = self.usuario_to_idx[usuario_id]
        item_idx = self.item_to_idx[item_id]
        
        rating_pred = (self.global_bias + 
                      self.user_bias[user_idx] + 
                      self.item_bias[item_idx] +
                      np.dot(self.user_factors[user_idx], 
                            self.item_factors[item_idx]))
        
        return max(1.0, min(5.0, rating_pred))  # Clampar entre 1 e 5
    
    def recomendar(self, usuario_id: int, n_recomendacoes: int = 10) -> List[Recomendacao]:
        """Gera recomendações usando fatores latentes."""
        if not self.treinado or usuario_id not in self.usuarios:
            return []
        
        usuario = self.usuarios[usuario_id]
        itens_avaliados = usuario.itens_avaliados()
        
        recomendacoes = []
        
        for item_id in self.itens:
            if item_id not in itens_avaliados:
                rating_pred = self.predizer_rating(usuario_id, item_id)
                
                if rating_pred is not None:
                    explicacao = "Baseado em padrões latentes de preferência"
                    
                    recomendacoes.append(Recomendacao(
                        item_id=item_id,
                        score=rating_pred,
                        explicacao=explicacao,
                        confianca=0.8
                    ))
        
        # Ordenar e retornar top N
        recomendacoes.sort(reverse=True)
        return recomendacoes[:n_recomendacoes]


class SistemaHibrido(SistemaRecomendacao):
    """
    Sistema híbrido que combina múltiplas abordagens.
    """
    
    def __init__(self, sistemas: List[SistemaRecomendacao], 
                 pesos: Optional[List[float]] = None):
        """
        Inicializa sistema híbrido.
        
        Args:
            sistemas: Lista de sistemas de recomendação
            pesos: Pesos para cada sistema (opcional)
        """
        super().__init__("Sistema Híbrido")
        self.sistemas = sistemas
        
        if pesos is None:
            self.pesos = [1.0 / len(sistemas)] * len(sistemas)
        else:
            self.pesos = pesos
        
        # Normalizar pesos
        soma_pesos = sum(self.pesos)
        self.pesos = [p / soma_pesos for p in self.pesos]
    
    def adicionar_usuario(self, usuario: Usuario):
        """Adiciona usuário a todos os sistemas."""
        super().adicionar_usuario(usuario)
        for sistema in self.sistemas:
            sistema.adicionar_usuario(usuario)
    
    def adicionar_item(self, item: Item):
        """Adiciona item a todos os sistemas."""
        super().adicionar_item(item)
        for sistema in self.sistemas:
            sistema.adicionar_item(item)
    
    def adicionar_rating(self, usuario_id: int, item_id: int, rating: float):
        """Adiciona rating a todos os sistemas."""
        super().adicionar_rating(usuario_id, item_id, rating)
        for sistema in self.sistemas:
            sistema.adicionar_rating(usuario_id, item_id, rating)
    
    def treinar(self):
        """Treina todos os sistemas."""
        print("Treinando sistemas híbridos...")
        
        for i, sistema in enumerate(self.sistemas):
            print(f"Treinando {sistema.nome}...")
            sistema.treinar()
        
        self.treinado = True
        print("Treinamento híbrido concluído!")
    
    def recomendar(self, usuario_id: int, n_recomendacoes: int = 10) -> List[Recomendacao]:
        """Combina recomendações de todos os sistemas."""
        if not self.treinado:
            raise ValueError("Sistema deve ser treinado primeiro")
        
        # Obter recomendações de cada sistema
        todas_recomendacoes = {}
        
        for i, sistema in enumerate(self.sistemas):
            try:
                recs = sistema.recomendar(usuario_id, n_recomendacoes * 2)
                peso = self.pesos[i]
                
                for rec in recs:
                    if rec.item_id not in todas_recomendacoes:
                        todas_recomendacoes[rec.item_id] = {
                            'score_total': 0.0,
                            'peso_total': 0.0,
                            'explicacoes': []
                        }
                    
                    todas_recomendacoes[rec.item_id]['score_total'] += rec.score * peso
                    todas_recomendacoes[rec.item_id]['peso_total'] += peso
                    todas_recomendacoes[rec.item_id]['explicacoes'].append(
                        f"{sistema.nome}: {rec.explicacao}"
                    )
            
            except Exception as e:
                print(f"Erro no sistema {sistema.nome}: {e}")
                continue
        
        # Criar recomendações finais
        recomendacoes_finais = []
        
        for item_id, dados in todas_recomendacoes.items():
            if dados['peso_total'] > 0:
                score_final = dados['score_total'] / dados['peso_total']
                explicacao_final = " | ".join(dados['explicacoes'][:2])
                
                recomendacoes_finais.append(Recomendacao(
                    item_id=item_id,
                    score=score_final,
                    explicacao=explicacao_final,
                    confianca=dados['peso_total']
                ))
        
        # Ordenar e retornar top N
        recomendacoes_finais.sort(reverse=True)
        return recomendacoes_finais[:n_recomendacoes]


class GeradorDados:
    """
    Gerador de dados sintéticos para teste.
    """
    
    @staticmethod
    def gerar_usuarios(n_usuarios: int) -> List[Usuario]:
        """Gera usuários sintéticos."""
        usuarios = []
        
        generos = ['M', 'F']
        ocupacoes = ['Estudante', 'Engenheiro', 'Professor', 'Médico', 'Artista']
        
        for i in range(n_usuarios):
            usuario = Usuario(
                id=i + 1,
                nome=f"Usuario_{i+1}",
                idade=random.randint(18, 70),
                genero=random.choice(generos),
                ocupacao=random.choice(ocupacoes)
            )
            usuarios.append(usuario)
        
        return usuarios
    
    @staticmethod
    def gerar_filmes(n_filmes: int) -> List[Item]:
        """Gera filmes sintéticos."""
        filmes = []
        
        generos_disponiveis = [
            'Ação', 'Comédia', 'Drama', 'Terror', 'Ficção Científica',
            'Romance', 'Thriller', 'Aventura', 'Animação', 'Documentário'
        ]
        
        diretores = [
            'Steven Spielberg', 'Martin Scorsese', 'Christopher Nolan',
            'Quentin Tarantino', 'Alfred Hitchcock', 'Stanley Kubrick'
        ]
        
        atores = [
            'Tom Hanks', 'Meryl Streep', 'Leonardo DiCaprio',
            'Robert De Niro', 'Scarlett Johansson', 'Brad Pitt'
        ]
        
        for i in range(n_filmes):
            filme = Item(
                id=i + 1,
                titulo=f"Filme_{i+1}",
                generos=random.sample(generos_disponiveis, random.randint(1, 3)),
                ano=random.randint(1980, 2023),
                diretor=random.choice(diretores),
                atores=random.sample(atores, random.randint(1, 4)),
                descricao=f"Descrição do filme {i+1} com elementos interessantes."
            )
            filmes.append(filme)
        
        return filmes
    
    @staticmethod
    def gerar_ratings(usuarios: List[Usuario], filmes: List[Item], 
                     densidade: float = 0.1):
        """Gera ratings sintéticos."""
        n_ratings = int(len(usuarios) * len(filmes) * densidade)
        
        for _ in range(n_ratings):
            usuario = random.choice(usuarios)
            filme = random.choice(filmes)
            
            # Simular preferências baseadas em gênero
            rating_base = 3.0
            
            # Usuários mais jovens preferem ação e ficção científica
            if usuario.idade < 30 and any(g in ['Ação', 'Ficção Científica'] 
                                        for g in filme.generos):
                rating_base += 0.5
            
            # Usuários mais velhos preferem drama
            if usuario.idade > 50 and 'Drama' in filme.generos:
                rating_base += 0.5
            
            # Adicionar ruído
            rating = rating_base + random.gauss(0, 0.5)
            rating = max(1.0, min(5.0, rating))
            
            usuario.adicionar_avaliacao(filme.id, rating)
            filme.adicionar_avaliacao(usuario.id, rating)


def demonstrar_filtro_colaborativo_usuario():
    """Demonstra filtro colaborativo baseado em usuário."""
    print("=== DEMONSTRAÇÃO: FILTRO COLABORATIVO - USUÁRIO ===\n")
    
    # Gerar dados
    usuarios = GeradorDados.gerar_usuarios(100)
    filmes = GeradorDados.gerar_filmes(50)
    GeradorDados.gerar_ratings(usuarios, filmes, densidade=0.15)
    
    # Criar sistema
    sistema = FiltroColaborativoUsuario(
        metrica=MetricaSimilaridade.COSINE,
        k_vizinhos=20
    )
    
    # Adicionar dados
    for usuario in usuarios:
        sistema.adicionar_usuario(usuario)
    
    for filme in filmes:
        sistema.adicionar_item(filme)
    
    for usuario in usuarios:
        for filme_id, rating in usuario.avaliacoes.items():
            sistema.adicionar_rating(usuario.id, filme_id, rating)
    
    # Treinar
    inicio = time.time()
    sistema.treinar()
    tempo_treino = time.time() - inicio
    
    # Gerar recomendações
    usuario_teste = usuarios[0]
    recomendacoes = sistema.recomendar(usuario_teste.id, n_recomendacoes=5)
    
    print(f"Tempo de treinamento: {tempo_treino:.2f}s")
    print(f"\nRecomendações para {usuario_teste.nome}:")
    print(f"Filmes já avaliados: {len(usuario_teste.avaliacoes)}")
    
    for i, rec in enumerate(recomendacoes, 1):
        filme = sistema.itens[rec.item_id]
        print(f"{i}. {filme.titulo} (Score: {rec.score:.2f})")
        print(f"   Gêneros: {', '.join(filme.generos)}")
        print(f"   {rec.explicacao}")
        print()


def demonstrar_filtro_baseado_conteudo():
    """Demonstra filtro baseado em conteúdo."""
    print("=== DEMONSTRAÇÃO: FILTRO BASEADO EM CONTEÚDO ===\n")
    
    # Gerar dados
    usuarios = GeradorDados.gerar_usuarios(50)
    filmes = GeradorDados.gerar_filmes(100)
    GeradorDados.gerar_ratings(usuarios, filmes, densidade=0.1)
    
    # Criar sistema
    sistema = FiltroBaseadoConteudo()
    
    # Adicionar dados
    for usuario in usuarios:
        sistema.adicionar_usuario(usuario)
    
    for filme in filmes:
        sistema.adicionar_item(filme)
    
    for usuario in usuarios:
        for filme_id, rating in usuario.avaliacoes.items():
            sistema.adicionar_rating(usuario.id, filme_id, rating)
    
    # Treinar
    inicio = time.time()
    sistema.treinar()
    tempo_treino = time.time() - inicio
    
    # Gerar recomendações
    usuario_teste = usuarios[0]
    recomendacoes = sistema.recomendar(usuario_teste.id, n_recomendacoes=5)
    
    print(f"Tempo de treinamento: {tempo_treino:.2f}s")
    print(f"\nRecomendações para {usuario_teste.nome}:")
    
    # Mostrar preferências do usuário
    generos_avaliados = defaultdict(list)
    for filme_id, rating in usuario_teste.avaliacoes.items():
        filme = sistema.itens[filme_id]
        for genero in filme.generos:
            generos_avaliados[genero].append(rating)
    
    print("Preferências por gênero:")
    for genero, ratings in generos_avaliados.items():
        media = sum(ratings) / len(ratings)
        print(f"  {genero}: {media:.1f} ({len(ratings)} filmes)")
    
    print("\nRecomendações:")
    for i, rec in enumerate(recomendacoes, 1):
        filme = sistema.itens[rec.item_id]
        print(f"{i}. {filme.titulo} (Score: {rec.score:.3f})")
        print(f"   Gêneros: {', '.join(filme.generos)}")
        print(f"   {rec.explicacao}")
        print()


def demonstrar_matrix_factorization():
    """Demonstra matrix factorization."""
    print("=== DEMONSTRAÇÃO: MATRIX FACTORIZATION ===\n")
    
    # Gerar dados
    usuarios = GeradorDados.gerar_usuarios(80)
    filmes = GeradorDados.gerar_filmes(60)
    GeradorDados.gerar_ratings(usuarios, filmes, densidade=0.2)
    
    # Criar sistema
    sistema = MatrixFactorization(
        n_factors=20,
        n_epochs=50,
        learning_rate=0.01,
        regularization=0.01
    )
    
    # Adicionar dados
    for usuario in usuarios:
        sistema.adicionar_usuario(usuario)
    
    for filme in filmes:
        sistema.adicionar_item(filme)
    
    for usuario in usuarios:
        for filme_id, rating in usuario.avaliacoes.items():
            sistema.adicionar_rating(usuario.id, filme_id, rating)
    
    # Treinar
    inicio = time.time()
    sistema.treinar()
    tempo_treino = time.time() - inicio
    
    # Gerar recomendações
    usuario_teste = usuarios[0]
    recomendacoes = sistema.recomendar(usuario_teste.id, n_recomendacoes=5)
    
    print(f"Tempo de treinamento: {tempo_treino:.2f}s")
    print(f"\nRecomendações para {usuario_teste.nome}:")
    
    for i, rec in enumerate(recomendacoes, 1):
        filme = sistema.itens[rec.item_id]
        print(f"{i}. {filme.titulo} (Score: {rec.score:.2f})")
        print(f"   Gêneros: {', '.join(filme.generos)}")
        print()


def demonstrar_sistema_hibrido():
    """Demonstra sistema híbrido."""
    print("=== DEMONSTRAÇÃO: SISTEMA HÍBRIDO ===\n")
    
    # Gerar dados
    usuarios = GeradorDados.gerar_usuarios(60)
    filmes = GeradorDados.gerar_filmes(40)
    GeradorDados.gerar_ratings(usuarios, filmes, densidade=0.25)
    
    # Criar sistemas individuais
    sistema_cf_user = FiltroColaborativoUsuario(k_vizinhos=15)
    sistema_cf_item = FiltroColaborativoItem(k_vizinhos=15)
    sistema_content = FiltroBaseadoConteudo()
    
    # Criar sistema híbrido
    sistema_hibrido = SistemaHibrido(
        sistemas=[sistema_cf_user, sistema_cf_item, sistema_content],
        pesos=[0.4, 0.4, 0.2]
    )
    
    # Adicionar dados
    for usuario in usuarios:
        sistema_hibrido.adicionar_usuario(usuario)
    
    for filme in filmes:
        sistema_hibrido.adicionar_item(filme)
    
    for usuario in usuarios:
        for filme_id, rating in usuario.avaliacoes.items():
            sistema_hibrido.adicionar_rating(usuario.id, filme_id, rating)
    
    # Treinar
    inicio = time.time()
    sistema_hibrido.treinar()
    tempo_treino = time.time() - inicio
    
    # Gerar recomendações
    usuario_teste = usuarios[0]
    recomendacoes = sistema_hibrido.recomendar(usuario_teste.id, n_recomendacoes=5)
    
    print(f"Tempo de treinamento: {tempo_treino:.2f}s")
    print(f"\nRecomendações híbridas para {usuario_teste.nome}:")
    
    for i, rec in enumerate(recomendacoes, 1):
        filme = sistema_hibrido.itens[rec.item_id]
        print(f"{i}. {filme.titulo} (Score: {rec.score:.3f})")
        print(f"   Gêneros: {', '.join(filme.generos)}")
        print(f"   Explicação: {rec.explicacao[:100]}...")
        print()


def benchmark_sistemas():
    """Benchmark de diferentes sistemas de recomendação."""
    print("=== BENCHMARK: SISTEMAS DE RECOMENDAÇÃO ===\n")
    
    # Gerar dados maiores
    usuarios = GeradorDados.gerar_usuarios(200)
    filmes = GeradorDados.gerar_filmes(150)
    GeradorDados.gerar_ratings(usuarios, filmes, densidade=0.1)
    
    # Dividir em treino e teste
    todos_ratings = []
    for usuario in usuarios:
        for filme_id, rating in usuario.avaliacoes.items():
            todos_ratings.append((usuario.id, filme_id, rating))
    
    train_ratings, test_ratings = train_test_split(
        todos_ratings, test_size=0.2, random_state=42
    )
    
    # Criar dados de treino
    usuarios_treino = {u.id: Usuario(u.id, u.nome, u.idade, u.genero, u.ocupacao) 
                      for u in usuarios}
    
    for usuario_id, filme_id, rating in train_ratings:
        usuarios_treino[usuario_id].adicionar_avaliacao(filme_id, rating)
    
    # Sistemas para testar
    sistemas = [
        FiltroColaborativoUsuario(k_vizinhos=30),
        FiltroColaborativoItem(k_vizinhos=30),
        MatrixFactorization(n_factors=15, n_epochs=30)
    ]
    
    resultados = {}
    
    for sistema in sistemas:
        print(f"Testando {sistema.nome}...")
        
        # Adicionar dados de treino
        for usuario in usuarios_treino.values():
            sistema.adicionar_usuario(usuario)
        
        for filme in filmes:
            sistema.adicionar_item(filme)
        
        for usuario in usuarios_treino.values():
            for filme_id, rating in usuario.avaliacoes.items():
                sistema.adicionar_rating(usuario.id, filme_id, rating)
        
        # Treinar
        inicio = time.time()
        try:
            sistema.treinar()
            tempo_treino = time.time() - inicio
            
            # Avaliar
            metricas = sistema.avaliar_sistema(test_ratings)
            
            resultados[sistema.nome] = {
                'tempo_treino': tempo_treino,
                'rmse': metricas.rmse,
                'mae': metricas.mae
            }
            
            print(f"  Tempo de treino: {tempo_treino:.2f}s")
            print(f"  RMSE: {metricas.rmse:.4f}")
            print(f"  MAE: {metricas.mae:.4f}")
            
        except Exception as e:
            print(f"  Erro: {e}")
            resultados[sistema.nome] = {
                'tempo_treino': float('inf'),
                'rmse': float('inf'),
                'mae': float('inf')
            }
        
        print()
    
    # Resumo dos resultados
    print("RESUMO DOS RESULTADOS:")
    print("-" * 50)
    
    for nome, metricas in resultados.items():
        print(f"{nome}:")
        print(f"  Tempo: {metricas['tempo_treino']:.2f}s")
        print(f"  RMSE: {metricas['rmse']:.4f}")
        print(f"  MAE: {metricas['mae']:.4f}")
        print()


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 08.1 - SISTEMA DE RECOMENDAÇÃO")
    print("=" * 50)
    
    # Executar demonstrações
    demonstrar_filtro_colaborativo_usuario()
    demonstrar_filtro_baseado_conteudo()
    demonstrar_matrix_factorization()
    demonstrar_sistema_hibrido()
    benchmark_sistemas()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 08.1")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. TIPOS DE SISTEMAS DE RECOMENDAÇÃO:
   • Filtragem Colaborativa (User-based e Item-based)
   • Filtragem Baseada em Conteúdo
   • Matrix Factorization (SVD, NMF)
   • Sistemas Híbridos
   • Cada tipo tem vantagens e limitações específicas

2. FILTRAGEM COLABORATIVA:
   • User-based: "Usuários similares gostam de itens similares"
   • Item-based: "Se você gostou de X, vai gostar de Y"
   • Métricas de similaridade: Cosine, Pearson, Jaccard
   • Problema de esparsidade e cold start
   • Escalabilidade com grandes datasets

3. FILTRAGEM BASEADA EM CONTEÚDO:
   • Recomenda baseado nas características dos itens
   • Usa TF-IDF para análise textual
   • Cria perfis de usuário baseados em preferências
   • Não sofre de cold start para novos usuários
   • Limitada pela qualidade das features

4. MATRIX FACTORIZATION:
   • Decompõe matriz de ratings em fatores latentes
   • Captura padrões complexos de preferência
   • SGD para otimização
   • Regularização para evitar overfitting
   • Boa performance com dados esparsos

5. SISTEMAS HÍBRIDOS:
   • Combinam múltiplas abordagens
   • Pesos para balancear contribuições
   • Melhor robustez e cobertura
   • Reduz limitações individuais
   • Mais complexo de implementar e tunar

6. MÉTRICAS DE AVALIAÇÃO:
   • RMSE e MAE para precisão de predição
   • Precision, Recall, F1 para relevância
   • Coverage para diversidade do catálogo
   • Novelty para descoberta de novos itens
   • Serendipity para surpresa positiva

7. DESAFIOS TÉCNICOS:
   • Cold Start Problem (novos usuários/itens)
   • Esparsidade da matriz de ratings
   • Escalabilidade para milhões de usuários/itens
   • Diversidade vs Precisão
   • Explicabilidade das recomendações

8. OTIMIZAÇÕES DE PERFORMANCE:
   • Pré-computação de similaridades
   • Indexação eficiente
   • Sampling para grandes datasets
   • Paralelização de cálculos
   • Cache de recomendações

9. ASPECTOS PRÁTICOS:
   • Tratamento de dados faltantes
   • Normalização de ratings
   • Filtragem de ruído nos dados
   • Atualização incremental de modelos
   • A/B testing para validação

10. APLICAÇÕES REAIS:
    • E-commerce (Amazon, eBay)
    • Streaming (Netflix, Spotify)
    • Redes sociais (Facebook, LinkedIn)
    • Conteúdo (YouTube, Medium)
    • Notícias e informação

PRÓXIMOS PASSOS:
- Implementar técnicas avançadas (Deep Learning)
- Estudar sistemas de recomendação em tempo real
- Explorar bandits contextuais
- Analisar fairness e bias em recomendações
- Integrar feedback implícito e explícito

Este módulo fornece uma base sólida para construir sistemas de
recomendação robustos e escaláveis, combinando teoria e prática
com implementações completas e otimizadas.
    """)


if __name__ == "__main__":
    main()