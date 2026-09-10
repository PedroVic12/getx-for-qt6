import QtQuick
import QtQuick.Controls

TextField {
    id: control
    placeholderTextColor: "#7f849c"
    color: "#cdd6f4"
    font.pixelSize: 13
    leftPadding: 12
    rightPadding: 12
    topPadding: 10
    bottomPadding: 10

    background: Rectangle {
        implicitWidth: 200
        implicitHeight: 40
        color: "#1e1e2e"
        radius: 8
        border.color: control.activeFocus ? "#89b4fa" : "#313244"
        border.width: control.activeFocus ? 2 : 1

        Behavior on border.color { ColorAnimation { duration: 150 } }
    }
}
