# import pymysql
#
# pymysql.install_as_MySQLdb()

from __future__ import absolute_import, unicode_literals

# 让 Django 在启动时加载 Celery
# Django が起動時に Celery をロードするようにする
from .celery import app as celery_app

__all__ = ('celery_app',)
