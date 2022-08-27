#!/bin/bash
docker exec annclonevalidation bash -c "source /home/.venvpy2/bin/activate && python expWith.py $1 $2"