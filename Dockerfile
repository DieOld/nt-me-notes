FROM python:3.7-slim as base
WORKDIR /notes
ENV PYTHONBUFFERED True
COPY requiremetns.txt .
RUN pip3 install -r requiremetns.txt
COPY swagger /swagger
COPY src .