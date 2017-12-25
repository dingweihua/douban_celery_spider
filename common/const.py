#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2017/12/25 下午9:56

HOST = 'https://movie.douban.com'
SEARCH_URL = 'https://movie.douban.com/cinema/nowplaying'
SUBJECT_URL = 'https://movie.douban.com/subject/{}'
REQ_TIMEOUT = 5
PROXIES = {'http': '110.88.31.99:808'}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Connection': 'keep-alive',
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}
