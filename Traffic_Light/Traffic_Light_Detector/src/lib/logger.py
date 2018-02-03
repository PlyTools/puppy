# coding=utf-8

import logging
import logging.handlers as handlers
import subprocess
import os
import time

from patterns.singleton import Singleton


class SizedTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """
    def __init__(self, filename, max_bytes=0, backup_count=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        # If rotation/rollover is wanted, it doesn't make sense to use another
        # mode. If for example 'w' were specified, then if there were multiple
        # runs of the calling application, the logs from previous runs would be
        # lost if the 'w' is respected, because the log file would be truncated
        # on each run.
        handlers.TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backup_count, encoding, delay, utc)
        self.maxBytes = max_bytes

    # noinspection PyIncorrectDocstring
    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            # due to non-posix-compliant Windows feature
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0


class Logger(Singleton):

    __log_filename = 'detector.py.log'
    __logger = None
    __log_file_path = "./"

    def __init__(self):
        pass

    def __call__(self):
        return self.__logger

    def critical(self, msg, *args, **kwargs):
        self.__logger.debug(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.__logger.error(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.__logger.warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.__logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.__logger.info(msg, *args, **kwargs)

    def init_logger(self, log_type, path):
        """

        :param path: Where log file will be created
        :param log_type: Type of log to recording. Example logging.NOTSET
        """
        self.__log_file_path = os.path.join(path, self.__log_filename)
        log_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)-8.8s] %(message)s")
        self.__logger = logging.getLogger()

        file_handler = SizedTimedRotatingFileHandler(
            self.__log_file_path,
            max_bytes=1000000,
            backup_count=5,
            interval=24,
            # encoding='bz2',
            # uncomment for bz2 compression
            )
        file_handler.setFormatter(log_formatter)
        self.__logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.__logger.addHandler(console_handler)

        self.__logger.setLevel(log_type)

    def log_command(self, cmd, path):
        """
        Super fast logging command output as opposed to Popen.communicate()

        :param path: The path where the command is run
        :type cmd: Command to call. Single string or array
        """

        with open(self.__log_file_path, 'a') as logfile:
            return subprocess.call(
                cmd if isinstance(cmd, list) else [cmd],
                cwd=path,
                stdout=logfile,
                stderr=logfile,
                shell=True)

logger = Logger()  # simple alias without ugly brackets
