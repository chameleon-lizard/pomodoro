#!/bin/sh

sudo cp pomodoro.py /usr/local/bin/pomodoro
sudo chmod +x /usr/local/bin/pomodoro

mkdir -p ~/.cache/pomodoro
touch ~/.cache/pomodoro/data
