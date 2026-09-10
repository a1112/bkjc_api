"""Package-relative assets, with an explicit deployment override."""
from pathlib import Path
import os

DLL_PATH = Path(os.environ["BKJC_CIMG_DLL_DIR"]).expanduser().resolve() if os.environ.get("BKJC_CIMG_DLL_DIR") else Path(__file__).resolve().parent / "dll/x64"
WIDTH = 4096
HEIGHT = 1024
POOL_SIZE = 8
