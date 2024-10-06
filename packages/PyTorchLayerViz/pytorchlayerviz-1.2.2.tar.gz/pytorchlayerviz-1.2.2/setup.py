from setuptools import setup, find_packages

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

VERSION = '1.2.2'
DESCRIPTION = "PyTorchLayerViz is a Python library that allows you to visualize the weights and feature maps of a PyTorch model."

setup(
    name="PyTorchLayerViz",
    version=VERSION,
    author="Simone Panico",
    author_email="simone.panico@icloud.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['torch', 'torchvision', 'pillow', 'matplotlib'],
    keywords=['python', 'pytorch', 'deep learning', 'model'],
)