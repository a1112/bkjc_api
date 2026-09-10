# bkjc_tools

This package consolidates the CIMG Python wrapper and 31 DLL assets formerly held in `a1112/bkjc_tool`, together with the API's compatibility behavior. Import paths remain `bkjc_tools.CimgReadCore` and `bkjc_tools.cimg_read.CimgReadCore`.

Install from the API repository root with `python -m pip install -e ./packages/bkjc-tools`. Decoding requires **Windows x64 Python** and the vendor's runtime dependencies. Import and contract tests work without loading any vendor DLL.

DLLs load only on the first actual decode. Each numbered legacy decoder and the modern decoder serialize calls through a lock; unavailable libraries and decoding exceptions propagate and release the lock. Busy decoders wait without recursive polling. The package never copies DLLs into its installation directory or registers Windows shell handlers on import.

Assets resolve relative to the installed package, including in a PyInstaller bundle. Set `BKJC_CIMG_DLL_DIR` before import to explicitly use an external deployment directory. Legacy decoding expects the supplied `OldCimgRead0.dll` through `OldCimgRead7.dll`; it does not manufacture missing copies. `mspdb80.dll` is a historical x86 debugging asset retained from the source, not a decoder loaded by this wrapper. Other supplied decoder DLLs are x64.

The existing public image/array/buffer functions and legacy `systemVersion=0` / modern `systemVersion=1` selection remain available. The caller must provide the image's correct dimensions: the opaque vendor ABI takes a path and pointer, not a destination capacity. Python-side size checks cannot protect against a native decoder writing beyond that capacity or crashing on corrupt input.

Tests use fake decoders and known synthetic pixel bytes to validate dimensions, mode selection, load timing, concurrency, exceptions and retries. They do not establish real CIMG format correctness or vendor runtime compatibility. No vendor DLL is executed during this migration's tests.

`cimgOpen.py` and `ComCimg.py` preserve the optional historical Windows shell helpers; they are not automatic installation steps and have not been executed. The COM example is not a completed thumbnail provider. Original wrappers, metadata and editor files are retained under `docs/repository-consolidation/` at the API root. Existing source license declarations and third-party DLL ownership continue to apply; consolidation does not grant additional redistribution rights.
