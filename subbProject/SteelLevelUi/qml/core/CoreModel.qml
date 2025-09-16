import QtQuick

Item {

    property int ping_ms: -1

    property ListModel main_model: ListModel{}


    function initModel(data){
        main_model.clear()
        data.forEach((item)=>{
                        main_model.append(item)
                     })
    }

}
