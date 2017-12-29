#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2017/12/25 下午9:34

from celery import Celery
from kombu import Queue, Exchange

import config

broker = 'amqp://myuser:password@127.0.0.1/myvhost'
backend = 'redis://127.0.0.1:6379/0'
tasks = [
    'tasks.movie',
]

app = Celery(
    'douban_celery_spider', include=tasks, broker=broker, backend=backend
)

app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERYD_LOG_FILE=config.WORKER_LOG,
    CELERYBEAT_LOG_FILE=config.BEAT_LOG,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_QUEUES=(
        Queue(
            name='celery',
            exchange=Exchange('celery', type='direct'),
            routing_key='celery'
        ),
        Queue(
            name='movie_detail',
            exchange=Exchange('movie_detail', type='direct'),
            routing_key='movie_detail'
        ),
    ),
    CELERY_ROUTES={
        'tasks.movie.crawling_nowplaying': {'queue': 'celery', 'routing_key': 'celery'},
        'tasks.movie.crawl_movie_detail': {'queue': 'movie_detail', 'routing_key': 'movie_detail'},
    }
)
