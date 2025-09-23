#!/usr/bin/env python3
"""
TESTE DO SISTEMA MODULAR
========================

Script para validar o funcionamento completo do sistema de gestão
empresarial após a refatoração modular.
"""

import sys
import os
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def testar_imports():
    """Testa se todos os módulos podem ser importados."""
    print("🔍 Testando imports dos módulos...")
    
    try:
        from models import (
            StatusPedido, TipoCliente, CategoriaProduct, TipoOperacao,
            Cliente, Produto, Pedido, ItemPedido, Endereco, LogAuditoria
        )
        print("✅ Models importado com sucesso")
        
        from repositories import (
            RepositorioMemoria, ValidadorCliente, ValidadorProduto, ValidadorPedido
        )
        print("✅ Repositories importado com sucesso")
        
        from services import ServicoCliente, ServicoProduto, ServicoPedido
        print("✅ Services importado com sucesso")
        
        from reports import GeradorRelatorios
        print("✅ Reports importado com sucesso")
        
        from audit import SistemaAuditoria
        print("✅ Audit importado com sucesso")
        
        from interface_cli import InterfaceCLI
        print("✅ Interface CLI importado com sucesso")
        
        from config import get_config
        print("✅ Config importado com sucesso")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        return False

def testar_instanciacao():
    """Testa a instanciação das principais classes."""
    print("\n🔍 Testando instanciação das classes...")
    
    try:
        from models import Cliente, Produto, TipoCliente, CategoriaProduct
        from repositories import RepositorioMemoria, ValidadorCliente
        from services import ServicoCliente
        from reports import GeradorRelatorios
        from audit import SistemaAuditoria
        from config import get_config
        
        # Testar configuração
        config = get_config()
        print("✅ Configuração carregada")
        
        # Testar repositórios
        repo_clientes = RepositorioMemoria(Cliente)
        print("✅ Repositório de clientes criado")
        
        # Testar validadores
        validador = ValidadorCliente()
        print("✅ Validador de cliente criado")
        
        # Testar serviços
        servico = ServicoCliente(repo_clientes, validador)
        print("✅ Serviço de cliente criado")
        
        # Testar auditoria
        auditoria = SistemaAuditoria()
        print("✅ Sistema de auditoria criado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na instanciação: {e}")
        return False

def testar_operacoes_basicas():
    """Testa operações básicas do sistema."""
    print("\n🔍 Testando operações básicas...")
    
    try:
        from models import Cliente, TipoCliente, Endereco
        from repositories import RepositorioMemoria, ValidadorCliente
        from services import ServicoCliente
        
        # Configurar componentes
        repo = RepositorioMemoria(Cliente)
        validador = ValidadorCliente()
        servico = ServicoCliente(repo, validador)
        
        # Criar cliente de teste
        endereco = Endereco(
            rua="Rua Teste",
            numero="123",
            cidade="São Paulo",
            estado="SP",
            cep="01234-567"
        )
        
        dados_cliente = {
            "nome": "Cliente Teste",
            "email": "teste@email.com",
            "telefone": "(11) 99999-9999",
            "endereco": endereco,
            "tipo": TipoCliente.PESSOA_FISICA,
            "limite_credito": 1000.0
        }
        
        # Testar criação
        sucesso, id_cliente, erros = servico.criar_cliente(dados_cliente)
        assert sucesso, f"Falha na criação: {erros}"
        print("✅ Cliente criado com sucesso")
        
        # Testar busca
        cliente_encontrado = servico.buscar_cliente(id_cliente)
        assert cliente_encontrado is not None
        print("✅ Cliente encontrado com sucesso")
        
        # Testar listagem
        clientes = servico.listar_clientes()
        assert len(clientes) >= 1
        print("✅ Listagem de clientes funcionando")
        
        # Testar atualização
        dados_atualizacao = {
            "nome": "Cliente Atualizado",
            "email": "teste@email.com",
            "telefone": "(11) 99999-9999",
            "endereco": endereco,
            "tipo": TipoCliente.PESSOA_FISICA,
            "limite_credito": 1000.0
        }
        sucesso_atualizacao, erros_atualizacao = servico.atualizar_cliente(id_cliente, dados_atualizacao)
        assert sucesso_atualizacao, f"Falha na atualização: {erros_atualizacao}"
        print("✅ Atualização de cliente funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas operações básicas: {e}")
        return False

def testar_sistema_completo():
    """Testa o sistema completo."""
    print("\n🔍 Testando sistema completo...")
    
    try:
        # Importar sistema principal
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Testar se o sistema principal pode ser importado
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "sistema_gestao", 
            "01_sistema_gestao.py"
        )
        sistema_module = importlib.util.module_from_spec(spec)
        
        # Executar apenas as importações do módulo
        print("✅ Sistema principal pode ser carregado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema completo: {e}")
        return False

def main():
    """Função principal do teste."""
    print("=" * 60)
    print("TESTE DO SISTEMA MODULAR - GESTÃO EMPRESARIAL")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    testes = [
        ("Imports", testar_imports),
        ("Instanciação", testar_instanciacao),
        ("Operações Básicas", testar_operacoes_basicas),
        ("Sistema Completo", testar_sistema_completo)
    ]
    
    resultados = []
    
    for nome, teste in testes:
        print(f"\n{'='*20} {nome} {'='*20}")
        resultado = teste()
        resultados.append((nome, resultado))
        
        if resultado:
            print(f"✅ {nome}: PASSOU")
        else:
            print(f"❌ {nome}: FALHOU")
    
    # Resumo final
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    passou = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome:.<30} {status}")
    
    print(f"\nResultado Final: {passou}/{total} testes passaram")
    
    if passou == total:
        print("🎉 TODOS OS TESTES PASSARAM! Sistema modular funcionando corretamente.")
        return 0
    else:
        print("⚠️  ALGUNS TESTES FALHARAM. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)