FROM python:3.10

# RUN apt-get update
# RUN apt-get install -y python
# RUN apt-get install -y python3.10

# RUN apt-get -y install python3.10-pip

COPY ./ .

RUN python3.10 -m venv venv

RUN . /venv/bin/activate && pip3 install -r /requirements.txt