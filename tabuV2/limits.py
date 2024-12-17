import os
import json
import matplotlib.pyplot as plt

from tabu import *
from google_solver import *


iterations = 20
tabuListSize = 5

testsPath = "tests/"
if __name__ == "__main__":
    for filename in os.listdir(testsPath):
        if not filename.endswith(".json"): continue
        try:
            file = open(testsPath + filename, 'r')
            jobsData = json.loads(file.read())["jobs_data"]
            file.close()

            tabu = TabuSearch(Solution.from_list(jobsData), iterations=iterations, tabuListSize=tabuListSize)
            benchmark = GoogleSolve(jobsData)
            print(filename, "Optimal", tabu.GetMakespan(), "Google", benchmark)

            plotX = [i for i in range(len(tabu.history))]
            plt.plot(plotX, [(hist - benchmark) / benchmark for hist in tabu.history])
            plt.plot(plotX, [0 for _ in range(len(tabu.history))])

        except Exception as ex:
            print(filename, "Skipped due to", ex)
            continue

    plt.show()
