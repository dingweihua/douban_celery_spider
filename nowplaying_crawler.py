#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2017/12/25 下午7:09

from tasks.workers import app


def get_nowplaying_detail():
    """
    获取正在上映的电影详情列表
    :return:
    """
    app.send_task('tasks.movie.crawl_nowplaying')


def get_nowplaying_detail_list():
    """
    获取正在上映的电影详情列表
    :return:
    """
    app.send_task('tasks.movie.crawl_nowplaying_id_list')


def get_movie_detail(douban_id):
    """
    获取正在上映的电影详情列表
    :return:
    """
    app.send_task('tasks.movie.crawl_movie_detail', args=(douban_id,))


if __name__ == '__main__':
    # get_nowplaying_detail()
    # get_nowplaying_detail_list()
    douban_id = '27011205'
    get_movie_detail(douban_id)
