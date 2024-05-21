import logging

formatStr = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
formatStr2 = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=formatStr)