# Repository Guidelines

## Project Structure & Module Organization
`bkjc_database/` is the installable package. Core connection helpers (`SqlBase.py`, `SqlTool.py`, `dbm.py`, `core.py`) live at the package root; keep new adapters beside them to stay discoverable. Connector-specific shims sit in `ms/` (MySQL) and `ss/` (SQL Server), while `NerCarDataBase/` contains vendor schemas under `mysql/`, `sqlserver/`, and `SqlManage/`. Interactive smoke tests now live under `demo/` (see `_demo_config.py`, `testMySql.py`, `testSqlServer.py`, `defect_overview.py`, `steel_timeline.py`, `export_defect_classes.py`). Legacy probes that ship with the package stay under `bkjc_database/test/`. Assets such as `DefectClass.json` and utility scripts (`mp4tojpg.py`) remain in the repository root for shared access.

## Build, Test, and Development Commands
1. Create an isolated environment: `python -m venv .venv && .\.venv\Scripts\activate`.
2. Install deps for local hacking: `pip install -r requirements.txt`.
3. Install the package itself (editable keeps imports stable): `pip install -e .` or run `install.bat`.
4. Configure demo env vars (`BKJC_DRIVE`, `BKJC_HOST`, `BKJC_USER`, `BKJC_PASSWORD`, optional `BKJC_SEQ_NO`, etc.) and run `python demo/testMySql.py` or `python demo/testSqlServer.py`.
5. Run targeted demos as needed:
   - `python demo/defect_overview.py` summarizes per-camera defect counts for `BKJC_SEQ_LIST`.
   - `python demo/steel_timeline.py` lists steels in a rolling date window (`BKJC_TIMELINE_DAYS`).
   - `python demo/export_defect_classes.py` exports `getDefectClass()` data into `demo/output/defect_classes.json`.
6. Legacy link verification: `python -m bkjc_database.test.LinkMysql` to confirm credentials defined in `CONFIG.DbConfig3d0()`.

## Coding Style & Naming Conventions
Target Python ≥3.6 and follow PEP 8 (4-space indents, lower_snake_case functions, PascalCase classes). Module filenames stay short and descriptive (`dbm.py`, `SqlTool.py`); mirror that pattern for new adapters. Central configuration objects extend `DbConfigBase` in `CONFIG.py`; reuse that inheritance model and avoid hard-coding secrets outside config classes. When adding SQL helpers, keep method names action-oriented (`getSteelBy…`, `getDefectBy…`) and guard raw queries inside helper methods so interface modules stay declarative.

## Testing Guidelines
This project uses pragmatic integration scripts instead of a test runner. Mirror the `test*.py` naming when adding scenarios, and focus on deterministic IDs (e.g., `dbm.getSteelById(1)`) so failures are easy to triage. Populate local fixtures in `DefectClass.json` when validating classification lookups. For code touching both `ms` and `ss` backends, run both smoke scripts and capture elapsed time (`time:` output) plus the expected tuple counts in the PR description. Add unit-style checks under `bkjc_database/test/` only when they do not require live database credentials.

## Commit & Pull Request Guidelines
Recent history (`git log -5 --oneline`) shows short, imperative subjects such as `ch dbi`, `ADD CRATE`, and `重构`. Keep following that style: ≤50 characters, component prefix when helpful (`dbm: guard null steel IDs`), and present tense verbs. Each PR should describe the database(s) exercised, link to any issue IDs, and include console excerpts for the scripts above so reviewers can verify DB reachability. Add screenshots only when schema diffs or defect-class tables change.

## Security & Configuration Tips
Connection details live in `CONFIG.py` and via `core.setBaseUrl(...)`. Never commit real passwords—create local-only subclasses (e.g., `DbConfigLocal`) or read from environment variables before instantiating `DbConfigBase`. Keep `DefectClass.json` anonymized; if sensitive classes are required for debugging, attach them through a secure channel instead of Git.
