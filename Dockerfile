FROM python:3.10-bullseye

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
RUN echo "vizsciflow:vizsciflow" | chpasswd && adduser vizsciflow sudo
RUN groupadd docker
RUN usermod -aG docker vizsciflow
#RUN echo "vizsciflow" | setfacl --modify user:vizsciflow:rw /var/run/docker.sock

# separate venv for python 2.7
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output /home/get-pip.py
RUN python2 /home/get-pip.py

WORKDIR /home/vizsciflow
COPY ./src ./src
COPY .env .


RUN mkdir -p /home/venvs/.venv
RUN chown -R vizsciflow:vizsciflow /home/venvs
RUN chown -R vizsciflow:vizsciflow /home/vizsciflow

USER vizsciflow
RUN python -m venv /home/venvs/.venv
RUN /home/venvs/.venv/bin/pip install --upgrade pip
RUN /home/venvs/.venv/bin/pip install -r ./src/requirements/requirements.txt
RUN /home/venvs/.venv/bin/pip install wfdsl

# separate venv for pycoQC
RUN python -m venv /home/venvs/.venvpycoqc
RUN /home/venvs/.venvpycoqc/bin/pip install --upgrade pip
RUN /home/venvs/.venvpycoqc/bin/pip install pycoQC

RUN python2 -m pip install virtualenv
RUN python2 -m virtualenv /home/venvs/.venvpy2
RUN /home/venvs/.venvpy2/bin/pip install --upgrade pip
RUN /home/venvs/.venvpy2/bin/pip install -r ./src/requirements/requirements2.txt

RUN /home/venvs/.venv/bin/pip install gunicorn
RUN /home/venvs/.venv/bin/pip install pysam

# to debug celery in docker
#RUN /home/vizsciflow/venvs/.venv/bin/pip install debugpy -t /tmp

ENV FLASK_APP manage.py
ENV FLASK_CONFIG development

# Give ownership to vizsciflow user
#RUN chown vizsciflow:vizsciflow ./src/plugins
#RUN chmod +rwx -R /home/vizsciflow/
#RUN chmod +rwx -R ../venvs

USER vizsciflow
WORKDIR /home/vizsciflow/src