import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    height: root.height
    width: item_width+6
    color: "#00000000"
    border.width: 1
    border.color: "#22FFFFFF"


    Label{
        anchors.centerIn: parent
        text: steelLevelModel.getValue(key)
    }

}
