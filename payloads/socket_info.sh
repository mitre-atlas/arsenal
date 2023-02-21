#!/bin/bash


# Check if "ss" command is available
if command -v ss &> /dev/null; then 
    # Show TCP connections (-t) in listening (-l) state, w/o resolving the IP addresses 
    # and the port number (-n). Output format is <"Local Address:Port" "Process">. 
    # - Ex. row: 127.0.0.1:33203 users:(("containerd",pid=120,fd=8))

    # Check (1) "sudo" command available and (2) current user is "sudo" group member
    if command -v sudo &> /dev/null && id -nG "$USER" | grep -qw "sudo"; then
        # Display the name of the process using the socket (-p)
        sudo ss -t -l -n -p | grep -v "State" | awk '{print $4 " " $6}'
    else 
        # If available to user, display the name of the process using the socket (-p)
        ss -t -l -n -p | grep -v "State" | awk '{print $4 " " $6}'
    fi
fi