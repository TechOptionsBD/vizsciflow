#!/bin/bash
source "/home/mainul/miniconda3/bin/activate" "/home/mainul/miniconda3/envs/qiime2-2018.11"
#calling the required tools here... such as 
"/home/mainul/miniconda3/envs/qiime2-2018.11/bin/qiime tools view" $1
"/home/mainul/miniconda3/bin/deactivate"

