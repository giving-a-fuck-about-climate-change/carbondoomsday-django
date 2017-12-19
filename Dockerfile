FROM jfloff/alpine-python:latest

WORKDIR /carbondoomsday/
COPY . /carbondoomsday/

RUN apk add --update --no-cache build-base postgresql-dev python3-dev

RUN pip install pipenv

RUN pipenv install
