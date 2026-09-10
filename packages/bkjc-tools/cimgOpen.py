import sys
import winreg
import ctypes
import os

from argparse import ArgumentParser

from bkjc_tools.cimg_read import CimgReadCore
exe_path = sys.executable


def is_admin():
    try:
        # 只有在Windows系统下才能运行
        is_admin = os.name == 'nt' and ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        # 如果不是Windows系统，或者其他原因导致调用失败，则默认不是管理员
        is_admin = False
    return is_admin


def set_context_menu(file_type, menu_name, command):
    # file_type 通常是文件扩展名，例如 '.txt'
    # menu_name 是上下文菜单中显示的名称
    # command 是点击菜单项时执行的命令

    # 打开 (或创建) 文件类型的键
    key_path = f'{file_type}\\shell\\{menu_name}\\command'
    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
        # 设置命令
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, command)


def main():
    if is_admin():
        set_context_menu('.cimg', '打开cimg', rf'{exe_path} "%1"')
    else:
        print("不是管理员")
    parser = ArgumentParser(description='Process some integers.')
    parser.add_argument('image')
    args = parser.parse_args()
    print(args.image)
    CimgReadCore.ReadCimgToImage(args.image).show()  # load image


if __name__ == '__main__':
    main()
