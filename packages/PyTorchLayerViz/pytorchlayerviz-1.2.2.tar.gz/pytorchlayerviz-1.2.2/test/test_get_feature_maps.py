import unittest
import os
import matplotlib.pyplot as plt
from PIL import Image
import torch
from torch import nn
from torchvision import datasets, transforms, models
from torchvision.transforms import ToTensor
import numpy as np
from PyTorchLayerViz.main import get_feature_maps

pretrained_model = models.vgg16(pretrained=True)

# Dynamically set the path to the 'brain.tif' file and output images
input_image_path = os.path.join(os.path.dirname(__file__), 'brain.tif')
output_images_dir = os.path.join(os.path.dirname(__file__), 'output_images')

torch.manual_seed(42)

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

class TestGetFeatureMaps(unittest.TestCase):
    def test_maxPool(self):
        layers_to_check = [nn.MaxPool2d]
        numpyArr_from_function = get_feature_maps(model=pretrained_model, layers_to_check=layers_to_check, input_image_path=input_image_path)

        # Dynamically load the correct .npy file for testing
        numpyArr_from_file = np.load(os.path.join(output_images_dir, 'test_maxPool.npy'))

        np.testing.assert_array_equal(numpyArr_from_function, numpyArr_from_file)

    def test_moreLayers(self):
        layers_to_check = [nn.MaxPool2d, nn.Conv2d]
        numpyArr_from_function = get_feature_maps(model=pretrained_model, layers_to_check=layers_to_check, input_image_path=input_image_path)

        # Dynamically load the correct .npy file for testing
        numpyArr_from_file = np.load(os.path.join(output_images_dir, 'test_moreLayers.npy'))

        np.testing.assert_array_equal(numpyArr_from_function, numpyArr_from_file)

    def test_transform(self):
        layers_to_check = [nn.MaxPool2d, nn.Conv2d]
        numpyArr_from_function = get_feature_maps(model=pretrained_model, layers_to_check=layers_to_check, input_image_path=input_image_path, transform=transform)

        # Dynamically load the correct .npy file for testing
        numpyArr_from_file = np.load(os.path.join(output_images_dir, 'test_transform.npy'))

        np.testing.assert_array_equal(numpyArr_from_function, numpyArr_from_file)

if __name__ == '__main__':
    unittest.main()
