FROM alpine:latest

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools kafka-python pymongo 

WORKDIR /app 

COPY *.py ./

CMD python3 -u db-consumer.py