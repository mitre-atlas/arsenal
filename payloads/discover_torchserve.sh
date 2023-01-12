#!/bin/bash

PING_PATH="{$1}/ping"
DESCRIPTION_PATH="{$1}/api-description"
INFERENCE_ENTRY_POINT_PATH="{$1}/predictions"
MODELS_ENTRY_POINT_PATH="{$1}/models"


# check if "curl" command is available
if command -v curl &> /dev/null; then
    # first, try "Health API" (https://pytorch.org/serve/inference_api.html#health-check-api),
    # Management API will not return "Healthy" in the output
    if curl -s PING_PATH | grep "Healthy"; then
        echo "INFERENCE API" && echo $INFERENCE_ENTRY_POINT_PATH
    elif curl -s DESCRIPTION_PATH | grep "List registered models in TorchServe."; then
        echo "MANAGEMENT API" && echo $MODELS_ENTRY_POINT_PATH
    fi
fi