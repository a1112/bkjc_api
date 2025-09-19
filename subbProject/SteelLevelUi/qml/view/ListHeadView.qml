
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


SplitView {
    Layout.fillWidth: true
    spacing: 0
    Repeater{
        model: coreModel.titleleLeveModel
        TitleRowItem{
        }
    }
}
