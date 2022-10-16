#!/bin/bash

tmux new-session -d -s marketplace_bot
tmux send-keys -t marketplace_bot 'python3 buyAxies.py' C-m
tmux a