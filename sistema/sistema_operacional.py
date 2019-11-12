from sistema.arquivo import Arquivo
from sistema.disco import Disco
from sistema.fila_prioridade import FilaDePrioridade
from sistema.job import Job, IOException
from sistema.memoria import Memoria
import ast


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
            terminou = False
            try:
                terminou = job.implementar()
            except IOException:
                print('Chamada de IO para o JOB:')
                print(job)
                self.memoria.remove_job(job.name)
                self.disco.adiciona_job(job)
            if terminou:
                self.memoria.remove_job(job.name)

        if self.disco.ocupado:
            job_retornado = self.disco.realiza_io()
            if job_retornado is not None:
                job_retornado.prioridade = 4
                self.memoria.aloca_job(job_retornado)

    def adiciona_job(self, id_, row):
        nome = row['Nome Do Job']
        prioridade = int(row['Prioridade'])
        duracao = int(row['Duracao (CLKs)'])
        tamanho = int(row['Tamanho (Kbytes)'])
        nomes_de_arquivos = ast.literal_eval(row['Arquivos'])
        arquivos = []
        for key, value in self.disco.arquivos.items():
            if key in nomes_de_arquivos:
                arquivos.append(Arquivo(key, value))
        job = Job(id_, nome, tamanho, duracao, arquivos, prioridade)
        print('Acao de adicionar job recebida. Nome do Job: ', job.name)
        self.jobs.insert(job)

    def remove_job(self, row):
        self.memoria.remove_job(row['Nome Do Job'])

    def is_free(self):
        return len(self.memoria.jobs_ativos) == 0
