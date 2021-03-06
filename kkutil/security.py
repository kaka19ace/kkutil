#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


"""
util regex tool
refs:
http://www.symantec.com/connect/articles/detection-sql-injection-and-cross-site-scripting-attacks
"""

import re

INJECTION_REGEX = re.compile(
    r"(%27)|(\')|(\-\-)|(%23)|(#)|"  # Regex for detection of SQL meta-characters
    r"\w*((%27)|(\'))\s+((%6F)|o|(%4F))((%72)|r|(%52))\s*|"  # Modified regex for detection of SQL meta-characters eg: ' or 1 = 1' detect word 'or',
    r"((%3D)|(=))[^\n]*((%27)|(\')|(\-\-)|(%3B)|(;))"  # Regex for typical SQL Injection attack eg: '= 1 --'
    r"((%27)|(\'))union|"  # Regex for detecting SQL Injection with the UNION keyword
    r"((%27)|(\'))select|"  # Regex for detecting SQL Injection with the UNION keyword
    r"((%27)|(\'))insert|"  # Regex for detecting SQL Injection with the UNION keyword
    r"((%27)|(\'))update|"  # Regex for detecting SQL Injection with the UNION keyword
    r"((%27)|(\'))drop",  # Regex for detecting SQL Injection with the UNION keyword
    re.IGNORECASE
)

CSS_ATTACK_REGREX = re.compile(r"((%3C)|<)((%2F)|/)*[a-z0-9%]+((%3E)|>)", re.IGNORECASE)

CSS_IMG_SRC_ATTACK_REGEX = re.compile(
    r"((%3C)|<)((%69)|i|(%49))((%6D)|m|(%4D))((%67)|g|(%47))[^\n]+((%3E)|>)",
    re.IGNORECASE
)

CSS_PARANOID_ATTACK_REGEX = re.compile("((%3C)|<)[^\n]+((%3E)|>)", re.IGNORECASE)


def is_injection_string(s):
    return True if INJECTION_REGEX.match(s) else False


def is_css_attack_string(s):
    if CSS_ATTACK_REGREX.match(s) or \
        CSS_IMG_SRC_ATTACK_REGEX.match(s) or \
            CSS_PARANOID_ATTACK_REGEX.match(s):
        return True
    return False
