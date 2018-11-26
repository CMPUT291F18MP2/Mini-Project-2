#!/usr/bin/python
# -*- coding: utf-8 -*-

"""argparse and entry point script for mini-project-2"""

import argparse
import os
import sys
import logging
from logging import getLogger, basicConfig, Formatter
from logging.handlers import TimedRotatingFileHandler

from mini_project_2.phase1 import generate_data_files
from mini_project_2.phase2 import phase2
from mini_project_2.phase3 import phase3

__log__ = getLogger(__name__)

LOG_LEVEL_STRINGS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


def log_level(log_level_string):
    if log_level_string not in LOG_LEVEL_STRINGS:
        raise argparse.ArgumentTypeError(
            "invalid choice: {} (choose from {})".format(
                log_level_string,
                LOG_LEVEL_STRINGS
            )
        )
    return getattr(logging, log_level_string, logging.INFO)


def get_parser():
    """Create and return the argparser for mini-project-2"""
    parser = argparse.ArgumentParser(
        description="Start the mini-project-2 shell"
    )
    parser.add_argument("--phase", help="Project part to do.", required=True,
                        type=int)
    parser.add_argument("-i", dest="input_file", default=None,
                       type=str, help="Input data file. None -> STD_IN")

    group = parser.add_argument_group(title="Logging")
    group.add_argument("--log-level", dest="log_level", default="INFO",
                       type=log_level, help="Set the logging output level")
    group.add_argument("--log-dir", dest="log_dir",
                       help="Enable TimeRotatingLogging at the directory "
                            "specified")
    group.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose logging")

    return parser


def main(argv=sys.argv[1:]):
    """main entry point mini-project-2"""
    parser = get_parser()
    args = parser.parse_args(argv)
    sys.argv = []

    # configure logging
    handlers_ = []
    log_format = Formatter(fmt="[%(asctime)s] [%(levelname)s] - %(message)s")
    if args.log_dir:
        os.makedirs(args.log_dir, exist_ok=True)
        file_handler = TimedRotatingFileHandler(
            os.path.join(args.log_dir, "mini_project_2.log"),
            when="d", interval=1, backupCount=7, encoding="UTF-8",
        )
        file_handler.setFormatter(log_format)
        file_handler.setLevel(args.log_level)
        handlers_.append(file_handler)
    if args.verbose:
        stream_handler = logging.StreamHandler(stream=sys.stderr)
        stream_handler.setFormatter(log_format)
        stream_handler.setLevel(args.log_level)
        handlers_.append(stream_handler)

    basicConfig(
        handlers=handlers_,
        level=args.log_level
    )
    if args.phase == 1:
        generate_data_files(args.input_file)
    if args.phase == 2:
        phase2()
    if args.phase == 3:
        phase3()
    if args.phase < 1 or args.phase > 3:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
