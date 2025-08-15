#!/usr/bin/env fish
# this probably only works on my computer
redis-server --port 3001 &
cdv .
ls *.py | entr -r python3 app.py
