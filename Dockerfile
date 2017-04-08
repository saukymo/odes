FROM ubuntu:latest
MAINTAINER Shaobo Liu <shaobo@mkdef.com>
LABEL Description="This image is used to odes."
RUN apt-get update -y
RUN apt-get install -y libpq-dev
RUN apt-get install -y python3-pip python3-dev build-essential
COPY src/api /app
COPY requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]