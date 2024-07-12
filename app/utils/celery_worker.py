import os
from celery import Celery

broker_url = os.getenv("CELERY_BROKER_URL")
app = Celery("worker", broker=broker_url, backend="rpc://")


@app.task
def add(x, y):
    return x + y
