#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2017/12/25 下午7:11

import requests
from bs4 import BeautifulSoup
from celery import group

from common import const
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
def crawl_nowplaying():
    """
    爬取正在热映的电影
    :return:
    """
    search_url = const.SEARCH_URL
    res_search = requests.get(
        search_url,
        headers=const.HEADERS,
        proxies=const.PROXIES,
        timeout=const.REQ_TIMEOUT
    )
    soup_search = BeautifulSoup(res_search.content, 'lxml')

    content_tag = soup_search.find('div', id='nowplaying')
    if not content_tag:
        return []
    # 搜索列表
    list_tag = content_tag.find('ul', class_='lists')
    if not list_tag:
        return []
    douban_id_list = []
    # 电影详情信息
    for li_tag in content_tag.find_all('li', class_='list-item'):
        douban_id = li_tag.attrs.get('id', '')
        if not douban_id:
            continue
        app.send_task('tasks.movie.crawl_movie_detail', args=(douban_id,))
        douban_id_list.append(douban_id)
    return douban_id_list
