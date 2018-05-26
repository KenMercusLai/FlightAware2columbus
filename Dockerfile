FROM python:3.6

WORKDIR /opt

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get -y install graphviz && \
    pip install pipenv && \
    pipenv run pip install pyinotify

