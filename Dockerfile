FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get upgrade -y
RUN pip install -r requirements.txt
RUN apt-get install build-essential -y
RUN g++ -std=c++11 calculations/longstaffschwartz/longstaff_schwartz.cpp calculations/longstaffschwartz/main.cpp -o calculations/longstaffschwartz/main

EXPOSE 8050/tcp

CMD [ "python3", "server.py" ]
