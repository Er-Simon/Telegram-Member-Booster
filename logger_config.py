import consts
import datetime
import logging
import utils


LOG_FILE_PATH = consts.LOG_FILE_PATH.format(
    utils.get_current_datetime_str()
)

class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, timezone=None):
        super().__init__(fmt)
        self.datefmt = datefmt
        self.timezone = timezone
    
    def formatTime(self, record, datefmt=None):
        dt = datetime.datetime.fromtimestamp(record.created, self.timezone)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime(self.datefmt) 

logger = logging.getLogger("telegram_member_booster")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE_PATH)
console_handler = logging.StreamHandler()

formatter = CustomFormatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(funcName)s] - %(message)s ',
    datefmt=consts.DATETIME_FORMAT,
    timezone=consts.TZ_INFO 
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger():
    return logger
