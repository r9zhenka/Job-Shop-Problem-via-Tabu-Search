import collections
from ortools.sat.python import cp_model
# from classes import Task, Job

def GoogleSolve(jobs_data):
    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)
    # Computes horizon dynamically as the sum of all durations.
    horizon = sum(task[1] for job in jobs_data for task in job)

    # Create the model.
    model = cp_model.CpModel()

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple("task_type", "start end interval")
    # Named tuple to manipulate solution information.
    assigned_task_type = collections.namedtuple(
        "assigned_task_type", "start job index duration"
    )

    # Creates job intervals and add to the corresponding machine lists.
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine, duration = task
            suffix = f"_{job_id}_{task_id}"
            start_var = model.new_int_var(0, horizon, "start" + suffix)
            end_var = model.new_int_var(0, horizon, "end" + suffix)
            interval_var = model.new_interval_var(
                start_var, duration, end_var, "interval" + suffix
            )
            all_tasks[job_id, task_id] = task_type(
                start=start_var, end=end_var, interval=interval_var
            )
            machine_to_intervals[machine].append(interval_var)

    # Create and add disjunctive constraints.
    for machine in all_machines:
        model.add_no_overlap(machine_to_intervals[machine])

    # Precedences inside a job.
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.add(
                all_tasks[job_id, task_id + 1].start >= all_tasks[job_id, task_id].end
            )

    # Makespan objective.
    obj_var = model.new_int_var(0, horizon, "makespan")
    model.add_max_equality(
        obj_var,
        [all_tasks[job_id, len(job) - 1].end for job_id, job in enumerate(jobs_data)],
    )
    model.minimize(obj_var)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # print("Solution:")
        # Create one list of assigned tasks per machine.
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(
                        start=solver.value(all_tasks[job_id, task_id].start),
                        job=job_id,
                        index=task_id,
                        duration=task[1],
                    )
                )

        # Create per machine output lines.
        output = ""
        for machine in all_machines:
            # Sort by starting time.
            assigned_jobs[machine].sort()
            sol_line_tasks = "Machine " + str(machine) + ": "
            sol_line = "           "

            for assigned_task in assigned_jobs[machine]:
                name = f"job_{assigned_task.job}_task_{assigned_task.index}"
                # add spaces to output to align columns.
                sol_line_tasks += f"{name:15}"

                start = assigned_task.start
                duration = assigned_task.duration
                sol_tmp = f"[{start},{start + duration}]"
                # add spaces to output to align columns.
                sol_line += f"{sol_tmp:15}"

            sol_line += "\n"
            sol_line_tasks += "\n"
            output += sol_line_tasks
            output += sol_line
        # print('-------------')
        return int(solver.objective_value)
# @GoogleSolve
def adapter(file_name):

    CPU = (10/4, 4, 'CPU')
    GPU = (6/3, 3, 'GPU')
    MPU = (10/4, 4, 'MPU')
    with open(file_name, "r") as f:
        jobs_data = json.load(f)
        adapted_data = []
        for tasks in jobs_data:
            for task in tasks.values():
                adapted_task = []
                for job in task:
                    accept_machine = job[0]
                    weight = job[1]
                    okruglitel = random.randint(0,1)
                    if accept_machine == 'CPU':
                        accept_machine = 0
                        w = math.ceil(weight/CPU[0]/CPU[1])
                        adapted_task.append((accept_machine, w - okruglitel if w>1 else w))
                    elif accept_machine == 'GPU':
                        accept_machine = 1
                        w = math.ceil(weight/GPU[0]/GPU[1])
                        adapted_task.append((accept_machine, w - okruglitel if w>1 else w))
                    elif accept_machine == 'MPU':
                        accept_machine = 2
                        w = math.ceil(weight/MPU[0]/MPU[1])
                        adapted_task.append((accept_machine, w - okruglitel if w>1 else w))
                adapted_data.append(adapted_task)

        return adapted_data
import json
import math
import random
# from generate_data import n_test_files
# if __name__ == '__main__':
# # def
#     # n_test_files = 10
#     for i in range(1, n_test_files + 1):
#         file_name = f'tests/data_for_cl{i}.json'
#         with open(file_name, 'r') as f:
#
#             # x = json.load(f)
#             # print(x)
#             print(GoogleSolve(adapter(file_name)))
#             # print(adapter(x))