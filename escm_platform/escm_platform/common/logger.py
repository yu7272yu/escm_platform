# coding=utf-8
import logging
import os
import re
import threading
from datetime import datetime

from escm_platform.common.constants import Constants

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(root_dir, "logs")
lock = threading.RLock()


class Logger:
    def __init__(self, logger_level=logging.DEBUG):
        self.__logger = logging.getLogger()
        self.__logger.setLevel(logger_level)
        self.__lock = threading.RLock()
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_dir = os.path.join(self.root_dir, "logs")

    def debug(self, msg, file_name=None, *args, **kwargs):
        if file_name is not None:
            self.__lock.acquire()
            fh = self.__createFileHandler(file_name)
            self.__logger.addHandler(fh)
            self.__logger.debug(msg, *args, **kwargs)
            self.__logger.removeHandler(fh)
            self.__lock.release()
        else:
            self.__logger.debug(msg, *args, **kwargs)

    def info(self, msg, file_name=None, *args, **kwargs):
        if file_name is not None:
            self.__lock.acquire()
            fh = self.__createFileHandler(file_name)
            self.__logger.addHandler(fh)
            self.__logger.info(msg, *args, **kwargs)
            self.__logger.removeHandler(fh)
            self.__lock.release()
        else:
            self.__logger.info(msg, *args, **kwargs)

    def warning(self, msg, file_name=None, *args, **kwargs):
        if file_name is not None:
            self.__lock.acquire()
            fh = self.__createFileHandler(file_name)
            self.__logger.addHandler(fh)
            self.__logger.warning(msg, *args, **kwargs)
            self.__logger.removeHandler(fh)
            self.__lock.release()
        else:
            self.__logger.warning(msg, *args, **kwargs)

    def error(self, msg, file_name=None, *args, **kwargs):
        if file_name is not None:
            self.__lock.acquire()
            fh = self.__createFileHandler(file_name)
            self.__logger.addHandler(fh)
            self.__logger.error(msg, *args, **kwargs)
            self.__logger.removeHandler(fh)
            self.__lock.release()
        else:
            self.__logger.error(msg, *args, **kwargs)

    def critical(self, msg, file_name=None, *args, **kwargs):
        if file_name is not None:
            self.__lock.acquire()
            fh = self.__createFileHandler(file_name)
            self.__logger.addHandler(fh)
            self.__logger.critical(msg, *args, **kwargs)
            self.__logger.removeHandler(fh)
            self.__lock.release()
        else:
            self.__logger.critical(msg, *args, **kwargs)

    def __createFileHandler(self, file_name):
        if not re.search(r'^\d{4}-\d{2}-\d{2}', file_name):
            file_name = datetime.now().strftime("%Y-%m-%d_") + file_name
        if not re.search(r'.log$', file_name):
            file_name = file_name + ".log"

        fh = logging.FileHandler(os.path.join(self.log_dir, file_name), encoding='UTF-8')
        formatter = logging.Formatter(Constants.LOG_TEXT_FORMAT, Constants.LOG_DATE_FORMAT)
        fh.setFormatter(formatter)
        fh.set_name(file_name)
        return fh


if __name__ == '__main__':
    logger = Logger()
    for i in range(5):
        logger.info('测试一下', '2.log')
        logger.error('测试一下', '2.log')
        logger.debug('测试一下', '2.log')
        logger.debug('测试一下', '1.log')
