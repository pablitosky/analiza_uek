FROM python:3.12-slim

COPY ./requirements.txt /app/requirements.txt
# dependencies
WORKDIR /app
RUN pip install setuptools
RUN pip install -r requirements.txt

COPY . /app