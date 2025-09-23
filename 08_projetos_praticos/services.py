"""
Módulo de Serviços de Negócio
============================

Este módulo contém as implementações dos serviços que encapsulam a lógica de negócio
do sistema de gestão empresarial.

Padrões de Design:
- Service Layer: Encapsula lógica de negócio complexa
- Dependency Injection: Serviços recebem dependências via construtor
- Single Responsibility: Cada serviço tem uma responsabilidade específica

Estruturas de Dados Utilizadas:
- List: Para coleções de entidades retornadas pelos serviços
- Tuple: Para retornos múltiplos (sucesso, dados, erros)
- Dict: Para filtros e dados de entrada
- Optional: Para valores que podem ser None

Algoritmos Implementados:
- Busca linear: Para filtros por nome (busca parcial)
- Ordenação: Para listas de clientes VIP e produtos
- Validação em cascata: Verificações sequenciais com parada antecipada
"""

from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import sys
import os

# Adicionar o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Cliente, Produto, Pedido, ItemPedido, StatusPedido, TipoCliente, CategoriaProduct
from repositories import RepositorioBase, ValidadorBase


# ================================
# SERVIÇOS DE NEGÓCIO
# ================================

class ServicoCliente:
    """
    Serviço para gerenciar clientes.
    
    Responsabilidades:
    - Validação de dados de cliente
    - Verificação de unicidade de email
    - Operações CRUD com regras de negócio
    - Buscas especializadas (por nome, clientes VIP)
    
    Complexidade das operações:
    - Criar: O(1) + validação
    - Buscar por ID: O(1)
    - Buscar por nome: O(n) - busca linear
    - Listar com filtros: O(k) onde k é o número de resultados
    """
    
    def __init__(self, repositorio: RepositorioBase, validador: ValidadorBase):
        """
        Inicializa o serviço com suas dependências.
        
        Args:
            repositorio: Implementação do repositório para persistência
            validador: Implementação do validador para regras de negócio
        """
        self.repositorio = repositorio
        self.validador = validador
    
    def criar_cliente(self, dados: Dict[str, Any]) -> Tuple[bool, str, List[str]]:
        """
        Cria um novo cliente.
        
        Processo:
        1. Valida dados de entrada
        2. Verifica unicidade do email
        3. Cria entidade Cliente
        4. Persiste no repositório
        
        Args:
            dados: Dicionário com dados do cliente
            
        Returns:
            Tuple[bool, str, List[str]]: (sucesso, id_cliente, lista_erros)
        """
        # Validação de dados
        valido, erros = self.validador.validar(dados)
        if not valido:
            return False, "", erros
        
        # Verificar email único (regra de negócio)
        if dados.get('email'):
            clientes_existentes = self.repositorio.buscar_por_campo('email', dados['email'])
            if clientes_existentes:
                return False, "", ["Email já cadastrado"]
        
        # Criar e persistir cliente
        cliente = Cliente(**dados)
        id_cliente = self.repositorio.criar(cliente)
        return True, id_cliente, []
    
    def buscar_cliente(self, id: str) -> Optional[Cliente]:
        """
        Busca um cliente por ID.
        
        Complexidade: O(1) - acesso direto por chave
        """
        return self.repositorio.buscar(id)
    
    def listar_clientes(self, filtros: Dict[str, Any] = None) -> List[Cliente]:
        """
        Lista clientes com filtros opcionais.
        
        Complexidade: Depende dos filtros e índices disponíveis
        """
        return self.repositorio.listar(filtros)
    
    def atualizar_cliente(self, id: str, dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Atualiza um cliente existente.
        
        Processo:
        1. Valida novos dados
        2. Atualiza no repositório
        3. Retorna resultado da operação
        """
        valido, erros = self.validador.validar(dados)
        if not valido:
            return False, erros
        
        sucesso = self.repositorio.atualizar(id, dados)
        if not sucesso:
            return False, ["Cliente não encontrado"]
        
        return True, []
    
    def deletar_cliente(self, id: str) -> bool:
        """
        Deleta um cliente.
        
        Complexidade: O(k) onde k é o número de campos indexados
        """
        return self.repositorio.deletar(id)
    
    def buscar_por_nome(self, nome: str) -> List[Cliente]:
        """
        Busca clientes por nome (busca parcial).
        
        Implementa busca linear com comparação case-insensitive.
        Complexidade: O(n) onde n é o número total de clientes
        """
        todos_clientes = self.repositorio.listar()
        return [
            cliente for cliente in todos_clientes
            if nome.lower() in cliente.nome.lower()
        ]
    
    def clientes_vip(self) -> List[Cliente]:
        """
        Retorna clientes VIP ordenados por total de compras.
        
        Processo:
        1. Busca clientes VIP usando índice - O(k)
        2. Ordena por total de compras - O(k log k)
        
        Complexidade total: O(k log k) onde k é o número de clientes VIP
        """
        clientes = self.repositorio.buscar_por_campo('tipo', TipoCliente.VIP)
        return sorted(clientes, key=lambda c: c.total_compras, reverse=True)


class ServicoProduto:
    """
    Serviço para gerenciar produtos.
    
    Responsabilidades:
    - Validação de dados de produto
    - Controle de estoque
    - Operações CRUD com regras de negócio
    - Identificação de produtos com baixo estoque
    - Buscas por categoria e nome
    """
    
    def __init__(self, repositorio: RepositorioBase, validador: ValidadorBase):
        """Inicializa o serviço com suas dependências."""
        self.repositorio = repositorio
        self.validador = validador
    
    def criar_produto(self, dados: Dict[str, Any]) -> Tuple[bool, str, List[str]]:
        """
        Cria um novo produto.
        
        Similar ao criar_cliente, mas sem verificação de unicidade.
        """
        valido, erros = self.validador.validar(dados)
        if not valido:
            return False, "", erros
        
        produto = Produto(**dados)
        id_produto = self.repositorio.criar(produto)
        return True, id_produto, []
    
    def buscar_produto(self, id: str) -> Optional[Produto]:
        """Busca um produto por ID."""
        return self.repositorio.buscar(id)
    
    def listar_produtos(self, filtros: Dict[str, Any] = None) -> List[Produto]:
        """Lista produtos com filtros opcionais."""
        return self.repositorio.listar(filtros)
    
    def atualizar_produto(self, id: str, dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Atualiza um produto existente."""
        valido, erros = self.validador.validar(dados)
        if not valido:
            return False, erros
        
        sucesso = self.repositorio.atualizar(id, dados)
        if not sucesso:
            return False, ["Produto não encontrado"]
        
        return True, []
    
    def deletar_produto(self, id: str) -> bool:
        """Deleta um produto."""
        return self.repositorio.deletar(id)
    
    def produtos_baixo_estoque(self) -> List[Produto]:
        """
        Retorna produtos com estoque baixo.
        
        Utiliza a propriedade calculada `precisa_reposicao` do modelo Produto.
        Complexidade: O(n) onde n é o número total de produtos
        """
        todos_produtos = self.repositorio.listar()
        return [p for p in todos_produtos if p.precisa_reposicao]
    
    def produtos_por_categoria(self, categoria: CategoriaProduct) -> List[Produto]:
        """
        Retorna produtos de uma categoria.
        
        Utiliza índice automático por categoria.
        Complexidade: O(k) onde k é o número de produtos na categoria
        """
        return self.repositorio.buscar_por_campo('categoria', categoria)
    
    def buscar_por_nome(self, nome: str) -> List[Produto]:
        """
        Busca produtos por nome (busca parcial).
        
        Implementação similar à busca de clientes por nome.
        """
        todos_produtos = self.repositorio.listar()
        return [
            produto for produto in todos_produtos
            if nome.lower() in produto.nome.lower()
        ]
    
    def atualizar_estoque(self, id: str, quantidade: int) -> bool:
        """
        Atualiza o estoque de um produto.
        
        Regras de negócio:
        - Não permite estoque negativo
        - Atualiza atomicamente
        
        Args:
            id: ID do produto
            quantidade: Quantidade a ser adicionada (pode ser negativa)
            
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        produto = self.repositorio.buscar(id)
        if not produto:
            return False
        
        novo_estoque = produto.estoque + quantidade
        if novo_estoque < 0:
            return False  # Não permite estoque negativo
        
        return self.repositorio.atualizar(id, {'estoque': novo_estoque})


class ServicoPedido:
    """
    Serviço para gerenciar pedidos.
    
    Responsabilidades:
    - Validação de pedidos complexos
    - Verificação de existência de cliente e produtos
    - Controle de estoque durante criação/cancelamento
    - Cálculos de totais e descontos
    - Gestão de status de pedidos
    
    Este é o serviço mais complexo, pois coordena múltiplas entidades.
    """
    
    def __init__(self, repositorio: RepositorioBase, validador: ValidadorBase,
                 servico_cliente: ServicoCliente, servico_produto: ServicoProduto):
        """
        Inicializa o serviço com suas dependências.
        
        Note que este serviço depende de outros serviços (Dependency Injection).
        """
        self.repositorio = repositorio
        self.validador = validador
        self.servico_cliente = servico_cliente
        self.servico_produto = servico_produto
    
    def criar_pedido(self, dados: Dict[str, Any]) -> Tuple[bool, str, List[str]]:
        """
        Cria um novo pedido.
        
        Processo complexo:
        1. Valida dados básicos do pedido
        2. Verifica existência do cliente
        3. Para cada item:
           - Verifica existência do produto
           - Verifica disponibilidade de estoque
           - Cria ItemPedido
        4. Cria o pedido
        5. Reserva estoque para todos os itens
        6. Persiste o pedido
        
        Esta operação é transacional na lógica (all-or-nothing).
        """
        # Validação básica
        valido, erros = self.validador.validar(dados)
        if not valido:
            return False, "", erros
        
        # Verificar se cliente existe
        cliente = self.servico_cliente.buscar_cliente(dados['cliente_id'])
        if not cliente:
            return False, "", ["Cliente não encontrado"]
        
        # Verificar produtos e estoque
        itens_pedido = []
        for item_dados in dados['itens']:
            produto = self.servico_produto.buscar_produto(item_dados['produto_id'])
            if not produto:
                return False, "", [f"Produto {item_dados['produto_id']} não encontrado"]
            
            if produto.estoque < item_dados['quantidade']:
                return False, "", [f"Estoque insuficiente para {produto.nome}"]
            
            # Criar item do pedido
            item = ItemPedido(
                produto_id=item_dados['produto_id'],
                quantidade=item_dados['quantidade'],
                preco_unitario=item_dados.get('preco_unitario', produto.preco),
                desconto=item_dados.get('desconto', 0.0)
            )
            itens_pedido.append(item)
        
        # Criar pedido
        pedido_dados = dados.copy()
        pedido_dados['itens'] = itens_pedido
        pedido = Pedido(**pedido_dados)
        
        # Reservar estoque (operação crítica)
        for item in itens_pedido:
            self.servico_produto.atualizar_estoque(item.produto_id, -item.quantidade)
        
        id_pedido = self.repositorio.criar(pedido)
        return True, id_pedido, []
    
    def buscar_pedido(self, id: str) -> Optional[Pedido]:
        """Busca um pedido por ID."""
        return self.repositorio.buscar(id)
    
    def listar_pedidos(self, filtros: Dict[str, Any] = None) -> List[Pedido]:
        """Lista pedidos com filtros opcionais."""
        return self.repositorio.listar(filtros)
    
    def atualizar_status(self, id: str, novo_status: StatusPedido) -> bool:
        """
        Atualiza o status de um pedido.
        
        Operação simples que pode ser expandida para incluir
        validações de transição de status.
        """
        return self.repositorio.atualizar(id, {'status': novo_status})
    
    def cancelar_pedido(self, id: str) -> bool:
        """
        Cancela um pedido e restaura o estoque.
        
        Processo:
        1. Busca o pedido
        2. Verifica se pode ser cancelado
        3. Restaura estoque de todos os itens
        4. Atualiza status para CANCELADO
        
        Esta é uma operação compensatória (rollback).
        """
        pedido = self.repositorio.buscar(id)
        if not pedido or pedido.status == StatusPedido.CANCELADO:
            return False
        
        # Restaurar estoque
        for item in pedido.itens:
            self.servico_produto.atualizar_estoque(item.produto_id, item.quantidade)
        
        return self.atualizar_status(id, StatusPedido.CANCELADO)
    
    def pedidos_por_cliente(self, cliente_id: str) -> List[Pedido]:
        """
        Retorna pedidos de um cliente.
        
        Utiliza índice automático por cliente_id.
        """
        return self.repositorio.buscar_por_campo('cliente_id', cliente_id)
    
    def pedidos_por_status(self, status: StatusPedido) -> List[Pedido]:
        """
        Retorna pedidos por status.
        
        Utiliza índice automático por status.
        """
        return self.repositorio.buscar_por_campo('status', status)
    
    def pedidos_periodo(self, data_inicio: datetime, data_fim: datetime) -> List[Pedido]:
        """
        Retorna pedidos em um período.
        
        Como não há índice por data, utiliza busca linear.
        Complexidade: O(n) onde n é o número total de pedidos
        
        Para otimizar, poderia ser criado um índice por data ou
        usar estruturas de dados especializadas como árvores de intervalo.
        """
        todos_pedidos = self.repositorio.listar()
        return [
            pedido for pedido in todos_pedidos
            if data_inicio <= pedido.data_pedido <= data_fim
        ]