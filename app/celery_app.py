from celery import Celery

celery_app = Celery(
    "task",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=[
        "app.modules.research.task"
    ],  # explicit include, matches your actual filename
)
