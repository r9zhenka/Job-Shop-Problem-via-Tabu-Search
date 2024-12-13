import os
import json

from tabu import *
from google_solver import *
from visualisation import Gantt

testsPath = "tests/"
if __name__ == "__main__":
    fileCount = len(os.listdir(testsPath))
    for i in range(10, 15):
        filename = str(i) + ".json"
        print('-' * 20)
        try:
            file = open(testsPath + filename, 'r')
            jobsData = json.loads(file.read())["jobs_data"]
            file.close()
            START_TIME = time.time()
            tabu = TabuSearch(Solution.from_list(jobsData))
            END_TIME = time.time()
            print(filename)
            # print("Operations", tabu.operations)
            # print("Tabu", tabu.GetMakespan(), "Google", GoogleSolve(jobsData))
            Gantt(tabu.GetMachinesSchedule(), filename=filename, \
                  stats={'makespan': tabu.GetMakespan(), 'time': round(END_TIME - START_TIME, 5)}, benchmark_makespan=GoogleSolve(jobsData))
        except Exception as ex:
            print(filename, "Skipped due to", ex)
            continue
