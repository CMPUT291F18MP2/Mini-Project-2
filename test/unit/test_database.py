#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pytests interacting with databases for mini-project-1"""

import sqlite3
import pytest



@pytest.fixture(scope="session")
def mock_db(tmpdir_factory):
    """pytest fixture returning the path to a mock database for testing"""
    filename = str(tmpdir_factory.mktemp("data").join("test.db"))
    return filename


def test_example(mock_db):
    """Test example for interacting with data mocks"""
    database = sqlite3.connect(mock_db)
    print(database.execute("""SELECT name FROM members""").fetchall())

###############################
# tests related to shell.py
###############################
