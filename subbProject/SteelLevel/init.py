from fastapi import FastAPI

app = FastAPI()

def initServer(app_):
    global app
    app=app_