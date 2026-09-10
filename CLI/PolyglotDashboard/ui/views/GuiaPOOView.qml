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
            text: "📖 Guia Poliglota: POO, QML & Matemática Aplicada"
            color: "#cdd6f4"
            font.pixelSize: 18
            font.bold: true
            Layout.topMargin: 5
        }

        Text {
            text: "Acompanhe seu progresso de estudo em C++, Python, Julia e Lua, e teste scripts de matemática aplicada diretamente pela interface:"
            color: "#a6adc8"
            font.pixelSize: 12
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }

        // --- CHECKLIST DE ESTUDOS POO ---
        Rectangle {
            Layout.fillWidth: true
            implicitHeight: checklistColumn.implicitHeight + 30
            color: "#181825"
            radius: 12
            border.color: "#cba6f7"
            border.width: 1.5

            ColumnLayout {
                id: checklistColumn
                anchors.fill: parent
                anchors.margins: 15
                spacing: 8

                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "🎯 Checklist de Aprendizado POO Poliglota"
                        color: "#cba6f7"
                        font.pixelSize: 14
                        font.bold: true
                    }
                    Item { Layout.fillWidth: true }
                    Text {
                        text: "Guia: guia_poo_poliglota.qmd"
                        color: "#a6adc8"
                        font.pixelSize: 11
                    }
                }

                Repeater {
                    model: appController ? appController.get_poo_checklist() : []

                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: 44
                        color: modelData.concluido ? "#1e2030" : "#1e1e2e"
                        radius: 8
                        border.color: modelData.concluido ? "#a6e3a1" : "#313244"

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 8
                            spacing: 10

                            CheckBox {
                                checked: modelData.concluido
                                onCheckedChanged: appController.toggle_poo_topic(index)
                            }

                            Text {
                                text: modelData.modulo + ": " + modelData.titulo
                                color: modelData.concluido ? "#a6e3a1" : "#cdd6f4"
                                font.pixelSize: 12
                                font.strikeout: modelData.concluido
                                font.bold: true
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }
                        }
                    }
                }
            }
        }

        // --- SEÇÃO DE MATEMÁTICA APLICADA & LUA UTILS ---
        Text {
            text: "⚡ Regra de Cramer, Thévenin & Voz Kokoro TTS:"
            color: "#b4befe"
            font.pixelSize: 14
            font.bold: true
            Layout.topMargin: 10
        }

        RowLayout {
            spacing: 10
            Layout.fillWidth: true

            ModernButton {
                text: "📐 Cramer 3x3 & Thévenin (Julia)"
                bgCor: "#a6e3a1"
                textoCor: "#11111b"
                Layout.fillWidth: true
                onClicked: mathConsoleArea.text = appController.run_polyglot_inline("julia", "circuitos_thevenin_cramer.jl", "")
            }

            ModernButton {
                text: "🐍 Newton-Raphson (Python)"
                bgCor: "#f9e2af"
                textoCor: "#11111b"
                Layout.fillWidth: true
                onClicked: mathConsoleArea.text = appController.run_polyglot_inline("python", "matematica_python.py", "2.0")
            }

            ModernButton {
                text: "🔊 Ouvir Voz Kokoro TTS"
                bgCor: "#cba6f7"
                textoCor: "#11111b"
                Layout.fillWidth: true
                onClicked: appController.falar_voz_kokoro("Boa noite Pedro! Descanse bem. Amanhã vamos estudar Regra de Cramer e Thévenin na mão!")
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
                    id: mathConsoleArea
                    readOnly: true
                    color: "#89b4fa"
                    font.family: "Monospace"
                    font.pixelSize: 11
                    placeholderText: "Saída dos scripts de Regra de Cramer, Thévenin e Matemática aparecerá aqui..."
                    wrapMode: Text.Wrap
                }
            }
        }
    }
}
