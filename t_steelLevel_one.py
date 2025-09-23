from threading import  Thread
from subbProject.ApiForwarder import core
from core import mainApp as app
from core.config import BaseConfig

BaseConfig.level_only = True

import subbProject.SteelLevel.init

subbProject.SteelLevel.init.initServer(app)
from subbProject.SteelLevel.script import ScriptLevel
import subbProject.SteelLevel.api


ScriptLevel(core.tabelList["6"])