import QtQuick
import Qt.labs.settings
Item {
    id:root

    property var lastUrls:{return {}}

    function getLastUrlByKey(key){
        return lastUrls[key]
    }
    ListModel{

    }

    property string hostname: "127.0.0.1"
    property int port:8010

    readonly property string protocol: "http://"
    readonly property string ws_protocol:"ws://"

    property PortTool portTool :PortTool{
    }

    readonly property string serverUrl: protocol+hostname+":"+port


    function url(reUrl,...args){
        let key =""

        for(let argIndex in args){
            key=args[0]
            if (typeof(args[argIndex])=='object')
            {
                reUrl+=getGetArgs(args[argIndex])
            }
            else{
                 reUrl+="/"+args[argIndex]
                }
        }
        return reUrl
    }


    function getPostArgs(dictData){
        let res=""
        for(let key in dictData){
            if(res){
                res+="&"
            }
            res+=key+"="+dictData[key]
        }
        return res
    }


    function getGetArgs(dictData){
        let res=""
        for(let key in dictData){
            if(res){
                res+="&"
            }
            else{
            res+="?"
            }
            res+=key+"="+dictData[key]
        }
        return res
    }
}
