from typing import List, Union
import argparse
import sys
import os
import json
import requests

# FIXME remove when we don't have threading errors
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np
from io import BytesIO
from PIL import Image

from counterfit.core.targets import CFTarget
from counterfit.core import Counterfit
from counterfit.core.output import CFPrint

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
    help_s = "The type of attack (s) to run."
    # TODO below will get ALL art attacks, not just black-box; so don't use it yet...
    default_art_attacks = list(Counterfit.get_frameworks()["art"]["attacks"].keys())
    default_attacks_to_run = ["hop_skip_jump"] # ["hop_skip_jump", "boundary"]
    # TODO make choices list "complete"
    # choices = ["boundary", "copycat_cnn", "functionally_equivalent_extraction", "hop_skip_jump", "knockoff_nets"] 
    parser.add_argument("--attacks", help=help_s, nargs='*', metavar="List of attacks", default=default_attacks_to_run)
    # parser.add_argument("--data-type", help=help_s, choices=choices, default="image", type=str)
    # help_s = "This is used to uniquely identify a target model within Counterfit."
    # parser.add_argument("--target-name", help=help_s, required=True, type=str)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


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
    # X = np.zeros(input_shape)
    X = [] # X will be array of ndarrays, not just a single array (very nonintuitive)

    def load(self):
        input_path = self.fullpath(self.sample_input_path)
        # print(input_path)
        # print(os.path.exists(input_path))
        # sample_input = Image.open(input_path)
        # print(sample_input)
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
        # print(result)
        scores = np.zeros((self.num_output_classes,))
        for cat, score in result.items():
            # if cat == "tabby":
            #     print(score)
            #     print(self.class_map[cat])
            scores[self.class_map[cat]] = score

        return scores.tolist()
        

def main():
    # TODO(afennelly) refactor the sub tasks below to separate methods
    args = setup_args()
    attacks_list = args.attacks
    # TODO(afennelly) error checks for correct usage, ie handle bad endpoint
    # NOTE: below will break for Windows OS
    pred_endpoint = f"http://{args.endpoint}"
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
        for name, task_type in MODEL_ARCHITECTURES_MAP.items():
            # choose first element (by convention; no intuition behind this convention)
            if name in model_name:
                model_type = task_type
                break
    
    # check if the model architecture "type" has been set
    if model_type == "Image Classification":
        kwargs = {"target_name": model_name,"endpoint": pred_endpoint}
        ts_target = TorchServeImageNetClassifier(**kwargs)
        ts_target.load()
        for attack in attacks_list:
            try:
                print(f"Building attack: {attack}...")
                cf_attack = Counterfit.build_attack(ts_target, attack)
                # set num_iter to 60% of default value to speed up attack
                if attack == "boundary":
                    cf_attack.options.attack_parameters["max_iter"]["current"] = 2000
                elif attack == "hop_skip_jump":
                    cf_attack.options.attack_parameters["max_iter"]["current"] = 5
                # print(cf_attack.options.attack_parameters["max_iter"]["current"])
                # print(cf_attack.options.attack_parameters)
                print(f"Running attack on the {ts_target.target_name} CFTarget...")
                results = Counterfit.run_attack(cf_attack)
                print(f"Initial labels: {cf_attack.initial_labels}")
                print(f"Final labels: {cf_attack.final_labels}")
                # print(f"Run summary:")
                # print(cf_attack.run_summary)
            except Exception as error:
                CFPrint.failed(f"Failed to run attack {attack} with error: {error}")

        # input = target.X
        # print(type(input))
        # print(input.shape)
        # scores = target.predict(input)
        # print(scores)
        
        # TODO: provide `load` and `predict` functions, depending on whether `model_type`
        # is "Image Classification", "Object Detection", or "Image Segmentation".
        # load, predict = get_load_and_predict_functions(model_type)
        # TODO: output_classes should be wrt the desired dataset, ie ImageNet, COCO, etc.
        # output_classes = get_output_classes(model_type)
        # # NOTE: If we were actually able to exfiltrate the model, we could potentially 
        # # set `classifier` below to "open_box"; assumption holds for now.
        # target = Counterfit.build_target(
        #     data_type="image", 
        #     endpoint=pred_endpoint,
        #     output_classes=output_classes, # FIXME
        #     classifier="closed_box", 
        #     input_shape=(3, 720, 720), # FIXME not sure if this value matters 
        #     load_func=load, # FIXME
        #     predict_func=predict, # FIXME
        #     X=[], # FIXME
        # )

        # print(model_name)
        # print(model_type)
        # model_type = get_model_type(arch_map=MODEL_ARCHITECTURES_MAP, model_name=model_name)


if __name__ == "__main__":
    main()


# cf attacks for image, closed-box, art:
# ["boundary", "copycat_cnn", "functionally_equivalent_extraction", "hop_skip_jump", "knockoff_nets"]
