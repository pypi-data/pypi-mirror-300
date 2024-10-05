from setuptools import setup, find_packages

with open("README.md", "r" ) as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "image_procession",
    version = "0.0.2",
    author = "Alex",
    description = "Image Processing Package using Skimage",
    long_description = page_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/lexsouza83/image-processing-package.git",
    packages = find_packages(),
    install_requires = requirements,
    python_requires = '>=3.5'
)