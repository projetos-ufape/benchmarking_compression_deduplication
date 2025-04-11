#!/bin/bash
echo "Starting..."

tech=$1
key=$2
round=$3

# while [ $round -lt 3 ]
# do
    echo "round - $round"
    # tech=zip
    # key=guide_test-zip
    mkdir -p resultados-$tech

    /usr/src/app/monitoramento.sh $round $tech $key &
    
    arquivo_original="/usr/src/app/data/GUIDE_Test.csv"
    arquivo_comprimido="/usr/src/app/data/GUIDE_Test.zip"
    strace -c -e trace=read,write,open zip -v $arquivo_comprimido $arquivo_original > /dev/null 2> resultados-$tech/resultado-$key-$round.txt

    echo "finding monitoramento.sh..."
    zip_pid=$(pgrep monitoramento.s)
    kill -TERM $zip_pid
    echo "killed monitoramento.sh..."


    tamanho_original=$(stat -c %s "$arquivo_original")
    tamanho_comprimido=$(stat -c %s "$arquivo_comprimido")

    taxa=$(echo "scale=4; 1 - ($tamanho_comprimido / $tamanho_original)" | bc)
    taxa_percentual=$(echo "scale=2; $taxa * 100" | bc)
    echo "" >> resultados-$tech/resultado-$key-$round.txt
    echo "original reduzido taxa" >> resultados-$tech/resultado-$key-$round.txt
    echo "$tamanho_original $tamanho_comprimido $taxa_percentual" >> resultados-$tech/resultado-$key-$round.txt

    rm $arquivo_comprimido
    # round=`expr $round + 1`
# done

