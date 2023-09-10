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
RUN setfacl --modify user:vizsciflow:rw /var/run/docker.sock

WORKDIR /home/vizsciflow
COPY ./src ./src
COPY .env .


RUN mkdir -p /home/venvs/.venv
RUN chown -R vizsciflow:vizsciflow /home/venvs
RUN chown -R vizsciflow:vizsciflow /home/vizsciflow

USER vizsciflow

RUN curl https://pyenv.run | bash
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init --path)"\nfi' >> ~/.bashrc
RUN exec $SHELL

RUN python -m venv /home/venvs/.venv
RUN /home/venvs/.venv/bin/pip install --upgrade pip
RUN /home/venvs/.venv/bin/pip install -r ./src/requirements/requirements.txt


# to debug celery in docker
#RUN /home/vizsciflow/venvs/.venv/bin/pip install debugpy -t /tmp

ENV FLASK_APP manage.py
ENV FLASK_CONFIG production

WORKDIR /home/vizsciflow/src