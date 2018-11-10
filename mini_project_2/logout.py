#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Logout functionality"""

from mini_project_2.common import ShellArgumentParser


def get_logout_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell` ``logout`` command"""
    parser = ShellArgumentParser(
        prog="logout",
        description="Logout to the mini-project-2 database")

    return parser
