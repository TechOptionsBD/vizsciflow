#!/bin/bash
echo "source /home/venvs/.venvpy2/bin/activate && python validateClones.py $1 $2 $3 $4"
docker exec clonecognition bash -c "source /home/venvs/.venvpy2/bin/activate && python validateClones.py $1 $2 $3 $4"