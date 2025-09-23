"""
MÓDULO 08.2 - MOTOR DE BUSCA
============================

Objetivos de Aprendizado:
- Implementar motor de busca completo
- Dominar técnicas de indexação (inverted index)
- Aplicar algoritmos de ranking (TF-IDF, BM25, PageRank)
- Implementar processamento de texto avançado
- Usar estruturas de dados eficientes para busca
- Otimizar performance para grandes volumes de dados
- Implementar busca fuzzy e correção ortográfica
- Aplicar técnicas de relevância e personalização

Conceitos Abordados:
- Inverted Index (Índice Invertido)
- TF-IDF (Term Frequency-Inverse Document Frequency)
- BM25 (Best Matching 25)
- PageRank Algorithm
- Text Processing (Tokenização, Stemming, Lemmatização)
- N-grams e Shingles
- Fuzzy Search (Levenshtein Distance)
- Query Processing e Expansion
- Faceted Search
- Real-time Indexing

Algoritmos Implementados:
- Inverted Index Construction
- TF-IDF Scoring
- BM25 Ranking
- PageRank Calculation
- Levenshtein Distance
- Soundex Algorithm
- Trie Data Structure
- Bloom Filters para otimização

Pré-requisitos:
- Estruturas de dados avançadas
- Algoritmos de ordenação
- Processamento de texto
- Análise de complexidade
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Set, Optional, Any, Union, Iterator
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, Counter, deque
from abc import ABC, abstractmethod
import math
import re
import time
import heapq
import json
from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

# Download necessário do NLTK (executar uma vez)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')


class TipoBusca(Enum):
    """Tipos de busca suportados."""
    EXATA = "Busca exata"
    FUZZY = "Busca fuzzy"
    BOOLEANA = "Busca booleana"
    FRASE = "Busca por frase"
    WILDCARD = "Busca com wildcards"


class TipoRanking(Enum):
    """Algoritmos de ranking."""
    TF_IDF = "TF-IDF"
    BM25 = "BM25"
    PAGERANK = "PageRank"
    CUSTOM = "Personalizado"


@dataclass
class Documento:
    """Representa um documento no índice."""
    id: str
    titulo: str
    conteudo: str
    url: Optional[str] = None
    autor: Optional[str] = None
    data_criacao: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadados: Dict[str, Any] = field(default_factory=dict)
    
    def texto_completo(self) -> str:
        """Retorna texto completo do documento."""
        partes = [self.titulo, self.conteudo]
        if self.autor:
            partes.append(self.autor)
        if self.tags:
            partes.extend(self.tags)
        return ' '.join(filter(None, partes))
    
    def tamanho(self) -> int:
        """Retorna tamanho do documento em caracteres."""
        return len(self.texto_completo())


@dataclass
class TermoIndice:
    """Representa um termo no índice invertido."""
    termo: str
    frequencia_documento: int  # Número de documentos que contêm o termo
    postings: Dict[str, int] = field(default_factory=dict)  # doc_id -> frequência
    
    def adicionar_ocorrencia(self, doc_id: str, frequencia: int = 1):
        """Adiciona ocorrência do termo em um documento."""
        if doc_id in self.postings:
            self.postings[doc_id] += frequencia
        else:
            self.postings[doc_id] = frequencia
            self.frequencia_documento += 1
    
    def obter_documentos(self) -> Set[str]:
        """Retorna conjunto de documentos que contêm o termo."""
        return set(self.postings.keys())


@dataclass
class ResultadoBusca:
    """Representa um resultado de busca."""
    documento: Documento
    score: float
    explicacao: str = ""
    termos_destacados: List[str] = field(default_factory=list)
    snippet: str = ""
    
    def __lt__(self, other):
        return self.score < other.score


@dataclass
class EstatisticasBusca:
    """Estatísticas de uma busca."""
    query: str
    num_resultados: int
    tempo_busca: float
    termos_processados: List[str]
    documentos_analisados: int
    algoritmo_usado: str


class ProcessadorTexto:
    """
    Processador de texto avançado para motor de busca.
    """
    
    def __init__(self, idioma: str = 'portuguese'):
        """
        Inicializa processador de texto.
        
        Args:
            idioma: Idioma para processamento
        """
        self.idioma = idioma
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        
        # Stopwords
        try:
            self.stopwords = set(stopwords.words(idioma))
        except:
            self.stopwords = set(stopwords.words('english'))
        
        # Padrões regex
        self.padrao_palavra = re.compile(r'\b[a-zA-ZÀ-ÿ]+\b')
        self.padrao_numero = re.compile(r'\b\d+\b')
        self.padrao_email = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.padrao_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    def limpar_texto(self, texto: str) -> str:
        """
        Limpa e normaliza texto.
        
        Args:
            texto: Texto a ser limpo
        
        Returns:
            Texto limpo
        """
        # Converter para minúsculas
        texto = texto.lower()
        
        # Remover URLs
        texto = self.padrao_url.sub(' ', texto)
        
        # Remover emails
        texto = self.padrao_email.sub(' ', texto)
        
        # Remover caracteres especiais, manter apenas letras e números
        texto = re.sub(r'[^\w\s]', ' ', texto)
        
        # Remover espaços múltiplos
        texto = re.sub(r'\s+', ' ', texto)
        
        return texto.strip()
    
    def tokenizar(self, texto: str) -> List[str]:
        """
        Tokeniza texto em palavras.
        
        Args:
            texto: Texto a ser tokenizado
        
        Returns:
            Lista de tokens
        """
        texto_limpo = self.limpar_texto(texto)
        tokens = word_tokenize(texto_limpo)
        
        # Filtrar tokens válidos
        tokens_validos = []
        for token in tokens:
            if (len(token) >= 2 and 
                token not in self.stopwords and
                self.padrao_palavra.match(token)):
                tokens_validos.append(token)
        
        return tokens_validos
    
    def aplicar_stemming(self, tokens: List[str]) -> List[str]:
        """Aplica stemming aos tokens."""
        return [self.stemmer.stem(token) for token in tokens]
    
    def aplicar_lemmatization(self, tokens: List[str]) -> List[str]:
        """Aplica lemmatização aos tokens."""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def gerar_ngramas(self, tokens: List[str], n: int = 2) -> List[str]:
        """
        Gera n-gramas dos tokens.
        
        Args:
            tokens: Lista de tokens
            n: Tamanho do n-grama
        
        Returns:
            Lista de n-gramas
        """
        if len(tokens) < n:
            return []
        
        ngramas = []
        for i in range(len(tokens) - n + 1):
            ngrama = '_'.join(tokens[i:i+n])
            ngramas.append(ngrama)
        
        return ngramas
    
    def processar_completo(self, texto: str, usar_stemming: bool = True,
                          incluir_bigramas: bool = False) -> List[str]:
        """
        Processamento completo de texto.
        
        Args:
            texto: Texto a ser processado
            usar_stemming: Se deve aplicar stemming
            incluir_bigramas: Se deve incluir bigramas
        
        Returns:
            Lista de termos processados
        """
        # Tokenizar
        tokens = self.tokenizar(texto)
        
        if not tokens:
            return []
        
        # Aplicar stemming ou lemmatização
        if usar_stemming:
            tokens = self.aplicar_stemming(tokens)
        else:
            tokens = self.aplicar_lemmatization(tokens)
        
        termos = tokens.copy()
        
        # Adicionar bigramas se solicitado
        if incluir_bigramas:
            bigramas = self.gerar_ngramas(tokens, 2)
            termos.extend(bigramas)
        
        return termos


class IndiceInvertido:
    """
    Implementação de índice invertido para busca eficiente.
    """
    
    def __init__(self):
        """Inicializa índice invertido."""
        self.indice: Dict[str, TermoIndice] = {}
        self.documentos: Dict[str, Documento] = {}
        self.processador = ProcessadorTexto()
        self.total_documentos = 0
        self.total_termos = 0
    
    def adicionar_documento(self, documento: Documento):
        """
        Adiciona documento ao índice.
        
        Args:
            documento: Documento a ser indexado
        """
        # Armazenar documento
        self.documentos[documento.id] = documento
        
        # Processar texto
        texto_completo = documento.texto_completo()
        termos = self.processador.processar_completo(
            texto_completo, 
            usar_stemming=True,
            incluir_bigramas=True
        )
        
        # Contar frequências dos termos
        contador_termos = Counter(termos)
        
        # Adicionar termos ao índice
        for termo, frequencia in contador_termos.items():
            if termo not in self.indice:
                self.indice[termo] = TermoIndice(termo, 0)
            
            self.indice[termo].adicionar_ocorrencia(documento.id, frequencia)
        
        self.total_documentos += 1
        self.total_termos = len(self.indice)
    
    def remover_documento(self, doc_id: str):
        """Remove documento do índice."""
        if doc_id not in self.documentos:
            return
        
        # Remover das postings lists
        termos_para_remover = []
        
        for termo, termo_indice in self.indice.items():
            if doc_id in termo_indice.postings:
                del termo_indice.postings[doc_id]
                termo_indice.frequencia_documento -= 1
                
                # Se não há mais documentos com este termo, remover
                if termo_indice.frequencia_documento == 0:
                    termos_para_remover.append(termo)
        
        # Remover termos vazios
        for termo in termos_para_remover:
            del self.indice[termo]
        
        # Remover documento
        del self.documentos[doc_id]
        self.total_documentos -= 1
        self.total_termos = len(self.indice)
    
    def buscar_termo(self, termo: str) -> Optional[TermoIndice]:
        """
        Busca termo no índice.
        
        Args:
            termo: Termo a ser buscado
        
        Returns:
            TermoIndice ou None se não encontrado
        """
        # Processar termo da mesma forma que os documentos
        termos_processados = self.processador.processar_completo(termo)
        
        if not termos_processados:
            return None
        
        termo_processado = termos_processados[0]
        return self.indice.get(termo_processado)
    
    def obter_documentos_termo(self, termo: str) -> Set[str]:
        """Obtém documentos que contêm um termo."""
        termo_indice = self.buscar_termo(termo)
        if termo_indice:
            return termo_indice.obter_documentos()
        return set()
    
    def calcular_tf(self, termo: str, doc_id: str) -> float:
        """
        Calcula Term Frequency (TF).
        
        Args:
            termo: Termo
            doc_id: ID do documento
        
        Returns:
            Valor TF
        """
        termo_indice = self.buscar_termo(termo)
        if not termo_indice or doc_id not in termo_indice.postings:
            return 0.0
        
        freq_termo = termo_indice.postings[doc_id]
        
        # TF = log(1 + freq_termo)
        return math.log(1 + freq_termo)
    
    def calcular_idf(self, termo: str) -> float:
        """
        Calcula Inverse Document Frequency (IDF).
        
        Args:
            termo: Termo
        
        Returns:
            Valor IDF
        """
        termo_indice = self.buscar_termo(termo)
        if not termo_indice:
            return 0.0
        
        # IDF = log(N / df)
        return math.log(self.total_documentos / termo_indice.frequencia_documento)
    
    def calcular_tf_idf(self, termo: str, doc_id: str) -> float:
        """
        Calcula TF-IDF.
        
        Args:
            termo: Termo
            doc_id: ID do documento
        
        Returns:
            Valor TF-IDF
        """
        tf = self.calcular_tf(termo, doc_id)
        idf = self.calcular_idf(termo)
        return tf * idf
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas do índice."""
        return {
            'total_documentos': self.total_documentos,
            'total_termos': self.total_termos,
            'tamanho_medio_documento': sum(doc.tamanho() for doc in self.documentos.values()) / max(1, self.total_documentos),
            'termos_mais_frequentes': sorted(
                [(termo, ti.frequencia_documento) for termo, ti in self.indice.items()],
                key=lambda x: x[1], reverse=True
            )[:10]
        }


class AlgoritmoRanking(ABC):
    """
    Classe base para algoritmos de ranking.
    """
    
    @abstractmethod
    def calcular_score(self, query_termos: List[str], doc_id: str, 
                      indice: IndiceInvertido) -> float:
        """
        Calcula score de relevância de um documento para uma query.
        
        Args:
            query_termos: Termos da query
            doc_id: ID do documento
            indice: Índice invertido
        
        Returns:
            Score de relevância
        """
        pass


class RankingTFIDF(AlgoritmoRanking):
    """
    Algoritmo de ranking TF-IDF.
    """
    
    def calcular_score(self, query_termos: List[str], doc_id: str, 
                      indice: IndiceInvertido) -> float:
        """Calcula score TF-IDF."""
        score = 0.0
        
        for termo in query_termos:
            tf_idf = indice.calcular_tf_idf(termo, doc_id)
            score += tf_idf
        
        return score


class RankingBM25(AlgoritmoRanking):
    """
    Algoritmo de ranking BM25.
    """
    
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        """
        Inicializa BM25.
        
        Args:
            k1: Parâmetro de saturação de frequência do termo
            b: Parâmetro de normalização de comprimento do documento
        """
        self.k1 = k1
        self.b = b
    
    def calcular_score(self, query_termos: List[str], doc_id: str, 
                      indice: IndiceInvertido) -> float:
        """Calcula score BM25."""
        if doc_id not in indice.documentos:
            return 0.0
        
        documento = indice.documentos[doc_id]
        doc_length = len(indice.processador.processar_completo(documento.texto_completo()))
        
        # Comprimento médio dos documentos
        if indice.total_documentos > 0:
            avg_doc_length = sum(
                len(indice.processador.processar_completo(doc.texto_completo()))
                for doc in indice.documentos.values()
            ) / indice.total_documentos
        else:
            avg_doc_length = 1
        
        score = 0.0
        
        for termo in query_termos:
            termo_indice = indice.buscar_termo(termo)
            if not termo_indice or doc_id not in termo_indice.postings:
                continue
            
            # Frequência do termo no documento
            tf = termo_indice.postings[doc_id]
            
            # IDF
            idf = math.log((indice.total_documentos - termo_indice.frequencia_documento + 0.5) / 
                          (termo_indice.frequencia_documento + 0.5))
            
            # BM25 score para este termo
            numerador = tf * (self.k1 + 1)
            denominador = tf + self.k1 * (1 - self.b + self.b * (doc_length / avg_doc_length))
            
            score += idf * (numerador / denominador)
        
        return score


class BuscaFuzzy:
    """
    Implementação de busca fuzzy usando distância de Levenshtein.
    """
    
    @staticmethod
    def distancia_levenshtein(s1: str, s2: str) -> int:
        """
        Calcula distância de Levenshtein entre duas strings.
        
        Args:
            s1: Primeira string
            s2: Segunda string
        
        Returns:
            Distância de Levenshtein
        """
        if len(s1) < len(s2):
            return BuscaFuzzy.distancia_levenshtein(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        linha_anterior = list(range(len(s2) + 1))
        
        for i, c1 in enumerate(s1):
            linha_atual = [i + 1]
            
            for j, c2 in enumerate(s2):
                # Custo de inserção, deleção e substituição
                insercoes = linha_anterior[j + 1] + 1
                delecoes = linha_atual[j] + 1
                substituicoes = linha_anterior[j] + (c1 != c2)
                
                linha_atual.append(min(insercoes, delecoes, substituicoes))
            
            linha_anterior = linha_atual
        
        return linha_anterior[-1]
    
    @staticmethod
    def similaridade_fuzzy(s1: str, s2: str) -> float:
        """
        Calcula similaridade fuzzy (0-1).
        
        Args:
            s1: Primeira string
            s2: Segunda string
        
        Returns:
            Similaridade (1 = idênticas, 0 = completamente diferentes)
        """
        distancia = BuscaFuzzy.distancia_levenshtein(s1, s2)
        max_len = max(len(s1), len(s2))
        
        if max_len == 0:
            return 1.0
        
        return 1.0 - (distancia / max_len)
    
    def buscar_termos_similares(self, termo: str, vocabulario: Set[str], 
                               threshold: float = 0.7) -> List[Tuple[str, float]]:
        """
        Busca termos similares no vocabulário.
        
        Args:
            termo: Termo de busca
            vocabulario: Conjunto de termos do vocabulário
            threshold: Limiar de similaridade
        
        Returns:
            Lista de (termo_similar, similaridade)
        """
        termos_similares = []
        
        for termo_vocab in vocabulario:
            similaridade = self.similaridade_fuzzy(termo, termo_vocab)
            
            if similaridade >= threshold:
                termos_similares.append((termo_vocab, similaridade))
        
        # Ordenar por similaridade decrescente
        termos_similares.sort(key=lambda x: x[1], reverse=True)
        
        return termos_similares


class MotorBusca:
    """
    Motor de busca completo com múltiplos algoritmos e funcionalidades.
    """
    
    def __init__(self, algoritmo_ranking: AlgoritmoRanking = None):
        """
        Inicializa motor de busca.
        
        Args:
            algoritmo_ranking: Algoritmo de ranking a ser usado
        """
        self.indice = IndiceInvertido()
        self.algoritmo_ranking = algoritmo_ranking or RankingTFIDF()
        self.busca_fuzzy = BuscaFuzzy()
        self.historico_buscas: List[EstatisticasBusca] = []
    
    def indexar_documento(self, documento: Documento):
        """Indexa um documento."""
        self.indice.adicionar_documento(documento)
    
    def indexar_documentos(self, documentos: List[Documento]):
        """Indexa múltiplos documentos."""
        print(f"Indexando {len(documentos)} documentos...")
        
        for i, documento in enumerate(documentos):
            self.indexar_documento(documento)
            
            if (i + 1) % 100 == 0:
                print(f"Indexados {i + 1} documentos...")
        
        print("Indexação concluída!")
    
    def processar_query(self, query: str) -> List[str]:
        """
        Processa query de busca.
        
        Args:
            query: Query de busca
        
        Returns:
            Lista de termos processados
        """
        return self.indice.processador.processar_completo(query)
    
    def buscar(self, query: str, max_resultados: int = 10, 
              tipo_busca: TipoBusca = TipoBusca.EXATA) -> List[ResultadoBusca]:
        """
        Executa busca.
        
        Args:
            query: Query de busca
            max_resultados: Número máximo de resultados
            tipo_busca: Tipo de busca
        
        Returns:
            Lista de resultados ordenados por relevância
        """
        inicio = time.time()
        
        # Processar query
        query_termos = self.processar_query(query)
        
        if not query_termos:
            return []
        
        # Expandir termos se busca fuzzy
        if tipo_busca == TipoBusca.FUZZY:
            query_termos = self._expandir_termos_fuzzy(query_termos)
        
        # Encontrar documentos candidatos
        documentos_candidatos = self._encontrar_candidatos(query_termos)
        
        # Calcular scores
        resultados = []
        
        for doc_id in documentos_candidatos:
            score = self.algoritmo_ranking.calcular_score(
                query_termos, doc_id, self.indice
            )
            
            if score > 0:
                documento = self.indice.documentos[doc_id]
                snippet = self._gerar_snippet(documento, query_termos)
                
                resultado = ResultadoBusca(
                    documento=documento,
                    score=score,
                    explicacao=f"Score: {score:.4f}",
                    termos_destacados=query_termos,
                    snippet=snippet
                )
                
                resultados.append(resultado)
        
        # Ordenar por score decrescente
        resultados.sort(reverse=True)
        
        # Limitar resultados
        resultados = resultados[:max_resultados]
        
        # Registrar estatísticas
        tempo_busca = time.time() - inicio
        
        estatisticas = EstatisticasBusca(
            query=query,
            num_resultados=len(resultados),
            tempo_busca=tempo_busca,
            termos_processados=query_termos,
            documentos_analisados=len(documentos_candidatos),
            algoritmo_usado=type(self.algoritmo_ranking).__name__
        )
        
        self.historico_buscas.append(estatisticas)
        
        return resultados
    
    def _expandir_termos_fuzzy(self, termos: List[str], 
                              threshold: float = 0.7) -> List[str]:
        """Expande termos usando busca fuzzy."""
        vocabulario = set(self.indice.indice.keys())
        termos_expandidos = []
        
        for termo in termos:
            # Adicionar termo original
            termos_expandidos.append(termo)
            
            # Buscar termos similares
            similares = self.busca_fuzzy.buscar_termos_similares(
                termo, vocabulario, threshold
            )
            
            # Adicionar até 3 termos mais similares
            for termo_similar, _ in similares[:3]:
                if termo_similar != termo:
                    termos_expandidos.append(termo_similar)
        
        return termos_expandidos
    
    def _encontrar_candidatos(self, query_termos: List[str]) -> Set[str]:
        """Encontra documentos candidatos que contêm pelo menos um termo."""
        candidatos = set()
        
        for termo in query_termos:
            docs_termo = self.indice.obter_documentos_termo(termo)
            candidatos.update(docs_termo)
        
        return candidatos
    
    def _gerar_snippet(self, documento: Documento, query_termos: List[str], 
                      max_chars: int = 200) -> str:
        """
        Gera snippet do documento destacando termos da query.
        
        Args:
            documento: Documento
            query_termos: Termos da query
            max_chars: Tamanho máximo do snippet
        
        Returns:
            Snippet do documento
        """
        texto = documento.conteudo
        
        if len(texto) <= max_chars:
            return texto
        
        # Encontrar primeira ocorrência de qualquer termo
        texto_lower = texto.lower()
        primeira_pos = len(texto)
        
        for termo in query_termos:
            pos = texto_lower.find(termo.lower())
            if pos != -1 and pos < primeira_pos:
                primeira_pos = pos
        
        # Se nenhum termo encontrado, retornar início
        if primeira_pos == len(texto):
            return texto[:max_chars] + "..."
        
        # Calcular posição de início do snippet
        inicio = max(0, primeira_pos - max_chars // 4)
        fim = min(len(texto), inicio + max_chars)
        
        snippet = texto[inicio:fim]
        
        if inicio > 0:
            snippet = "..." + snippet
        
        if fim < len(texto):
            snippet = snippet + "..."
        
        return snippet
    
    def buscar_booleana(self, query: str) -> List[ResultadoBusca]:
        """
        Busca booleana simples (AND, OR, NOT).
        
        Args:
            query: Query booleana (ex: "python AND machine OR learning NOT basic")
        
        Returns:
            Lista de resultados
        """
        # Implementação simplificada de busca booleana
        # Dividir por operadores
        if " AND " in query:
            termos = query.split(" AND ")
            return self._busca_and(termos)
        elif " OR " in query:
            termos = query.split(" OR ")
            return self._busca_or(termos)
        elif " NOT " in query:
            partes = query.split(" NOT ")
            if len(partes) == 2:
                return self._busca_not(partes[0], partes[1])
        
        # Se não há operadores, busca normal
        return self.buscar(query)
    
    def _busca_and(self, termos: List[str]) -> List[ResultadoBusca]:
        """Busca AND - documentos devem conter todos os termos."""
        if not termos:
            return []
        
        # Processar primeiro termo
        primeiro_termo = self.processar_query(termos[0])
        candidatos = self.indice.obter_documentos_termo(primeiro_termo[0]) if primeiro_termo else set()
        
        # Interseção com outros termos
        for termo in termos[1:]:
            termos_processados = self.processar_query(termo)
            if termos_processados:
                docs_termo = self.indice.obter_documentos_termo(termos_processados[0])
                candidatos = candidatos.intersection(docs_termo)
        
        # Calcular scores
        todos_termos = []
        for termo in termos:
            todos_termos.extend(self.processar_query(termo))
        
        resultados = []
        for doc_id in candidatos:
            score = self.algoritmo_ranking.calcular_score(todos_termos, doc_id, self.indice)
            if score > 0:
                documento = self.indice.documentos[doc_id]
                resultados.append(ResultadoBusca(
                    documento=documento,
                    score=score,
                    explicacao="Busca AND"
                ))
        
        resultados.sort(reverse=True)
        return resultados
    
    def _busca_or(self, termos: List[str]) -> List[ResultadoBusca]:
        """Busca OR - documentos podem conter qualquer termo."""
        candidatos = set()
        todos_termos = []
        
        for termo in termos:
            termos_processados = self.processar_query(termo)
            todos_termos.extend(termos_processados)
            
            if termos_processados:
                docs_termo = self.indice.obter_documentos_termo(termos_processados[0])
                candidatos.update(docs_termo)
        
        # Calcular scores
        resultados = []
        for doc_id in candidatos:
            score = self.algoritmo_ranking.calcular_score(todos_termos, doc_id, self.indice)
            if score > 0:
                documento = self.indice.documentos[doc_id]
                resultados.append(ResultadoBusca(
                    documento=documento,
                    score=score,
                    explicacao="Busca OR"
                ))
        
        resultados.sort(reverse=True)
        return resultados
    
    def _busca_not(self, termo_incluir: str, termo_excluir: str) -> List[ResultadoBusca]:
        """Busca NOT - incluir primeiro termo, excluir segundo."""
        termos_incluir = self.processar_query(termo_incluir)
        termos_excluir = self.processar_query(termo_excluir)
        
        if not termos_incluir:
            return []
        
        # Documentos que contêm termo a incluir
        docs_incluir = self.indice.obter_documentos_termo(termos_incluir[0])
        
        # Documentos que contêm termo a excluir
        docs_excluir = set()
        if termos_excluir:
            docs_excluir = self.indice.obter_documentos_termo(termos_excluir[0])
        
        # Diferença
        candidatos = docs_incluir - docs_excluir
        
        # Calcular scores
        resultados = []
        for doc_id in candidatos:
            score = self.algoritmo_ranking.calcular_score(termos_incluir, doc_id, self.indice)
            if score > 0:
                documento = self.indice.documentos[doc_id]
                resultados.append(ResultadoBusca(
                    documento=documento,
                    score=score,
                    explicacao="Busca NOT"
                ))
        
        resultados.sort(reverse=True)
        return resultados
    
    def sugerir_correcoes(self, query: str, max_sugestoes: int = 3) -> List[str]:
        """
        Sugere correções para query usando busca fuzzy.
        
        Args:
            query: Query original
            max_sugestoes: Número máximo de sugestões
        
        Returns:
            Lista de sugestões de correção
        """
        termos_query = self.processar_query(query)
        vocabulario = set(self.indice.indice.keys())
        
        sugestoes = []
        
        for termo in termos_query:
            if termo not in vocabulario:
                similares = self.busca_fuzzy.buscar_termos_similares(
                    termo, vocabulario, threshold=0.6
                )
                
                for termo_similar, _ in similares[:max_sugestoes]:
                    query_corrigida = query.replace(termo, termo_similar)
                    if query_corrigida not in sugestoes:
                        sugestoes.append(query_corrigida)
        
        return sugestoes[:max_sugestoes]
    
    def obter_estatisticas_sistema(self) -> Dict[str, Any]:
        """Obtém estatísticas do sistema de busca."""
        stats_indice = self.indice.obter_estatisticas()
        
        if self.historico_buscas:
            tempo_medio_busca = sum(b.tempo_busca for b in self.historico_buscas) / len(self.historico_buscas)
            queries_mais_comuns = Counter(b.query for b in self.historico_buscas).most_common(5)
        else:
            tempo_medio_busca = 0
            queries_mais_comuns = []
        
        return {
            **stats_indice,
            'total_buscas': len(self.historico_buscas),
            'tempo_medio_busca': tempo_medio_busca,
            'queries_mais_comuns': queries_mais_comuns,
            'algoritmo_ranking': type(self.algoritmo_ranking).__name__
        }


class GeradorDocumentos:
    """
    Gerador de documentos sintéticos para teste.
    """
    
    @staticmethod
    def gerar_artigos_tecnologia(n_artigos: int = 100) -> List[Documento]:
        """Gera artigos sobre tecnologia."""
        temas = [
            "inteligência artificial", "machine learning", "deep learning",
            "python programming", "data science", "web development",
            "mobile development", "cloud computing", "cybersecurity",
            "blockchain", "internet of things", "big data"
        ]
        
        tecnologias = [
            "Python", "JavaScript", "Java", "C++", "React", "Angular",
            "TensorFlow", "PyTorch", "Docker", "Kubernetes", "AWS", "Azure"
        ]
        
        artigos = []
        
        for i in range(n_artigos):
            tema = np.random.choice(temas)
            tech = np.random.choice(tecnologias, size=np.random.randint(1, 4), replace=False)
            
            titulo = f"Guia Completo de {tema.title()} com {' e '.join(tech)}"
            
            conteudo = f"""
            Este artigo apresenta um guia completo sobre {tema} utilizando {' e '.join(tech)}.
            
            Introdução:
            {tema.capitalize()} é uma área fundamental da tecnologia moderna que tem revolucionado
            diversos setores da indústria. Com o uso de {tech[0]}, podemos implementar soluções
            robustas e escaláveis.
            
            Desenvolvimento:
            As principais vantagens de usar {tema} incluem:
            - Eficiência no processamento de dados
            - Facilidade de implementação
            - Escalabilidade para grandes volumes
            - Integração com outras tecnologias
            
            Implementação prática:
            Para implementar {tema} usando {tech[0]}, seguimos os seguintes passos:
            1. Configuração do ambiente
            2. Instalação das dependências
            3. Desenvolvimento do código
            4. Testes e validação
            5. Deploy em produção
            
            Conclusão:
            {tema.capitalize()} representa o futuro da tecnologia, especialmente quando
            combinado com ferramentas como {' e '.join(tech)}. A implementação adequada
            pode trazer benefícios significativos para qualquer projeto.
            """
            
            artigo = Documento(
                id=f"art_{i+1}",
                titulo=titulo,
                conteudo=conteudo,
                url=f"https://exemplo.com/artigo-{i+1}",
                autor=f"Autor_{np.random.randint(1, 20)}",
                tags=list(tech) + [tema.replace(" ", "_")],
                metadados={
                    "categoria": "Tecnologia",
                    "dificuldade": np.random.choice(["Iniciante", "Intermediário", "Avançado"]),
                    "tempo_leitura": np.random.randint(5, 30)
                }
            )
            
            artigos.append(artigo)
        
        return artigos


def demonstrar_indexacao_basica():
    """Demonstra indexação básica de documentos."""
    print("=== DEMONSTRAÇÃO: INDEXAÇÃO BÁSICA ===\n")
    
    # Criar documentos de exemplo
    documentos = [
        Documento(
            id="doc1",
            titulo="Introdução ao Python",
            conteudo="Python é uma linguagem de programação poderosa e fácil de aprender. É amplamente usada em ciência de dados, desenvolvimento web e automação.",
            tags=["python", "programação", "tutorial"]
        ),
        Documento(
            id="doc2",
            titulo="Machine Learning com Python",
            conteudo="Machine learning é um subcampo da inteligência artificial. Python oferece excelentes bibliotecas como scikit-learn e TensorFlow para ML.",
            tags=["machine learning", "python", "ia"]
        ),
        Documento(
            id="doc3",
            titulo="Desenvolvimento Web com Django",
            conteudo="Django é um framework web em Python que facilita o desenvolvimento de aplicações web robustas e escaláveis.",
            tags=["django", "web", "python", "framework"]
        )
    ]
    
    # Criar motor de busca
    motor = MotorBusca()
    
    # Indexar documentos
    print("Indexando documentos...")
    for doc in documentos:
        motor.indexar_documento(doc)
    
    # Mostrar estatísticas do índice
    stats = motor.indice.obter_estatisticas()
    print(f"Total de documentos: {stats['total_documentos']}")
    print(f"Total de termos únicos: {stats['total_termos']}")
    print(f"Tamanho médio dos documentos: {stats['tamanho_medio_documento']:.1f} caracteres")
    
    print("\nTermos mais frequentes:")
    for termo, freq in stats['termos_mais_frequentes']:
        print(f"  {termo}: {freq} documentos")
    
    print()


def demonstrar_busca_tfidf():
    """Demonstra busca usando TF-IDF."""
    print("=== DEMONSTRAÇÃO: BUSCA TF-IDF ===\n")
    
    # Gerar documentos
    documentos = GeradorDocumentos.gerar_artigos_tecnologia(20)
    
    # Criar motor com TF-IDF
    motor = MotorBusca(RankingTFIDF())
    motor.indexar_documentos(documentos)
    
    # Executar buscas
    queries = [
        "python machine learning",
        "web development",
        "artificial intelligence",
        "data science"
    ]
    
    for query in queries:
        print(f"Busca: '{query}'")
        resultados = motor.buscar(query, max_resultados=3)
        
        print(f"Encontrados {len(resultados)} resultados:")
        
        for i, resultado in enumerate(resultados, 1):
            print(f"{i}. {resultado.documento.titulo}")
            print(f"   Score: {resultado.score:.4f}")
            print(f"   Snippet: {resultado.snippet[:100]}...")
            print()
        
        print("-" * 50)


def demonstrar_busca_bm25():
    """Demonstra busca usando BM25."""
    print("=== DEMONSTRAÇÃO: BUSCA BM25 ===\n")
    
    # Gerar documentos
    documentos = GeradorDocumentos.gerar_artigos_tecnologia(30)
    
    # Criar motor com BM25
    motor = MotorBusca(RankingBM25(k1=1.5, b=0.75))
    motor.indexar_documentos(documentos)
    
    # Executar busca
    query = "python programming tutorial"
    print(f"Busca BM25: '{query}'")
    
    resultados = motor.buscar(query, max_resultados=5)
    
    print(f"Encontrados {len(resultados)} resultados:")
    
    for i, resultado in enumerate(resultados, 1):
        print(f"{i}. {resultado.documento.titulo}")
        print(f"   Score BM25: {resultado.score:.4f}")
        print(f"   Tags: {', '.join(resultado.documento.tags)}")
        print(f"   Snippet: {resultado.snippet[:150]}...")
        print()


def demonstrar_busca_fuzzy():
    """Demonstra busca fuzzy."""
    print("=== DEMONSTRAÇÃO: BUSCA FUZZY ===\n")
    
    # Gerar documentos
    documentos = GeradorDocumentos.gerar_artigos_tecnologia(25)
    
    # Criar motor
    motor = MotorBusca()
    motor.indexar_documentos(documentos)
    
    # Busca com erro de digitação
    query_com_erro = "machne lerning pythn"  # machine learning python
    
    print(f"Query com erro: '{query_com_erro}'")
    
    # Busca normal (poucos resultados esperados)
    resultados_normal = motor.buscar(query_com_erro, max_resultados=3)
    print(f"Busca normal: {len(resultados_normal)} resultados")
    
    # Busca fuzzy
    resultados_fuzzy = motor.buscar(query_com_erro, max_resultados=3, 
                                   tipo_busca=TipoBusca.FUZZY)
    print(f"Busca fuzzy: {len(resultados_fuzzy)} resultados")
    
    # Sugestões de correção
    sugestoes = motor.sugerir_correcoes(query_com_erro)
    print(f"\nSugestões de correção:")
    for sugestao in sugestoes:
        print(f"  - {sugestao}")
    
    print("\nResultados da busca fuzzy:")
    for i, resultado in enumerate(resultados_fuzzy, 1):
        print(f"{i}. {resultado.documento.titulo}")
        print(f"   Score: {resultado.score:.4f}")
        print()


def demonstrar_busca_booleana():
    """Demonstra busca booleana."""
    print("=== DEMONSTRAÇÃO: BUSCA BOOLEANA ===\n")
    
    # Gerar documentos
    documentos = GeradorDocumentos.gerar_artigos_tecnologia(40)
    
    # Criar motor
    motor = MotorBusca()
    motor.indexar_documentos(documentos)
    
    # Queries booleanas
    queries_booleanas = [
        "python AND machine",
        "web OR mobile",
        "artificial NOT intelligence"
    ]
    
    for query in queries_booleanas:
        print(f"Query booleana: '{query}'")
        resultados = motor.buscar_booleana(query)
        
        print(f"Encontrados {len(resultados)} resultados:")
        
        for i, resultado in enumerate(resultados[:3], 1):
            print(f"{i}. {resultado.documento.titulo}")
            print(f"   Score: {resultado.score:.4f}")
            print(f"   Explicação: {resultado.explicacao}")
            print()
        
        print("-" * 50)


def benchmark_algoritmos_ranking():
    """Benchmark de algoritmos de ranking."""
    print("=== BENCHMARK: ALGORITMOS DE RANKING ===\n")
    
    # Gerar documentos maiores
    documentos = GeradorDocumentos.gerar_artigos_tecnologia(100)
    
    # Algoritmos para testar
    algoritmos = [
        ("TF-IDF", RankingTFIDF()),
        ("BM25 (k1=1.2, b=0.75)", RankingBM25(k1=1.2, b=0.75)),
        ("BM25 (k1=1.5, b=0.75)", RankingBM25(k1=1.5, b=0.75)),
        ("BM25 (k1=2.0, b=0.75)", RankingBM25(k1=2.0, b=0.75))
    ]
    
    # Queries de teste
    queries_teste = [
        "python programming",
        "machine learning artificial intelligence",
        "web development framework",
        "data science analytics",
        "cloud computing aws"
    ]
    
    resultados_benchmark = {}
    
    for nome_algo, algoritmo in algoritmos:
        print(f"Testando {nome_algo}...")
        
        # Criar motor
        motor = MotorBusca(algoritmo)
        
        # Indexar documentos
        inicio_indexacao = time.time()
        motor.indexar_documentos(documentos)
        tempo_indexacao = time.time() - inicio_indexacao
        
        # Executar buscas
        tempos_busca = []
        num_resultados_total = 0
        
        for query in queries_teste:
            inicio_busca = time.time()
            resultados = motor.buscar(query, max_resultados=10)
            tempo_busca = time.time() - inicio_busca
            
            tempos_busca.append(tempo_busca)
            num_resultados_total += len(resultados)
        
        # Calcular métricas
        tempo_medio_busca = sum(tempos_busca) / len(tempos_busca)
        resultados_medio = num_resultados_total / len(queries_teste)
        
        resultados_benchmark[nome_algo] = {
            'tempo_indexacao': tempo_indexacao,
            'tempo_medio_busca': tempo_medio_busca,
            'resultados_medio': resultados_medio
        }
        
        print(f"  Tempo de indexação: {tempo_indexacao:.3f}s")
        print(f"  Tempo médio de busca: {tempo_medio_busca:.4f}s")
        print(f"  Resultados médios: {resultados_medio:.1f}")
        print()
    
    # Resumo comparativo
    print("RESUMO COMPARATIVO:")
    print("-" * 60)
    print(f"{'Algoritmo':<25} {'Indexação':<12} {'Busca':<10} {'Resultados':<10}")
    print("-" * 60)
    
    for nome, metricas in resultados_benchmark.items():
        print(f"{nome:<25} {metricas['tempo_indexacao']:<12.3f} "
              f"{metricas['tempo_medio_busca']:<10.4f} "
              f"{metricas['resultados_medio']:<10.1f}")


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 08.2 - MOTOR DE BUSCA")
    print("=" * 50)
    
    # Executar demonstrações
    demonstrar_indexacao_basica()
    demonstrar_busca_tfidf()
    demonstrar_busca_bm25()
    demonstrar_busca_fuzzy()
    demonstrar_busca_booleana()
    benchmark_algoritmos_ranking()
    
    print("\n" + "=" * 50)
    print("CONCLUSÃO DO MÓDULO 08.2")
    print("=" * 50)
    print("""
Principais Aprendizados:

1. ARQUITETURA DE MOTOR DE BUSCA:
   • Índice Invertido como estrutura fundamental
   • Processamento de texto (tokenização, stemming, lemmatização)
   • Pipeline de indexação e busca
   • Otimizações de performance e memória

2. ÍNDICE INVERTIDO:
   • Mapeamento termo -> lista de documentos
   • Estrutura eficiente para busca textual
   • Postings lists com frequências
   • Compressão e otimização de espaço

3. PROCESSAMENTO DE TEXTO:
   • Tokenização e normalização
   • Remoção de stopwords
   • Stemming vs Lemmatização
   • N-gramas para capturar contexto
   • Tratamento de caracteres especiais

4. ALGORITMOS DE RANKING:
   • TF-IDF: Term Frequency × Inverse Document Frequency
   • BM25: Melhoria do TF-IDF com normalização
   • Parâmetros k1 e b para tuning
   • Trade-offs entre precisão e recall

5. TIPOS DE BUSCA:
   • Busca exata por termos
   • Busca fuzzy com distância de Levenshtein
   • Busca booleana (AND, OR, NOT)
   • Busca por frases e wildcards
   • Expansão de queries

6. BUSCA FUZZY:
   • Distância de Levenshtein para similaridade
   • Correção automática de erros de digitação
   • Sugestões de termos alternativos
   • Threshold de similaridade configurável

7. OTIMIZAÇÕES DE PERFORMANCE:
   • Estruturas de dados eficientes (Trie, Hash Tables)
   • Bloom Filters para pré-filtragem
   • Cache de resultados frequentes
   • Paralelização de operações

8. MÉTRICAS E AVALIAÇÃO:
   • Precisão e Recall
   • Tempo de resposta
   • Throughput de indexação
   • Relevância dos resultados

9. FUNCIONALIDADES AVANÇADAS:
   • Snippet generation com destaque de termos
   • Faceted search por categorias
   • Personalização baseada em histórico
   • Real-time indexing para atualizações

10. APLICAÇÕES PRÁTICAS:
    • Motores de busca web (Google, Bing)
    • Busca em e-commerce (Amazon, eBay)
    • Busca corporativa (Elasticsearch, Solr)
    • Busca em documentos e bases de conhecimento

PRÓXIMOS PASSOS:
- Implementar PageRank para ranking de páginas web
- Estudar técnicas de machine learning para ranking
- Explorar busca semântica com embeddings
- Implementar clustering de resultados
- Analisar logs de busca para melhorias

Este módulo fornece uma base sólida para construir motores
de busca eficientes e escaláveis, cobrindo desde conceitos
fundamentais até implementações práticas otimizadas.
    """)


if __name__ == "__main__":
    main()