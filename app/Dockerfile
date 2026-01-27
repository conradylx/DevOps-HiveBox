FROM python:3.13.7-alpine@sha256:9ba6d8cbebf0fb6546ae71f2a1c14f6ffd2fdab83af7fa5669734ef30ad48844

RUN apk add --no-cache curl

RUN addgroup -g 1000 hiveboxgrp && \
    adduser -u 1000 -G hiveboxgrp -S hiveboxusr

WORKDIR /code

COPY version.txt /code/version.txt
COPY ./requirements.txt ./requirements-dev.txt /code/app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --require-hashes -r /code/app/requirements.txt && \
    chown -R hiveboxusr:hiveboxgrp /code && \
    chmod -R 750 /code

COPY --chown=hiveboxusr:hiveboxgrp . /code/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

USER hiveboxusr

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]