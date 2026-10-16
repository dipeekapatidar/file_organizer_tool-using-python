"""Writes every operation to logs/operations.log with a timestamp."""
import logging
import os
from config import LOG_DIR, LOG_FILE

os.makedirs(LOG_DIR, exist_ok=True)
_logger = logging.getLogger("file_organizer")
if not _logger.handlers:
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s", "%Y-%m-%d %H:%M:%S"))
    _logger.addHandler(handler)
    _logger.setLevel(logging.INFO)


def log(message):
    _logger.info(message)


def read_recent(lines=20):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f.readlines()[-lines:]]
