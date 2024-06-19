import socket
import json
import os
import sys
from ctypes import *
from os.path import *
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Response
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

app = FastAPI()

mainApp = app
testApp = app

configApp = app

steelGetApp = app

root = abspath(dirname(__file__))
root = os.path.abspath(os.path.join(os.path.basename(__file__), "../.."))


def get_path(path_name):
    return os.path.join(os.path.dirname(sys.executable) if "python.exe" not in sys.executable else
                        os.path.dirname(os.path.dirname(__file__)), path_name)


def get_config_path(path_name):
    return get_path("config/"+path_name)





