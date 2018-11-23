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


# def test_main(tmpdir):
#     tmp_file = tmpdir.join("thefile_name.json")
#     tmp_file_name = str(tmp_file)
#     with mock.patch('builtins.input', return_value='foo'):
#         with mock.patch('mini_project_2.shell.MiniProjectShell.cmdloop', return_value='bar'):
#             main(["-i", tmp_file_name])
