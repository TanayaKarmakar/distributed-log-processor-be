import logging
import os

LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}

# Default log level (can be overridden via env var)
DEFAULT_LOG_LEVEL = LOG_LEVELS.get(os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)

# Configurable log format options
LOG_FORMAT = os.getenv(
    "LOG_FORMAT",
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

DATE_FORMAT = os.getenv("DATE_FORMAT", "%Y-%m-%d %H:%M:%S")

# Log frequency (in seconds) – configurable instead of hardcoded 5s
LOG_FREQUENCY = int(os.getenv("LOG_FREQUENCY", 5))

# Log file path (if needed)
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
