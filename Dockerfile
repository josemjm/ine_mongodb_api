FROM mongo:latest

EXPOSE 27017

# install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get -y install python3.8

FROM python:3.8

WORKDIR /ine_mongodb_api
COPY ./ ./
RUN pip3 install -r requirements.txt

CMD ["/bin/bash"]