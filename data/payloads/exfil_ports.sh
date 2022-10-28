#!/bin/bash

ips=$(ip addr | grep inet | grep -v "inet6" | awk '{print $2 " " $8}')
echo $ips
