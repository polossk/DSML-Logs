#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'providing some simple tools of processing xlsx file'

__author__ = 'polossk'

def abc2dec(column_name):
    ret = 0
    for _ in map(lambda ch: ord(ch) - ord('A') + 1, column_name):
        ret = _ + ret * 26
    return ret
