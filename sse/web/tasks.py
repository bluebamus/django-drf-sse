import time
from celery import shared_task
from celery.signals import task_prerun, task_postrun, task_failure
from config.celery import app


@shared_task
def add(x, y):
    return x + y


@shared_task(bind=True)
def multitasking_update_state(self, x, y):
    result = x + y
    for i in range(1, 6):
        intermediate_result = result * (2 * i)
        print(f"intermediate_result : {i} : {intermediate_result}")
        self.update_state(
            state="IN_PROGRESS", meta={"current": i, "result": intermediate_result}
        )
        time.sleep(1)  # 작업 진행을 위한 대기 시간 (예시)

    self.update_state(state="SUCCESS")
    return {"status": "Task completed!"}


# daphne -b 0.0.0.0 -p 8000 config.asgi:application

# celery --app=config worker -l INFO -P gevent
