#!/bin/bash
echo "Starting service..."

# Lista de tecnologias
# isoladas | compactação_deduplicação | deduplicação_compactação
techs=("zip" "7z" "gzip" "bzip2" "borg" "restic" "zbackup" \
    "zip_borg" "zip_restic" "zip_zbackup" \
    "7z_borg" "7z_restic" "7z_zbackup" \
    "gzip_borg" "gzip_restic" "gzip_zbackup" \
    "bzip2_borg" "bzip2_restic" "bzip2_zbackup" \
    "borg_zip" "borg_7z" "borg_gzip" "borg_bzip2" \
    "restic_zip" "restic_7z" "restic_gzip" "restic_bzip2" \
    "zbackup_zip" "zbackup_7z" "zbackup_gzip" "zbackup_bzip2" \
    )

# Lista de arquivos
files=("GUIDE_Test.csv" "linux-master-clone")

make down

for tech in "${techs[@]}"; do
    export TECH="$tech"

    for file in "${files[@]}"; do
        export FILENAME="$file"

        for round in {1..10}; do
            export ROUND="$round"

            echo "Executando: TECH=$TECH, FILENAME=$FILENAME, ROUND=$ROUND"

            make up-build
            make down
        done
    done
done
