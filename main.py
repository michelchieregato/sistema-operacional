import logging
from sistema.sistema_operacional import SistemaOperacional
import pandas as pd
import time

log_file = open('log_do_sistema.log', 'w')
logging.basicConfig(stream=log_file, level=logging.INFO)

sistema_operacional = SistemaOperacional()

print('Bem vindo ao sistema operacional...')
print('Lendo o arquivo jobs.csv')
instrucoes = pd.read_csv('./arquivos/jobs.csv')
clock = 0
encerrar = False
print('Sistema rodando...')
while not encerrar or not sistema_operacional.is_free():
    instrucoes_do_ciclo = instrucoes[instrucoes['Tempo da Acao'] == clock]
    for id_, row in instrucoes_do_ciclo.iterrows():
        if row['Acao'] == 'adicionar':
            sistema_operacional.adiciona_job(id_ + 1, row)
        elif row['Acao'] == 'deletar':
            sistema_operacional.remove_job(row)
        else:
            encerrar = True
    sistema_operacional.processa_ciclo()
    time.sleep(0.15)
    clock += 1

