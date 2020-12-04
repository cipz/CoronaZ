FROM alpine:latest

ENV PYTHONUNBUFFERED=1
ENV RUN_ARGS=""

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools kafka-python pymongo

WORKDIR /app 

COPY *.py ./
COPY config.json ./

CMD python3 main.py -s kafka:9092 coronaz ${RUN_ARGS} --config-file ./config.json