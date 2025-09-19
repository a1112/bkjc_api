from core import mainApp as app
import uvicorn

import subbProject.SteelLevel.init
subbProject.SteelLevel.init.initServer(app)
import subbProject.SteelLevel.main
import subbProject.SteelLevel.api
import subbProject.SteelLevel.script


if __name__ == '__main__':
    app=subbProject.SteelLevel.api.app
    uvicorn.run(app, host='0.0.0.0', port=8009)