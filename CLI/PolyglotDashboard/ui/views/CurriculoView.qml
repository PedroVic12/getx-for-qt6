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
            text: "📄 Gerador Dinâmico de Currículo (Estilo iLovePDF - KDE QML)"
            color: "#cdd6f4"
            font.pixelSize: 18
            font.bold: true
            Layout.topMargin: 5
        }

        Text {
            text: "Preencha a vaga desejada e ajuste o objetivo para gerar um PDF/DOCX profissional automaticamente."
            color: "#a6adc8"
            font.pixelSize: 12
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }

        // --- Form Box ---
        Rectangle {
            Layout.fillWidth: true
            implicitHeight: formLayout.implicitHeight + 30
            color: "#181825"
            radius: 12
            border.color: "#313244"

            ColumnLayout {
                id: formLayout
                anchors.fill: parent
                anchors.margins: 15
                spacing: 12

                Text {
                    text: "📌 Vaga Alvo / Cargo Desejado:"
                    color: "#b4befe"
                    font.pixelSize: 13
                    font.bold: true
                }

                CustomInput {
                    id: inputVaga
                    placeholderText: "Ex: Engenheiro Eletricista / Desenvolvedor Python Qt"
                    text: "Engenheiro Eletricista / Desenvolvedor C++ Qt"
                    Layout.fillWidth: true
                }

                Text {
                    text: "🎯 Texto do Objetivo Profissional:"
                    color: "#b4befe"
                    font.pixelSize: 13
                    font.bold: true
                }

                Rectangle {
                    Layout.fillWidth: true
                    implicitHeight: 90
                    color: "#1e1e2e"
                    radius: 8
                    border.color: "#313244"

                    ScrollView {
                        anchors.fill: parent
                        anchors.margins: 8
                        clip: true

                        TextArea {
                            id: inputObjetivo
                            color: "#cdd6f4"
                            font.pixelSize: 12
                            wrapMode: Text.Wrap
                            text: "Atuar no desenvolvimento de sistemas de automação, simulação de redes elétricas e software desktop de alta performance, aplicando conhecimentos da UFF e experiência prática no ONS."
                        }
                    }
                }

                RowLayout {
                    spacing: 12
                    Layout.topMargin: 10
                    Layout.fillWidth: true

                    ModernButton {
                        text: "📄 Gerar PDF (ReportLab)"
                        bgCor: "#1e66f5"
                        Layout.fillWidth: true
                        onClicked: appController.generate_cv_pdf(inputVaga.text, inputObjetivo.text, "")
                    }

                    ModernButton {
                        text: "📝 Gerar Word (.docx)"
                        bgCor: "#a6e3a1"
                        textoCor: "#11111b"
                        Layout.fillWidth: true
                        onClicked: appController.generate_cv_docx(inputVaga.text, inputObjetivo.text, "")
                    }
                }
            }
        }

        // --- Info Box ---
        Rectangle {
            Layout.fillWidth: true
            implicitHeight: 110
            color: "#11111b"
            radius: 10
            border.color: "#45475a"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 6

                Text {
                    text: "👤 Perfil Base do Candidato:"
                    color: "#fab387"
                    font.pixelSize: 13
                    font.bold: true
                }
                Text {
                    text: "Pedro Victor Rodrigues Veras | Niterói - RJ"
                    color: "#cdd6f4"
                    font.pixelSize: 12
                }
                Text {
                    text: "UFF Engenharia Elétrica | Estagiário PLC ONS (2025-2026)"
                    color: "#a6adc8"
                    font.pixelSize: 11
                }
            }
        }
    }
}
