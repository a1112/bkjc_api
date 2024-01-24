#  encoding = utf-8
systemDatabase = ["master", "model", "msdb", "tempdb"]
baseUrl = "mssql+pymssql://ARNTUSER:ARNTUSER@127.0.0.1:1433/{}?charset=utf8"
echo: bool = False
beforeInit=True
databaseCheckInfo = {}  # 数据库正确性验证字典


def reDatabaseName(databaseName: str):
    return databaseName.replace("$", "_x_").replace("@", "_a_").replace("#", "_J_")


drive = None


def setBaseUrl(ip="127.0.0.1", port=-1435, user="ARNTUSER", password="ARNTUSER", chart='utf8', drive_="sqlserver"):
    global baseUrl,drive
    drive = drive_
    driveUrl = ""

    if drive.lower() == "sqlserver":
        driveUrl = "mssql+pymssql"
        port = 1433
        cameraCount = 6
        databaseList = ['DWDiagnostics', 'DWConfiguration', 'DWQueue', 'Classifier', 'SteelRecord', "ConfigCenter"
                        ] + ["ClientDefectDB{}".format(i) for i in range(cameraCount)]  # RcvSteelID ConfigCenter
    elif drive.lower() == "mysql":
        driveUrl = "mysql+pymysql"
        port = 3306
    baseUrl = "{driveUrl}://{user}:{password}@{ip}:{port}/_replace_code_database_?charset={chart}".format(
        driveUrl=driveUrl,
        ip=ip, port=port, user=user, password=password, chart=chart
    ).replace("_replace_code_database_", "{}")
    print(baseUrl)
    return baseUrl


create = False
