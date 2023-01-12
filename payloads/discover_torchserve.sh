#!/bin/bash

# store each bind addr as element in array (from target.api.binding_address_list)
IFS=', ' read -r -a candidates_arr <<< "$1"

# check if "curl" command is available
if command -v curl &> /dev/null; then
    # iterate over each binding address
    for bind_addr in "${candidates_arr[@]}"
    do
        ping_path="$bind_addr/ping"
        description_path="$bind_addr/api-description"
        inference_entry_point_path="$bind_addr/predictions"
        models_entry_point_path="$bind_addr/models"
        # echo $ping_path
        # first, try "Health API" (https://pytorch.org/serve/inference_api.html#health-check-api),
        # Management API will not return "Healthy" in the output
        if curl -s $ping_path | grep "Healthy" &> /dev/null; then
            echo "INFERENCE_API $inference_entry_point_path"
        elif curl -s $description_path | grep "List registered models in TorchServe." &> /dev/null; then
            echo "MANAGEMENT_API $models_entry_point_path"
        fi
    done
fi