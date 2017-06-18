FROM jfloff/alpine-python:latest

WORKDIR /carbondoomsday
COPY . /carbondoomsday

RUN apk add --update \
  build-base     \
  postgresql-dev \
  python3-dev

RUN mkdir /var/log/uwsgi/

RUN pip install -U pip
RUN pip install -e .
RUN pip install -r requirements/production.txt
