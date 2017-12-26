#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2017/12/25 下午7:11

import requests
from bs4 import BeautifulSoup

from common import const
from tasks.workers import app


@app.task()
def crawl_movie_detail(douban_id):
    """
    根据电影id获取电影详情信息
    :param douban_id:
    :return:
    """
    subject_url = const.SUBJECT_URL.format(douban_id)
    movie_detail = {
        'douban_id': douban_id,
        'title': '',
        'director': '',
        'actors': [],
        'imdb': ''
    }
    # 获取电影详情页
    try:
        res_page = requests.get(
            subject_url,
            headers=const.HEADERS,
            proxies=const.PROXIES,
            timeout=const.REQ_TIMEOUT
        )
    except TimeoutError:
        print(u'豆瓣电影详情无法访问')
        return movie_detail

    # 电影信息
    soup_movie = BeautifulSoup(res_page.content, 'lxml')
    content = soup_movie.find('div', id='content')
    if not content:
        return movie_detail
    # 片名
    title_tag = content.find('span', property='v:itemreviewed')
    if title_tag:
        movie_detail['title'] = title_tag.get_text()
    # 电影详情
    clearfix = content.find('div', class_='subject clearfix')
    if not clearfix:
        return movie_detail
    # 导演
    director_tag = clearfix.find(rel='v:directedBy')
    if director_tag:
        movie_detail['director'] = director_tag.get_text()
    # 主演
    for actor_tag in clearfix.find_all(rel='v:starring'):
        actor = actor_tag.get_text()
        if not actor:
            continue
        movie_detail['actors'].append(actor)
    # IMDb链接
    imdb_tag = clearfix.find('a', rel='nofollow')
    if imdb_tag:
        movie_detail['imdb'] = imdb_tag.attrs.get('href', '')
    return movie_detail


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
