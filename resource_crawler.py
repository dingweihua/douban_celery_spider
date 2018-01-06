#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2018/1/6 下午5:23

from celery import chain

from tasks import movie


def get_douban_subject_movie_resource(tag, sort, page_start, page_limit):
    """
    按subject获取豆瓣电影下载资源
    :param tag:
    :param sort:
    :param page_start:
    :param page_limit:
    :return:
    """
    chain(
        movie.douban_get_subject_id_list.s(tag, sort, page_start, page_limit),
        movie.douban_get_movie_resource_by_group.s())()


if __name__ == '__main__':
    tag = u'经典'
    sort = 'recommend'
    page_start = 0
    page_limit = 10
    # executed tasks count:
    #     douban_get_subject_id_list: 1
    #     douban_get_movie_resource_by_group: 1
    #     douban_get_movie_resource: page_limit
    #     crawl_movie_detail: page_limit
    #     get_multi_movie_resource_by_group: page_limit
    #     bt_get_movie_resource: page_limit
    #     ed2k_get_movie_resource: page_limit
    get_douban_subject_movie_resource(tag, sort, page_start, page_limit)
