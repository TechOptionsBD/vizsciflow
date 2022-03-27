FROM python:3.8-buster

ARG UID
RUN mkdir -p /home/vizsciflow
RUN useradd -u ${UID} vizsciflow 

RUN apt-get update \
 && apt-get install -y --no-install-recommends  \
        build-essential \
        debhelper \
        devscripts \
        gcc \
        gettext \
        libffi-dev \
        libjpeg-dev \
        libmemcached-dev \
        libpq-dev \
        libxml2 \
        libxml2-dev \
        libxslt1-dev \
        memcached \
        netcat \
        python3-dev \
        python3-gdal \
        python3-ldap \
        python3-lxml \
        python3-pil \
        python3-pip \
        python3-psycopg2 \
        zip \
        zlib1g-dev \
        default-jre \
        default-jdk \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /home/vizsciflow
COPY ./src .
COPY .env .
COPY ./.vscode ./.vscode

RUN python -m venv .venv
RUN .venv/bin/pip install --upgrade pip
RUN .venv/bin/pip install -r requirements/requirements.txt
RUN .venv/bin/pip install -i https://test.pypi.org/simple/ wfdsl 

RUN .venv/bin/pip install gunicorn
RUN .venv/bin/pip install pysam

# to debug celery in docker
#RUN .venv/bin/pip install debugpy -t /tmp

ENV FLASK_APP manage.py
ENV FLASK_CONFIG development

RUN chown -R vizsciflow:vizsciflow ./

USER vizsciflow