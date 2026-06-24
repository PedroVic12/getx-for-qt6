@echo off
setlocal enabledelayedexpansion

if "%~1"=="" (
    set /p PROJECT_NAME="📂 Digite o nome do projeto [qt6_app]: "
) else (
    set PROJECT_NAME=%~1
)

if "%PROJECT_NAME%"=="" set PROJECT_NAME=qt6_app

set TEMPLATE_TYPE=%~2
if "%TEMPLATE_TYPE%"=="" (
    echo ===========================================
    echo 🌟 Selecione o Template de Projeto para Qt6:
    echo ===========================================
    echo 1] PySide6 MVC [Widgets] - [Padrao/Elite]
    echo 2] PySide6 Qt Quick [QML]
    echo 3] PySide6 Qt Designer [.ui]
    echo 4] C++ Qt Quick [QML + CMake]
    echo 5] C++ Qt Widgets [.ui + CMake]
    echo ===========================================
    set /p TEMPLATE_TYPE="Digite a opcao (1-5) [1]: "
)
if "%TEMPLATE_TYPE%"=="" set TEMPLATE_TYPE=1

python "%~dp0generator.py" "%PROJECT_NAME%" "%TEMPLATE_TYPE%"
