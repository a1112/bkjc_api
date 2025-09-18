import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
        id:root
    ColumnLayout{
        anchors.fill: parent
        ListHeadView{
            height: 30
        }

        Item{
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            ListView{
                anchors.fill: parent
                model: coreModel.steelLevelModel

                ScrollBar.vertical: ScrollBar { }

                delegate:SteelLevelItem{
                }
            }
        }
    }
}
