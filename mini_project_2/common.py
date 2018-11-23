#!/usr/bin/python
# -*- coding: utf-8 -*-

"""common utilities utilized by mini-project-2"""

import argparse
import sys

MINI_PROJECT_DATE_FMT = "%Y-%m-%d"


class ShellArgumentException(Exception):
    """Custom exception class noting a invalid argument within a
    :class:`.shell.MiniProjectShell` command"""
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
