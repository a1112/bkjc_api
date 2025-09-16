import QtQuick
import QtQuick.Controls

Row {
    height: parent.height
    Label{

        height: parent.height
        text: qsTr("ip:")
        font.bold: true
        font.pointSize: 15
        anchors.verticalCenter: parent.verticalCenter
    }

    TextField{

        text: api.apiConfig.hostname
        implicitHeight: parent.height
        height: parent.height

    }


}
