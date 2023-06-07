from typing import List, Union
import argparse
import sys
import os
import json
import requests

# FIXME: Added to 
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import numpy as np
from io import BytesIO
from PIL import Image

try:
    from counterfit.core.targets import CFTarget
    from counterfit.core import Counterfit
    from counterfit.core.output import CFPrint
except ImportError as e:
    import pip

    pip.main(['install', '--user', 'counterfit[dev] @ git+https://github.com/Azure/counterfit.git@main'])

    from counterfit.core.targets import CFTarget
    from counterfit.core import Counterfit
    from counterfit.core.output import CFPrint


# Map (common) DL model architecture to (typical) task "type"
MODEL_ARCHITECTURES_MAP = {
    "alexnet": "Image Classification",
    "densenet161": "Image Classification",
    "resnet": "Image Classification",
    "resnet-18": "Image Classification",
    "resnet-50": "Image Classification",
    "resnet-101": "Image Classification",
    "resnet-152-batch_v2": "Image Classification",
    "vgg16": "Image Classification",
    "vgg19": "Image Classification",
    "mobilenet": "Image Classification",
    "squeezenet1_1": "Image Classification",
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


def get_output_classes(model_type: str) -> List[str]:
    dataset = DEFAULT_DATASET_MAP[model_type]
    if dataset == "ImageNet":
        labels_map = json.load(open("imagenet_name_to_index.json"))
        output_labels = list(labels_map.keys())
        # print(output_labels[:5])
        return output_labels
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    

class TorchServeImageNetClassifier(CFTarget):
    data_type = "image"
    target_name = "torchserve_imagenet_classifier"
    task = "classification"
    class_map = json.load(open("imagenet_name_to_index.json"))
    output_classes = list(class_map.keys())
    endpoint = ""
    input_shape = (720, 720, 3)
    output_classes = get_output_classes("Image Classification")
    sample_input_path = "kitten.jpg"
    classifier = "closed-box"
    X = [] # X will be array of ndarrays, not just a single array (very nonintuitive)

    def load(self):
        input_path = self.fullpath(self.sample_input_path)
        self.X.append(np.asarray(Image.open(input_path)).astype(np.float32))
        # FIXME there are only 998 output classes, not 1000
        self.num_output_classes = len(self.output_classes)

    def predict(self, x_batch):
        # check if x_batch is a single image or a batch of images
        if len(x_batch.shape) == 4:
            x = x_batch[0]
        else:
            x = x_batch

        # prepare input image to be sent to endpoint
        img = Image.fromarray((x * 255).astype(np.uint8))
        tmp = BytesIO()
        img.save(tmp, format="PNG")
        bytes = tmp.getvalue()
        
        # send image to endpoint and get response
        result = requests.post(self.endpoint, files={"data": bytes}).json()
        scores = np.zeros((self.num_output_classes,))
        for cat, score in result.items():
            scores[self.class_map[cat]] = score

        return scores.tolist()


def get_model_name_from_endpoint(endpoint):
    # retrieve "model name" from passed in args.endpoint
    pred_path_list = endpoint.split('/')
    if pred_path_list[-2] == "predictions":
        # args.endpoint == "<binding_addr>/predictions/{model_name}"
        return pred_path_list[-1]
    elif pred_path_list[-3] == "predictions":
        # args.endpoint == "<binding_addr>/predictions/{model_name}/{version}"
        return pred_path_list[2]


def get_model_type_from_model_name(model_name):
    print(model_name)
    for name, task_type in MODEL_ARCHITECTURES_MAP.items():
        # choose first element (by convention; no intuition behind this convention)
        if name in model_name:
            return task_type
    return ""


def image_classification(attack_list, endpoint, model_name):
    kwargs = {"target_name": model_name,"endpoint": endpoint}
    ts_target = TorchServeImageNetClassifier(**kwargs)
    ts_target.load()
    for attack in attack_list:
        try:
            print(f"Building attack: {attack}...")
            cf_attack = Counterfit.build_attack(ts_target, attack)
            # set num_iter to 60% of default value to speed up attack
            if attack == "boundary":
                cf_attack.options.attack_parameters["max_iter"]["current"] = 2000
            elif attack == "hop_skip_jump":
                cf_attack.options.attack_parameters["max_iter"]["current"] = 5
            print(f"Running attack on the {ts_target.target_name} CFTarget...")
            Counterfit.run_attack(cf_attack)
            print(f"Initial labels: {cf_attack.initial_labels}")
            print(f"Final labels: {cf_attack.final_labels}")
        except Exception as error:
            CFPrint.failed(f"Failed to run attack {attack} with error: {error}")


def setup_args():
    # TODO below will get ALL art attacks, not just black-box; so don't use it yet...
    default_art_attacks = list(Counterfit.get_frameworks()["art"]["attacks"].keys())
    default_attacks_to_run = ["hop_skip_jump"]
    # TODO make choices list "complete"
    # choices = ["boundary", "copycat_cnn", "functionally_equivalent_extraction", "hop_skip_jump", "knockoff_nets"] 

    parser = argparse.ArgumentParser(description="Build CFTarget.")

    parser.add_argument("--endpoint", help="API route or model file location where Counterfit will collect outputs.", required=True, type=str)
    parser.add_argument("--attacks", help="The type of attack (s) to run.", nargs='*', metavar="List of attacks", default=default_attacks_to_run)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return args


def main():
    args = setup_args()
    # TODO(afennelly) error checks for correct usage, ie handle bad endpoint
    # NOTE: below will break for Windows OS
    pred_endpoint = f"http://{args.endpoint}"

    model_name = get_model_name_from_endpoint(pred_endpoint)
    model_type = get_model_type_from_model_name(model_name)

    # check if the model architecture "type" has been set
    if model_type == "Image Classification":
        image_classification(
            attack_list=args.attacks,
            endpoint=pred_endpoint,
            model_name=model_name
        )


if __name__ == "__main__":
    main()
