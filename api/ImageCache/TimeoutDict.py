from collections import OrderedDict
import threading
import time


class TimeoutDict(threading.Thread):
    def __init__(self, capacity, timeout_seconds=30 * 60):
        super().__init__()
        self.capacity = capacity
        self.timeout_seconds = timeout_seconds
        self.data = OrderedDict()
        self.lock = threading.Lock()
        self.start()

    def __setitem__(self, key, value):
        # 如果字典已满，则删除最旧的条目
        with self.lock:
            if len(self.data) >= self.capacity:
                self._remove_oldest()
            # 设置键值对，并记录当前时间戳
            self.data[key] = {'value': value, 'timestamp': time.time()}

    def __getitem__(self, key):
        # 如果键不存在，则返回None
        if key not in self.data:
            return None
        entry = self.data[key]

        return entry['value']

    def __contains__(self, item):
        return item in self.data

    def run(self):
        while True:
            for key in self.data:
                entry = self.data[key]
            # 如果条目已过期，则删除并返回None
                if time.time() - entry['timestamp'] > self.timeout_seconds:
                    del self.data[key]
            time.sleep(60*5)

    def _remove_oldest(self):
        # 删除最旧的条目
        if self.data:
            oldest_key = next(iter(self.data))
            del self.data[oldest_key]


# # 示例用法：
# timeout_dict = TimeoutDict(capacity=3, timeout_seconds=5)
# #
# timeout_dict['key1',2]='value1'
# timeout_dict.set('key2', 'value2')
# timeout_dict.set('key3', 'value3')
#
# print(timeout_dict.get('key1'))  # 输出: value1
#
# # 等待一段时间，让超时发生
# time.sleep(6)
#
# print(timeout_dict.get('key1'))  # 输出: None，因为已超时
#
# timeout_dict.set('key4', 'value4')  # 新条目会替换掉最旧的条目
#
# print(timeout_dict.get('key2'))  # 输出: None，因为已超时
# print(timeout_dict.get('key4'))  # 输出: value4
