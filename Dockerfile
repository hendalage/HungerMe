ARG APP_IMAGE=python:3.10.1-alpine

FROM $APP_IMAGE AS base

ENV FLASK_APP project


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "-m" , "flask", "run"]
