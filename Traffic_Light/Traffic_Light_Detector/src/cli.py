# coding=utf-8

import argparse
import os

import crop
import settings
import distutils.util
from lib.logger import logger
from src.detector import processing


class Cli(object):
    __cli_args = None
    __base_path = "/"

    def __init__(self, base_path):
        """
        Initialize CLI arguments
        """
        parser = argparse.ArgumentParser(description='Detect traffic light status changes by stream or video.')
        parser.add_argument('action', choices=['init', 'proceed'], default='process', nargs=1,
                            help='init: Return ROI for your selection on current source; \nprocess: Save status changes'
                                 ' (frames and timestamp)')
        parser.add_argument('param', nargs='?', help='Video or stream id')
        parser.add_argument("-v", "--verbose", action="store_true", help="")

        self.__cli_args = parser.parse_args()

        self.__base_path = base_path

    def run(self):
        method = getattr(self, self.__cli_args.action[0])
        if not method:
            logger.error("Method {} not implemented".format(self.__cli_args.action[0]))
            raise NotImplementedError("Method {} not implemented".format(self.__cli_args.action[0]))
        method()

    def init(self):
        """
        Return ROI for your selection on current source
        """
        if len(self.__cli_args.param) > 0:
            video_file = os.path.join(self.__base_path, settings.CAMERAS_PATH, self.__cli_args.param + '.mp4')
            logger.info('ROI (put into config file): ' + str(crop.select(video_file=video_file)))
        else:
            logger.error('Video or stream id not defined')

    def proceed(self):
        """
        Proceed detector.py current source
        """
        if len(self.__cli_args.param) > 0:

            video_file = os.path.join(self.__base_path, settings.CAMERAS_PATH, self.__cli_args.param + '.mp4')
            config_file = os.path.join(self.__base_path, settings.CAMERAS_PATH, self.__cli_args.param + '.config')

            if (not os.path.exists(config_file)) or not os.path.exists(config_file):
                logger.error('ROI for video not defined. You must init first.')
            else:
                with open(config_file, 'r') as data:
                    content = data.readlines()
                # noinspection PyTypeChecker
                config = dict(s.replace('\n', '').split('=') for s in content)

                processing.run(
                    video_file=video_file,
                    frame_crop=config["frame"].split(","),
                    light_cycle=int(config["cycle"]),
                    min_contour_area=int(config["minContourArea"]),
                    vertical=distutils.util.strtobool(config["vertical"])
                )
        else:
            logger.error('Video or stream id not defined')
