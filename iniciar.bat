@echo off
title Curso de Logica de Programacao e Estruturas de Dados
color 0A

echo.
echo ========================================
echo  CURSO DE LOGICA DE PROGRAMACAO
echo  E ESTRUTURAS DE DADOS EM PYTHON
echo ========================================
echo.
echo Iniciando o curso...
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao foi encontrado!
    echo.
    echo Por favor, instale o Python 3.6+ e tente novamente.
    echo Voce pode baixar em: https://python.org
    echo.
    pause
    exit /b 1
)

REM Executar o script principal
python executar_curso.py

REM Pausar no final para ver mensagens
echo.
pause