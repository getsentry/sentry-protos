FROM python:3.11

WORKDIR /pkg
RUN mkdir -p pkg
COPY . /pkg