import QtQuick
import QtQuick.Controls

Label {
    function ping_to_string(ping_ms){
        if (ping_ms === -1){
            return "连接错误"
        }
        return "" + ping_ms+" ms"

    }
    function ping_to_color(ping_ms){

        if (ping_ms<0){
            return "red"
        }

        if (ping_ms<50){
            return "green"
        }

        if (ping_ms<200){
            return "yellow"
        }

        return "red"
    }

    font.pointSize: 15

    text: ping_to_string(coreModel.ping_ms)
    color: ping_to_color(coreModel.ping_ms)

}
