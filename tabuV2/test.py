import os
import json

from tabu import *
from google_solver import *


testsPath = "tests/"
if __name__ == "__main__":
    fileCount = len(os.listdir(testsPath))
    for i in range(fileCount):
        filename = str(i) + ".json"
        print('-' * 20)
        try:
            file = open(testsPath + filename, 'r')
            jobsData = json.loads(file.read())["jobs_data"]
            file.close()

            tabu = TabuSearch(Solution.from_list(jobsData))
            print(filename)
            print("Operations", tabu.operations)
            print("Tabu", tabu.GetMakespan(), "Google", GoogleSolve(jobsData))

        except Exception as ex:
            print(filename, "Skipped due to", ex)
            continue
