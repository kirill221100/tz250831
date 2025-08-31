FROM python:3.12-slim
RUN apt-get -y update
RUN apt-get -y upgrade
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
