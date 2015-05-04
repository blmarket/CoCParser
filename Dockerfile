FROM python:3

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y gfortran libblas-dev liblapack-dev && \
    pip install numpy && \
    pip install scipy && \
    mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install -r requirements.txt

COPY . /usr/src/app
