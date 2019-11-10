from sistema.disco import Disco
from sistema.fila_prioridade import FilaDePrioridade
from sistema.job import Job
from sistema.memoria import Memoria


class SistemaOperacional:

    def __init__(self):
        self.memoria = Memoria()
        self.disco = Disco()
        self.jobs = FilaDePrioridade()

    def processa_ciclo(self):
        while not self.jobs.isEmpty():
            job = self.jobs.pop()
            self.memoria.aloca_job(job)

        for job in self.memoria.jobs_ativos:
            terminou = job.implementar()
            if terminou:
                self.memoria.remove_job(job.name)


    def adiciona_job(self, id_, row):
        nome = row['Nome Do Job']
        prioridade = int(row['Prioridade'])
        duracao = int(row['Duracao (CLKs)'])
        tamanho = int(row['Tamanho (Kbytes)'])
        arquivos = row['Arquivos']
        job = Job(id_, nome, tamanho, duracao, arquivos, prioridade)
        print('Acao de adicionar job recebida. Nome do Job: ', job.name)
        self.jobs.insert(job)

    def remove_job(self, row):
        self.memoria.remove_job(row['Nome Do Job'])

    def is_free(self):
        return len(self.memoria.jobs_ativos) == 0