from copy import deepcopy
from json.decoder import JSONDecoder
import random
import time
import json
# [{Job: [[Type_ind, [precedence, weight]]] - type Operation} - type Job]
# class Operation(dict):
class Operation:
    def __init__(self, machines: list, job_id: int, precedence: int, weight: int):
        # super().__init__(self)
        self.machines = machines
        self.weight = weight
        self.precedence = precedence
        self.job = job_id

    def __str__(self):
        return f'{self.job, self.weight, self.machines}'
    def __repr__(self):
        return self.__str__()
    def acceptable_machines(self):
        x = str(self.machines)
        CPU = [f'machine{x}' for x in range(1, 4)]
        GPU = [f'machine{x}' for x in range(4, 7)]
        QPU = [f'machine{x}' for x in range(7, 11)]
        # self.machines = self.machines.get_number()
        if x == 'CPU':
            return CPU
        elif x == 'GPU':
            return GPU
        elif x == 'QPU':
            return QPU

class Job(dict):
    def __init__(self, dictionary = {}):
        super().__init__()
        self.list_of_operations = dictionary.values()
        self.job_number = str(dictionary.keys()) #conv -> more than 1 tasks work incorrect


    def __str__(self):
        return f'{self.job_number, self.list_of_operations}'


    def get_job_id(self):
        for keys, values in self.items():
            # x = keys
            self.job_number = keys
        id_=''
        for i in str(self.job_number):
            if i.isdigit():
                id_+=i

        return int(id_)


    # def generator(self, n: int, *operations):
    #     J = Job()
    #     J = Job({f'Job{n}': op for op in operations})
    #     return T


    def List_of_operations(self):
        all_operations = []
        for keys, values in self.items():
            job = keys.get_task_id()
            for value in values:
                # num_mach = keys.get_task_id()
                # value.weight = value
                op = Operation()
                op.num_mach = value[0]
                op.precedence, op.weight = value[1][:]   #?????
                all_operations.append(op)
        return self.list_of_operations

class Machine_types:
    def __init__(self, kind = None, efficiency = 1):
        # super().__init__()
        self.efficiency = efficiency
        self.name = None
        self.kind = kind #'GPU' for example


    def is_acceptable(self, operation: Operation) -> bool:
        if self.name in operation.acceptable_machines():
            return True
        else:
            return False

class Solution(dict):
    def __init__(self):
        self.query = {}
        return


    def __repr__(self):
        x = ''
        for i in range(1, 11):
            x += str(f'machine{i} has these {len(self[f'machine{i}'])} operations: ') + str(self[f'machine{i}']) + '\n'
        return x

    #не учитывает пустоты
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
        for job in conv:
            job = Job()
            # for y in job.list_of_operations[0]:
            for operation in job.List_of_operations():
                # тут уже важно, чтобы выполнялась прецеденция + решение принималось в виде матрицы времени
                m = Machine_types(random.choice(operation.acceptable_machines())) #не все машины могут заполниться
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

def Tabu_Search(iterations = 10**3, tabuSetSize = 10, initialSolution = Solution()):
    currentSolution = initialSolution
    bestSolution = currentSolution

    tabuSet = [] #set()

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
            # print("No non-tabu neighbors found, terminate the search")
            break

        currentSolution = bestNeighbor
        tabuSet.append(bestNeighbor)

        if len(tabuSet) > tabuSetSize:
            tabuSet.pop()

        if bestNeighbor.get_makespan() < bestSolution.get_makespan():
            bestSolution = bestNeighbor

    return bestSolution

# if __name__ == '__main__':

    # for i in range(1, n_test_files+1):
    #     print(f'\nfile{i}')
    #     file_name = f'tests/data_for_cl{i}.json'
    #     x = input_data(file_name)
    #     start_res = x.get_makespan()
    #     mx = 1000
    #     hc = hill_climbing(x, iterations = mx)
    #     hc_res = hc.get_makespan()
    #     ts = Tabu_Search(initialSolution = x, tabuSetSize = 100, iterations = mx)
    #     ts_res = ts.get_makespan()
    #     # gs_res = GoogleSolve(adapter(file_name))
    #     with open('results.txt', 'a', encoding='utf-8') as f:
    #         f.write(f'\nfile: {file_name}\n \
    #                 Start {start_res}\n \
    #                 Hill_climbing {hc_res}\n \
    #                 Tabu Search {ts_res}\n \
    #                 Google solver {gs_res}')