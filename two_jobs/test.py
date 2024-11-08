import os

from two_jobs import *
from google_solver import *

testsPath = "two_jobs/tests/"
if __name__ == "__main__":
    for filename in os.listdir(testsPath):
        try:
            file = open(testsPath + filename, 'r')
            jobsData = json.loads(file.read())["jobs_data"]
            file.close()

            solver = Solver(jobsData)
            print(filename, "Optimal", solver.Solve()[1], "Google", GoogleSolve(jobsData))

        except Exception as ex:
            print(filename, "Skipped due to", ex)
            continue
