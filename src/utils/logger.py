import logging
import sys
from pathlib import Path
from src.core.config_loader import config

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger

    # Format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler
    log_dir = config.base_path / config.get("paths.logs", "logs")
    log_dir.mkdir(exist_ok=True)
    
    fh = logging.FileHandler(log_dir / "app.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
