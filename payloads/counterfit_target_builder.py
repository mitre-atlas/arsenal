import argparse
import sys
import os
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

MODEL_ARCHITECTURES_MAP = {
    "alexnet": "Image Classification",
    "densenet": "Image Classification",
    "resnet": "Image Classification",
    "vgg": "Image Classification",
    "mobilenet": "Image Classification",
    "squeezenet": "Image Classification",
    "rcnn": "Object Detection",
    "faster": "Object Detection",
    "fastrcnn": "Object Detection",
    "maskrcnn": "Object Detection",
    "yolo": "Object Detection",
    "deeplab": "Image Segmentaion"
}


def setup_args():
    """Parse command line options (mode and config)."""
    parser = argparse.ArgumentParser(description="Build CFTarget.")
    help_s = "API route or model file location where Counterfit will collect outputs."
    parser.add_argument("--endpoint", help=help_s, required=True, type=str)
    help_s, choices = "The type of data the target model uses.", ["tabular", "text", "images"]
    parser.add_argument("--data-type", help=help_s, choices=choices, default="images", type=str)
    # help_s = "This is used to uniquely identify a target model within Counterfit."
    # parser.add_argument("--target-name", help=help_s, required=True, type=str)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def get_model_type(arch_map, model_name):
    pass
    


# class BaseTargetForImageDataType(CFTarget):
#     target_data_type = "image"
#     target_name = "torchserve-imagenet-classifer"
#     target_endpoint = "http://{}:{}/predictions/{}".format(
#         _DISCOVERED_IP,
#         _DISCOVERED_PORT,
#         _MODEL
#     )
    
#     # self.image_file_path 
#     def load(self):
#         # FIXME 
#         with open(self.image_file_path) as f:
#             catmap = json.load(f)

#         self.catmap = catmap
#         self.target_output_classes = len(catmap)

#     def predict(self, x):
#         for xx in x:
#             img = Image.fromarray(xx)

#             tmp = BytesIO()
#             img.save(tmp, format="PNG")
#             bytes = tmp.getvalue()

#             result = requests.post(self.target_endpoint, files={"data": bytes}).json()

#             scores = np.zeros((self.target_output_classes,))
#             for cat, score in result.items():
#                 scores[self.catmap[cat]] = score
                
#             return scores.tolist()
def main():
    args = setup_args()
    # TODO(afennelly) error checks for correct usage, ie handle bad endpoint
    # NOTE: below will break for Windows OS
    path_list = args.endpoint.split('/')
    # fetch model name and sloppily handle case of the version being specified (/predictions/{model_name}/{version})
    model_name = ''
    if path_list[-2] == 'predictions':
        model_name = path_list[-1]
    elif path_list [-3] == 'predictions':
        model_name = path_list[2]

    model_type = ""
    for name, type in MODEL_ARCHITECTURES_MAP.items():
        # choose first element; no intuition behind this, just choosing convention
        if model_name and name in model_name:
            model_type = type
            break
    
    if model_name:
        print(model_name)
        print(model_type)
        model_type = get_model_type(arch_map=MODEL_ARCHITECTURES_MAP, model_name=model_name)


if __name__ == "__main__":
    main()