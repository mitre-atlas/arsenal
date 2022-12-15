#!/bin/bash

# check if "ip" command is available
if command -v ip &> /dev/null; then 
    # look at protocol addresses of all available devices
    if [ $# -eq 0 ]; then
        ip -4 addr show | grep -A 2 "LOWER_UP" | grep inet | awk '{print $NF " " $2}'
    # look at protocol address of a specific device
    else
        ip -4 addr show dev $1 | grep -A 2 "LOWER_UP" | grep inet | awk '{print $NF " " $2}'
    fi
fi