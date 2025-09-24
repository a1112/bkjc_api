"""
启动服务


"""


from threading import  Thread
from subbProject.ApiForwarder import core
from core import mainApp as app
import uvicorn
from core.config import BaseConfig

BaseConfig.level_only = True

import subbProject.SteelLevel.init
subbProject.SteelLevel.init.initServer(app)
import subbProject.SteelLevel.api   # 接口位置

if __name__ == '__main__':
    threads=[]

    app = subbProject.SteelLevel.api.app
    uvicorn.run(app, host='0.0.0.0', port=8010)