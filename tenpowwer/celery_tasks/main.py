from celery import Celery

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tenpowwer.settings")
# 3.创建celery实例
app = Celery('celery_tasks')
# 3.加载celery配置
app.config_from_object('celery_tasks.config')
# 4.自动注册celery任务
app.autodiscover_tasks(['celery_tasks.sms'])


