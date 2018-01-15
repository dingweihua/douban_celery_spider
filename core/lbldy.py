#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2018/1/15 下午7:53

import re
import requests
import time
from bs4 import BeautifulSoup

from common import const


def crawl_movie_resources(movie_info):
    """
    根据电影信息抓取电影下载资源
    :param movie_info:
    :return:
    """
    title = movie_info.get('title', '')
    search_list = crawl_movie_search_list(title)
    time.sleep(1)
    res_list = []
    for detail_url in search_list:
        resources = crawl_movie_resource(detail_url)
        time.sleep(1)
        if resources:
            res_list.extend(resources)
    return res_list


def crawl_movie_search_list(name):
    """
    龙部落获取电影搜索列表
    :param name:
    :return:
    """
    search_url = '{}/{}'.format(const.LBLDY_SEARCH_URL, name)
    res_search = requests.get(search_url, headers=const.HEADERS, timeout=const.REQ_TIMEOUT)
    soup_search = BeautifulSoup(res_search.content, 'lxml')
    # 搜索列表
    content_tag = soup_search.find('div', id='center')
    if not content_tag:
        return []
    search_list = []
    # 电影详情信息
    for table_tag in content_tag.find_all(class_='postlist'):
        a_tag = table_tag.find('a', rel='bookmark')
        if not a_tag:
            continue
        detail_url = a_tag.attrs.get('href', '')
        if detail_url:
            search_list.append(detail_url)
    return search_list


def crawl_movie_resource(movie_url):
    """
    根据影片详情链接获取下载资源
    :param movie_url:
    :return:
    """
    res_detail = requests.get(movie_url, headers=const.HEADERS, timeout=const.REQ_TIMEOUT)
    soup_detail = BeautifulSoup(res_detail.content, 'lxml')
    # 下载资源列表
    content_tag = soup_detail.find('div', class_='entry')
    if not content_tag:
        return []
    resources = []
    res_starts = False
    for p_tag in content_tag.find_all('p'):
        # <p>下载地址：</p>之后的<p>为下载资源
        p_tag_text = p_tag.get_text()
        if p_tag_text.startswith(u'下载地址'):
            res_starts = True
        if not res_starts:
            continue

        a_tag = p_tag.find('a')
        if not a_tag:
            continue
        resource = a_tag.get('href')
        # 判断网盘/云盘
        if u'网盘' in p_tag_text or u'云盘' in p_tag_text:
            resource = re.sub(r'<a>.*</a>', resource, p_tag_text)
        # 只抓取下载资源
        if resource.startswith(('http://', 'https://')):
            continue
        resources.append(resource)
    return resources
