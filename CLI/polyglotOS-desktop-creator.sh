#!/bin/bash

PROJECT_NAME="PolyglotOS"
echo "Construindo o ecossistema poliglota $PROJECT_NAME..."
mkdir -p $PROJECT_NAME/core
mkdir -p $PROJECT_NAME/ui
cd $PROJECT_NAME

# ==========================================
# 1. C++ (Motor de Alta Performance)
# ==========================================
cat << 'EOF' > core/algoritmo.cpp
#include <iostream>

// extern "C" impede o name mangling do C++ para o Python conseguir ler
extern "C" {
    int calcular_potencia_maxima(int tensao, int corrente) {
        // Simulação de um cálculo pesado em C++
        return tensao * corrente;
    }
}
EOF
# Compila o C++ para uma biblioteca compartilhada (.so) no Linux
g++ -shared -fPIC -o core/libalgoritmo.so core/algoritmo.cpp
echo "Biblioteca C++ compilada com sucesso."

# ==========================================
# 2. Julia (Cálculos Científicos)
# ==========================================
cat << 'EOF' > core/simulacao.jl
# Recebe argumentos do terminal enviados pelo Python
if length(ARGS) > 0
    valor = parse(Float64, ARGS[1])
    resultado = valor ^ 2.5 # Cálculo científico hipotético
    println("Julia processou o valor: ", round(resultado, digits=2))
else
    println("Nenhum dado recebido pelo Julia.")
end
EOF

# ==========================================
# 3. Lua (Scripts Rápidos / Regras)
# ==========================================
cat << 'EOF' > core/regras.lua
-- Script Lua chamado pelo Python
local args = {...}
if #args > 0 then
    local usuario = args[1]
    print("Lua diz: Bem-vindo ao sistema de XP, " .. usuario .. "!")
else
    print("Lua executou com sucesso, mas sem argumentos.")
end
EOF

# ==========================================
# 4. Python (O Maestro / Backend)
# ==========================================
cat << 'EOF' > app.py
import subprocess
import ctypes
import os
from PySide6.QtCore import QObject, Slot

class PolyglotBackend(QObject):
    def __init__(self):
        super().__init__()
        # Carrega a biblioteca C++ compilada
        base_dir = os.path.dirname(os.path.abspath(__file__))
        lib_path = os.path.join(base_dir, "core", "libalgoritmo.so")
        self.cpp_lib = ctypes.CDLL(lib_path)
    
    @Slot(int, int, result=str)
    def run_cpp(self, tensao, corrente):
        # Executa a função em C++ diretamente na memória
        resultado = self.cpp_lib.calcular_potencia_maxima(tensao, corrente)
        return f"C++ retornou a potência: {resultado} W"

    @Slot(str, result=str)
    def run_julia(self, valor):
        # Executa o script Julia via subprocesso
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(base_dir, "core", "simulacao.jl")
        result = subprocess.run(["julia", script, valor], capture_output=True, text=True)
        return result.stdout.strip()

    @Slot(str, result=str)
    def run_lua(self, nome):
        # Executa o script Lua via subprocesso
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(base_dir, "core", "regras.lua")
        result = subprocess.run(["lua", script, nome], capture_output=True, text=True)
        return result.stdout.strip()
EOF

cat << 'EOF' > main.py
import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from app import PolyglotBackend

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Registra o backend Python/C++/Julia/Lua no QML
    backend = PolyglotBackend()
    engine.rootContext().setContextProperty("backend", backend)
    
    qml_file = os.path.join(os.path.dirname(__file__), "ui", "main.qml")
    engine.load(qml_file)
    
    if not engine.rootObjects():
        sys.exit(-1)
        
    sys.exit(app.exec())
EOF

# ==========================================
# 5. QML + JavaScript (Interface Dinâmica)
# ==========================================
cat << 'EOF' > ui/main.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 500
    height: 600
    title: "Polyglot OS - 5 Linguagens"
    color: "#1e1e2e"

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20

        Label {
            id: displayResultado
            text: "Aguardando execução..."
            color: "#cdd6f4"
            font.pixelSize: 16
            Layout.alignment: Qt.AlignHCenter
            wrapMode: Text.WordWrap
            Layout.maximumWidth: 400
        }

        // Botão 1: Chama C++ via Python
        Button {
            text: "1. Executar C++ (Cálculo de Potência)"
            Layout.fillWidth: true
            onClicked: {
                // Chama C++ com parâmetros 220 (Tensão) e 15 (Corrente)
                displayResultado.text = backend.run_cpp(220, 15)
                displayResultado.color = "#f38ba8" // Vermelho
            }
        }

        // Botão 2: Chama Julia via Python
        Button {
            text: "2. Executar Julia (Simulação)"
            Layout.fillWidth: true
            onClicked: {
                displayResultado.text = backend.run_julia("42.5")
                displayResultado.color = "#a6e3a1" // Verde
            }
        }

        // Botão 3: Chama Lua via Python
        Button {
            text: "3. Executar Lua (Regras de XP)"
            Layout.fillWidth: true
            onClicked: {
                displayResultado.text = backend.run_lua("Pedro")
                displayResultado.color = "#89b4fa" // Azul
            }
        }

        // Botão 4: Executa JavaScript nativo no QML
        Button {
            text: "4. Executar JavaScript (UI Logic)"
            Layout.fillWidth: true
            onClicked: {
                // Lógica JS embutida no frontend
                let data = new Date();
                let hora = data.toLocaleTimeString();
                displayResultado.text = "JS processou a UI localmente às: " + hora;
                displayResultado.color = "#f9e2af" // Amarelo
            }
        }
    }
}
EOF

echo "Projeto Poliglota criado com sucesso!"
echo "Para executar, certifique-se de ter julia e lua instalados no Arch Linux (sudo pacman -S julia lua)"
echo "Rode com: cd $PROJECT_NAME && python main.py"


