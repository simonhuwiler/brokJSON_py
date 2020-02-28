import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="brokJSON",
    version="1.0.0",
    description="Convert GeoJSON to BrokJSON and vice versa",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.brokjson.dev",
    author="Simon Huwiler",
    author_email="webmaster@simonhuwiler.ch",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["brokjson"],
    include_package_data=True,
    install_requires=[]
)