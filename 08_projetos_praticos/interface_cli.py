"""
INTERFACE CLI - SISTEMA DE GESTÃO EMPRESARIAL
============================================

Interface de linha de comando para interação com o sistema de gestão.
Demonstra como criar interfaces de usuário intuitivas e funcionais.
"""

# Importações padrão
from typing import Dict, List, Any, Optional
import sys
import os

# Adicionar o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importações dos módulos locais
from models import StatusPedido, TipoCliente, CategoriaProduct, Cliente, Produto, Pedido


class InterfaceCLI:
    """Interface de linha de comando para o sistema."""
    
    def __init__(self, sistema):
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