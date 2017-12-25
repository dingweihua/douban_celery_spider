#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2017/12/25 下午7:10

import requests
from bs4 import BeautifulSoup

from common import const


def get_nowplaying_id_list():
    """
    获取正在上映的电影页面列表
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
        douban_id_list.append(douban_id)
    return douban_id_list


if __name__ == '__main__':
    print()
