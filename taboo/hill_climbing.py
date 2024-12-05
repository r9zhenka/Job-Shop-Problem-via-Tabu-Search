#another_try.py
from jo_sho_try import dick
from collections import defaultdict
from copy import deepcopy
import json
import random

class hill_climbing_method(dict):
    def __init__(self):
        super().__init__()
        self.machines_number = 10
        self.tasks_number = 100
    def crs(self, d, machines_number = 10, tasks_number = 100):
        self.clear()  
        for i in range(machines_number):
            machine_key = f'machine{i+1}'
            self[machine_key] = []
            
        for i in range(tasks_number):
            machine_key = f'machine{random.choice(range(1, machines_number + 1))}'
            self[machine_key].append(d.get(f'task{i + 1}'))
          
        return self  #
    def create_random_solution(self, machines_number = 10, tasks_number = 100):
        
        d = deepcopy(self)
        self.clear()  #
        for i in range(tasks_number):
            machine_key = f'machine{random.choice(range(1, machines_number + 1))}'
            if machine_key not in self:
                self[machine_key] = []
            self[machine_key].append(d.get(f'task{i + 1}'))
        return self

    def max_value_of_dict(self):
        max_ = 0
        # print(d)
        for key, value in self.items():
            # print(key, value)
            m_load = sum(sum(self[key], []))
            if m_load > max_:
                max_ = m_load
                max_key = key
        return (max_, max_key)

    def makespan(self):
        return self.max_value_of_dict()[0]

    def hill_climbing(self, data, max_iterations=10 ** 5, num_machines = 10):
        d = self.crs(data)
        cur_solution = deepcopy(d)

        cur_makespan = cur_solution.makespan()
        mk_list = []
        for iteration in range(max_iterations):
            new_solution = deepcopy(cur_solution)
            machine_lose = f'machine{random.choice([_ for _ in range(1, 11)])}'

            try:
                if new_solution[machine_lose]:
                    l_job = new_solution[machine_lose].pop(random.choice([_ for _ in range(len(new_solution[machine_lose]))]))
                    machine_get = f'machine{random.choice([_ for _ in range(1, 11)])}'
                    new_solution[machine_get].append(l_job)
            except:
                print(machine_lose, new_solution)
                ...

            new_makespan = new_solution.makespan()
            if new_makespan < cur_makespan:
                cur_solution = new_solution
                cur_makespan = new_makespan
                print(f"Iteration {iteration + 1}, Makespan: {cur_makespan}")
                l_iter = iteration
            mk_list.append(cur_makespan)
            if iteration > 100 and len(set(mk_list[-100:])) < 2:
                cur_solution = self.crs(data)
               

        return cur_solution, cur_makespan, l_iter


if __name__ == '__main__':
    with open('data.json', 'r') as f:
        data = json.load(f)
    input_data = hill_climbing_method()
    input_data.crs(d = data)
    print(input_data)
    num_machines = 10
    max_iterations = 10000
    best_solution, best_makespan, iter = input_data.hill_climbing(data, num_machines=num_machines, max_iterations=max_iterations)
    print("best_solution:")
    print(best_solution)
    print("makespan:", best_makespan)
    print("iter", iter)


