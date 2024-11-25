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
# пока получается, что работы из разных тасков будут перемешиваться
from copy import deepcopy
import random
import json
class Job(dict):
    def __init__(self, machines, job):
        super().__init__(self)
        self.machines = machines
        self.job = job
    def __str__(self):
        return f'{self.job, self.machines}'
    def __repr__(self):
        return self.__str__()

    def acceptable_machines(self):
        self.machines = self.machines.get_number()
        return self.machines

    def cur_job(self):
        return self.job

class Task(dict):
    def __init__(self, dictionary):
        super().__init__()
        self.list_of_jobs = list(dictionary.values())
        self.task_number = str(dictionary.keys()) #conv -> more than 1 tasks work incorrect
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
        all_jobs = []
        for keys, values in self.items():
            all_jobs.append(Job(keys, values))
        return self.list_of_jobs

class Machine_types:
    def __init__(self, name, efficiency):
        self.efficiency = efficiency
        self.name = name #'GPU' for example
    def get_efficiency(self):
        return self.efficiency

    def is_acceptable(self, job: Job) -> bool:
        if self.name in job.acceptable_machines():
            return True
        else:
            return False
    def get_number(self):
        # for keys, values in self.items():
        #     # x = keys
        #     self.task_number = keys
        number = ''
        for i in str(self.name):
            if i.isdigit():
                number += i

        return int(number)
class CPU(Machine_types): #нужно ли делать классы для каждой машины?
    pass
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
        return f'...'
        # return self.__str__()
    def a(self, cam):
        list_acceptable_machines = []

    def create_random_solution(self, machines_list):
        # new_solution = [[for i in range(len(machines_list))]]
        new_solution = [[] for _ in range(10)]
        # check_list = lambda x:
        for x in conv:
            # print(x)
            for i in range(len(x.list_of_jobs[0])):
                current_job = x.list_of_jobs[0][i]    # z.cur_job() - вес работы, z.acceptable_machines() - допустимые машины
                current_weight = current_job.cur_job()
                CAM = [current_job.acceptable_machines()]    #CAM - current acceptable machines
                # input()
                print(CAM)
                # cur_machine_number = random.randint(1, 10)

                cur_machine_number = random.choice(CAM)
                new_solution[cur_machine_number].append(current_job)
                # cur_machine_number = cur_machine_number.get_number()
                # new_solution[cur_machine_number].append(random.choice(CAM))
            # чтобы работы из разных тасков не сливались, здесь нужен разделитель
        # for keys, values in z:
                # print(str(keys), values.list_of_jobs)
                # new_solution.append(values[0][0])
                # print(values[0][0])
                # print(keys, values)
                # a=1

        return new_solution


if __name__ == '__main__':
    Machines1 = ['machine1', 'machine2', 'machine3', 'machine4', 'machine5'] #создавать так машины нельзя! их нужно делать как Machines3!
    Weight1 = 8
    Jobik1 = Job(machines=Machines1, job=Weight1)
    Weight2 = 10
    Machines2 = ['machine6', 'machine7']
    Jobik2 = Job(machines=Machines2, job=Weight2)
    Task1 = Task({'Task1': [Jobik1, Jobik2]})
    Jobik3 = Job(machines=Machines2, job=Weight1)
    Task2 = Task({'Task2': [Jobik3]})

    Machines3 = Machine_types(name='machine1', efficiency=0.8)
    Jobik33 = Job(machines=Machines3, job=Weight1)
    Task3 = Task({'Task3': [Jobik33]})
    # for_conveyer = (Task1)
    conv = Conveyer()
    print(Machines3.get_number())

    # machines_list = ['machine1', 'machine2', 'machine3', 'machine4', 'machine5',\
    #                  'machine6', 'machine7', 'machine8', 'machine9', 'machine10']
    machines_list = [Machines3]
    # можно попробовать сделать лист всех
    # машин как сет машин для всех заданных тасков
    conv.add_element(Task3)
    # conv.add_element(Task2)
    sol = Solution(conv)
    x = sol.create_random_solution(machines_list)
    # print(x)
    # print(conv)
    # print(Task1.List_of_jobs()[0][1])
    # print(Task1)
