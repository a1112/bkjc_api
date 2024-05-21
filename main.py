import uvicorn
from core import mainApp as app
from config import info
import api
import pymssql

if __name__ == '__main__':
    uvicorn.run(app=app, host=info["ip"], port=info["port"])
