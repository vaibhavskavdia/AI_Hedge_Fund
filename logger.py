import logging
import os
from datetime import datetime

# Log directory
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name
LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Logging configuration
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    force=True   # 🔥 VERY IMPORTANT
)

# Create logger object
logger = logging.getLogger("AI-Hedge_Fund")