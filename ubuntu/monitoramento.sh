#!/bin/bash

round=$1
tech=$2
key=$3

cd resultados/resultados-$tech
echo "Cont MemTotal CPUPercent MemUsed datetime" > log-$key-$round.txt
cont=1

while [ True ]
do
        mem=`free | grep Mem | awk {'print $2'}`
        cpuAndMem=`pidstat -ur -h -p ALL 1 1 | grep $tech | awk '{sum += $8; memUsed += $13;} END {printf "%.2f %.2f\n", sum, memUsed}'`
        date=`date +"%Y-%m-%dT%H:%M:%S%z"`
        echo $cont $mem $cpuAndMem $date >> log-$key-$round.txt
        cont=`expr $cont + 1`
done