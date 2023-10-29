import logging
import sys
from colorlog import ColoredFormatter
from dotenv import load_dotenv
import os

load_dotenv()

def setup_logger(name):    # log filename timestamp level message
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s %(asctime)s %(name)s: %(reset)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    return logger

