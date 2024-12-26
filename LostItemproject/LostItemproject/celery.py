from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置默认的 Django settings 模块
# デフォルトの Django 設定モジュールを設定する
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LostItemproject.settings')

# 创建 Celery 应用
# Celeryアプリケーションの作成
app = Celery('LostItemproject')

# 从 Django 的 settings 中加载配置
# Django の設定から設定を読み込む
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
# 自動検出タスク
app.autodiscover_tasks()

# 设置 Celery Beat 的调度器为 django_celery_beat 的 DatabaseScheduler
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
