#!/bin/bash
echo "Starting..."

round=1

while [ $round -lt 2 ]
do
    echo "round - $round"
    /usr/src/app/monitoramento.sh $round zip zip &

    echo `zip -v /usr/src/app/data/GUIDE_Test.zip /usr/src/app/data/GUIDE_Test.csv` > loggg.txt

    round=`expr $round + 1`
done


# monitoramento_zip_pid=$(pgrep monitoramento.zip.sh)  
# kill -TERM $monitoramento_zip_pid