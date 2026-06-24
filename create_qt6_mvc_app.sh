#!/bin/bash

# Se o primeiro argumento ($1) estiver vazio, pede o input do usuário
if [ -z "$1" ]; then
    read -p "📂 Digite o nome do projeto: " PROJECT_NAME
else
    PROJECT_NAME=$1
fi

PROJECT_NAME=${PROJECT_NAME:-"qt6_app"}

# Seleção de Template
TEMPLATE_TYPE=$2
if [ -z "$TEMPLATE_TYPE" ]; then
    echo "==========================================="
    echo "🌟 Selecione o Template de Projeto para Qt6:"
    echo "==========================================="
    echo "1) PySide6 MVC (Widgets) - [Padrão/Elite]"
    echo "2) PySide6 Qt Quick (QML)"
    echo "3) PySide6 Qt Designer (.ui)"
    echo "4) C++ Qt Quick (QML + CMake)"
    echo "5) C++ Qt Widgets (.ui + CMake)"
    echo "==========================================="
    read -p "Digite a opção (1-5) [1]: " TEMPLATE_TYPE
fi

TEMPLATE_TYPE=${TEMPLATE_TYPE:-"1"}

# Obtém a pasta onde o script está localizado
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python3 "$DIR/generator.py" "$PROJECT_NAME" "$TEMPLATE_TYPE"
