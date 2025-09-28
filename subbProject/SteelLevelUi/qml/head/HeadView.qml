import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Column{
    id:root
    Layout.fillWidth: true
    height: 40
RowLayout {
        anchors.fill: parent
        spacing: 30

        ProductionLineSelect{
            height: 40
        }

        SearchSelect{


        }

        DateTimeItem{
            title:qsTr("起始")
        }

        DateTimeItem{
            title:qsTr("结束")
        }

        Item{
            Layout.fillWidth: true
            height: 1
        }

        Button{
            text: qsTr("查询")
            height: 40
            onClicked: {
                core.search()
            }
        }

        Button{
            text: qsTr("导出")
            height: 40
            onClicked: {
                core.exportExcel()
            }
        }

    }
}
