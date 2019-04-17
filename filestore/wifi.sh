#!/bin/bash

function wifi_scan {
    /System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport scan
}

function wifi_hardware {
    networksetup -listallhardwareports
}

function wifi_on {
    networksetup -setairportpower en0 on
}

function wifi_off {
    networksetup -setairportpower en0 off
}

function wifi_connect {
    networksetup -setairportnetwork en0 $2 $3
}

if [ $1 = "scan" ]; then
    wifi_scan
elif [ $1 = "hardware" ]; then
    wifi_hardware
elif [ $1 = "on" ]; then
    wifi_on
elif [ $1 = "off" ]; then
    wifi_off
elif [ $1 = "connect" ]; then
    wifi_connect
else
  echo "no action"
fi
