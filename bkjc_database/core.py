#  encoding = utf-8
from . import CONFIG


def reDatabaseName(databaseName: str):
    return databaseName.replace("$", "_x_").replace("@", "_a_").replace("#", "_J_")


def setBaseUrl(ip="127.0.0.1", port=0, user="ARNTUSER", password="ARNTUSER", chart='utf8', drive_="sqlserver"):
    CONFIG.drive = drive_
    driveUrl = ""
    if drive_ == "sqlserver":
        driveUrl = "mssql+pymssql"
        port = 1433
        cameraCount = 6
        CONFIG.databaseList = ['DWDiagnostics', 'DWConfiguration', 'DWQueue', 'Classifier', 'SteelRecord', "ConfigCenter"
                        ] + ["ClientDefectDB{}".format(i) for i in range(cameraCount)]  # RcvSteelID ConfigCenter
    elif drive_ == "mysql":
        driveUrl = "mysql+pymysql"
        port = 3306
    baseUrl = "{driveUrl}://{user}:{password}@{ip}:{port}/_replace_code_database_?charset={chart}".format(
        driveUrl=driveUrl,
        ip=ip, port=port, user=user, password=password, chart=chart
    ).replace("_replace_code_database_", "{}")
    print(baseUrl)
    CONFIG.baseUrl = baseUrl
    return baseUrl


create = False
