import random
import json
import os
num_jobs = 100
types_machines = ['CPU', 'GPU', 'QPU']

n_test_files = 10
folder_path = 'tests'
os.makedirs(folder_path, exist_ok=True)
for ind_file in range(1, n_test_files+1):
    whole_input = []
    for i in range(1, num_jobs+1):
        n_operations = 3                      # random.randint(1, 3)
        job = {}
        for j in range(n_operations):
            operation = (types_machines[j], (j, random.randint(1, 10))) #type = tuple
            if f'Job{i}' in job.keys():
                job[f'Job{i}'].append(operation)
            else:
                job[f'Job{i}'] = [operation]
        whole_input.append(job)
    file_path = os.path.join(folder_path, f'data_for_cl{ind_file}.json')
    with open(file_path, 'w') as file:
        json.dump(whole_input, file, indent=4)


# [{task1: [[Type_machine, [precedence, weight]]] - type Job} - type Task]