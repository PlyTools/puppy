#!/usr/bin/python
#  coding=utf-8

if __name__ == '__main__':
    import os
    import sys
    import logging
    import settings
    import src

    base_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(base_path)

    base_log_path = os.path.join(base_path, settings.LOG_PATH)
    logger_path = "/var/log/traffic-light-detector.py" if settings.GLOBAL_LOG else base_log_path

    src.lib.logger.init_logger(logging.NOTSET, logger_path)

    cli = src.cli.Cli(base_path)
    cli.run()
