# syntax=docker/dockerfile:1
FROM python:3.9.13-alpine
RUN pip install --upgrade pip
WORKDIR /docker-restfullapp
COPY requirements.txt /docker-restfullapp/requirements.txt
RUN apk add build-base
RUN pip install -r requirements.txt
COPY .. /docker-restfullapp
CMD ["python", "main.py"]