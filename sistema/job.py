from enum import Enum

class EstadoJob(Enum):
    SUBMETIDO = 0
    ESPERANDO = 1
    PROCESSANDO = 2
    FINALIZADO = 3


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

    # Necessário para usar a FilaDePrioridade
    def __lt__(self, other):
        return self.prioridade < other.prioridade

    def __gt__(self, other):
        return self.prioridade > other.prioridade

    def __eq__(self, other):
        return self.id == other.id

    def implementar(self):
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
