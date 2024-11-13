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

# Using full path to Python in venv
RUN python -m venv venv

RUN /bin/bash -c "source venv/bin/activate && pip install -U poetry pip optimum-quanto runpod && poetry install --no-root"

# Install packages
# RUN pip install -U poetry pip

# RUN poetry install --no-root

# RUN pip install optimum-quanto runpod

# Ensure the script is executable
RUN chmod +x ./train.sh

# Call your file when your container starts
CMD [ "venv/bin/python", "./index.py" ]