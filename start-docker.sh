#!/bin/bash
echo "Starting service..."

export TECH=zbackup_zip
export FILENAME=GUIDE_Test.csv
export ROUND=1


while [ $ROUND -le 2 ]
do
    make up
    ROUND=`expr $ROUND + 1`
done
