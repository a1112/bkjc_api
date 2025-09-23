from threading import  Thread
from subbProject.ApiForwarder import core
from core import mainApp as app
import uvicorn
from core.config import BaseConfig

BaseConfig.level_only = True

import subbProject.SteelLevel.init

subbProject.SteelLevel.init.initServer(app)
from subbProject.SteelLevel.script import ScriptLevel
import subbProject.SteelLevel.api



def server_item(k, v):
    import uvicorn
    from core import mainApp as app
    import config
    ScriptLevel(v)


if __name__ == '__main__':
    threads=[]
    for k,v in core.tabelList.items():
        p = Thread(target=server_item, args=(k,v))
        threads.append(p)
        p.start()

    app = subbProject.SteelLevel.api.app
    uvicorn.run(app, host='0.0.0.0', port=8009)