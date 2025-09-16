import QtQuick

Item {

    Timer{
        interval: 3000
        repeat: true
        running: true
        onTriggered: {
            let start_time= Date.now()
            api.getDelay(
                        (text)=>{
                            coreModel.ping_ms = Date.now()-start_time
                        },(err)=>{
                            coreModel.ping_ms = -1
                        }
                        )

        }

    }


}
