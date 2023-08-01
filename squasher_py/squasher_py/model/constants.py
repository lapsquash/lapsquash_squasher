from datetime import datetime
from os import path

import squasher_py

__now = datetime.now()
__now_str = __now.strftime("%Y-%m-%d_%H-%M-%S")

OUTPUT_DIR = path.join(path.dirname(squasher_py.__file__), "..", "out")
LOG_DIR = path.join(OUTPUT_DIR, "logs")
LOG_PATH = path.join(LOG_DIR, f"{__now_str}.log")
