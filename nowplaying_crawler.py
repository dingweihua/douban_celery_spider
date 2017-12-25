#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2017/12/25 下午7:09

from movie import movie_list
from tasks.workers import app


def get_nowplaying_detail_list():
    """
    获取正在上映的电影详情列表
    :return:
    """
    douban_id_list = movie_list.get_nowplaying_id_list()
    for douban_id in douban_id_list:
        app.send_task(
            'tasks.movie_detail.get_movie_detail', args=(douban_id,)
        )


if __name__ == '__main__':
    get_nowplaying_detail_list()
