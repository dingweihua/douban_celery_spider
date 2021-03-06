#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@126.com)
#
# Created: 2017/12/25 下午9:34

from celery import Celery
from kombu import Queue, Exchange

import config

broker = 'amqp://myuser:password@127.0.0.1:5672/myvhost'
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
        Queue(
            name='bt',
            exchange=Exchange('bt', type='direct'),
            routing_key='bt'
        ),
        Queue(
            name='ed2k',
            exchange=Exchange('ed2k', type='direct'),
            routing_key='ed2k'
        ),
    ),
    CELERY_ROUTES={
        'tasks.movie.crawl_nowplaying_id_list': {'queue': 'celery', 'routing_key': 'celery'},
        'tasks.movie.douban_get_subject_id_list': {'queue': 'celery', 'routing_key': 'celery'},
        'tasks.movie.crawl_movie_detail': {'queue': 'movie_detail', 'routing_key': 'movie_detail'},
        'tasks.movie.group_crawl_movie_detail': {'queue': 'movie_detail', 'routing_key': 'movie_detail'},
        'tasks.movie.douban_get_movie_resource_by_group': {'queue': 'celery', 'routing_key': 'celery'},
        'tasks.movie.douban_get_movie_resource': {'queue': 'celery', 'routing_key': 'celery'},
        'tasks.movie.get_multi_movie_resource_by_group': {'queue': 'celery', 'routing_key': 'celery'},
        'tasks.movie.bt_get_movie_resource': {'queue': 'bt', 'routing_key': 'bt'},
        'tasks.movie.ed2k_get_movie_resource': {'queue': 'ed2k', 'routing_key': 'ed2k'},
    }
)
