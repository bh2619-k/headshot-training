# Include Python
FROM python:3.10.12-buster
FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel

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
RUN apt update && apt install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

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