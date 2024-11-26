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
    def __init__(self, machines = None, job = None):
        super().__init__(self)
        self.machines = machines
        self.job = job

    def __str__(self):
        return f'{self.job, self.machines}'
    def __repr__(self):
        return self.__str__()

    def acceptable_machines(self):
        x = str(self.machines)
        CPU = [f'machine{x}' for x in range(1, 4)]
        GPU = [f'machine{x}' for x in range(4, 7)]
        MPU = [f'machine{x}' for x in range(7, 11)]
        # self.machines = self.machines.get_number()
        if x == 'CPU':
            return CPU
        elif x == 'GPU':
            return GPU
        elif x == 'MPU':
            return MPU
        # return self.machines
    def generator(self):
        type_of_machines = ['CPU', 'GPU', 'MPU']
        m = random.choice(type_of_machines)
        w = random.randint(1, 10)
        a = Job(machines=m, job = w)
        return a
    def cur_job(self):
        return self.job

class Task(dict):
    def __init__(self, dictionary = {}):
        super().__init__()
        self.list_of_jobs = list(dictionary.values())
        self.task_number = str(dictionary.keys()) #conv -> more than 1 tasks work incorrect
        # for i in range(len(list(dictionary.values())[0])): #можно создать переменные инициации для каждой работы списка?

    def __str__(self):
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
    def generator(self, n: int, *jobs):
        T = Task()
        T = Task({f'Task{n}': job for job in jobs})
        return T
    
    def List_of_jobs(self):
        all_jobs = []
        for keys, values in self.items():
            all_jobs.append(Job(keys, values))
        return self.list_of_jobs

class Machine_types:
    def __init__(self, name = None, efficiency = 1):
        # super().__init__()
        self.efficiency = efficiency
        self.name = name #'GPU' for example
        self.kind = None

    def is_acceptable(self, job: Job) -> bool:
        if self.name in job.acceptable_machines():
            return True
        else:
            return False
    def types(self):
        CPU = [Machine_types(f'machine{x}', x) for x in range(1, 4)]
        GPU = [Machine_types(f'machine{x}', x - 3) for x in range(4, 7)]
        MPU = [Machine_types(f'machine{x}', x - 6) for x in range(7, 11)]
        if str(self) in CPU:
            self.kind = CPU
        elif str(self) in GPU:
            self.kind = 'GPU'
        elif str(self) in MPU:
            self.kind = 'MPU'
        else:
            raise ValueError
        return self.kind

    def get_efficiency(self):
        # types(self)
        return self.efficiency
    def get_number(self):
        number = ''
        for i in str(self.name):
            if i.isdigit():
                number += i
        return int(number)

class Conveyer(dict):
    def __init__(self):
        # self.elements = elements
        super().__init__()
    # def __str__(self):
        # return f'{self.elements}'
    def add_element(self, task: Task):
        # self.add(task)
        return
class Solution(dict):
    def __init__(self):#, conv: Conveyer):
        self.query = {}
        return
    def __repr__(self):
        x = ''
        for i in range(1, 11):
            x += str(self[f'machine{i}']) + '\n'
        return x
        # return self.__str__()

    def get_makespan(self):
        max_makespan = 0
        for machine_name in self.keys():
            current_makespan = 0
            m_n = Machine_types(machine_name)
            for job in self[machine_name]:
                current_makespan += job.job
            current_makespan /= m_n.get_efficiency() ###Attention! Machine_name is str, so we use duplicate = Mach_types(mach_name)
            max_makespan = max(current_makespan, max_makespan)
        return max_makespan
    def get_neighbour(self):
        pass
    def conv_to_solution(self, conv: Conveyer):
        new_solution = Solution()
        n_s = [[] for _ in range(10)]
        mch = []
        for x in conv:
            for y in x.list_of_jobs[0]:
                m = Machine_types(random.choice(y.acceptable_machines())) #не все машины могут заполниться
                if m.name in new_solution.keys():
                    new_solution[m.name].append(y)
                else:
                    new_solution[m.name] = [y]
        return new_solution
    def create_random_solution(self, machines_list):
        # new_solution = [[for i in range(len(machines_list))]]
        new_solution = [[] for _ in range(10)]
        # check_list = lambda x:
        #
        for x in conv:
            # print(x)
            for i in range(len(x.list_of_jobs[0])):
                current_job = x.list_of_jobs[0][i]    # z.cur_job() - вес работы, z.acceptable_machines() - допустимые машины
                current_weight = current_job.cur_job()
                CAM = [current_job.acceptable_machines()]    #CAM - current acceptable machines
                # input()
                # print(CAM)
                # cur_machine_number = random.choice
                cur_machine_number = random.choice(CAM)
                new_solution[cur_machine_number].append(current_job)
        return new_solution
                

        return new_solution
def type_of_machines():
    x = CPU(name='machine1')
def generate_for_conv(num_machines = 10, num_tasks = 100):
    max_weight = 10
    conv = {}
    machines_types = ['CPU', 'GPU', 'MPU']
    for i in range(1, num_tasks+1):
        jobs_in_task = random.randint(1, 3)
        j = []
        for _ in range(jobs_in_task):
            weight = random.randint(1, max_weight)
            m_type = random.choice(machines_types)
            j.append(Job(job=weight, machines=m_type))
        conv[f'Task{i}'] = j.copy()
    return conv

if __name__ == '__main__':
    conv = Conveyer()
    n_tasks = 100
    tasks = []
    for n_task in range(n_tasks):
        T = Task()
        n_jobs = random.randint(1, 3)
        j = Job()
        x = []
        for i in range(n_jobs):
            x.append(j.generator())
        t = deepcopy(T.generator(n_task+1, x))
        # print(t)
        tasks.append(t)
    print(type(tasks[99]))
    print(tasks[99].list_of_jobs[0][0])#[0].acceptable_machines())
    s = Solution()
    print(s.conv_to_solution(tasks).get_makespan())
    
