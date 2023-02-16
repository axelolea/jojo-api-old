FROM python:3.10.6-slim-buster

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install netcat gcc postgresql libpq-dev \
    && apt-get clean

# install application dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/
RUN chmod +x /usr/src/entrypoint.sh