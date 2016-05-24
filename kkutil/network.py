#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import struct
import socket


PY2 = (int(sys.version[0]) == 2)

# ----- ip util ----------
NET_IP_LOCALHOST = 0
NET_IP_IPV4 = 1
NET_IP_IPV6 = 2
NET_IP_UNKNOWN_TYPE = 3


def get_ip_type(net_address):
    """
    :param net_address: human readable net_address string
    :return: ip type
    """
    # .1 detect localhost
    if net_address == "localhost" or net_address == "127.0.0.1":
        return NET_IP_LOCALHOST

    # .2 detect ipv4 or ipv6
    try:
        socket.inet_pton(socket.AF_INET, net_address)
    except:
        pass
    else:
        return NET_IP_IPV4

    # check ipv6
    try:
        socket.inet_pton(socket.AF_INET6, net_address)
    except:
        # not ipv4 or ipv6
        return NET_IP_UNKNOWN_TYPE
    else:
        return NET_IP_IPV6


def ipv4_str_to_int(ip_string="127.0.0.1"):
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


def gethostname():
    return socket.gethostname()
