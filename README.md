# PySonar

> Decentralized Machine Learning Client

[![Chat on Slack](https://img.shields.io/badge/chat-on%20slack-7A5979.svg)](https://openmined.slack.com/messages/team_pysonar)
[![Build Status](https://travis-ci.org/OpenMined/PySonar.svg?branch=master)](https://travis-ci.org/OpenMined/PySonar)

<!-- TOC depthFrom:2 -->

- [Setup](#setup)
    - [Using Docker](#using-docker)
- [Usage](#usage)
    - [Bootstrap environment](#bootstrap-environment)
    - [Start](#start)
    - [Know issues](#know-issues)
- [License](#license)

<!-- /TOC -->

Sonar is a smart contract library that allows data scientists to publish new _models_ they want to get trained into the _ModelRepository_ and people to pick models they can train on their personal data.

You can find a working proof of concept in the [notebooks](./notebooks) directory.

## Setup

### Using Docker

Using [Docker](https://www.docker.com) is the easiest way to get this running.

1. Run `docker-compose up`. This will launch IPFS, the in-memory fake ethereum blockchain with the smart contract, [OpenMined mine.js](https://github.com/OpenMined/mine.js) and the jupyter notebooks
2. Open the the Jupyter notebooks on [http://localhost:8888](http://localhost:8888)
3. Step through the notebook and check the output of the previous `docker-compose up` to get some infos on what happens

## Usage

### Bootstrap environment

Before running the demo there are a couple of prerequisites you need to install.

#### Base libraries

Before installing the python packages you need to make sure your system holds a set of basic math libraries required for the encryption operations (`phe` lib)

* [mpc](http://www.multiprecision.org/index.php?prog=mpc): arithmetic of complex numbers with arbitrarily high precision and correct rounding of the result
* [mpfr](http://www.mpfr.org/): multiple-precision floating-point computations
* [gmp](https://gmplib.org/): GNU multiple precision arithmetic library

For MacOS with brew just run:

```sh
brew install libmpc mpfr gmp
```

#### Solidity

The solidity tools are required to compile the contract of our demo.
See [installing solidity](http://solidity.readthedocs.io/en/develop/installing-solidity.html) for instructions for your platform.

#### IPFS

As the network itself is too big to actually host it on the blockchain you need `IPFS` to host the files.
For installation see the [ipfs installation page](https://dist.ipfs.io/#go-ipfs) or run:

```sh
brew install ipfs
```

After installation is complete run `ipfs init` to initialize your local IPFS system.

#### PIP packages

Make sure you have a clean python3 install and continue with installing all the packages

```sh
pip install -r requirements.txt
```

#### PIP package maintenance

PySonar utilizes pip-tools to help with maintaining PIP packages
(https://github.com/jazzband/pip-tools)

To update all packages, periodically re-run
```
pip-compile --upgrade
```

#### Build local libraries

First you need to get `sonar` package bundled up

```sh
python setup.py install
```

Then make sure you also have the [`syft`](https://github.com/OpenMined/syft) package properly installed. Head over to the repository and follow its instructions.

#### Import Smart Contract ABI

The interface for our `Sonar` smart contract is distributed via an npm package. You can import the `ModelRepository.abi` file to your local environment by running

```sh
make import-abi
```

which will place the file at `abis/ModelRepository.abi`.

### Start

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

### Known issues

* there have been reports of the `brew` installation of solidity not working properly

If you experience any problems while running this demo please create a [github issue](https://github.com/OpenMined/sonar/issues) and help us get better.

## License

[Apache-2.0](https://github.com/OpenMined/PySonar/blob/master/LICENSE) by OpenMined contributors
