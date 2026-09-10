# bkjc_api

数据库实现来自固定提交的 `a1112/bkjc_database`，安装入口为 requirements.txt。同名内置数据库包已转为惰性档案，完整记录见 [依赖迁移](docs/dependency-consolidation/bkjc_database/README.md)。`bkjc_tools` 的本地 CIMG 实现继续保留。

```sh
python -m venv .venv
# 激活虚拟环境后
python -m pip install -r requirements.txt
python -m pytest tests/test_database_dependency.py -q
```

最低 Python 3.10。测试不会启动设备或连接数据库。运行 API 前按现有配置选择现场，并先通过 core.init.initDataBase(info) 完成配置；每进程仅使用一套数据库配置。`info.port` 仍是 HTTP 监听端口；数据库端口使用独立可选字段 `db_port`，未设置时采用 MySQL 3306 / SQL Server 1433。真实 MySQL/SQL Server、CIMG 与完整服务仍需现场验收。数据库配套 PR 应先于 API PR 合并，旧 dist/Server 中的二进制需要另行重建。
