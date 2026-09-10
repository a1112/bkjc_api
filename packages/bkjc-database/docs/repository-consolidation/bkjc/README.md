# bkjc consolidation and caller review

Source: https://github.com/a1112/bkjc at `f733a3e8bcee3fc27c1e943a12d6006d84f220ed`.
Maintained package: `bkjc_database/` at `f1ea4b7f4dcb871e7ff489781ffed903e86ea6c1`.
Caller examined: a1112/bkjc_api at `ee04908807d7c1b4767b8d766b6ca1a7f4351734`.

## Source preservation

The 98-file snapshot has 38 files already present by exact mode/blob, 21 inert
originals, two redacted configuration/core files and 37 excluded Python bytecode
files. The unusual `sqlserver/__pycache__/SteelRecord.py` is source code and is
preserved; only `.pyc` files are excluded. The manifest identifies every path.
Exact configuration bytes are retained in ignored local storage at
`.repository-consolidation-local/bkjc/`; back up this directory separately before
deleting the original local clone. Public Git only contains the redacted copy.

## Model and interface findings

- The mapped MySQL/SQL Server model definitions are already retained. The
  `ncdplate.py` difference only changes SQLAlchemy's `declarative_base` import.
- The maintained `Mysql_4d0` and `SqlServer_3d0` include all old public method
  names. Their semantics are not assumed equivalent: connection lifetime,
  configuration and object initialization changed.
- `dbm.py` now provides a lazy proxy instead of eager construction. Replacing it
  with the old source would undo this behavior.
- Old module functions in Ncdhotstrip, Ncdhotstripdefect, ConfigCenter and
  SteelRecord have moved into objects/classes. Their old implementations remain
  recoverable in originals; they are not installed as a second Python package.

## bkjc_api dependency blockers

The API imports `bkjc_database`, not a package from the `bkjc` repository. Deleting
the old bkjc repository after preservation does not itself switch these imports.
The API has its own `bkjc_database/` copy which takes precedence over an installed
package when launched from its checkout. Its requirements file also contains a
bare GitHub HTML URL, not an installable pinned VCS requirement.

Do not remove that vendored copy in this archival PR. A functional replacement
requires separate migration and database fixtures for these concrete contracts:

| Caller | Current incompatibility to resolve before replacing the vendored package |
|---|---|
| `api/dataSynchronizer/DefectSynchronizer.py` | Calls module-level `getLastDefectId`, `appendDefect`, `getDefectByDefectId`, `getSteelBySeqNo`; target exposes object methods. Target DefectDb returns one row/None while caller iterates. |
| Same synchronizer | Commits shared `defectinfodatabase.session`; replacement needs an explicit transaction boundary and incremental query contract, not aliases alone. |
| `core/init.py` | Uses `core.setBaseUrl` and CONFIG.database_type; target models inspect CONFIG.globDbConfig during import. Initialization order must be made explicit. |
| MySQL model imports | Target constructs instances and calls `createDatabase(Base.metadata)` during import; importing it for a test could create schema on a configured server. |

No live SQL Server/MySQL connection or DDL was run. No production database/API
code is changed. Byte-level preservation and static interface review establish
source retention, not runtime compatibility. These API blockers are pre-existing
and remain open; the API repository must be retained.

## Retirement

Merge this PR, recheck its manifest on the maintained branch and confirm the
source commit is unchanged before retiring bkjc. Back up the ignored config
original and any needed branches/history/hosted records separately. This PR is
an explicit historical archive, not a deployment or functional API migration.
