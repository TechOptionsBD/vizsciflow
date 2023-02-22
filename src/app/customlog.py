import os
import logging
from logging.handlers import RotatingFileHandler

def configure_logger(logfile):
    # create the file if it doesn't exist
    if not os.path.isfile(logfile):
        os.makedirs(os.path.dirname(logfile), exist_ok=True)
        open(logfile, 'w').close()

    log_format = '%(asctime)s [%(levelname)s] %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO, filename=logfile)

    file_handler = RotatingFileHandler(logfile, maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)