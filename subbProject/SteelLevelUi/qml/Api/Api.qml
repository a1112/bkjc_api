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

    function getLevelTitle(success, failure){
        return ajax.get(apiConfig.url(apiConfig.serverUrl,"getLevelTitle"),success, failure)
    }

    function getLevelDataByTime(fromDateStr,toDateStr,success, failure){
        return ajax.get(apiConfig.url(apiConfig.serverUrl,"getLevelData"),success, failure)
    }

    function openApi(port){
            return Qt.openUrlExternally(apiConfig.url(apiConfig.protocol+apiConfig.hostname+":"+port,"docs"))
    }


    function getDelay(success, failure){
        return ajax.get(apiConfig.url(apiConfig.serverUrl,"delay"),success, failure)

    }

    function getProductionLine(success, failure){
        return ajax.get(apiConfig.url(apiConfig.serverUrl,"getProductionLine"),success, failure)
    }

}
