FROM python:3.8-buster

RUN useradd vizsciflow
WORKDIR /home/vizsciflow
COPY . .

RUN python -m venv .venv
RUN .venv/bin/pip install --upgrade pip
RUN .venv/bin/pip install -r requirements/requirements.txt
RUN .venv/bin/pip install -i https://test.pypi.org/simple/ wfdsl 

RUN .venv/bin/pip install gunicorn
# to debug celery in docker
RUN .venv/bin/pip install debugpy -t /tmp

ENV FLASK_APP manage.py
ENV FLASK_CONFIG docker

RUN chown -R vizsciflow:vizsciflow ./

USER vizsciflow