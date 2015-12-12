#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @date     Dec 13 2015
# @brief     
#

import sys
import signal
import ctypes
import socket
import struct

import traceback

import time
import datetime
from decimal import Decimal

import json
import hashlib
import base64

PY2 = (int(sys.version[0]) == 2)


def get_exception_message():
    return json.dumps(traceback.format_exception(*sys.exc_info()))


def register_quit_handler(handler, signals=None):
    """
    :param handler: process your things after receive quit signal
    :param signals:
        if not signals: default signals are SIGQUIT SIGTERM SIGINT
        else use the param signals as you want
    :return:
    """
    if not signals:
        signals = [signal.SIGQUIT, signal.SIGTERM, signal.SIGINT]
    for s in signals:
        signal.signal(s, handler)


class TypeUtil(object):
    @staticmethod
    def int32_to_uint32(i):
        return ctypes.c_uint32(i).value

    @staticmethod
    def uint32_to_int(i):
        return ctypes.c_int(i).value

    @staticmethod
    def str_to_integer(i, default=None):
        try:
            i = int(i)
        except:
            i = default
        return i

    @staticmethod
    def is_whitespaces_str(s):
        return True if len(s.strip(" \t\n\r\f\v")) == 0 else False


class TimeUtil(object):
    @staticmethod
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

    @classmethod
    def timestamp_to_format_time_str(cls, timestamp, time_format="%Y-%m-%d %H:%M:%S"):
        """
        :param timestamp: integer or string(integer)
        :param time_format: if not set: default "%Y-%m-%d %H:%M:%S"
        :return: time format output
        """
        return datetime.datetime.fromtimestamp(int(timestamp)).strftime(time_format)

    @staticmethod
    def format_time_str_to_timestamp(time_str, time_format='%Y-%m-%d'):
        return int(time.mktime(time.strptime(time_str, time_format)))


class IPUtil(object):
    NET_IP_LOCALHOST = 0
    NET_IP_IPV4 = 1
    NET_IP_IPV6 = 2
    NET_IP_UNKNOWN_TYPE = 3

    @classmethod
    def get_ip_type(cls, net_address):
        """
        :param net_address: human readable net_address string
        :return: ip type
        """
        # .1 detect localhost
        if net_address == "localhost" or net_address == "127.0.0.1":
            return cls.NET_IP_LOCALHOST

        # .2 detect ipv4 or ipv6
        try:
            socket.inet_pton(socket.AF_INET, net_address)
        except:
            pass
        else:
            return cls.NET_IP_IPV4

        # check ipv6
        try:
            socket.inet_pton(socket.AF_INET6, net_address)
        except:
            # not ipv4 or ipv6
            return cls.NET_IP_UNKNOWN_TYPE
        else:
            return cls.NET_IP_IPV6

    @classmethod
    def ipv4_str_to_int(cls, ip_string="127.0.0.1"):
        """
        :param ip_string:  default 127.0.0.1
        :return: ipv4 32bit unsigned long
        """
        try:
            socket.inet_pton(socket.AF_INET, ip_string)
        except:
            et, ei, tb = sys.exc_info()
            if not PY2:
                raise ei.with_traceback(tb)
            else:
                ei.__traceback__ = tb
                raise ei

        packed_ip = socket.inet_aton(ip_string)
        # ! network (= big-endian)
        # L unsigned long integer
        return struct.unpack("!L", packed_ip)[0]

    @staticmethod
    def ipv6_str_to_binary_form_string(ip_string="::1"):
        """
        socket.inet_pton(socket.AF_INET6, ip_string)
        Python 2:  socket.inet_pton return str   (element is str)
        Python 3:  socket.inet_pton return bytes (element is byte)

        Faq: why store ipv6 with str
        A:  if we using integer, we must use 128-bit ,
            but now the machine is 64bit,  128 need long long int
            mysql bigint just 8bytes, 64bits.

        :param ip_string:  default ::1 (localhost)
        :return: str ipv6 binary form string
        """
        try:
            binary_ip = socket.inet_pton(socket.AF_INET6, ip_string)
        except:
            # refs: tornado.util.py: function: raise_exc_info
            if not PY2:
                exec("""
                raise e.with_traceback(sys.exc_info()[2])
""")
            else:
                exec("""
                exc_info = sys.exc_info()
                raise exc_info[0], exc_info[1], exc_info[2]
""")

        # In Python 3 is bytes/ In Python 2 is str
        return binary_ip.decode('utf-8') if isinstance(binary_ip[0], int) else binary_ip


class CryptUtil(object):
    @staticmethod
    def str_to_md5_str(base_str):
        return hashlib.md5(base_str.encode()).hexdigest()

    @staticmethod
    def str_to_base64_str(base_str):
        return base64.b64encode(base_str.encode()).decode()
