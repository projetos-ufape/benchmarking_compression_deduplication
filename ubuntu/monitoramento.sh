#!/bin/bash

round=$1
tech=$2
key=$3

mkdir -p resultados-$tech
cd resultados-$tech
echo "Cont MemTotal CPUPercent MemUsed kB_rd/s kB_wr/s datetime" > log-$key-$round.txt
cont=1

while [ True ]
do
        mem=`free | grep Mem | awk {'print $2'}`
        cpuAndMem=`pidstat -ur -h -d -p ALL 1 1 | grep $tech | awk '{sum += $8; memUsed += $13; kbRd += $15; kbWr += $16} END {printf "%.2f %.2f %.2f %.2f\n", sum, memUsed, kbRd, kbWr}'`
        date=`date +"%Y-%m-%dT%H:%M:%S%z"`
        echo $cont $mem $cpuAndMem $date >> log-$key-$round.txt
        cont=`expr $cont + 1`
done