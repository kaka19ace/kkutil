#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


import ctypes


def int32_to_uint32(i):
    return ctypes.c_uint32(i).value


def uint32_to_int(i):
    return ctypes.c_int(i).value


def str_to_int(i, default=None):
    try:
        i = int(i)
    except:
        i = default
    return i
