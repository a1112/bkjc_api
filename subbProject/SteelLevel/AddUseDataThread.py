import time
from pathlib import Path

from threading import Thread
import config


class AddUseDataThread(Thread):
    def __init__(self):
        inFileFolder = config.get_path("in")
        self.inFileFolder = Path(inFileFolder)
        self.fileCache = []
        super(Thread).__init__()
        self.start()

    def run(self):
        while True:
            xlsx_files = self.inFileFolder.glob("*.xlsx")
            for f_ in xlsx_files:
                if f_.name in self.fileCache:
                    continue
                self.fileCache.append(f_.name)



            time.sleep(10)
