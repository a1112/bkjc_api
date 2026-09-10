from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("bkjc_tools", includes=["dll/x64/*.dll"])
