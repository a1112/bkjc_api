from fastapi import FastAPI

app:FastAPI = None


def initServer(app_):
    global app
    app = app_
