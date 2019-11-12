from sistema.fila_prioridade import FilaDePrioridade, find_sub_list
from sistema.job import Job, EstadoJob

TAMANHO_TOTAL = 10000


class Disco:

    def __init__(self):
        self.espacos_de_memoria = [0] * TAMANHO_TOTAL
        self.fila_de_espera = FilaDePrioridade()
        self.espacos_ocupados = {}
        self.tempo_para_terminar_acesso = 0
        self.job_ativo = None
        self.arquivos = {}

    @property
    def ocupado(self):
        return self.job_ativo is not None

    def adiciona_arquivos(self, arquivo):
        espaco_necessario = [0] * arquivo.tamanho
        indices_da_memoria = find_sub_list(self.espacos_de_memoria, espaco_necessario)
        if indices_da_memoria:
            self.espacos_ocupados[arquivo.name] = indices_da_memoria
            self.arquivos[arquivo.name] = arquivo.tamanho
            for i in range(*indices_da_memoria):
                self.espacos_de_memoria[i] = 1
            print('Arquivo Adicionado!')
            print(self)

    def acesso_valido(self, job):
        for arquivo in job.acessos_de_arquivos:
            if arquivo.name not in self.espacos_ocupados.keys():
                return False
        return True

    def adiciona_job(self, job: Job):
        if not self.ocupado:
            self.job_ativo = job
            arquivo = self.job_ativo.acessos_de_arquivos.pop()
            self.tempo_para_terminar_acesso = arquivo.tamanho // 10
        else:
            self.fila_de_espera.insert(job)

    def realiza_io(self):
        self.tempo_para_terminar_acesso -= 1
        print('Realizando I/O!! Job {}, faltando {} ciclos'.format(self.job_ativo.name, self.tempo_para_terminar_acesso))
        if self.tempo_para_terminar_acesso <= 0:
            job = self.job_ativo
            job.estado = EstadoJob.SUBMETIDO
            self.job_ativo = None
            if not self.fila_de_espera.isEmpty():
                novo_job = self.fila_de_espera.pop()
                self.adiciona_job(novo_job)
            return job

    def __str__(self):
        message = '\n###################################### ESTADO DO DISCO #########################################'
        message += '\nJobs na fila, por ordem:\n'
        for job in self.fila_de_espera.queue:
            message += str(job)
        message += '\nArquivos na memória, e posicoes que eles ocupam:\n'
        for key, value in self.espacos_ocupados.items():
            message += 'Job {}:\n'.format(key)
            message += '\tPosicoes: [{}, {}]'.format(value[0], value[1])
        return message
