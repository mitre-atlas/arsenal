#!/bin/bash

ips=$(ip addr| grep scope.global | awk '{print $2 " " $8}')
timeout 30s nmap -oN '/tmp/nmap_scan.txt' -sn $ips