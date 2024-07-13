# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create a directory for the code and set it as the working directory
RUN mkdir /code
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt /code/
RUN apt-get update \
    && apt-get install -y libpq-dev \
    && apt-get install -y vim \
    && pip install -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . /code/
