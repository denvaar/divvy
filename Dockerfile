FROM python:3.5
ENV PYTHONUNBUFFERED 1
ENV DIVVY_ENV development_docker
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install --upgrade pip
RUN pip install -r server/misc/requirements.txt
