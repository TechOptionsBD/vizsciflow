#!/bin/bash
SETUP_SCRIPT="./setup.sh"

git clone https://$1:$2@github.com/srlabUsask/vizsciflow.git
cd vizsciflow

bash "$SETUP_SCRIPT" 
