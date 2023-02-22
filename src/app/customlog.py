import logging
from logging.handlers import RotatingFileHandler
log_format = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO, filename='mylog.log')

file_handler = RotatingFileHandler('mylog.log', maxBytes=1024 * 1024 * 100, backupCount=20)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)