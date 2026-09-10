import QtQuick
import QtQuick.Controls

Button {
    id: control
    property color bgCor: "#1e66f5"
    property color textoCor: "#ffffff"

    contentItem: Text {
        text: control.text
        font.pixelSize: 13
        font.bold: true
        color: control.textoCor
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    background: Rectangle {
        implicitWidth: 120
        implicitHeight: 40
        radius: 8
        color: control.down ? Qt.darker(control.bgCor, 1.2) : (control.hovered ? Qt.lighter(control.bgCor, 1.1) : control.bgCor)
        border.color: Qt.lighter(control.bgCor, 1.2)
        border.width: control.hovered ? 1 : 0

        Behavior on color { ColorAnimation { duration: 150 } }
    }
}
