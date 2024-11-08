import os

from two_jobs import *
from google_solver import *


if __name__ == "__main__":
    for filename in os.listdir("2xN/tests"):
        try:
            file = open("2xN/tests/" + filename, 'r')
            jobsData = json.loads(file.read())["jobs_data"]
            file.close()

            solver = Solver(jobsData)
            print(filename, "Optimal", solver.Solve()[1], "Google", GoogleSolve(jobsData))

        except Exception as ex:
            print(filename, "Skipped due to", ex)
            continue
