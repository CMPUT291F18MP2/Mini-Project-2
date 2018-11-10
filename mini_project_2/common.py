#!/usr/bin/python
# -*- coding: utf-8 -*-

"""common utilities utilized by mini-project-2"""

import argparse
import sys

import pendulum

MINI_PROJECT_DATE_FMT = "%Y-%m-%d"


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


def price(price_string: str) -> int:
    price = int(price_string)
    if price < 0:
        raise argparse.ArgumentTypeError(
            "invalid price: {} (please choose a non negative price)".format(
                price_string
            )
        )
    return price


def greater_than_zero_number(value: str) -> int:
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("%s must be a greater than zero number" % value)
    return value


def date(date_str: str) -> pendulum.DateTime:
    return pendulum.parse(date_str)