from celery import Celery

# Note: On Windows with standard Redis usage, 
# ensure Redis server is running at localhost:6379

celery_app = Celery(
    "video_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=['app.tasks.video_tasks']
)

# celery_app.conf.task_routes = {
#     "app.tasks.video_tasks.*": {"queue": "video"}
# }

# Windows compatibility setting (sometimes needed)
celery_app.conf.broker_connection_retry_on_startup = True
