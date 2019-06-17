#!/bin/bash

function wifi_scan {
    /System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport scan
}

function wifi_pref {
    networksetup -listpreferredwirelessnetworks en0
}

function wifi_on {
    networksetup -setairportpower en0 on
}

function wifi_off {
    networksetup -setairportpower en0 off
}

if [ $1 = "scan" ]; then
    wifi_scan
elif [ $1 = "pref" ]; then
    wifi_pref
elif [ $1 = "on" ]; then
    wifi_on
elif [ $1 = "off" ]; then
    wifi_off
else
  echo "no action"
fi
