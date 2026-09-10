# bkjc_database

Shared MySQL and SQL Server access for bkjc_api. Python 3.10 or newer is required.

Install with `python -m pip install .`. Configure the database explicitly before importing driver models. See [API dependency contracts](docs/api-dependency-contract.md) for initialization, sequence cursors, transaction boundaries and offline validation.

Run `python -m pytest tests/test_api_contract.py -q` after installing pytest. These tests use SQLite and fixtures; the existing scripts in `demo/` still require a configured deployment database.
