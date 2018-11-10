#!/usr/bin/python
# -*- coding: utf-8 -*-

"""command shell for mini-project-2"""

import cmd
import sqlite3
from logging import getLogger

from mini_project_2.common import ShellArgumentException
from mini_project_2.logout import get_logout_parser
__log__ = getLogger(__name__)


def logged_in(f):
    """Annotation to check if someone is logged in before attempting a
    command in the :class:`.MainProjectShell`"""
    def wrapper(*args):
        if args[0].login_session:
            return f(*args)
        else:
            __log__.error("you must be logged in to use this function")
    return wrapper


class MiniProjectShell(cmd.Cmd):
    """Main shell for mini-project-2"""
    intro = \
        "Welcome to mini-project-2 shell. Type help or ? to list commands\n"
    prompt = "mini-project-2>"

    def __init__(self, database: sqlite3.Connection,
                 register_start: bool = False):
        """Initialize the mini-project-2 shell

        :param database: :class:`sqlite3.Connection` to the database to
        interact with the mini-project-2 shell
        """
        super().__init__()
        self.database = database
        self.register_start = register_start

    def cmdloop(self, intro=None):
        # start a login command at start.
        super().cmdloop()

    # ===============================
    # Shell command definitions
    # ===============================

    @logged_in
    def do_logout(self, arg):
        """Logout from the mini-project-2 database"""
        parser = get_logout_parser()
        try:
            parser.parse_args(arg.split())
        except ShellArgumentException:
            __log__.exception("invalid logout arguement")

    @staticmethod
    def help_logout():
        """Print the argparser help message for logout"""
        get_logout_parser().print_help()

    def do_exit(self, arg):
        """Logout (if needed) and exit out of the mini-project-2 shell"""
        __log__.info("exiting mini-project-2 shell")
        self.database.close()
        return True