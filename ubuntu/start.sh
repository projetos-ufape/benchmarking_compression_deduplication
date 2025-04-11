#!/bin/bash
echo "Starting..."

techs=$1
filename=$2
round=$3

mkdir -p resultados/resultados-$techs

origin_file=$filename
temp_file=$origin_file
base_name=""
result_path="resultados/resultados-$techs"
result_file=""

IFS='_' read -r -a TECH_ARRAY <<< "$1"

for tech in "${TECH_ARRAY[@]}"; do
    echo "rodando - $tech"
    suffix=""
    cmd=""
    
    case "$tech" in
        zip)
            suffix="zip"
            cmd="zip -v"
            ;;
        gzip)
            suffix="gz"
            cmd="gzip -c"
            ;;
        bzip2)
            suffix="bz2"
            cmd="bzip2 -c"
            ;;
        7z)
            suffix="7z"
            cmd="7z a"
            ;;
        duperemove)
            suffix="dedup"
            cmd="duperemove -dhr"
            ;;
        borgbackup)
            suffix="borg"
            cmd="borg create --compression lz4 repo::archive"
            ;;
        restic)
            suffix="restic"
            cmd="restic backup"
            ;;
        opendedup)
            suffix="sdfs"
            cmd="sdfscli backup"
            ;;
        *)
            echo "Tecnologia não suportada: $tech"
            exit 1
            ;;
    esac

    base_name=$(basename "$temp_file" | cut -f1 -d '.')
    file_compressed="$base_name.$suffix"
    echo "file_compressed: $file_compressed"
    result_file="resultado-$base_name-$tech-$round.txt"

    /usr/src/app/monitoramento.sh $round $tech $base_name $result_path &

    echo "executando comando: $cmd"
    if [[ "$tech" == "zip" || "$tech" == "7z" ]]; then
        strace -c -e trace=read,write,open $cmd /usr/src/app/data/$file_compressed /usr/src/app/data/$temp_file > /dev/null 2> $result_path/$result_file
    elif [[ "$tech" == "gzip" || "$tech" == "bzip2" ]]; then
        strace -c -e trace=read,write,open $cmd /usr/src/app/data/$temp_file > /usr/src/app/data/$file_compressed 2> $result_path/$result_file
    else
        # Comandos simulados para deduplicadores e backups
        echo "no implementation"
    fi

    echo "finding monitoramento.sh..."
    monitor_pid=$(pgrep -f monitoramento.sh)
    kill -TERM $monitor_pid
    echo "killed monitoramento.sh..."

    temp_file=$file_compressed
done

origin_size=$(stat -c %s "/usr/src/app/data/$origin_file")
compressed_size=$(stat -c %s "/usr/src/app/data/$file_compressed")

rate=$(echo "scale=4; 1 - ($compressed_size / $origin_size)" | bc)
rate_percent=$(echo "scale=2; $rate * 100" | bc)

echo "" >> $result_path/$result_file
echo "original reduzido taxa" >> $result_path/$result_file
echo "$origin_size $compressed_size $rate_percent" >> $result_path/$result_file

rm "/usr/src/app/data/$file_compressed"
echo "finished job"
