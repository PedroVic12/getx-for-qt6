import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "views"
import "components"

ApplicationWindow {
    id: window
    visible: true
    width: 920
    height: 700
    title: "Dashboard Poliglota & Toolbox KDE (MVC QML)"
    color: "#11111b"

    // --- MENU LATERAL RESPONSIVO (DRAWER) ---
    Drawer {
        id: drawer
        width: Math.min(window.width * 0.75, 290)
        height: window.height

        background: Rectangle {
            color: "#181825"
            border.color: "#313244"
            border.width: 1
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 18
            spacing: 10

            RowLayout {
                spacing: 10
                Text {
                    text: "⚡ Batcaverna 2026"
                    color: "#cba6f7"
                    font.pixelSize: 20
                    font.bold: true
                }
            }

            Text {
                text: "Menu de Navegação MVC"
                color: "#7f849c"
                font.pixelSize: 11
                Layout.bottomMargin: 5
            }

            Rectangle { Layout.fillWidth: true; height: 1; color: "#313244" }

            ModernButton {
                text: "🚀 Central Poliglota"
                bgCor: stackLayout.currentIndex === 0 ? "#1e66f5" : "#1e1e2e"
                textoCor: "#cdd6f4"
                Layout.fillWidth: true
                onClicked: {
                    stackLayout.currentIndex = 0
                    headerTitle.text = "Central de Execução Poliglota"
                    drawer.close()
                }
            }

            ModernButton {
                text: "📄 Gerador de Currículo"
                bgCor: stackLayout.currentIndex === 1 ? "#1e66f5" : "#1e1e2e"
                textoCor: "#cdd6f4"
                Layout.fillWidth: true
                onClicked: {
                    stackLayout.currentIndex = 1
                    headerTitle.text = "Gerador de Currículos KDE"
                    drawer.close()
                }
            }

            ModernButton {
                text: "📋 Rotina Diária & WIP"
                bgCor: stackLayout.currentIndex === 2 ? "#1e66f5" : "#1e1e2e"
                textoCor: "#cdd6f4"
                Layout.fillWidth: true
                onClicked: {
                    stackLayout.currentIndex = 2
                    headerTitle.text = "Rotina Diária Anti-Kanban"
                    drawer.close()
                }
            }

            ModernButton {
                text: "📖 Guia POO & Matemática"
                bgCor: stackLayout.currentIndex === 3 ? "#1e66f5" : "#1e1e2e"
                textoCor: "#cdd6f4"
                Layout.fillWidth: true
                onClicked: {
                    stackLayout.currentIndex = 3
                    headerTitle.text = "Guia POO & Matemática Aplicada"
                    drawer.close()
                }
            }

            Item { Layout.fillHeight: true } // Espaçador flexível

            Rectangle { Layout.fillWidth: true; height: 1; color: "#313244" }

            Text {
                text: "UFF Engenharia Elétrica | Qt6 QML"
                color: "#585b70"
                font.pixelSize: 11
            }
        }
    }

    // --- CABEÇALHO (TOOLBAR) ---
    header: ToolBar {
        background: Rectangle { color: "#181825"; border.color: "#313244"; border.width: 1 }

        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 10
            anchors.rightMargin: 10

            ToolButton {
                text: "☰"
                font.pixelSize: 22
                contentItem: Text {
                    text: parent.text
                    color: "#cba6f7"
                    font.pixelSize: 20
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                onClicked: drawer.open()
            }

            Label {
                id: headerTitle
                text: "Central de Execução Poliglota"
                font.pixelSize: 16
                font.bold: true
                color: "#cdd6f4"
                horizontalAlignment: Qt.AlignHCenter
                Layout.fillWidth: true
            }

            Item { Layout.preferredWidth: 40 }
        }
    }

    // --- CONTEÚDO PRINCIPAL (STACKLAYOUT DE TABS) ---
    Item {
        anchors.fill: parent
        anchors.margins: 15

        StackLayout {
            id: stackLayout
            anchors.fill: parent
            currentIndex: 0

            PolyglotView {}
            CurriculoView {}
            RotinaDiariaView {}
            GuiaPOOView {}
        }
    }

    // --- TOAST NOTIFICATION OVERLAY ---
    Rectangle {
        id: toastOverlay
        visible: false
        opacity: 0.0
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 25
        implicitWidth: Math.min(toastText.implicitWidth + 30, window.width - 40)
        implicitHeight: 40
        radius: 20
        color: "#1e1e2e"
        border.color: "#89b4fa"
        border.width: 1.5

        RowLayout {
            anchors.centerIn: parent
            spacing: 8
            Text {
                id: toastText
                text: ""
                color: "#cdd6f4"
                font.pixelSize: 12
                font.bold: true
            }
        }

        Behavior on opacity { NumberAnimation { duration: 200 } }

        Timer {
            id: toastTimer
            interval: 3500
            onTriggered: {
                toastOverlay.opacity = 0.0
                toastHideTimer.start()
            }
        }

        Timer {
            id: toastHideTimer
            interval: 200
            onTriggered: toastOverlay.visible = false
        }
    }

    Connections {
        target: appController
        function onToastMessage(msg, type) {
            toastText.text = msg
            if (type === "success") toastOverlay.border.color = "#a6e3a1"
            else if (type === "error") toastOverlay.border.color = "#f38ba8"
            else toastOverlay.border.color = "#89b4fa"

            toastOverlay.visible = true
            toastOverlay.opacity = 1.0
            toastTimer.restart()
        }
    }
}
