FROM ubuntu:22.04

RUN apt-get update && apt-get install -y openssh-server git bash nodejs npm curl wget vim 

RUN mkdir -p /root/.ssh
RUN mkdir -p /root/config

COPY args.sh /root/args.sh

EXPOSE 22

