#  encoding = utf-8
#  配置中心
import json
import os
import sys


def get_path(path_name):
    return os.path.join(os.path.dirname(sys.executable) if "python.exe" not in sys.executable else
                        os.path.dirname(__file__), path_name)


def load_json(file_name):
    with open(get_path(file_name), 'r+', encoding='utf-8')as file:
        try:
            return json.load(file)
        except json.decoder.JSONDecodeError as e:
            raise json.decoder.JSONDecodeError


def getCurrentSteelId():
    with open(get_path("config/currentSteelId.txt"), 'r', encoding='utf-8') as f:
        return int(f.read())


def setCurrentSteelId(seqNo):
    with open(get_path("config/currentSteelId.txt"), 'w', encoding='utf-8') as f:
        f.write(str(seqNo))


#  END Base Init


