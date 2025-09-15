import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Row {
    id:root
    height: 40
    property alias title: title_id.text
    spacing: 5
    Label{
        id:title_id
        anchors.verticalCenter: parent.verticalCenter

        text: qsTr("日期")
    }

    TextField{
        width: 80
        implicitHeight: root.height
        selectByMouse: true
    }
    Label{
        anchors.verticalCenter: parent.verticalCenter
        text: qsTr("年")
    }
    TextField{
        width: 50
        implicitHeight: root.height
        selectByMouse: true
    }
    Label{
        anchors.verticalCenter: parent.verticalCenter
        text: qsTr("月")
    }
    TextField{
        width: 50
        implicitHeight: root.height
        selectByMouse: true
    }
    Label{
        anchors.verticalCenter: parent.verticalCenter
        text: qsTr("日")
    }
    TextField{
        width: 50
        implicitHeight: root.height
        selectByMouse: true
    }
    Label{
        anchors.verticalCenter: parent.verticalCenter
        text: qsTr("时")
    }
    TextField{
        width: 50
        implicitHeight: root.height
        selectByMouse: true
    }
    Label{
        anchors.verticalCenter: parent.verticalCenter
        text: qsTr("分")
    }
}
