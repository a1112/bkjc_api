import QtQuick

Item {

    property int porintCount:0

    property var eqMap:{
    "defect_image":"image"
    }

    property var port_assignments:{
        //  端口自动分配字典
        return {}
    }

    function stringToHash(str) {
        let hash = 0
        for (let i = 0; i < str.length; i++) {
            let ch = str.charCodeAt(i)
            hash = (hash << 5) - hash + ch
            hash |= 0 // 转换为 32 位整数
        }
        return hash
    }


    function getAutoUrl(key){
        return protocol + hostname + ":" + get_key_port(key)
    }
    function getAutoWsUrl(key){
        return ws_protocol + hostname+ ":" + server_port_base
    }
}
