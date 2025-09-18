import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../model"
ItemDelegate {
    id:root
    property SteelLevelModel steelLevelModel: SteelLevelModel{}

    Layout.fillWidth: true
    width: parent.width
    height: 30
    Row{
        anchors.fill: parent
        Repeater{
            model: coreModel.titleleLeveModel

            SteelLevelItemItem{

            }

        }


    }

    Component.onCompleted: {
        steelLevelModel.init(coreModel.steelLevelModel.get(index))
    }
}
