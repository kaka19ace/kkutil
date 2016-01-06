#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @file     system.py
# @author   kaka_ace <xiang.ace@gmail.com>
# @date     Jan 06 2016
# @brief     
#

import sys
import json
import signal
import traceback


def get_exception_message():
    """
    useless, just json format the exception message,
    and log with other level which is not EXCEPTION
    """
    return json.dumps(traceback.format_exception(*sys.exc_info()))


def register_quit_handler(handler, signals=None):
    """
    :param handler: process your things after receive quit signal
    :param signals:
        if not signals: default signals are SIGQUIT SIGTERM SIGINT
        else use the param signals as you want
    """
    if not signals:
        signals = [signal.SIGQUIT, signal.SIGTERM, signal.SIGINT]
    for s in signals:
        signal.signal(s, handler)
