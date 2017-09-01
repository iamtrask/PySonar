# PySonar

> Federated Deep Learning Client via Sonar Smart Contract on the Ethereum Blockchain

[![Build Status](https://travis-ci.org/OpenMined/PySonar.svg?branch=master)](https://travis-ci.org/OpenMined/PySonar)

<!-- TOC depthFrom:2 -->

- [installation](#installation)
    - [base libraries](#base-libraries)
    - [solidity](#solidity)
    - [ipfs](#ipfs)
    - [pip packages](#pip-packages)
    - [build local libraries](#build-local-libraries)
- [usage](#usage)
- [known issues](#known-issues)

<!-- /TOC -->

Sonar is a smart contract library that allows data scientists to publish new _models_ they want to get trained into the _ModelRepository_ and people to pick models they can train on their personal data.

You can find a working proof of concept in the [notebooks](./notebooks) directory.

## Running with Docker

Using Docker is the easiest way to get this running.

1. Install Docker from https://www.docker.com/
    - For macOS users with [Homebrew](https://brew.sh/) installed, use `brew cask install docker`
2. Run `docker-compose up`
3. Look for the Jupyter notebook URL, it should look like `http://0.0.0.0:8888/?token=<long token here>` - open that URL in your web browser
4. When running the notebooks, search the verbose output of the `docker-compose up` command for the `eth_getCode` -> `ModelRepository` address and copy into the last line of the cell under "Setting up the Experiment" as explained in the "ATTENTION" comment 🙂
5. Step through the notebook

## installation

Before running the demo there are a couple of prerequisites you need to install.

### base libraries

Before installing the python packages you need to make sure your system holds a set of basic math libraries required for the encryption operations (`phe` lib):

* [mpc](https://www.musicpd.org/clients/mpc/): Command-line music player client for mpd
* [mpfr](http://www.mpfr.org/): multiple-precision floating-point computations
* [gmp](https://gmplib.org/): GNU multiple precision arithmetic library

For MacOS with brew just run:

```sh
brew install libmpc mpfr gmp
```

### solidity

The solidity tools are required to compile the contract of our demo.
See [installing solidity](http://solidity.readthedocs.io/en/develop/installing-solidity.html) for instructions for your platform.

### ipfs

As the network itself is too big to actually host it on the blockchain you need `IPFS` to host the files.
For installation see the [ipfs installation page](https://dist.ipfs.io/#go-ipfs) or run

```sh
brew install ipfs
```

After installation is complete run `ipfs init` to initialize your local IPFS system.

### pip packages

Make sure you have a clean python3 install and continue with installing all the packages

```sh
pip install -r requirements.txt
```

### build local libraries

First you need to get `sonar` package bundled up

```sh
python setup.py install
```

Then make sure you also have the [`syft`](https://github.com/OpenMined/syft) package properly installed. Head over to the repository and follow its instructions.

## usage

After you made sure all the installation steps are done you need to set up your local mock environment.

```sh
# start the ipfs daemon in the background
ipfs daemon&
# run local ethereum mock
testrpc -a 1000
```

Now open a second shell, start the notebook and follow its instructions

```sh
jupyter notebook notebooks
```

## known issues

* there have been reports of the `brew` installation of solidity not working properly

If you experience any problems while running this demo please create a [github issue](https://github.com/OpenMined/sonar/issues) and help us get better.
