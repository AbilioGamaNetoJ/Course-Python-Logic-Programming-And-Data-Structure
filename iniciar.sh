#!/bin/bash

# Script de inicialização do Curso de Lógica de Programação
# Para Linux/Mac

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}========================================"
echo -e " CURSO DE LÓGICA DE PROGRAMAÇÃO"
echo -e " E ESTRUTURAS DE DADOS EM PYTHON"
echo -e "========================================${NC}"
echo ""
echo -e "${YELLOW}Iniciando o curso...${NC}"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}ERRO: Python não foi encontrado!${NC}"
        echo ""
        echo "Por favor, instale o Python 3.6+ e tente novamente."
        echo "Você pode instalar com:"
        echo "  Ubuntu/Debian: sudo apt install python3"
        echo "  macOS: brew install python3"
        echo "  Ou baixe em: https://python.org"
        echo ""
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Verificar versão do Python
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}Python $PYTHON_VERSION detectado${NC}"

# Tornar o script executável (caso não seja)
chmod +x "$0"

# Executar o script principal
echo -e "${YELLOW}Executando o curso...${NC}"
echo ""

$PYTHON_CMD executar_curso.py

# Mensagem final
echo ""
echo -e "${BLUE}Obrigado por usar o Curso de Lógica de Programação!${NC}"