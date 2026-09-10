# 原 API 本地 bkjc_tools 保留记录

原 API 包的 38 个跟踪文件逐项记录在 manifest.json：相同 DLL/源码引用新的同仓库工具包，差异文本保留原始字节。原 API 的 loadDll 早退、错误吞掉后空池递归，以及独立工具在 import 时装载/复制 DLL 的行为都不再作为运行实现；新的统一包装器使用延迟加载、单解码器锁和明确失败。

API 的高层图片、NumPy 数组和缓冲区函数保持入口兼容。底层 ReadCimgDataToBuff 现在要求有容量的 ctypes 数组；不接受无法验证容量的裸指针。真实解码仍受厂商 ABI 和部署运行库约束，模拟测试不代表真实 CIMG 验收。
