#!/bin/bash

TARGET=$1
GIT_DIR=$2
BRANCH=$3

git --work-tree=$TARGET --git-dir=$GIT_DIR checkout -f $BRANCH

