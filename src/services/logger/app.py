import time
import os
import logging
from datetime import datetime
import config  # import your config.py
from logging.handlers import RotatingFileHandler


def setup_logger():
    """Configure logger to log to both console and rotating file."""
    # log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = config.LOG_FORMAT
    log_file = config.LOG_FILE
    log_frequency = config.LOG_FREQUENCY

    # Configure logging based on config.py
    logging.basicConfig(
        level=config.DEFAULT_LOG_LEVEL,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Create logs directory if not exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configure logging
    logger = logging.getLogger("LoggerService")
    #logger.setLevel(getattr(logging, log_level, logging.INFO))

    formatter = logging.Formatter(log_format)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating File handler (1MB per file, keep last 5 backups)
    file_handler = RotatingFileHandler(log_file, maxBytes=1 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger, log_frequency

def main():
    """Simple logger service using config.py settings."""

    logger, log_frequency = setup_logger()
    logger.info("Starting distributed logger service...")

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Logger service is running at {timestamp}")
        time.sleep(log_frequency)

if __name__ == "__main__":
    main()
