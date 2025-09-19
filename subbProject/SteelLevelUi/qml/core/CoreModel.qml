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

    property ListModel productionLineModel: ListModel{
        dynamicRoles :true
    }

    function initProductionLineModel(data_dict){
        productionLineModel.clear()

        for (let key in data_dict){
            let item_data = data_dict[key]
            item_data["index"] = key
            productionLineModel.append(item_data)
        }

        data.forEach((item)=>{
                         productionLineModel.append(item)
                      })
    }
}
