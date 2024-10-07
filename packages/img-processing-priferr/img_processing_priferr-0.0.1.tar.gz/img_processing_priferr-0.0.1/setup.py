from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="img_processing_priferr",
    version="0.0.1",
    author="priferr",
    author_email="ipriferr@gmail.com",
    description="Study Image Processing Using Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/priferr/img_processing_pkg",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)
