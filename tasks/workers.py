#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2017/12/25 下午9:34

from celery import Celery

broker = 'amqp://username:password@127.0.0.1/myvhost'
backend = 'redis://127.0.0.1:6379/0'
tasks = [
    'tasks.movie_detail',
]

app = Celery(
    'douban_celery_spider', include=tasks, broker=broker, backend=backend
)

