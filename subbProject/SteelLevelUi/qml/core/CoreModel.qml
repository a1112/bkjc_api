import QtQuick
import "../model"
Item {

    property int ping_ms: -1

    function initModel(data){
        steelLevelModel.clear()
        data.forEach((item)=>{
                        steelLevelModel.append(item)
                     })
    }

    function initTitleMpdel(data){
        titleleLeveModel.clear()
        data.forEach((item)=>{
                         titleleLeveModel.append(item)
                      })

    }

    property ListModel steelLevelModel: ListModel{
        dynamicRoles :true
    }

    property ListModel titleleLeveModel: ListModel{
        dynamicRoles :true
    }

}
