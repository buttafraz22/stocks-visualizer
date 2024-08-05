import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocksbackend.settings")
app = Celery("stocksbackend")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.timezone = 'Asia/Karachi'

# Task should run on 22:00 on Asia/Karachi Timezone on Tuesdays->Saturdays

app.conf.beat_schedule = {
    'data-reports-task': {
        'task': 'worker.tasks.get_daily_reports',  
        'schedule': crontab(minute=15, hour=17, day_of_week='2-6'), # 2-6: Tuesday -> Saturday
    },
}

app.autodiscover_tasks()

