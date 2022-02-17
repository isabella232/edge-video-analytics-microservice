# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: MIT

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""Logging utilities
"""
import os
import logging
import util.log as eii_logging


# Globals
DEV_MODE = None
LOG_LEVEL = None


def configure_logging(log_level, dev_mode):
    """Set the global variables for the logging utilities.

    :param str log_level: Global application log level
    :param bool dev_mode: Flag for whether the service is running in dev mode
    """
    global DEV_MODE
    global LOG_LEVEL

    log_level = log_level.upper()
    # assert log_level in eii_logging.LOG_LEVEL, \
    #         f'Invalid log level: {log_level}'

    DEV_MODE = dev_mode
    LOG_LEVEL = log_level


def get_logger(name):
    """Get a new logger with the specified name.

    :param str name: Logger name
    :return: New Python logger
    """
    global DEV_MODE
    global LOG_LEVEL
    return eii_logging.configure_logging(LOG_LEVEL, name, DEV_MODE)
