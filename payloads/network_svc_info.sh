#!/bin/bash

# define what host discovery techniques should be used 
#   - see https://nmap.org/book/host-discovery-techniques.html
#   - privileged users "default" would be "-PE -PS443 -PA80 -PP"
HOST_DISC_OPTS="-PS443 -PA80" 
# define input options to improve scan time
#   - intuition on selected values: https://nmap.org/book/man-performance.html
TIME_OPTS="-T4 --max-rtt-timeout 100ms --max-retries 0 --min-parallelism 10"
# assume first arg passed will always contain an IPv4 network address
TRG=$1

# check if command "nmap" is available
if command -v nmap &> /dev/null; then
    # perform ping scan of network and capture "up" hosts in UP_HOSTS_LIST
    UP_HOSTS_LIST=$(nmap -sn $HOST_DISC_OPTS $TIME_OPTS $TRG | awk '/Nmap scan/{gsub(/[()]/,"",$NF); print $NF}')
    nmap -oG up_hosts_scan.txt $UP_HOSTS_LIST &> /dev/null
    cat up_hosts_scan.txt | grep -v "Status" | grep -v "Nmap"
    rm up_hosts_scan.txt
fi