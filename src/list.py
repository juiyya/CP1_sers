import time
import random
import tracemalloc
import csv
import pathlib
from codecarbon import EmissionsTracker 

# diretorio do script src atual
src_dir = pathlib.Path(__file__).parent

# diretório de saída dos resultados
saida_csv = src_dir / "outputs" / "resultados.csv"
saida_emissions = saida_csv.parent / "emissions.csv"

# salvar resultados de linkedlist em csv
def salvar_resultados_csv(nome_arquivo, dados, cabecalho):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            arquivo_existe = True
    except FileNotFoundError:
        arquivo_existe = False
    
    with open(nome_arquivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=cabecalho)
        if not arquivo_existe:
            writer.writeheader()
        writer.writerow(dados)
# config do tracker de emissões
tracker = EmissionsTracker(
    output_dir=str(src_dir / "outputs"),  # muda diretório do tracker
    output_file="emissions.csv"
)
# início do teste e do tracker
tracker.start()
tracemalloc.start()
inicio = time.time()

#LISTA
lista = []
# insert 
for i in range(100_000):
    lista.append(i)
# busca 
for i in range(50_000):
    valor = random.randint(0, 99_999)
    if valor in lista:
        pass
# remocao 
for i in range(20_000):
    if lista:
        lista.pop()

# tempo de execução
fim = time.time()
tempo_execucao = fim - inicio

#emissoes c02
emissoes = tracker.stop()

# energia total usada
energia = tracker._total_energy.kWh

#memoria
memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
tracemalloc.stop()
    
print("Tempo de execução:", fim - inicio, "segundos")
print("Memória atual usada:", memoria_atual / 10**6, "MB")
print("Pico de memória:", memoria_pico / 10**6, "MB")
print("Energia consumida:", f"{energia / 10**6:.12f}"  , "kWh")


# dados para salvar em csv
dados = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "estrutura": "lista",
    "tempo_execucao": tempo_execucao,
    "memoria_atual_mb": memoria_atual / 10**6,
    "memoria_pico_mb": memoria_pico / 10**6,
    'energia_gasta_kwh': energia,
    'tamanho_estrutura': len(lista)
}

# salvar resultados em csv
cabecalho = [
    'timestamp',
    'estrutura',
    'tempo_execucao',
    'memoria_atual_mb',
    'memoria_pico_mb',
    'energia_gasta_kwh',
    'tamanho_estrutura',
]

salvar_resultados_csv(saida_csv, dados, cabecalho)

print(f"dados salvos em {saida_csv}")
