import pythoncom
import win32gui
from win32com.server.util import wrap
from win32comext.shell import shell, shellcon


class ThumbnailProvider:
    _reg_clsid_ = "{84F76B0B-34A7-4774-A2A3-43AA7F62E9B4}"
    _reg_desc_ = "My Thumbnail Provider"
    _reg_progid_ = "Python.ThumbnailProvider"
    _public_methods_ = ['GetThumbnail']
    _com_interfaces_ = [shell.IID_IExtractImage, pythoncom.IID_IDispatch]

    def GetThumbnail(self, *args,**kwargs):
        # 创建一个位图，并返回其句柄
        # 这里只是一个示例，实际上你需要根据文件生成位图
        print(args)
        print(kwargs)
        hdc = win32gui.GetDC(0)
        win32gui.ReleaseDC(0, hdc)
        # 这里我们没有处理透明度，所以使用WTSAT_RGB


def register_thumbnail_provider():
    # 注册COM服务器
    import win32com.server.register
    win32com.server.register.RegisterServer(ThumbnailProvider._reg_clsid_,
                                            "Python.ThumbnailProvider",
                                            "Python Thumbnail Provider",
                                            ThumbnailProvider._reg_progid_,
                                            "Python.ThumbnailProvider.1",
                                            None)


if __name__ == '__main__':
    register_thumbnail_provider()
    input("Press any key to exit.")