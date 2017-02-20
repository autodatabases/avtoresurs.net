#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import sys


def print_error(exception_info=None):
    """ print error traceback from exception info
     Args:
     :param exception_info: we can get like this: info sys.exc_info() """
    if not exception_info:
        exception_info = sys.exc_info()
    exc_type, exc_value, exc_traceback = exception_info
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)

