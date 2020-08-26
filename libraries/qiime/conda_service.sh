#!/bin/bash
source "/home/phenodoop/miniconda3/bin/activate" "/home/phenodoop/miniconda3/envs/qiime2-2018.11"
#calling the required tools here... such as
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
"/home/phenodoop/miniconda3/envs/qiime2-2018.11/bin/qiime" $1
"/home/phenodoop/miniconda3/bin/deactivate"