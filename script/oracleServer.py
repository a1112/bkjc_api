import time
import uvicorn
import cx_Oracle
import fastapi
app = fastapi.FastAPI()
tns = cx_Oracle.makedsn("10.6.25.12", "1521", "LGORD")  # 监听Oracle数据库
db = cx_Oracle.connect("mid", "mid", tns)  # 连接数据库
print(db)
cur = db.cursor()


@app.get("/search/steelNo/{steelNo:str}")
def searchySteelNo(steelNo):
    sql_code = "SELECT * FROM MES_SHEET_INFO WHERE MAT_NO = '{}'"
    ex=cur.execute(sql_code.format(steelNo))
    data = ex.fetchone()
    if data:
        return data


uvicorn.run(app=app, host="0.0.0.0", port=1002)