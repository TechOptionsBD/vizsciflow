#!/bin/bash
sum=0
while [ -n "$1" ]; do
    sum=`expr $sum + $1`
    shift
done
echo $sum