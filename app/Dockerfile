FROM python:3.12-alpine
LABEL maintainer="yura.reshetnyk295@gmail.com"

ENV PYTHONDONTWRITEDYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY . .

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
      build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r requirements.txt && \
    if [ $DEV = "true" ]; \
      then /py/bin/pip install -r requirements.dev.txt ; \
    fi && \
    apk del .tmp-build-deps && \
    rm -f requirements.txt && \
    rm -f requirements.dev.txt && \
    adduser -D -H default-user

ENV PATH="/py/bin:$PATH"

USER default-user

EXPOSE 8000