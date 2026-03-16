from email.mime import base
import time
import random
from codecarbon import EmissionsTracker
import tracemalloc
import pathlib
import csv

# diretorio do script src atual
src_dir = pathlib.Path(__file__).parent

# diretorio de saida dos resultados
saida_csv = src_dir / "outputs" / "resultados.csv"
saida_emissions = saida_csv.parent / "emissions.csv"

# salvar resultados de hashmap em csv
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

tracker.start()
tracemalloc.start()

# HASHMAP
hash_dict = {}
inicio = time.time()

# inserção
for i in range(100000):
    hash_dict[i] = i
# busca    
for i in range(50000):
    chave = random.randint(0, 99999)
    if chave in hash_dict:
        pass
# remoção        
for i in range(20000):
    chave = random.randint(0, 99999)
    hash_dict.pop(chave, None)

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

# print dos resultados terminal
print("Tempo de execução:", tempo_execucao, "segundos")
print("Memória atual usada:", memoria_atual / 10**6, "MB")
print("Pico de memória:", memoria_pico / 10**6, "MB")
print("Energia consumida:", f"{energia / 10**6:.12f}"  , "kWh")

# dados para salvar em csv
dados = {
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'estrutura': 'hash_map',
    'tempo_execucao': tempo_execucao,
    'memoria_atual_mb': memoria_atual / 10**6,
    'memoria_pico_mb': memoria_pico / 10**6,
    'energia_gasta_kwh': energia / 10**6,
    'tamanho_estrutura': len(hash_dict)
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

print(f"\ndados salvos em {saida_csv}")