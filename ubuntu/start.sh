#!/bin/bash
echo "Starting..."

round=1

while [ $round -lt 3 ]
do
    echo "round - $round"
    tech=zip
    key=guide_test-zip
    /usr/src/app/monitoramento.sh $round $tech $key &
    echo `zip -v /usr/src/app/data/GUIDE_Test.zip /usr/src/app/data/GUIDE_Test.csv` > resultados-$key-$round.txt

    echo "finding monitoramento.sh..."
    zip_pid=$(pgrep monitoramento.s)
    kill -TERM $zip_pid
    echo "killed monitoramento.sh..."
    rm /usr/src/app/data/GUIDE_Test.zip
    round=`expr $round + 1`
done


# monitoramento_zip_pid=$(pgrep monitoramento.zip.sh)  
# kill -TERM $monitoramento_zip_pid