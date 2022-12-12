#!/bin/bash

# check if "ip" command is available
if command -v ip &> /dev/null; then 
    # look at protocol addresses of all available devices
    ip -4 addr show | grep inet | awk '{print $NF " " $2}'
fi