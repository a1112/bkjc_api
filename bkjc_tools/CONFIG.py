from pathlib import Path
import os
import sys

DLL_PATH = Path(__file__).parent / "dll/x64" if "python.exe" in sys.executable.lower() else Path(
    sys.executable).parent / "dll/x64"
WIDTH = 4096
HEIGHT = 1024
POOL_SIZE = 8
