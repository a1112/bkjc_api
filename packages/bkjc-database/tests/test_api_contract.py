"""Deterministic SQLite contracts; never connect to deployment databases."""
import importlib
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest
from sqlalchemy import BigInteger, Column, Integer, String, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import declarative_base, sessionmaker

from bkjc_database import CONFIG, core
from bkjc_database.sync import sync_defects_once


@compiles(TINYINT, "sqlite")
def tinyint_sqlite(type_, compiler, **kwargs):
    return "INTEGER"


@compiles(BigInteger, "sqlite")
def bigint_sqlite(type_, compiler, **kwargs):
    return "INTEGER"


@pytest.mark.parametrize("drive,port", [("mysql", 3306), ("sqlserver", 1433)])
def test_configuration_is_explicit_and_does_not_print_credentials(drive, port, capsys):
    from sqlalchemy.engine import make_url
    config = core.configure_database(dict(drive=drive, database_type="ncdplate", user="test@user", password="a:{b}@/c", upServer="example.invalid"))
    parsed = make_url(config.baseUrl.format("fixture"))
    assert parsed.username == "test@user" and parsed.password == "a:{b}@/c"
    assert parsed.port == port and parsed.database == "fixture"
    assert CONFIG.globDbConfig is config
    assert config.database_type == "ncdplate"
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("settings", [{"drive": "oracle"}, {"database_type": "unknown"}])
def test_invalid_configuration_rejected(settings):
    with pytest.raises(ValueError):
        core.configure_database(dict(user="test", password="test", **settings))


@pytest.mark.parametrize("schema", ["ncdhotstrip", "ncdplate"])
def test_mysql_model_imports_do_not_connect_or_create_schema(schema):
    script = '''
import sqlalchemy
from sqlalchemy.schema import MetaData
def forbidden(*a, **k): raise AssertionError("Unexpected database access")
sqlalchemy.create_engine = forbidden
MetaData.create_all = forbidden
from bkjc_database import core
core.configure_database(dict(drive="mysql", database_type=SCHEMA, user="fixture", password="fixture"))
from bkjc_database.NerCarDataBase.mysql import Ncdhotstrip, Ncdhotstripdefect, Ncdplatedevice, defectinfodatabase
assert Ncdhotstripdefect.Camdefect1.__module__.endswith("ncdhotstripdefect" if SCHEMA == "ncdhotstrip" else "ncdplatedefect")
assert Ncdplatedevice.deviceDb.getRkmonitorInfo() is None
'''.replace("SCHEMA", repr(schema))
    subprocess.run([sys.executable, "-c", script], check=True, capture_output=True, text=True)


def test_init_dbm_defers_connection_until_use(monkeypatch):
    from bkjc_database import dbm
    cfg = CONFIG.DbConfig3d0()
    calls = []
    sentinel = SimpleNamespace(isSqlServer=lambda: True)
    monkeypatch.setattr(dbm, "_get_dbm_", lambda config: calls.append(config) or sentinel)
    proxy = dbm.init_dbm(cfg)
    assert calls == []
    assert proxy.isSqlServer() is True
    assert calls == [cfg]


@pytest.fixture
def destination():
    core.configure_database(dict(drive="mysql", user="fixture", password="fixture"))
    from bkjc_database.NerCarDataBase.mysql.defectinfodatabase import DefectInfoDb
    from bkjc_database.NerCarDataBase.mysql.models.defectinfodatabase import Base
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    db = DefectInfoDb()
    db.Session = sessionmaker(bind=engine)
    yield db
    engine.dispose()


def defect(number, camera=1, seq=10):
    return SimpleNamespace(defectID=number, camNo=camera, seqNo=seq, topInObj=2,
        bottomInObj=9, leftToEdge=3, rightToEdge=4, leftInObj=5, rightInObj=8, imgIndex=6)


class Source:
    def __init__(self, rows): self.rows = rows
    def getDefectsAfter(self, camera, cursor, limit):
        return sorted([r for r in self.rows if r.camNo == camera and r.defectID > cursor], key=lambda r: r.defectID)[:limit]


def steels():
    return SimpleNamespace(getSteelBySeqNo=lambda seq: SimpleNamespace(steelID="steel-"+str(seq)))


def test_incremental_sync_uses_correct_surfaces_and_does_not_duplicate(destination):
    source = Source([defect(5), defect(2), defect(8, 2)])
    assert sync_defects_once(source, steels(), destination, 1) == 2
    assert sync_defects_once(source, steels(), destination, 1) == 1
    assert sync_defects_once(source, steels(), destination, 1) == 0
    with destination.Session() as session:
        assert destination.getLastDefectId(1, session) == 5
        assert destination.getLastDefectId(0, session) == 8
        row = destination.getLastDefect(1, session)
        assert row.defectLen == 7 and row.defectwidth == 3


def test_missing_steel_rolls_back_whole_surface_batch(destination):
    source = Source([defect(2), defect(3, seq=11)])
    lookup = SimpleNamespace(getSteelBySeqNo=lambda seq: SimpleNamespace(steelID="ok") if seq == 10 else None)
    with pytest.raises(ValueError, match="Missing steel"):
        sync_defects_once(source, lookup, destination)
    with destination.Session() as session:
        assert destination.getLastDefectId(1, session) == 0
    assert sync_defects_once(source, steels(), destination) == 2


def test_query_failure_does_not_advance_cursor(destination):
    def fail(*args): raise RuntimeError("source unavailable")
    with pytest.raises(RuntimeError):
        sync_defects_once(SimpleNamespace(getDefectsAfter=fail), steels(), destination)
    with destination.Session() as session:
        assert destination.getLastDefectId(1, session) == 0


def test_commit_failure_rolls_back_and_closes_session(destination):
    from sqlalchemy import event
    source = Source([defect(1)])
    def fail_commit(session):
        session.flush()
        raise RuntimeError("commit failed")
    event.listen(destination.Session, "before_commit", fail_commit)
    try:
        with pytest.raises(RuntimeError, match="commit failed"):
            sync_defects_once(source, steels(), destination)
    finally:
        event.remove(destination.Session, "before_commit", fail_commit)
    with destination.Session() as session:
        assert destination.getLastDefectId(1, session) == 0
    assert sync_defects_once(source, steels(), destination) == 1


@pytest.mark.parametrize("rows", [[defect(3), defect(2)], [defect(1, 2)]])
def test_invalid_source_order_or_camera_rolls_back(destination, rows):
    with pytest.raises(ValueError):
        sync_defects_once(SimpleNamespace(getDefectsAfter=lambda *args: rows), steels(), destination)
    with destination.Session() as session:
        assert destination.getLastDefectId(1, session) == 0


def test_incremental_defect_query_is_strict_ordered_and_bounded(monkeypatch):
    core.configure_database(dict(drive="mysql", user="fixture", password="fixture"))
    module = importlib.import_module("bkjc_database.NerCarDataBase.mysql.Ncdhotstripdefect")
    engine = create_engine("sqlite://")
    module.Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    monkeypatch.setattr(module.defectDb, "Session", sessions)
    with sessions.begin() as session:
        session.add_all([module.Camdefect1(defectID=n, seqNo=1, camNo=1) for n in (9, 3, 6)])
        session.add(module.Camdefect2(defectID=4, seqNo=1, camNo=2))
    assert [r.defectID for r in module.defectDb.getDefectsAfter(1, 3, 1)] == [6]
    assert [r.defectID for r in module.defectDb.getDefectsAfter(2, 0)] == [4]
    assert module.defectDb.getDefectsAfter(1, 99) == []
    with pytest.raises(ValueError): module.defectDb.getDefectsAfter(3, 0)
    engine.dispose()


def test_mysql_sequence_query_preserves_pair_shape_without_property_row(monkeypatch):
    core.configure_database(dict(drive="mysql", user="fixture", password="fixture"))
    module = importlib.import_module("bkjc_database.ms.dbi")
    base = declarative_base()
    class Steel(base):
        __tablename__ = "steel"
        seqNo = Column(Integer, primary_key=True)
        steelID = Column(String)
    engine = create_engine("sqlite://")
    base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    monkeypatch.setattr(module.Ncdhotstrip, "Steelrecord", Steel)
    monkeypatch.setattr(module.Ncdhotstrip, "Session", sessions)
    with sessions.begin() as session:
        session.add_all([Steel(seqNo=n, steelID=str(n)) for n in (7, 1, 4)])
    rows = module.Mysql_4d0().getSteelBySequence(1, 1)
    assert len(rows) == 1 and len(rows[0]) == 2
    assert rows[0][0].seqNo == 4 and rows[0][1] == "4"
    engine.dispose()


def test_sqlserver_sequence_cursor_is_distinct_from_internal_id(monkeypatch):
    # Run actual SQLAlchemy query logic with fixture mappings; no schema introspection.
    import types
    base = declarative_base()
    class Steel(base):
        __tablename__ = "steel"
        ID = Column(Integer, primary_key=True)
        SequeceNo = Column(Integer)
        SteelID = Column(Integer)
    class SteelID(base):
        __tablename__ = "steel_id"
        ID = Column(Integer, primary_key=True)
    engine = create_engine("sqlite://")
    base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    with sessions.begin() as session:
        session.add_all([Steel(ID=1, SequeceNo=30), Steel(ID=50, SequeceNo=10), Steel(ID=3, SequeceNo=20)])
    prefix = "bkjc_database.NerCarDataBase.sqlserver."
    for name in ("ClientDefectDB", "ConfigCenter", "SteelRecord"):
        stub = types.ModuleType(prefix+name)
        if name == "SteelRecord": stub.Steel, stub.SteelID, stub.Session = Steel, SteelID, sessions
        monkeypatch.setitem(sys.modules, prefix+name, stub)
    sys.modules.pop("bkjc_database.ss.dbi", None)
    module = importlib.import_module("bkjc_database.ss.dbi")
    db = module.SqlServer_3d0()
    assert [row[0].SequeceNo for row in db.getSteelBySequence(10, 15)] == [20, 30]
    assert [row[0].ID for row in db.getSteelByNum(10, startID=10)] == [50]
    engine.dispose()
