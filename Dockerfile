FROM python:slim

RUN useradd vizsciflow

#RUN git clone https://mainulhossain:!Lisfa_2005!@github.com/srlabUsask/vizsciflow.git
WORKDIR /home/vizsciflow
COPY . .
#RUN apt-get install -y postgresql
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/requirements.txt
RUN venv/bin/pip install -i https://test.pypi.org/simple/ wfdsl 

RUN venv/bin/pip install gunicorn

RUN chmod +x boot.sh

ENV FLASK_APP manage.py

RUN chown -R vizsciflow:vizsciflow ./
USER vizsciflow

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
#RUN . venv/bin/activate
#RUN exec gunicorn -b :5000 --access-logfile - --error-logfile - -w 4 manage:app
