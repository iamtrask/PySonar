# This Dockerfile uses Docker Multi-Stage Builds
# See https://docs.docker.com/engine/userguide/eng-image/multistage-build/

### Base Image
# Setup up a base image to use in build and runtime images
FROM openmined/pysyft:hydrogen AS base

EXPOSE 8888
CMD ["jupyter", "notebook", "--config=./jupyter_notebook_config.py", "--allow-root"]

# Intermediate build container
FROM base AS build
WORKDIR /pysonar

# Install build OS packages
RUN apk add --no-cache \
            python3 \
            python3-dev \
            alpine-sdk \
            nodejs \
            nodejs-npm \
            git \
            linux-headers \
            lapack-dev \
            gfortran \
            gmp-dev \
            gmp-dev \
            mpfr-dev \
            mpc1-dev

#Pysonar image
FROM build AS pysonar

# Setup workdir and copy requirements file
COPY requirements.txt /pysonar

# Install python packages
RUN ["pip3", "install", "numpy", "scipy"]
RUN ["pip3", "install", "-r", "/pysonar/requirements.txt"]

# install pySonar lib
COPY . /pysonar
RUN ["python3", "setup.py", "install"]

# import abi via NPM module
RUN ["make", "import-abi"]

# Runtime image
FROM base AS runtime
WORKDIR /notebooks

RUN ["pip3", "install", "jupyter", "notebook"]
COPY notebooks /notebooks
COPY jupyter_notebook_config.py /notebooks/

# Copy artifacts from pysonar image
COPY --from=pysonar /pysonar/ /pysonar/
