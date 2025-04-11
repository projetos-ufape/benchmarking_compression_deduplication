#!/bin/bash

round=$1
tech=$2
base_name=$3
path=$4

echo "monitoramento $round $tech $base_name $path"

cd $path
echo "Cont MemTotal CPUPercent MemUsed datetime" > log-$base_name-$tech-$round.txt
cont=1

while [ True ]
do
        mem=`free | grep Mem | awk {'print $2'}`
        cpuAndMem=`pidstat -ur -h -p ALL 1 1 | grep $tech | awk '{sum += $8; memUsed += $13;} END {printf "%.2f %.2f\n", sum, memUsed}'`
        date=`date +"%Y-%m-%dT%H:%M:%S%z"`
        echo $cont $mem $cpuAndMem $date >> log-$base_name-$tech-$round.txt
        cont=`expr $cont + 1`
done