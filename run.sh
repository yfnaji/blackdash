#!/bin/sh

pip3 install virtualenv

if [ $# -eq 1 ]; then
    if [ "$1" = "--debug" ]; then
        debug="debug"
    else
        debug="_"
    fi
else
    debug="_"
fi

if ! [[ -d blackdash-venv ]]; then
    python3 -m venv blackdash-venv
fi

if [[ "$OSTYPE" = "msys" ]] || [[ "$OSTYPE" = "cygwin" ]]; then
    call blackdash-venv/Scripts/activate
else
    source blackdash-venv/bin/activate
fi

pip install -r requirements.txt
g++ -std=c++11 calculations/longstaffschwartz/longstaff_schwartz.cpp calculations/longstaffschwartz/main.cpp -o calculations/longstaffschwartz/main

python server.py $debug
