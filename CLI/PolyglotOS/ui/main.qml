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
