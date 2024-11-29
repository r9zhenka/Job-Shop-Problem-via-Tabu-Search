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
from json.decoder import JSONDecoder
import random
import time
import json


class Job(dict):
    def __init__(self, machines, weight):
        super().__init__(self)
        self.machines = machines
        self.weight = weight


    def __str__(self):
        return f'{self.weight, self.machines}'


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
        a = Job(m, w)
        return a


class Task(dict):
    def __init__(self, dictionary = {}):
        super().__init__()
        self.list_of_jobs = list(dictionary.values())
        self.task_number = str(dictionary.keys()) #conv -> more than 1 tasks work incorrect


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
        super().__init__()


    def add_element(self, task: Task):
        return


    @staticmethod
    def conv_to_solution(conv) -> 'Solution':
        new_solution = Solution()
        for x in conv:
            for y in x.list_of_jobs[0]:
                m = Machine_types(random.choice(y.acceptable_machines())) #не все машины могут заполниться
                if m.name in new_solution.keys():
                    new_solution[m.name].append(y)
                else:
                    new_solution[m.name] = [y]
        return new_solution
class Solution(dict):
    def __init__(self):
        self.query = {}
        return


    def __repr__(self):
        x = ''
        for i in range(1, 11):
            x += str(f'machine{i} has these {len(self[f'machine{i}'])} jobs: ') + str(self[f'machine{i}']) + '\n'
        return x


    def get_makespan(self):
        max_makespan = 0
        for machine_name in self.keys():
            current_makespan = 0
            m_n = Machine_types(machine_name)
            for job in self[machine_name]:
                current_makespan += job.weight
            current_makespan /= m_n.get_efficiency() ###Attention! Machine_name is str, so we use duplicate = Mach_types(mach_name)
            max_makespan = max(current_makespan, max_makespan)
        return max_makespan


    def get_neighbour(self, num_machine = 0):
        solution1 = deepcopy(self)
        if num_machine == 0:
            num_machine = random.choice(list(solution1.keys()))
        # m = random.choice(list(solution1.keys()))
        # я решил передавать номер машины,
        # чтобы с точностью пройти по всем
        m = num_machine
        job = random.choice(solution1[m])
        # new_m = random.choice(job.acceptable_machines()) # мы будем добавлять это задание ко всем \
        # доступным машинам и возвращать решение с наименьшим мэйкспаном
        solution1[m].remove(job)
        best_makespan = 10**5   # self.get_makespan()
        # best_solution =
        for x in job.acceptable_machines():
            #возможно, при m мы имеем наименьший мэйкспан. нужно ли исключать возможность холостого выхода?
            # я полагаю, что нужно искл, так как а!=сосед(а)
            # и полагая лучший_мэйкспан = 0, я также исключаю текущее решение
            if x!=m:
                solution1[x].append(job)
                cur_makespan = solution1.get_makespan()
                if cur_makespan < best_makespan:
                    best_solution = deepcopy(solution1)
                solution1[x].remove(job)

        return best_solution


    def get_list_of_neighbour(self):
        list_ = []

        for num_machine in self.keys():
            # частое копирование приводит к увеличению времени выполнения в 50 раз на 1000 итераций!
            solution1 = deepcopy(self)
            if len(self[num_machine]) == 0:
                continue
            # if num_machine == 0:
            #     num_machine = random.choice(list(solution1.keys()))

            # m = random.choice(list(solution1.keys()))
            # я решил передавать номер машины, \
            # чтобы с точностью пройти по всем
            m = num_machine
            job = random.choice(solution1[m])
            # new_m = random.choice(job.acceptable_machines()) # мы будем добавлять это задание ко всем \
            # доступным машинам и возвращать решение с наименьшим мэйкспаном
            solution1[m].remove(job)
            best_makespan = 10**5   # self.get_makespan()
            for x in job.acceptable_machines():
                #возможно, при m мы имеем наименьший мэйкспан. нужно ли исключать возможность холостого выхода?
                # я полагаю, что нужно искл, так как а!=сосед(а)
                # и полагая лучший_мэйкспан = 0, я также исключаю текущее решение
                if x!=m:
                    solution1[x].append(job)
                    list_.append(deepcopy(solution1))
                    solution1[x].remove(job)

        return list_


    @classmethod
    def conv_to_solution(cls, conv) -> 'Solution':
        new_solution = Solution()
        for x in conv:
            for y in x.list_of_jobs[0]:
                m = Machine_types(random.choice(y.acceptable_machines())) #не все машины могут заполниться
                if m.name in new_solution.keys():
                    new_solution[m.name].append(y)
                else:
                    new_solution[m.name] = [y]
        return new_solution


    def create_random_solution(self):
        new_solution = Solution()
        for x in self.values():
            for y in x:
                mch = random.choice(y.acceptable_machines())
                if mch in new_solution.keys():
                    new_solution[mch].append(y)
                else:
                    new_solution[mch] = [y]
        return new_solution


    @classmethod
    def from_json(cls, filename : str) -> 'Solution':
        file = open(filename, 'r')
        data = json.loads(file.read())
        file.close()

        tasks = []
        for n_task in data["jobs_data"]:
            tasks.append(Task(n_task))


        # ~create initial_solution - рандомно распределяем по всем машинам~
        return cls.conv_to_solution(tasks)



def timeit(func):
    """
    Decorator for measuring function's running time.
    """
    def measure_time(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        print("Processing time of %s(): %.2f seconds."
              % (func.__qualname__, time.time() - start_time))
        return result
    return measure_time


@timeit
def hill_climbing(solution = Solution(), iterations = 10**3):
    # solution1 = deepcopy(solution)
    # best_makespan = current_makespan = solution1.get_makespan()
    # iter = 'No changes'
    # for i in range(max_iterations):
    #     for each_machine in solution1.keys():
    #         new_sol = solution1.get_neighbour(each_machine)
    #         if new_sol.get_makespan() < best_makespan:
    #             solution1 = deepcopy(new_sol)
    #             best_makespan = new_sol.get_makespan()
    #             iter = i
    # return solution1, iter
    currentSolution = deepcopy(solution)
    bestSolution = deepcopy(currentSolution)

    # tabuSet = []  # set()

    for _ in range(iterations):
        neighbors = currentSolution.get_list_of_neighbour()
        bestNeighbor = None
        bestNeighborMakespan = float('inf')

        for neighbor in neighbors:

            neighborMakespan = neighbor.get_makespan()
            if neighborMakespan < bestNeighborMakespan:
                bestNeighbor = neighbor
                bestNeighborMakespan = neighborMakespan

        if bestNeighbor is None:
            break

        currentSolution = bestNeighbor

        if bestNeighbor.get_makespan() < bestSolution.get_makespan():
            bestSolution = bestNeighbor

    return bestSolution


@timeit
def Tabu_Search(iterations = 10**3, tabuSetSize = 10, initialSolution = Solution()):
    currentSolution = initialSolution
    bestSolution = currentSolution

    tabuSet =[] #set()

    for _ in range(iterations):
        neighbors = currentSolution.get_list_of_neighbour()
        bestNeighbor = None
        bestNeighborMakespan = float('inf')

        for neighbor in neighbors:
            if neighbor not in tabuSet:
                neighborMakespan = neighbor.get_makespan()
                if neighborMakespan < bestNeighborMakespan:
                    bestNeighbor = neighbor
                    bestNeighborMakespan = neighborMakespan

        if bestNeighbor is None:
            print("No non-tabu neighbors found, terminate the search")
            break

        currentSolution = bestNeighbor
        tabuSet.append(bestNeighbor)

        if len(tabuSet) > tabuSetSize:
            tabuSet.pop()

        if bestNeighbor.get_makespan() < bestSolution.get_makespan():
            bestSolution = bestNeighbor

    return bestSolution

def input_data(file_name = 'data_for_cl.json'):
    with open(file_name, 'r') as f:
        x = json.load(f)
        inp = []
        for task in x:
            for key, values in task.items():
                j = []
                for value in values:
                    j.append(Job(value[0], weight=value[1]))
                t = Task({key: deepcopy(j)})
                inp.append(t)
    s = Solution()
    output = s.conv_to_solution(inp)
    print(output.get_makespan())
    return output

if __name__ == '__main__':
    # print(input_data('data_for_cl.json'))
    x = input_data('data_for_cl.json')
    n_tasks = 100
    tasks = []
    mx = 1000
    hc = hill_climbing(x, iterations = mx)
    print(hc.get_makespan())
    ts = Tabu_Search(initialSolution = x, tabuSetSize = 10, iterations = mx)
    print(ts.get_makespan())
