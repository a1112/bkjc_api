"""Check wheel payloads independently of editable imports and source checkouts."""
import hashlib
from pathlib import Path
import sys
import zipfile

root = Path(__file__).resolve().parents[1]
directory = Path(sys.argv[1])
for package, folder in [("bkjc_database", "bkjc-database"), ("bkjc_tools", "bkjc-tools")]:
    wheels = list(directory.glob(package + "-*.whl"))
    assert len(wheels) == 1, (package, wheels)
    with zipfile.ZipFile(wheels[0]) as archive:
        names = set(archive.namelist())
        assert package + "/__init__.py" in names
        assert not any(".repository-consolidation-local" in n or "/__pycache__/" in n or "/originals/" in n or n.endswith(".pyc") for n in names)
        metadata = archive.read(next(n for n in names if n.endswith(".dist-info/METADATA"))).decode()
        assert "git+" not in metadata
        if package == "bkjc_tools":
            assets = list((root / "packages" / folder / package / "dll/x64").glob("*.dll"))
            assert len(assets) == 31
            for path in assets:
                payload = archive.read(package + "/dll/x64/" + path.name)
                assert hashlib.sha256(payload).digest() == hashlib.sha256(path.read_bytes()).digest(), path.name
        else:
            assert package + "/NerCarDataBase/config/DBconfig.json" in names
            assert package + "/sync.py" in names
    print(f"Verified {wheels[0].name}")
