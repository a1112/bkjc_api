#  encoding = utf-8
from . import CONFIG


def reDatabaseName(databaseName: str):
    return databaseName.replace("$", "_x_").replace("@", "_a_").replace("#", "_J_")


def configure_database(info):
    """Configure before model imports. Does not connect or emit credentials."""
    from sqlalchemy.engine import URL
    drive = info.get("drive", "sqlserver")
    if drive not in ("mysql", "sqlserver"):
        raise ValueError("drive must be mysql or sqlserver")
    schema = info.get("database_type", "ncdhotstrip")
    if schema not in ("ncdhotstrip", "ncdplate"):
        raise ValueError("Unsupported database_type")
    config = CONFIG.DbConfig4d0() if drive == "mysql" else CONFIG.DbConfig3d0()
    config.database_type = schema
    config.baseUrl = URL.create(
        "mysql+pymysql" if drive == "mysql" else "mssql+pymssql",
        username=info["user"], password=info["password"],
        host=info.get("upServer", "127.0.0.1"),
        port=int(info.get("port") or (3306 if drive == "mysql" else 1433)),
        database="BKJC_DATABASE_PLACEHOLDER", query={"charset": info.get("charset", "utf8")},
    ).render_as_string(hide_password=False).replace("{", "%7B").replace("}", "%7D").replace("BKJC_DATABASE_PLACEHOLDER", "{}")
    CONFIG.globDbConfig = config
    CONFIG.database_type, CONFIG.drive, CONFIG.baseUrl = schema, drive, config.baseUrl
    return config


def setBaseUrl(ip="127.0.0.1", port=0, user="ARNTUSER", password="ARNTUSER", chart="utf8", drive_="sqlserver"):
    return configure_database(dict(upServer=ip, port=port, user=user, password=password,
        charset=chart, drive=drive_, database_type=getattr(CONFIG, "database_type", "ncdhotstrip"))).baseUrl


create = False
