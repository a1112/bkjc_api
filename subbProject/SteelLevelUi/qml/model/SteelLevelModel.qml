import QtQuick

Item {
    // {
    //     "id": 1,
    //     "steelID": 1280,
    //     "level": 1,
    //     "level_under": null,
    //     "steelType": "NM300TPGJ",
    //     "levelInfo": null,
    //     "levelInfo_under": null,
    //     "plant_classification": null,
    //     "length": 7.05,
    //     "grade": 1,
    //     "grade_under": null,
    //     "width": 1.65,
    //     "msg": "['无缺陷', '无缺陷']",
    //     "productionLine_classification": null,
    //     "thick": 3,
    //     "level_up": null,
    //     "msg_under": null,
    //     "steelName": "3B2559580201801",
    //     "upDefectNum": null,
    //     "levelInfo_up": null,
    //     "packageName": "",
    //     "downDefectNum": null,
    //     "grade_up": null,
    //     "seqNo": 1280,
    //     "detectTime": "2023-11-06T20:49:32",
    //     "msg_up": null
    //   }



    property var id_
    property var steelID_
    property var level_
    property var level_under_
    property var steelType_
    property var levelInfo_
    property var levelInfo_under_

    property var plant_classification_
    property var length_

    property var grade_
    property var grade_under_
    property var width_
    property var msg_
    property var productionLine_classification_
    property var thick_
    property var level_up_
    property var msg_under_
    property var steelName_
    property var upDefectNum_
    property var levelInfo_up_
    property var packageName_
    property var downDefectNum_
    property var grade_up_
    property var seqNo_
    property var detectTime_
    property var msg_up_

    property var modelData

    function getValue(key){
        return modelData[key]
    }


    function init(model){
        modelData = model
        id_ = model["id"]
        steelID_ = model["steelID"]
        level_ = model["level"]
        level_under_ = model["level_under"]
        steelType_ = model["steelType"]
        levelInfo_ = model["levelInfo"]
        levelInfo_under_ = model["levelInfo_under"]
        plant_classification_ = model["plant_classification"]
        length_ = model["length"]
        grade_ = model["grade"]
        grade_under_ = model["grade_under"]
        width_ = model["width"]
        msg_ = model["msg"]
        productionLine_classification_ = model["productionLine_classification"]
        thick_ = model["thick"]
        level_up_ = model["level_up"]
        msg_under_ = model["msg_under"]
        steelName_ = model["steelName"]
        upDefectNum_ = model["upDefectNum"]
        levelInfo_up_ = model["levelInfo_up"]
        packageName_ = model["packageName"]
        downDefectNum_ = model["downDefectNum"]
        grade_up_ = model["grade_up"]
        seqNo_ = model["seqNo"]
        detectTime_ = model["detectTime"]
        msg_up_ = model["msg_up"]


    }
}
