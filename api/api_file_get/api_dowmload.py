import os
import json

from fastapi import UploadFile, File
from starlette.responses import FileResponse

import config

from core import app
if config.CLIENT_CONFIG_FILE.exists():
    client_info = json.load(config.CLIENT_CONFIG_FILE.open("r", encoding=config.base_encoding))
else:
    client_info = {"version": "0.0.0",
                   "updateList": []}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file to the server.
    Parameters:
        file (UploadFile): The file to be uploaded.

    Returns:
        dict: A dictionary containing information about the uploaded file.
    """
    file_location = os.path.join(config.UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}


@app.get("/client_version")
async def client_version():
    """
    Uploads a file to the server.
    Parameters:

    Returns:
        dict: A dictionary containing information about the uploaded file.
    """
    return client_info["version"]


@app.get("/client_update/{version}")
async def client_update(version: str):
    """
    Uploads a file to the server.
    Parameters:

    Returns:
        dict: A dictionary containing information about the uploaded file.
    """
    if version != client_info["version"]:
        return {"update": True, "updateList": client_info["updateList"], "version": client_info["version"],
                "upMsg":client_info["msg"]}
    return {"update": False, "version": client_info["version"], "upMsg":client_info["msg"]}


@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Downloads a file from the server.

    Parameters:
        filename (str): The name of the file to be downloaded.

    Returns:
        FileResponse or dict: If the file exists, returns a FileResponse object representing the file.
                              If the file does not exist, returns a dictionary with an error message.
    """
    file_location = os.path.join(config.CLIENT_DIRECTORY, filename)
    if os.path.exists(file_location):
        return FileResponse(file_location)
    return {"error": "File not found"}


@app.get("/updateList")
async def updateList():
    """
    Downloads a file from the server.

    Parameters:
        filename (str): The name of the file to be downloaded.

    Returns:
        FileResponse or dict: If the file exists, returns a FileResponse object representing the file.
                              If the file does not exist, returns a dictionary with an error message.
    """
    return client_info["updateList"]