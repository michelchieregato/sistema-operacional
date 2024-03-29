class FilaDePrioridade(object):

    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def isEmpty(self):
        return len(self.queue) == 0

    def insert(self, data, in_top=False):
        if in_top:
            self.queue.insert(0, data)
        else:
            for i in range(len(self.queue)):
                if data > self.queue[i]:
                    self.queue.insert(i, data)
                    return
            self.queue.append(data)

    def remove_by_name(self, name):
        for i, job in enumerate(self.queue):
            print('Job', job)
            print('Nome do job', job.name)
            if job.name == name:
                self.queue.pop(i)
                return True
        return False

    # for popping an element based on Priority
    def pop(self):
        if not self.isEmpty():
            return self.queue.pop(0)


def find_sub_list(espacos, sl):
    """
    Procura pela primeira sequencia de zeros do tamanho do job
    """
    results = []
    sll = len(sl)
    for ind in (i for i, e in enumerate(espacos) if e == sl[0]):
        if espacos[ind:ind + sll] == sl:
            return ind, ind + sll - 1
    return results