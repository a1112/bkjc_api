"""Exercise the installed dependency without starting API modules or devices."""
import importlib.util
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_file(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_checkout_does_not_shadow_installed_database():
    script = "import bkjc_database; from pathlib import Path; print(Path(bkjc_database.__file__).resolve())"
    result = subprocess.run([sys.executable, "-c", script], cwd=ROOT, capture_output=True, text=True, check=True)
    package_file = Path(result.stdout.strip())
    assert not package_file.is_relative_to(ROOT)
    assert not (ROOT / "bkjc_database/__init__.py").exists()


@pytest.mark.parametrize("drive", ["mysql", "sqlserver"])
def test_api_configuration_initializes_maintained_lazy_proxy(drive, monkeypatch):
    from bkjc_database import CONFIG, dbm
    def forbidden(*args): raise AssertionError("Configuration must not connect")
    monkeypatch.setattr(dbm, "_get_dbm_", forbidden)
    module = load_file("api_database_init_contract", "core/init.py")
    proxy = module.initDataBase(dict(drive=drive, database_type="ncdplate", upServer="test.invalid", user="fixture", password="fixture", port=809))
    assert proxy is dbm.dbm and CONFIG.globDbConfig.drive == drive
    assert CONFIG.globDbConfig.database_type == "ncdplate"
    from sqlalchemy.engine import make_url
    assert make_url(CONFIG.globDbConfig.baseUrl.format("test")).port == (3306 if drive == "mysql" else 1433)
    module.initDataBase(dict(drive=drive, upServer="test.invalid", user="fixture", password="fixture", port=809, db_port=12345))
    assert make_url(CONFIG.globDbConfig.baseUrl.format("test")).port == 12345


def test_synchronizer_calls_shared_contract_without_legacy_module_functions(monkeypatch):
    module = load_file("api_synchronizer_contract", "api/dataSynchronizer/DefectSynchronizer.py")
    calls = []
    monkeypatch.setattr(module, "sync_defects_once", lambda *args: calls.append(args) or 3)
    source, steels, destination = object(), object(), object()
    sync = module.DefectSynchronizer(source, steels, destination, batch_size=25)
    assert sync.run_once() == 3
    assert calls == [(source, steels, destination, 25)]
    sync.stop()
    sync.run()
    assert len(calls) == 1


def test_sequence_route_uses_explicit_sequence_cursor():
    import ast
    tree = ast.parse((ROOT / "api/api_defect_view/api_steel_get.py").read_text("utf-8"))
    method = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "getSteelList")
    method.decorator_list = []
    calls = []
    backend = SimpleNamespace(getSteelBySequence=lambda *args: calls.append(args) or [["steel", "id"]], isSqlServer=lambda: False)
    namespace = {"dbm": backend, "addSteelCache": lambda steel, identifier: (steel, identifier)}
    exec(compile(ast.Module(body=[method], type_ignores=[]), "api_steel_get.py", "exec"), namespace)
    assert namespace["getSteelList"](10, 100) == [("steel", "id")]
    assert calls == [(10, 100)]
