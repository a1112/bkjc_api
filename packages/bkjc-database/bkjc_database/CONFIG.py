from abc import ABC


class DbConfigBase(ABC):
    def __init__(self):
        self.drive = "sqlserver"

        self.baseUrl = "mssql+pymssql://ARNTUSER:ARNTUSER@127.0.0.1:1433/{}?charset=utf8"
        self.echo = False
        self.beforeInit = True
        self.databaseCheckInfo = {}  # 数据库正确性验证字典


    @property
    def url(self):
        return self.baseUrl

# database_type = "ncdhotstrip"
# systemDatabase = ["master", "model", "msdb", "tempdb"]
# baseUrl = "mssql+pymssql://ARNTUSER:ARNTUSER@127.0.0.1:1433/{}?charset=utf8"
# echo: bool = False
# beforeInit = True
# databaseCheckInfo = {}  # 数据库正确性验证字典
# drive = "sqlserver"
# databaseList = ['DWDiagnostics', 'DWConfiguration', 'DWQueue', 'Classifier', 'SteelRecord', "ConfigCenter"]
globDbConfig:DbConfigBase|None=None

class DbConfig3d0(DbConfigBase):
    def __init__(self):
        super().__init__()
        global globDbConfig
        globDbConfig =self
        self.systemDatabase = ["master", "model", "msdb", "tempdb"]
        self.baseUrl = "mssql+pymssql://ARNTUSER:ARNTUSER@127.0.0.1:1433/{}?charset=utf8"
        self.echo = False
        self.beforeInit = True
        self.databaseCheckInfo = {}  # 数据库正确性验证字典
        self.drive = "sqlserver"
        self.databaseList = ['DWDiagnostics', 'DWConfiguration', 'DWQueue', 'Classifier', 'SteelRecord', "ConfigCenter"]

class DbConfig4d0(DbConfigBase):
    def __init__(self):
        super().__init__()
        global globDbConfig
        globDbConfig =self
        self.database_type = "ncdhotstrip"
        self.systemDatabase = ["master", "model", "msdb", "tempdb"]
        drives="mysql+pymysql"
        self.baseUrl = drives+"://root:nercar@127.0.0.1:3306/{}?charset=utf8"
        # self.baseUrl="sqlite:///test.db"
        self.echo = False
        self.beforeInit = True
        self.databaseCheckInfo = {}  # 数据库正确性验证字典
        self.drive = "mysql"



