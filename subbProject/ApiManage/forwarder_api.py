from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import requests
import io
from core import app, default_forwarder_server_dict, ForwarderServer

from forwarder_base import *


@app.get("/forward/serverStatus")
async def server_status():
    """
    获取转发服务器的状态
    Returns:
        转发服务器的状态
    """
    return await forward("serverStatus")
