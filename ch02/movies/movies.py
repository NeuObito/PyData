#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-29 14:56:13
# @Author  : xuejun (xuemyjun@gmail.com)
# @Link    : https://github.com/NeuObito

import os
import pandas as pd

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('users.dat', sep="::", header=None, names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('ratings.dat', sep="::", header=None, names=rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('movies.dat', sep="::", header=None, names=mnames)

# 将数据合并
data = pd.merge(pd.merge(ratings, users), movies)

# 按性别计算每部电影的平均分
mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
# print(mean_ratings[:5])

# 过滤掉评分不足250的电影
ratings_by_title = data.groupby('title').size()
active_titles = ratings_by_title.index[ratings_by_title > 250]
# print(active_titles)

mean_ratings = mean_ratings.ix[active_titles]
# print(mean_ratings)

# 为了了解女性观众喜欢的电影，可以对F列降序排列
top_female_ratings = mean_ratings.sort_index(by='F', ascending=False)
# print(top_female_ratings[:10])

# 找出男性和女性评分分歧最大的电影
# 一个办法是给mean_ratings加上一个用于存放平均得分之差的列，并对其进行排序
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_index(by="diff")
# print(sorted_by_diff[:10])

# 如果只是想找出分歧最大的电影（不考虑性别因素），则可以计算得分数据的方差或者标准差
# 根据电影名称分组的得分数据的标准差
rating_std_by_title = data.groupby(by='title')['rating'].std()
# 根据active_titles进行过滤
rating_std_by_title = rating_std_by_title.ix[active_titles]
# 根据值对Series进行降序排列
rating_std_by_title.order(ascending=False)[:10]
print(rating_std_by_title)
