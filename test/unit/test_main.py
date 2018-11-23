#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pytests for :mod:`.__main__`"""
import argparse

import pytest

from mini_project_2.__main__ import get_parser, log_level


def test_get_parser():
    parser = get_parser()
    assert parser


def test_log_level():
    with pytest.raises(argparse.ArgumentTypeError):
        log_level("test")
