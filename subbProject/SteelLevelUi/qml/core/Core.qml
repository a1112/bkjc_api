import QtQuick
Item {

    function search(){
        coreStatus.dataLoading=true
        api.getLevelDataByTime(
                    "","",
                    (text)=>{
                        let json_data = JSON.parse(text)
                        coreModel.initModel(json_data)
                        coreStatus.dataLoading=false
                    },

                    (err)=>{
                        coreStatus.dataLoading=false
                    }

                    )

    }

    function init(){
        api.getLevelTitle(
                    (text)=>{
                        coreModel.initTitleMpdel(JSON.parse(text))

                        coreStatus.inited = true
                    }, (err)=>{
                        coreStatus.inited = false
                    }
                    )
        api.getProductionLine(
                    (text)=>{
                        coreModel.initProductionLineModel(JSON.parse(text))
                        coreStatus.inited = true
                    }, (err)=>{
                        coreStatus.inited = false
                    }
                    )

    }
}
