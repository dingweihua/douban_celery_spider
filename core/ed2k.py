#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2018/1/6 下午5:19

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


def crawl_movie_search_list(title):
    """
    获取电影搜索列表
    :param title:
    :return:
    """
    search_url = const.ED2K_SEARCH_URL
    data = {'SearchWord': title}
    try:
        res_search = requests.post(
            search_url,
            data,
            headers=const.HEADERS,
            # proxies=const.PROXIES,
            timeout=const.REQ_TIMEOUT
        )
    except TimeoutError:
        return []
    soup_search = BeautifulSoup(res_search.content, 'html.parser')
    # 搜索列表
    content_tag = soup_search.find('table', class_='CommonListArea')
    if not content_tag:
        return []
    search_list = []
    # 电影详情信息
    for table_tag in content_tag.find_all('tr', class_='CommonListCell'):
        is_movie = False
        for a_tag in table_tag.find_all('a'):
            a_tag_href = a_tag.attrs.get('href', '')
            if not is_movie:
                if a_tag_href == u'/Type/电影':
                    is_movie = True
                    continue
            if re.match(r'^/ShowFile/.*\.html', a_tag_href):
                search_list.append(const.ED2K_HOST + a_tag_href)
                break
    return search_list


def crawl_movie_resource(movie_url):
    """
    根据影片详情链接获取下载资源
    :param movie_url:
    :return:
    """
    try:
        res_detail = requests.get(
            movie_url, headers=const.HEADERS, timeout=const.REQ_TIMEOUT
        )
    except TimeoutError:
        return []
    soup_detail = BeautifulSoup(res_detail.content, 'html.parser')
    resources = []
    ignore_starts = ('/Profile.asp', 'http://', 'https://')
    # 下载资源列表
    for table_tag in soup_detail.find_all('table', class_='CommonListArea'):
        for tr_tag in table_tag.find_all('tr', class_='CommonListCell'):
            for a_tag in tr_tag.find_all('a'):
                if a_tag.parent.name != 'td':
                    continue
                resource = a_tag.get('href')
                if resource.startswith(ignore_starts):
                    continue
                resources.append(resource)
        # 下载链接可能是通过<script></script>渲染出来的
        script_tag = table_tag.find('script')
        if not script_tag:
            continue
        script_text = script_tag.get_text()
        if 'ShowMagnet' in script_text:
            magnets = re.findall(r'ShowMagnet\(\"(.*)\"\)', script_text)
            if magnets:
                resources.extend(magnets)
    return resources
