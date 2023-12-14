#!/bin/sh

name=$1
model=$2

if [ "$name" = "MultiWoz" ]; then
    python3 testAPI_MultiWoz.py $model
elif [ "$name" = "SGD" ]; then
    python3 testAPI_SGD.py $model
elif [ "$name" = "DSTC" ]; then
    python3 testAPI_alexa.py $model
else
    echo "The dataset name is wrong"
fi