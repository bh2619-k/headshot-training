FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

# Define your working directory
WORKDIR /

# Add your file
ADD . .

# Create folders
RUN mkdir datasets
RUN mkdir datasets/ohwx
RUN mkdir cache
RUN mkdir cache/vae
RUN mkdir cache/vae/ohwx
RUN mkdir cache/text
RUN mkdir cache/text/ohwx

# Install libgl1-mesa-glx
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y libgl1-mesa-glx

# Using full path to Python in venv
RUN python -m venv .venv

ENV PATH=".venv/bin:$PATH"

# Install packages
RUN pip install -U poetry pip

RUN poetry install --no-root

RUN pip install optimum-quanto runpod

# Ensure the script is executable
RUN chmod +x ./train.sh

# Call your file when your container starts
CMD [ "python", "./index.py" ]