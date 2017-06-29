#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-29 16:09:31
# @Author  : xuejun (xj174850@163.com)
# @Link    : https://github.com/NeuObito

import os
import pandas as pd
import matplotlib.pyplot as plt

# yob1880.txt是一个非常标准的以逗号隔开的格式，所以可以使用pandas.read_csv将其加载到DataFrame中
names1880 = pd.read_csv('yob1880.txt', names=['name', 'sex', 'births'])

# 使用births列的sex分组小计表示年度的Births总和
# print(names1880.groupby('sex').births.sum())

# 将分散的数据组装到一个DataFrame中
years = range(1880, 2011)

pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    filename = "yob%d.txt" % year
    frame = pd.read_csv(filename, names=columns)

    frame['year'] = year
    pieces.append(frame)

# ignore_index设置为True，表示不保留read_csv所返回的原始行号
names = pd.concat(pieces, ignore_index=True)
total_births = names.pivot_table('births', index='year', columns='sex', aggfunc=sum)
# print(total_births['F'].axes[0].values)


def add_prop(group):
    # 整数除法会向下调整
    births = group.births.astype(float)

    group['prop'] = births / births.sum()
    return group


def get_top1000(group):
    return group.sort_index(by='births', ascending=False)[:1000]


def get_quantile_count(group, q=0.5):
    group = group.sort_index(by='prop', ascending=False)
    return group.prop.cumsum().searchsorted(0.5) + 1


if __name__ == '__main__':
    # 绘制曲线图
    # x = total_births.axes[0].values
    # y1 = total_births['F'].values
    # y2 = total_births['M'].values

    # plt.plot(x, y1, label='F')
    # plt.plot(x, y2, label='M')

    # plt.title('line chart')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.legend()
    # plt.show()

    names = names.groupby(['year', 'sex']).apply(add_prop)
    grouped = names.groupby(['year', 'sex'])
    top1000 = grouped.apply(get_top1000)

    boys = top1000[top1000.sex == 'M']
    girls = top1000[top1000.sex == 'F']
    total_births = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)

    subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
    years = subset.John.axes[0].values

    # 绘制多图
    # plt.figure()

    # #figure分成四行一列，取得第一个子图的句柄，第一个子图跨度为一行一列，起点是表格(0, 0)
    # ax1 = plt.subplot2grid((4, 1), (0, 0), rowspan=1, colspan=1)
    # ax1.plot(years, subset.John.values, label='John')

    # # 取第二个图的句柄，起点为(1, 0)
    # ax2 = plt.subplot2grid((4, 1), (1, 0), rowspan=1, colspan=1)
    # ax2.plot(years, subset.Harry.values, label='John')

    # ax3 = plt.subplot2grid((4, 1), (2, 0), rowspan=1, colspan=1)
    # ax3.plot(years, subset.Mary.values, label='John')

    # ax4 = plt.subplot2grid((4, 1), (3, 0), rowspan=1, colspan=1)
    # ax4.plot(years, subset.Mary.values, label='John')

    # plt.show()

    # table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)

    # # 绘制线图
    # plt.plot(table.axes[0].values, table.F.values)
    # plt.plot(table.axes[0].values, table.M.values)
    # plt.show()

    # 统计出生人数前50%的不同名字的数量
    # 统计2010年出生的男孩数量
    df = boys[boys.year == 2010]
    prop_cumsum = df.sort_index(by='prop', ascending=False).prop.cumsum()

    diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
    diversity = diversity.unstack('sex')
    # 绘制线图
    # plt.plot(diversity.axes[0].values, diversity.F.values)
    # plt.plot(diversity.axes[0].values, diversity.M.values)
    # plt.show()
