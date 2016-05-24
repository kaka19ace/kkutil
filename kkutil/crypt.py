#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import base64
import hashlib


def to_md5(s):
    """
    :param s: str
    """
    return hashlib.md5(s.encode()).hexdigest()


def to_base64(s):
    """
    :param s: str
    """
    return base64.b64encode(s.encode()).decode()
