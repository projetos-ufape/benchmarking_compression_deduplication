#!/bin/bash
echo "Starting..."

techs=$1
filename=$2
round=$3

mkdir -p resultados/resultados-$techs

origin_file=$filename
temp_file=$filename
base_name=""
result_path="resultados/resultados-$techs"
result_file=""

IFS='_' read -r -a TECH_ARRAY <<< "$techs"

for tech in "${TECH_ARRAY[@]}"; do
    echo "rodando - $tech"
    suffix=""
    cmd=""
    
    base_name=$(basename "$temp_file" | cut -f1 -d '.')
    file_compressed=""
    result_file="resultado-$base_name-$tech-$round.txt"

    is_dir=false
    if [ -d "/usr/src/app/data/$temp_file" ]; then
        is_dir=true
    fi

    echo "$origin_file $temp_file , $base_name "

    case "$tech" in
        zip)
            suffix="zip"
            file_compressed="$base_name.$suffix"
            cmd="zip -r /usr/src/app/data/$file_compressed /usr/src/app/data/$temp_file"
            ;;
        gzip)
            suffix="gz"
            if $is_dir; then
                tar_file="$base_name.tar"
                tar -cf "/usr/src/app/data/$tar_file" -C "/usr/src/app/data" "$temp_file" 
                temp_file="$tar_file"
            fi
            file_compressed="$base_name.$suffix"
            cmd="gzip -c /usr/src/app/data/$temp_file > /usr/src/app/data/$file_compressed"
            ;;
        bzip2)
            suffix="bz2"
            if $is_dir; then
                tar_file="$base_name.tar"
                tar -cf "/usr/src/app/data/$tar_file" -C "/usr/src/app/data" "$temp_file" 
                temp_file="$tar_file"
            fi
            file_compressed="$base_name.$suffix"
            cmd="bzip2 -c /usr/src/app/data/$temp_file > /usr/src/app/data/$file_compressed"
            ;;
        7z)
            suffix="7z"
            file_compressed="$base_name.$suffix"
            cmd="7z a /usr/src/app/data/$file_compressed /usr/src/app/data/$temp_file"
            ;;
        borg)
            suffix="borg"
            repo="tmp/${base_name}-${round}"
            mkdir -p "/usr/src/app/data/$repo"
            export BORG_PASSPHRASE="test"
            borg init --encryption=none "/usr/src/app/data/$repo"
            cmd="borg create /usr/src/app/data/$repo::backup-round-$round /usr/src/app/data/$temp_file"
            file_compressed="$repo"
            du -bcs "/usr/src/app/data/$repo" > "/usr/src/app/data/${repo}.size"
            ;;
        restic)
            suffix="restic"
            repo="tmp/${base_name}-${round}"
            mkdir -p "/usr/src/app/data/$repo"
            export RESTIC_PASSWORD="test"
            export RESTIC_REPOSITORY="/usr/src/app/data/$repo"
            restic init
            cmd="restic backup /usr/src/app/data/$temp_file"
            file_compressed="$repo"
            du -bcs "/usr/src/app/data/$repo" | grep total | awk '{print $1}' > "/usr/src/app/data/${repo}.size"
            ;;
        zbackup)
            suffix="zbackup"
            repo="tmp/${base_name}-${round}"
            mkdir -p "/usr/src/app/data/$repo"
            zbackup init --non-encrypted "/usr/src/app/data/$repo"
            cmd="tar -cf - /usr/src/app/data/$temp_file 2>/dev/null | strace -c -e trace=read,write,open zbackup --non-encrypted backup /usr/src/app/data/$repo/backups/backup-$round 2> $result_path/$result_file"
            file_compressed="$repo"
            ;;
        *)
            echo "Tecnologia não suportada: $tech"
            exit 1
            ;;
    esac

    echo "file_compressed: $file_compressed"
    /usr/src/app/monitoramento.sh $round $tech $base_name $result_path &

    echo "executando comando: $cmd"
    
    if [[ "$tech" == "zip" || "$tech" == "7z" ]]; then
        strace -c -e trace=read,write,open $cmd > /dev/null 2> $result_path/$result_file
    elif [[ "$tech" == "gzip" || "$tech" == "bzip2" ]]; then
        eval "strace -c -e trace=read,write,open $cmd" 2> $result_path/$result_file
    elif [[ "$tech" == "borg" || "$tech" == "restic" ]]; then  # Atualizado
        strace -c -e trace=read,write,open $cmd > /dev/null 2> $result_path/$result_file
    elif [[ "$tech" == "zbackup" ]]; then
        eval "$cmd"
    fi

    echo "finding monitoramento.sh..."
    monitor_pid=$(pgrep -f monitoramento.sh)
    kill -TERM $monitor_pid
    echo "killed monitoramento.sh..."

    if [[ "$tech" == "gzip" || "$tech" == "bzip2" ]] && [ "$temp_file" != "$origin_file" ]; then
        rm -f "/usr/src/app/data/$temp_file"
    fi

    temp_file=$file_compressed
done

if [ -d "/usr/src/app/data/$origin_file" ]; then
    origin_size=$(du -bcs "/usr/src/app/data/$origin_file" | awk '/total/ {print $1}')
else
    origin_size=$(stat -c %s "/usr/src/app/data/$origin_file")
fi

if [[ -f "/usr/src/app/data/${temp_file}.size" ]]; then
    compressed_size=$(cat "/usr/src/app/data/${temp_file}.size")
else
    compressed_size=$(stat -c %s "/usr/src/app/data/$file_compressed")
fi

rate=$(echo "scale=4; 1 - ($compressed_size / $origin_size)" | bc)
rate_percent=$(echo "scale=2; $rate * 100" | bc)

echo "" >> $result_path/$result_file
echo "original reduzido taxa" >> $result_path/$result_file
echo "$origin_size $compressed_size $rate_percent" >> $result_path/$result_file

find "/usr/src/app/data/tmp/" -name "*${round}*" -exec rm -rf {} \; 2>/dev/null

echo "finished job"