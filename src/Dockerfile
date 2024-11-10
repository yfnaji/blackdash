FROM python:3.11-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install build-essential -y

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

RUN pip install --no-cache-dir -r requirements.txt
RUN g++ -std=c++11 calculations/longstaffschwartz/longstaff_schwartz.cpp calculations/longstaffschwartz/main.cpp -o calculations/longstaffschwartz/main

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server:srv"]