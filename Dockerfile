FROM ubuntu:latest
MAINTAINER Shaobo Liu <shaobo@mkdef.com>
LABEL Description="This image is used to odes."
RUN apt-get update -y
RUN apt-get install -y libxml2-dev libxslt1-dev libpq-dev
RUN apt-get install -y python3-pip python3-dev build-essential
ARG POSTGRES_ADDR
ARG POSTGRES_USER 
ARG POSTGRES_PASSWORD
ENV POSTGRES_ADDR=$POSTGRES_ADDR 
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD 
COPY src/api /app
COPY requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]