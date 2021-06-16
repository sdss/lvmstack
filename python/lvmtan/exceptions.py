# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-12-05 12:01:21
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-12-05 12:19:32

from __future__ import print_function, division, absolute_import


class LvmtanError(Exception):
    """A custom core Lvmtan exception"""

    def __init__(self, message=None):

        message = 'There has been an error' \
            if not message else message

        super(LvmtanError, self).__init__(message)


class LvmtanNotImplemented(LvmtanError):
    """A custom exception for not yet implemented features."""

    def __init__(self, message=None):

        message = 'This feature is not implemented yet.' \
            if not message else message

        super(LvmtanNotImplemented, self).__init__(message)


class LvmtanAPIError(LvmtanError):
    """A custom exception for API errors"""

    def __init__(self, message=None):
        if not message:
            message = 'Error with Http Response from Lvmtan API'
        else:
            message = 'Http response error from Lvmtan API. {0}'.format(message)

        super(LvmtanAPIError, self).__init__(message)


class LvmtanApiAuthError(LvmtanAPIError):
    """A custom exception for API authentication errors"""
    pass


class LvmtanMissingDependency(LvmtanError):
    """A custom exception for missing dependencies."""
    pass


class LvmtanWarning(Warning):
    """Base warning for Lvmtan."""


class LvmtanUserWarning(UserWarning, LvmtanWarning):
    """The primary warning class."""
    pass


class LvmtanSkippedTestWarning(LvmtanUserWarning):
    """A warning for when a test is skipped."""
    pass


class LvmtanDeprecationWarning(LvmtanUserWarning):
    """A warning for deprecated features."""
    pass
