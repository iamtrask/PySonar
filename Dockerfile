FROM openmined/pysonar:base
COPY requirements.txt /pysonar
RUN ["pip3", "install", "-r", "/pysonar/requirements.txt"]

COPY . /pysonar
WORKDIR /pysonar
RUN ["python3", "setup.py", "install"]
