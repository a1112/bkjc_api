import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Row {
    id:root
    TitleLabelItem{
        text: qsTr("产线名称:")
    }

    ComboBox{
        width: 200
        height: root.height
        model: coreModel.productionLineModel
        textRole: "DeviceName"
    }

}
