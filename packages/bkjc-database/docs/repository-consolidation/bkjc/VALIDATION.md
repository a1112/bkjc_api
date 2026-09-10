# Validation (2026-09-10)

The manifest covers all 98 source paths. Consumer matches and archived bytes
were verified using Git blob IDs and modes; both sensitive originals were
verified in the ignored local backup. All 37 excluded files are Python bytecode.

Static review compared the MySQL and SQL Server schema/interface definitions
and the bkjc_api call sites described in README.md. No active Python package file
was changed. No database import, connection, schema creation or live integration
test was run: model imports may create databases and no test database was supplied.

This establishes recoverable source preservation. It does not establish API
runtime compatibility or resolve the listed pre-existing caller blockers.
