from torchserve import TorchServeImageNetClassifier
from skimage.io import imread

target = TorchServeImageNetClassifier()
target.load()

im=imread("3dogs.jpg")[None,...]
scores = target.predict(im)
print(scores)