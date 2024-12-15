import os
import json

from tabu import *
from google_solver import *
from visualisation import Gantt, Comparison

testsPath = "tests/test_on_dims/"
if __name__ == "__main__":
    fileCount = len(os.listdir(testsPath))
    avg_deviation = []
    files_names = []
    benchmarks = []
    mksp = []
    # print(os.listdir(testsPath))
    for filename in os.listdir(testsPath):
        # filename = str(i) + ".json"
        print('-' * 20)
        try:
            file = open(testsPath + filename, 'r')
            jobsData = json.loads(file.read())["jobs_data"]
            file.close()
            iterations = 100
            tabuSetSize = 30
            START_TIME = time.time()
            tabu = TabuSearch(Solution.from_list(jobsData), iterations=iterations, tabuSetSize=tabuSetSize)
            END_TIME = time.time()
            mk = tabu.GetMakespan()
            benchmark = GoogleSolve(jobsData)
            Gantt(tabu.GetMachinesSchedule(), filename=filename, \
                  stats={'makespan': mk, 'time': round(END_TIME - START_TIME, 4), \
                         'iterations': iterations, 'tabuSetSize': tabuSetSize}, \
                  benchmark_makespan= benchmark)
            print(filename)
            files_names.append(filename)
            benchmarks.append(benchmark)
            mksp.append(mk)
            avg_deviation.append(round(mk / benchmark, 2))

            # print("Operations", tabu.operations)
            # print("Tabu", tabu.GetMakespan(), "Google", GoogleSolve(jobsData))
        except Exception as ex:
            print(filename, "Skipped due to", ex)
            continue

    Comparison(files_names, benchmarks, mksp, {'avg_deviation: ': f" + {(round((sum(avg_deviation)/len(avg_deviation) - 1)*100, 5))}%"})