#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'providing some simple tools of processing csv file'

__author__ = 'polossk'

import csv

def write_csv(filename, data_table):
    with open(filename, 'wt', newline='') as fout:
        csvout = csv.writer(fout)
        csvout.writerows(data_table)
