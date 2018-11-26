#!/usr/bin/python
# -*- coding: utf-8 -*-

"""common utilities utilized by mini-project-2"""

import os

import mini_project_2

MINI_PROJECT_DATE_FMT = "%Y-%m-%d"
MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))
AD_INDEX = os.path.join(MINI_PROJECT_2_PATH, "database/ad.idx")
TE_INDEX = os.path.join(MINI_PROJECT_2_PATH, "database/te.idx")
PR_INDEX = os.path.join(MINI_PROJECT_2_PATH, "database/pr.idx")
DA_INDEX = os.path.join(MINI_PROJECT_2_PATH, "database/da.idx")


class ShellArgumentException(Exception):
    """Custom exception class noting a invalid argument within a
    :class:`.shell.MiniProjectShell` command"""
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
