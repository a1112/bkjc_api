import sys
import os
import json
from pathlib import Path
from core import init, get_path, get_config_path
from core.config import MAIN_INFO, isLoc

info = MAIN_INFO

if isLoc():
    from core.config.localConfig import *
else:
    from core.config.NetConfig import *

if not forwarder:
    init.initDataBase(info)



