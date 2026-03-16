import time
import random
from codecarbon import EmissionsTracker
import tracemalloc
import csv
import pathlib

# diretorio do script src atual
src_dir = pathlib.Path(__file__).parent

# diretorio de saida dos resultados
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

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    # inserção    
    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    # busca 
    def search(self, value):
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False
    # remoção 
    def remove(self, value):
        current = self.head
        prev = None

        while current:
            if current.data == value:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False
# config do tracker de emissões    
tracker = EmissionsTracker(
    output_dir=str(src_dir / "outputs"),  # muda diretório do tracker
    output_file="emissions.csv"
)
# inicia o tracker e tracemalloc para medir memória
tracker.start()
tracemalloc.start()

# teste de desempenho da linked list
lista = LinkedList()
inicio = time.time()
# inserção 
for i in range(100000):
    lista.insert(i)
# busca  
for i in range(50000):
    valor = random.randint(0, 99999)
    lista.search(valor)
# remoção 
for i in range(20000):
    lista.remove(i)

# fim do teste e cálculo de tempo
fim = time.time()

# tempo de execução
tempo_execucao = fim - inicio

# emissões de CO2
emissoes = tracker.stop()

# energia total usada
energia = tracker._total_energy.kWh

# memória atual e pico de memória
memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

# print dos resultados no terminal
print("Tempo de execução:", tempo_execucao, "segundos")
print("Memória atual usada:", memoria_atual / 10**6, "MB")
print("Pico de memória:", memoria_pico / 10**6, "MB")
print("Energia consumida:", f"{energia / 10**6:.12f}"  , "kWh")

# calcula tamanho da lista encadeada
size = 0
cur = lista.head
while cur:
    size += 1
    cur = cur.next

# dados para salvar em csv
dados = {
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'estrutura': 'linked_list',
    'tempo_execucao': tempo_execucao,
    'memoria_atual_mb': memoria_atual / 10**6,
    'memoria_pico_mb': memoria_pico / 10**6,
    'energia_gasta_kwh': energia,
    'tamanho_estrutura': size
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

print("\nresultados salvos em resultados.csv")