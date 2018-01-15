#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2017/12/25 下午7:11

from celery import group, chain

from core import douban, bttiantangs, ed2k, lbldy
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


@app.task()
def douban_get_movie_resource_by_group(douban_id_list):
    """
    grpup: 根据豆瓣电影id获取电影下载资源
    :param douban_id_list:
    :return:
    """
    group(douban_get_movie_resource.s(
        douban_id) for douban_id in douban_id_list)()


@app.task()
def douban_get_movie_resource(douban_id):
    """
    根据豆瓣电影id获取电影下载资源
    :param douban_id:
    :return:
    """
    chain(crawl_movie_detail.s(douban_id),
          get_multi_movie_resource_by_group.s())()


@app.task()
def get_multi_movie_resource_by_group(movie_info):
    """
    grpup: 获取多个电影资源网站上的下载资源
    :param movie_info:
    :return:
    """
    group(bt_get_movie_resource.s(movie_info),
          lbldy_get_movie_resource.s(movie_info),
          ed2k_get_movie_resource.s(movie_info))()


@app.task()
def bt_get_movie_resource(movie_info):
    """
    bt天堂：根据电影信息获取电影下载资源
    :param movie_info:
    :return:
    """
    return bttiantangs.crawl_movie_resources(movie_info)


@app.task()
def ed2k_get_movie_resource(movie_info):
    """
    ed2k：根据电影信息获取电影下载资源
    :param movie_info:
    :return:
    """
    return ed2k.crawl_movie_resources(movie_info)


@app.task()
def lbldy_get_movie_resource(movie_info):
    """
    lbldy：根据电影信息获取电影下载资源
    :param movie_info:
    :return:
    """
    return lbldy.crawl_movie_resources(movie_info)
