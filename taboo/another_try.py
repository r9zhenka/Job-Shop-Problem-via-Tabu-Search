import random

from jo_sho_try import dick
from collections import defaultdict
from copy import deepcopy
import random
machines_number = 10
tasks_number = 100

def create_random_solution(d: dict, machines_number = machines_number, tasks_number = tasks_number):
    random_solution = defaultdict(list)
    for i in range(tasks_number):
        random_solution[f'machine{random.choice([_ for _ in range(1, 11)])}'].append(d.get(f'task{i+1}'))
    return random_solution

def max_value_of_dict(d: dict):
    max_ = 0
    # print(d)
    for key, value in d.items():
        # print(sum(sum(d[key], [])), '///////')
        if sum(sum(d[key], [])) > max_:
            max_ = sum(sum(d[key], []))
            max_key = key
    return (max_, key)

makespan = lambda x: max_value_of_dict(x)[0]

# print(makespan(create_random_solution(dick)))
def hill_climbing(max_iterations = 10**5, d = dick, num_machines = machines_number):
    cur_solution = create_random_solution(d)
    cur_makespan = makespan(cur_solution)
    mk_list = []
    for iteration in range(max_iterations):
        new_solution = deepcopy(cur_solution)
        machine_lose = f'machine{random.choice([_ for _ in range(1, 11)])}'

        if new_solution[machine_lose]:
            l_job = new_solution[machine_lose].pop(random.choice([_ for _ in range(len(new_solution[machine_lose]))]))
            machine_get = f'machine{random.choice([_ for _ in range(1, 11)])}'
            new_solution[machine_get].append(l_job)

        new_makespan = makespan(new_solution)
        if new_makespan < cur_makespan:
            cur_solution = new_solution
            cur_makespan = new_makespan
            print(f"Iteration {iteration + 1}, Makespan: {cur_makespan}")
            l_iter = iteration
        mk_list.append(cur_makespan)
        if iteration > 100 and len(set(mk_list[-50:])) <2:
            cur_solution = create_random_solution(d)

            # print('застрял', iteration)
            # break
            # print(set(mk_list[-200:]), mk_list[-200:])
    return cur_solution, cur_makespan, l_iter


if __name__ == '__main__':
    with open('data1.txt', 'r') as f:
        dick = eval(f.read())  # Загружаем задачи как словарь (используйте eval с осторожностью)

    num_machines = 10
    max_iterations = 100000
    best_solution, best_makespan, iter = hill_climbing(d = dick, num_machines=num_machines, max_iterations=max_iterations)
    print("Лучшее найденное решение:")
    print(best_solution)
    print("Мэйкспан:", best_makespan)
    print("iter", iter)


