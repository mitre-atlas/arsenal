#!/bin/bash

if command -v curl &> /dev/null; then
    model="$1/models"
    # this is only tested for one model in ip_addr/models
    if curl -s $model | grep "modelName" >> /dev/null; then
        model_name="$(curl -s $model | grep "modelName" | awk -F '"' '{print $4}')"
        echo "MODEL $model_name"
    else
        echo "MODEL null"
    fi
fi