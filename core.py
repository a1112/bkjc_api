import os
from ctypes import *
from os.path import *
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