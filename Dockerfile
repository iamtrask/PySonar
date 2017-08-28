FROM alpine:edge
RUN ["apk", "add", "--no-cache", "python3", "python3-dev", "musl-dev", "linux-headers", "g++", "lapack-dev", "gfortran", "gmp-dev", "mpfr-dev", "mpc1-dev"]
RUN ["pip3", "install", "numpy"]
RUN ["pip3", "install", "scipy"]

RUN ["mkdir", "/pysonar"]
COPY requirements.txt /pysonar
RUN ["pip3", "install", "-r", "/pysonar/requirements.txt"]

COPY . /pysonar
WORKDIR /pysonar
RUN ["python3", "setup.py", "install"]
