from enum import Enum
from random import randint


class EstadoJob(Enum):
    SUBMETIDO = 0
    ESPERANDO = 1
    PROCESSANDO = 2
    IO = 3
    FINALIZADO = 4


class IOException(Exception):
    """
    Caso o job necessite de uma operacão de I/O, ele
    """

    def __init__(self):
        super().__init__('Foi realizado um pedido de IO.')


class Job:

    def __init__(self, job_id, job_name, tamanho, tempo_maximo, acessos_de_arquivos, prioridade=0):
        self.id = job_id
        self.name = job_name
        self.tamanho = tamanho
        self.tempo_maximo = tempo_maximo
        self.acessos_de_arquivos = acessos_de_arquivos
        self.estado = EstadoJob.SUBMETIDO
        self.prioridade = prioridade
        self.ciclo = 0
        self.momentos_de_interrupcao = []

        for arquivo in acessos_de_arquivos:
            self.momentos_de_interrupcao.append(randint(0, self.tamanho))

    # Necessário para usar a FilaDePrioridade
    def __lt__(self, other):
        return self.prioridade < other.prioridade

    def __gt__(self, other):
        return self.prioridade > other.prioridade

    def __eq__(self, other):
        return self.id == other.id

    def _retira_momento(self):
        self.momentos_de_interrupcao = [*filter(lambda x: x != self.ciclo, self.momentos_de_interrupcao)]

    def _verifica_interrupcao(self):
        if self.ciclo in self.momentos_de_interrupcao:
            self.estado = EstadoJob.IO
            self._retira_momento()


    def implementar(self):
        self._verifica_interrupcao()

        if self.estado == EstadoJob.IO:
            raise IOException

        print('Processando job {} no ciclo {} de {}'.format(self.name, self.ciclo, self.tempo_maximo))
        self.ciclo += 1
        if self.ciclo == self.tempo_maximo:
            print('Job {} finalizado'.format(self.name))
            self.estado = EstadoJob.FINALIZADO
            return True
        return False

    def __str__(self):
        message = 'Job: {}, Id: {}, Tamanho: {}, Prioridade: {}'.format(self.name, self.id,
                                                                        self.tamanho, self.prioridade)
        return message
