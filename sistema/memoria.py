from enum import Enum

from sistema.fila_prioridade import FilaDePrioridade, find_sub_list
from sistema.job import EstadoJob

TAMANHO_TOTAL = 1000
ESPACO_LIVRE = 0


class Memoria:
    """
    Representa a memoria do sistema. Ela tem um tamanho de TAMANHO_TOTAL.
    Ela é representada por um vetor, com espacos (ocupados ou não).
    """

    def __init__(self):
        self.espacos_de_memoria = [ESPACO_LIVRE] * TAMANHO_TOTAL
        self.espacos_ocupados = {}
        self.jobs_ativos = []
        self.fila_de_espera = FilaDePrioridade()

    def _remove_job_ativo(self, job_name):
        self.jobs_ativos = [*filter(lambda x: x.name != job_name, self.jobs_ativos)]

    def aloca_job(self, job, in_top=False):
        """
        Tenta alocar job na fila. Se o job não cabe na memória, coloca-o na fila.
        """
        espaco_necessario = [ESPACO_LIVRE] * job.tamanho
        indices_da_memoria = find_sub_list(self.espacos_de_memoria, espaco_necessario)
        if indices_da_memoria:
            print('Alocando job {} na memória, nas posicoes de {} a {}'.format(job.name, indices_da_memoria[0], indices_da_memoria[0]))
            self.espacos_ocupados[job.name] = indices_da_memoria
            self.jobs_ativos.append(job)
            for i in range(*indices_da_memoria):
                self.espacos_de_memoria[i] = job.id
            print('Alocado!')
            print('\n###################################### ESTADO DA MEMORIA #########################################')
            self.mostra_jobs()
            print(self)
        else:
            # Significa que não tem espaco livre na espacos_de_memoria
            # Coloca o job na fila de espera
            # Se in_top = False, coloca na fila de acordo com sua prioridade, indo para o final dela
            # Se in_top = True, coloca de novo no topo, para ser o proximo a ser retirado.
            print('Job não cabe na memória!')
            print('Alocando job {} na fila de espera da memória'.format(job.name))
            job.estado = EstadoJob.ESPERANDO
            self.fila_de_espera.insert(job, in_top)
            print('Alocado!')
            self.mostra_jobs()

    def remove_job_da_memoria(self, job_name):
        if job_name not in self.espacos_ocupados:
            print('Erro! Job não está na memória')
            return

        indices_da_memoria = self.espacos_ocupados.pop(job_name)
        self._remove_job_ativo(job_name)
        print('Removendo job {} da memória. Liberando as posicoes de {} a {}'.format(job_name, indices_da_memoria[0],
                                                                          indices_da_memoria[0]))

        for i in range(*indices_da_memoria):
            self.espacos_de_memoria[i] = ESPACO_LIVRE

        if not self.fila_de_espera.isEmpty():
            job = self.fila_de_espera.pop()
            self.aloca_job(job, in_top=True)

    def remove_job(self, name):
        removeu_da_fila = self.fila_de_espera.remove_by_name(name)
        if not removeu_da_fila:
            self.remove_job_da_memoria(name)

    def mostra_jobs(self):
        print('Jobs na fila da memória, por ordem:')
        for job in self.fila_de_espera.queue:
            print(job)
        print('\nJobs na memória, e posicoes que ocupam:')
        for key, value in self.espacos_ocupados.items():
            print('Job {}:'.format(key))
            print('\tPosicoes: [{}, {}]'.format(value[0], value[1]))

    def __str__(self):
        message = ''
        colunas = 10
        linhas = len(self.espacos_de_memoria) // colunas

        for linha in range(linhas):
            message += '['
            message += '] ['.join(map(lambda x: str(x).zfill(3), self.espacos_de_memoria[linha * colunas: (linha + 1) * colunas]))
            message += ']\n'
        return message
