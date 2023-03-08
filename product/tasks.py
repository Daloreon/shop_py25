from celery import shared_task

@shared_task
def big_function():
    import time
    time.sleep(10) 