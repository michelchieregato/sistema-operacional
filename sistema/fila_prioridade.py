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
            print(type(job.name))
            print(type(name))
            if job.name == name:
                self.queue.pop(i)
                return True
        return False

    # for popping an element based on Priority
    def pop(self):
        if not self.isEmpty():
            return self.queue.pop(0)
