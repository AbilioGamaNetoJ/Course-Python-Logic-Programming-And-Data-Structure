#!/usr/bin/env python3
"""
Script Principal do Curso de Lógica de Programação e Estruturas de Dados

Este script facilita a execução de todos os módulos e funcionalidades do curso
sem a necessidade de comandos complexos no terminal.

Autor: Professor de Lógica de Programação
Data: 2024
"""

import os
import sys
import importlib.util
from pathlib import Path

# Adicionar o diretório atual ao path do Python
CURSO_DIR = Path(__file__).parent
sys.path.insert(0, str(CURSO_DIR))

def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_banner():
    """Exibe o banner do curso."""
    print("=" * 80)
    print("🐍 CURSO COMPLETO DE LÓGICA DE PROGRAMAÇÃO E ESTRUTURAS DE DADOS")
    print("=" * 80)
    print("📚 Professor de Lógica de Programação")
    print("🎯 Versão: 1.0.0 | Ano: 2024")
    print("=" * 80)
    print()

def listar_modulos():
    """Lista todos os módulos disponíveis no curso."""
    modulos = {
        "1": {
            "nome": "Fundamentos de Lógica",
            "pasta": "01_fundamentos_logica",
            "descricao": "Introdução ao Python, tipos de dados, operadores e estruturas básicas"
        },
        "2": {
            "nome": "Estruturas de Dados Nativas",
            "pasta": "02_estruturas_dados_nativas", 
            "descricao": "Listas, tuplas, dicionários, conjuntos e manipulação de strings"
        },
        "3": {
            "nome": "Algoritmos de Busca e Ordenação",
            "pasta": "03_algoritmos_busca_ordenacao",
            "descricao": "Algoritmos fundamentais de busca e ordenação com análise comparativa"
        },
        "4": {
            "nome": "Estruturas de Dados Lineares",
            "pasta": "04_estruturas_dados_lineares",
            "descricao": "Pilhas, filas, listas ligadas e suas aplicações práticas"
        },
        "5": {
            "nome": "Estruturas de Dados Não-Lineares",
            "pasta": "05_estruturas_dados_nao_lineares",
            "descricao": "Árvores, grafos, heaps e estruturas hierárquicas"
        },
        "6": {
            "nome": "Algoritmos Avançados",
            "pasta": "06_algoritmos_avancados",
            "descricao": "Programação dinâmica, algoritmos gulosos e técnicas avançadas"
        },
        "7": {
            "nome": "Análise de Complexidade",
            "pasta": "07_analise_complexidade",
            "descricao": "Notação Big O, análise de performance e otimização"
        },
        "8": {
            "nome": "Projetos Práticos",
            "pasta": "08_projetos_praticos",
            "descricao": "Projetos integrados aplicando todos os conceitos aprendidos"
        }
    }
    
    print("📋 MÓDULOS DISPONÍVEIS:")
    print()
    for num, info in modulos.items():
        print(f"{num}. {info['nome']}")
        print(f"   📁 {info['pasta']}")
        print(f"   📝 {info['descricao']}")
        print()
    
    return modulos

def listar_arquivos_modulo(pasta_modulo):
    """Lista os arquivos disponíveis em um módulo específico."""
    caminho_modulo = CURSO_DIR / pasta_modulo
    
    if not caminho_modulo.exists():
        print(f"❌ Módulo '{pasta_modulo}' não encontrado!")
        return []
    
    arquivos_py = list(caminho_modulo.glob("*.py"))
    arquivos_py.sort()
    
    print(f"📁 ARQUIVOS DO MÓDULO '{pasta_modulo.upper()}':")
    print()
    
    arquivos_info = []
    for i, arquivo in enumerate(arquivos_py, 1):
        nome_arquivo = arquivo.name
        print(f"{i}. {nome_arquivo}")
        arquivos_info.append(arquivo)
    
    print()
    return arquivos_info

def executar_arquivo(caminho_arquivo):
    """Executa um arquivo Python específico."""
    import subprocess
    
    try:
        print(f"🚀 Executando: {caminho_arquivo.name}")
        print("=" * 60)
        
        # Executar o arquivo usando subprocess para mostrar a saída
        resultado = subprocess.run(
            [sys.executable, str(caminho_arquivo)],
            capture_output=False,  # Não capturar saída, deixar aparecer no terminal
            text=True,
            cwd=str(caminho_arquivo.parent)
        )
        
        print("=" * 60)
        if resultado.returncode == 0:
            print("✅ Execução concluída com sucesso!")
        else:
            print(f"⚠️ Execução finalizada com código: {resultado.returncode}")
        
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        print("💡 Verifique se o arquivo está correto e tente novamente.")

def testar_utils():
    """Testa o pacote utils."""
    try:
        print("🧪 TESTANDO PACOTE UTILS:")
        print("=" * 40)
        
        # Importar utils
        import utils
        
        # Testar algumas funcionalidades básicas
        from utils.helpers import formatar_tempo, gerar_lista_aleatoria
        from utils.constants import TAMANHOS_TESTE
        from utils.decorators import medir_tempo
        
        print("✅ Imports realizados com sucesso!")
        
        # Teste básico
        lista_teste = gerar_lista_aleatoria(10)
        print(f"📊 Lista gerada: {lista_teste}")
        
        tempo_formatado = formatar_tempo(0.001234)
        print(f"⏱️  Tempo formatado: {tempo_formatado}")
        
        print(f"📏 Tamanhos de teste: {TAMANHOS_TESTE}")
        
        print("=" * 40)
        print("✅ Pacote utils funcionando corretamente!")
        
    except Exception as e:
        print(f"❌ Erro no teste do utils: {e}")
        print("💡 Verifique se todos os arquivos do utils estão corretos.")

def executar_projeto_integrador():
    """Executa o projeto integrador final."""
    try:
        print("🎯 EXECUTANDO PROJETO INTEGRADOR FINAL:")
        print("=" * 50)
        
        caminho_integrador = CURSO_DIR / "08_projetos_praticos" / "05_projeto_integrador.py"
        
        if caminho_integrador.exists():
            executar_arquivo(caminho_integrador)
        else:
            print("❌ Projeto integrador não encontrado!")
            
    except Exception as e:
        print(f"❌ Erro na execução do projeto integrador: {e}")

def executar_demonstracao_completa():
    """Executa a demonstração completa de todos os testes."""
    try:
        print("🧪 EXECUTANDO DEMONSTRAÇÃO COMPLETA:")
        print("=" * 50)
        
        caminho_demo = CURSO_DIR / "08_projetos_praticos" / "06_demonstracao_testes.py"
        
        if caminho_demo.exists():
            executar_arquivo(caminho_demo)
        else:
            print("❌ Demonstração de testes não encontrada!")
            
    except Exception as e:
        print(f"❌ Erro na execução da demonstração: {e}")

def menu_principal():
    """Exibe o menu principal do curso."""
    while True:
        limpar_tela()
        exibir_banner()
        
        print("🎯 MENU PRINCIPAL:")
        print()
        print("1. 📚 Explorar Módulos do Curso")
        print("2. 🧪 Testar Pacote Utils")
        print("3. 🎯 Executar Projeto Integrador")
        print("4. 🧪 Demonstração Completa")
        print("5. 📖 Sobre o Curso")
        print("0. 🚪 Sair")
        print()
        
        opcao = input("👉 Escolha uma opção: ").strip()
        
        if opcao == "1":
            menu_modulos()
        elif opcao == "2":
            input("\n👉 Pressione Enter para continuar...")
            testar_utils()
            input("\n👉 Pressione Enter para voltar ao menu...")
        elif opcao == "3":
            input("\n👉 Pressione Enter para continuar...")
            executar_projeto_integrador()
            input("\n👉 Pressione Enter para voltar ao menu...")
        elif opcao == "4":
            input("\n👉 Pressione Enter para continuar...")
            executar_demonstracao_completa()
            input("\n👉 Pressione Enter para voltar ao menu...")
        elif opcao == "5":
            mostrar_sobre()
        elif opcao == "0":
            print("\n👋 Obrigado por usar o Curso de Lógica de Programação!")
            print("🎓 Continue praticando e evoluindo seus conhecimentos!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")
            input("👉 Pressione Enter para continuar...")

def menu_modulos():
    """Menu para explorar os módulos do curso."""
    while True:
        limpar_tela()
        exibir_banner()
        
        modulos = listar_modulos()
        
        print("0. 🔙 Voltar ao Menu Principal")
        print()
        
        opcao = input("👉 Escolha um módulo (0-8): ").strip()
        
        if opcao == "0":
            break
        elif opcao in modulos:
            menu_arquivos_modulo(modulos[opcao])
        else:
            print("❌ Opção inválida! Tente novamente.")
            input("👉 Pressione Enter para continuar...")

def menu_arquivos_modulo(info_modulo):
    """Menu para explorar arquivos de um módulo específico."""
    while True:
        limpar_tela()
        exibir_banner()
        
        print(f"📁 MÓDULO: {info_modulo['nome']}")
        print(f"📝 {info_modulo['descricao']}")
        print()
        
        arquivos = listar_arquivos_modulo(info_modulo['pasta'])
        
        if not arquivos:
            print("❌ Nenhum arquivo encontrado neste módulo!")
            input("👉 Pressione Enter para voltar...")
            break
        
        print("0. 🔙 Voltar aos Módulos")
        print()
        
        opcao = input("👉 Escolha um arquivo para executar (0-{}): ".format(len(arquivos))).strip()
        
        if opcao == "0":
            break
        
        try:
            indice = int(opcao) - 1
            if 0 <= indice < len(arquivos):
                input("\n👉 Pressione Enter para executar...")
                limpar_tela()
                executar_arquivo(arquivos[indice])
                input("\n👉 Pressione Enter para voltar...")
            else:
                print("❌ Número inválido!")
                input("👉 Pressione Enter para continuar...")
        except ValueError:
            print("❌ Digite apenas números!")
            input("👉 Pressione Enter para continuar...")

def mostrar_sobre():
    """Mostra informações sobre o curso."""
    limpar_tela()
    exibir_banner()
    
    print("📖 SOBRE O CURSO:")
    print()
    print("🎯 Este é um curso completo de Lógica de Programação e Estruturas de Dados")
    print("   desenvolvido em Python, cobrindo desde conceitos básicos até projetos avançados.")
    print()
    print("📚 CONTEÚDO ABORDADO:")
    print("   • Fundamentos de programação e lógica")
    print("   • Estruturas de dados nativas do Python")
    print("   • Algoritmos de busca e ordenação")
    print("   • Estruturas de dados lineares e não-lineares")
    print("   • Algoritmos avançados e técnicas de otimização")
    print("   • Análise de complexidade e performance")
    print("   • Projetos práticos integrados")
    print()
    print("🛠️ FERRAMENTAS INCLUÍDAS:")
    print("   • Pacote utils com funções auxiliares")
    print("   • Decoradores para análise de performance")
    print("   • Validadores especializados")
    print("   • Ferramentas de benchmark e profiling")
    print()
    print("🎓 OBJETIVO:")
    print("   Desenvolver raciocínio lógico sólido e domínio completo de")
    print("   estruturas de dados e algoritmos fundamentais.")
    print()
    
    input("👉 Pressione Enter para voltar ao menu...")

def verificar_ambiente():
    """Verifica se o ambiente está configurado corretamente."""
    print("🔍 Verificando ambiente...")
    
    # Verificar versão do Python
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ é necessário!")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detectado")
    
    # Verificar estrutura de pastas
    pastas_necessarias = [
        "01_fundamentos_logica",
        "02_estruturas_dados_nativas", 
        "03_algoritmos_busca_ordenacao",
        "04_estruturas_dados_lineares",
        "05_estruturas_dados_nao_lineares",
        "06_algoritmos_avancados",
        "07_analise_complexidade",
        "08_projetos_praticos",
        "utils"
    ]
    
    for pasta in pastas_necessarias:
        if not (CURSO_DIR / pasta).exists():
            print(f"❌ Pasta '{pasta}' não encontrada!")
            return False
    
    print("✅ Estrutura de pastas verificada")
    
    # Verificar pacote utils
    try:
        import utils
        print("✅ Pacote utils carregado com sucesso")
        
        # Verificar se todos os módulos utils estão funcionando
        modulos_utils = ['helpers', 'constants', 'decorators', 'validators', 'performance']
        modulos_ok = []
        modulos_erro = []
        
        for modulo in modulos_utils:
            try:
                getattr(utils, modulo)
                modulos_ok.append(modulo)
            except AttributeError:
                modulos_erro.append(modulo)
        
        if modulos_erro:
            print(f"⚠️  Alguns módulos utils com problemas: {', '.join(modulos_erro)}")
            print("💡 Funcionalidade pode estar limitada")
        else:
            print("✅ Todos os módulos utils funcionando corretamente")
            
    except ImportError as e:
        print(f"❌ Erro ao carregar pacote utils: {e}")
        print("⚠️  Funcionalidade limitada - alguns recursos podem não funcionar")
        print("💡 Execute 'pip install -r requirements.txt' para resolver dependências")
    
    return True

if __name__ == "__main__":
    try:
        # Verificar ambiente
        if not verificar_ambiente():
            print("\n❌ Ambiente não está configurado corretamente!")
            print("💡 Verifique se todos os arquivos estão presentes.")
            input("👉 Pressione Enter para sair...")
            sys.exit(1)
        
        print("✅ Ambiente verificado com sucesso!")
        input("\n👉 Pressione Enter para iniciar o curso...")
        
        # Iniciar menu principal
        menu_principal()
        
    except KeyboardInterrupt:
        print("\n\n👋 Curso interrompido pelo usuário. Até logo!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("💡 Contate o suporte se o problema persistir.")
        input("👉 Pressione Enter para sair...")