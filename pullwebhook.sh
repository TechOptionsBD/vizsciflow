#!/bin/bash

TARGET=$1
GIT_DIR=$2
BRANCH=$3

git --work-tree=$TARGET --git-dir=$GIT_DIR checkout -f $BRANCH
#git --work-tree=$TARGET --git-dir=$GIT_DIR pull

# restart the web service; you may need to restart nginx.
# for vizsciflow, supervisor does it.
echo sr-hadoop | sudo -S supervisorctl restart all