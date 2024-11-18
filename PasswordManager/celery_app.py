from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "tasks",
    broker="redis://redis_pass:6380/0",
    backend="redis://redis_pass:6380/0",
)


celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "delete password for inactive": {
            "task": "jobs.tasks.print_message",
            "schedule": crontab(hour=0, minute=0),
        },
    },
)
