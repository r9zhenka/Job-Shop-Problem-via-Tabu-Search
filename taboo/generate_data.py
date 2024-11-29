import random
import json

num_tasks = 100
types_machines = ['CPU', 'GPU', 'MPU']
whole_input = []
for i in range(1, num_tasks+1):
    n_jobs = random.randint(1, 3)
    task = {}
    for j in range(n_jobs):
        job = (random.choice(types_machines), random.randint(1, 10)) #type = tuple
        if f'Task{i}' in task.keys():
            task[f'Task{i}'].append(job)
        else:
            task[f'Task{i}'] = [job]
    whole_input.append(task)
with open('data_for_cl.json', 'w') as file:
    json.dump(whole_input, file, indent=4)
