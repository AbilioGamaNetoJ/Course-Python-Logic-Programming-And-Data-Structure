"""
MÓDULO DE RELATÓRIOS
===================

Este módulo contém as classes responsáveis pela geração de relatórios
do sistema de gestão empresarial.
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter

# Adicionar o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import StatusPedido, TipoCliente, CategoriaProduct
from config import get_config


class GeradorRelatorios:
    """
    Classe responsável pela geração de relatórios do sistema.
    """
    
    def __init__(self, servico_cliente, servico_produto, servico_pedido):
        """
        Inicializa o gerador de relatórios.
        
        Args:
            servico_cliente: Serviço de clientes
            servico_produto: Serviço de produtos
            servico_pedido: Serviço de pedidos
        """
        self.servico_cliente = servico_cliente
        self.servico_produto = servico_produto
        self.servico_pedido = servico_pedido
        self.config = get_config()
    
    def relatorio_vendas_periodo(self, data_inicio: datetime, data_fim: datetime) -> Dict[str, Any]:
        """
        Gera relatório de vendas para um período específico.
        
        Args:
            data_inicio: Data de início do período
            data_fim: Data de fim do período
            
        Returns:
            Dicionário com dados do relatório
        """
        pedidos = self.servico_pedido.listar_pedidos()
        
        # Filtrar pedidos do período
        pedidos_periodo = [
            p for p in pedidos 
            if data_inicio <= p.data_pedido <= data_fim and p.status != StatusPedido.CANCELADO
        ]
        
        # Calcular métricas
        total_vendas = sum(p.total for p in pedidos_periodo)
        quantidade_pedidos = len(pedidos_periodo)
        ticket_medio = total_vendas / quantidade_pedidos if quantidade_pedidos > 0 else 0
        
        # Produtos mais vendidos
        produtos_vendidos = defaultdict(int)
        for pedido in pedidos_periodo:
            for item in pedido.itens:
                produtos_vendidos[item.produto_id] += item.quantidade
        
        produtos_mais_vendidos = []
        for produto_id, quantidade in sorted(produtos_vendidos.items(), key=lambda x: x[1], reverse=True):
            produto = self.servico_produto.buscar_produto(produto_id)
            if produto:
                produtos_mais_vendidos.append({
                    'produto': produto.nome,
                    'produto_id': produto_id,
                    'quantidade': quantidade
                })
        
        return {
            'periodo': f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}",
            'total_vendas': total_vendas,
            'quantidade_pedidos': quantidade_pedidos,
            'ticket_medio': ticket_medio,
            'produtos_mais_vendidos': produtos_mais_vendidos
        }
    
    def relatorio_estoque(self) -> Dict[str, Any]:
        """
        Gera relatório de estoque atual.
        
        Returns:
            Dicionário com dados do estoque
        """
        produtos = self.servico_produto.listar_produtos()
        
        total_produtos = len(produtos)
        valor_total_estoque = sum(p.preco * p.estoque for p in produtos)
        
        # Produtos com estoque baixo
        produtos_baixo_estoque = [
            p for p in produtos 
            if p.estoque <= p.estoque_minimo
        ]
        
        # Produtos que precisam de reposição
        produtos_reposicao = []
        for produto in produtos_baixo_estoque:
            produtos_reposicao.append({
                'nome': produto.nome,
                'estoque_atual': produto.estoque,
                'estoque_minimo': produto.estoque_minimo,
                'categoria': produto.categoria.value
            })
        
        # Estoque por categoria
        estoque_por_categoria = defaultdict(lambda: {'quantidade': 0, 'valor': 0})
        for produto in produtos:
            categoria = produto.categoria.value
            estoque_por_categoria[categoria]['quantidade'] += produto.estoque
            estoque_por_categoria[categoria]['valor'] += produto.preco * produto.estoque
        
        return {
            'total_produtos': total_produtos,
            'valor_total_estoque': valor_total_estoque,
            'produtos_baixo_estoque': len(produtos_baixo_estoque),
            'produtos_reposicao': produtos_reposicao,
            'estoque_por_categoria': dict(estoque_por_categoria)
        }
    
    def relatorio_clientes(self) -> Dict[str, Any]:
        """
        Gera relatório de clientes.
        
        Returns:
            Dicionário com dados dos clientes
        """
        clientes = self.servico_cliente.listar_clientes()
        
        total_clientes = len(clientes)
        clientes_ativos = len([c for c in clientes if c.ativo])
        clientes_inativos = total_clientes - clientes_ativos
        
        # Clientes por tipo
        clientes_por_tipo = Counter(c.tipo.value for c in clientes)
        
        # Top clientes por valor de compras
        top_clientes = sorted(clientes, key=lambda c: c.total_compras, reverse=True)
        top_clientes_dados = []
        for cliente in top_clientes[:10]:
            top_clientes_dados.append({
                'nome': cliente.nome,
                'total_compras': cliente.total_compras,
                'numero_pedidos': cliente.numero_pedidos,
                'tipo': cliente.tipo.value
            })
        
        # Análise de atividade (últimos 30 dias)
        data_limite = datetime.now() - timedelta(days=30)
        pedidos_recentes = self.servico_pedido.listar_pedidos()
        clientes_ativos_recentes = set()
        
        for pedido in pedidos_recentes:
            if pedido.data_pedido >= data_limite:
                clientes_ativos_recentes.add(pedido.cliente_id)
        
        return {
            'total_clientes': total_clientes,
            'clientes_ativos': clientes_ativos,
            'clientes_inativos': clientes_inativos,
            'clientes_por_tipo': dict(clientes_por_tipo),
            'top_clientes': top_clientes_dados,
            'clientes_ativos_30_dias': len(clientes_ativos_recentes)
        }
    
    def relatorio_produtos_performance(self) -> Dict[str, Any]:
        """
        Gera relatório de performance de produtos.
        
        Returns:
            Dicionário com dados de performance
        """
        produtos = self.servico_produto.listar_produtos()
        pedidos = self.servico_pedido.listar_pedidos()
        
        # Calcular vendas por produto
        vendas_por_produto = defaultdict(lambda: {'quantidade': 0, 'receita': 0})
        
        for pedido in pedidos:
            if pedido.status != StatusPedido.CANCELADO:
                for item in pedido.itens:
                    produto_id = item.produto_id
                    vendas_por_produto[produto_id]['quantidade'] += item.quantidade
                    vendas_por_produto[produto_id]['receita'] += item.subtotal
        
        # Produtos mais vendidos
        produtos_performance = []
        for produto in produtos:
            vendas = vendas_por_produto[produto.id]
            produtos_performance.append({
                'nome': produto.nome,
                'categoria': produto.categoria.value,
                'quantidade_vendida': vendas['quantidade'],
                'receita_gerada': vendas['receita'],
                'estoque_atual': produto.estoque,
                'preco': produto.preco,
                'margem_estimada': vendas['receita'] * 0.3  # Assumindo 30% de margem
            })
        
        # Ordenar por receita
        produtos_performance.sort(key=lambda x: x['receita_gerada'], reverse=True)
        
        # Performance por categoria
        performance_categoria = defaultdict(lambda: {'receita': 0, 'quantidade': 0})
        for produto_perf in produtos_performance:
            categoria = produto_perf['categoria']
            performance_categoria[categoria]['receita'] += produto_perf['receita_gerada']
            performance_categoria[categoria]['quantidade'] += produto_perf['quantidade_vendida']
        
        return {
            'produtos_performance': produtos_performance,
            'performance_por_categoria': dict(performance_categoria),
            'total_produtos_analisados': len(produtos_performance)
        }
    
    def relatorio_financeiro(self, periodo_dias: int = 30) -> Dict[str, Any]:
        """
        Gera relatório financeiro para um período.
        
        Args:
            periodo_dias: Número de dias para análise
            
        Returns:
            Dicionário com dados financeiros
        """
        data_limite = datetime.now() - timedelta(days=periodo_dias)
        pedidos = self.servico_pedido.listar_pedidos()
        
        # Filtrar pedidos do período
        pedidos_periodo = [
            p for p in pedidos 
            if p.data_pedido >= data_limite and p.status != StatusPedido.CANCELADO
        ]
        
        # Calcular métricas financeiras
        receita_total = sum(p.total for p in pedidos_periodo)
        numero_transacoes = len(pedidos_periodo)
        ticket_medio = receita_total / numero_transacoes if numero_transacoes > 0 else 0
        
        # Receita por dia
        receita_por_dia = defaultdict(float)
        for pedido in pedidos_periodo:
            data_str = pedido.data_pedido.strftime('%Y-%m-%d')
            receita_por_dia[data_str] += pedido.total
        
        # Receita por categoria
        receita_por_categoria = defaultdict(float)
        for pedido in pedidos_periodo:
            for item in pedido.itens:
                produto = self.servico_produto.buscar_produto(item.produto_id)
                if produto:
                    receita_por_categoria[produto.categoria.value] += item.subtotal
        
        # Análise de crescimento (comparar com período anterior)
        data_limite_anterior = data_limite - timedelta(days=periodo_dias)
        pedidos_periodo_anterior = [
            p for p in pedidos 
            if data_limite_anterior <= p.data_pedido < data_limite and p.status != StatusPedido.CANCELADO
        ]
        
        receita_anterior = sum(p.total for p in pedidos_periodo_anterior)
        crescimento = ((receita_total - receita_anterior) / receita_anterior * 100) if receita_anterior > 0 else 0
        
        return {
            'periodo_dias': periodo_dias,
            'receita_total': receita_total,
            'numero_transacoes': numero_transacoes,
            'ticket_medio': ticket_medio,
            'receita_por_dia': dict(receita_por_dia),
            'receita_por_categoria': dict(receita_por_categoria),
            'crescimento_percentual': crescimento,
            'receita_periodo_anterior': receita_anterior
        }
    
    def dashboard_executivo(self) -> Dict[str, Any]:
        """
        Gera dados para dashboard executivo.
        
        Returns:
            Dicionário com KPIs principais
        """
        # Métricas dos últimos 30 dias
        relatorio_30_dias = self.relatorio_financeiro(30)
        relatorio_vendas = self.relatorio_vendas_periodo(
            datetime.now() - timedelta(days=30),
            datetime.now()
        )
        relatorio_estoque = self.relatorio_estoque()
        relatorio_clientes = self.relatorio_clientes()
        
        # KPIs principais
        kpis = {
            'receita_30_dias': relatorio_30_dias['receita_total'],
            'crescimento_receita': relatorio_30_dias['crescimento_percentual'],
            'ticket_medio': relatorio_30_dias['ticket_medio'],
            'total_pedidos': relatorio_vendas['quantidade_pedidos'],
            'total_clientes': relatorio_clientes['total_clientes'],
            'clientes_ativos_30_dias': relatorio_clientes['clientes_ativos_30_dias'],
            'valor_estoque': relatorio_estoque['valor_total_estoque'],
            'produtos_baixo_estoque': relatorio_estoque['produtos_baixo_estoque'],
            'top_produto': relatorio_vendas['produtos_mais_vendidos'][0] if relatorio_vendas['produtos_mais_vendidos'] else None
        }
        
        return {
            'kpis': kpis,
            'data_atualizacao': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'periodo_analise': '30 dias'
        }
    
    def exportar_relatorio_csv(self, tipo_relatorio: str, dados: Dict[str, Any], nome_arquivo: Optional[str] = None) -> str:
        """
        Exporta relatório para arquivo CSV.
        
        Args:
            tipo_relatorio: Tipo do relatório
            dados: Dados do relatório
            nome_arquivo: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo gerado
        """
        import csv
        from pathlib import Path
        
        if not nome_arquivo:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_arquivo = f"relatorio_{tipo_relatorio}_{timestamp}.csv"
        
        # Criar diretório de exports se não existir
        export_dir = Path(self.config.system.export_directory)
        export_dir.mkdir(exist_ok=True)
        
        caminho_arquivo = export_dir / nome_arquivo
        
        # Escrever dados no CSV baseado no tipo de relatório
        with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
            if tipo_relatorio == 'vendas':
                writer = csv.writer(csvfile)
                writer.writerow(['Produto', 'Quantidade Vendida'])
                for produto in dados.get('produtos_mais_vendidos', []):
                    writer.writerow([produto['produto'], produto['quantidade']])
            
            elif tipo_relatorio == 'estoque':
                writer = csv.writer(csvfile)
                writer.writerow(['Produto', 'Estoque Atual', 'Estoque Mínimo', 'Categoria'])
                for produto in dados.get('produtos_reposicao', []):
                    writer.writerow([
                        produto['nome'], 
                        produto['estoque_atual'], 
                        produto['estoque_minimo'],
                        produto['categoria']
                    ])
            
            elif tipo_relatorio == 'clientes':
                writer = csv.writer(csvfile)
                writer.writerow(['Cliente', 'Total Compras', 'Número Pedidos', 'Tipo'])
                for cliente in dados.get('top_clientes', []):
                    writer.writerow([
                        cliente['nome'],
                        cliente['total_compras'],
                        cliente['numero_pedidos'],
                        cliente['tipo']
                    ])
        
        return str(caminho_arquivo)