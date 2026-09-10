# 移除同名内置包，使用固定维护库

原 `bkjc_database/` 的 64 个跟踪文件已保存到 [manifest.json](manifest.json) 和惰性原文档案，避免再遮蔽 pip 安装包。原 CONFIG.py 的完整内容在迁移机器 `.repository-consolidation-local/bkjc_api/bkjc_database/CONFIG.py`，必须单独备份；这里只提交遮蔽后的记录。原 Git 提交也记录于清单。

配套数据库 PR 提供显式惰性初始化、成对返回的序号查询、缺陷增量接口和事务边界。API 通过 requirements.txt 固定到已审查的数据库提交。请先合并数据库 PR，再合并本 API PR；构建/部署时应重新安装依赖和重建打包产物，旧 dist 文件不代表已升级。

验证：5 项 API 契约测试通过（从 checkout 导入安装包、两种驱动初始化、同步适配与序号路由），数据库侧 16 项离线测试通过。未启动完整 API、现场数据同步、PLC、真实数据库或 CIMG DLL；这些功能的部署验收仍需现场环境。

## bkjc_tool / CIMG 审查结论

保留本仓库的 bkjc_tools 和独立 a1112/bkjc_tool。相同模块名不能证明可互换：API 版本 loadDll 提前返回 None，调用路径和池初始化与独立工具不同；独立工具在导入时装载 DLL 并创建池。本次未执行 DLL 或替换解码实现。requirements 中去掉了不可安装且会与本地实现冲突的裸 bkjc_tool URL。后续统一需有已知像素校验值的 CIMG 样本、DLL 版本和失败/并发测试，当前不列删除。

API、数据库和 bkjc_tool 三个仓库均保留。本次完成依赖代码整合，不是现场升级验收。
