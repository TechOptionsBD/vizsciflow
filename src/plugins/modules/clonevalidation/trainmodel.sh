#!/bin/bash
docker exec annclonevalidation bash -c "source /home/venvs/.venvpy2/bin/activate && python expWith.py $1 $2"