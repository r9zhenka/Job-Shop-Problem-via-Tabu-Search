import random
import json
import os
num_tasks = 100
types_machines = ['CPU', 'GPU', 'MPU']
whole_input = []
n_test_files = 10
folder_path = 'tests'
os.makedirs(folder_path, exist_ok=True)
for ind_file in range(1, n_test_files+1):
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
    file_path = os.path.join(folder_path, f'data_for_cl{ind_file}.json')
    with open(file_path, 'w') as file:
        json.dump(whole_input, file, indent=4)
