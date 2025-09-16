import QtQuick

Item {

    id:api_base

    property int delay: 0
    property color connectColor: delay>0?delay<200?"green":"yellow" :"red"

    // WebSocket {}

    property Ajax ajax: Ajax{}
    function url(serverUrl, ...args){
        let reUrl=serverUrl
        for(let argIndex in args){
            reUrl+="/"+args[argIndex]
        }
        return reUrl
    }

    property ApiConfig apiConfig: ApiConfig{}

    function getLevelDataByTime(fromDateStr,toDateStr,success, failure){
        return ajax.get(apiConfig.url(apiConfig.serverUrl,"LevelData"),success, failure)
    }

    function openApi(port){
            return Qt.openUrlExternally(apiConfig.url(apiConfig.protocol+apiConfig.hostname+":"+port,"docs"))
    }


    function getDelay(success, failure){
        return ajax.get(apiConfig.url(apiConfig.serverUrl,"delay"),success, failure)

    }
}
