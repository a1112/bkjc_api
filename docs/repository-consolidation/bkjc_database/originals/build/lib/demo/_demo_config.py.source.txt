"""
Utility helpers shared by demo scripts.

Set the following environment variables before running any demo to point at a
real database instance:

BKJC_DRIVE     -> "mysql" (default) or "sqlserver"
BKJC_HOST      -> hostname/IP, defaults to 127.0.0.1
BKJC_PORT      -> optional port override (3306/1433 inferred by drive)
BKJC_USER      -> database user (root/ARNTUSER by default)
BKJC_PASSWORD  -> database password
BKJC_CHARSET   -> optional charset, defaults to utf8
"""

from __future__ import annotations

import os
from typing import Tuple

from bkjc_database import CONFIG, core
from bkjc_database.dbm import get_dbm


def _detect_drive(raw_drive: str | None) -> Tuple[str, CONFIG.DbConfigBase]:
    drive = (raw_drive or "mysql").strip().lower()
    if drive not in {"mysql", "sqlserver"}:
        raise ValueError(f"Unsupported BKJC_DRIVE value: {raw_drive}")
    if drive == "sqlserver":
        return drive, CONFIG.DbConfig3d0()
    return drive, CONFIG.DbConfig4d0()


def bootstrap_dbm():
    """
    Configure core connection parameters from environment variables and return
    a ready-to-use dbm object.
    """
    drive, config = _detect_drive(os.getenv("BKJC_DRIVE"))

    host = os.getenv("BKJC_HOST", "127.0.0.1")
    port = int(os.getenv("BKJC_PORT") or (1433 if drive == "sqlserver" else 3306))
    user = os.getenv("BKJC_USER") or ("ARNTUSER" if drive == "sqlserver" else "root")
    password = os.getenv("BKJC_PASSWORD") or ("ARNTUSER" if drive == "sqlserver" else "mercar")
    charset = os.getenv("BKJC_CHARSET", "utf8")

    core.setBaseUrl(
        ip=host,
        port=port,
        user=user,
        password=password,
        chart=charset,
        drive_=drive,
    )
    return get_dbm(config, reGet=True)


def print_banner(script_name: str, extra: str = ""):
    divider = "=" * 60
    print(divider)
    print(f"{script_name} demo")
    if extra:
        print(extra)
    print(divider)
