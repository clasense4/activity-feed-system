FROM python:3.6.8-alpine

RUN apk update \
  && apk add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . .