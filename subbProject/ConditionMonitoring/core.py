from fastapi import FastAPI

app = FastAPI()
mainApp = app
testApp = app

configApp = app

steelGetApp = app


def initServer(app_):
    global app
    app = app_
    global mainApp
    mainApp = app_
    global testApp
    testApp = app_
    global configApp
    configApp = app_
    global steelGetApp
    steelGetApp = app_
    pass
