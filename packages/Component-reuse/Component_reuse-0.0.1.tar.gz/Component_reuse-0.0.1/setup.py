from os import path

from setuptools import find_packages
from setuptools import setup

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Component_reuse",
    version="0.0.1",
    author="ORION",
    author_email="orion@liferaftinc.com",
    packages=find_packages(),
    install_requires=[
        "pika",
    ],
    description="Component_reuse",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
