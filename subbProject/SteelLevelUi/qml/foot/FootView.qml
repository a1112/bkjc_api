import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

Rectangle {
    color: "#00000000"
    border.width: 1
    border.color: "#00000000"
    Layout.fillWidth: true

    height: 40

    RowLayout{
        anchors.fill: parent
        IpInfo{}

        Item{
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
        PingInfo{

        }

    }


}
