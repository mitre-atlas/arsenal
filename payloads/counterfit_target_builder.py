import argparse
import sys
import os
import json
import requests

import numpy as np
from io import BytesIO
from PIL import Image

from counterfit.core.targets import CFTarget
from counterfit.core import Counterfit

# Map (common) DL model architecture to (typical) task "type"
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
    "deeplab": "Image Segmentation"
}

# Map (common) DL task to (typical) benchmark dataset
DEFAULT_DATASET_MAP = {
    "Image Classification": "ImageNet",
    "Object Detection": "COCO", 
    "Image Segmentation": "COCO"
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


class BaseTargetForImageDataType(CFTarget):
    target_data_type = "image"
    target_name = "" # "torchserve-imagenet-classifer"
    target_endpoint = ""
    
    def load(self):
        # FIXME 
        with open(self.image_file_path) as f:
            catmap = json.load(f)

        self.catmap = catmap
        self.target_output_classes = len(catmap)

    def predict(self, x):
        for xx in x:
            img = Image.fromarray(xx)

            tmp = BytesIO()
            img.save(tmp, format="PNG")
            bytes = tmp.getvalue()

            result = requests.post(self.target_endpoint, files={"data": bytes}).json()

            scores = np.zeros((self.target_output_classes,))
            for cat, score in result.items():
                scores[self.catmap[cat]] = score
                
            return scores.tolist()
        

def main():
    # TODO(afennelly) refactor the sub tasks below to separate methods
    args = setup_args()
    # TODO(afennelly) error checks for correct usage, ie handle bad endpoint
    # NOTE: below will break for Windows OS
    pred_endpoint = args.endpoint
    pred_path_list = pred_endpoint.split('/')

    # retrieve "model name" from passed in args.endpoint
    model_name = ""
    # NOTE: below is (sloppily) handling case where model version is specified
    if pred_path_list[-2] == "predictions":
        # args.endpoint == "<binding_addr>/predictions/{model_name}"
        model_name = pred_path_list[-1]
    elif pred_path_list[-3] == "predictions":
        # args.endpoint == "<binding_addr>/predictions/{model_name}/{version}"
        model_name = pred_path_list[2]

    # (attempt) to retrieve the model architecture "type" ("intended task")
    model_type = ""
    if model_name:
        for name, type in MODEL_ARCHITECTURES_MAP.items():
            # choose first element (by convention; no intuition behind this convention)
            if name in model_name:
                model_type = type
                break
    
    # check if the model architecture "type" has been set
    if model_type:
        target = Counterfit.build_target(
            data_type="image", 
            endpoint=pred_endpoint,
            output_classes=[],
        )
        print(model_name)
        print(model_type)
        model_type = get_model_type(arch_map=MODEL_ARCHITECTURES_MAP, model_name=model_name)


if __name__ == "__main__":
    main()