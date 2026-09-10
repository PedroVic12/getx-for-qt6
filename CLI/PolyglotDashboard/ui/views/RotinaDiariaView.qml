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
            text: "📋 Rotina Diária & Anti-Kanban (Batcaverna 2026)"
            color: "#cdd6f4"
            font.pixelSize: 18
            font.bold: true
            Layout.topMargin: 5
        }

        Text {
            text: "Post-it Digital de 3 Itens. Conclua os 3 itens para encerrar o expediente de desenvolvimento do dia."
            color: "#a6adc8"
            font.pixelSize: 12
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }

        // --- Post-it Card Container ---
        Rectangle {
            Layout.fillWidth: true
            implicitHeight: postItColumn.implicitHeight + 30
            color: "#181825"
            radius: 12
            border.color: "#f9e2af"
            border.width: 1.5

            ColumnLayout {
                id: postItColumn
                anchors.fill: parent
                anchors.margins: 15
                spacing: 10

                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "📌 Post-it Digital do Dia (Máx 3 Itens WIP)"
                        color: "#f9e2af"
                        font.pixelSize: 14
                        font.bold: true
                    }
                    Item { Layout.fillWidth: true }
                    Text {
                        text: "Hierarquia: UFF > Saúde > Projetos"
                        color: "#a6adc8"
                        font.pixelSize: 11
                    }
                }

                Repeater {
                    model: appController.get_postit_items()

                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: 48
                        color: modelData.concluido ? "#1e2030" : "#1e1e2e"
                        radius: 8
                        border.color: modelData.concluido ? "#a6e3a1" : "#313244"

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 12

                            CheckBox {
                                checked: modelData.concluido
                                onCheckedChanged: appController.toggle_postit_item(index)
                            }

                            Text {
                                text: modelData.titulo
                                color: modelData.concluido ? "#a6e3a1" : "#cdd6f4"
                                font.pixelSize: 13
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

        // --- Pomodoro Counter Box ---
        Rectangle {
            Layout.fillWidth: true
            implicitHeight: 80
            color: "#11111b"
            radius: 10
            border.color: "#313244"

            RowLayout {
                anchors.fill: parent
                anchors.margins: 15
                spacing: 15

                Text {
                    text: "⏱️ Pomodoros Concluídos:"
                    color: "#89b4fa"
                    font.pixelSize: 14
                    font.bold: true
                }

                Text {
                    id: txtPomodoro
                    text: appController.get_pomodoros_count() + " / 6 Meta"
                    color: "#a6e3a1"
                    font.pixelSize: 16
                    font.bold: true
                }

                Item { Layout.fillWidth: true }

                ModernButton {
                    text: "➕ Registrar Pomodoro"
                    bgCor: "#89b4fa"
                    textoCor: "#11111b"
                    onClicked: {
                        appController.add_pomodoro()
                        txtPomodoro.text = appController.get_pomodoros_count() + " / 6 Meta"
                    }
                }
            }
        }
    }
}
