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
    
    base_name=$(basename "$temp_file" | cut -f1 -d '.')
    file_compressed=""
    result_file="resultado-$base_name-$tech-$round.txt"

    case "$tech" in
        zip)
            suffix="zip"
            file_compressed="$base_name.$suffix"
            cmd="zip -v /usr/src/app/data/$file_compressed /usr/src/app/data/$temp_file"
            ;;
        gzip)
            suffix="gz"
            file_compressed="$base_name.$suffix"
            cmd="gzip -c /usr/src/app/data/$temp_file > /usr/src/app/data/$file_compressed"
            ;;
        bzip2)
            suffix="bz2"
            file_compressed="$base_name.$suffix"
            cmd="bzip2 -c /usr/src/app/data/$temp_file > /usr/src/app/data/$file_compressed"
            ;;
        7z)
            suffix="7z"
            file_compressed="$base_name.$suffix"
            cmd="7z a /usr/src/app/data/$file_compressed /usr/src/app/data/$temp_file"
            ;;
        duperemove)
            suffix="dedup"
            dedup_dir="/usr/src/app/tmp/duperemove/$base_name-$round"
            mkdir -p "$dedup_dir"
            cp "/usr/src/app/data/$temp_file" "$dedup_dir"
            cmd="duperemove -dr --hashfile=$dedup_dir/hashfile $dedup_dir"
            file_compressed="$base_name.$suffix"
            ;;
        borg)
            suffix="borg"
            repo="tmp/borgrepo-$base_name-$round"
            mkdir -p "/usr/src/app/data/$repo"
            export BORG_PASSPHRASE="test"
            borg init --encryption=none "/usr/src/app/data/$repo"
            cmd="borg create --stats /usr/src/app/data/$repo::backup-round-$round /usr/src/app/data/$temp_file"
            file_compressed=$repo
            ;;
        restic)
            suffix="restic"
            repo="/usr/src/app/tmp/resticrepo-$base_name-$round"
            mkdir -p "$repo"
            export RESTIC_PASSWORD="test"
            export RESTIC_REPOSITORY="$repo"
            restic init
            cmd="restic backup /usr/src/app/data/$temp_file"
            file_compressed="$base_name.$suffix"
            ;;
        opendedup)
            suffix="sdfs"
            sdfs_dir="/usr/src/app/tmp/sdfs/$base_name-$round"
            mkdir -p "$sdfs_dir"
            cp "/usr/src/app/data/$temp_file" "$sdfs_dir"
            cmd="ls $sdfs_dir"
            file_compressed="$base_name.$suffix"
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
    # elif [[ "$tech" == "duperemove" ]]; then
    #     strace -c -e trace=read,write,open $cmd > /dev/null 2> $result_path/$result_file
    #     cp "$dedup_dir/$(basename $temp_file)" "/usr/src/app/data/$file_compressed"
    elif [[ "$tech" == "borg)" ]]; then
        strace -c -e trace=read,write,open $cmd > /dev/null 2> $result_path/$result_file
        du -bcs "/usr/src/app/data/$repo" > "/usr/src/app/data/$file_compressed"
    elif [[ "$tech" == "restic" ]]; then
        strace -c -e trace=read,write,open $cmd > /dev/null 2> $result_path/$result_file
        du -bcs "$repo" | grep total | awk '{print $1}' > "/usr/src/app/data/$file_compressed"
    elif [[ "$tech" == "opendedup" ]]; then
        strace -c -e trace=read,write,open $cmd > /dev/null 2> $result_path/$result_file
        cp "$sdfs_dir/$(basename $temp_file)" "/usr/src/app/data/$file_compressed"
    fi

    echo "finding monitoramento.sh..."
    monitor_pid=$(pgrep -f monitoramento.sh)
    kill -TERM $monitor_pid
    echo "killed monitoramento.sh..."

    temp_file=$file_compressed
done

echo "origin_file: /usr/src/app/data/$origin_file"
echo "compressed_file: /usr/src/app/data/$file_compressed"

origin_size=$(stat -c %s "/usr/src/app/data/$origin_file")
compressed_size=$(stat -c %s "/usr/src/app/data/$file_compressed")

rate=$(echo "scale=4; 1 - ($compressed_size / $origin_size)" | bc)
rate_percent=$(echo "scale=2; $rate * 100" | bc)

echo "" >> $result_path/$result_file
echo "original reduzido taxa" >> $result_path/$result_file
echo "$origin_size $compressed_size $rate_percent" >> $result_path/$result_file

if [ -e "/usr/src/app/data/$file_compressed" ]; then
    if [ -d "/usr/src/app/data/$file_compressed" ]; then
        rm -rf "/usr/src/app/data/$file_compressed"
    else
        rm -f "/usr/src/app/data/$file_compressed"
    fi
fi

echo "finished job"
