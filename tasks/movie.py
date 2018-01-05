#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2017/12/25 下午7:11

from celery import group

from core import douban
from tasks.workers import app


@app.task()
def crawl_movie_detail(douban_id):
    """
    根据电影id获取电影详情信息
    :param douban_id:
    :return:
    """
    return douban.crawl_movie_detail(douban_id)


@app.task()
def crawl_movie_detail_by_group(douban_id_list):
    """
    根据电影id获取电影详情信息
    :param douban_id_list:
    :return:
    """
    group(crawl_movie_detail.s(douban_id) for douban_id in douban_id_list)()


@app.task()
def crawl_nowplaying_id_list():
    """
    爬取正在热映的电影豆瓣id列表
    :return:
    """
    return douban.crawl_nowplaying_id_list()


@app.task()
def douban_get_subject_id_list(tag, sort, page_start, page_limit):
    """
    按照subject获取豆瓣id列表
    :param tag:
    :param sort:
    :param page_start:
    :param page_limit:
    :return:
    """
    return douban.get_subject_id_list(tag, sort, page_start, page_limit)
