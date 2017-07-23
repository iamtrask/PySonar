# sonar
Federated Deep Learning via Ethereum Blockchain

## installation

### prerequisites

Before installing the python packages you need to make sure your system holds a set of basic math libraries required for the encryption operations:

* [mpc](https://www.musicpd.org/clients/mpc/): Command-line music player client for mpd
* mpfr: multiple-precision floating-point computations
* gmp: GNU multiple precision arithmetic library

For MacOS

```sh
brew install libmpc mpfr gmp
```

For Linux

```

```

### pip packages

Make sure you have a clean python3 install and continue with installing all the packages

```sh
pip install -r requirements.txt
```

### create packages

Create local packages

```sh
python setup.py install
```

You should now be able to start the demo with `jupyter notebook` and go through the instructions.
