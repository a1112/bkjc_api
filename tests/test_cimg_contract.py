"""CIMG wrapper contracts with fake decoders; vendor DLLs are never executed."""
import concurrent.futures
import ctypes
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace

import numpy as np
import pytest

from bkjc_tools import CimgReadCore as cimg


@pytest.fixture
def source(tmp_path):
    p = tmp_path / "fixture.cimg"
    p.write_bytes(b"synthetic wrapper fixture, not a vendor image")
    return p


def test_import_does_not_load_decoders_or_copy_files():
    script = '''
# Allow NumPy/Pillow to initialize their own runtime, then guard vendor imports.
import numpy
from PIL import Image
import ctypes, shutil, os
def forbidden(*args, **kwargs): raise AssertionError("Native decoder or copy called on import")
ctypes.CDLL = forbidden
shutil.copy = forbidden
os.add_dll_directory = forbidden
from bkjc_tools import CimgReadCore
assert CimgReadCore.CimgReadDll.dll is None
assert all(reader.dll is None for reader in CimgReadCore.oldCimgDllList)
'''
    subprocess.run([sys.executable, "-c", script], check=True, capture_output=True, text=True)


@pytest.mark.parametrize("version", [0, 1])
def test_decode_preserves_dimensions_pixels_and_mode(monkeypatch, source, version):
    calls = []
    expected = bytes(range(12))
    def load(path):
        def decode(filename, buff):
            calls.append((Path(path).name, filename))
            ctypes.memmove(buff, expected, len(expected))
        return SimpleNamespace(ReadCimgData=decode)
    monkeypatch.setattr(cimg, "loadDll", load)
    monkeypatch.setattr(cimg, "oldCimgDllList", [cimg.OldCimgRead(0)])
    monkeypatch.setattr(cimg, "CimgReadDll", cimg.OldCimgRead(0, filename="CimgRead.dll"))
    arr = cimg.ReadCimgToNumpyArray(source, 4, 3, systemVersion=version)
    assert arr.shape == (3, 4) and arr.dtype == np.uint8
    assert arr.tobytes() == expected
    image = cimg.ReadCimgToImage(source, 4, 3, systemVersion=version)
    assert image.size == (4, 3) and image.mode == "L" and image.tobytes() == expected
    assert calls[0][0] == ("CimgRead.dll" if version else "OldCimgRead0.dll")


def test_each_decoder_loads_once_and_serializes_concurrent_calls(monkeypatch, source):
    load_calls = []
    counter_lock = threading.Lock()
    active, maximum = 0, 0
    entered = threading.Event()
    release = threading.Event()
    def load(path):
        load_calls.append(path)
        def decode(filename, buff):
            nonlocal active, maximum
            with counter_lock:
                active += 1
                maximum = max(maximum, active)
            entered.set()
            assert release.wait(10)
            ctypes.memmove(buff, b"\x01\x02", 2)
            with counter_lock:
                active -= 1
        return SimpleNamespace(ReadCimgData=decode)
    monkeypatch.setattr(cimg, "loadDll", load)
    monkeypatch.setattr(cimg, "oldCimgDllList", [cimg.OldCimgRead(0)])
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        first = pool.submit(cimg.ReadCimgData, source, 2)
        assert entered.wait(10)
        pending = [pool.submit(cimg.ReadCimgData, source, 2) for _ in range(7)]
        release.set()
        assert all(job.result(timeout=5).raw == b"\x01\x02" for job in [first]+pending)
    assert maximum == 1 and len(load_calls) == 1


def test_load_failure_releases_lock_and_can_retry(monkeypatch, source):
    calls = []
    reader = cimg.OldCimgRead(0)
    def load(path):
        calls.append(path)
        if len(calls) == 1: raise OSError("missing runtime")
        return SimpleNamespace(ReadCimgData=lambda name, buff: ctypes.memmove(buff, b"a", 1))
    monkeypatch.setattr(cimg, "loadDll", load)
    monkeypatch.setattr(cimg, "oldCimgDllList", [reader])
    with pytest.raises(OSError): cimg.ReadCimgData(source, 1)
    assert not reader.locked() and reader.dll is None
    assert cimg.ReadCimgData(source, 1).raw == b"a"


def test_decode_exception_releases_lock(monkeypatch, source):
    calls = []
    def decode(name, buff):
        calls.append(name)
        if len(calls) == 1: raise RuntimeError("decoder failure")
        ctypes.memmove(buff, b"b", 1)
    reader = cimg.OldCimgRead(0)
    monkeypatch.setattr(cimg, "loadDll", lambda path: SimpleNamespace(ReadCimgData=decode))
    monkeypatch.setattr(cimg, "oldCimgDllList", [reader])
    with pytest.raises(RuntimeError): cimg.ReadCimgData(source, 1)
    assert not reader.locked()
    assert cimg.ReadCimgData(source, 1).raw == b"b"


@pytest.mark.parametrize("size", [0, -1, True, 1.5, cimg.MAX_BUFFER_SIZE+1])
def test_invalid_buffer_size_fails_before_loading(monkeypatch, source, size):
    monkeypatch.setattr(cimg, "loadDll", lambda *args: pytest.fail("must not load"))
    with pytest.raises(ValueError): cimg.ReadCimgData(source, size)


def test_missing_file_and_invalid_mode_do_not_load(monkeypatch, tmp_path, source):
    monkeypatch.setattr(cimg, "loadDll", lambda *args: pytest.fail("must not load"))
    with pytest.raises(FileNotFoundError): cimg.ReadCimgData(tmp_path / "missing", 1)
    with pytest.raises(ValueError): cimg.ReadCimgData(source, 1, systemVersion=3)
    with pytest.raises(ValueError): cimg.ReadCimgData("bad\0name", 1)
    with pytest.raises(TypeError): cimg.ReadCimgDataToBuff(ctypes.c_void_p(), source)


def test_empty_pool_fails_without_recursive_retry(monkeypatch, source):
    monkeypatch.setattr(cimg, "oldCimgDllList", [])
    with pytest.raises(RuntimeError, match="No legacy"):
        cimg.ReadCimgData(source, 1)


def test_unsupported_platform_fails_explicitly(monkeypatch):
    monkeypatch.setattr(cimg.sys, "platform", "linux")
    with pytest.raises(RuntimeError, match="Windows x64"):
        cimg.loadDll("unused.dll")


def test_loader_closes_search_handle_when_library_load_fails(monkeypatch, tmp_path):
    dll = tmp_path / "decoder.dll"
    dll.write_bytes(b"not executable; loader is mocked")
    handle = SimpleNamespace(closed=False)
    handle.close = lambda: setattr(handle, "closed", True)
    monkeypatch.setattr(cimg.sys, "platform", "win32")
    monkeypatch.setattr(cimg.os, "add_dll_directory", lambda path: handle, raising=False)
    def fail(*args, **kwargs): raise OSError("fixture error")
    monkeypatch.setattr(cimg.ctypes, "CDLL", fail)
    with pytest.raises(OSError): cimg.loadDll(dll)
    assert handle.closed


def test_packaged_decoder_assets_exist():
    directory = Path(cimg.DLL_PATH)
    assert (directory / "CimgRead.dll").is_file()
    assert all((directory / f"OldCimgRead{i}.dll").is_file() for i in range(8))
