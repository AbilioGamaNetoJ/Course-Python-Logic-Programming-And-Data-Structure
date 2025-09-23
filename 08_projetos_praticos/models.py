"""
Módulo de Modelos de Dados - Sistema de Gestão Empresarial

Este módulo contém todas as classes de dados, enums e tipos utilizados
no sistema de gestão empresarial. Mantém a separação clara entre
estruturas de dados e lógica de negócio.

Classes principais:
- Cliente: Representa clientes do sistema
- Produto: Representa produtos do catálogo
- Pedido: Representa pedidos de compra
- ItemPedido: Representa itens individuais de um pedido
- Endereco: Representa endereços
- LogAuditoria: Representa logs de auditoria

Enums:
- StatusPedido: Status possíveis para pedidos
- TipoCliente: Tipos de cliente
- CategoriaProduct: Categorias de produtos
- TipoOperacao: Tipos de operação para auditoria
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum, auto

# Importar configurações
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


# ================================
# ENUMS E TIPOS DE DADOS
# ================================

class StatusPedido(Enum):
    """Status possíveis para pedidos."""
    PENDENTE = "Pendente"
    PROCESSANDO = "Processando"
    ENVIADO = "Enviado"
    ENTREGUE = "Entregue"
    CANCELADO = "Cancelado"


class TipoCliente(Enum):
    """Tipos de cliente."""
    PESSOA_FISICA = "Pessoa Física"
    PESSOA_JURIDICA = "Pessoa Jurídica"
    VIP = "VIP"
    CORPORATIVO = "Corporativo"


class CategoriaProduct(Enum):
    """Categorias de produtos."""
    ELETRONICOS = "Eletrônicos"
    ROUPAS = "Roupas"
    LIVROS = "Livros"
    CASA = "Casa e Jardim"
    ESPORTES = "Esportes"
    ALIMENTACAO = "Alimentação"


class TipoOperacao(Enum):
    """Tipos de operação para auditoria."""
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()


# ================================
# CLASSES DE DADOS
# ================================

@dataclass
class Endereco:
    """
    Representa um endereço completo.
    
    Attributes:
        rua: Nome da rua
        numero: Número do endereço
        complemento: Complemento (opcional)
        bairro: Nome do bairro
        cidade: Nome da cidade
        estado: Estado/UF
        cep: Código postal
    """
    rua: str
    numero: str
    complemento: str = ""
    bairro: str = ""
    cidade: str = ""
    estado: str = ""
    cep: str = ""
    
    def __str__(self) -> str:
        """Representação string do endereço."""
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"
    
    def endereco_completo(self) -> str:
        """Retorna o endereço completo formatado."""
        partes = [
            f"{self.rua}, {self.numero}",
            self.complemento,
            self.bairro,
            f"{self.cidade}/{self.estado}",
            f"CEP: {self.cep}" if self.cep else ""
        ]
        return " - ".join(filter(None, partes))


@dataclass
class Cliente:
    """
    Representa um cliente do sistema.
    
    Attributes:
        id: Identificador único do cliente
        nome: Nome completo do cliente
        email: Email do cliente
        telefone: Telefone de contato
        tipo: Tipo do cliente (enum TipoCliente)
        endereco: Endereço do cliente
        data_cadastro: Data de cadastro no sistema
        ativo: Status ativo/inativo
        limite_credito: Limite de crédito disponível
        total_compras: Total histórico de compras
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    nome: str = ""
    email: str = ""
    telefone: str = ""
    tipo: TipoCliente = TipoCliente.PESSOA_FISICA
    endereco: Optional[Endereco] = None
    data_cadastro: datetime = field(default_factory=datetime.now)
    ativo: bool = True
    limite_credito: float = field(default_factory=lambda: config.business.default_credit_limit)
    total_compras: float = 0.0
    
    def __post_init__(self):
        """Inicialização pós-criação do objeto."""
        if not self.endereco:
            self.endereco = Endereco("", "")
    
    @property
    def credito_disponivel(self) -> float:
        """Calcula o crédito disponível do cliente."""
        return max(0, self.limite_credito - self.total_compras)
    
    @property
    def is_vip(self) -> bool:
        """Verifica se o cliente é VIP."""
        return self.tipo in [TipoCliente.VIP, TipoCliente.CORPORATIVO]


@dataclass
class Produto:
    """
    Representa um produto do catálogo.
    
    Attributes:
        id: Identificador único do produto
        nome: Nome do produto
        descricao: Descrição detalhada
        categoria: Categoria do produto (enum CategoriaProduct)
        preco: Preço unitário
        estoque: Quantidade em estoque
        estoque_minimo: Estoque mínimo para reposição
        fornecedor: Nome do fornecedor
        data_cadastro: Data de cadastro no sistema
        ativo: Status ativo/inativo
        peso: Peso do produto (kg)
        dimensoes: Dimensões do produto
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    nome: str = ""
    descricao: str = ""
    categoria: CategoriaProduct = CategoriaProduct.ELETRONICOS
    preco: float = 0.0
    estoque: int = 0
    estoque_minimo: int = field(default_factory=lambda: config.business.min_stock_level)
    fornecedor: str = ""
    data_cadastro: datetime = field(default_factory=datetime.now)
    ativo: bool = True
    peso: float = 0.0
    dimensoes: str = ""
    
    @property
    def precisa_reposicao(self) -> bool:
        """Verifica se o produto precisa de reposição."""
        return self.estoque <= self.estoque_minimo
    
    @property
    def valor_estoque(self) -> float:
        """Calcula o valor total do estoque."""
        return self.preco * self.estoque
    
    @property
    def disponivel(self) -> bool:
        """Verifica se o produto está disponível para venda."""
        return self.ativo and self.estoque > 0
    
    def pode_vender(self, quantidade: int) -> bool:
        """Verifica se é possível vender a quantidade solicitada."""
        return self.disponivel and self.estoque >= quantidade


@dataclass
class ItemPedido:
    """
    Representa um item individual de um pedido.
    
    Attributes:
        produto_id: ID do produto
        quantidade: Quantidade solicitada
        preco_unitario: Preço unitário no momento do pedido
        desconto: Desconto aplicado (0.0 a 1.0)
    """
    produto_id: str
    quantidade: int
    preco_unitario: float
    desconto: float = 0.0
    
    @property
    def subtotal(self) -> float:
        """Calcula o subtotal do item com desconto."""
        return (self.preco_unitario * self.quantidade) * (1 - self.desconto)
    
    @property
    def valor_desconto(self) -> float:
        """Calcula o valor total do desconto."""
        return (self.preco_unitario * self.quantidade) * self.desconto
    
    def aplicar_desconto(self, percentual: float) -> None:
        """Aplica um desconto percentual ao item."""
        self.desconto = max(0.0, min(1.0, percentual))


@dataclass
class Pedido:
    """
    Representa um pedido de compra.
    
    Attributes:
        id: Identificador único do pedido
        cliente_id: ID do cliente que fez o pedido
        itens: Lista de itens do pedido
        status: Status atual do pedido
        data_pedido: Data de criação do pedido
        data_entrega: Data prevista/realizada de entrega
        endereco_entrega: Endereço para entrega
        observacoes: Observações adicionais
        desconto_total: Desconto aplicado ao pedido total
        frete: Valor do frete
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    cliente_id: str = ""
    itens: List[ItemPedido] = field(default_factory=list)
    status: StatusPedido = StatusPedido.PENDENTE
    data_pedido: datetime = field(default_factory=datetime.now)
    data_entrega: Optional[datetime] = None
    endereco_entrega: Optional[Endereco] = None
    observacoes: str = ""
    desconto_total: float = 0.0
    frete: float = 0.0
    
    @property
    def subtotal(self) -> float:
        """Calcula o subtotal dos itens."""
        return sum(item.subtotal for item in self.itens)
    
    @property
    def total(self) -> float:
        """Calcula o total do pedido."""
        return (self.subtotal - self.desconto_total) + self.frete
    
    @property
    def quantidade_itens(self) -> int:
        """Retorna a quantidade total de itens."""
        return sum(item.quantidade for item in self.itens)
    
    @property
    def pode_cancelar(self) -> bool:
        """Verifica se o pedido pode ser cancelado."""
        return self.status in [StatusPedido.PENDENTE, StatusPedido.PROCESSANDO]
    
    def adicionar_item(self, item: ItemPedido) -> None:
        """Adiciona um item ao pedido."""
        self.itens.append(item)
    
    def remover_item(self, produto_id: str) -> bool:
        """Remove um item do pedido pelo ID do produto."""
        for i, item in enumerate(self.itens):
            if item.produto_id == produto_id:
                del self.itens[i]
                return True
        return False
    
    def aplicar_desconto_total(self, valor: float) -> None:
        """Aplica um desconto ao total do pedido."""
        self.desconto_total = max(0.0, valor)


@dataclass
class LogAuditoria:
    """
    Representa um log de auditoria para rastreamento de operações.
    
    Attributes:
        id: Identificador único do log
        timestamp: Data e hora da operação
        tipo_operacao: Tipo de operação realizada
        entidade: Nome da entidade afetada
        entidade_id: ID da entidade afetada
        usuario: Usuário que realizou a operação
        detalhes: Detalhes adicionais da operação
        ip_origem: IP de origem da operação
        user_agent: User agent da operação
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    tipo_operacao: TipoOperacao = TipoOperacao.READ
    entidade: str = ""
    entidade_id: str = ""
    usuario: str = "sistema"
    detalhes: Dict[str, Any] = field(default_factory=dict)
    ip_origem: str = "127.0.0.1"
    user_agent: str = "Sistema Interno"
    
    def __str__(self) -> str:
        """Representação string do log."""
        return f"{self.timestamp} - {self.usuario} - {self.tipo_operacao.value} - {self.entidade}:{self.entidade_id}"
    
    def adicionar_detalhe(self, chave: str, valor: Any) -> None:
        """Adiciona um detalhe ao log."""
        self.detalhes[chave] = valor