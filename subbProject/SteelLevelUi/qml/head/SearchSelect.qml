import QtQuick

//  查询方式

import QtQuick.Controls
import QtQuick.Layouts

Row {
    id:root
    TitleLabelItem{
        text: qsTr("查询方式:")
    }

    ComboBox{
        width: 100
        height: root.height
        model: coreModel.allSearchModel

    }

}
