import QtQuick
import QtQuick.Window
import QtQuick.Controls.Material
import QtQuick.Layouts

import "qml/head"
import "qml/view"
import "qml/core"
import "qml/api"
import "qml/foot"
import "qml"
ApplicationWindow {

    width: 1800
    height: 960
    visible: true
    title: qsTr("判级数据导出程序")
    Material.theme: Material.Dark

    property Core core: Core{}
    property Api api: Api{}
    property CoreModel coreModel: CoreModel{}

    property CoreTimer coreTimer: CoreTimer{}

    property CoreStatus coreStatus: CoreStatus{}

    property DialogView dialogView: DialogView{}

    ColumnLayout{
        anchors.fill: parent
        HeadView{}
        SteelLevelTabelView{
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        FootView{}
    }

    Component.onCompleted: {
        core.init()
    }
}
