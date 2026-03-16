import csv
from collections import defaultdict
import pathlib

import matplotlib.pyplot as plt

# diretorio do script src atual
src_dir = pathlib.Path(__file__).parent

#diretorio de saida dos resultados (trace)
saida_csv = src_dir / "outputs" / "resultados.csv"

# le os resultados do csv e retorna um dicionario com os resultados por estrutura
def ler_resultados(saida_csv=saida_csv):
    resultados = defaultdict(list)

    with open(saida_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            estrutura = row.get("estrutura") or row.get("script")
            if not estrutura:
                continue

            tempo = float(row.get("tempo_execucao", 0) or 0)
            memoria = float(row.get("memoria_pico_mb", 0) or 0)
            energia = float(row.get("energia_gasta_kwh", 0) or 0)

            resultados[estrutura].append({
                "tempo": tempo,
                "memoria": memoria,
                "energia": energia,
            })

    return resultados

# calcula a media de tempo, memoria e energia por estrutura
def media_por_estrutura(resultados):
    medias = {}
    for estrutura, entradas in resultados.items():
        if not entradas:
            continue
        medias[estrutura] = {
            "tempo": sum(e["tempo"] for e in entradas) / len(entradas),
            "memoria": sum(e["memoria"] for e in entradas) / len(entradas),
            "energia": sum(e["energia"] for e in entradas) / len(entradas),
        }
    return medias

# plota graficos de barras para tempo, memoria e energia
def plotar_barras(medias):
    estruturas = list(medias.keys())
    
    tempos = [medias[e]["tempo"] for e in estruturas]
    memorias = [medias[e]["memoria"] for e in estruturas]
    energias = [medias[e]["energia"] for e in estruturas]

    #tempo medio execucao
    plt.figure(figsize=(8, 4))
    plt.bar(estruturas, tempos, color="tab:blue")
    plt.title("Tempo médio de execução")
    plt.ylabel("segundos")
    
    for i, tempo in enumerate(tempos):
        plt.text(i, tempo, f'{tempo:.2f}s', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.show()

    # pico medio memoria
    plt.figure(figsize=(8, 4))
    plt.bar(estruturas, memorias, color="tab:orange")
    plt.title("Memória pico média")
    plt.ylabel("MB")
    
    for i, memoria in enumerate(memorias):
        plt.text(i, memoria, f'{memoria:.2f} MB', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.show()

    # energia media consumida
    plt.figure(figsize=(8, 4))
    plt.bar(estruturas, energias)
    plt.title("Energia média consumida")
    plt.ylabel("kWh")
    for i, energia in enumerate(energias):
        plt.text(i, energia, f'{energia:.12f} kWh', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    resultados = ler_resultados()
    if not resultados:
        raise SystemExit("nenhum resultado encontrado em 'resultados.csv'")

    medias = media_por_estrutura(resultados)
    plotar_barras(medias)
