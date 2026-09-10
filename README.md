# bkjc_api

API、数据库访问和 CIMG 工具在同一个仓库维护：

| 目录 | 用途 |
|---|---|
| `api/`、`core/` | API 与现场业务 |
| `packages/bkjc-database/` | MySQL/SQL Server 安装包、示例和契约测试 |
| `packages/bkjc-tools/` | CIMG 安装包、31 个 DLL 与可选历史 Shell 工具 |

```sh
# 从仓库根目录执行，Python >= 3.10
python -m venv .venv
# 激活虚拟环境后
python -m pip install -r requirements.txt
# 只运行离线契约测试时可安装较小依赖集：
python -m pip install -r requirements-contract.txt
python -m pytest tests/test_database_dependency.py tests/test_cimg_contract.py packages/bkjc-database/tests/test_api_contract.py -q
```

依赖从当前 checkout 的两个包目录安装，不再从独立 bkjc_database / bkjc_tool 仓库拉取。包布局和 wheel/PyInstaller 用法见 [packages/README.md](packages/README.md)。

API 通过 `core.init.initDataBase(info)` 配置数据库，每进程使用一套配置。`info.port` 是 HTTP 监听端口，数据库端口使用可选 `db_port`（默认 MySQL 3306 / SQL Server 1433）。配置要在模型导入前完成，不会因导入 MySQL 模型而自动创建 schema。

CIMG 模块导入时不装载厂商 DLL。实际解码只支持 Windows x64，使用包内 DLL 或显式的 `BKJC_CIMG_DLL_DIR`；调用者仍需提供正确的图像尺寸。真实 CIMG 像素、现场数据库、PLC 和完整 API 服务未在离线测试中验收。旧 `dist/` 二进制需要重新打包。

本轮 37 项离线测试、两个 wheel 构建及安装载荷检查通过。迁移说明见 [数据库](docs/repository-consolidation/bkjc_database/README.md)、[CIMG 工具](docs/repository-consolidation/bkjc_tool/README.md)。上一轮去除内置数据库副本的记录仍保留在 [历史依赖迁移](docs/dependency-consolidation/bkjc_database/README.md)。
