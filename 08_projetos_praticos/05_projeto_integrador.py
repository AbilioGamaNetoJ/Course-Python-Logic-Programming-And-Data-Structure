"""
MÓDULO 08.5 - PROJETO INTEGRADOR: SISTEMA DE ANÁLISE EMPRESARIAL
===============================================================

PROJETO FINAL DO CURSO DE LÓGICA DE PROGRAMAÇÃO E ESTRUTURAS DE DADOS

Objetivos do Projeto:
- Integrar TODOS os conceitos aprendidos no curso
- Demonstrar aplicação prática em cenário empresarial
- Implementar sistema completo com múltiplos módulos
- Aplicar boas práticas de programação e arquitetura
- Criar interface de usuário intuitiva
- Implementar persistência de dados
- Aplicar análise de performance e otimização

Conceitos Integrados:
- Estruturas de Dados (Listas, Dicionários, Árvores, Grafos)
- Algoritmos de Ordenação e Busca
- Programação Orientada a Objetos
- Tratamento de Exceções
- Análise de Complexidade
- Otimização de Código
- Sistemas de Recomendação
- Motor de Busca
- Simulação de Eventos
- Análise de Dados

Arquitetura do Sistema:
- Camada de Dados (Persistência e Cache)
- Camada de Negócios (Lógica Empresarial)
- Camada de Serviços (APIs Internas)
- Camada de Apresentação (Interface)
- Camada de Análise (Business Intelligence)

Funcionalidades Principais:
- Gestão de Clientes e Produtos
- Sistema de Vendas e Estoque
- Análise de Performance de Vendas
- Recomendações Personalizadas
- Busca Inteligente de Produtos
- Simulação de Cenários de Negócio
- Dashboard Executivo
- Relatórios Automatizados
"""

import json
import csv
import sqlite3
import pickle
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict, deque, Counter
from abc import ABC, abstractmethod
import heapq
import random
import math
import statistics
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sistema_empresarial.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS E TIPOS DE DADOS
# ============================================================================

class StatusPedido(Enum):
    """Status possíveis de um pedido."""
    PENDENTE = "Pendente"
    PROCESSANDO = "Processando"
    ENVIADO = "Enviado"
    ENTREGUE = "Entregue"
    CANCELADO = "Cancelado"


class TipoCliente(Enum):
    """Tipos de cliente."""
    BRONZE = "Bronze"
    PRATA = "Prata"
    OURO = "Ouro"
    PLATINA = "Platina"


class CategoriasProduto(Enum):
    """Categorias de produtos."""
    ELETRONICOS = "Eletrônicos"
    ROUPAS = "Roupas"
    CASA = "Casa e Jardim"
    ESPORTES = "Esportes"
    LIVROS = "Livros"
    ALIMENTACAO = "Alimentação"


class TipoAnalise(Enum):
    """Tipos de análise disponíveis."""
    VENDAS = "Análise de Vendas"
    CLIENTES = "Análise de Clientes"
    PRODUTOS = "Análise de Produtos"
    ESTOQUE = "Análise de Estoque"
    FINANCEIRO = "Análise Financeira"


# ============================================================================
# MODELOS DE DADOS
# ============================================================================

@dataclass
class Endereco:
    """Modelo de endereço."""
    rua: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    
    def __str__(self) -> str:
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"


@dataclass
class Cliente:
    """Modelo de cliente."""
    id: int
    nome: str
    email: str
    telefone: str
    endereco: Endereco
    tipo: TipoCliente = TipoCliente.BRONZE
    data_cadastro: datetime = field(default_factory=datetime.now)
    total_compras: float = 0.0
    numero_pedidos: int = 0
    ativo: bool = True
    
    def __post_init__(self):
        """Atualiza tipo do cliente baseado no total de compras."""
        self._atualizar_tipo_cliente()
    
    def _atualizar_tipo_cliente(self):
        """Atualiza o tipo do cliente baseado no valor total de compras."""
        if self.total_compras >= 50000:
            self.tipo = TipoCliente.PLATINA
        elif self.total_compras >= 20000:
            self.tipo = TipoCliente.OURO
        elif self.total_compras >= 5000:
            self.tipo = TipoCliente.PRATA
        else:
            self.tipo = TipoCliente.BRONZE
    
    def adicionar_compra(self, valor: float):
        """Adiciona uma compra ao histórico do cliente."""
        self.total_compras += valor
        self.numero_pedidos += 1
        self._atualizar_tipo_cliente()
    
    def calcular_desconto(self) -> float:
        """Calcula desconto baseado no tipo de cliente."""
        descontos = {
            TipoCliente.BRONZE: 0.0,
            TipoCliente.PRATA: 0.05,
            TipoCliente.OURO: 0.10,
            TipoCliente.PLATINA: 0.15
        }
        return descontos.get(self.tipo, 0.0)


@dataclass
class Produto:
    """Modelo de produto."""
    id: int
    nome: str
    descricao: str
    categoria: CategoriasProduto
    preco: float
    estoque: int
    estoque_minimo: int = 10
    peso: float = 0.0
    dimensoes: str = ""
    ativo: bool = True
    data_cadastro: datetime = field(default_factory=datetime.now)
    total_vendido: int = 0
    avaliacao_media: float = 0.0
    numero_avaliacoes: int = 0
    
    def __post_init__(self):
        """Validações pós-inicialização."""
        if self.preco < 0:
            raise ValueError("Preço não pode ser negativo")
        if self.estoque < 0:
            raise ValueError("Estoque não pode ser negativo")
    
    def esta_em_falta(self) -> bool:
        """Verifica se o produto está em falta."""
        return self.estoque <= self.estoque_minimo
    
    def pode_vender(self, quantidade: int) -> bool:
        """Verifica se é possível vender a quantidade solicitada."""
        return self.ativo and self.estoque >= quantidade
    
    def vender(self, quantidade: int) -> bool:
        """Realiza a venda do produto."""
        if self.pode_vender(quantidade):
            self.estoque -= quantidade
            self.total_vendido += quantidade
            return True
        return False
    
    def adicionar_estoque(self, quantidade: int):
        """Adiciona estoque ao produto."""
        if quantidade > 0:
            self.estoque += quantidade
    
    def adicionar_avaliacao(self, nota: float):
        """Adiciona uma avaliação ao produto."""
        if 1 <= nota <= 5:
            total_pontos = self.avaliacao_media * self.numero_avaliacoes
            self.numero_avaliacoes += 1
            self.avaliacao_media = (total_pontos + nota) / self.numero_avaliacoes


@dataclass
class ItemPedido:
    """Item de um pedido."""
    produto_id: int
    quantidade: int
    preco_unitario: float
    desconto: float = 0.0
    
    def calcular_subtotal(self) -> float:
        """Calcula o subtotal do item."""
        subtotal = self.quantidade * self.preco_unitario
        return subtotal * (1 - self.desconto)


@dataclass
class Pedido:
    """Modelo de pedido."""
    id: int
    cliente_id: int
    itens: List[ItemPedido]
    status: StatusPedido = StatusPedido.PENDENTE
    data_pedido: datetime = field(default_factory=datetime.now)
    data_entrega: Optional[datetime] = None
    desconto_total: float = 0.0
    frete: float = 0.0
    observacoes: str = ""
    
    def calcular_subtotal(self) -> float:
        """Calcula o subtotal do pedido."""
        return sum(item.calcular_subtotal() for item in self.itens)
    
    def calcular_total(self) -> float:
        """Calcula o total do pedido."""
        subtotal = self.calcular_subtotal()
        total_com_desconto = subtotal * (1 - self.desconto_total)
        return total_com_desconto + self.frete
    
    def adicionar_item(self, item: ItemPedido):
        """Adiciona um item ao pedido."""
        self.itens.append(item)
    
    def remover_item(self, produto_id: int) -> bool:
        """Remove um item do pedido."""
        for i, item in enumerate(self.itens):
            if item.produto_id == produto_id:
                del self.itens[i]
                return True
        return False
    
    def atualizar_status(self, novo_status: StatusPedido):
        """Atualiza o status do pedido."""
        self.status = novo_status
        if novo_status == StatusPedido.ENTREGUE:
            self.data_entrega = datetime.now()


# ============================================================================
# ESTRUTURAS DE DADOS AVANÇADAS
# ============================================================================

class ArvoreAVL:
    """
    Árvore AVL para indexação eficiente de dados.
    Usada para busca rápida de clientes e produtos.
    """
    
    class No:
        def __init__(self, chave, valor):
            self.chave = chave
            self.valor = valor
            self.altura = 1
            self.esquerda = None
            self.direita = None
    
    def __init__(self):
        self.raiz = None
        self.tamanho = 0
    
    def _altura(self, no):
        """Retorna a altura do nó."""
        return no.altura if no else 0
    
    def _fator_balanceamento(self, no):
        """Calcula o fator de balanceamento."""
        return self._altura(no.esquerda) - self._altura(no.direita) if no else 0
    
    def _atualizar_altura(self, no):
        """Atualiza a altura do nó."""
        if no:
            no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))
    
    def _rotacao_direita(self, y):
        """Rotação à direita."""
        x = y.esquerda
        T2 = x.direita
        
        x.direita = y
        y.esquerda = T2
        
        self._atualizar_altura(y)
        self._atualizar_altura(x)
        
        return x
    
    def _rotacao_esquerda(self, x):
        """Rotação à esquerda."""
        y = x.direita
        T2 = y.esquerda
        
        y.esquerda = x
        x.direita = T2
        
        self._atualizar_altura(x)
        self._atualizar_altura(y)
        
        return y
    
    def inserir(self, chave, valor):
        """Insere um par chave-valor na árvore."""
        self.raiz = self._inserir_recursivo(self.raiz, chave, valor)
        self.tamanho += 1
    
    def _inserir_recursivo(self, no, chave, valor):
        """Inserção recursiva com balanceamento."""
        # Inserção normal da BST
        if not no:
            return self.No(chave, valor)
        
        if chave < no.chave:
            no.esquerda = self._inserir_recursivo(no.esquerda, chave, valor)
        elif chave > no.chave:
            no.direita = self._inserir_recursivo(no.direita, chave, valor)
        else:
            # Chave já existe, atualizar valor
            no.valor = valor
            return no
        
        # Atualizar altura
        self._atualizar_altura(no)
        
        # Obter fator de balanceamento
        balance = self._fator_balanceamento(no)
        
        # Casos de rotação
        # Caso Esquerda-Esquerda
        if balance > 1 and chave < no.esquerda.chave:
            return self._rotacao_direita(no)
        
        # Caso Direita-Direita
        if balance < -1 and chave > no.direita.chave:
            return self._rotacao_esquerda(no)
        
        # Caso Esquerda-Direita
        if balance > 1 and chave > no.esquerda.chave:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)
        
        # Caso Direita-Esquerda
        if balance < -1 and chave < no.direita.chave:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)
        
        return no
    
    def buscar(self, chave):
        """Busca um valor pela chave."""
        return self._buscar_recursivo(self.raiz, chave)
    
    def _buscar_recursivo(self, no, chave):
        """Busca recursiva."""
        if not no or no.chave == chave:
            return no.valor if no else None
        
        if chave < no.chave:
            return self._buscar_recursivo(no.esquerda, chave)
        else:
            return self._buscar_recursivo(no.direita, chave)
    
    def listar_em_ordem(self):
        """Lista todos os valores em ordem."""
        resultado = []
        self._em_ordem_recursivo(self.raiz, resultado)
        return resultado
    
    def _em_ordem_recursivo(self, no, resultado):
        """Percurso em ordem recursivo."""
        if no:
            self._em_ordem_recursivo(no.esquerda, resultado)
            resultado.append((no.chave, no.valor))
            self._em_ordem_recursivo(no.direita, resultado)


class CacheInteligente:
    """
    Cache LRU (Least Recently Used) para otimização de consultas.
    """
    
    class No:
        def __init__(self, chave, valor):
            self.chave = chave
            self.valor = valor
            self.anterior = None
            self.proximo = None
    
    def __init__(self, capacidade: int = 1000):
        self.capacidade = capacidade
        self.cache = {}
        
        # Criar nós dummy para head e tail
        self.head = self.No(0, 0)
        self.tail = self.No(0, 0)
        self.head.proximo = self.tail
        self.tail.anterior = self.head
        
        self.hits = 0
        self.misses = 0
    
    def _adicionar_no(self, no):
        """Adiciona nó logo após o head."""
        no.anterior = self.head
        no.proximo = self.head.proximo
        
        self.head.proximo.anterior = no
        self.head.proximo = no
    
    def _remover_no(self, no):
        """Remove um nó da lista."""
        no.anterior.proximo = no.proximo
        no.proximo.anterior = no.anterior
    
    def _mover_para_head(self, no):
        """Move nó para o head (mais recentemente usado)."""
        self._remover_no(no)
        self._adicionar_no(no)
    
    def _remover_tail(self):
        """Remove o último nó (menos recentemente usado)."""
        ultimo_no = self.tail.anterior
        self._remover_no(ultimo_no)
        return ultimo_no
    
    def get(self, chave):
        """Obtém valor do cache."""
        if chave in self.cache:
            no = self.cache[chave]
            self._mover_para_head(no)
            self.hits += 1
            return no.valor
        else:
            self.misses += 1
            return None
    
    def put(self, chave, valor):
        """Adiciona valor ao cache."""
        if chave in self.cache:
            no = self.cache[chave]
            no.valor = valor
            self._mover_para_head(no)
        else:
            novo_no = self.No(chave, valor)
            
            if len(self.cache) >= self.capacidade:
                # Remover o menos recentemente usado
                tail = self._remover_tail()
                del self.cache[tail.chave]
            
            self.cache[chave] = novo_no
            self._adicionar_no(novo_no)
    
    def taxa_acerto(self) -> float:
        """Calcula a taxa de acerto do cache."""
        total = self.hits + self.misses
        return (self.hits / total) * 100 if total > 0 else 0.0
    
    def limpar(self):
        """Limpa o cache."""
        self.cache.clear()
        self.head.proximo = self.tail
        self.tail.anterior = self.head
        self.hits = 0
        self.misses = 0


class FilaPrioridade:
    """
    Fila de prioridade usando heap para processamento de pedidos.
    """
    
    def __init__(self):
        self.heap = []
        self.contador = 0
    
    def adicionar(self, item, prioridade):
        """Adiciona item com prioridade."""
        # Usar contador para quebrar empates (FIFO)
        heapq.heappush(self.heap, (prioridade, self.contador, item))
        self.contador += 1
    
    def remover(self):
        """Remove item de maior prioridade."""
        if self.heap:
            prioridade, contador, item = heapq.heappop(self.heap)
            return item
        return None
    
    def esta_vazia(self) -> bool:
        """Verifica se a fila está vazia."""
        return len(self.heap) == 0
    
    def tamanho(self) -> int:
        """Retorna o tamanho da fila."""
        return len(self.heap)
    
    def peek(self):
        """Visualiza o próximo item sem removê-lo."""
        if self.heap:
            return self.heap[0][2]
        return None


# ============================================================================
# CAMADA DE PERSISTÊNCIA
# ============================================================================

class GerenciadorBancoDados:
    """
    Gerenciador de banco de dados SQLite para persistência.
    """
    
    def __init__(self, nome_banco: str = "sistema_empresarial.db"):
        self.nome_banco = nome_banco
        self.conexao = None
        self._inicializar_banco()
    
    def _inicializar_banco(self):
        """Inicializa o banco de dados e cria tabelas."""
        try:
            self.conexao = sqlite3.connect(self.nome_banco, check_same_thread=False)
            self.conexao.row_factory = sqlite3.Row
            self._criar_tabelas()
            logger.info(f"Banco de dados {self.nome_banco} inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar banco de dados: {e}")
            raise
    
    def _criar_tabelas(self):
        """Cria as tabelas necessárias."""
        cursor = self.conexao.cursor()
        
        # Tabela de clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefone TEXT,
                endereco_rua TEXT,
                endereco_numero TEXT,
                endereco_bairro TEXT,
                endereco_cidade TEXT,
                endereco_estado TEXT,
                endereco_cep TEXT,
                tipo TEXT DEFAULT 'Bronze',
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_compras REAL DEFAULT 0.0,
                numero_pedidos INTEGER DEFAULT 0,
                ativo BOOLEAN DEFAULT 1
            )
        """)
        
        # Tabela de produtos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                estoque INTEGER NOT NULL,
                estoque_minimo INTEGER DEFAULT 10,
                peso REAL DEFAULT 0.0,
                dimensoes TEXT,
                ativo BOOLEAN DEFAULT 1,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_vendido INTEGER DEFAULT 0,
                avaliacao_media REAL DEFAULT 0.0,
                numero_avaliacoes INTEGER DEFAULT 0
            )
        """)
        
        # Tabela de pedidos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                status TEXT DEFAULT 'Pendente',
                data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_entrega TIMESTAMP,
                desconto_total REAL DEFAULT 0.0,
                frete REAL DEFAULT 0.0,
                observacoes TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        """)
        
        # Tabela de itens do pedido
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                desconto REAL DEFAULT 0.0,
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        """)
        
        # Índices para otimização
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_clientes_email ON clientes (email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_produtos_categoria ON produtos (categoria)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_cliente ON pedidos (cliente_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_data ON pedidos (data_pedido)")
        
        self.conexao.commit()
        logger.info("Tabelas criadas/verificadas com sucesso")
    
    def salvar_cliente(self, cliente: Cliente) -> int:
        """Salva um cliente no banco de dados."""
        cursor = self.conexao.cursor()
        
        if cliente.id == 0:  # Novo cliente
            cursor.execute("""
                INSERT INTO clientes (nome, email, telefone, endereco_rua, endereco_numero,
                                    endereco_bairro, endereco_cidade, endereco_estado, endereco_cep,
                                    tipo, total_compras, numero_pedidos, ativo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cliente.nome, cliente.email, cliente.telefone,
                cliente.endereco.rua, cliente.endereco.numero, cliente.endereco.bairro,
                cliente.endereco.cidade, cliente.endereco.estado, cliente.endereco.cep,
                cliente.tipo.value, cliente.total_compras, cliente.numero_pedidos, cliente.ativo
            ))
            cliente.id = cursor.lastrowid
        else:  # Atualizar cliente existente
            cursor.execute("""
                UPDATE clientes SET nome=?, email=?, telefone=?, endereco_rua=?, endereco_numero=?,
                                  endereco_bairro=?, endereco_cidade=?, endereco_estado=?, endereco_cep=?,
                                  tipo=?, total_compras=?, numero_pedidos=?, ativo=?
                WHERE id=?
            """, (
                cliente.nome, cliente.email, cliente.telefone,
                cliente.endereco.rua, cliente.endereco.numero, cliente.endereco.bairro,
                cliente.endereco.cidade, cliente.endereco.estado, cliente.endereco.cep,
                cliente.tipo.value, cliente.total_compras, cliente.numero_pedidos, cliente.ativo,
                cliente.id
            ))
        
        self.conexao.commit()
        return cliente.id
    
    def carregar_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """Carrega um cliente do banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        row = cursor.fetchone()
        
        if row:
            endereco = Endereco(
                rua=row['endereco_rua'],
                numero=row['endereco_numero'],
                bairro=row['endereco_bairro'],
                cidade=row['endereco_cidade'],
                estado=row['endereco_estado'],
                cep=row['endereco_cep']
            )
            
            return Cliente(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                telefone=row['telefone'],
                endereco=endereco,
                tipo=TipoCliente(row['tipo']),
                data_cadastro=datetime.fromisoformat(row['data_cadastro']),
                total_compras=row['total_compras'],
                numero_pedidos=row['numero_pedidos'],
                ativo=bool(row['ativo'])
            )
        
        return None
    
    def listar_clientes(self, ativo_apenas: bool = True) -> List[Cliente]:
        """Lista todos os clientes."""
        cursor = self.conexao.cursor()
        
        if ativo_apenas:
            cursor.execute("SELECT * FROM clientes WHERE ativo = 1 ORDER BY nome")
        else:
            cursor.execute("SELECT * FROM clientes ORDER BY nome")
        
        clientes = []
        for row in cursor.fetchall():
            endereco = Endereco(
                rua=row['endereco_rua'],
                numero=row['endereco_numero'],
                bairro=row['endereco_bairro'],
                cidade=row['endereco_cidade'],
                estado=row['endereco_estado'],
                cep=row['endereco_cep']
            )
            
            cliente = Cliente(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                telefone=row['telefone'],
                endereco=endereco,
                tipo=TipoCliente(row['tipo']),
                data_cadastro=datetime.fromisoformat(row['data_cadastro']),
                total_compras=row['total_compras'],
                numero_pedidos=row['numero_pedidos'],
                ativo=bool(row['ativo'])
            )
            clientes.append(cliente)
        
        return clientes
    
    def salvar_produto(self, produto: Produto) -> int:
        """Salva um produto no banco de dados."""
        cursor = self.conexao.cursor()
        
        if produto.id == 0:  # Novo produto
            cursor.execute("""
                INSERT INTO produtos (nome, descricao, categoria, preco, estoque, estoque_minimo,
                                    peso, dimensoes, ativo, total_vendido, avaliacao_media, numero_avaliacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                produto.nome, produto.descricao, produto.categoria.value, produto.preco,
                produto.estoque, produto.estoque_minimo, produto.peso, produto.dimensoes,
                produto.ativo, produto.total_vendido, produto.avaliacao_media, produto.numero_avaliacoes
            ))
            produto.id = cursor.lastrowid
        else:  # Atualizar produto existente
            cursor.execute("""
                UPDATE produtos SET nome=?, descricao=?, categoria=?, preco=?, estoque=?, estoque_minimo=?,
                                  peso=?, dimensoes=?, ativo=?, total_vendido=?, avaliacao_media=?, numero_avaliacoes=?
                WHERE id=?
            """, (
                produto.nome, produto.descricao, produto.categoria.value, produto.preco,
                produto.estoque, produto.estoque_minimo, produto.peso, produto.dimensoes,
                produto.ativo, produto.total_vendido, produto.avaliacao_media, produto.numero_avaliacoes,
                produto.id
            ))
        
        self.conexao.commit()
        return produto.id
    
    def carregar_produto(self, produto_id: int) -> Optional[Produto]:
        """Carrega um produto do banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        row = cursor.fetchone()
        
        if row:
            return Produto(
                id=row['id'],
                nome=row['nome'],
                descricao=row['descricao'],
                categoria=CategoriasProduto(row['categoria']),
                preco=row['preco'],
                estoque=row['estoque'],
                estoque_minimo=row['estoque_minimo'],
                peso=row['peso'],
                dimensoes=row['dimensoes'],
                ativo=bool(row['ativo']),
                data_cadastro=datetime.fromisoformat(row['data_cadastro']),
                total_vendido=row['total_vendido'],
                avaliacao_media=row['avaliacao_media'],
                numero_avaliacoes=row['numero_avaliacoes']
            )
        
        return None
    
    def listar_produtos(self, categoria: Optional[CategoriasProduto] = None, 
                       ativo_apenas: bool = True) -> List[Produto]:
        """Lista produtos com filtros opcionais."""
        cursor = self.conexao.cursor()
        
        query = "SELECT * FROM produtos WHERE 1=1"
        params = []
        
        if ativo_apenas:
            query += " AND ativo = 1"
        
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria.value)
        
        query += " ORDER BY nome"
        
        cursor.execute(query, params)
        
        produtos = []
        for row in cursor.fetchall():
            produto = Produto(
                id=row['id'],
                nome=row['nome'],
                descricao=row['descricao'],
                categoria=CategoriasProduto(row['categoria']),
                preco=row['preco'],
                estoque=row['estoque'],
                estoque_minimo=row['estoque_minimo'],
                peso=row['peso'],
                dimensoes=row['dimensoes'],
                ativo=bool(row['ativo']),
                data_cadastro=datetime.fromisoformat(row['data_cadastro']),
                total_vendido=row['total_vendido'],
                avaliacao_media=row['avaliacao_media'],
                numero_avaliacoes=row['numero_avaliacoes']
            )
            produtos.append(produto)
        
        return produtos
    
    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        if self.conexao:
            self.conexao.close()
            logger.info("Conexão com banco de dados fechada")


# ============================================================================
# CAMADA DE SERVIÇOS
# ============================================================================

class ServicoClientes:
    """
    Serviço para gerenciamento de clientes.
    """
    
    def __init__(self, bd: GerenciadorBancoDados):
        self.bd = bd
        self.cache = CacheInteligente(capacidade=500)
        self.indice_email = ArvoreAVL()
        self._carregar_indices()
    
    def _carregar_indices(self):
        """Carrega índices em memória para busca rápida."""
        clientes = self.bd.listar_clientes(ativo_apenas=False)
        for cliente in clientes:
            self.indice_email.inserir(cliente.email, cliente.id)
            self.cache.put(f"cliente_{cliente.id}", cliente)
    
    def criar_cliente(self, nome: str, email: str, telefone: str, endereco: Endereco) -> Cliente:
        """Cria um novo cliente."""
        # Verificar se email já existe
        if self.buscar_por_email(email):
            raise ValueError(f"Email {email} já está em uso")
        
        cliente = Cliente(
            id=0,  # Será definido pelo banco
            nome=nome,
            email=email,
            telefone=telefone,
            endereco=endereco
        )
        
        # Salvar no banco
        cliente_id = self.bd.salvar_cliente(cliente)
        cliente.id = cliente_id
        
        # Atualizar índices
        self.indice_email.inserir(email, cliente_id)
        self.cache.put(f"cliente_{cliente_id}", cliente)
        
        logger.info(f"Cliente criado: {nome} (ID: {cliente_id})")
        return cliente
    
    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        """Busca cliente por ID."""
        # Tentar cache primeiro
        cliente = self.cache.get(f"cliente_{cliente_id}")
        if cliente:
            return cliente
        
        # Buscar no banco
        cliente = self.bd.carregar_cliente(cliente_id)
        if cliente:
            self.cache.put(f"cliente_{cliente_id}", cliente)
        
        return cliente
    
    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email."""
        cliente_id = self.indice_email.buscar(email)
        if cliente_id:
            return self.buscar_por_id(cliente_id)
        return None
    
    def atualizar_cliente(self, cliente: Cliente) -> bool:
        """Atualiza dados do cliente."""
        try:
            self.bd.salvar_cliente(cliente)
            self.cache.put(f"cliente_{cliente.id}", cliente)
            logger.info(f"Cliente atualizado: {cliente.nome} (ID: {cliente.id})")
            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar cliente {cliente.id}: {e}")
            return False
    
    def listar_todos(self, ativo_apenas: bool = True) -> List[Cliente]:
        """Lista todos os clientes."""
        return self.bd.listar_clientes(ativo_apenas)
    
    def desativar_cliente(self, cliente_id: int) -> bool:
        """Desativa um cliente."""
        cliente = self.buscar_por_id(cliente_id)
        if cliente:
            cliente.ativo = False
            return self.atualizar_cliente(cliente)
        return False
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas dos clientes."""
        clientes = self.listar_todos(ativo_apenas=False)
        
        if not clientes:
            return {}
        
        total_clientes = len(clientes)
        clientes_ativos = len([c for c in clientes if c.ativo])
        
        # Distribuição por tipo
        distribuicao_tipo = Counter(c.tipo.value for c in clientes if c.ativo)
        
        # Estatísticas de compras
        valores_compras = [c.total_compras for c in clientes if c.ativo and c.total_compras > 0]
        
        stats = {
            'total_clientes': total_clientes,
            'clientes_ativos': clientes_ativos,
            'clientes_inativos': total_clientes - clientes_ativos,
            'distribuicao_tipo': dict(distribuicao_tipo),
            'taxa_cache': self.cache.taxa_acerto()
        }
        
        if valores_compras:
            stats.update({
                'valor_medio_compras': statistics.mean(valores_compras),
                'valor_mediano_compras': statistics.median(valores_compras),
                'maior_comprador': max(valores_compras),
                'menor_comprador': min(valores_compras)
            })
        
        return stats


class ServicoProdutos:
    """
    Serviço para gerenciamento de produtos.
    """
    
    def __init__(self, bd: GerenciadorBancoDados):
        self.bd = bd
        self.cache = CacheInteligente(capacidade=1000)
        self.indice_categoria = defaultdict(list)
        self._carregar_indices()
    
    def _carregar_indices(self):
        """Carrega índices em memória."""
        produtos = self.bd.listar_produtos(ativo_apenas=False)
        for produto in produtos:
            self.indice_categoria[produto.categoria.value].append(produto.id)
            self.cache.put(f"produto_{produto.id}", produto)
    
    def criar_produto(self, nome: str, descricao: str, categoria: CategoriasProduto,
                     preco: float, estoque: int, estoque_minimo: int = 10,
                     peso: float = 0.0, dimensoes: str = "") -> Produto:
        """Cria um novo produto."""
        produto = Produto(
            id=0,  # Será definido pelo banco
            nome=nome,
            descricao=descricao,
            categoria=categoria,
            preco=preco,
            estoque=estoque,
            estoque_minimo=estoque_minimo,
            peso=peso,
            dimensoes=dimensoes
        )
        
        # Salvar no banco
        produto_id = self.bd.salvar_produto(produto)
        produto.id = produto_id
        
        # Atualizar índices
        self.indice_categoria[categoria.value].append(produto_id)
        self.cache.put(f"produto_{produto_id}", produto)
        
        logger.info(f"Produto criado: {nome} (ID: {produto_id})")
        return produto
    
    def buscar_por_id(self, produto_id: int) -> Optional[Produto]:
        """Busca produto por ID."""
        # Tentar cache primeiro
        produto = self.cache.get(f"produto_{produto_id}")
        if produto:
            return produto
        
        # Buscar no banco
        produto = self.bd.carregar_produto(produto_id)
        if produto:
            self.cache.put(f"produto_{produto_id}", produto)
        
        return produto
    
    def buscar_por_categoria(self, categoria: CategoriasProduto) -> List[Produto]:
        """Busca produtos por categoria."""
        produtos_ids = self.indice_categoria.get(categoria.value, [])
        produtos = []
        
        for produto_id in produtos_ids:
            produto = self.buscar_por_id(produto_id)
            if produto and produto.ativo:
                produtos.append(produto)
        
        return sorted(produtos, key=lambda p: p.nome)
    
    def buscar_por_nome(self, termo: str) -> List[Produto]:
        """Busca produtos por nome (busca parcial)."""
        produtos = self.bd.listar_produtos(ativo_apenas=True)
        termo_lower = termo.lower()
        
        resultados = []
        for produto in produtos:
            if termo_lower in produto.nome.lower() or termo_lower in produto.descricao.lower():
                resultados.append(produto)
        
        return sorted(resultados, key=lambda p: p.nome)
    
    def atualizar_produto(self, produto: Produto) -> bool:
        """Atualiza dados do produto."""
        try:
            self.bd.salvar_produto(produto)
            self.cache.put(f"produto_{produto.id}", produto)
            logger.info(f"Produto atualizado: {produto.nome} (ID: {produto.id})")
            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar produto {produto.id}: {e}")
            return False
    
    def listar_todos(self, categoria: Optional[CategoriasProduto] = None) -> List[Produto]:
        """Lista todos os produtos."""
        return self.bd.listar_produtos(categoria, ativo_apenas=True)
    
    def produtos_em_falta(self) -> List[Produto]:
        """Lista produtos em falta de estoque."""
        produtos = self.listar_todos()
        return [p for p in produtos if p.esta_em_falta()]
    
    def mais_vendidos(self, limite: int = 10) -> List[Produto]:
        """Lista os produtos mais vendidos."""
        produtos = self.listar_todos()
        return sorted(produtos, key=lambda p: p.total_vendido, reverse=True)[:limite]
    
    def melhor_avaliados(self, limite: int = 10) -> List[Produto]:
        """Lista os produtos melhor avaliados."""
        produtos = [p for p in self.listar_todos() if p.numero_avaliacoes >= 5]
        return sorted(produtos, key=lambda p: p.avaliacao_media, reverse=True)[:limite]
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas dos produtos."""
        produtos = self.listar_todos()
        
        if not produtos:
            return {}
        
        # Estatísticas básicas
        total_produtos = len(produtos)
        produtos_em_falta = len(self.produtos_em_falta())
        
        # Distribuição por categoria
        distribuicao_categoria = Counter(p.categoria.value for p in produtos)
        
        # Estatísticas de preços
        precos = [p.preco for p in produtos]
        
        # Estatísticas de estoque
        estoques = [p.estoque for p in produtos]
        
        stats = {
            'total_produtos': total_produtos,
            'produtos_em_falta': produtos_em_falta,
            'distribuicao_categoria': dict(distribuicao_categoria),
            'preco_medio': statistics.mean(precos),
            'preco_mediano': statistics.median(precos),
            'preco_maximo': max(precos),
            'preco_minimo': min(precos),
            'estoque_total': sum(estoques),
            'estoque_medio': statistics.mean(estoques),
            'taxa_cache': self.cache.taxa_acerto()
        }
        
        return stats


class ServicoPedidos:
    """
    Serviço para gerenciamento de pedidos.
    """
    
    def __init__(self, bd: GerenciadorBancoDados, servico_clientes: ServicoClientes,
                 servico_produtos: ServicoProdutos):
        self.bd = bd
        self.servico_clientes = servico_clientes
        self.servico_produtos = servico_produtos
        self.fila_processamento = FilaPrioridade()
        self.pedidos_em_memoria = {}
        self.proximo_id = 1
        
        # Thread para processamento de pedidos
        self.processando = True
        self.thread_processamento = threading.Thread(target=self._processar_pedidos)
        self.thread_processamento.daemon = True
        self.thread_processamento.start()
    
    def criar_pedido(self, cliente_id: int, itens: List[Tuple[int, int]], 
                    observacoes: str = "") -> Optional[Pedido]:
        """
        Cria um novo pedido.
        
        Args:
            cliente_id: ID do cliente
            itens: Lista de tuplas (produto_id, quantidade)
            observacoes: Observações do pedido
        
        Returns:
            Pedido criado ou None se houver erro
        """
        # Verificar se cliente existe
        cliente = self.servico_clientes.buscar_por_id(cliente_id)
        if not cliente:
            logger.error(f"Cliente {cliente_id} não encontrado")
            return None
        
        # Criar itens do pedido
        itens_pedido = []
        valor_total = 0.0
        
        for produto_id, quantidade in itens:
            produto = self.servico_produtos.buscar_por_id(produto_id)
            if not produto:
                logger.error(f"Produto {produto_id} não encontrado")
                return None
            
            if not produto.pode_vender(quantidade):
                logger.error(f"Estoque insuficiente para produto {produto.nome}")
                return None
            
            item = ItemPedido(
                produto_id=produto_id,
                quantidade=quantidade,
                preco_unitario=produto.preco,
                desconto=cliente.calcular_desconto()
            )
            
            itens_pedido.append(item)
            valor_total += item.calcular_subtotal()
        
        # Criar pedido
        pedido = Pedido(
            id=self.proximo_id,
            cliente_id=cliente_id,
            itens=itens_pedido,
            observacoes=observacoes
        )
        
        self.proximo_id += 1
        
        # Calcular frete baseado no valor total
        pedido.frete = self._calcular_frete(valor_total, cliente.tipo)
        
        # Armazenar em memória
        self.pedidos_em_memoria[pedido.id] = pedido
        
        # Adicionar à fila de processamento
        prioridade = self._calcular_prioridade_pedido(cliente, valor_total)
        self.fila_processamento.adicionar(pedido.id, prioridade)
        
        logger.info(f"Pedido {pedido.id} criado para cliente {cliente.nome}")
        return pedido
    
    def _calcular_frete(self, valor_total: float, tipo_cliente: TipoCliente) -> float:
        """Calcula o frete baseado no valor total e tipo de cliente."""
        if valor_total >= 200:  # Frete grátis acima de R$ 200
            return 0.0
        
        frete_base = 15.0
        
        # Desconto no frete por tipo de cliente
        descontos_frete = {
            TipoCliente.BRONZE: 0.0,
            TipoCliente.PRATA: 0.2,
            TipoCliente.OURO: 0.4,
            TipoCliente.PLATINA: 0.6
        }
        
        desconto = descontos_frete.get(tipo_cliente, 0.0)
        return frete_base * (1 - desconto)
    
    def _calcular_prioridade_pedido(self, cliente: Cliente, valor_total: float) -> int:
        """
        Calcula prioridade do pedido (menor número = maior prioridade).
        """
        prioridade = 100  # Prioridade base
        
        # Prioridade por tipo de cliente
        prioridades_cliente = {
            TipoCliente.PLATINA: -30,
            TipoCliente.OURO: -20,
            TipoCliente.PRATA: -10,
            TipoCliente.BRONZE: 0
        }
        
        prioridade += prioridades_cliente.get(cliente.tipo, 0)
        
        # Prioridade por valor do pedido
        if valor_total >= 1000:
            prioridade -= 20
        elif valor_total >= 500:
            prioridade -= 10
        
        return prioridade
    
    def _processar_pedidos(self):
        """Thread para processar pedidos da fila."""
        while self.processando:
            try:
                if not self.fila_processamento.esta_vazia():
                    pedido_id = self.fila_processamento.remover()
                    if pedido_id in self.pedidos_em_memoria:
                        self._processar_pedido_individual(pedido_id)
                
                time.sleep(1)  # Processar a cada segundo
            except Exception as e:
                logger.error(f"Erro no processamento de pedidos: {e}")
    
    def _processar_pedido_individual(self, pedido_id: int):
        """Processa um pedido individual."""
        pedido = self.pedidos_em_memoria.get(pedido_id)
        if not pedido:
            return
        
        try:
            # Verificar e reservar estoque
            for item in pedido.itens:
                produto = self.servico_produtos.buscar_por_id(item.produto_id)
                if produto and produto.pode_vender(item.quantidade):
                    produto.vender(item.quantidade)
                    self.servico_produtos.atualizar_produto(produto)
                else:
                    # Cancelar pedido se não há estoque
                    pedido.atualizar_status(StatusPedido.CANCELADO)
                    logger.warning(f"Pedido {pedido_id} cancelado por falta de estoque")
                    return
            
            # Atualizar dados do cliente
            cliente = self.servico_clientes.buscar_por_id(pedido.cliente_id)
            if cliente:
                cliente.adicionar_compra(pedido.calcular_total())
                self.servico_clientes.atualizar_cliente(cliente)
            
            # Atualizar status do pedido
            pedido.atualizar_status(StatusPedido.PROCESSANDO)
            
            # Simular tempo de processamento
            time.sleep(2)
            
            # Finalizar processamento
            pedido.atualizar_status(StatusPedido.ENVIADO)
            
            logger.info(f"Pedido {pedido_id} processado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao processar pedido {pedido_id}: {e}")
            pedido.atualizar_status(StatusPedido.CANCELADO)
    
    def buscar_pedido(self, pedido_id: int) -> Optional[Pedido]:
        """Busca um pedido por ID."""
        return self.pedidos_em_memoria.get(pedido_id)
    
    def listar_pedidos_cliente(self, cliente_id: int) -> List[Pedido]:
        """Lista pedidos de um cliente."""
        return [p for p in self.pedidos_em_memoria.values() if p.cliente_id == cliente_id]
    
    def listar_pedidos_por_status(self, status: StatusPedido) -> List[Pedido]:
        """Lista pedidos por status."""
        return [p for p in self.pedidos_em_memoria.values() if p.status == status]
    
    def cancelar_pedido(self, pedido_id: int) -> bool:
        """Cancela um pedido."""
        pedido = self.buscar_pedido(pedido_id)
        if pedido and pedido.status in [StatusPedido.PENDENTE, StatusPedido.PROCESSANDO]:
            pedido.atualizar_status(StatusPedido.CANCELADO)
            logger.info(f"Pedido {pedido_id} cancelado")
            return True
        return False
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas dos pedidos."""
        pedidos = list(self.pedidos_em_memoria.values())
        
        if not pedidos:
            return {}
        
        # Estatísticas por status
        distribuicao_status = Counter(p.status.value for p in pedidos)
        
        # Estatísticas financeiras
        valores_pedidos = [p.calcular_total() for p in pedidos 
                          if p.status != StatusPedido.CANCELADO]
        
        stats = {
            'total_pedidos': len(pedidos),
            'pedidos_na_fila': self.fila_processamento.tamanho(),
            'distribuicao_status': dict(distribuicao_status)
        }
        
        if valores_pedidos:
            stats.update({
                'valor_total_vendas': sum(valores_pedidos),
                'valor_medio_pedido': statistics.mean(valores_pedidos),
                'valor_mediano_pedido': statistics.median(valores_pedidos),
                'maior_pedido': max(valores_pedidos),
                'menor_pedido': min(valores_pedidos)
            })
        
        return stats
    
    def parar_processamento(self):
        """Para o processamento de pedidos."""
        self.processando = False
        if self.thread_processamento.is_alive():
            self.thread_processamento.join()


# ============================================================================
# SISTEMA DE RECOMENDAÇÕES
# ============================================================================

class SistemaRecomendacoes:
    """
    Sistema de recomendações baseado em histórico de compras.
    """
    
    def __init__(self, servico_produtos: ServicoProdutos, servico_pedidos: ServicoPedidos):
        self.servico_produtos = servico_produtos
        self.servico_pedidos = servico_pedidos
        self.matriz_cliente_produto = defaultdict(lambda: defaultdict(int))
        self.similaridade_produtos = {}
        self._atualizar_matriz()
    
    def _atualizar_matriz(self):
        """Atualiza a matriz cliente-produto."""
        # Limpar matriz existente
        self.matriz_cliente_produto.clear()
        
        # Reconstruir matriz com base nos pedidos
        for pedido in self.servico_pedidos.pedidos_em_memoria.values():
            if pedido.status == StatusPedido.ENTREGUE:
                for item in pedido.itens:
                    self.matriz_cliente_produto[pedido.cliente_id][item.produto_id] += item.quantidade
    
    def _calcular_similaridade_produtos(self):
        """Calcula similaridade entre produtos usando correlação de Pearson."""
        produtos_ids = set()
        for cliente_produtos in self.matriz_cliente_produto.values():
            produtos_ids.update(cliente_produtos.keys())
        
        produtos_ids = list(produtos_ids)
        
        for i, produto1 in enumerate(produtos_ids):
            for produto2 in produtos_ids[i+1:]:
                similaridade = self._pearson_correlation(produto1, produto2)
                self.similaridade_produtos[(produto1, produto2)] = similaridade
                self.similaridade_produtos[(produto2, produto1)] = similaridade
    
    def _pearson_correlation(self, produto1: int, produto2: int) -> float:
        """Calcula correlação de Pearson entre dois produtos."""
        # Encontrar clientes que compraram ambos os produtos
        clientes_comuns = []
        
        for cliente_id, produtos in self.matriz_cliente_produto.items():
            if produto1 in produtos and produto2 in produtos:
                clientes_comuns.append(cliente_id)
        
        if len(clientes_comuns) < 2:
            return 0.0
        
        # Calcular correlação
        x_values = [self.matriz_cliente_produto[c][produto1] for c in clientes_comuns]
        y_values = [self.matriz_cliente_produto[c][produto2] for c in clientes_comuns]
        
        if len(set(x_values)) == 1 or len(set(y_values)) == 1:
            return 0.0
        
        try:
            # Calcular correlação de Pearson manualmente
            n = len(x_values)
            sum_x = sum(x_values)
            sum_y = sum(y_values)
            sum_x2 = sum(x * x for x in x_values)
            sum_y2 = sum(y * y for y in y_values)
            sum_xy = sum(x * y for x, y in zip(x_values, y_values))
            
            numerador = n * sum_xy - sum_x * sum_y
            denominador = math.sqrt((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y))
            
            if denominador == 0:
                return 0.0
            
            return numerador / denominador
        except:
            return 0.0
    
    def recomendar_produtos_colaborativo(self, cliente_id: int, num_recomendacoes: int = 5) -> List[Tuple[Produto, float]]:
        """
        Recomenda produtos usando filtragem colaborativa.
        """
        if cliente_id not in self.matriz_cliente_produto:
            # Cliente novo - recomendar produtos mais populares
            return self._recomendar_populares(num_recomendacoes)
        
        # Atualizar similaridades se necessário
        if not self.similaridade_produtos:
            self._calcular_similaridade_produtos()
        
        produtos_cliente = self.matriz_cliente_produto[cliente_id]
        recomendacoes = defaultdict(float)
        
        # Para cada produto que o cliente comprou
        for produto_id, quantidade in produtos_cliente.items():
            # Encontrar produtos similares
            for (p1, p2), similaridade in self.similaridade_produtos.items():
                if p1 == produto_id and p2 not in produtos_cliente and similaridade > 0.1:
                    recomendacoes[p2] += similaridade * quantidade
        
        # Ordenar recomendações por score
        recomendacoes_ordenadas = sorted(recomendacoes.items(), key=lambda x: x[1], reverse=True)
        
        # Converter para objetos Produto
        resultado = []
        for produto_id, score in recomendacoes_ordenadas[:num_recomendacoes]:
            produto = self.servico_produtos.buscar_por_id(produto_id)
            if produto and produto.ativo:
                resultado.append((produto, score))
        
        return resultado
    
    def recomendar_produtos_baseado_conteudo(self, cliente_id: int, num_recomendacoes: int = 5) -> List[Produto]:
        """
        Recomenda produtos baseado no conteúdo (categoria preferida).
        """
        if cliente_id not in self.matriz_cliente_produto:
            return self._recomendar_populares(num_recomendacoes)
        
        # Analisar preferências de categoria do cliente
        preferencias_categoria = defaultdict(int)
        produtos_cliente = self.matriz_cliente_produto[cliente_id]
        
        for produto_id, quantidade in produtos_cliente.items():
            produto = self.servico_produtos.buscar_por_id(produto_id)
            if produto:
                preferencias_categoria[produto.categoria] += quantidade
        
        # Encontrar categoria preferida
        if not preferencias_categoria:
            return self._recomendar_populares(num_recomendacoes)
        
        categoria_preferida = max(preferencias_categoria.items(), key=lambda x: x[1])[0]
        
        # Recomendar produtos da categoria preferida que o cliente não comprou
        produtos_categoria = self.servico_produtos.buscar_por_categoria(categoria_preferida)
        recomendacoes = []
        
        for produto in produtos_categoria:
            if produto.id not in produtos_cliente:
                recomendacoes.append(produto)
        
        # Ordenar por avaliação e popularidade
        recomendacoes.sort(key=lambda p: (p.avaliacao_media, p.total_vendido), reverse=True)
        
        return recomendacoes[:num_recomendacoes]
    
    def _recomendar_populares(self, num_recomendacoes: int) -> List[Tuple[Produto, float]]:
        """Recomenda produtos mais populares para clientes novos."""
        produtos_populares = self.servico_produtos.mais_vendidos(num_recomendacoes)
        return [(produto, 1.0) for produto in produtos_populares]
    
    def recomendar_hibrido(self, cliente_id: int, num_recomendacoes: int = 5) -> List[Tuple[Produto, float]]:
        """
        Sistema híbrido combinando filtragem colaborativa e baseada em conteúdo.
        """
        # Obter recomendações colaborativas
        rec_colaborativas = self.recomendar_produtos_colaborativo(cliente_id, num_recomendacoes * 2)
        
        # Obter recomendações baseadas em conteúdo
        rec_conteudo = self.recomendar_produtos_baseado_conteudo(cliente_id, num_recomendacoes * 2)
        
        # Combinar recomendações com pesos
        recomendacoes_finais = {}
        
        # Peso 0.7 para colaborativo
        for produto, score in rec_colaborativas:
            recomendacoes_finais[produto.id] = (produto, score * 0.7)
        
        # Peso 0.3 para conteúdo
        for produto in rec_conteudo:
            if produto.id in recomendacoes_finais:
                produto_atual, score_atual = recomendacoes_finais[produto.id]
                recomendacoes_finais[produto.id] = (produto_atual, score_atual + 0.3)
            else:
                recomendacoes_finais[produto.id] = (produto, 0.3)
        
        # Ordenar por score final
        resultado = sorted(recomendacoes_finais.values(), key=lambda x: x[1], reverse=True)
        
        return resultado[:num_recomendacoes]


# ============================================================================
# MOTOR DE BUSCA
# ============================================================================

class MotorBuscaProdutos:
    """
    Motor de busca para produtos com ranking TF-IDF.
    """
    
    def __init__(self, servico_produtos: ServicoProdutos):
        self.servico_produtos = servico_produtos
        self.indice_invertido = defaultdict(set)
        self.documentos = {}  # produto_id -> texto completo
        self.tf_idf = {}
        self._construir_indice()
    
    def _construir_indice(self):
        """Constrói o índice invertido dos produtos."""
        produtos = self.servico_produtos.listar_todos()
        
        for produto in produtos:
            # Criar documento de texto para o produto
            texto_produto = f"{produto.nome} {produto.descricao} {produto.categoria.value}"
            self.documentos[produto.id] = texto_produto.lower()
            
            # Tokenizar e adicionar ao índice
            tokens = self._tokenizar(texto_produto)
            for token in tokens:
                self.indice_invertido[token].add(produto.id)
        
        self._calcular_tf_idf()
    
    def _tokenizar(self, texto: str) -> List[str]:
        """Tokeniza o texto removendo pontuação e palavras vazias."""
        import re
        
        # Remover pontuação e converter para minúsculas
        texto_limpo = re.sub(r'[^\w\s]', ' ', texto.lower())
        tokens = texto_limpo.split()
        
        # Palavras vazias em português
        stop_words = {
            'a', 'o', 'e', 'de', 'do', 'da', 'em', 'um', 'uma', 'para', 'com', 'por',
            'na', 'no', 'ao', 'dos', 'das', 'se', 'que', 'como', 'mais', 'mas', 'ou'
        }
        
        # Filtrar palavras vazias e tokens muito curtos
        tokens_filtrados = [token for token in tokens if len(token) > 2 and token not in stop_words]
        
        return tokens_filtrados
    
    def _calcular_tf_idf(self):
        """Calcula TF-IDF para todos os termos e documentos."""
        total_documentos = len(self.documentos)
        
        for produto_id, texto in self.documentos.items():
            tokens = self._tokenizar(texto)
            tf_documento = Counter(tokens)
            total_tokens = len(tokens)
            
            self.tf_idf[produto_id] = {}
            
            for termo, freq in tf_documento.items():
                # Term Frequency
                tf = freq / total_tokens
                
                # Inverse Document Frequency
                df = len(self.indice_invertido[termo])
                idf = math.log(total_documentos / df) if df > 0 else 0
                
                # TF-IDF
                self.tf_idf[produto_id][termo] = tf * idf
    
    def buscar(self, consulta: str, limite: int = 10) -> List[Tuple[Produto, float]]:
        """
        Busca produtos usando TF-IDF.
        
        Args:
            consulta: Termo de busca
            limite: Número máximo de resultados
        
        Returns:
            Lista de tuplas (produto, score)
        """
        tokens_consulta = self._tokenizar(consulta)
        
        if not tokens_consulta:
            return []
        
        # Calcular score para cada produto
        scores = defaultdict(float)
        
        for token in tokens_consulta:
            if token in self.indice_invertido:
                for produto_id in self.indice_invertido[token]:
                    if produto_id in self.tf_idf and token in self.tf_idf[produto_id]:
                        scores[produto_id] += self.tf_idf[produto_id][token]
        
        # Ordenar por score
        resultados_ordenados = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Converter para objetos Produto
        resultados = []
        for produto_id, score in resultados_ordenados[:limite]:
            produto = self.servico_produtos.buscar_por_id(produto_id)
            if produto and produto.ativo:
                resultados.append((produto, score))
        
        return resultados
    
    def buscar_fuzzy(self, consulta: str, limite: int = 10) -> List[Tuple[Produto, float]]:
        """
        Busca fuzzy usando distância de Levenshtein.
        """
        def distancia_levenshtein(s1: str, s2: str) -> int:
            """Calcula distância de Levenshtein entre duas strings."""
            if len(s1) < len(s2):
                return distancia_levenshtein(s2, s1)
            
            if len(s2) == 0:
                return len(s1)
            
            linha_anterior = list(range(len(s2) + 1))
            for i, c1 in enumerate(s1):
                linha_atual = [i + 1]
                for j, c2 in enumerate(s2):
                    insercoes = linha_anterior[j + 1] + 1
                    delecoes = linha_atual[j] + 1
                    substituicoes = linha_anterior[j] + (c1 != c2)
                    linha_atual.append(min(insercoes, delecoes, substituicoes))
                linha_anterior = linha_atual
            
            return linha_anterior[-1]
        
        consulta_lower = consulta.lower()
        resultados_fuzzy = []
        
        produtos = self.servico_produtos.listar_todos()
        
        for produto in produtos:
            # Calcular similaridade com nome e descrição
            nome_lower = produto.nome.lower()
            desc_lower = produto.descricao.lower()
            
            # Distância com o nome
            dist_nome = distancia_levenshtein(consulta_lower, nome_lower)
            similaridade_nome = 1 - (dist_nome / max(len(consulta_lower), len(nome_lower)))
            
            # Verificar se consulta está contida na descrição
            similaridade_desc = 0.5 if consulta_lower in desc_lower else 0
            
            # Score final
            score_final = max(similaridade_nome, similaridade_desc)
            
            if score_final > 0.3:  # Threshold mínimo
                resultados_fuzzy.append((produto, score_final))
        
        # Ordenar por score
        resultados_fuzzy.sort(key=lambda x: x[1], reverse=True)
        
        return resultados_fuzzy[:limite]
    
    def sugerir_correcoes(self, consulta: str) -> List[str]:
        """Sugere correções para termos de busca."""
        tokens_consulta = self._tokenizar(consulta)
        sugestoes = []
        
        for token in tokens_consulta:
            if token not in self.indice_invertido:
                # Encontrar termos similares
                melhores_sugestoes = []
                
                for termo_indice in self.indice_invertido.keys():
                    if abs(len(token) - len(termo_indice)) <= 2:  # Filtro inicial
                        dist = self._distancia_levenshtein_simples(token, termo_indice)
                        if dist <= 2:  # Máximo 2 caracteres de diferença
                            melhores_sugestoes.append((termo_indice, dist))
                
                # Ordenar por distância
                melhores_sugestoes.sort(key=lambda x: x[1])
                
                if melhores_sugestoes:
                    sugestoes.append(melhores_sugestoes[0][0])
                else:
                    sugestoes.append(token)
            else:
                sugestoes.append(token)
        
        return sugestoes
    
    def _distancia_levenshtein_simples(self, s1: str, s2: str) -> int:
        """Versão simplificada da distância de Levenshtein."""
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        
        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2 + 1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        
        return distances[-1]
    
    def atualizar_indice(self):
        """Atualiza o índice com novos produtos."""
        self.indice_invertido.clear()
        self.documentos.clear()
        self.tf_idf.clear()
        self._construir_indice()


# ============================================================================
# ANÁLISE DE DADOS E RELATÓRIOS
# ============================================================================

class AnalisadorDados:
    """
    Analisador de dados para gerar insights de negócio.
    """
    
    def __init__(self, servico_clientes: ServicoClientes, servico_produtos: ServicoProdutos,
                 servico_pedidos: ServicoPedidos):
        self.servico_clientes = servico_clientes
        self.servico_produtos = servico_produtos
        self.servico_pedidos = servico_pedidos
    
    def analise_vendas_periodo(self, data_inicio: datetime, data_fim: datetime) -> Dict[str, Any]:
        """Análise de vendas em um período específico."""
        pedidos_periodo = []
        
        for pedido in self.servico_pedidos.pedidos_em_memoria.values():
            if (data_inicio <= pedido.data_pedido <= data_fim and 
                pedido.status != StatusPedido.CANCELADO):
                pedidos_periodo.append(pedido)
        
        if not pedidos_periodo:
            return {'erro': 'Nenhum pedido encontrado no período'}
        
        # Métricas básicas
        total_pedidos = len(pedidos_periodo)
        receita_total = sum(p.calcular_total() for p in pedidos_periodo)
        ticket_medio = receita_total / total_pedidos
        
        # Análise por dia
        vendas_por_dia = defaultdict(float)
        pedidos_por_dia = defaultdict(int)
        
        for pedido in pedidos_periodo:
            data_str = pedido.data_pedido.strftime('%Y-%m-%d')
            vendas_por_dia[data_str] += pedido.calcular_total()
            pedidos_por_dia[data_str] += 1
        
        # Produtos mais vendidos
        produtos_vendidos = defaultdict(int)
        for pedido in pedidos_periodo:
            for item in pedido.itens:
                produtos_vendidos[item.produto_id] += item.quantidade
        
        top_produtos = []
        for produto_id, quantidade in sorted(produtos_vendidos.items(), 
                                           key=lambda x: x[1], reverse=True)[:10]:
            produto = self.servico_produtos.buscar_por_id(produto_id)
            if produto:
                top_produtos.append({
                    'produto': produto.nome,
                    'quantidade': quantidade,
                    'receita': quantidade * produto.preco
                })
        
        return {
            'periodo': f"{data_inicio.strftime('%d/%m/%Y')} - {data_fim.strftime('%d/%m/%Y')}",
            'total_pedidos': total_pedidos,
            'receita_total': receita_total,
            'ticket_medio': ticket_medio,
            'vendas_por_dia': dict(vendas_por_dia),
            'pedidos_por_dia': dict(pedidos_por_dia),
            'top_produtos': top_produtos
        }
    
    def analise_clientes(self) -> Dict[str, Any]:
        """Análise detalhada dos clientes."""
        clientes = self.servico_clientes.listar_todos()
        
        if not clientes:
            return {'erro': 'Nenhum cliente encontrado'}
        
        # Segmentação por valor
        clientes_por_valor = {
            'alto_valor': [c for c in clientes if c.total_compras >= 10000],
            'medio_valor': [c for c in clientes if 1000 <= c.total_compras < 10000],
            'baixo_valor': [c for c in clientes if c.total_compras < 1000]
        }
        
        # Análise de retenção (clientes que fizeram mais de uma compra)
        clientes_retidos = [c for c in clientes if c.numero_pedidos > 1]
        taxa_retencao = (len(clientes_retidos) / len(clientes)) * 100
        
        # Distribuição geográfica
        distribuicao_estados = Counter(c.endereco.estado for c in clientes)
        distribuicao_cidades = Counter(c.endereco.cidade for c in clientes)
        
        # Clientes mais valiosos
        top_clientes = sorted(clientes, key=lambda c: c.total_compras, reverse=True)[:10]
        
        return {
            'total_clientes': len(clientes),
            'segmentacao_valor': {
                'alto_valor': len(clientes_por_valor['alto_valor']),
                'medio_valor': len(clientes_por_valor['medio_valor']),
                'baixo_valor': len(clientes_por_valor['baixo_valor'])
            },
            'taxa_retencao': taxa_retencao,
            'distribuicao_estados': dict(distribuicao_estados.most_common(10)),
            'distribuicao_cidades': dict(distribuicao_cidades.most_common(10)),
            'top_clientes': [
                {
                    'nome': c.nome,
                    'total_compras': c.total_compras,
                    'numero_pedidos': c.numero_pedidos,
                    'tipo': c.tipo.value
                } for c in top_clientes
            ]
        }
    
    def analise_produtos(self) -> Dict[str, Any]:
        """Análise detalhada dos produtos."""
        produtos = self.servico_produtos.listar_todos()
        
        if not produtos:
            return {'erro': 'Nenhum produto encontrado'}
        
        # Análise por categoria
        produtos_por_categoria = defaultdict(list)
        for produto in produtos:
            produtos_por_categoria[produto.categoria.value].append(produto)
        
        # Performance por categoria
        performance_categoria = {}
        for categoria, prods in produtos_por_categoria.items():
            receita_categoria = sum(p.preco * p.total_vendido for p in prods)
            performance_categoria[categoria] = {
                'total_produtos': len(prods),
                'receita_total': receita_categoria,
                'produtos_vendidos': sum(p.total_vendido for p in prods),
                'preco_medio': statistics.mean(p.preco for p in prods)
            }
        
        # Produtos em falta
        produtos_falta = self.servico_produtos.produtos_em_falta()
        
        # Produtos sem movimento
        produtos_sem_movimento = [p for p in produtos if p.total_vendido == 0]
        
        # Análise de preços
        precos = [p.preco for p in produtos]
        
        return {
            'total_produtos': len(produtos),
            'performance_categoria': performance_categoria,
            'produtos_em_falta': len(produtos_falta),
            'produtos_sem_movimento': len(produtos_sem_movimento),
            'analise_precos': {
                'preco_medio': statistics.mean(precos),
                'preco_mediano': statistics.median(precos),
                'preco_maximo': max(precos),
                'preco_minimo': min(precos)
            },
            'top_produtos_falta': [
                {
                    'nome': p.nome,
                    'estoque_atual': p.estoque,
                    'estoque_minimo': p.estoque_minimo
                } for p in produtos_falta[:10]
            ]
        }
    
    def gerar_relatorio_executivo(self) -> Dict[str, Any]:
        """Gera relatório executivo completo."""
        # Período dos últimos 30 dias
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=30)
        
        # Coletar todas as análises
        analise_vendas = self.analise_vendas_periodo(data_inicio, data_fim)
        analise_clientes = self.analise_clientes()
        analise_produtos = self.analise_produtos()
        
        # KPIs principais
        kpis = {
            'receita_mensal': analise_vendas.get('receita_total', 0),
            'pedidos_mensal': analise_vendas.get('total_pedidos', 0),
            'ticket_medio': analise_vendas.get('ticket_medio', 0),
            'total_clientes': analise_clientes.get('total_clientes', 0),
            'taxa_retencao': analise_clientes.get('taxa_retencao', 0),
            'produtos_ativos': analise_produtos.get('total_produtos', 0),
            'produtos_em_falta': analise_produtos.get('produtos_em_falta', 0)
        }
        
        # Insights e recomendações
        insights = []
        
        if kpis['taxa_retencao'] < 30:
            insights.append("Taxa de retenção baixa - implementar programa de fidelidade")
        
        if kpis['produtos_em_falta'] > 10:
            insights.append("Muitos produtos em falta - revisar política de estoque")
        
        if kpis['ticket_medio'] < 100:
            insights.append("Ticket médio baixo - implementar estratégias de upselling")
        
        return {
            'data_relatorio': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'periodo_analise': f"Últimos 30 dias ({data_inicio.strftime('%d/%m/%Y')} - {data_fim.strftime('%d/%m/%Y')})",
            'kpis_principais': kpis,
            'analise_vendas': analise_vendas,
            'analise_clientes': analise_clientes,
            'analise_produtos': analise_produtos,
            'insights_recomendacoes': insights
        }


# ============================================================================
# INTERFACE DO SISTEMA
# ============================================================================

class InterfaceSistema:
    """
    Interface de linha de comando para o sistema empresarial.
    """
    
    def __init__(self):
        self.bd = GerenciadorBancoDados()
        self.servico_clientes = ServicoClientes(self.bd)
        self.servico_produtos = ServicoProdutos(self.bd)
        self.servico_pedidos = ServicoPedidos(self.bd, self.servico_clientes, self.servico_produtos)
        self.sistema_recomendacoes = SistemaRecomendacoes(self.servico_produtos, self.servico_pedidos)
        self.motor_busca = MotorBuscaProdutos(self.servico_produtos)
        self.analisador = AnalisadorDados(self.servico_clientes, self.servico_produtos, self.servico_pedidos)
        
        # Carregar dados de exemplo se necessário
        self._verificar_dados_exemplo()
    
    def _verificar_dados_exemplo(self):
        """Verifica se há dados no sistema e carrega exemplos se necessário."""
        if not self.servico_clientes.listar_todos():
            print("Sistema vazio detectado. Carregando dados de exemplo...")
            self._carregar_dados_exemplo()
    
    def _carregar_dados_exemplo(self):
        """Carrega dados de exemplo para demonstração."""
        # Criar clientes de exemplo
        enderecos_exemplo = [
            Endereco("Rua das Flores", "123", "Centro", "São Paulo", "SP", "01234-567"),
            Endereco("Av. Paulista", "456", "Bela Vista", "São Paulo", "SP", "01310-100"),
            Endereco("Rua Oscar Freire", "789", "Jardins", "São Paulo", "SP", "01426-001"),
            Endereco("Rua Augusta", "321", "Consolação", "São Paulo", "SP", "01305-000"),
            Endereco("Av. Faria Lima", "654", "Itaim Bibi", "São Paulo", "SP", "04538-132")
        ]
        
        nomes_exemplo = [
            "João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa", "Carlos Ferreira"
        ]
        
        emails_exemplo = [
            "joao.silva@email.com", "maria.santos@email.com", "pedro.oliveira@email.com",
            "ana.costa@email.com", "carlos.ferreira@email.com"
        ]
        
        for i, (nome, email, endereco) in enumerate(zip(nomes_exemplo, emails_exemplo, enderecos_exemplo)):
            cliente = self.servico_clientes.criar_cliente(
                nome=nome,
                email=email,
                telefone=f"(11) 9999-{1000+i}",
                endereco=endereco
            )
        
        # Criar produtos de exemplo
        produtos_exemplo = [
            ("Smartphone Samsung Galaxy", "Smartphone Android com 128GB", CategoriasProduto.ELETRONICOS, 899.99, 50),
            ("iPhone 13", "iPhone com 256GB de armazenamento", CategoriasProduto.ELETRONICOS, 2499.99, 30),
            ("Notebook Dell", "Notebook para trabalho e estudos", CategoriasProduto.ELETRONICOS, 1899.99, 25),
            ("Camiseta Polo", "Camiseta polo masculina algodão", CategoriasProduto.ROUPAS, 79.99, 100),
            ("Jeans Feminino", "Calça jeans feminina skinny", CategoriasProduto.ROUPAS, 129.99, 80),
            ("Tênis Esportivo", "Tênis para corrida e caminhada", CategoriasProduto.ESPORTES, 199.99, 60),
            ("Livro Python", "Livro sobre programação Python", CategoriasProduto.LIVROS, 59.99, 40),
            ("Cafeteira Elétrica", "Cafeteira automática 12 xícaras", CategoriasProduto.CASA, 149.99, 35),
            ("Bicicleta Mountain Bike", "Bicicleta para trilhas", CategoriasProduto.ESPORTES, 899.99, 20),
            ("Chocolate Gourmet", "Chocolate belga premium", CategoriasProduto.ALIMENTACAO, 29.99, 200)
        ]
        
        for nome, desc, categoria, preco, estoque in produtos_exemplo:
            self.servico_produtos.criar_produto(
                nome=nome,
                descricao=desc,
                categoria=categoria,
                preco=preco,
                estoque=estoque
            )
        
        # Criar alguns pedidos de exemplo
        clientes = self.servico_clientes.listar_todos()
        produtos = self.servico_produtos.listar_todos()
        
        for i in range(5):
            cliente = random.choice(clientes)
            num_itens = random.randint(1, 3)
            itens_pedido = []
            
            for _ in range(num_itens):
                produto = random.choice(produtos)
                quantidade = random.randint(1, 3)
                itens_pedido.append((produto.id, quantidade))
            
            pedido = self.servico_pedidos.criar_pedido(
                cliente_id=cliente.id,
                itens=itens_pedido,
                observacoes=f"Pedido de exemplo {i+1}"
            )
        
        print("Dados de exemplo carregados com sucesso!")
    
    def executar(self):
        """Executa o loop principal da interface."""
        print("=" * 60)
        print("SISTEMA DE ANÁLISE EMPRESARIAL")
        print("Projeto Integrador - Curso de Lógica de Programação")
        print("=" * 60)
        
        while True:
            try:
                self._mostrar_menu_principal()
                opcao = input("\nEscolha uma opção: ").strip()
                
                if opcao == '0':
                    self._finalizar_sistema()
                    break
                elif opcao == '1':
                    self._menu_clientes()
                elif opcao == '2':
                    self._menu_produtos()
                elif opcao == '3':
                    self._menu_pedidos()
                elif opcao == '4':
                    self._menu_busca()
                elif opcao == '5':
                    self._menu_recomendacoes()
                elif opcao == '6':
                    self._menu_relatorios()
                elif opcao == '7':
                    self._menu_estatisticas()
                else:
                    print("Opção inválida! Tente novamente.")
                
                input("\nPressione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\nSistema interrompido pelo usuário.")
                self._finalizar_sistema()
                break
            except Exception as e:
                print(f"\nErro inesperado: {e}")
                logger.error(f"Erro na interface: {e}")
    
    def _mostrar_menu_principal(self):
        """Mostra o menu principal."""
        print("\n" + "=" * 60)
        print("MENU PRINCIPAL")
        print("=" * 60)
        print("1. Gerenciar Clientes")
        print("2. Gerenciar Produtos")
        print("3. Gerenciar Pedidos")
        print("4. Sistema de Busca")
        print("5. Sistema de Recomendações")
        print("6. Relatórios e Análises")
        print("7. Estatísticas do Sistema")
        print("0. Sair")
    
    def _menu_clientes(self):
        """Menu de gerenciamento de clientes."""
        while True:
            print("\n" + "-" * 40)
            print("GERENCIAMENTO DE CLIENTES")
            print("-" * 40)
            print("1. Listar todos os clientes")
            print("2. Buscar cliente por ID")
            print("3. Buscar cliente por email")
            print("4. Criar novo cliente")
            print("5. Estatísticas de clientes")
            print("0. Voltar ao menu principal")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '0':
                break
            elif opcao == '1':
                self._listar_clientes()
            elif opcao == '2':
                self._buscar_cliente_por_id()
            elif opcao == '3':
                self._buscar_cliente_por_email()
            elif opcao == '4':
                self._criar_cliente()
            elif opcao == '5':
                self._mostrar_estatisticas_clientes()
            else:
                print("Opção inválida!")
    
    def _listar_clientes(self):
        """Lista todos os clientes."""
        clientes = self.servico_clientes.listar_todos()
        
        if not clientes:
            print("Nenhum cliente encontrado.")
            return
        
        print(f"\n{'ID':<5} {'Nome':<25} {'Email':<30} {'Tipo':<10} {'Total Compras':<15}")
        print("-" * 85)
        
        for cliente in clientes:
            print(f"{cliente.id:<5} {cliente.nome:<25} {cliente.email:<30} "
                  f"{cliente.tipo.value:<10} R$ {cliente.total_compras:<12.2f}")
    
    def _buscar_cliente_por_id(self):
        """Busca cliente por ID."""
        try:
            cliente_id = int(input("Digite o ID do cliente: "))
            cliente = self.servico_clientes.buscar_por_id(cliente_id)
            
            if cliente:
                self._mostrar_detalhes_cliente(cliente)
            else:
                print("Cliente não encontrado.")
        except ValueError:
            print("ID inválido!")
    
    def _buscar_cliente_por_email(self):
        """Busca cliente por email."""
        email = input("Digite o email do cliente: ").strip()
        cliente = self.servico_clientes.buscar_por_email(email)
        
        if cliente:
            self._mostrar_detalhes_cliente(cliente)
        else:
            print("Cliente não encontrado.")
    
    def _mostrar_detalhes_cliente(self, cliente: Cliente):
        """Mostra detalhes completos de um cliente."""
        print(f"\n{'='*50}")
        print(f"DETALHES DO CLIENTE")
        print(f"{'='*50}")
        print(f"ID: {cliente.id}")
        print(f"Nome: {cliente.nome}")
        print(f"Email: {cliente.email}")
        print(f"Telefone: {cliente.telefone}")
        print(f"Endereço: {cliente.endereco}")
        print(f"Tipo: {cliente.tipo.value}")
        print(f"Data de Cadastro: {cliente.data_cadastro.strftime('%d/%m/%Y')}")
        print(f"Total de Compras: R$ {cliente.total_compras:.2f}")
        print(f"Número de Pedidos: {cliente.numero_pedidos}")
        print(f"Desconto Atual: {cliente.calcular_desconto()*100:.1f}%")
        print(f"Status: {'Ativo' if cliente.ativo else 'Inativo'}")
    
    def _criar_cliente(self):
        """Cria um novo cliente."""
        try:
            print("\n" + "-" * 30)
            print("CRIAR NOVO CLIENTE")
            print("-" * 30)
            
            nome = input("Nome: ").strip()
            email = input("Email: ").strip()
            telefone = input("Telefone: ").strip()
            
            print("\nEndereço:")
            rua = input("Rua: ").strip()
            numero = input("Número: ").strip()
            bairro = input("Bairro: ").strip()
            cidade = input("Cidade: ").strip()
            estado = input("Estado: ").strip()
            cep = input("CEP: ").strip()
            
            endereco = Endereco(rua, numero, bairro, cidade, estado, cep)
            
            cliente = self.servico_clientes.criar_cliente(nome, email, telefone, endereco)
            print(f"\nCliente criado com sucesso! ID: {cliente.id}")
            
        except ValueError as e:
            print(f"Erro ao criar cliente: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
    
    def _mostrar_estatisticas_clientes(self):
        """Mostra estatísticas dos clientes."""
        stats = self.servico_clientes.obter_estatisticas()
        
        print(f"\n{'='*50}")
        print("ESTATÍSTICAS DE CLIENTES")
        print(f"{'='*50}")
        print(f"Total de Clientes: {stats.get('total_clientes', 0)}")
        print(f"Clientes Ativos: {stats.get('clientes_ativos', 0)}")
        print(f"Clientes Inativos: {stats.get('clientes_inativos', 0)}")
        print(f"Taxa de Acerto do Cache: {stats.get('taxa_cache', 0):.1f}%")
        
        if 'distribuicao_tipo' in stats:
            print(f"\nDistribuição por Tipo:")
            for tipo, quantidade in stats['distribuicao_tipo'].items():
                print(f"  {tipo}: {quantidade}")
        
        if 'valor_medio_compras' in stats:
            print(f"\nEstatísticas de Compras:")
            print(f"  Valor Médio: R$ {stats['valor_medio_compras']:.2f}")
            print(f"  Valor Mediano: R$ {stats['valor_mediano_compras']:.2f}")
            print(f"  Maior Comprador: R$ {stats['maior_comprador']:.2f}")
            print(f"  Menor Comprador: R$ {stats['menor_comprador']:.2f}")
    
    def _finalizar_sistema(self):
        """Finaliza o sistema de forma segura."""
        print("\nFinalizando sistema...")
        
        # Parar processamento de pedidos
        self.servico_pedidos.parar_processamento()
        
        # Fechar conexão com banco
        self.bd.fechar_conexao()
        
        print("Sistema finalizado com sucesso!")
        print("Obrigado por usar o Sistema de Análise Empresarial!")


# ============================================================================
# FUNÇÃO PRINCIPAL E DEMONSTRAÇÕES
# ============================================================================

def demonstracao_completa():
    """
    Demonstração completa do sistema integrador.
    """
    print("=" * 80)
    print("DEMONSTRAÇÃO DO PROJETO INTEGRADOR")
    print("Sistema de Análise Empresarial Completo")
    print("=" * 80)
    
    # Inicializar sistema
    sistema = InterfaceSistema()
    
    print("\n1. DEMONSTRAÇÃO DE ESTRUTURAS DE DADOS")
    print("-" * 50)
    
    # Demonstrar Árvore AVL
    arvore = ArvoreAVL()
    print("Inserindo dados na Árvore AVL...")
    for i in [10, 5, 15, 3, 7, 12, 18]:
        arvore.inserir(i, f"Valor_{i}")
    
    print("Dados em ordem:", arvore.listar_em_ordem())
    print("Busca por chave 7:", arvore.buscar(7))
    
    # Demonstrar Cache LRU
    cache = CacheInteligente(capacidade=3)
    print("\nTestando Cache LRU...")
    cache.put("A", "Valor A")
    cache.put("B", "Valor B")
    cache.put("C", "Valor C")
    print("Cache após inserções:", cache.get("A"), cache.get("B"), cache.get("C"))
    
    cache.put("D", "Valor D")  # Deve remover A
    print("Após inserir D:", cache.get("A"), cache.get("D"))
    print(f"Taxa de acerto: {cache.taxa_acerto():.1f}%")
    
    # Demonstrar Fila de Prioridade
    fila = FilaPrioridade()
    print("\nTestando Fila de Prioridade...")
    fila.adicionar("Tarefa Normal", 5)
    fila.adicionar("Tarefa Urgente", 1)
    fila.adicionar("Tarefa Baixa", 10)
    
    print("Processando por prioridade:")
    while not fila.esta_vazia():
        print(f"  - {fila.remover()}")
    
    print("\n2. DEMONSTRAÇÃO DE SERVIÇOS")
    print("-" * 50)
    
    # Estatísticas dos serviços
    stats_clientes = sistema.servico_clientes.obter_estatisticas()
    stats_produtos = sistema.servico_produtos.obter_estatisticas()
    stats_pedidos = sistema.servico_pedidos.obter_estatisticas()
    
    print(f"Clientes cadastrados: {stats_clientes.get('total_clientes', 0)}")
    print(f"Produtos cadastrados: {stats_produtos.get('total_produtos', 0)}")
    print(f"Pedidos realizados: {stats_pedidos.get('total_pedidos', 0)}")
    
    print("\n3. DEMONSTRAÇÃO DE RECOMENDAÇÕES")
    print("-" * 50)
    
    # Testar recomendações para o primeiro cliente
    clientes = sistema.servico_clientes.listar_todos()
    if clientes:
        cliente = clientes[0]
        print(f"Recomendações para {cliente.nome}:")
        
        # Recomendações colaborativas
        rec_colab = sistema.sistema_recomendacoes.recomendar_produtos_colaborativo(cliente.id, 3)
        if rec_colab:
            print("  Filtragem Colaborativa:")
            for produto, score in rec_colab:
                print(f"    - {produto.nome} (Score: {score:.2f})")
        
        # Recomendações baseadas em conteúdo
        rec_conteudo = sistema.sistema_recomendacoes.recomendar_produtos_baseado_conteudo(cliente.id, 3)
        if rec_conteudo:
            print("  Baseado em Conteúdo:")
            for produto in rec_conteudo:
                print(f"    - {produto.nome}")
    
    print("\n4. DEMONSTRAÇÃO DE BUSCA")
    print("-" * 50)
    
    # Testar motor de busca
    resultados_busca = sistema.motor_busca.buscar("smartphone", 3)
    if resultados_busca:
        print("Resultados para 'smartphone':")
        for produto, score in resultados_busca:
            print(f"  - {produto.nome} (Score: {score:.3f})")
    
    # Busca fuzzy
    resultados_fuzzy = sistema.motor_busca.buscar_fuzzy("smartfone", 3)  # Erro proposital
    if resultados_fuzzy:
        print("\nBusca fuzzy para 'smartfone':")
        for produto, score in resultados_fuzzy:
            print(f"  - {produto.nome} (Similaridade: {score:.3f})")
    
    print("\n5. DEMONSTRAÇÃO DE ANÁLISES")
    print("-" * 50)
    
    # Gerar relatório executivo
    relatorio = sistema.analisador.gerar_relatorio_executivo()
    
    print("KPIs Principais:")
    kpis = relatorio.get('kpis_principais', {})
    print(f"  Receita Mensal: R$ {kpis.get('receita_mensal', 0):.2f}")
    print(f"  Pedidos Mensais: {kpis.get('pedidos_mensal', 0)}")
    print(f"  Ticket Médio: R$ {kpis.get('ticket_medio', 0):.2f}")
    print(f"  Taxa de Retenção: {kpis.get('taxa_retencao', 0):.1f}%")
    
    if relatorio.get('insights_recomendacoes'):
        print("\nInsights e Recomendações:")
        for insight in relatorio['insights_recomendacoes']:
            print(f"  • {insight}")
    
    print("\n6. DEMONSTRAÇÃO DE PERFORMANCE")
    print("-" * 50)
    
    # Benchmark de operações
    import time
    
    # Teste de inserção em árvore AVL
    arvore_teste = ArvoreAVL()
    inicio = time.time()
    for i in range(1000):
        arvore_teste.inserir(i, f"valor_{i}")
    tempo_arvore = time.time() - inicio
    print(f"Inserção de 1000 itens na Árvore AVL: {tempo_arvore:.4f}s")
    
    # Teste de cache
    cache_teste = CacheInteligente(100)
    inicio = time.time()
    for i in range(1000):
        cache_teste.put(f"chave_{i}", f"valor_{i}")
    tempo_cache = time.time() - inicio
    print(f"Inserção de 1000 itens no Cache: {tempo_cache:.4f}s")
    
    # Teste de busca
    inicio = time.time()
    for _ in range(100):
        sistema.motor_busca.buscar("produto", 5)
    tempo_busca = time.time() - inicio
    print(f"100 buscas no motor de busca: {tempo_busca:.4f}s")
    
    print("\n" + "=" * 80)
    print("DEMONSTRAÇÃO CONCLUÍDA")
    print("=" * 80)
    print("\nO sistema demonstrou com sucesso:")
    print("✓ Estruturas de dados avançadas (Árvore AVL, Cache LRU, Fila de Prioridade)")
    print("✓ Algoritmos de busca e ordenação")
    print("✓ Sistema de recomendações (colaborativo e baseado em conteúdo)")
    print("✓ Motor de busca com TF-IDF e busca fuzzy")
    print("✓ Análise de dados e geração de relatórios")
    print("✓ Persistência em banco de dados SQLite")
    print("✓ Programação orientada a objetos")
    print("✓ Tratamento de exceções")
    print("✓ Threading para processamento assíncrono")
    print("✓ Análise de performance e otimização")
    
    # Finalizar sistema
    sistema._finalizar_sistema()


def main():
    """
    Função principal do sistema.
    """
    print("Sistema de Análise Empresarial")
    print("Escolha o modo de execução:")
    print("1. Interface Interativa")
    print("2. Demonstração Completa")
    print("3. Sair")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    if opcao == '1':
        sistema = InterfaceSistema()
        sistema.executar()
    elif opcao == '2':
        demonstracao_completa()
    elif opcao == '3':
        print("Saindo...")
    else:
        print("Opção inválida!")


if __name__ == "__main__":
    main()


"""
============================================================================
CONCLUSÃO DO PROJETO INTEGRADOR
============================================================================

Este projeto integrador representa a culminação de todo o aprendizado do curso
de Lógica de Programação e Estruturas de Dados em Python. Ele demonstra a
aplicação prática de todos os conceitos estudados em um sistema empresarial
completo e funcional.

CONCEITOS INTEGRADOS:
====================

1. ESTRUTURAS DE DADOS FUNDAMENTAIS:
   - Listas, Dicionários, Conjuntos e Tuplas
   - Aplicação em armazenamento e manipulação de dados empresariais
   - Uso eficiente para diferentes tipos de operações

2. ESTRUTURAS DE DADOS AVANÇADAS:
   - Árvore AVL para indexação rápida de clientes e produtos
   - Cache LRU para otimização de consultas frequentes
   - Fila de Prioridade para processamento de pedidos
   - Índice Invertido para sistema de busca

3. ALGORITMOS DE ORDENAÇÃO E BUSCA:
   - Implementação de busca binária em estruturas ordenadas
   - Algoritmos de ordenação para ranking de produtos
   - Busca fuzzy com distância de Levenshtein
   - TF-IDF para relevância em buscas textuais

4. PROGRAMAÇÃO ORIENTADA A OBJETOS:
   - Classes bem estruturadas com responsabilidades claras
   - Herança e polimorfismo em sistemas de recomendação
   - Encapsulamento de dados e métodos
   - Padrões de design como Strategy e Factory

5. TRATAMENTO DE EXCEÇÕES:
   - Validação robusta de dados de entrada
   - Recuperação graceful de erros de sistema
   - Logging estruturado para debugging
   - Transações seguras em operações críticas

6. ANÁLISE DE COMPLEXIDADE:
   - Otimização de algoritmos para O(log n) quando possível
   - Uso de estruturas apropriadas para cada tipo de operação
   - Análise de trade-offs entre tempo e espaço
   - Profiling e medição de performance

7. PERSISTÊNCIA DE DADOS:
   - Banco de dados SQLite para armazenamento permanente
   - Índices otimizados para consultas frequentes
   - Transações ACID para consistência
   - Cache em memória para performance

8. SISTEMAS INTELIGENTES:
   - Algoritmos de recomendação colaborativa
   - Filtragem baseada em conteúdo
   - Sistema híbrido combinando múltiplas abordagens
   - Motor de busca com ranking inteligente

9. ANÁLISE DE DADOS:
   - Estatísticas descritivas e inferenciais
   - Geração de insights de negócio
   - Relatórios executivos automatizados
   - Visualização de tendências e padrões

10. PROGRAMAÇÃO CONCORRENTE:
    - Threading para processamento assíncrono de pedidos
    - Sincronização segura de recursos compartilhados
    - Processamento em background sem bloquear interface
    - Gerenciamento de estado thread-safe

ARQUITETURA DO SISTEMA:
======================

O sistema foi projetado seguindo princípios de arquitetura limpa:

- CAMADA DE DADOS: Modelos de domínio e persistência
- CAMADA DE SERVIÇOS: Lógica de negócio e regras
- CAMADA DE APLICAÇÃO: Casos de uso e orquestração
- CAMADA DE INTERFACE: Interação com usuário

FUNCIONALIDADES IMPLEMENTADAS:
=============================

1. Gestão completa de clientes com segmentação automática
2. Catálogo de produtos com controle de estoque
3. Sistema de pedidos com processamento assíncrono
4. Recomendações personalizadas usando múltiplos algoritmos
5. Motor de busca inteligente com correção automática
6. Análises avançadas com geração de insights
7. Relatórios executivos automatizados
8. Interface de linha de comando intuitiva

TÉCNICAS DE OTIMIZAÇÃO:
======================

1. Cache LRU para consultas frequentes
2. Índices em memória para busca rápida
3. Estruturas de dados apropriadas para cada operação
4. Lazy loading de dados pesados
5. Batch processing para operações em lote
6. Connection pooling para banco de dados
7. Algoritmos otimizados com complexidade adequada

BOAS PRÁTICAS APLICADAS:
=======================

1. Código limpo e bem documentado
2. Separação clara de responsabilidades
3. Tratamento robusto de erros
4. Logging estruturado para debugging
5. Testes implícitos através de demonstrações
6. Configuração flexível e extensível
7. Padrões de design reconhecidos

PRÓXIMOS PASSOS:
===============

Este projeto pode ser estendido com:

1. Interface web usando Flask/Django
2. API REST para integração externa
3. Machine Learning para previsões avançadas
4. Processamento de big data com pandas/numpy
5. Visualizações interativas com matplotlib/plotly
6. Deploy em cloud (AWS, Azure, GCP)
7. Containerização com Docker
8. Testes automatizados com pytest
9. CI/CD pipeline
10. Monitoramento e alertas

APRENDIZADOS CONSOLIDADOS:
=========================

Este projeto demonstra que o aluno agora possui:

✓ Domínio completo de estruturas de dados fundamentais e avançadas
✓ Capacidade de escolher algoritmos apropriados para cada problema
✓ Habilidade de projetar sistemas complexos e escaláveis
✓ Conhecimento de otimização e análise de performance
✓ Experiência com persistência e gerenciamento de dados
✓ Competência em programação orientada a objetos
✓ Capacidade de implementar sistemas inteligentes
✓ Habilidade de análise de dados e geração de insights
✓ Experiência com programação concorrente
✓ Conhecimento de boas práticas de desenvolvimento

O curso de Lógica de Programação e Estruturas de Dados está COMPLETO!

Parabéns por chegar até aqui e construir um sistema tão robusto e completo!
"""