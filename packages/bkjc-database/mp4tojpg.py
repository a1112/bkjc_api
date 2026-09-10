from cv2 import VideoCapture
from cv2 import imwrite
from pathlib import Path
from PIL import Image
# 定义保存图片函数
# image:要保存的图片名字
# addr；图片地址与相片名字的前部分
# num: 相片，名字的后缀。int 类型
def save_image(image, addr, num,name):
    address = addr + str(num) + "_" + name+".jpg"
    print(address)
    Image.fromarray(image).convert("L").save(address)


if __name__ == '__main__':
    folder = fr"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Platform\WhatsNew\Content\media"
    for mp4 in Path(folder).glob("*.mp4"):
        print(mp4)
        out_path = "./output/"  # 保存图片路径+名字
        Path(out_path).mkdir(parents=True, exist_ok=True)
        is_all_frame = False  # 是否取所有的帧
        sta_frame = 1  # 开始帧
        end_frame = 40  # 结束帧

        ######
        time_interval = 1  # 时间间隔

        # 读取视频文件
        videoCapture = VideoCapture(str(mp4))

        # 读帧
        success, frame = videoCapture.read()
        i = 0
        j = 0
        if is_all_frame:
            time_interval = 1

        while success:
            i = i + 1
            if (i % time_interval == 0):
                if is_all_frame == False:
                    if i >= sta_frame and i <= end_frame:
                        j = j + 1
                        print('save frame:', i)
                        print(out_path)
                        save_image(frame, out_path, j, mp4.stem)
                    elif i > end_frame:
                        break
                else:
                    j = j + 1
                    print('save frame:', i)
                    save_image(frame, out_path, j, mp4.stem)

            success, frame = videoCapture.read()