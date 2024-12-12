import os
import json

from tabu import *
from google_solver import *


testsPath = "tests/"
if __name__ == "__main__":
    fileCount = len(os.listdir(testsPath))
    for i in range(fileCount):
        if i > 10: break

        filename = str(i) + ".json"

        try:
            file = open(testsPath + filename, 'r')
            jobsData = json.loads(file.read())["jobs_data"]
            file.close()

            tabu = TabuSearch(Solution.from_list(jobsData)).GetMakespan()
            print(filename, "Tabu", tabu, "Google", GoogleSolve(jobsData))

        except Exception as ex:
            print(filename, "Skipped due to", ex)
            continue
