FROM python:3.10-bullseye
SHELL ["/bin/bash", "-c"]
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
        python \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt-get update \
  && apt-get install -y --no-install-recommends  \
  acl \
  sudo \
  docker-ce-cli

ARG UID
ARG HOME="/home/vizsciflow"
RUN mkdir -p $HOME
RUN useradd -u ${UID} vizsciflow

RUN echo "vizsciflow:vizsciflow" | chpasswd && adduser vizsciflow sudo
RUN groupadd docker
RUN usermod -aG docker vizsciflow
#RUN echo "vizsciflow" | setfacl --modify user:vizsciflow:rw /var/run/docker.sock
#RUN setfacl --modify user:vizsciflow:rw /var/run/docker.sock

WORKDIR $HOME
COPY ./src ./src
COPY .env .

RUN mkdir -p /home/venvs/.venv
RUN python -m venv /home/venvs/.venv
RUN /home/venvs/.venv/bin/pip install -r ./src/requirements/requirements.txt
RUN chown -R vizsciflow:vizsciflow /home/venvs
RUN chown -R vizsciflow:vizsciflow $HOME

# to debug celery in docker
#RUN $HOME/venvs/.venv/bin/pip install debugpy -t /tmp

ENV FLASK_APP manage.py
ENV FLASK_CONFIG production

USER vizsciflow
WORKDIR $HOME/src