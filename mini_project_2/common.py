#!/usr/bin/python
# -*- coding: utf-8 -*-

"""common utilities utilized by mini-project-2"""

import argparse
import os
import sys

import mini_project_2

MINI_PROJECT_DATE_FMT = "%Y-%m-%d"

MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))
ads_file = os.path.join(MINI_PROJECT_2_PATH, "data/ads.txt")
terms_file = os.path.join(MINI_PROJECT_2_PATH, "data/terms.txt")
pdates_file = os.path.join(MINI_PROJECT_2_PATH, "data/pdates.txt")
prices_file = os.path.join(MINI_PROJECT_2_PATH, "data/prices.txt")


class ShellArgumentException(Exception):
    """Custom exception class noting a invalid argument within a
    :class:`.shell.MiniProjectShell` command"""
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class ShellArgumentParser(argparse.ArgumentParser):
    """Custom argument parser for use in :class`.shell.MiniProjectShell`"""

    def __init__(self, *args, **kwargs):
        # set ``add_help`` to false to avoid conflicts with the shell
        kwargs["add_help"] = False
        super().__init__(*args, **kwargs)

    def error(self, message):
        self.print_help(sys.stderr)
        raise ShellArgumentException(message)