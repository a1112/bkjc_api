from __future__ import annotations

import threading
from typing import Optional

from bkjc_database import CONFIG

_DBM_LOCK = threading.RLock()
_dbm_instance = None
_active_config: Optional[CONFIG.DbConfigBase] = None


def _get_dbm_(config: CONFIG.DbConfigBase):
    if config.drive == "sqlserver":
        from .ss.dbi import SqlServer_3d0 as SqlObj
    else:
        from .ms.dbi import Mysql_4d0 as SqlObj
    return SqlObj()


def _resolve_config(config: Optional[CONFIG.DbConfigBase]) -> CONFIG.DbConfigBase:
    if config:
        return config
    if CONFIG.globDbConfig:
        return CONFIG.globDbConfig
    return CONFIG.DbConfig4d0()


def init_dbm(config: CONFIG.DbConfigBase):
    """
    Force creation of a dbm instance with the provided configuration.
    """
    global _dbm_instance, _active_config
    with _DBM_LOCK:
        _active_config = config
        _dbm_instance = _get_dbm_(config)
        return _dbm_instance


def get_dbm(config: Optional[CONFIG.DbConfigBase] = None, reGet: bool = False):
    """
    Lazily return a dbm instance. When `reGet` is True a fresh instance is built
    using the provided (or resolved) configuration.
    """
    global _dbm_instance, _active_config
    resolved_config = _resolve_config(config)
    with _DBM_LOCK:
        if reGet:
            return _get_dbm_(resolved_config)
        if _dbm_instance is None or _active_config is not resolved_config:
            _active_config = resolved_config
            _dbm_instance = _get_dbm_(resolved_config)
        return _dbm_instance


class _LazyDbmProxy:
    """
    Proxy object so `from bkjc_database.dbm import dbm` still works while actual
    connections are established only when first used.
    """

    def __getattr__(self, item):
        target = get_dbm()
        return getattr(target, item)


dbm = _LazyDbmProxy()
