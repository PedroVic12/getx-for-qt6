import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: card
    property string titulo: "Título"
    property string subtitulo: "Subtítulo"
    property string icone: "⚡"
    property color corDestaque: "#89b4fa"
    signal clicked()

    implicitWidth: 350
    implicitHeight: 90
    radius: 12
    color: mouseArea.containsMouse ? "#1e1e2e" : "#181825"
    border.color: mouseArea.containsMouse ? corDestaque : "#313244"
    border.width: 1.5

    Behavior on border.color { ColorAnimation { duration: 150 } }
    Behavior on color { ColorAnimation { duration: 150 } }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        Rectangle {
            implicitWidth: 44
            implicitHeight: 44
            radius: 10
            color: Qt.alpha(corDestaque, 0.2)

            Text {
                text: card.icone
                font.pixelSize: 22
                anchors.centerIn: parent
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 3

            Text {
                text: card.titulo
                color: "#cdd6f4"
                font.pixelSize: 14
                font.bold: true
                elide: Text.ElideRight
                Layout.fillWidth: true
            }

            Text {
                text: card.subtitulo
                color: "#a6adc8"
                font.pixelSize: 11
                wrapMode: Text.WordWrap
                maximumLineCount: 2
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
        }

        Text {
            text: "▶"
            color: corDestaque
            font.pixelSize: 14
            font.bold: true
            opacity: mouseArea.containsMouse ? 1.0 : 0.4
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: card.clicked()
    }
}
