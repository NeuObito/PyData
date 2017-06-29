#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-25
# @Author  : ${xuejun} (${xuemyjun@gmail.com})

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import time

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


def top_counts_use_series(records, n=10):
    frame = DataFrame(records)
    results = Series([x.split()[0] for x in frame.a.dropna()])

    # return results[:n]
    return results.value_counts()[:n]


def top_counts_is_windows(recors, n=10):
    """统计用户使用的是否为Windows"""
    frame = DataFrame(records)
    cframe = frame[frame.a.notnull()]
    operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')

    # 根据时区分组
    by_tz_os = cframe.groupby(['tz', operating_system])
    agg_counts = by_tz_os.size().unstack().fillna(0)

    # 用于按升序排列
    indexer = agg_counts.sum(1).argsort()

    # 通过take按照排序顺序截取最后n行
    count_subset = agg_counts.take(indexer)[-n:]
    return count_subset


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path, "usagov_bitly_data2012-03-16-1331923249.txt")
    records = get_records(filename)
    counts = top_counts_use_frame(records)
    # counts.plot(kind="barh", rot=0)
    # print(counts.keys())
    country = counts.keys()

    # 柱状图
    # plt.bar(range(10), [counts.get(cn, 0) for cn in counts.keys()], align="center", yerr=0.0001)
    # plt.xticks(range(10), country)
    # plt.xlabel("Nums")
    # plt.ylabel("Country")
    # plt.title("Test")
    # plt.gcf().autofmt_xdate()
    # plt.show()

    # 条形图
    # plt.yticks(range(10), country, fontsize=10)
    # plt.barh(range(10), [counts.get(cn, 0) for cn in counts.keys()], align="center", xerr=0.0001)
    # plt.gcf().autofmt_xdate()
    # plt.show()

    # print(top_counts_is_windows(records)['Not Windows'].axes[0].values)
    print(type(top_counts_is_windows(records)['Not Windows'].values))
    values1 = top_counts_is_windows(records)['Not Windows'].values
    values2 = top_counts_is_windows(records)['Windows'].values
    print(values1)
    print(values2)

    country = top_counts_is_windows(records)['Not Windows'].axes[0].values
    # 堆叠柱状图
    # plt.bar(range(10), values1, label="Not Windows")
    # plt.bar(range(10), values2, bottom=values1, label="Windows")
    # plt.xticks(range(10), country)
    # plt.xlabel("Nums")
    # plt.ylabel("Country")
    # plt.title("Test")
    # plt.legend()
    # plt.gcf().autofmt_xdate()
    # plt.show()

    # 正负条形图
    # plt.yticks(range(len(country)), country, fontsize=10)
    # plt.barh(range(len(values1)), values1, label="Not Windows")
    # plt.barh(range(len(values2)), -values2, label="Windows")
    # plt.legend()
    # plt.show()

    # 堆叠条形图 有问题
    # plt.yticks(range(len(country)), country, fontsize=10)
    # plt.barh(range(len(values1)), values1, label="Not Windows")
    # plt.barh(range(len(values2)), values2, bottom=values1, label="Windows")
    # plt.legend()
    # plt.show()
