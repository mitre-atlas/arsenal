import argparse
import sys
import json
import requests

import numpy as np
from io import BytesIO
from PIL import Image

import counterfit
# from counterfit.core.targets import CFTarget

import logging
# step 1: retrieve "model name" from passed in args.endpoint
# step 2: for each key in model_arch dict, check if key in "model name". if found, store in arch_type
# step 3: map arch_type to BaseTargetFor<arch_type>DataType 
# ASIDE on differences for each created ImageDataType target:
# - image_file_path
# - 
# step 4: 


def setup_args():
    """Parse command line options (mode and config)."""
    parser = argparse.ArgumentParser(description="Build CFTarget.")
    help_s = "API route or model file location where Counterfit will collect outputs."
    parser.add_argument("--endpoint", help=help_s, required=True, type=str)
    help_s, choices = "The type of data the target model uses.", ["tabular", "text", "images"]
    parser.add_argument("--data-type", help=help_s, choices=choices, default="images", type=str)
    help_s = "This is used to uniquely identify a target model within Counterfit."
    parser.add_argument("--target-name", help=help_s, required=True, type=str)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()
def main():
    print(counterfit.__version__)

if __name__ == "__main__":
    main()