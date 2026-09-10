# bkjc_api 统一依赖契约

API 原来内置 `bkjc_database/`，会遮蔽安装版本。本次与 API 的配套 PR 将调用方切换到固定提交的维护库；两仓库继续独立维护，不属于可删除项目。

## 初始化和返回值

使用 `core.configure_database(info)`（drive、database_type、upServer、user、password、可选 port/charset）设置配置，再 `dbm.init_dbm(config)` 获取惰性代理。密码按 URL 编码且不打印。模型随首次导入选择 schema；一个进程使用一种数据库配置，切换现场或 schema 应重启进程。默认 API 服务不在 import 时创建 MySQL schema。DbItem 仅在调用 Session 时连接；数据库建表仍需显式 createDatabase(metadata) 和相应权限。

`getSteelBySequence(number, start_seq_no)` 按 seqNo/SequeceNo 升序读取严格大于游标的记录，统一返回 `[steel, identifier]` 的列表。MySQL 不要求可选的属性行存在。原 `getSteelByNum` 的 ID 游标契约保留；SQL Server 序号和内部 ID 不混用。旧设备 `getRkmonitorInfo()` 的 None 占位行为保留。

## 同步事务

`sync_defects_once(source, steels, destination, batch_size)` 使用有界升序批次；camera 1 对应 Top=1，camera 2 对应 Top=0。每个表面一个目标 Session/事务，读取已提交最大 defectNo，写入后统一提交。缺钢板、源查询错误、顺序/相机错误和提交失败均回滚当前表面的批次；重试重新读取游标。另一表面可能已提交，下一轮会从它的已提交游标继续。

这是单同步 worker 的增量契约，不是分布式并发去重。现有数据库必须已存在；不会运行 DDL。尚未验证断号后补写、生产数据修订或并行同步，需要相应部署约束。

## 验证

```sh
python -m pip install . pytest
python -m pytest tests/test_api_contract.py -q
```

Python 3.12 / SQLAlchemy 2.0.52 下 16 项离线测试通过：两个配置驱动、两套 MySQL 模型选择及禁止 import 连接/DDL、增量边界与分页、重试/回滚、MySQL 返回结构和 SQL Server 双游标。SQLite 测试使用最小 SQL Server 字段映射，不能替代真实驱动、反射和现场 schema 验收。没有执行线上 MySQL/SQL Server smoke、读写或 DDL；上线前仍需用脱敏现场配置运行原 demo/testMySql.py、demo/testSqlServer.py，并记录结果。包元数据补齐运行依赖，Python 下限调整到源码实际要求的 3.10。
