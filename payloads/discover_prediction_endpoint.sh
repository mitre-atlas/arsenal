#!/bin/bash

if command -v curl &> /dev/null; then
    model="$1/models"
    # this is only tested for one model in ip_addr/models
    if curl -s $model | grep "modelName" >> /dev/null; then
        model_name="$(curl -s $model | grep "modelName" | awk -F '"' '{print $4}')"
        echo "$1 $model_name"
    else
        echo "$1 null"
    fi
fi