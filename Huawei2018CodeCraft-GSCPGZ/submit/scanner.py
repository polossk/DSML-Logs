# -*- coding: utf-8 -*-
from datetime import datetime, date

DAY_LIMIT = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
DAY_LIMIT_ACCU = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def _is_leap(yyyy):
    return yyyy % 4 == 0 and (yyyy % 100 != 0 or yyyy % 400 == 0)

def _day_limit(yyyy, mm):
    if mm == 2 and _is_leap(yyyy):
        return 29
    else: return DAY_LIMIT[mm]


def ymd2ordinal(d0):
    yyyy, mm, dd = d0[:3]
    y = yyyy - 1
    days_before_year = y * 365 + y // 4 - y // 100 + y // 400
    days_before_month = DAY_LIMIT_ACCU[mm] + (mm > 2 and _is_leap(yyyy))
    return dd + days_before_month + days_before_year

def weekday(d0):
    return (6 + ymd2ordinal(d0)) % 7


def scanner(filename):
    raw_text, ret, querys = [], [], []
    with open(filename, 'r') as fin:
        raw_text = fin.readlines()
    for line in raw_text:
        words = line.strip().split('\t')
        name, type = words[:2]
        date_, time_ = words[-1].split(' ')
        yy, mm, dd = [int(_) for _ in date_.split('-')]
        ret.append([name, type, yy, mm, dd])
    return ret


def next_date(d0):
    yyyy, mm, dd = d0[:3]
    if dd + 1 <= _day_limit(yyyy, mm):
        return [yyyy, mm, dd + 1]
    elif mm == 12:
        return [yyyy + 1, 1, 1]
    else: return [yyyy, mm + 1, 1]


def merge(raw):
    # item = [yyyy, mm, dd, weekday, flavor$$]
    start_date = raw[0][2:5]
    start_item = raw[0][2:5] + [0] * 16
    merged = [start_item]
    last_date = start_date
    for item in raw:
        if item[2:5] != last_date:
            while item[2:5] != last_date:
                last_date = next_date(last_date)
                last_item = last_date + [0] * 16
                merged.append(last_item)
        else:
            type = int(item[1].replace('flavor', ''))
            if type > 15 or type < 1: continue
            merged[-1][4 + type - 1] += 1
    for item in merged:
        item[3] = weekday(item[:3])
    return merged


def main(): # unit_test
    data = scanner('./../raw_training_data/data_2015_1.txt')
    merged = merge(data)
    for elem in merged:
        print(elem)


if __name__ == '__main__':
    main()
