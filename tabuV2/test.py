import os
import json
import time
from tabu import *
from google_solver import *
import matplotlib.pyplot as plt
def visual(data: dict):
    #avg_value
    avg_on_machine = [[] for i in range(max(data.keys())+1)]
    for key in data.keys():
        avg_on_machine[key] = sum(data[key]) / len(data[key])
    while [] in avg_on_machine:
        avg_on_machine.remove([])
    plt.bar(data.keys(), avg_on_machine)
    plt.xlabel("machine No:") 
    plt.ylabel("makespan")
    plt.show()
    return
def num_last_mach(jobsdata):
    nm = 1
    for x in range(len(jobsdata)):
        for i in range(len(jobsdata[x])):
            nm = max(nm, jobsdata[x][i][0]+1)
    return nm
    
testsPath = "tests_for_graphics/"
if __name__ == "__main__":
    fileCount = len(os.listdir(testsPath))
    res = {}
    #каждому имени файла (х на графике, ключ в словаре)будем сопоставлять [google_res, tabu_res]
    for i in range(fileCount):
        # if i > 30: break

        filename = str(i) + ".json"

        try:
            file = open(testsPath + filename, 'r')
            jobsData = json.loads(file.read())["jobs_data"]
            machines = num_last_mach(jobsData)
            # print(machines)

            file.close()
            google = GoogleSolve(jobsData)
            if machines in res:
                res[machines].append(google)
            else:
                res[machines] = [google]
            print(filename, "Google: ", google)
            # tabu = TabuSearch(Solution.from_list(jobsData)).GetMakespan()
            # print("Tabu", tabu)

        except Exception as ex:
            print(filename, "Skipped due to", ex)
            continue

    visual(res)

















# import os
# import json

# from tabu import *
# from google_solver import *


# testsPath = "tests/"
# if __name__ == "__main__":
#     fileCount = len(os.listdir(testsPath))
#     for i in range(fileCount):
#         # if i > 16: break

#         filename = str(i) + ".json"

#         try:
#             file = open(testsPath + filename, 'r')
#             jobsData = json.loads(file.read())["jobs_data"]
#             file.close()

#             tabu = TabuSearch(Solution.from_list(jobsData)).GetMakespan()
#             print(filename, "Tabu", tabu, "Google", GoogleSolve(jobsData))

#         except Exception as ex:
#             print(filename, "Skipped due to", ex)
#             continue
