# -*- coding: utf-8 -*-
from celery import Celery, task
from celery.schedules import crontab
from celery.task import periodic_task
from common.log import logger

@task()
def ngTask(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.info("手动任务执行")
    return x + y

@periodic_task(run_every=crontab(minute='*', hour='*', day_of_week="*"))
def ngTask2():
    """
    定义一个 celery 异步任务
    """
    logger.info("周期性执行任务")