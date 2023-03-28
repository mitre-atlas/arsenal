#!/bin/bash

if command -v curl &> /dev/null; then
    models_endpoint="$1/models"
    # echo $models_endpoint
    # this is only tested for one model in ip_addr/models
    if curl -s $models_endpoint | grep "modelName" >> /dev/null; then
        model_name="$(curl -s $models_endpoint | grep "modelName" | awk -F '"' '{print $4}')"
        echo "$model_name"
    # else
    #     echo "$1 null"
    fi
fi