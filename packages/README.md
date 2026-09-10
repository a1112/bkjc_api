# Shared packages in bkjc_api

- `bkjc-database/`: maintained MySQL/SQL Server package, including demos and offline contracts.
- `bkjc-tools/`: CIMG wrappers, DLL assets and historical optional shell utilities.

From the repository root:

```sh
python -m pip install -r requirements.txt
# Small contract-test environment, without full API/device dependencies:
python -m pip install -r requirements-contract.txt
python -m pytest tests/test_database_dependency.py tests/test_cimg_contract.py packages/bkjc-database/tests/test_api_contract.py -q
```

Both dependency lists install the packages from this checkout. There is no runtime Git requirement on either source repository. Keep packages below this directory rather than adding root-level `bkjc_database/` or `bkjc_tools/` folders that could shadow an installed version.

Build distributable wheels independently with `python -m pip wheel --no-deps ./packages/bkjc-database ./packages/bkjc-tools --wheel-dir <output-directory>`. PyInstaller's `hooks/hook-bkjc_tools.py` collects the package-relative DLL assets; rebuild the API executable after installing these packages. Previously committed executables are historical and have not been rebuilt by this change.

Source retention and local configuration backups are described in `docs/repository-consolidation/bkjc_database/` and `docs/repository-consolidation/bkjc_tool/`. Those source repositories may enter retirement review only after the consolidation PR is merged and the default-branch manifests are rechecked.
