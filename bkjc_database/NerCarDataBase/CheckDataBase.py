from bkjc_database.NerCarDataBase import core, SqlBase


def checkDataBase():
    SqlBase.beforeInit = False  # 避免数据库不存在时报错
    SqlBase.driveType = "mysql"
    core.setBaseUrl(drive="mysql", user="root", password="519223")
    engine = SqlBase.get_engine("")
    # core.databaseList = [d.lower() for d in core.databaseList]
    currentDatabaseList =[i[0] for i in engine.execute("show databases").all()]
    print("当前存在数据库 {}".format(currentDatabaseList))
    lossDatabases = [i for i in core.databaseList if i not in currentDatabaseList]
    print("系统需要数据库 {}".format(core.databaseList))
    print(" 当前缺少数据库 {}".format(lossDatabases))
    for databaseName in core.databaseList:
        if databaseName.lower() not in currentDatabaseList:
            print("开始 创建 {} 数据库".format(databaseName))
            engine.execute("create database {}".format(databaseName))
        if "ClientDefectDB" not in databaseName:
            exec("from NerCarDataBase import {databaseName}".format(databaseName=databaseName))
            exec ("{databaseName}.dbInit()".format(databaseName=databaseName))
            exec("{databaseName}.metadata.create_all({databaseName}.engine)".format(databaseName=databaseName))
        else:
            #  创建 缺陷数据库
            from bkjc_database.NerCarDataBase.sqlserver import ClientDefectDB
            ClientDefectDB.dbInit()
            ClientDefectDB.metadata.create_all(ClientDefectDB.engine)
