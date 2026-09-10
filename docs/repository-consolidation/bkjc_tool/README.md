# a1112/bkjc_tool 整合到 bkjc_api

来源默认分支提交：`1c49e6ddb56bfd838eb5b896fe03c123d18614c9`。安装包目录：`packages/bkjc-tools/`。

用户明确允许审查后公开私有工具源码及 DLL。31 个 DLL 全部保留，其中解码器为 x64，mspdb80.dll 是历史 x86 调试资产。API 本地同名工具的独有文本另外归档；运行入口统一到此安装包。

逐文件来源路径、模式、Git blob 与接收路径见 [manifest.json](manifest.json)。调整过的文件保留原始字节；编译产物、字节码和工具配置只作惰性原文档案。源文件快照全部覆盖，原始署名及许可声明保留。

## 功能与验证

根目录 requirements 使用同仓库安装包，移除指向两个来源仓库的运行依赖。37 项测试覆盖数据库/API 契约及 CIMG 延迟装载、合成像素尺寸、并发锁、失败重试和输入校验。两个 wheel 构建及包外安装导入检查通过；DLL 和 JSON 资源完整，敏感备份不入包。测试使用 SQLite、最小模型和模拟解码器，没有连接生产库、执行 DDL、真实 CIMG DLL、COM 注册或 PLC。PyInstaller 已加入 DLL 数据 hook，但完整 API exe 未重建。

## 退役条件

本 PR 合并后，应重新核对目标默认分支 manifest、来源 HEAD、其他分支和外部调用方，再给出来源删除地址。独立消费者可从 API 仓库安装子目录包，例如 `bkjc_database @ git+https://github.com/a1112/bkjc_api.git@<reviewed-commit>#subdirectory=packages/bkjc-database`；工具对应 packages/bkjc-tools。当前两个来源仓库尚未删除。

范围是默认分支跟踪文件快照；完整 Git 历史、其他分支、Issues、Releases 和 GitHub 设置不包含在文件迁移中。必须保留接收项目的 `.repository-consolidation-local` 配置原件；这些备份不可随来源本机目录一起清理。
