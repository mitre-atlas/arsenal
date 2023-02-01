import json
import requests
import numpy as np
from io import BytesIO
from PIL import Image

from counterfit.core.targets import CFTarget


# use the ip fact source here
_DISCOVERED_IP = "172.22.0.5"
# use the http-proxy port fact source here
_DISCOVERED_PORT = "8080"
# use the user-selected model here
_MODEL = "resnet-18"

class TorchServeImageNetClassifier(CFTarget):
    target_data_type = "image"
    target_name = "torchserve-imagenet-classifer"
    target_endpoint = "http://{}:{}/predictions/{}".format(
        _DISCOVERED_IP,
        _DISCOVERED_PORT,
        _MODEL
    )

    def load(self):
        with open("/home/afennelly/arsenal/data/payloads/cfit/imagenet-catmap.json", "r") as f:
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