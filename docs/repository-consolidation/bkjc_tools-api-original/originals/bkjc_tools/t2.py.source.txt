import os
import sys
import ctypes
import platform


def load_dll():
    # 1. 设置 DLL 路径
    dll_dir = r"D:\LCX\BKJC\bkjc_api\bkjc_tools\dll\x64"
    dll_path = os.path.join(dll_dir, "OldCimgRead0.dll")

    # 2. 检查文件是否存在
    if not os.path.exists(dll_path):
        print(f"[错误] DLL 文件不存在: {dll_path}")
        return None

    # 3. 添加路径到系统环境变量
    os.environ['PATH'] = dll_dir + ';' + os.environ['PATH']

    # 4. 检查系统架构兼容性
    python_arch = platform.architecture()[0]
    if python_arch != "64bit":
        print(f"[警告] Python 是 {python_arch}，但尝试加载 x64 DLL，可能导致失败")

    # 5. 尝试加载 DLL
    try:
        # 方法一：使用完整路径
        my_dll = ctypes.WinDLL(dll_path)
        print(f"成功加载 DLL: {dll_path}")
        return my_dll
    except OSError as e:
        print(f"[错误] 加载失败 (方法1): {e}")

    try:
        # 方法二：仅使用文件名（依赖 PATH）
        my_dll = ctypes.WinDLL("OldCimgRead0.dll")
        print("成功加载 DLL (文件名方式)")
        return my_dll
    except OSError as e:
        print(f"[错误] 加载失败 (方法2): {e}")

    # 6. 尝试获取错误详情
    error_code = ctypes.GetLastError()
    print(f"系统错误代码: {error_code}")

    # 建议安装 Visual C++ Redistributable
    print("建议解决方案: 安装 Microsoft Visual C++ Redistributable for Visual Studio")
    print("下载地址: https://aka.ms/vs/17/release/vc_redist.x64.exe")

    return None


# 执行加载
if __name__ == "__main__":
    dll = load_dll()
    if dll:
        print("DLL 加载成功，可以调用函数了")
        # 示例：调用 DLL 中的函数
        try:
            # 假设 DLL 中有名为 process_image 的函数
            dll.process_image.argtypes = [ctypes.c_char_p]
            dll.process_image.restype = ctypes.c_int

            result = dll.process_image(b"image.jpg")
            print(f"函数调用成功，返回值: {result}")
        except AttributeError:
            print("在 DLL 中找不到指定函数")