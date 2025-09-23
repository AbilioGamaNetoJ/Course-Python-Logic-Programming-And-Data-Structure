from typing import Any, Dict, List
import json
import csv
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import logging
import threading
from contextlib import contextmanager
import sys
import os
from collections import Counter
from dataclasses import asdict

# Adicionar o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import StatusPedido, TipoCliente, CategoriaProduct, TipoOperacao, Cliente, Produto, Pedido, ItemPedido
from repositories import RepositorioMemoria, ValidadorCliente, ValidadorProduto, ValidadorPedido
from services import ServicoCliente, ServicoProduto, ServicoPedido
from reports import GeradorRelatorios
from audit import SistemaAuditoria
from interface_cli import InterfaceCLI
from config import get_config


# ================================
# SISTEMA DE GESTÃO EMPRESARIAL
# ================================

class SistemaGestao:
    """Sistema principal de gestão empresarial."""
    
    def __init__(self):
        # Obter configurações
        self.config = get_config()
        
        # Repositórios
        self.repo_clientes = RepositorioMemoria(Cliente)
        self.repo_produtos = RepositorioMemoria(Produto)
        self.repo_pedidos = RepositorioMemoria(Pedido)
        
        # Validadores
        self.validador_cliente = ValidadorCliente()
        self.validador_produto = ValidadorProduto()
        self.validador_pedido = ValidadorPedido()
        
        # Serviços
        self.servico_cliente = ServicoCliente(self.repo_clientes, self.validador_cliente)
        self.servico_produto = ServicoProduto(self.repo_produtos, self.validador_produto)
        self.servico_pedido = ServicoPedido(
            self.repo_pedidos, self.validador_pedido,
            self.servico_cliente, self.servico_produto
        )
        
        # Sistemas auxiliares
        self.gerador_relatorios = GeradorRelatorios(
            self.servico_cliente, self.servico_produto, self.servico_pedido
        )
        self.auditoria = SistemaAuditoria()
        
        # Configurar logging
        self._configurar_logging()
    
    def _configurar_logging(self):
        """Configura o sistema de logging usando configurações centralizadas."""
        # Configurar handlers baseados nas configurações
        handlers = []
        
        # Handler para arquivo se especificado
        if self.config.logging.log_file:
            handlers.append(logging.FileHandler(
                self.config.logging.log_file, 
                encoding='utf-8'
            ))
        
        # Handler para console se habilitado
        if self.config.logging.console_output:
            handlers.append(logging.StreamHandler())
        
        # Configurar logging básico
        logging.basicConfig(
            level=getattr(logging, self.config.logging.level.value),
            format=self.config.logging.format,
            handlers=handlers,
            force=True  # Força reconfiguração se já existir
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Sistema de logging configurado - Nível: {self.config.logging.level.value}")
    
    def inicializar_dados_exemplo(self):
        """Inicializa o sistema com dados de exemplo usando configurações centralizadas."""
        if not self.config.system.init_sample_data:
            self.logger.info("Carregamento de dados de exemplo desabilitado nas configurações")
            return
            
        self.logger.info("Inicializando dados de exemplo...")
        
        # Criar clientes usando configurações
        clientes_exemplo = [
            {
                'nome': 'João Silva',
                'email': 'joao@email.com',
                'telefone': '11999999999',
                'tipo': TipoCliente.PESSOA_FISICA,
                'limite_credito': self.config.business.default_credit_limit
            },
            {
                'nome': 'Empresa ABC Ltda',
                'email': 'contato@abc.com',
                'telefone': '1133333333',
                'tipo': TipoCliente.PESSOA_JURIDICA,
                'limite_credito': self.config.business.default_credit_limit * 10  # Empresas têm limite maior
            },
            {
                'nome': 'Maria Santos',
                'email': 'maria@email.com',
                'telefone': '11888888888',
                'tipo': TipoCliente.VIP,
                'limite_credito': self.config.business.default_credit_limit * 2,
                'total_compras': 25000.0
            }
        ]
        
        for cliente_dados in clientes_exemplo:
            sucesso, id_cliente, erros = self.servico_cliente.criar_cliente(cliente_dados)
            if sucesso:
                self.logger.info(f"Cliente criado: {cliente_dados['nome']}")
            else:
                self.logger.error(f"Erro ao criar cliente: {erros}")
        
        # Criar produtos usando configurações
        produtos_exemplo = [
            {
                'nome': 'Smartphone XYZ',
                'descricao': 'Smartphone com 128GB',
                'categoria': CategoriaProduct.ELETRONICOS,
                'preco': 1200.0,
                'estoque': 50,
                'estoque_minimo': self.config.business.min_stock_level * 2,  # Produtos caros têm estoque maior
                'fornecedor': 'Tech Corp'
            },
            {
                'nome': 'Camiseta Polo',
                'descricao': 'Camiseta polo 100% algodão',
                'categoria': CategoriaProduct.ROUPAS,
                'preco': 89.90,
                'estoque': 100,
                'estoque_minimo': self.config.business.min_stock_level * 4,  # Roupas têm rotatividade alta
                'fornecedor': 'Fashion Inc'
            },
            {
                'nome': 'Livro Python',
                'descricao': 'Guia completo de Python',
                'categoria': CategoriaProduct.LIVROS,
                'preco': 79.90,
                'estoque': 30,
                'estoque_minimo': self.config.business.min_stock_level,
                'fornecedor': 'Editora Tech'
            }
        ]
        
        for produto_dados in produtos_exemplo:
            sucesso, id_produto, erros = self.servico_produto.criar_produto(produto_dados)
            if sucesso:
                self.logger.info(f"Produto criado: {produto_dados['nome']}")
            else:
                self.logger.error(f"Erro ao criar produto: {erros}")
        
        self.logger.info("Dados de exemplo inicializados com sucesso!")
    
    def dashboard_resumo(self) -> Dict[str, Any]:
        """Retorna resumo do dashboard."""
        total_clientes = self.repo_clientes.contar()
        total_produtos = self.repo_produtos.contar()
        total_pedidos = self.repo_pedidos.contar()
        
        # Pedidos por status
        pedidos_status = {}
        for status in StatusPedido:
            pedidos_status[status.value] = len(
                self.servico_pedido.pedidos_por_status(status)
            )
        
        # Produtos baixo estoque
        produtos_baixo_estoque = len(self.servico_produto.produtos_baixo_estoque())
        
        # Vendas do mês
        inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        relatorio_mes = self.gerador_relatorios.relatorio_vendas_periodo(
            inicio_mes, datetime.now()
        )
        
        return {
            'total_clientes': total_clientes,
            'total_produtos': total_produtos,
            'total_pedidos': total_pedidos,
            'pedidos_por_status': pedidos_status,
            'produtos_baixo_estoque': produtos_baixo_estoque,
            'vendas_mes': relatorio_mes['total_vendas'],
            'pedidos_mes': relatorio_mes['quantidade_pedidos']
        }
    
    def exportar_dados(self, formato: str = 'json') -> str:
        """Exporta dados do sistema."""
        dados = {
            'clientes': [asdict(c) for c in self.servico_cliente.listar_clientes()],
            'produtos': [asdict(p) for p in self.servico_produto.listar_produtos()],
            'pedidos': [asdict(p) for p in self.servico_pedido.listar_pedidos()]
        }
        
        if formato.lower() == 'json':
            return json.dumps(dados, default=str, indent=2, ensure_ascii=False)
        elif formato.lower() == 'csv':
            # Implementar exportação CSV
            return "Exportação CSV não implementada"
        else:
            raise ValueError("Formato não suportado")
    
    def backup_sistema(self, caminho: str):
        """Cria backup do sistema."""
        dados_backup = self.exportar_dados('json')
        
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            arquivo.write(dados_backup)
        
        self.logger.info(f"Backup criado em: {caminho}")
    
    def restaurar_backup(self, caminho: str):
        """Restaura backup do sistema."""
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            
            # Limpar dados atuais
            self.repo_clientes = RepositorioMemoria(Cliente)
            self.repo_produtos = RepositorioMemoria(Produto)
            self.repo_pedidos = RepositorioMemoria(Pedido)
            
            # Restaurar clientes
            for cliente_dados in dados.get('clientes', []):
                cliente = Cliente(**cliente_dados)
                self.repo_clientes.criar(cliente)
            
            # Restaurar produtos
            for produto_dados in dados.get('produtos', []):
                produto = Produto(**produto_dados)
                self.repo_produtos.criar(produto)
            
            # Restaurar pedidos
            for pedido_dados in dados.get('pedidos', []):
                # Converter itens
                itens = []
                for item_dados in pedido_dados.get('itens', []):
                    item = ItemPedido(**item_dados)
                    itens.append(item)
                
                pedido_dados['data_pedido'] = datetime.fromisoformat(pedido_dados['data_pedido'])
                pedido_dados['status'] = StatusPedido(pedido_dados['status'])
                
                # Restaurar itens
                from models import ItemPedido
                itens = []
                for item_data in pedido_dados.get('itens', []):
                    item = ItemPedido(**item_data)
                    itens.append(item)
                pedido_dados['itens'] = itens
                
                pedido = Pedido(**pedido_dados)
                self.repo_pedidos.criar(pedido)
            
            self.logger.info(f"Backup restaurado de: {caminho}")
            
        except Exception as e:
            self.logger.error(f"Erro ao restaurar backup: {e}")
            raise


# ================================
# INTERFACE DE LINHA DE COMANDO
# ================================

class InterfaceCLI:
    """Interface de linha de comando para o sistema."""
    
    def __init__(self, sistema: SistemaGestao):
        self.sistema = sistema
    
    def executar(self):
        """Executa a interface principal."""
        print("=" * 60)
        print("SISTEMA DE GESTÃO EMPRESARIAL")
        print("=" * 60)
        
        while True:
            self.mostrar_menu_principal()
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '0':
                print("Encerrando sistema...")
                break
            elif opcao == '1':
                self.menu_clientes()
            elif opcao == '2':
                self.menu_produtos()
            elif opcao == '3':
                self.menu_pedidos()
            elif opcao == '4':
                self.menu_relatorios()
            elif opcao == '5':
                self.mostrar_dashboard()
            elif opcao == '9':
                self.sistema.inicializar_dados_exemplo()
                print("Dados de exemplo carregados!")
            else:
                print("Opção inválida!")
    
    def mostrar_menu_principal(self):
        """Mostra o menu principal."""
        print("\n" + "=" * 40)
        print("MENU PRINCIPAL")
        print("=" * 40)
        print("1. Gerenciar Clientes")
        print("2. Gerenciar Produtos")
        print("3. Gerenciar Pedidos")
        print("4. Relatórios")
        print("5. Dashboard")
        print("9. Carregar Dados de Exemplo")
        print("0. Sair")
    
    def menu_clientes(self):
        """Menu de gerenciamento de clientes."""
        while True:
            print("\n" + "=" * 30)
            print("GERENCIAR CLIENTES")
            print("=" * 30)
            print("1. Listar Clientes")
            print("2. Buscar Cliente")
            print("3. Criar Cliente")
            print("4. Atualizar Cliente")
            print("5. Deletar Cliente")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '0':
                break
            elif opcao == '1':
                self.listar_clientes()
            elif opcao == '2':
                self.buscar_cliente()
            elif opcao == '3':
                self.criar_cliente()
            elif opcao == '4':
                self.atualizar_cliente()
            elif opcao == '5':
                self.deletar_cliente()
            else:
                print("Opção inválida!")
    
    def listar_clientes(self):
        """Lista todos os clientes."""
        clientes = self.sistema.servico_cliente.listar_clientes()
        
        if not clientes:
            print("Nenhum cliente cadastrado.")
            return
        
        print(f"\n{'ID':<36} {'Nome':<30} {'Email':<30} {'Tipo':<15}")
        print("-" * 111)
        
        for cliente in clientes:
            print(f"{cliente.id:<36} {cliente.nome:<30} {cliente.email:<30} {cliente.tipo.value:<15}")
    
    def buscar_cliente(self):
        """Busca um cliente por ID."""
        id_cliente = input("Digite o ID do cliente: ").strip()
        cliente = self.sistema.servico_cliente.buscar_cliente(id_cliente)
        
        if cliente:
            print(f"\nCliente encontrado:")
            print(f"ID: {cliente.id}")
            print(f"Nome: {cliente.nome}")
            print(f"Email: {cliente.email}")
            print(f"Telefone: {cliente.telefone}")
            print(f"Tipo: {cliente.tipo.value}")
            print(f"Total Compras: R$ {cliente.total_compras:.2f}")
        else:
            print("Cliente não encontrado.")
    
    def criar_cliente(self):
        """Cria um novo cliente."""
        print("\nCriando novo cliente:")
        
        dados = {
            'nome': input("Nome: ").strip(),
            'email': input("Email: ").strip(),
            'telefone': input("Telefone: ").strip(),
            'limite_credito': float(input("Limite de Crédito: ") or "0")
        }
        
        # Tipo de cliente
        print("\nTipos de cliente:")
        for i, tipo in enumerate(TipoCliente, 1):
            print(f"{i}. {tipo.value}")
        
        tipo_opcao = int(input("Escolha o tipo: ") or "1")
        dados['tipo'] = list(TipoCliente)[tipo_opcao - 1]
        
        sucesso, id_cliente, erros = self.sistema.servico_cliente.criar_cliente(dados)
        
        if sucesso:
            print(f"Cliente criado com sucesso! ID: {id_cliente}")
        else:
            print("Erro ao criar cliente:")
            for erro in erros:
                print(f"- {erro}")
    
    def atualizar_cliente(self):
        """Atualiza um cliente."""
        id_cliente = input("Digite o ID do cliente: ").strip()
        cliente = self.sistema.servico_cliente.buscar_cliente(id_cliente)
        
        if not cliente:
            print("Cliente não encontrado.")
            return
        
        print(f"\nAtualizando cliente: {cliente.nome}")
        print("(Deixe em branco para manter o valor atual)")
        
        dados = {}
        
        nome = input(f"Nome ({cliente.nome}): ").strip()
        if nome:
            dados['nome'] = nome
        
        email = input(f"Email ({cliente.email}): ").strip()
        if email:
            dados['email'] = email
        
        telefone = input(f"Telefone ({cliente.telefone}): ").strip()
        if telefone:
            dados['telefone'] = telefone
        
        if dados:
            sucesso, erros = self.sistema.servico_cliente.atualizar_cliente(id_cliente, dados)
            
            if sucesso:
                print("Cliente atualizado com sucesso!")
            else:
                print("Erro ao atualizar cliente:")
                for erro in erros:
                    print(f"- {erro}")
        else:
            print("Nenhuma alteração realizada.")
    
    def deletar_cliente(self):
        """Deleta um cliente."""
        id_cliente = input("Digite o ID do cliente: ").strip()
        cliente = self.sistema.servico_cliente.buscar_cliente(id_cliente)
        
        if not cliente:
            print("Cliente não encontrado.")
            return
        
        confirmacao = input(f"Confirma a exclusão do cliente '{cliente.nome}'? (s/N): ").strip().lower()
        
        if confirmacao == 's':
            sucesso = self.sistema.servico_cliente.deletar_cliente(id_cliente)
            if sucesso:
                print("Cliente deletado com sucesso!")
            else:
                print("Erro ao deletar cliente.")
        else:
            print("Operação cancelada.")
    
    def menu_produtos(self):
        """Menu de gerenciamento de produtos."""
        while True:
            print("\n" + "=" * 30)
            print("GERENCIAR PRODUTOS")
            print("=" * 30)
            print("1. Listar Produtos")
            print("2. Buscar Produto")
            print("3. Criar Produto")
            print("4. Atualizar Produto")
            print("5. Deletar Produto")
            print("6. Produtos Baixo Estoque")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '0':
                break
            elif opcao == '1':
                self.listar_produtos()
            elif opcao == '2':
                self.buscar_produto()
            elif opcao == '3':
                self.criar_produto()
            elif opcao == '4':
                self.atualizar_produto()
            elif opcao == '5':
                self.deletar_produto()
            elif opcao == '6':
                self.produtos_baixo_estoque()
            else:
                print("Opção inválida!")
    
    def listar_produtos(self):
        """Lista todos os produtos."""
        produtos = self.sistema.servico_produto.listar_produtos()
        
        if not produtos:
            print("Nenhum produto cadastrado.")
            return
        
        print(f"\n{'Nome':<30} {'Categoria':<15} {'Preço':<10} {'Estoque':<8} {'Status'}")
        print("-" * 75)
        
        for produto in produtos:
            status = "⚠️ Baixo" if produto.precisa_reposicao else "✅ OK"
            print(f"{produto.nome:<30} {produto.categoria.value:<15} R${produto.preco:<9.2f} {produto.estoque:<8} {status}")
    
    def buscar_produto(self):
        """Busca um produto por ID."""
        id_produto = input("Digite o ID do produto: ").strip()
        produto = self.sistema.servico_produto.buscar_produto(id_produto)
        
        if produto:
            print(f"\nProduto encontrado:")
            print(f"ID: {produto.id}")
            print(f"Nome: {produto.nome}")
            print(f"Descrição: {produto.descricao}")
            print(f"Categoria: {produto.categoria.value}")
            print(f"Preço: R$ {produto.preco:.2f}")
            print(f"Estoque: {produto.estoque}")
            print(f"Estoque Mínimo: {produto.estoque_minimo}")
            print(f"Fornecedor: {produto.fornecedor}")
            print(f"Valor Total Estoque: R$ {produto.valor_estoque:.2f}")
        else:
            print("Produto não encontrado.")
    
    def criar_produto(self):
        """Cria um novo produto."""
        print("\nCriando novo produto:")
        
        dados = {
            'nome': input("Nome: ").strip(),
            'descricao': input("Descrição: ").strip(),
            'preco': float(input("Preço: ") or "0"),
            'estoque': int(input("Estoque: ") or "0"),
            'estoque_minimo': int(input("Estoque Mínimo: ") or "5"),
            'fornecedor': input("Fornecedor: ").strip()
        }
        
        # Categoria
        print("\nCategorias:")
        for i, categoria in enumerate(CategoriaProduct, 1):
            print(f"{i}. {categoria.value}")
        
        cat_opcao = int(input("Escolha a categoria: ") or "1")
        dados['categoria'] = list(CategoriaProduct)[cat_opcao - 1]
        
        sucesso, id_produto, erros = self.sistema.servico_produto.criar_produto(dados)
        
        if sucesso:
            print(f"Produto criado com sucesso! ID: {id_produto}")
        else:
            print("Erro ao criar produto:")
            for erro in erros:
                print(f"- {erro}")
    
    def atualizar_produto(self):
        """Atualiza um produto."""
        id_produto = input("Digite o ID do produto: ").strip()
        produto = self.sistema.servico_produto.buscar_produto(id_produto)
        
        if not produto:
            print("Produto não encontrado.")
            return
        
        print(f"\nAtualizando produto: {produto.nome}")
        print("(Deixe em branco para manter o valor atual)")
        
        dados = {}
        
        nome = input(f"Nome ({produto.nome}): ").strip()
        if nome:
            dados['nome'] = nome
        
        preco = input(f"Preço ({produto.preco}): ").strip()
        if preco:
            dados['preco'] = float(preco)
        
        estoque = input(f"Estoque ({produto.estoque}): ").strip()
        if estoque:
            dados['estoque'] = int(estoque)
        
        if dados:
            sucesso, erros = self.sistema.servico_produto.atualizar_produto(id_produto, dados)
            
            if sucesso:
                print("Produto atualizado com sucesso!")
            else:
                print("Erro ao atualizar produto:")
                for erro in erros:
                    print(f"- {erro}")
        else:
            print("Nenhuma alteração realizada.")
    
    def deletar_produto(self):
        """Deleta um produto."""
        id_produto = input("Digite o ID do produto: ").strip()
        produto = self.sistema.servico_produto.buscar_produto(id_produto)
        
        if not produto:
            print("Produto não encontrado.")
            return
        
        confirmacao = input(f"Confirma a exclusão do produto '{produto.nome}'? (s/N): ").strip().lower()
        
        if confirmacao == 's':
            sucesso = self.sistema.servico_produto.deletar_produto(id_produto)
            if sucesso:
                print("Produto deletado com sucesso!")
            else:
                print("Erro ao deletar produto.")
        else:
            print("Operação cancelada.")
    
    def produtos_baixo_estoque(self):
        """Lista produtos com estoque baixo."""
        produtos = self.sistema.servico_produto.produtos_baixo_estoque()
        
        if not produtos:
            print("Nenhum produto com estoque baixo.")
            return
        
        print(f"\n{'Nome':<30} {'Estoque':<8} {'Mínimo':<8} {'Diferença'}")
        print("-" * 60)
        
        for produto in produtos:
            diferenca = produto.estoque_minimo - produto.estoque
            print(f"{produto.nome:<30} {produto.estoque:<8} {produto.estoque_minimo:<8} {diferenca}")
    
    def menu_pedidos(self):
        """Menu de gerenciamento de pedidos."""
        while True:
            print("\n" + "=" * 30)
            print("GERENCIAR PEDIDOS")
            print("=" * 30)
            print("1. Listar Pedidos")
            print("2. Buscar Pedido")
            print("3. Criar Pedido")
            print("4. Atualizar Status")
            print("5. Cancelar Pedido")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '0':
                break
            elif opcao == '1':
                self.listar_pedidos()
            elif opcao == '2':
                self.buscar_pedido()
            elif opcao == '3':
                self.criar_pedido()
            elif opcao == '4':
                self.atualizar_status_pedido()
            elif opcao == '5':
                self.cancelar_pedido()
            else:
                print("Opção inválida!")
    
    def listar_pedidos(self):
        """Lista todos os pedidos."""
        pedidos = self.sistema.servico_pedido.listar_pedidos()
        
        if not pedidos:
            print("Nenhum pedido cadastrado.")
            return
        
        print(f"\n{'ID':<8} {'Cliente':<30} {'Status':<12} {'Total':<10} {'Data'}")
        print("-" * 75)
        
        for pedido in pedidos:
            cliente = self.sistema.servico_cliente.buscar_cliente(pedido.cliente_id)
            nome_cliente = cliente.nome if cliente else "Cliente não encontrado"
            data_str = pedido.data_pedido.strftime("%d/%m/%Y")
            
            print(f"{pedido.id[:8]:<8} {nome_cliente:<30} {pedido.status.value:<12} R${pedido.total:<9.2f} {data_str}")
    
    def buscar_pedido(self):
        """Busca um pedido por ID."""
        id_pedido = input("Digite o ID do pedido: ").strip()
        pedido = self.sistema.servico_pedido.buscar_pedido(id_pedido)
        
        if not pedido:
            print("Pedido não encontrado.")
            return
        
        cliente = self.sistema.servico_cliente.buscar_cliente(pedido.cliente_id)
        
        print(f"\nPedido encontrado:")
        print(f"ID: {pedido.id}")
        print(f"Cliente: {cliente.nome if cliente else 'Cliente não encontrado'}")
        print(f"Status: {pedido.status.value}")
        print(f"Data: {pedido.data_pedido.strftime('%d/%m/%Y %H:%M')}")
        print(f"Total: R$ {pedido.total:.2f}")
        print(f"Quantidade de Itens: {pedido.quantidade_itens}")
        
        print("\nItens do Pedido:")
        for i, item in enumerate(pedido.itens, 1):
            produto = self.sistema.servico_produto.buscar_produto(item.produto_id)
            nome_produto = produto.nome if produto else "Produto não encontrado"
            print(f"{i}. {nome_produto} - Qtd: {item.quantidade} - Preço: R$ {item.preco_unitario:.2f} - Subtotal: R$ {item.subtotal:.2f}")
    
    def criar_pedido(self):
        """Cria um novo pedido."""
        print("\nCriando novo pedido:")
        
        # Listar clientes
        clientes = self.sistema.servico_cliente.listar_clientes()
        if not clientes:
            print("Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
            return
        
        print("\nClientes disponíveis:")
        for i, cliente in enumerate(clientes, 1):
            print(f"{i}. {cliente.nome} ({cliente.email})")
        
        cliente_opcao = int(input("Escolha o cliente: ")) - 1
        if cliente_opcao < 0 or cliente_opcao >= len(clientes):
            print("Cliente inválido.")
            return
        
        cliente_selecionado = clientes[cliente_opcao]
        
        # Listar produtos
        produtos = self.sistema.servico_produto.listar_produtos()
        if not produtos:
            print("Nenhum produto cadastrado. Cadastre produtos primeiro.")
            return
        
        print("\nProdutos disponíveis:")
        for i, produto in enumerate(produtos, 1):
            print(f"{i}. {produto.nome} - R$ {produto.preco:.2f} (Estoque: {produto.estoque})")
        
        # Adicionar itens
        itens = []
        while True:
            produto_opcao = input("\nEscolha o produto (número) ou 'f' para finalizar: ").strip()
            
            if produto_opcao.lower() == 'f':
                break
            
            try:
                produto_idx = int(produto_opcao) - 1
                if produto_idx < 0 or produto_idx >= len(produtos):
                    print("Produto inválido.")
                    continue
                
                produto_selecionado = produtos[produto_idx]
                quantidade = int(input(f"Quantidade de {produto_selecionado.nome}: "))
                
                if quantidade <= 0:
                    print("Quantidade deve ser maior que zero.")
                    continue
                
                if quantidade > produto_selecionado.estoque:
                    print(f"Estoque insuficiente. Disponível: {produto_selecionado.estoque}")
                    continue
                
                item = {
                    'produto_id': produto_selecionado.id,
                    'quantidade': quantidade,
                    'preco_unitario': produto_selecionado.preco
                }
                itens.append(item)
                print(f"Item adicionado: {produto_selecionado.nome} x{quantidade}")
                
            except ValueError:
                print("Entrada inválida.")
        
        if not itens:
            print("Nenhum item adicionado. Pedido cancelado.")
            return
        
        # Criar pedido
        dados_pedido = {
            'cliente_id': cliente_selecionado.id,
            'itens': itens
        }
        
        sucesso, id_pedido, erros = self.sistema.servico_pedido.criar_pedido(dados_pedido)
        
        if sucesso:
            print(f"Pedido criado com sucesso! ID: {id_pedido}")
        else:
            print("Erro ao criar pedido:")
            for erro in erros:
                print(f"- {erro}")
    
    def atualizar_status_pedido(self):
        """Atualiza o status de um pedido."""
        id_pedido = input("Digite o ID do pedido: ").strip()
        pedido = self.sistema.servico_pedido.buscar_pedido(id_pedido)
        
        if not pedido:
            print("Pedido não encontrado.")
            return
        
        print(f"\nPedido: {id_pedido[:8]}")
        print(f"Status atual: {pedido.status.value}")
        
        print("\nNovos status disponíveis:")
        for i, status in enumerate(StatusPedido, 1):
            print(f"{i}. {status.value}")
        
        status_opcao = int(input("Escolha o novo status: ")) - 1
        if status_opcao < 0 or status_opcao >= len(StatusPedido):
            print("Status inválido.")
            return
        
        novo_status = list(StatusPedido)[status_opcao]
        sucesso = self.sistema.servico_pedido.atualizar_status(id_pedido, novo_status)
        
        if sucesso:
            print("Status atualizado com sucesso!")
        else:
            print("Erro ao atualizar status.")
    
    def cancelar_pedido(self):
        """Cancela um pedido."""
        id_pedido = input("Digite o ID do pedido: ").strip()
        pedido = self.sistema.servico_pedido.buscar_pedido(id_pedido)
        
        if not pedido:
            print("Pedido não encontrado.")
            return
        
        if pedido.status == StatusPedido.CANCELADO:
            print("Pedido já está cancelado.")
            return
        
        confirmacao = input(f"Confirma o cancelamento do pedido {id_pedido[:8]}? (s/N): ").strip().lower()
        
        if confirmacao == 's':
            sucesso = self.sistema.servico_pedido.cancelar_pedido(id_pedido)
            if sucesso:
                print("Pedido cancelado com sucesso! Estoque restaurado.")
            else:
                print("Erro ao cancelar pedido.")
        else:
            print("Operação cancelada.")
    
    def menu_relatorios(self):
        """Menu de relatórios."""
        while True:
            print("\n" + "=" * 30)
            print("RELATÓRIOS")
            print("=" * 30)
            print("1. Relatório de Vendas")
            print("2. Relatório de Estoque")
            print("3. Relatório de Clientes")
            print("4. Relatório de Auditoria")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '0':
                break
            elif opcao == '1':
                self.relatorio_vendas()
            elif opcao == '2':
                self.relatorio_estoque()
            elif opcao == '3':
                self.relatorio_clientes()
            elif opcao == '4':
                self.relatorio_auditoria()
            else:
                print("Opção inválida!")
    
    def relatorio_vendas(self):
        """Exibe relatório de vendas."""
        print("\nRelatório de Vendas - Últimos 30 dias")
        
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=30)
        
        relatorio = self.sistema.gerador_relatorios.relatorio_vendas_periodo(data_inicio, data_fim)
        
        print(f"Período: {relatorio['periodo']}")
        print(f"Total de Vendas: R$ {relatorio['total_vendas']:.2f}")
        print(f"Quantidade de Pedidos: {relatorio['quantidade_pedidos']}")
        print(f"Ticket Médio: R$ {relatorio['ticket_medio']:.2f}")
        
        if relatorio['produtos_mais_vendidos']:
            print("\nProdutos Mais Vendidos:")
            for produto in relatorio['produtos_mais_vendidos'][:5]:
                print(f"- {produto['produto']}: {produto['quantidade']} unidades")
    
    def relatorio_estoque(self):
        """Exibe relatório de estoque."""
        print("\nRelatório de Estoque")
        
        relatorio = self.sistema.gerador_relatorios.relatorio_estoque()
        
        print(f"Total de Produtos: {relatorio['total_produtos']}")
        print(f"Valor Total do Estoque: R$ {relatorio['valor_total_estoque']:.2f}")
        print(f"Produtos com Estoque Baixo: {relatorio['produtos_baixo_estoque']}")
        
        if relatorio['produtos_reposicao']:
            print("\nProdutos que Precisam de Reposição:")
            for produto in relatorio['produtos_reposicao'][:10]:
                print(f"- {produto['nome']}: {produto['estoque_atual']} (mín: {produto['estoque_minimo']})")
    
    def relatorio_clientes(self):
        """Exibe relatório de clientes."""
        print("\nRelatório de Clientes")
        
        relatorio = self.sistema.gerador_relatorios.relatorio_clientes()
        
        print(f"Total de Clientes: {relatorio['total_clientes']}")
        print(f"Clientes Inativos: {relatorio['clientes_inativos']}")
        
        print("\nClientes por Tipo:")
        for tipo, quantidade in relatorio['clientes_por_tipo'].items():
            print(f"- {tipo}: {quantidade}")
        
        if relatorio['top_clientes']:
            print("\nTop 5 Clientes:")
            for cliente in relatorio['top_clientes'][:5]:
                print(f"- {cliente['nome']}: R$ {cliente['total_compras']:.2f}")
    
    def relatorio_auditoria(self):
        """Exibe relatório de auditoria."""
        print("\nRelatório de Auditoria - Últimos 30 dias")
        
        relatorio = self.sistema.auditoria.relatorio_atividade(30)
        
        print(f"Total de Operações: {relatorio['total_operacoes']}")
        
        print("\nOperações por Tipo:")
        for tipo, quantidade in relatorio['operacoes_por_tipo'].items():
            print(f"- {tipo}: {quantidade}")
        
        print("\nAtividade por Usuário:")
        for usuario, quantidade in relatorio['atividade_por_usuario'].items():
            print(f"- {usuario}: {quantidade}")
    
    def mostrar_dashboard(self):
        """Mostra o dashboard do sistema."""
        print("\n" + "=" * 50)
        print("DASHBOARD DO SISTEMA")
        print("=" * 50)
        
        dashboard = self.sistema.dashboard_resumo()
        
        print(f"Total de Clientes: {dashboard['total_clientes']}")
        print(f"Total de Produtos: {dashboard['total_produtos']}")
        print(f"Total de Pedidos: {dashboard['total_pedidos']}")
        print(f"Produtos com Estoque Baixo: {dashboard['produtos_baixo_estoque']}")
        
        print(f"\nVendas do Mês: R$ {dashboard['vendas_mes']:.2f}")
        print(f"Pedidos do Mês: {dashboard['pedidos_mes']}")
        
        print("\nPedidos por Status:")
        for status, quantidade in dashboard['pedidos_por_status'].items():
            print(f"- {status}: {quantidade}")


# ================================
# FUNÇÕES DE DEMONSTRAÇÃO
# ================================

def demonstrar_estruturas_dados():
    """Demonstra o uso das estruturas de dados no sistema."""
    print("\n" + "=" * 60)
    print("DEMONSTRAÇÃO: ESTRUTURAS DE DADOS")
    print("=" * 60)
    
    # Criar sistema
    sistema = SistemaGestao()
    
    print("\n1. REPOSITÓRIO COM ÍNDICES (Dicionários + Sets)")
    print("-" * 50)
    
    # Demonstrar índices automáticos
    cliente_dados = {
        'nome': 'João Silva',
        'email': 'joao@email.com',
        'tipo': TipoCliente.PESSOA_FISICA
    }
    
    sucesso, id_cliente, _ = sistema.servico_cliente.criar_cliente(cliente_dados)
    print(f"Cliente criado: {id_cliente}")
    
    # Busca por índice (O(1))
    clientes_pf = sistema.repo_clientes.buscar_por_campo('tipo', TipoCliente.PESSOA_FISICA)
    print(f"Busca por tipo (O(1)): {len(clientes_pf)} clientes encontrados")
    
    print("\n2. LISTAS ORDENADAS PARA RELATÓRIOS")
    print("-" * 50)
    
    # Criar produtos para demonstrar ordenação
    produtos_dados = [
        {'nome': 'Produto A', 'preco': 100.0, 'estoque': 50},
        {'nome': 'Produto B', 'preco': 200.0, 'estoque': 3},  # Baixo estoque
        {'nome': 'Produto C', 'preco': 150.0, 'estoque': 25}
    ]
    
    for produto_dados in produtos_dados:
        sistema.servico_produto.criar_produto(produto_dados)
    
    # Produtos ordenados por estoque (algoritmo de ordenação)
    produtos = sistema.servico_produto.listar_produtos()
    produtos_ordenados = sorted(produtos, key=lambda p: p.estoque)
    
    print("Produtos ordenados por estoque:")
    for produto in produtos_ordenados:
        print(f"- {produto.nome}: {produto.estoque} unidades")
    
    print("\n3. SETS PARA VALIDAÇÕES ÚNICAS")
    print("-" * 50)
    
    # Demonstrar validação de email único
    cliente_duplicado = {
        'nome': 'Maria Silva',
        'email': 'joao@email.com',  # Email já existe
        'tipo': TipoCliente.PESSOA_FISICA
    }
    
    sucesso, _, erros = sistema.servico_cliente.criar_cliente(cliente_duplicado)
    print(f"Tentativa de email duplicado: {'Sucesso' if sucesso else 'Falhou'}")
    if erros:
        print(f"Erro: {erros[0]}")
    
    print("\n4. COUNTER PARA ESTATÍSTICAS")
    print("-" * 50)
    
    # Simular alguns pedidos
    pedidos_dados = [
        {'cliente_id': id_cliente, 'itens': [{'produto_id': produtos[0].id, 'quantidade': 2, 'preco_unitario': 100.0}]},
        {'cliente_id': id_cliente, 'itens': [{'produto_id': produtos[1].id, 'quantidade': 1, 'preco_unitario': 200.0}]}
    ]
    
    for pedido_dados in pedidos_dados:
        sistema.servico_pedido.criar_pedido(pedido_dados)
    
    # Usar Counter para estatísticas
    pedidos = sistema.servico_pedido.listar_pedidos()
    status_counter = Counter(p.status.value for p in pedidos)
    
    print("Pedidos por status (Counter):")
    for status, quantidade in status_counter.items():
        print(f"- {status}: {quantidade}")


def demonstrar_algoritmos():
    """Demonstra algoritmos implementados no sistema."""
    print("\n" + "=" * 60)
    print("DEMONSTRAÇÃO: ALGORITMOS")
    print("=" * 60)
    
    sistema = SistemaGestao()
    sistema.inicializar_dados_exemplo()
    
    print("\n1. ALGORITMO DE BUSCA BINÁRIA")
    print("-" * 50)
    
    # Busca por ID (implementada com dicionário - O(1))
    clientes = sistema.servico_cliente.listar_clientes()
    if clientes:
        cliente_id = clientes[0].id
        inicio = datetime.now()
        cliente_encontrado = sistema.servico_cliente.buscar_cliente(cliente_id)
        fim = datetime.now()
        
        print(f"Busca por ID: {(fim - inicio).total_seconds() * 1000:.2f}ms")
        print(f"Cliente encontrado: {cliente_encontrado.nome if cliente_encontrado else 'Não encontrado'}")
    
    print("\n2. ALGORITMOS DE ORDENAÇÃO")
    print("-" * 50)
    
    # Ordenação de produtos por diferentes critérios
    produtos = sistema.servico_produto.listar_produtos()
    
    # Por preço (crescente)
    produtos_por_preco = sorted(produtos, key=lambda p: p.preco)
    print("Produtos ordenados por preço:")
    for produto in produtos_por_preco:
        print(f"- {produto.nome}: R$ {produto.preco:.2f}")
    
    # Por estoque (decrescente)
    produtos_por_estoque = sorted(produtos, key=lambda p: p.estoque, reverse=True)
    print("\nProdutos ordenados por estoque (maior primeiro):")
    for produto in produtos_por_estoque:
        print(f"- {produto.nome}: {produto.estoque} unidades")
    
    print("\n3. ALGORITMO DE FILTRAGEM")
    print("-" * 50)
    
    # Filtro combinado usando múltiplos critérios
    produtos_filtrados = [
        p for p in produtos 
        if p.preco > 50 and p.estoque > 10 and p.ativo
    ]
    
    print(f"Produtos com preço > R$ 50 e estoque > 10: {len(produtos_filtrados)}")
    for produto in produtos_filtrados:
        print(f"- {produto.nome}: R$ {produto.preco:.2f} ({produto.estoque} unidades)")
    
    print("\n4. ALGORITMO DE AGREGAÇÃO")
    print("-" * 50)
    
    # Calcular estatísticas usando algoritmos de agregação
    if produtos:
        preco_medio = sum(p.preco for p in produtos) / len(produtos)
        preco_maximo = max(p.preco for p in produtos)
        preco_minimo = min(p.preco for p in produtos)
        valor_total_estoque = sum(p.valor_estoque for p in produtos)
        
        print(f"Preço médio: R$ {preco_medio:.2f}")
        print(f"Preço máximo: R$ {preco_maximo:.2f}")
        print(f"Preço mínimo: R$ {preco_minimo:.2f}")
        print(f"Valor total do estoque: R$ {valor_total_estoque:.2f}")


def demonstrar_padroes_design():
    """Demonstra padrões de design implementados."""
    print("\n" + "=" * 60)
    print("DEMONSTRAÇÃO: PADRÕES DE DESIGN")
    print("=" * 60)
    
    print("\n1. PADRÃO REPOSITORY")
    print("-" * 50)
    print("- Abstração do acesso a dados")
    print("- Interface comum para diferentes tipos de armazenamento")
    print("- Facilita testes e mudanças de implementação")
    
    # Demonstrar polimorfismo com repositórios
    repo_cliente = RepositorioMemoria(Cliente)
    print(f"Repositório criado: {type(repo_cliente).__name__}")
    
    print("\n2. PADRÃO STRATEGY (Validadores)")
    print("-" * 50)
    print("- Diferentes estratégias de validação")
    print("- Facilita adição de novas regras")
    print("- Separação de responsabilidades")
    
    validador = ValidadorCliente()
    dados_validos = {'nome': 'João', 'email': 'joao@email.com'}
    dados_invalidos = {'nome': '', 'email': 'email_invalido'}
    
    valido1, erros1 = validador.validar(dados_validos)
    valido2, erros2 = validador.validar(dados_invalidos)
    
    print(f"Dados válidos: {valido1}")
    print(f"Dados inválidos: {valido2}, Erros: {erros2}")
    
    print("\n3. PADRÃO FACADE (Sistema Principal)")
    print("-" * 50)
    print("- Interface simplificada para subsistemas complexos")
    print("- Coordenação entre múltiplos serviços")
    print("- Reduz acoplamento entre componentes")
    
    sistema = SistemaGestao()
    print(f"Sistema criado com {len(sistema.__dict__)} componentes integrados")
    
    print("\n4. PADRÃO OBSERVER (Auditoria)")
    print("-" * 50)
    print("- Rastreamento automático de operações")
    print("- Desacoplamento entre ação e logging")
    print("- Facilita compliance e debugging")
    
    # Simular operação com auditoria
    sistema.auditoria.registrar_operacao(
        TipoOperacao.CREATE, 
        'Cliente', 
        'test-id', 
        'usuario_teste',
        {'acao': 'Demonstração de auditoria'}
    )
    
    logs = sistema.auditoria.repositorio_logs.listar()
    print(f"Logs registrados: {len(logs)}")


def benchmark_performance():
    """Executa benchmark de performance do sistema."""
    print("\n" + "=" * 60)
    print("BENCHMARK DE PERFORMANCE")
    print("=" * 60)
    
    sistema = SistemaGestao()
    
    print("\n1. TESTE DE CRIAÇÃO EM MASSA")
    print("-" * 50)
    
    # Benchmark criação de clientes
    inicio = datetime.now()
    
    for i in range(1000):
        dados_cliente = {
            'nome': f'Cliente {i}',
            'email': f'cliente{i}@email.com',
            'tipo': TipoCliente.PESSOA_FISICA
        }
        sistema.servico_cliente.criar_cliente(dados_cliente)
    
    fim = datetime.now()
    tempo_criacao = (fim - inicio).total_seconds()
    
    print(f"1000 clientes criados em: {tempo_criacao:.3f}s")
    print(f"Taxa: {1000/tempo_criacao:.0f} clientes/segundo")
    
    print("\n2. TESTE DE BUSCA EM MASSA")
    print("-" * 50)
    
    clientes = sistema.servico_cliente.listar_clientes()
    ids_clientes = [c.id for c in clientes[:100]]
    
    inicio = datetime.now()
    
    for cliente_id in ids_clientes:
        sistema.servico_cliente.buscar_cliente(cliente_id)
    
    fim = datetime.now()
    tempo_busca = (fim - inicio).total_seconds()
    
    print(f"100 buscas executadas em: {tempo_busca:.3f}s")
    print(f"Taxa: {100/tempo_busca:.0f} buscas/segundo")
    
    print("\n3. TESTE DE FILTROS COMPLEXOS")
    print("-" * 50)
    
    inicio = datetime.now()
    
    # Filtros usando índices
    clientes_pf = sistema.repo_clientes.buscar_por_campo('tipo', TipoCliente.PESSOA_FISICA)
    
    fim = datetime.now()
    tempo_filtro = (fim - inicio).total_seconds()
    
    print(f"Filtro por tipo executado em: {tempo_filtro*1000:.2f}ms")
    print(f"Resultados encontrados: {len(clientes_pf)}")
    
    print("\n4. ANÁLISE DE COMPLEXIDADE")
    print("-" * 50)
    print("Operações e suas complexidades:")
    print("- Busca por ID: O(1) - Hash table")
    print("- Busca por campo indexado: O(1) - Índice")
    print("- Busca por campo não indexado: O(n) - Linear")
    print("- Ordenação: O(n log n) - Timsort")
    print("- Inserção: O(1) - Amortizado")
    print("- Remoção: O(1) - Hash table")


def main():
    """Função principal para demonstração completa."""
    print("MÓDULO 08.1 - SISTEMA DE GESTÃO EMPRESARIAL")
    print("=" * 60)
    
    # Executar demonstrações
    demonstrar_estruturas_dados()
    demonstrar_algoritmos()
    demonstrar_padroes_design()
    benchmark_performance()
    
    print("\n" + "=" * 60)
    print("INTERFACE INTERATIVA")
    print("=" * 60)
    
    # Perguntar se deseja executar interface
    resposta = input("Deseja executar a interface interativa? (s/N): ").strip().lower()
    
    if resposta == 's':
        sistema = SistemaGestao()
        interface = InterfaceCLI(sistema)
        interface.executar()
    
    print("\n" + "=" * 60)
    print("CONCLUSÃO DO MÓDULO 08.1")
    print("=" * 60)
    print("""
Principais Aprendizados:

1. INTEGRAÇÃO DE ESTRUTURAS DE DADOS:
   • Dicionários para índices rápidos (O(1))
   • Listas para coleções ordenadas
   • Sets para validações de unicidade
   • Counter para estatísticas
   • defaultdict para agrupamentos

2. IMPLEMENTAÇÃO DE ALGORITMOS:
   • Busca por hash (O(1))
   • Ordenação por múltiplos critérios
   • Filtros combinados eficientes
   • Agregações estatísticas
   • Validações complexas

3. PADRÕES DE DESIGN APLICADOS:
   • Repository: Abstração de dados
   • Strategy: Validadores intercambiáveis
   • Facade: Interface simplificada
   • Observer: Sistema de auditoria
   • Factory: Criação de objetos

4. ARQUITETURA EM CAMADAS:
   • Camada de Dados (Repositórios)
   • Camada de Negócio (Serviços)
   • Camada de Apresentação (CLI)
   • Camada de Infraestrutura (Logging, Auditoria)

5. FUNCIONALIDADES EMPRESARIAIS:
   • CRUD completo para todas entidades
   • Validações de integridade
   • Relatórios e analytics
   • Sistema de auditoria
   • Backup e recuperação

6. OTIMIZAÇÕES DE PERFORMANCE:
   • Índices automáticos
   • Cache de objetos
   • Operações em lote
   • Lazy loading
   • Estruturas eficientes

7. QUALIDADE DE SOFTWARE:
   • Validação de dados
   • Tratamento de erros
   • Logging estruturado
   • Testes de performance
   • Documentação completa

8. CONCEITOS AVANÇADOS:
   • Threading para concorrência
   • Context managers
   • Decorators para funcionalidades
   • Type hints para clareza
   • Dataclasses para modelos

9. ANÁLISE DE COMPLEXIDADE:
   • Identificação de gargalos
   • Otimização baseada em dados
   • Trade-offs espaço-tempo
   • Benchmarks sistemáticos
   • Métricas de performance

10. BOAS PRÁTICAS:
    • Separação de responsabilidades
    • Código limpo e legível
    • Reutilização de componentes
    • Extensibilidade
    • Manutenibilidade

Este sistema demonstra como integrar todos os conceitos
do curso em uma aplicação real e robusta, preparando
para desenvolvimento de software profissional.

Próximo: Motor de Busca Inteligente
    """)


if __name__ == "__main__":
    main()
