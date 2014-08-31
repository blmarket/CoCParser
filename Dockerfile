FROM ubuntu:14.04

MAINTAINER Jeong, Heon <blmarket@gmail.com>

RUN echo hello

RUN apt-get update
RUN apt-get -y install software-properties-common git build-essential
RUN add-apt-repository -y ppa:chris-lea/node.js
RUN apt-get update
RUN apt-get -y install nodejs

RUN npm install -g coffee-script

ADD config.json /root/CoCParser/config.json
ADD . /root/CoCParser

WORKDIR /root/CoCParser/viewer

RUN npm install
RUN coffee -p --bare public/app.coffee > public/app.js

EXPOSE 80

ENV PORT 80
CMD [ "coffee", "app.coffee" ]
