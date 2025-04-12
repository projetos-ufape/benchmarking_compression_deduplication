import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def read_file(pasta, nome_arq1, nome_arq2, num_interacoes, conteudo):
    data = []
    
    for i in range(1, num_interacoes + 1):
        caminho1 = os.path.join(pasta, f"{nome_arq1}{i}.txt")
        caminho2 = os.path.join(pasta, f"{nome_arq2}{i}.txt")
        
        if os.path.exists(caminho1):
            try:
                df1 = pd.read_csv(caminho1, sep=r'\s+')
                media_MemTotal = df1["MemTotal"].mean()
                media_CPUPercent = df1["CPUPercent"].mean()
                media_MemUsed = df1["MemUsed"].mean()
                df1["datetime"] = pd.to_datetime(df1["datetime"])
                time_diff = (df1["datetime"].max() - df1["datetime"].min()).total_seconds()
            except Exception as e:
                print(f"Erro ao processar o arquivo {caminho1}: {e}")
                continue
        else:
            print(f"Arquivo não encontrado: {caminho1}")
            continue
        
        metric_read = None
        metric_write = None
        if os.path.exists(caminho2):
            try:
                with open(caminho2, "r") as f:
                    linhas = f.readlines()
                
                for linha in linhas:
                    partes = linha.strip().split()
                    if len(partes) >= 2:
                        if partes[-1].lower() == "read":
                            try:
                                metric_read = float(partes[3])
                            except:
                                metric_read = None
                        elif partes[-1].lower() == "write":
                            try:
                                metric_write = float(partes[3])
                            except:
                                metric_write = None
                filteredLines = [l.strip() for l in linhas if l.strip()]
                if filteredLines:
                    last_line = filteredLines[-1]
                    partitions = last_line.split()
                    if len(partitions) >= 3:
                        try:
                            compression_rate = float(partitions[-1])
                            compression_file = float(partitions[1])
                        except:
                            compression_rate = None
                            compression_file = None
            except Exception as e:
                print(f"Erro ao processar o arquivo {caminho2}: {e}")
        else:
            print(f"Arquivo não encontrado: {caminho2}")
            continue
        
        register = {
            "media_CPUPercent": media_CPUPercent,
            "media_MemUsed": media_MemUsed,
            "metric_read": metric_read,
            "metric_write": metric_write,
            "compression_rate": compression_rate,
            "compression_file": compression_file,
            "time_diff": time_diff,
            "conteudo": conteudo
        }
        
        data.append(register)
        
    df_final = pd.DataFrame(data)
    return df_final

def read_file_extended(pasta, nome_arq1, nome_arq2, nome_arq3, nome_arq4, num_interacoes, conteudo):
    data = []
    
    for i in range(1, num_interacoes + 1):
        caminho1 = os.path.join(pasta, f"{nome_arq1}{i}.txt")
        caminho2 = os.path.join(pasta, f"{nome_arq2}{i}.txt")
        caminho3 = os.path.join(pasta, f"{nome_arq3}{i}.txt")
        caminho4 = os.path.join(pasta, f"{nome_arq4}{i}.txt")
        
        if os.path.exists(caminho1) and os.path.exists(caminho3):
            try:
                df1 = pd.read_csv(caminho1, sep=r'\s+')
                df3 = pd.read_csv(caminho3, sep=r'\s+')
                
                df_combined = pd.concat([df1, df3], ignore_index=True)
                
                media_MemTotal = df_combined["MemTotal"].mean()
                media_CPUPercent = df_combined["CPUPercent"].mean()
                media_MemUsed = df_combined["MemUsed"].mean()
                df_combined["datetime"] = pd.to_datetime(df_combined["datetime"])
                time_diff = (df_combined["datetime"].max() - df_combined["datetime"].min()).total_seconds()
            except Exception as e:
                print(f"Erro ao processar os arquivos {caminho1} e/ou {caminho3}: {e}")
                continue
        else:
            if not os.path.exists(caminho1):
                print(f"Arquivo não encontrado: {caminho1}")
            if not os.path.exists(caminho3):
                print(f"Arquivo não encontrado: {caminho3}")
            continue
        
        metric_read_2 = None
        metric_write_2 = None
        metric_read_4 = None
        metric_write_4 = None
        
        if os.path.exists(caminho2):
            try:
                with open(caminho2, "r") as f:
                    linhas = f.readlines()
                for linha in linhas:
                    partes = linha.strip().split()
                    if len(partes) >= 2:
                        if partes[-1].lower() == "read":
                            try:
                                metric_read_2 = float(partes[3])
                            except:
                                metric_read_2 = None
                        elif partes[-1].lower() == "write":
                            try:
                                metric_write_2 = float(partes[3])
                            except:
                                metric_write_2 = None
            except Exception as e:
                print(f"Erro ao processar o arquivo {caminho2}: {e}")
                continue
        else:
            print(f"Arquivo não encontrado: {caminho2}")
            continue
        
        if os.path.exists(caminho4):
            try:
                with open(caminho4, "r") as f:
                    linhas = f.readlines()
                for linha in linhas:
                    partes = linha.strip().split()
                    if len(partes) >= 2:
                        if partes[-1].lower() == "read":
                            try:
                                metric_read_4 = float(partes[3])
                            except:
                                metric_read_4 = None
                        elif partes[-1].lower() == "write":
                            try:
                                metric_write_4 = float(partes[3])
                            except:
                                metric_write_4 = None
                filteredLines = [l.strip() for l in linhas if l.strip()]
                if filteredLines:
                    last_line = filteredLines[-1]
                    partitions = last_line.split()
                    if len(partitions) >= 3:
                        try:
                            compression_rate = float(partitions[-1])
                            compression_file = float(partitions[-2])
                        except:
                            compression_rate = None
                            compression_file = None
                    else:
                        compression_rate = None
                        compression_file = None
                else:
                    compression_rate = None
                    compression_file = None
            except Exception as e:
                print(f"Erro ao processar o arquivo {caminho4}: {e}")
                compression_rate = None
        else:
            print(f"Arquivo não encontrado: {caminho4}")
            continue
        
        if metric_read_2 is not None and metric_read_4 is not None:
            metric_read = metric_read_2 + metric_read_4
        elif metric_read_2 is not None:
            metric_read = metric_read_2
        else:
            metric_read = metric_read_4
        
        if metric_write_2 is not None and metric_write_4 is not None:
            metric_write = metric_write_2 + metric_write_4
        elif metric_write_2 is not None:
            metric_write = metric_write_2
        else:
            metric_write = metric_write_4
        
        register = {
            "media_CPUPercent": media_CPUPercent,
            "media_MemUsed": media_MemUsed,
            "metric_read": metric_read,
            "metric_write": metric_write,
            "compression_rate": compression_rate,
            "compression_file": compression_file,
            "time_diff": time_diff,
            "conteudo": conteudo
        }
        
        data.append(register)
        
    df_final = pd.DataFrame(data)
    return df_final

def salvar_tabela_imagem(df, nome_arquivo="./insights/tabela.png"):
    fig, ax = plt.subplots(figsize=(df.shape[1] * 2, df.shape[0] * 0.6))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=df.values, 
                     colLabels=df.columns, 
                     rowLabels=df.index, 
                     loc='center',
                     cellLoc='center')
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    
    plt.savefig(nome_arquivo, bbox_inches='tight', dpi=300)
    plt.close()
    print("Tabela salva com sucesso")

def extrair_insights(df, output_dir="insights"):
    if "conteudo" not in df.columns:
        print("Erro: o dataframe não contém a coluna 'conteudo'.")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    selected_cols = ["media_CPUPercent", "media_MemUsed", "metric_read", "metric_write", "compression_rate", "time_diff"]
    col_mapping = {
        "media_CPUPercent": "CPU Média (%)",
        "media_MemUsed": "Uso de Memória (GB)",
        "metric_read": "Chamadas de leitura",
        "metric_write": "Chamadas de escrita",
        "compression_rate": "Taxa de Compressão (%)",
        "time_diff": "Tempo de execução (seg)"
    }
    group_means = df.groupby("conteudo")[selected_cols].mean().rename(columns=col_mapping)
    group_means["Menor arquivo gerado"] = df.groupby("conteudo")["compression_file"].min() / 1024
    group_means["Maior arquivo gerado"] = df.groupby("conteudo")["compression_file"].max() / 1024

    tableName = output_dir + '/tabela_geral'
    salvar_tabela_imagem(group_means, tableName)
    for col in group_means.columns:
        plt.figure()
        group_means[col].plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title(f"{col} Média por Conteúdo")
        plt.xlabel("Conteúdo")
        plt.ylabel(col)
        plt.tight_layout()
        filename = os.path.join(output_dir, f"barplot_{col.replace(' ', '_')}.jpeg")
        plt.savefig(filename, format="jpeg", bbox_inches="tight")
        plt.close()
        print(f"Gráfico de barras para {col} salvo em: {filename}")
    for col in selected_cols:
        plt.figure()
        df.boxplot(column=col, by="conteudo")
        plt.title(f"Boxplot de {col_mapping[col]} por Conteúdo")
        plt.suptitle("")
        plt.xlabel("Conteúdo")
        plt.ylabel(col_mapping[col])
        plt.xticks(rotation=90)
        plt.tight_layout()
        filename = os.path.join(output_dir, f"boxplot_{col_mapping[col].replace(' ', '_')}.jpeg")
        plt.savefig(filename, format="jpeg", bbox_inches="tight")
        plt.close()
        print(f"Boxplot para {col_mapping[col]} salvo em: {filename}")

def main():

    if len(sys.argv) > 1 and sys.argv[1].lower() == 'l':
        print("sys_argv = ", sys.argv[1])
        dataBase = "linux-master-clone"
    else:
        dataBase = "GUIDE_Test"

    if len(sys.argv) > 2:
        numInteractions = int(sys.argv[2])
    else:
        numInteractions = 10

    print("Database escolhido: ", dataBase)
    print("Número de arquivos: ", numInteractions)

    df_gzip = read_file(
        "./resultados-gzip",
        f"log-{dataBase}-gzip-",
        f"resultado-{dataBase}-gzip-",
        numInteractions,
        "GZip"
    )
    df_zip = read_file(
        "./resultados-zip",
        f"log-{dataBase}-zip-",
        f"resultado-{dataBase}-zip-",
        numInteractions,
        "Zip"
    )
    df_7z = read_file(
        "./resultados-7z",
        f"log-{dataBase}-7z-",
        f"resultado-{dataBase}-7z-",
        numInteractions,
        "7Z"
    )
    df_bzip2 = read_file(
        "./resultados-bzip2",
        f"log-{dataBase}-bzip2-",
        f"resultado-{dataBase}-bzip2-",
        numInteractions,
        "BZip2"
    )
    df_zbackup = read_file(
        "./resultados-zbackup",
        f"log-{dataBase}-zbackup-",
        f"resultado-{dataBase}-zbackup-",
        numInteractions,
        "Zbackup"
    )
    df_borg = read_file(
        "./resultados-borg",
        f"log-{dataBase}-borg-",
        f"resultado-{dataBase}-borg-",
        numInteractions,
        "Borg"
    )
    df_restic = read_file(
        "./resultados-restic",
        f"log-{dataBase}-restic-",
        f"resultado-{dataBase}-restic-",
        numInteractions,
        "Restic"
    )

    df_gzip_zbackup = read_file_extended(
        "./resultados-gzip_zbackup",
        f"log-{dataBase}-gzip-",
        f"resultado-{dataBase}-gzip-",
        f"log-{dataBase}-zbackup-",
        f"resultado-{dataBase}-zbackup-",
        numInteractions,
        "Gzip-Zbackup"
    )
    df_gzip_borg = read_file_extended(
        "./resultados-gzip_borg",
        f"log-{dataBase}-gzip-",
        f"resultado-{dataBase}-gzip-",
        f"log-{dataBase}-borg-",
        f"resultado-{dataBase}-borg-",
        numInteractions,
        "Gzip-Borg"
    )
    df_gzip_restic = read_file_extended(
        "./resultados-gzip_restic",
        f"log-{dataBase}-gzip-",
        f"resultado-{dataBase}-gzip-",
        f"log-{dataBase}-restic-",
        f"resultado-{dataBase}-restic-",
        numInteractions,
        "Gzip-Restic"
    )
    df_zip_zbackup = read_file_extended(
        "./resultados-zip_zbackup",
        f"log-{dataBase}-zip-",
        f"resultado-{dataBase}-zip-",
        f"log-{dataBase}-zbackup-",
        f"resultado-{dataBase}-zbackup-",
        numInteractions,
        "Zip-Zbackup"
    )
    df_zip_borg = read_file_extended(
        "./resultados-zip_borg",
        f"log-{dataBase}-zip-",
        f"resultado-{dataBase}-zip-",
        f"log-{dataBase}-borg-",
        f"resultado-{dataBase}-borg-",
        numInteractions,
        "Zip-Borg"
    )
    df_zip_restic = read_file_extended(
        "./resultados-zip_restic",
        f"log-{dataBase}-zip-",
        f"resultado-{dataBase}-zip-",
        f"log-{dataBase}-restic-",
        f"resultado-{dataBase}-restic-",
        numInteractions,
        "Zip-Restic"
    )
    df_7z_borg = read_file_extended(
        "./resultados-7z_borg",
        f"log-{dataBase}-7z-",
        f"resultado-{dataBase}-7z-",
        f"log-{dataBase}-borg-",
        f"resultado-{dataBase}-borg-",
        numInteractions,
        "7z-Borg"
    )
    df_7z_restic = read_file_extended(
        "./resultados-7z_restic",
        f"log-{dataBase}-7z-",
        f"resultado-{dataBase}-7z-",
        f"log-{dataBase}-restic-",
        f"resultado-{dataBase}-restic-",
        numInteractions,
        "7z-Restic"
    )
    df_7z_zbackup = read_file_extended(
        "./resultados-7z_zbackup",
        f"log-{dataBase}-7z-",
        f"resultado-{dataBase}-7z-",
        f"log-{dataBase}-zbackup-",
        f"resultado-{dataBase}-zbackup-",
        numInteractions,
        "7z-Zbackup"
    )
    df_bzip2_zbackup = read_file_extended(
        "./resultados-bzip2_zbackup",
        f"log-{dataBase}-bzip2-",
        f"resultado-{dataBase}-bzip2-",
        f"log-{dataBase}-zbackup-",
        f"resultado-{dataBase}-zbackup-",
        numInteractions,
        "Bzip2-Zbackup"
    )
    df_bzip2_borg = read_file_extended(
        "./resultados-bzip2_borg",
        f"log-{dataBase}-bzip2-",
        f"resultado-{dataBase}-bzip2-",
        f"log-{dataBase}-borg-",
        f"resultado-{dataBase}-borg-",
        numInteractions,
        "Bzip2-Borg"
    )
    df_bzip2_restic = read_file_extended(
        "./resultados-bzip2_restic",
        f"log-{dataBase}-bzip2-",
        f"resultado-{dataBase}-bzip2-",
        f"log-{dataBase}-restic-",
        f"resultado-{dataBase}-restic-",
        numInteractions,
        "Bzip2-Restic"
    )

    df_zbackup_gzip = read_file_extended(
        "./resultados-zbackup_gzip",
        f"log-{dataBase}-zbackup-",
        f"resultado-{dataBase}-zbackup-",
        f"log-zbackuprepo-{dataBase}-gzip-",
        f"resultado-zbackuprepo-{dataBase}-1-gzip-",
        numInteractions,
        "ZBackup-Gzip"
    )
    df_zbackup_zip = read_file_extended(
        "./resultados-zbackup_zip",
        f"log-{dataBase}-zbackup-",
        f"resultado-{dataBase}-zbackup-",
        f"log-zbackuprepo-{dataBase}-1-zip-",
        f"resultado-zbackuprepo-{dataBase}-1-zip-",
        numInteractions,
        "ZBackup-Zip"
    )
    df_zbackup_7z = read_file_extended(
        "./resultados-zbackup_7z",
        f"log-{dataBase}-zbackup-",
        f"resultado-{dataBase}-zbackup-",
        f"log-zbackuprepo-{dataBase}-1-7z-",
        f"resultado-zbackuprepo-{dataBase}-1-7z-",
        numInteractions,
        "ZBackup-7z"
    )
    df_zbackup_bzip2 = read_file_extended(
        "./resultados-zbackup_bzip2",
        f"log-{dataBase}-zbackup-",
        f"resultado-{dataBase}-zbackup-",
        f"log-zbackuprepo-{dataBase}-1-bzip2-",
        f"resultado-zbackuprepo-{dataBase}-1-bzip2-",
        numInteractions,
        "ZBackup-Bzip2"
    )
    df_borg_gzip = read_file_extended(
        "./resultados-borg_gzip",
        f"log-{dataBase}-borg-",
        f"resultado-{dataBase}-borg-",
        f"log-borgrepo-{dataBase}-1-gzip-",
        f"resultado-borgrepo-{dataBase}-1-gzip-",
        numInteractions,
        "Borg-Gzip"
    )
    df_borg_zip = read_file_extended(
        "./resultados-borg_zip",
        f"log-{dataBase}-borg-",
        f"resultado-{dataBase}-borg-",
        f"log-borgrepo-{dataBase}-1-zip-",
        f"resultado-borgrepo-{dataBase}-1-zip-",
        numInteractions,
        "Borg-Zip"
    )
    df_borg_7z = read_file_extended(
        "./resultados-borg_7z",
        f"log-{dataBase}-borg-",
        f"resultado-{dataBase}-borg-",
        f"log-borgrepo-{dataBase}-1-7z-",
        f"resultado-borgrepo-{dataBase}-1-7z-",
        numInteractions,
        "Borg-7z"
    )
    df_borg_bzip2 = read_file_extended(
        "./resultados-borg_bzip2",
        f"log-{dataBase}-borg-",
        f"resultado-{dataBase}-borg-",
        f"log-borgrepo-{dataBase}-1-bzip2-",
        f"resultado-borgrepo-{dataBase}-1-bzip2-",
        numInteractions,
        "Borg-Bzip2"
    )
    df_restic_gzip = read_file_extended(
        "./resultados-restic_gzip",
        f"log-{dataBase}-restic-",
        f"resultado-{dataBase}-restic-",
        f"log-resticrepo-{dataBase}-1-gzip-",
        f"resultado-resticrepo-{dataBase}-1-gzip-",
        numInteractions,
        "Restic-Gzip"
    )
    df_restic_zip = read_file_extended(
        "./resultados-restic_zip",
        f"log-{dataBase}-restic-",
        f"resultado-{dataBase}-restic-",
        f"log-resticrepo-{dataBase}-1-zip-",
        f"resultado-resticrepo-{dataBase}-1-zip-",
        numInteractions,
        "Restic-Zip"
    )
    df_restic_7z = read_file_extended(
        "./resultados-restic_7z",
        f"log-{dataBase}-restic-",
        f"resultado-{dataBase}-restic-",
        f"log-resticrepo-{dataBase}-1-7z-",
        f"resultado-resticrepo-{dataBase}-1-7z-",
        numInteractions,
        "Restic-7z"
    )
    df_restic_bzip2 = read_file_extended(
        "./resultados-restic_bzip2",
        f"log-{dataBase}-restic-",
        f"resultado-{dataBase}-restic-",
        f"log-resticrepo-{dataBase}-1-bzip2-",
        f"resultado-resticrepo-{dataBase}-1-bzip2-",
        numInteractions,
        "Restic-Bzip2"
    )

    lista_dfs = [
        df_gzip, df_zip, df_7z, df_bzip2, df_zbackup, df_borg, df_restic,
        df_gzip_zbackup, df_gzip_borg, df_gzip_restic, df_zip_zbackup, df_zip_borg,
        df_zip_restic, df_7z_borg, df_7z_restic, df_7z_zbackup, df_bzip2_zbackup,
        df_bzip2_borg, df_bzip2_restic, df_zbackup_gzip, df_zbackup_zip, df_zbackup_7z,
        df_zbackup_bzip2, df_borg_gzip, df_borg_zip, df_borg_7z, df_borg_bzip2,
        df_restic_gzip, df_restic_zip, df_restic_7z, df_restic_bzip2
    ]

    # Concatena todos os DataFrames em um único DataFrame
    df_resultados = pd.concat(lista_dfs, ignore_index=True, axis=0)

    insightDir = "insights/" + dataBase
    extrair_insights(df_resultados, insightDir)

if __name__ == "__main__":
    main()