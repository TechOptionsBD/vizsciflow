#!/bin/bash

# Change to the subdirectory 'src' within the home directory
cd /home/vizsciflow/src

echo vizsciflow | sudo -S service postgresql start
/home/vizsciflow/wait_for_pg_ready.sh
/home/venvs/.venv/bin/gunicorn -b :8000 --access-logfile - --error-logfile - manage:app --timeout=300 --workers=8 --worker-connections=1000 --log-level=debug --timeout=300 --reload --threads=4
#/home/venvs/.venv/bin/gunicorn --worker-class eventlet -b :8000 --workers=1 --access-logfile - --error-logfile - manage:app --timeout=300  --worker-connections=1000 --log-level=debug --timeout=300 --reload
