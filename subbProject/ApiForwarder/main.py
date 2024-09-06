
import uvicorn

from core import app
from work_api import *
from forwarder_base import *
from forwarder_api import *


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=899)
