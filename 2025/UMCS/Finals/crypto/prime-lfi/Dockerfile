FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.11 python3.11-venv socat gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY challenge /app

RUN python3.11 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install nprime
    # need for the miller primarily test

EXPOSE 5000

USER root

CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:"/app/venv/bin/python3 -u /app/server.py",stderr
