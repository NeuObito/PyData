#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-25
# @Author  : ${xuejun} (${xuemyjun@gmail.com})

from matplotlib import pylab
from matplotlib import pyplot as plt
import os
import pandas as pd
import numpy as np
import json

from collections import Counter
from collections import defaultdict
from pandas import DataFrame, Series


def get_records(filename):
    records = [json.loads(line) for line in open(filename)]
    return records


def get_timezone(records):
    print(records[0]['tz'])
    return [rec['tz'] for rec in records if 'tz' in rec]


def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1

    return counts


def get_counts_use_counter(sequence):
    counts = defaultdict(int)

    for x in sequence:
        counts[x] += 1

    return counts


def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]


def top_counts_use_counter(count_dict, n=10):
    counts = Counter(count_dict)
    return counts.most_common(n)


def top_counts_use_frame(records, n=10):
    frame = DataFrame(records)
    clean_tz = frame['tz'].fillna('Missing')
    clean_tz[clean_tz == ''] = 'Unknown'
    return clean_tz.value_counts()[:n]


def show_use_plot(count_dict):
    pass


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path, "usagov_bitly_data2012-03-16-1331923249.txt")
    records = get_records(filename)
    counts = top_counts_use_frame(records)
    counts.plot(kind="barh", rot=0)
