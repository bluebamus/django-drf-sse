# django-drf-sse

Let's implement Server-Sent-Events (SSE) using django and drf. It works based on asynchronous operations using Celery and Redis.

# command

- daphne -b 0.0.0.0 -p 8000 config.asgi:application
- for windows
  - celery --app=config worker -l INFO -P gevent
