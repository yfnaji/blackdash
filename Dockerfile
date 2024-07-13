FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install build-essential -y

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN g++ -std=c++11 calculations/longstaffschwartz/longstaff_schwartz.cpp calculations/longstaffschwartz/main.cpp -o calculations/longstaffschwartz/main

EXPOSE 80/tcp
EXPOSE 443/tcp

CMD [ "python3", "server.py" ]