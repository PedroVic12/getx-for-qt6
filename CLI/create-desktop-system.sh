#!/bin/bash

PROJECT_NAME="PolyglotDashboard"
echo "Construindo o novo ecossistema $PROJECT_NAME..."

mkdir -p $PROJECT_NAME/scripts
mkdir -p $PROJECT_NAME/ui/components
cd $PROJECT_NAME

# ==========================================
# 1. SCRIPTS ISOLADOS (C++, Julia, Lua)
# ==========================================
cat << 'EOF' > scripts/potencia.cpp
#include <iostream>
#include <cstdlib>

int main(int argc, char* argv[]) {
    std::cout << "==================================\n";
    std::cout << " C++ : CÁLCULO DE POTÊNCIA\n";
    std::cout << "==================================\n";

    if (argc > 1) {
        int tensao = std::atoi(argv[1]);
        int corrente = 15; // Fixo para exemplo
        int potencia = tensao * corrente;
        std::cout << "Tensão recebida: " << tensao << "V\n";
        std::cout << "Corrente: " << corrente << "A\n";
        std::cout << "-> Potência Máxima: " << potencia << " W\n";
    } else {
        std::cout << "Nenhum parâmetro de tensão recebido.\n";
    }
    return 0;
}
EOF
g++ scripts/potencia.cpp -o scripts/potencia.out

cat << 'EOF' > scripts/simulacao.jl
println("==================================")
println(" JULIA : SIMULAÇÃO DE SISTEMA")
println("==================================")

if length(ARGS) > 0
    valor = parse(Float64, ARGS[1])
    resultado = valor ^ 2.5
    println("Parâmetro de entrada: ", valor)
    println("-> Resultado da simulação: ", round(resultado, digits=2))
else
    println("Nenhum dado recebido.")
end
EOF

cat << 'EOF' > scripts/regras.lua
print("==================================")
print(" LUA : MOTOR DE REGRAS E XP")
print("==================================")

local args = {...}
if #args > 0 then
    local usuario = args[1]
    print("Iniciando rotina diária para o usuário: " .. usuario)
    print("-> Status: XP Atualizado com Sucesso! +50pts")
else
    print("Executado sem parâmetros.")
end
EOF

# ==========================================
# 2. BACKEND PYTHON (backend.py)
# ==========================================
cat << 'EOF' > backend.py
import subprocess
import os
from PySide6.QtCore import QObject, Slot

class ProcessManager(QObject):
    @Slot(str, str, str)
    def executar_no_terminal(self, linguagem, arquivo, parametro):
        """
        Abre o Konsole (terminal padrão) e executa o script selecionado.
        A flag bash -c garante que a janela não feche após a execução.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(base_dir, "scripts", arquivo)

        # Monta o comando de acordo com a linguagem
        if linguagem == "cpp":
            cmd = f"{script_path} {parametro}"
        elif linguagem == "julia":
            cmd = f"julia {script_path} {parametro}"
        elif linguagem == "lua":
            cmd = f"lua {script_path} {parametro}"
        else:
            return

        # Comando final que segura o terminal aberto
        hold_terminal = f'{cmd}; echo ""; read -p "Pressione ENTER para fechar..."'

        try:
            # Chama o konsole passando o comando encapsulado no bash
            subprocess.Popen(['konsole', '-e', 'bash', '-c', hold_terminal])
        except Exception as e:
            print(f"Erro ao abrir o terminal: {e}")
EOF

# ==========================================
# 3. INTERFACE QML - COMPONENTE CARD (ui/components/CardBotao.qml)
# ==========================================
cat << 'EOF' > ui/components/CardBotao.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Button {
    id: control
    property string titulo: "Título"
    property string subtitulo: "Subtítulo"
    property string icone: "⚙️"
    property color corDestaque: "#cba6f7"

    Layout.fillWidth: true
    Layout.preferredHeight: 90

    background: Rectangle {
        color: control.down ? "#313244" : (control.hovered ? "#45475a" : "#1e1e2e")
        radius: 12
        border.color: control.hovered ? control.corDestaque : "#313244"
        border.width: 1

        // Sombra sutil (simulada)
        Rectangle {
            anchors.fill: parent
            anchors.topMargin: 2
            z: -1
            color: "#11111b"
            radius: 12
        }
    }

    contentItem: RowLayout {
        spacing: 15
        anchors.fill: parent
        anchors.margins: 15

        Text {
            text: control.icone
            font.pixelSize: 32
            Layout.alignment: Qt.AlignVCenter
        }

        ColumnLayout {
            spacing: 4
            Layout.fillWidth: true

            Text {
                text: control.titulo
                color: "#cdd6f4"
                font.pixelSize: 16
                font.bold: true
            }
            Text {
                text: control.subtitulo
                color: "#a6adc8"
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
            }
        }

        Text {
            text: "▶"
            color: control.corDestaque
            font.pixelSize: 18
            Layout.alignment: Qt.AlignVCenter
            opacity: control.hovered ? 1.0 : 0.3
        }
    }
}
EOF

# ==========================================
# 4. INTERFACE QML - TELA PRINCIPAL (ui/main.qml)
# ==========================================
cat << 'EOF' > ui/main.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components"

ApplicationWindow {
    id: window
    visible: true
    width: 420
    height: 700
    title: "Dashboard Poliglota"
    color: "#11111b"

    // MENU LATERAL (DRAWER)
    Drawer {
        id: drawer
        width: window.width * 0.7
        height: window.height

        background: Rectangle { color: "#181825" }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 15

            Text {
                text: "Menu Principal"
                color: "#cba6f7"
                font.pixelSize: 22
                font.bold: true
                Layout.bottomMargin: 20
            }

            Button {
                text: "🏠 Início"
                Layout.fillWidth: true
                onClicked: drawer.close()
            }
            Button {
                text: "⚙️ Configurações"
                Layout.fillWidth: true
            }

            Item { Layout.fillHeight: true } // Espaçador

            Text {
                text: "Versão 2.0"
                color: "#45475a"
                font.pixelSize: 12
            }
        }
    }

    // CABEÇALHO MOBILE
    header: ToolBar {
        background: Rectangle { color: "#181825" }
        RowLayout {
            anchors.fill: parent
            ToolButton {
                text: "☰" // Ícone Hamburger
                font.pixelSize: 20
                onClicked: drawer.open()
            }
            Label {
                text: "Central de Execução"
                font.pixelSize: 18
                color: "#cdd6f4"
                horizontalAlignment: Qt.AlignHCenter
                Layout.fillWidth: true
            }
            Item { Layout.preferredWidth: 40 } // Balanço de layout
        }
    }

    // CONTEÚDO PRINCIPAL (LISTA DE CARDS)
    ScrollView {
        anchors.fill: parent
        anchors.margins: 15
        clip: true

        ColumnLayout {
            width: parent.width
            spacing: 12

            Text {
                text: "Scripts Disponíveis"
                color: "#a6adc8"
                font.pixelSize: 14
                Layout.bottomMargin: 5
            }

            CardBotao {
                titulo: "Processar Tensão (C++)"
                subtitulo: "Abre o terminal e executa o binário otimizado."
                icone: "⚡"
                corDestaque: "#f38ba8" // Vermelho
                onClicked: backend.executar_no_terminal("cpp", "potencia.out", "220")
            }

            CardBotao {
                titulo: "Simulação de Sistemas (Julia)"
                subtitulo: "Invoca o modelo matemático no Konsole."
                icone: "📈"
                corDestaque: "#a6e3a1" // Verde
                onClicked: backend.executar_no_terminal("julia", "simulacao.jl", "42.5")
            }

            CardBotao {
                titulo: "Atualizar Regras Diárias (Lua)"
                subtitulo: "Executa script rápido de sistema de recompensa."
                icone: "🎮"
                corDestaque: "#89b4fa" // Azul
                onClicked: backend.executar_no_terminal("lua", "regras.lua", "Pedro_Victor")
            }

            CardBotao {
                titulo: "Relatório Rápido (Python)"
                subtitulo: "Apenas um exemplo de card extra na interface."
                icone: "🐍"
                corDestaque: "#f9e2af" // Amarelo
            }
        }
    }
}
EOF

# ==========================================
# 5. PONTO DE ENTRADA (main.py)
# ==========================================
cat << 'EOF' > main.py
import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from backend import ProcessManager

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Registra o backend para o QML
    backend = ProcessManager()
    engine.rootContext().setContextProperty("backend", backend)

    # Carrega a interface
    qml_file = os.path.join(os.path.dirname(__file__), "ui", "main.qml")
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
EOF

echo "Interface refatorada para Mobile-First e Cards criada!"
echo "Para executar: cd $PROJECT_NAME && python main.py"
