import os
import json

from two_jobs import *
from google_solver import *

testsPath = "tests/"
if __name__ == "__main__":
    fileCount = len(os.listdir(testsPath))
    for i in range(fileCount):
        # if i != 1: continue

        filename = str(i) + ".json"

        try:
            file = open(testsPath + filename, 'r')
            jobsData = json.loads(file.read())["jobs_data"]
            file.close()

            solver = Solver(jobsData)
            print(filename, "Optimal", solver.Solve()[1], "Google", GoogleSolve(jobsData))

        except Exception as ex:
            print(filename, "Skipped due to", ex)
            continue
