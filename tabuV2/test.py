import os
import json

from tabu import *
from google_solver import *
from visualisation import Gantt, Comparison

testsPath = "tests/"
if __name__ == "__main__":
    # fileCount = len(os.listdir(testsPath))
    avg_deviation = []
    files_names = []
    benchmarks = []
    mksp = []
    # print(os.listdir(testsPath))
    for filename in os.listdir(testsPath):

        if filename.endswith(".json") and filename == "15.json":
            for iterations in [1, 3, 5, 10, 30, 75, 100, 150, 200]:
                print('-' * 20)
                try:
                    filename_local = filename + f" {iterations} iterations"
                    directory = "/statistic/iteration_tests"
                    file = open(testsPath + filename, 'r')
                    jobsData = json.loads(file.read())["jobs_data"]
                    file.close()
                    # iterations = 10000
                    tabuSetSize = 30
                    START_TIME = time.time()
                    tabu = TabuSearch(Solution.from_list(jobsData), iterations=iterations, tabuSetSize=tabuSetSize)
                    END_TIME = time.time()
                    mk = tabu.GetMakespan()
                    benchmark = GoogleSolve(jobsData)
                    Gantt(tabu.GetMachinesSchedule(), filename=filename_local, \
                          stats={'makespan': mk, 'time': round(END_TIME - START_TIME, 4), \
                                 'iterations': iterations, 'tabuSetSize': tabuSetSize}, \
                          benchmark_makespan= benchmark, directory=directory, show = True)
                    print(filename_local)
                    files_names.append(f"{iterations} iterations")
                    benchmarks.append(benchmark)
                    mksp.append(mk)
                    avg_deviation.append(round(mk / benchmark, 2))

                    # print("Operations", tabu.operations)
                    # print("Tabu", tabu.GetMakespan(), "Google", GoogleSolve(jobsData))
                except Exception as ex:
                    print(filename, "Skipped due to", ex)
                    continue

            Comparison(files_names, benchmarks, mksp, directory=directory, \
               stats = {'avg_deviation: ': f" + {(round((sum(avg_deviation)/len(avg_deviation) - 1)*100, 5))}%"}, \
               show = 1, xlabel="iterations", ylabel="makespan")