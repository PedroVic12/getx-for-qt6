import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 600
    height: 450
    title: "Batcaverna - C++ Qt Quick App (teste_4)"

    background: Rectangle {
        color: "#1e1e2e"
    }

    Column {
        anchors.centerIn: parent
        spacing: 20

        Text {
            text: "Bem-vindo ao C++ Qt Quick (QML)!"
            font.pixelSize: 24
            font.bold: true
            color: "#cdd6f4"
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: "Nome atual no Controller: " + controller.name
            font.pixelSize: 16
            color: "#a6adc8"
            anchors.horizontalCenter: parent.horizontalCenter
        }

        TextField {
            id: nameInput
            placeholderText: "Digite seu nome..."
            color: "#cdd6f4"
            anchors.horizontalCenter: parent.horizontalCenter
            background: Rectangle {
                implicitWidth: 200
                implicitHeight: 40
                color: "#313244"
                radius: 6
            }
        }

        Button {
            text: "Enviar para C++"
            anchors.horizontalCenter: parent.horizontalCenter
            contentItem: Text {
                text: parent.text
                color: "#11111b"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
            }
            background: Rectangle {
                implicitWidth: 150
                implicitHeight: 40
                color: parent.down ? "#a6e3a1" : "#89b4fa"
                radius: 8
            }
            onClicked: {
                controller.greet(nameInput.text)
            }
        }
    }
}
