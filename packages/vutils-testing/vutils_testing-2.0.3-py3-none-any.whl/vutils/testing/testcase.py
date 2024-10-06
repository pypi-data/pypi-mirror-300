#
# File:    ./src/vutils/testing/testcase.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-02 00:59:53 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Extended :class:`unittest.TestCase`."""

import unittest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import unittest.mock


class TestCase(unittest.TestCase):
    """Extended :class:`unittest.TestCase`."""

    __slots__ = ()

    @staticmethod
    def assert_called_with(
        mock: "unittest.mock.Mock", *args: object, **kwargs: object
    ) -> None:
        """
        Check and reset the mock call.

        :param mock: The mock object
        :param args: Expected positional arguments
        :param kwargs: Expected key-value arguments

        Check whether the mock object has been called with given arguments and
        reset it.
        """
        mock.assert_called_once_with(*args, **kwargs)
        mock.reset_mock()

    @staticmethod
    def assert_not_called(mock: "unittest.mock.Mock") -> None:
        """
        Check that :arg:`mock` has not been called.

        :param mock: The mock object

        Check whether the mock object has not been called and reset it.
        """
        mock.assert_not_called()
        mock.reset_mock()
