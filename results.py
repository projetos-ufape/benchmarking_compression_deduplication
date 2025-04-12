import os
import pandas as pd
import matplotlib.pyplot as plt

def read_file(pasta, nome_arq1, nome_arq2, num_interacoes, conteudo):
    data = []
    
    for i in range(1, num_interacoes + 1):
        caminho1 = os.path.join(pasta, f"{nome_arq1}{i}.txt")
        caminho2 = os.path.join(pasta, f"{nome_arq2}{i}.txt")
        
        if os.path.exists(caminho1):
            try:
                df1 = pd.read_csv(caminho1, sep='\s+')
                media_MemTotal = df1["MemTotal"].mean()
                media_CPUPercent = df1["CPUPercent"].mean()
                media_MemUsed = df1["MemUsed"].mean()
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
                                metric_read = float(partes[1])
                            except:
                                metric_read = None
                        elif partes[-1].lower() == "write":
                            try:
                                metric_write = float(partes[1])
                            except:
                                metric_write = None
                filteredLines = [l.strip() for l in linhas if l.strip()]
                if filteredLines:
                    last_line = filteredLines[-1]
                    partitions = last_line.split()
                    if len(partitions) >= 3:
                        try:
                            compression_rate = float(partitions[-1])
                        except:
                            compression_rate = None
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
            "conteudo": conteudo
        }
        
        data.append(register)
        
    df_final = pd.DataFrame(data)
    return df_final

def extrair_insights(df, output_dir="insights"):
    if "conteudo" not in df.columns:
        print("Erro: o dataframe não contém a coluna 'conteudo'.")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    selected_cols = ["media_CPUPercent", "media_MemUsed", "metric_read", "metric_write", "compression_rate"]
    col_mapping = {
        "media_CPUPercent": "CPU Média",
        "media_MemUsed": "Uso de Memória",
        "metric_read": "Leitura",
        "metric_write": "Escrita",
        "compression_rate": "Taxa de Compressão"
    }
    group_means = df.groupby("conteudo")[selected_cols].mean().rename(columns=col_mapping)
    print("\nMédias Agrupadas por Conteúdo:")
    print(group_means)
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
        plt.tight_layout()
        filename = os.path.join(output_dir, f"boxplot_{col_mapping[col].replace(' ', '_')}.jpeg")
        plt.savefig(filename, format="jpeg", bbox_inches="tight")
        plt.close()
        print(f"Boxplot para {col_mapping[col]} salvo em: {filename}")

def main():
    df_gzip = read_file("./resultados-gzip", "log-GUIDE_Test-gzip-", "resultado-GUIDE_Test-gzip-", 1, "GZip")
    df_zip = read_file("./resultados-zip", "log-GUIDE_Test-zip-", "resultado-GUIDE_Test-zip-", 1, "Zip")
    df_7z = read_file("./resultados-7z", "log-GUIDE_Test-7z-", "resultado-GUIDE_Test-7z-", 1, "7Z")
    df_bzip2 = read_file("./resultados-bzip2", "log-GUIDE_Test-bzip2-", "resultado-GUIDE_Test-bzip2-", 1, "BZip2")


    #Dentro desse array [df_gzip, df_zip, df_7z, df_bzip2] adicione todos os outros dfs
    df_resultados = pd.concat([df_gzip, df_zip, df_7z, df_bzip2], axis=0, ignore_index=True)
    extrair_insights(df_resultados)

if __name__ == "__main__":
    main()