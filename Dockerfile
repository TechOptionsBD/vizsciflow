FROM python:slim

RUN useradd vizsciflow

#RUN git clone https://mainulhossain:!Lisfa_2005!@github.com/srlabUsask/vizsciflow.git
WORKDIR /home/vizsciflow
COPY . .

RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements/requirements.txt
RUN venv/bin/pip install -i https://test.pypi.org/simple/ wfdsl 

RUN venv/bin/pip install gunicorn

RUN chmod +x boot.sh

ENV FLASK_APP manage.py

RUN chown -R vizsciflow:vizsciflow ./
USER vizsciflow

EXPOSE 5000
#ENTRYPOINT ["./boot.sh"]
