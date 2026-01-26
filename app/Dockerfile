FROM python:3.13.7-alpine@sha256:9ba6d8cbebf0fb6546ae71f2a1c14f6ffd2fdab83af7fa5669734ef30ad48844

RUN apk add --no-cache curl

RUN addgroup -S hiveboxgrp && adduser -S -G hiveboxgrp hiveboxusr

WORKDIR /code

COPY version.txt /code/version.txt
COPY ./app/requirements.txt /code/app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --require-hashes -r /code/app/requirements.txt && \
    chown -R hiveboxusr:hiveboxgrp /code && \
    chmod -R 750 /code

COPY --chown=hiveboxusr:hiveboxgrp ./app /code/app

ENV PYTHONUNBUFFERED=1

USER hiveboxusr

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
