import random
from queue import Queue
# https://www.geeksforgeeks.org/what-is-tabu-search/

# задача:
#
# есть набор работ каждый из которых состоит из подзадач
# подзадача состоит из типа машины (CPU/GPU/..) на котором она может выполняться
# и вычислительной мощности требуемой для ее выполнения
#
# порядок выполнения важен
#
# цель - минимизировать makespan
#

class Task:
    def __init__(self, parent, type, power) -> None:
        self.parent = parent
        self.type = type
        self.power = power


class Job:
    def __init__(self, jobData) -> None:
        self.tasks = []
        self.progress = 0

        id, tasksList = jobData
        for type, power in tasksList:
            self.tasks.append(Task(id, type, power))


class Machine:
    def __init__(self, type : int, power : float) -> None:
        self.jobQueue = []
        self.power = power
        self.type = type


class Solution:
    def __init__(self, jsonData) -> None:
        # инициализируется случайным решением (пока что)

        machinesData = jsonData["machines_data"]

        self.machines = []
        return

    def GetMakespan(self) -> int:
        return 0

    def GetNeighbors(self) -> list: #[Solution]:
        neighbors = []
        return neighbors


def TabuSearch(iterations, tabuSetSize = 100000, initialSolution = Solution()):
    currentSolution = initialSolution
    bestSolution = currentSolution

    tabuSet = set()

    for _ in range(iterations):
        neighbors = currentSolution.GetNeighbors()
        bestNeighbor = None
        bestNeighborMakespan = float('inf')

        for neighbor in neighbors:
            if neighbor not in tabuSet:
                neighborMakespan = neighbor.GetMakespan()
                if neighborMakespan < bestNeighborMakespan:
                    bestNeighbor = neighbor
                    bestNeighborMakespan = neighborMakespan

        if bestNeighbor is None:
            print("No non-tabu neighbors found, terminate the search")
            break

        currentSolution = bestNeighbor
        tabuSet.add(bestNeighbor)

        if len(tabuSet) > tabuSetSize:
            tabuSet.pop()

        if bestNeighbor.GetMakespan() < bestSolution.GetMakespan:
            bestSolution = bestNeighbor

    return bestSolution


if __name__ == "__main__":
    bestSolution = TabuSearch(10)
