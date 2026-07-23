#!/bin/bash

sleep 8

export DISPLAY=:0
export XAUTHORITY=/home/tristan/.Xauthority

cd /home/tristan/recordmate || exit 1

exec /home/tristan/recordmate/venv/bin/python \
    /home/tristan/recordmate/src/app.py \
    >> /home/tristan/recordmate/recordmate.log 2>&1