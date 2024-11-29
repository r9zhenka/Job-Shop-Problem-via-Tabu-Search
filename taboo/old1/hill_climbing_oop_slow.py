import random
import json
from copy import deepcopy

class Task:
    def __init__(self, task_id, jobs):
        self.task_id = task_id
        self.jobs = jobs

    def __repr__(self):
        return f"Task({self.task_id}, jobs={self.jobs})"

class TaskManager:
    def __init__(self):
        self.tasks_dict = {}

    def add_task(self, task):
        self.tasks_dict[task.task_id] = task

    def get_tasks_dict(self):
        return self.tasks_dict

    def jobs(self):
        return list(self.tasks_dict.values())

    def __setitem__(self, key, value):
        self.tasks_dict[key] = value

    def __getitem__(self, key):
        return self.tasks_dict[key]

    def __repr__(self):
        return f"TaskManager({len(self.tasks_dict)} tasks)"

class Solution:
    def __init__(self, task_manager=None, makespan=0):
        self.task_manager = task_manager
        self.makespan = makespan

    def Makespan(self):
        if self.task_manager:
            machine_loads = {}
            for machine, tasks in self.task_manager.tasks_dict.items():
                total_time = sum(sum(task.jobs) for task in tasks)
                machine_loads[machine] = total_time
            self.makespan = max(machine_loads.values(), default=0)
            return self.makespan

    def GetNeighbor(self, max_iterations=10, num_machines=10):
        for _ in range(max_iterations):
            new_task_manager = deepcopy(self.task_manager)
            machine_lose = f'machine{random.choice(range(1, num_machines+1))}'

            if new_task_manager[machine_lose]:
                task = new_task_manager[machine_lose].pop(random.randint(0, len(new_task_manager[machine_lose])-1))
                machine_get = f'machine{random.choice(range(1, num_machines+1))}'
                new_task_manager[machine_get].append(task)
                new_solution = Solution(task_manager=new_task_manager)
                new_solution.Makespan()
                yield new_solution

    def create_random_solution(self, machines_number=10):
        if not self.task_manager:
            raise ValueError("TaskManager is not set for this solution.")
        machines = {f"machine{i+1}": [] for i in range(machines_number)}
        tasks = self.task_manager.jobs()
        for task in tasks:
            machine_key = random.choice(list(machines.keys()))
            machines[machine_key].append(task)
        self.task_manager.tasks_dict = machines

    def __str__(self):
        if self.task_manager:
            tasks_info = ", ".join(f"{k}: {len(v)} tasks" for k, v in self.task_manager.tasks_dict.items())
            return f"Solution with makespan={self.makespan}\nTasks distribution:\n{tasks_info}"
        else:
            return "Solution has no task_manager set."

def hill_climbing(tm: TaskManager, max_iterations=10**4, num_machines=10):
    solution = Solution(task_manager=tm)
    solution.create_random_solution()
    best_solution = deepcopy(solution)
    best_makespan = solution.Makespan()

    for _ in range(max_iterations):
        for neighbor in solution.GetNeighbor(max_iterations=10, num_machines=num_machines):
            if neighbor.makespan < best_makespan:
                best_solution = deepcopy(neighbor)
                best_makespan = neighbor.makespan
                break

    return best_solution, best_makespan

if __name__ == "__main__":
    tm = TaskManager()
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for key, value in data.items():
        tm.add_task(Task(task_id=key, jobs=value))

    sol, mk = hill_climbing(tm)
    print(sol, f'\nBest Makespan: {mk}')
