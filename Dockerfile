FROM python:3.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get install libpq-dev
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]
RUN pip install -r requirements.txt
COPY . /code/
