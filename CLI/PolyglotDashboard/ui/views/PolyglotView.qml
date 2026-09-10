import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

ScrollView {
    id: root
    contentWidth: availableWidth
    clip: true

    ColumnLayout {
        width: parent.width
        spacing: 16

        Text {
            text: "🚀 Central de Execução Poliglota (Algoritmos do Dia a Dia)"
            color: "#cdd6f4"
            font.pixelSize: 18
            font.bold: true
            Layout.topMargin: 5
        }

        Text {
            text: "Selecione um algoritmo para executar em terminal Linux independente ou capturar a saída:"
            color: "#a6adc8"
            font.pixelSize: 12
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }

        // --- C++ Card ---
        CardBotao {
            Layout.fillWidth: true
            titulo: "⚡ Análise de Potência AC & Triângulo S, P, Q (C++)"
            subtitulo: "Engenharia Elétrica UFF: Tensão RMS, Corrente, Potência Reativa e Capacitância µF."
            icone: "⚡"
            corDestaque: "#f38ba8"
            onClicked: appController.run_polyglot_terminal("cpp", "potencia_circuito.out", "220 15 30")
        }

        // --- Julia Card ---
        CardBotao {
            Layout.fillWidth: true
            titulo: "📈 EDO de Circuito RLC 2ª Ordem (Julia)"
            subtitulo: "Resolução analítica/numérica: Frequência natural ω₀, amortecimento α e raízes s₁, s₂."
            icone: "📈"
            corDestaque: "#a6e3a1"
            onClicked: appController.run_polyglot_terminal("julia", "analise_edo_circuito.jl", "10 0.1 0.0001")
        }

        // --- Lua Card ---
        CardBotao {
            Layout.fillWidth: true
            titulo: "🎮 Regras de Rotina Diária & WIP Post-it (Lua)"
            subtitulo: "Ecossistema Batcaverna 2026: Verificação de metas diárias e limitação de frentes abertas."
            icone: "🎮"
            corDestaque: "#89b4fa"
            onClicked: appController.run_polyglot_terminal("lua", "rotina_pomodoro.lua", "Pedro_Victor 5 3")
        }

        // --- C Card ---
        CardBotao {
            Layout.fillWidth: true
            titulo: "⚙️ Simulação de Fila de Eventos & Buffer ONS (C)"
            subtitulo: "Sistemas de Automação: Fila de despacho de manobras e taxa de overflow."
            icone: "⚙️"
            corDestaque: "#fab387"
            onClicked: appController.run_polyglot_terminal("c", "filas_atendimento_sim.out", "150")
        }

        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: "#313244"
            Layout.topMargin: 10
            Layout.bottomMargin: 10
        }

        Text {
            text: "💬 Console Log / Saída de Script Direct (Inline Output):"
            color: "#a6adc8"
            font.pixelSize: 13
            font.bold: true
        }

        RowLayout {
            spacing: 10
            Layout.fillWidth: true

            ModernButton {
                text: "▶ Executar C++ (Inline)"
                bgCor: "#f38ba8"
                onClicked: consoleArea.text = appController.run_polyglot_inline("cpp", "potencia_circuito.out", "220 18 35")
            }

            ModernButton {
                text: "▶ Executar Julia (Inline)"
                bgCor: "#a6e3a1"
                onClicked: consoleArea.text = appController.run_polyglot_inline("julia", "analise_edo_circuito.jl", "5 0.05 0.0002")
            }
        }

        Rectangle {
            Layout.fillWidth: true
            implicitHeight: 180
            color: "#11111b"
            radius: 8
            border.color: "#313244"

            ScrollView {
                anchors.fill: parent
                anchors.margins: 10
                clip: true

                TextArea {
                    id: consoleArea
                    readOnly: true
                    color: "#a6e3a1"
                    font.family: "Monospace"
                    font.pixelSize: 11
                    placeholderText: "Saída de execução direta aparecerá aqui..."
                    wrapMode: Text.Wrap
                }
            }
        }
    }
}
