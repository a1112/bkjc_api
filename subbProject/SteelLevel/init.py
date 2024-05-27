from fastapi import FastAPI

app = None


def initServer(app_):
    global app
    app = app_
