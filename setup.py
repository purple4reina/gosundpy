import codecs
import os.path

from setuptools import find_packages, setup

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('version'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="gosundpy",
    version=get_version("gosundpy/version.py"),
    url="https://github.com/purple4reina/gosundpy",
    author="Rey Abolofia",
    author_email="purple4reina@gmail.com",
    keywords="gosund,smartlife,tuya,iot,api,sdk,python",
    description="Python API for controling Gosund smart devices",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="MIT",
    project_urls={
        "Source": "https://github.com/purple4reina/gosundpy",
        "Bug Tracker": "https://github.com/purple4reina/gosundpy/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    install_requires=["tuya-iot-py-sdk==0.6.6"],
    packages=find_packages(),
    python_requires=">=3.7, <4",
)
