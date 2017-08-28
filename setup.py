import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="sonar",
    version="0.1.0",
    author="Amber Trask",
    author_email="contact@openmined.org",
    description=("A server library (inc. Smart Contracts)"
                 " for Federated Deep Learning over the Ethereum Blockchain"),
    license="Apache-2.0",
    keywords="deep learning machine artificial intelligence"
             " homomorphic encryption",
    packages=['sonar'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Alpha",
    ],
    tests_require=['pytest', 'pytest-flake8']
)
