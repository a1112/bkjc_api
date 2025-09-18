import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Rectangle {
    width: 120
    height: 30
    border.width: 1
    border.color: "#FFF"
    color: "#00005F"
    Label{
        anchors.centerIn: parent
        font.bold: true
        font.pointSize: 15
        text: qsTr(name)
    }
}
