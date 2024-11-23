# постановка задачи:
# нужно решить Job Shop Problem
# на вход подается словарь заданий
# каждое задание состоит из dict,
# в каждом dict Job сначала идет value = Job_weight
# (а если создать Job как dict{weight_job: acceptable_machines}
# и keys = list(acceptable_machines)
# Архитектура: {weight: acceptable_machines} \in Job \in Task \in Conveyer,
# \выходя из конвейера, распределяются по машинам
# conveyer = dict(Task1: list_of_jobs(dict(int(Weight1): list(acceptable_machines1)), \
# dict(int(Weight2): list(acceptable_machines2)), etc), Task2: list_of_jobs(...))
# Конвейер преобразуется в Solution (как выглядит?)
# class Job(dict):
# job.acceptable_machines() - возвращает список машин, на которых может быть выполнена эта работа
# job.cur_job() - возвращает значение веса работы
# Создание Job1: Jobik1 = Job(machines=Machines1, job=Weight1)
# class Task(dict):
# task.get_task_if() - возвращает номер задания ('Task1' -> int(1))
# task.List_of_jobs() - возвращает list(list(job1, job2, etc.)) Remember: job = {int(weight): list(acceptable_machines)}
# обратиться к job[1] Task1.List_of_jobs()[0][1], first parametr of Task1.List...() is always [0]!!!
# class Machine_types:
#
# где реализовать проверку на допустимость выполнения работы Х на машине У?
from copy import deepcopy
import random
import json
from copy import deepcopy
import random
class Job:
    def __init__(self, machines, job):
        self.machines = machines
        self.job = job
    def __str__(self):
        return f'{self.job, self.machines}'
    def __repr__(self):
        return self.__str__()

    def acceptable_machines(self):
        return self.machines

    def cur_job(self):
        return self.job

class Task(dict):
    def __init__(self, dictionary):
        # super().__init__()
        self.list_of_jobs = list(dictionary.values())
        self.task_number = str(dictionary.keys())
        # for i in range(len(list(dictionary.values())[0])): #можно создать переменные инициации для каждой работы списка?

    def __str__(self):
        # key = [key for key, values in self.items()]
        # values = [values for key, values in self.items()]
        return f'{self.task_number, self.list_of_jobs}'
    def get_task_id(self):
        for keys, values in self.items():
            # x = keys
            self.task_number = keys
        id_=''
        for i in str(self.task_number):
            if i.isdigit():
                id_+=i

        return int(id_)

        # self.task_number = x
        # return type(self.task_number)
    def List_of_jobs(self):

        return self.list_of_jobs

class Machine_types:
    def __init__(self, name, efficiency):
        self.efficiency = efficiency
        self.name = name #'GPU' for example
    def get_efficiency(self):
        return self.efficiency

class Conveyer(list):
    def __init__(self):
        # self.elements = elements
        super().__init__()

        return
    # def __str__(self):
        # return f'{self.elements}'
    def add_element(self, task: Task):
        self.append(task)
        return
class Solution:
    def __init__(self, conv: Conveyer):
        return
    def __repr__(self):
        return
        # return self.__str__()
    def create_random_solution(self):
        for x in conv:
            new_solution = 1
        return new_solution


if __name__ == '__main__':
    Machines1 = ['machine1', 'machine2', 'machine3', 'machine4', 'machine5']
    Weight1 = 8
    Jobik1 = Job(machines=Machines1, job=Weight1)
    Weight2 = 10
    Machines2 = ['machine6', 'machine7']
    Jobik2 = Job(machines=Machines2, job=Weight2)
    Task1 = Task({'Task1': [Jobik1, Jobik2]})
    for_conveyer = (Task1)
    conv = Conveyer()
    conv.add_element(Task1)
    # print(conv)
    print(Task1.List_of_jobs()[0][1])
    # print(Task1)
