# utils/logger.py
import logging
import logging.config
import os
from pathlib import Path

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.config.fileConfig(
        "config/logging.conf",
        disable_existing_loggers=False
    )
    
    return logging.getLogger("sms_campaign")

logger = setup_logging()