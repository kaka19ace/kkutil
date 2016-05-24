#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys

import time
import datetime
import calendar
from decimal import Decimal


PY2 = (int(sys.version[0]) == 2)


def seconds_to_duration_format(seconds=0, with_hour_output=False):
    seconds = int(Decimal(seconds).to_integral())

    if with_hour_output:
        hour = seconds // 3600
        minute = seconds % 3600 // 60
        second = seconds % 60
        return "{}:{:02}:{:02}".format(hour, minute, second)
    else:
        minute = seconds // 60
        second = seconds % 60
        return "{:02}:{:02}".format(minute, second)


def timestamp_to_format_time_str(timestamp, time_format="%Y-%m-%d %H:%M:%S"):
    """
    :param timestamp: integer or string(integer)
    :param time_format: if not set: default "%Y-%m-%d %H:%M:%S"
    :return: time format output
    """
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime(time_format)


def format_time_str_to_timestamp(time_str, time_format='%Y-%m-%d'):
    return int(time.mktime(time.strptime(time_str, time_format)))


def datetime_to_timestamp(dt, is_utc=False):
    """
    :param dt: datetime or date instance
    :param is_utc: bool
    """
    if not isinstance(dt, datetime.datetime):  # it is date
        dt = datetime.datetime.combine(dt, datetime.time.min)
    return time.mktime(dt.timetuple()) if not is_utc else calendar.timegm(dt.utctimetuple())
