#!/usr/bin/env bash
port=52697
# Send pwd and path
echo -e "$(pwd)\n$1" | nc 0 $port
jumpapp sublime_text