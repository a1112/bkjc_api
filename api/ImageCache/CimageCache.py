from .TimeoutDict import TimeoutDict


# 缓存 cimg 图像


class CimgCache(TimeoutDict):
    def __init__(self, capacity=800, timeout_seconds=60 * 30):
        super().__init__(capacity, timeout_seconds)


if __name__ == "__main__":
    cc = CimgCache()
    cc[1, 2, 3] = 2
    print(cc[1, 2, 3])
