import uvicorn
from fastapi import FastAPI

import subbProject.SteelLevel.init

app=FastAPI()
subbProject.SteelLevel.init.initServer(app)

import subbProject.SteelLevel.api

if __name__ == '__main__':
    app=subbProject.SteelLevel.api.app
    # subbProject.SteelLevel.api.export_text()
    uvicorn.run(app, host='0.0.0.0', port=8010)