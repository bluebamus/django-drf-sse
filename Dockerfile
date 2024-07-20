FROM python:3.11.1

ENV PYTHONUNBUFFERED 1

ARG DEV=false

RUN pip install --no-cache-dir poetry

# RUN if [ $DEV = true ]; then poetry install --no-dev
# RUN if [ $DEV = true ]; then poetry install --E redis

EXPOSE 8000
