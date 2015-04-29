FROM ubuntu:14.04

MAINTAINER Jeong, Heon <blmarket@gmail.com>

RUN apt-get update && \
    apt-get -y install software-properties-common git build-essential && \
    add-apt-repository -y ppa:chris-lea/node.js && \
    apt-get update && \
    apt-get -y install nodejs && \
    mkdir -p /root/CoCParser

RUN npm install -g coffee-script

ADD ../config.json /root/CoCParser/config.json
ADD . /root/CoCParser/viewer

WORKDIR /root/CoCParser/viewer

RUN npm install
RUN coffee -p --bare public/app.coffee > public/app.js

EXPOSE 80

ENV PORT 80
CMD [ "coffee", "app.coffee" ]
