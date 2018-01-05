#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2018/1/5 下午10:24

from tasks.workers import app


def get_douban_subject_id_list(tag, sort, page_start, page_limit):
    """
    按subject获取豆瓣电影id列表
    :param tag:
    :param sort:
    :param page_start:
    :param page_limit:
    :return:
    """
    app.send_task(
        'tasks.movie.douban_get_subject_id_list',
        args=(tag, sort, page_start, page_limit,)
    )


if __name__ == '__main__':
    tag = u'经典'
    sort = 'recommend'
    page_start = 0
    page_limit = 200
    get_douban_subject_id_list(tag, sort, page_start, page_limit)
