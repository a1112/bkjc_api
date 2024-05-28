from . import api_dowmload,api_config
import json
from core import app
from config import ipListJson
from pathlib import Path


@app.get("/getServerList")
def get_server_list():
    if Path(ipListJson).exists():
        return json.load(Path(ipListJson).open("r", encoding="utf-8"))
    return []